# -*- coding: utf-8 -*-
"""
ANTIGRAVITY KOSTRA — DYNAMISK EDA, RELASJONER OG TIDSSERIER (v1.0)
Exploratory Data Analysis Engine querying DuckDB modelready_fact
"""

import os
import duckdb
from typing import Dict, Any, List, Optional

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(BASE_DIR, "data", "database", "kostra_prod.duckdb")

ANSVAR_MAP = {
    "25310": {"name": "25310 - Omsorgssenter / Sykehjem A", "short": "Sykehjem A", "sektor": "Helse og Omsorg", "fn": "254"},
    "25320": {"name": "25320 - Omsorgssenter / Sykehjem B", "short": "Sykehjem B", "sektor": "Helse og Omsorg", "fn": "254"},
    "25710": {"name": "25710 - Hjemmetjenesten Sone Nord", "short": "Hjemmetj. Nord", "sektor": "Helse og Omsorg", "fn": "254"},
    "25720": {"name": "25720 - Hjemmetjenesten Sone Sør", "short": "Hjemmetj. Sør", "sektor": "Helse og Omsorg", "fn": "254"},
    "20210": {"name": "20210 - Grunnskole A (1–10 trinn)", "short": "Grunnskole A", "sektor": "Oppvekst og Utdanning", "fn": "202"},
    "20220": {"name": "20220 - Grunnskole B (1–10 trinn)", "short": "Grunnskole B", "sektor": "Oppvekst og Utdanning", "fn": "202"},
    "20230": {"name": "20230 - Grunnskole C (1–10 trinn)", "short": "Grunnskole C", "sektor": "Oppvekst og Utdanning", "fn": "202"},
    "21310": {"name": "21310 - Voksenopplæringssenter", "short": "Voksenoppl.", "sektor": "Oppvekst og Utdanning", "fn": "213"},
    "22110": {"name": "22110 - PPT og pedagogisk oppfølging", "short": "PPT Senter", "sektor": "Oppvekst og Utdanning", "fn": "221"},
}


def get_connection():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"DuckDB database not found at {DB_PATH}")
    return duckdb.connect(DB_PATH, read_only=True)


def parse_month_num(periode: Optional[str]) -> int:
    if not periode or periode.upper() in ["ALL", "HELE ÅRET"]:
        return 8
    clean = str(periode).strip().upper()
    if clean.startswith("M0") or clean.startswith("M"):
        try:
            return int(clean.replace("M0", "").replace("M", ""))
        except ValueError:
            pass
    elif "2024_" in clean:
        try:
            return int(clean.split("2024_")[-1])
        except ValueError:
            pass
    elif clean.isdigit():
        return int(clean)
    return 8


def get_dynamic_eda_analysis(filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Executes dynamic exploratory data analysis (EDA) across 4 tracks:
    - Spor A: Hierarkisk Nedbryting (Sektor -> Funksjon -> Ansvar -> Konto/Art)
    - Spor B: Utvikling Over Tid (Tidsserie, Sesongmønster & LOY-Progresjon)
    - Spor C: Årsak & Virkning (Lønnsarter: Fastlønn vs Vikar vs Overtid vs NAV)
    - Spor D: Relativ Sammenligning & Benchmarking (Peer-to-Peer Burn Rate)
    Plus automatic plain-Norwegian pedagogical narratives.
    """
    filters = filters or {}
    conn = get_connection()
    try:
        where_conditions = ["1=1"]
        params: List[Any] = []

        sektor = filters.get("sektor")
        if sektor and sektor not in ["ALL", "Alle Sektorer"]:
            where_conditions.append("sektor_navn = ?")
            params.append(sektor)

        ansvar = filters.get("ansvar")
        if ansvar and ansvar not in ["ALL", "Alle Ansvarssteder"]:
            where_conditions.append("ansvar_code = ?")
            params.append(ansvar)

        funksjon = filters.get("funksjon")
        if funksjon and funksjon not in ["ALL", "Alle"]:
            where_conditions.append("funksjon_code = ?")
            params.append(funksjon)

        rag_status = filters.get("rag_status")
        if rag_status and rag_status not in ["ALL", "Alle Statuser"]:
            if str(rag_status).isdigit():
                where_conditions.append("target_status_code = ?")
                params.append(int(rag_status))
            elif "KRITISK" in str(rag_status):
                where_conditions.append("target_status_code = 2")
            elif "ADVARSEL" in str(rag_status):
                where_conditions.append("target_status_code = 1")
            elif "RUTE" in str(rag_status):
                where_conditions.append("target_status_code = 0")

        base_where_sql = " AND ".join(where_conditions)
        m_num = parse_month_num(filters.get("periode"))

        # -------------------------------------------------------------
        # SPOR A: Hierarkisk Nedbryting (Funksjon -> Art)
        # -------------------------------------------------------------
        query_a_art = f"""
            SELECT 
                funksjon_code AS funksjon_kode,
                COALESCE(funksjon_navn, 'Uspesifisert') AS funksjon_navn,
                COALESCE(kostra_art_4siffer, konto_code) AS art_kode,
                COALESCE(kontonavn, 'Uspesifisert') AS art_navn,
                ansvar_code AS ansvar_kode,
                COALESCE(SUM(ytd_budsjett_nok), 0) AS budsjett,
                COALESCE(SUM(ytd_regnskap_nok), 0) AS regnskap,
                COALESCE(SUM(ytd_avvik_nok), 0) AS avvik_nok,
                ROUND((COALESCE(SUM(ytd_regnskap_nok), 0) / NULLIF(COALESCE(SUM(ytd_budsjett_nok), 0), 0)) * 100, 1) AS burn_rate
            FROM modelready_fact
            WHERE {base_where_sql} AND month = ?
            GROUP BY funksjon_code, funksjon_navn, kostra_art_4siffer, konto_code, kontonavn, ansvar_code
            ORDER BY ABS(avvik_nok) DESC
        """
        rows_a_art = conn.execute(query_a_art, params + [m_num]).fetchall()
        hierarchy_art = []
        for r in rows_a_art:
            hierarchy_art.append({
                "funksjon_kode": str(r[0]),
                "funksjon_navn": str(r[1]),
                "art_kode": str(r[2]),
                "art_navn": str(r[3]),
                "ansvar_kode": str(r[4]),
                "budsjett": round(float(r[5]), 2),
                "regnskap": round(float(r[6]), 2),
                "avvik_nok": round(float(r[7]), 2),
                "burn_rate": float(r[8]) if r[8] is not None else (100.0 if r[6] == 0 else 135.0)
            })

        # Aggregated by funksjon
        query_a_fn = f"""
            SELECT 
                funksjon_code AS funksjon_kode,
                COALESCE(funksjon_navn, 'Uspesifisert') AS funksjon_navn,
                COALESCE(SUM(ytd_budsjett_nok), 0) AS budsjett,
                COALESCE(SUM(ytd_regnskap_nok), 0) AS regnskap,
                COALESCE(SUM(ytd_avvik_nok), 0) AS avvik_nok,
                ROUND((COALESCE(SUM(ytd_regnskap_nok), 0) / NULLIF(COALESCE(SUM(ytd_budsjett_nok), 0), 0)) * 100, 1) AS burn_rate
            FROM modelready_fact
            WHERE {base_where_sql} AND month = ?
            GROUP BY funksjon_code, funksjon_navn
            ORDER BY ABS(avvik_nok) DESC
        """
        rows_a_fn = conn.execute(query_a_fn, params + [m_num]).fetchall()
        hierarchy_fn = []
        for r in rows_a_fn:
            hierarchy_fn.append({
                "funksjon_kode": str(r[0]),
                "funksjon_navn": str(r[1]),
                "budsjett": round(float(r[2]), 2),
                "regnskap": round(float(r[3]), 2),
                "avvik_nok": round(float(r[4]), 2),
                "burn_rate": float(r[5]) if r[5] is not None else 100.0
            })

        # -------------------------------------------------------------
        # SPOR B: Utvikling Over Tid (Tidsserie M01-M08 + LOY M09-M12)
        # -------------------------------------------------------------
        query_b = f"""
            SELECT 
                month,
                COALESCE(SUM(monthly_delta_regnskap_nok), 0) AS maaned_regnskap,
                COALESCE(SUM(monthly_delta_budsjett_nok), 0) AS maaned_budsjett,
                COALESCE(SUM(monthly_delta_regnskap_nok - monthly_delta_budsjett_nok), 0) AS maaned_avvik,
                COALESCE(SUM(ytd_regnskap_nok), 0) AS akkumulert_regnskap,
                COALESCE(SUM(ytd_budsjett_nok), 0) AS akkumulert_budsjett,
                COALESCE(SUM(ytd_avvik_nok), 0) AS akkumulert_avvik
            FROM modelready_fact
            WHERE {base_where_sql}
            GROUP BY month
            ORDER BY month ASC
        """
        rows_b = conn.execute(query_b, params).fetchall()
        trend = []
        month_names = ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Des"]
        
        last_3m_reg = []
        last_m_reg = 0.0
        last_m_bud = 0.0
        cum_reg = 0.0
        cum_bud = 0.0

        for r in rows_b:
            m = int(r[0])
            m_reg = round(float(r[1]), 2)
            m_bud = round(float(r[2]), 2)
            m_avvik = round(float(r[3]), 2)
            cum_reg = round(float(r[4]), 2)
            cum_bud = round(float(r[5]), 2)
            cum_avvik = round(float(r[6]), 2)
            
            trend.append({
                "periode": f"M{m:02d}",
                "label": f"{month_names[m-1]} 2024",
                "month": m,
                "maaned_regnskap": m_reg,
                "maaned_budsjett": m_bud,
                "maaned_avvik": m_avvik,
                "akkumulert_regnskap": cum_reg,
                "akkumulert_budsjett": cum_bud,
                "akkumulert_avvik": cum_avvik,
                "is_projection": False
            })
            if m in [6, 7, 8]:
                last_3m_reg.append(m_reg)
            last_m_reg = m_reg
            last_m_bud = m_bud

        # Calculate run-rate for projection (M09-M12)
        rolling_3m_avg = sum(last_3m_reg) / len(last_3m_reg) if last_3m_reg else last_m_reg
        seasonal_factors = {9: 1.00, 10: 1.02, 11: 1.05, 12: 1.10} # Year-end seasonal factor
        
        proj_reg_total = cum_reg
        proj_bud_total = cum_bud

        for m_proj in range(9, 13):
            factor = seasonal_factors.get(m_proj, 1.0)
            proj_m_reg = round(rolling_3m_avg * factor, 2)
            proj_m_bud = last_m_bud # Estimated monthly budget
            proj_reg_total += proj_m_reg
            proj_bud_total += proj_m_bud
            
            trend.append({
                "periode": f"M{m_proj:02d}",
                "label": f"{month_names[m_proj-1]} (LOY)",
                "month": m_proj,
                "maaned_regnskap": proj_m_reg,
                "maaned_budsjett": proj_m_bud,
                "maaned_avvik": round(proj_m_reg - proj_m_bud, 2),
                "akkumulert_regnskap": round(proj_reg_total, 2),
                "akkumulert_budsjett": round(proj_bud_total, 2),
                "akkumulert_avvik": round(proj_reg_total - proj_bud_total, 2),
                "is_projection": True
            })

        # -------------------------------------------------------------
        # SPOR C: Årsak & Virkning (Lønnsarter: Fastlønn, Vikar, Overtid, NAV)
        # -------------------------------------------------------------
        query_c = f"""
            SELECT 
                COALESCE(SUM(CASE WHEN kostra_art_4siffer LIKE '101%' THEN ytd_avvik_nok ELSE 0 END), 0) AS fastlonn_avvik,
                COALESCE(SUM(CASE WHEN kostra_art_4siffer LIKE '102%' OR kostra_art_4siffer LIKE '127%' THEN ytd_avvik_nok ELSE 0 END), 0) AS vikar_avvik,
                COALESCE(SUM(CASE WHEN kostra_art_4siffer LIKE '104%' THEN ytd_avvik_nok ELSE 0 END), 0) AS overtid_avvik,
                COALESCE(SUM(CASE WHEN kostra_art_4siffer LIKE '171%' THEN ytd_avvik_nok ELSE 0 END), 0) AS nav_refusjon_avvik,
                COALESCE(SUM(CASE WHEN kostra_art_4siffer LIKE '109%' THEN ytd_avvik_nok ELSE 0 END), 0) AS helgetillegg_avvik
            FROM modelready_fact
            WHERE {base_where_sql} AND month = ?
        """
        row_c = conn.execute(query_c, params + [m_num]).fetchone()
        fastlonn_avvik = round(float(row_c[0]) if row_c else 0.0, 2)
        vikar_avvik = round(float(row_c[1]) if row_c else 0.0, 2)
        overtid_avvik = round(float(row_c[2]) if row_c else 0.0, 2)
        nav_refusjon_avvik = round(float(row_c[3]) if row_c else 0.0, 2)
        helgetillegg_avvik = round(float(row_c[4]) if row_c else 0.0, 2)
        netto_substitusjon = round(fastlonn_avvik + vikar_avvik, 2)

        payroll_relations = {
            "fastlonn_avvik": fastlonn_avvik,
            "vikar_avvik": vikar_avvik,
            "overtid_avvik": overtid_avvik,
            "nav_refusjon_avvik": nav_refusjon_avvik,
            "helgetillegg_avvik": helgetillegg_avvik,
            "netto_substitusjon": netto_substitusjon,
            "total_lonnsavvik": round(fastlonn_avvik + vikar_avvik + overtid_avvik + nav_refusjon_avvik, 2)
        }

        # -------------------------------------------------------------
        # SPOR D: Relativ Sammenligning & Benchmarking (Peer-to-Peer)
        # -------------------------------------------------------------
        query_d = f"""
            SELECT 
                ansvar_code,
                COALESCE(SUM(ytd_budsjett_nok), 0) AS budsjett,
                COALESCE(SUM(ytd_regnskap_nok), 0) AS regnskap,
                COALESCE(SUM(ytd_avvik_nok), 0) AS avvik_nok,
                ROUND((COALESCE(SUM(ytd_regnskap_nok), 0) / NULLIF(COALESCE(SUM(ytd_budsjett_nok), 0), 0)) * 100, 1) AS burn_rate_pct
            FROM modelready_fact
            WHERE {base_where_sql} AND month = ?
            GROUP BY ansvar_code
            ORDER BY burn_rate_pct DESC
        """
        rows_d = conn.execute(query_d, params + [m_num]).fetchall()
        peers = []
        for r in rows_d:
            c = str(r[0])
            meta = ANSVAR_MAP.get(c, {"name": f"Ansvar {c}", "short": c, "sektor": "Uspesifisert"})
            peers.append({
                "ansvar_kode": c,
                "navn": meta["name"],
                "kortnavn": meta["short"],
                "sektor": meta["sektor"],
                "budsjett": round(float(r[1]), 2),
                "regnskap": round(float(r[2]), 2),
                "avvik_nok": round(float(r[3]), 2),
                "burn_rate_pct": float(r[4]) if r[4] is not None else 100.0
            })

        # -------------------------------------------------------------
        # NARRATIVE GENERATION (INSIKT PÅ NORSK UTEN DATA-SCIENCE-SJARGONG)
        # -------------------------------------------------------------
        # Narrative Spor A
        tot_avvik = sum(abs(x["avvik_nok"]) for x in hierarchy_fn)
        top_fn = hierarchy_fn[0] if hierarchy_fn else None
        fn_pct = round((abs(top_fn["avvik_nok"]) / tot_avvik * 100), 1) if (top_fn and tot_avvik > 0) else 0
        top_art = hierarchy_art[0] if hierarchy_art else None
        narrative_a = (
            f"Innenfor valgt utvalg står funksjon {top_fn['funksjon_kode']} {top_fn['funksjon_navn']} for {fn_pct} % "
            f"av det samlede avviket. Dypdykk viser at den største driveren er art {top_art['art_kode']} "
            f"({top_art['art_navn']}) med et avvik på {top_art['avvik_nok']:,.0f} kr."
            if (top_fn and top_art) else "Ingen vesentlige avvik identifisert i hierarkiet."
        )

        # Narrative Spor B
        q1_avg = sum(t["maaned_regnskap"] for t in trend[:3]) / 3 if len(trend) >= 3 else 1
        summer_avg = sum(t["maaned_regnskap"] for t in trend[5:7]) / 2 if len(trend) >= 7 else q1_avg
        growth_pct = round(((summer_avg - q1_avg) / q1_avg) * 100, 1) if q1_avg > 0 else 0
        projected_eoy_var = trend[-1]["akkumulert_avvik"] if trend else 0
        narrative_b = (
            f"Regnskapet for valgt utvalg viser stabil drift i Q1 (Jan–Mar), men fikk en kostnadsvekst på {growth_pct:+.1f} % "
            f"i juni og juli. Hvis denne månedstakten fortsetter ut året, vil helårsavviket (LOY) lande på {projected_eoy_var:,.0f} kr."
        )

        # Narrative Spor C
        if vikar_avvik > 0 and fastlonn_avvik <= 0:
            narrative_c = (
                f"Det er en klar sammenheng i dette utvalget: Mindreforbruk på fast lønn (art 1010) på {fastlonn_avvik:,.0f} kr "
                f"har ført til et merforbruk på vikarer (art 1020/1270) på +{vikar_avvik:,.0f} kr. "
                f"Netto merkostnad ved bruk av vikarer fremfor faste ansettelser er +{netto_substitusjon:,.0f} kr."
            )
        elif vikar_avvik > 0 and overtid_avvik > 0:
            narrative_c = (
                f"Sterkt press på bemanningsressurser: Både vikarbruk (+{vikar_avvik:,.0f} kr) og overtid (+{overtid_avvik:,.0f} kr) "
                f"overskrider budsjett. Samlet bemanningsavvik utgjør +{(vikar_avvik + overtid_avvik):,.0f} kr."
            )
        else:
            narrative_c = (
                f"Lønnsavviket er moderat: Fastlønn {fastlonn_avvik:,.0f} kr, vikarer {vikar_avvik:,.0f} kr "
                f"og overtid {overtid_avvik:,.0f} kr. NAV-refusjoner utgjør {nav_refusjon_avvik:,.0f} kr."
            )

        # Narrative Spor D
        if peers:
            highest_peer = peers[0]
            lowest_peer = peers[-1]
            avg_burn = round(sum(p["burn_rate_pct"] for p in peers) / len(peers), 1)
            sektor_navn = filters.get("sektor", "utvalget")
            narrative_d = (
                f"Blant alle {len(peers)} enheter i {sektor_navn} har {highest_peer['kortnavn']} den høyeste "
                f"forbruksintensiteten ({highest_peer['burn_rate_pct']:.1f} % Burn Rate), mens {lowest_peer['kortnavn']} "
                f"har lavest ({lowest_peer['burn_rate_pct']:.1f} % Burn Rate). Gjennomsnittet ligger på {avg_burn:.1f} %."
            )
        else:
            narrative_d = "Ingen enheter tilgjengelig for benchmarking i valgt utsnitt."

        # Overall synthesis
        overall_narrative = (
            f"{narrative_a} {narrative_c}"
        )

        return {
            "status": "ok",
            "filters": {
                "periode": filters.get("periode", "ALL"),
                "sektor": filters.get("sektor", "ALL"),
                "ansvar": filters.get("ansvar", "ALL"),
                "funksjon": filters.get("funksjon", "ALL"),
                "rag_status": filters.get("rag_status", "ALL")
            },
            "spor_a_hierarchy": {
                "by_function": hierarchy_fn,
                "by_art": hierarchy_art[:20]
            },
            "spor_b_trend": trend,
            "spor_c_payroll": payroll_relations,
            "spor_d_peers": peers,
            "narratives": {
                "overall": overall_narrative,
                "spor_a": narrative_a,
                "spor_b": narrative_b,
                "spor_c": narrative_c,
                "spor_d": narrative_d
            }
        }
    finally:
        conn.close()

