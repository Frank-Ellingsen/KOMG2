import os
import glob
import json
import uuid
import duckdb
import pandas as pd
from datetime import datetime

class DuckDBManager:
    def __init__(self, db_path: str = "data/database/kostra_prod.duckdb", raw_dir: str = "data/raw", export_dir: str = "data/export"):
        self.db_path = db_path
        self.raw_dir = raw_dir
        self.export_dir = export_dir
        os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
        os.makedirs(self.export_dir, exist_ok=True)

    def get_connection(self):
        return duckdb.connect(self.db_path)

    def _safe_read_file(self, file_path: str) -> pd.DataFrame:
        """Leser CSV- eller Excel-filer med automatisk tegnsett-deteksjon (UTF-8 / Latin1 / CP1252)."""
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        
        for enc in ['utf-8-sig', 'utf-8', 'latin1', 'cp1252']:
            try:
                return pd.read_csv(file_path, encoding=enc)
            except Exception:
                continue
        return pd.read_csv(file_path, encoding='latin1', on_bad_lines='skip')

    def _normalize_and_classify(self, df: pd.DataFrame, filename: str):
        """
        Gjennomfører dynamisk kolonnenormalisering:
        - Fjerner usynlige BOM-tegn (ï»¿, \ufeff).
        - Standardiserer alle datoer til ISO-format (YYYY-MM-DD).
        - Polstrer koder: 4-sifret kontokode fylles med '00' til 6-sifret, 3-sifret funksjon fylles med '00'.
        - Sletter kilde-avvik/differanser slik at avvik kun beregnes i SQL.
        - Klassifiserer filen som enten Dimensjon, Fakta eller Karantene.
        """
        filename_lower = filename.lower()
        
        # 1. Rens alle kolonnenavn for BOM og usynlige tegn
        df.columns = [str(c).replace('\ufeff', '').replace('ï»¿', '').strip() for c in df.columns]
        
        # Sjekk om dette er en eksplisitt dimensjonstabell
        is_explicit_dim = filename_lower.startswith('dim_') or any(x in filename_lower for x in ['ansvarsstruktur', 'kontoplan', 'funksjonsstruktur', 'sikkerhet'])
        has_text_descriptions = any(any(x in str(c).lower() for x in ['navn', 'beskrivelse', 'enhet', 'tittel']) for c in df.columns)
        has_financial_measures = any(any(x in str(c).lower() for x in ['budsjett', 'regnskap', 'belop', 'beløp', 'kostnad', 'utgift', 'påløpt', 'sum']) for c in df.columns)

        if is_explicit_dim or (has_text_descriptions and not has_financial_measures):
            return "DIMENSION", df, "Dimensjonstabell"

        # 2. Slett eventuelle kilde-avvikskolonner (Avvik, Varians, Diff)
        cols_to_drop = []
        for col in df.columns:
            c_lower = col.lower()
            if any(x in c_lower for x in ['avvik', 'differanse', 'varians', 'merforbruk', 'mindreforbruk']) and not any(x in c_lower for x in ['navn', 'beskrivelse', 'gruppe']):
                cols_to_drop.append(col)
        
        if cols_to_drop:
            df = df.drop(columns=cols_to_drop)

        # 3. Mapp kjerne-kolonner dynamisk for FAKTAFILER
        rename_dict = {}
        for col in df.columns:
            c = col.lower().strip()
            
            # KOSTRA Funksjon
            if any(x in c for x in ['funksjon', 'tjeneste']) and not any(x in c for x in ['navn', 'gruppe', 'beskrivelse', 'tekst', 'omrade', 'ansvarsstruktur']):
                rename_dict[col] = 'Funksjon'
            # KOSTRA Kontokode / Art
            elif any(x in c for x in ['kontokode', 'konto', 'art']) and not any(x in c for x in ['navn', 'gruppe', 'klasse', 'kategori', 'beskrivelse', 'regel']):
                rename_dict[col] = 'Kontokode_6Siffer'
            # Budsjett
            elif any(x in c for x in ['budsjett', 'ramme']):
                rename_dict[col] = 'Budsjett'
            # Regnskap / Beløp / Kostnad
            elif any(x in c for x in ['regnskap', 'belop', 'beløp', 'kostnad', 'utgift', 'påløpt', 'sum']):
                rename_dict[col] = 'Regnskap'
            # Dato / Periode
            elif any(x in c for x in ['dato', 'date', 'periode', 'maaned', 'måned', 'aar', 'år']):
                rename_dict[col] = 'Dato'

        df_mapped = df.rename(columns=rename_dict)
        mapped_cols = list(df_mapped.columns)

        # 4. Valider Minimumskrav for Faktafiler
        has_measures = any(c in mapped_cols for c in ['Budsjett', 'Regnskap'])
        if not has_measures:
            return "QUARANTINE", None, "Ingen gjenkjennbare beløpskolonner (Budsjett, Regnskap, Beløp eller Kostnad)"

        has_funksjon = 'Funksjon' in mapped_cols
        has_konto = 'Kontokode_6Siffer' in mapped_cols

        if not has_funksjon and not has_konto:
            return "QUARANTINE", None, "Mangler både KOSTRA Funksjon og Kontokode/Art"

        # 5. STANDARDISE DATOFORMAT TIL ISO YYYY-MM-DD
        if 'Dato' in df_mapped.columns:
            try:
                df_mapped['Dato'] = pd.to_datetime(df_mapped['Dato'], errors='coerce').dt.strftime('%Y-%m-%d')
            except Exception:
                pass

        # 6. KODE-POLSTRINGSREGLER (Padding / Fill Rules)
        # Hvis 6-sifret kontokode er 4-sifret (f.eks. 1010), fyll ut med '00' -> 101000
        if has_konto:
            def pad_konto(val):
                if pd.isna(val) or str(val).strip() == '' or str(val).strip().lower() in ['nan', 'none', 'null']:
                    return '999999'
                s = str(val).strip().split('.')[0]
                if len(s) == 4 and s.isdigit():
                    return s + '00'
                elif len(s) == 3 and s.isdigit():
                    return '0' + s + '00'
                elif len(s) < 6 and s.isdigit():
                    return s.ljust(6, '0')
                return s
            df_mapped['Kontokode_6Siffer'] = df_mapped['Kontokode_6Siffer'].apply(pad_konto)
        else:
            df_mapped['Kontokode_6Siffer'] = '999999'

        # Hvis Funksjon er 3-sifret (f.eks. 202 eller 254), fyll ut med '00' -> 20200
        if has_funksjon:
            def pad_funksjon(val):
                if pd.isna(val) or str(val).strip() == '' or str(val).strip().lower() in ['nan', 'none', 'null']:
                    return '9999'
                s = str(val).strip().split('.')[0]
                if len(s) == 3 and s.isdigit():
                    return s + '00'
                elif len(s) < 4 and s.isdigit():
                    return s.ljust(4, '0')
                return s
            df_mapped['Funksjon'] = df_mapped['Funksjon'].apply(pad_funksjon)
        else:
            df_mapped['Funksjon'] = '9999'

        # Sørg for at Budsjett og Regnskap finnes med standardverdi 0.0
        category = "Budsjett & Regnskap"
        if 'Budsjett' not in df_mapped.columns:
            df_mapped['Budsjett'] = 0.0
            category = "Regnskap"
        if 'Regnskap' not in df_mapped.columns:
            df_mapped['Regnskap'] = 0.0
            category = "Budsjett"

        df_mapped['source_file'] = filename
        return "FACT", df_mapped, category

    def build_from_raw(self):
        """
        Skanner DYNAMISK alle filer i data/raw uavhengig av filnavn og feltnavn:
        - Oppretter kun 'stg_fact' som samlet fakta-tabell i DuckDB.
        - Standardiserer alle datoer til YYYY-MM-DD.
        - Fyller ut manglende kontokoder (4 siffer + '00') og funksjonskoder (3 siffer + '00').
        - Genererer automatisk Ingestion & Exception Report.
        """
        conn = self.get_connection()
        
        # Slett gjenstående komskole-oblikk
        conn.execute("DROP VIEW IF EXISTS stg_fact_komskole;")
        conn.execute("DROP TABLE IF EXISTS stg_fact_komskole;")
        
        raw_files = []
        for ext in ['*.csv', '*.xlsx', '*.xls']:
            raw_files.extend(glob.glob(os.path.join(self.raw_dir, ext)))

        report = {
            "timestamp": datetime.now().isoformat(),
            "scanned_files_count": len(raw_files),
            "imported_fact_files": [],
            "imported_dim_files": [],
            "quarantined_files": []
        }

        if not raw_files:
            print(f"⚠️ Ingen filer funnet i: {os.path.abspath(self.raw_dir)}")
            conn.close()
            return report

        print(f"🔍 Starter Smart Ingestion-analyse av {len(raw_files)} filer...")

        fact_dfs = []

        for file_path in raw_files:
            filename = os.path.basename(file_path)

            try:
                df_raw = self._safe_read_file(file_path)
                if df_raw.empty:
                    report["quarantined_files"].append({
                        "filename": filename,
                        "reason": "Filen er tom"
                    })
                    print(f"  [❌ Avvist] {filename}: Filen er tom")
                    continue

                file_type, processed_df, detail = self._normalize_and_classify(df_raw, filename)

                if file_type == "FACT":
                    fact_dfs.append(processed_df)
                    report["imported_fact_files"].append({
                        "filename": filename,
                        "category": detail,
                        "rows": len(processed_df),
                        "preserved_columns": list(processed_df.columns)
                    })
                    print(f"  [📊 Fakta - {detail}] {filename} -> Godkjent! {len(processed_df)} rader, {len(processed_df.columns)} kolonner bevart.")

                elif file_type == "DIMENSION":
                    table_name = os.path.splitext(filename)[0]
                    table_name_clean = "".join([c if c.isalnum() or c == '_' else '_' for c in table_name])
                    conn.execute(f'CREATE OR REPLACE TABLE "{table_name_clean}" AS SELECT * FROM processed_df')
                    report["imported_dim_files"].append({
                        "filename": filename,
                        "table_name": table_name_clean,
                        "rows": len(processed_df),
                        "columns": list(processed_df.columns)
                    })
                    print(f"  [📑 Dimensjon] {filename} -> Importert med {len(processed_df.columns)} kolonner.")

                else:
                    report["quarantined_files"].append({
                        "filename": filename,
                        "reason": f"Mangler minimumsfelter -> {detail}"
                    })
                    print(f"  [❌ Avvist] {filename}: Mangler minimumsfelter -> {detail}")

            except Exception as e:
                report["quarantined_files"].append({
                    "filename": filename,
                    "reason": f"Kritisk innlesingsfeil: {str(e)}"
                })
                print(f"  [💥 Feil] {filename}: {e}")

        # 1. Last inn samlet fakta-tabell i DuckDB kun som 'stg_fact'
        if fact_dfs:
            combined_fact_df = pd.concat(fact_dfs, ignore_index=True)
            conn.execute("CREATE OR REPLACE TABLE stg_fact AS SELECT * FROM combined_fact_df")
            total_fact_rows = len(combined_fact_df)
            print(f"✅ Importerte totalt {total_fact_rows} rader fra {len(fact_dfs)} faktafiler til DuckDB-tabellen 'stg_fact'!")

        # 2. Opprett Audit Log
        conn.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                log_id VARCHAR PRIMARY KEY,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id VARCHAR,
                query_text VARCHAR,
                sektor_funksjon VARCHAR,
                avvik_belop_nok DOUBLE,
                rag_context VARCHAR,
                recommended_action VARCHAR,
                serper_used BOOLEAN,
                model_version VARCHAR
            );
        """)

        # 3. Opprett analytisk avviksview mot 'stg_fact'
        tables_res = conn.execute("SHOW TABLES").fetchall()
        existing_tables = [t[0] for t in tables_res]

        has_dim_funks = 'dim_kostra_funksjon' in existing_tables
        has_dim_konto = 'dim_kostra_kontoplan' in existing_tables

        funks_id_col = "KOSTRA_Funksjon_ID"
        funks_navn_col = "KOSTRA_Funksjon_Navn"
        if has_dim_funks:
            funks_cols = [c[1] for c in conn.execute("PRAGMA table_info('dim_kostra_funksjon')").fetchall()]
            if "KOSTRA_Funksjon_ID" in funks_cols:
                funks_id_col = "KOSTRA_Funksjon_ID"
            elif "Funksjon" in funks_cols:
                funks_id_col = "Funksjon"
            if "KOSTRA_Funksjon_Navn" in funks_cols:
                funks_navn_col = "KOSTRA_Funksjon_Navn"
            elif "Funksjonsnavn" in funks_cols:
                funks_navn_col = "Funksjonsnavn"

        konto_id_col = "Kontokode_6Siffer"
        konto_navn_col = "Kontonavn"
        if has_dim_konto:
            konto_cols = [c[1] for c in conn.execute("PRAGMA table_info('dim_kostra_kontoplan')").fetchall()]
            if "Kontokode_6Siffer" in konto_cols:
                konto_id_col = "Kontokode_6Siffer"
            elif "Kontokode" in konto_cols:
                konto_id_col = "Kontokode"
            if "Kontonavn" in konto_cols:
                konto_navn_col = "Kontonavn"

        join_funks = f"LEFT JOIN dim_kostra_funksjon df ON CAST(f.Funksjon AS VARCHAR) = CAST(df.{funks_id_col} AS VARCHAR) OR SUBSTR(CAST(f.Funksjon AS VARCHAR), 1, 3) = CAST(df.{funks_id_col} AS VARCHAR)" if has_dim_funks else ""
        join_konto = f"LEFT JOIN dim_kostra_kontoplan dk ON CAST(f.Kontokode_6Siffer AS VARCHAR) = CAST(dk.{konto_id_col} AS VARCHAR)" if has_dim_konto else ""

        select_funks_navn = f"COALESCE(df.{funks_navn_col}, CAST(f.Funksjon AS VARCHAR))" if has_dim_funks else "CAST(f.Funksjon AS VARCHAR)"
        select_konto_navn = f"COALESCE(dk.{konto_navn_col}, CAST(f.Kontokode_6Siffer AS VARCHAR))" if has_dim_konto else "CAST(f.Kontokode_6Siffer AS VARCHAR)"

        conn.execute(f"""
            CREATE OR REPLACE VIEW vw_avvik_summary AS
            SELECT 
                CAST(f.Funksjon AS VARCHAR) AS Funksjon_Kode,
                {select_funks_navn} AS KOSTRA_Funksjon_Navn,
                CAST(f.Kontokode_6Siffer AS VARCHAR) AS Kontokode_6Siffer,
                {select_konto_navn} AS Kontonavn,
                SUM(COALESCE(f.Budsjett, 0.0)) AS Sum_Budsjett,
                SUM(COALESCE(f.Regnskap, 0.0)) AS Sum_Regnskap,
                (SUM(COALESCE(f.Regnskap, 0.0)) - SUM(COALESCE(f.Budsjett, 0.0))) AS Avvik_Kr,
                CASE 
                    WHEN (SUM(COALESCE(f.Regnskap, 0.0)) - SUM(COALESCE(f.Budsjett, 0.0))) < -500000 THEN '🔴 KRITISK AVVIK'
                    WHEN (SUM(COALESCE(f.Regnskap, 0.0)) - SUM(COALESCE(f.Budsjett, 0.0))) < 0 THEN '🟡 ADVARSEL'
                    ELSE '🟢 I RUTE'
                END AS Status_Indikator
            FROM stg_fact f
            {join_funks}
            {join_konto}
            GROUP BY f.Funksjon, {select_funks_navn}, f.Kontokode_6Siffer, {select_konto_navn}
            ORDER BY Avvik_Kr ASC;
        """)

        conn.close()

        # 4. Generer Ingestion Report (JSON & Markdown)
        self._write_reports(report)
        return report

    def _write_reports(self, report: dict):
        json_path = os.path.join(self.export_dir, "ingestion_report.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        md_path = os.path.join(self.export_dir, "INGESTION_REPORT.md")
        md_content = [
            "# 📊 KOSTRA AI Workbench — Ingestion & Exception Report",
            f"**Generert:** {report['timestamp']}  ",
            f"**Totalt skannede filer:** {report['scanned_files_count']}\n",
            "---",
            "## ✅ Godkjente og Importerte Faktafiler (stg_fact)",
            "| Filnavn | Kategori | Rader | Bevarte Kolonner |",
            "| :--- | :--- | :--- | :--- |"
        ]

        if report["imported_fact_files"]:
            for item in report["imported_fact_files"]:
                cols_str = ", ".join(item['preserved_columns'][:4]) + ("..." if len(item['preserved_columns']) > 4 else "")
                md_content.append(f"| `{item['filename']}` | **{item['category']}** | {item['rows']} | {cols_str} |")
        else:
            md_content.append("| _Ingen faktafiler importert_ | - | - | - |")

        md_content.extend([
            "\n## 📑 Importerte Dimensjonstabeller",
            "| Filnavn | Tabellnavn i DuckDB | Rader | Antall Kolonner |",
            "| :--- | :--- | :--- | :--- |"
        ])

        if report["imported_dim_files"]:
            for item in report["imported_dim_files"]:
                md_content.append(f"| `{item['filename']}` | `{item['table_name']}` | {item['rows']} | {len(item['columns'])} |")
        else:
            md_content.append("| _Ingen dimensjonstabeller importert_ | - | - | - |")

        md_content.extend([
            "\n---",
            "## ⚠️ Karantene & Avviste Filer (Exception Log)",
            "| Filnavn | Årsak til Avvisning |",
            "| :--- | :--- |"
        ])

        if report["quarantined_files"]:
            for item in report["quarantined_files"]:
                md_content.append(f"| ❌ `{item['filename']}` | <font color='red'>{item['reason']}</font> |")
        else:
            md_content.append("| _Ingen filer lagt i karantene (100 % suksess)_ | - |")

        with open(md_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(md_content))

        print(f"📄 Rapport lagret: {md_path}")

    def get_top_avvik_df(self, limit: int = 10) -> pd.DataFrame:
        conn = self.get_connection()
        df = conn.execute(f"SELECT * FROM vw_avvik_summary LIMIT {limit};").fetchdf()
        conn.close()
        return df

    def log_audit_event(self, **kwargs) -> str:
        conn = self.get_connection()
        log_id = "LOG-" + str(uuid.uuid4())
        conn.execute("""
            INSERT INTO audit_log (log_id, user_id, query_text, sektor_funksjon, avvik_belop_nok, rag_context, recommended_action, serper_used, model_version)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """, (
            log_id,
            kwargs.get("user_id", "system"),
            kwargs.get("query_text", ""),
            kwargs.get("sektor_funksjon", ""),
            kwargs.get("avvik_belop_nok", 0.0),
            kwargs.get("rag_context", ""),
            kwargs.get("recommended_action", ""),
            kwargs.get("serper_used", False),
            kwargs.get("model_version", "gemini-1.5-flash")
        ))
        conn.close()
        return log_id

if __name__ == "__main__":
    db = DuckDBManager()
    db.build_from_raw()
