# 🏛️ KOSTRA AI Workbench & Financial Controlling Suite — Kristiansand Kommune

**AI-drevet avviksstyring, FAST & Power BI-Style Excel-modellering, ML-prognoser, tidsserieanalyser og automatisk revisjonskontroll**

KOSTRA AI Workbench er en produksjonsklar dataplattform og et helhetlig beslutningsstøttesystem utviklet for økonomiavdelingen, prosjekt-/økonomikontrollere og kommunedirektøren i Kristiansand kommune. Løsningen kombinerer en **Medallion Data Lakehouse-arkitektur** i DuckDB med maskinlæring (MLOps), et interaktivt **Streamlit-dashbord**, en **Power BI Semantic Model (`.pbip`)** og en **FAST-strukturert Excel-rapporteringsmodell (`Excel-Reporting-Analysis.xlsb`)**.

---

## 📋 Innholdsfortegnelse
1. [Prosjektarkitektur (Medallion & BI-Stack)](#-prosjektarkitektur-medallion--bi-stack)
2. [Hovedkomponenter & Moduler](#-hovedkomponenter--moduler)
3. [Excel Financial Modeling & Dashboard (FAST Standard)](#-excel-financial-modeling--dashboard-fast-standard)
4. [Mappe- og Filstruktur](#-mappe--og-filstruktur)
5. [Installasjon & Forutsetninger](#-installasjon--forutsetninger)
6. [Slik kjører du løsningen (A til Å)](#-slik-kjører-du-løsningen-a-til-å)
7. [ML-Modellportefølje & Algoritmer](#-ml-modellportefølje--algoritmer)
8. [Governance, Audit-logging & eInnsyn](#-governance-audit-logging--einnsyn)

---

## 📐 Prosjektarkitektur (Medallion & BI-Stack)

Databehandlingen bygger på en **3-lags Medallion-arkitektur** i DuckDB (`data/database/kostra_prod.duckdb`), som forsyner både Streamlit AI Workbench, Power BI og Excel Power Pivot (`ThisWorkbookDataModel`):

```text
┌────────────────────────────────────────────────────────────────────────┐
│                          RÅDATA (data/raw/*.csv)                       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Smart Ingestion & Kodepolstring
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│  BRONZE LAYER (stg_fact)                                               │
│  - Automatisk tegnsett-deteksjon (UTF-8, Latin1, CP1252)               │
│  - Kodepolstring (Konto: 4->6 siffer, Funksjon: 3->4/5 siffer)         │
│  - Renset for BOM-tegn og uønskede kildeavvik                          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ ISO-Datoer & LAG() Window Functions
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│  SILVER LAYER (silver_fact & vw_silver_snapshots)                      │
│  - Avstemt hovedbok over regnskapsperioder                             │
│  - Beregning av reelle månedlige nettotall (monthly_delta)             │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Feature Engineering (32 variabler)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│  GOLD LAYER (modelready_fact & Star Schema Dimensjoner)                │
│  1. Streamlit AI Workbench (src/app.py — 6 interaktive moduler)        │
│  2. Excel FAST & CUBE Workbook (Excel-Reporting-Analysis.xlsb)         │
│  3. Power BI Project (pbi-reporting-project.pbip / TMDL SemanticModel) │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🎛️ Hovedkomponenter & Moduler (`src/app.py`)

Streamlit-dashbordet (`src/app.py`) består av **6 interaktive moduler** designet for kommunal økonomistyring:

1. **📊 Avviksoversikt (Gold Layer):**
   * Månedlige og akkumulerte (YTD) sammenligninger av budsjett vs. regnskap.
   * Dynamiske filtere for perioder, rammeområder/sektorer og avviksstatus (🔴 / 🟡 / 🟢).
   * Grouped Bar Charts og trenddiagrammer via Plotly.

2. **📈 Tidsserie & Årsprognose (EAC / ETC):**
   * **Bokført YTD (Mnd 1–8):** Faktisk registrert forbruk.
   * **Projisert Q4 (Mnd 9–12):** Sesongkorrigert fremskriving (ETC) basert på 3-måneders rullende snitt og historiske sesongeffekter.
   * **EOY / EAC-Kalkyle (per 31.12):** Estimert årsresultat ved kalenderårets slutt.

3. **🌲 ML Prognoser & Early Warning (XAI):**
   * Forklarbar AI (XAI) som viser topp forklarende variabler (Feature Importance).
   * Early Warning-statusfordeling basert på Random Forest og Decision Tree.

4. **🚨 Anomaly Detection & Klyngeanalyse:**
   * **Hierarkisk Klustering (`hclust`):** Segmenterer kommunale avdelinger i 4 adferdsprofiler (*Stabil drift*, *Høyvolatil / Vikar*, *Sesong*, *Ekstraordinære avvik*).
   * **Isolation Forest & Z-Score:** Automatisk flagget sjekkliste for potensielle føringsfeil og bilagsavvik.

5. **⚙️ Modelready Datagrunnlag:**
   * Full forhåndsvisning og eksportmulighet av alle vaskede variabler i `modelready_fact`.

6. **💬 KI-Saksbehandler & Chatbot (RAG):**
   * Interaktiv KI-assistent som kombinerer oppslag i `modelready_fact` med Kommuneloven, KOSTRA-forskriften og kommunens økonomireglement.

---

## 📊 Excel Financial Modeling & Dashboard (`Excel-Reporting-Analysis.xlsb`)

Arbeidsboken `Excel-Reporting-Analysis.xlsb` (og `.xlsx`) er bygget etter **FAST-standarden** ([`excel.md`](excel.md)) og **Edward Tuftes Data-Ink Ratio**-prinsipper, koblet direkte til **Power Pivot (`ThisWorkbookDataModel`)** og 21 DAX-mål ([`DAX.md`](DAX.md)):

| Fane | Formål & Innhold |
| :--- | :--- |
| **`01_DASHBOARD`** | Koplingsfritt Power BI-style dashbord med `CUBEVALUE`/`CUBEMEMBER`-formler, sentralisert Slicer-panel (`År`, `Måned`, `KOSTRA Funksjon`, `Ansvarsenhet`), 6 avrundede KPI-kort, Sparklines (M1–M8), Combo Chart (Column + Line) og Bullet Chart. |
| **`02_OUTPUTS`** | Detaljerte finansielle oppstillinger: **Resultatoppstilling (Driftsregnskap & EAC)**, **Kontantstrømoppstilling** og **Balanseoppstilling** med full balanseavstemming (`0,00`). |
| **`03_CALCULATIONS`** | Beregningsmotor med én konsistent horisontal formel per rad (M1–M8 bokført + M9–M12 sesongjustert ETC/EAC-prognose) og CUBE-mellomstasjoner. |
| **`04_INPUTS`** | Dedikert parameterfane der alle hardkodede forutsetninger står i blå tekst (`#0000FF`) med globale navngitte områder (`Param_*`). |
| **`05_DATA_MODEL`** | Stjerneskjema-dokumentasjon og live avstemming av de 5 Power Query-tabellene (`modelready_fact`, `dim_date`, `dim_ansvar`, `dim_kostra_funksjon`, `dim_kostra_kontoplan`). |
| **`06_CHECKS`** | Sentral modellkontroll og feilsjekk (`CHK_01`–`CHK_11` + `MASTER_CHECK`) som verifiserer at samtlige differanser er `0,00`. |

---

## 📂 Mappe- og Filstruktur

```text
Kom - G2/
├── .env.example                        # Mal for miljøvariabler (kopieres til .env)
├── .gitignore                          # Git-ignoreringsregler for sikkerhet og tunge filer
├── Dockerfile                          # Container-definisjon for Streamlit & MLflow
├── docker-compose.yml                  # Multi-container orkestrering
├── requirements.txt                    # Python-avhengigheter
├── run.ps1                             # PowerShell CLI (-BuildDB, -Retrain, -Up, -Down, -All)
├── run_pipeline.bat                    # Batch-fil for helhetlig lokal kjøring (A til Å)
├── Excel-Reporting-Analysis.xlsb       # FAST & Power BI-Style Excel-modell (Binær)
├── Excel-Reporting-Analysis.xlsx       # FAST & Power BI-Style Excel-modell (OpenXML)
├── pbi-reporting-project.pbip          # Power BI Project (Git-vennlig TMDL-struktur)
├── pbi-reporting-project.Report/       # Power BI rapportdefinisjoner
├── pbi-reporting-project.SemanticModel/# Power BI semantisk modell (tabeller, relasjoner, DAX)
├── excel.md                            # Systemstandard for FAST & Power BI-Style Excel
├── DAX.md                              # DAX målkatalog for Power BI og Power Pivot
├── copilot.md                          # Standard for Python in Excel (=PY())
├── data/
│   ├── raw/                            # Inndatamappe for KOSTRA-CSV og dimensjonsfiler
│   ├── database/                       # Lokal DuckDB-database (ignoreres i Git, bygges av ETL)
│   └── export/                         # Automatisk genererte Ingestion- og Exception-rapporter
└── src/
    ├── app.py                          # Streamlit webapplikasjon og AI Workbench
    ├── canonical.py                    # Kanonisk datamodell og valideringsregler (Pydantic)
    ├── db_manager.py                   # DuckDB ETL, Medallion-pipeline og Audit Log
    └── retrain_pipeline.py             # Omtrening og evaluering av ML-modellene
```

---

## 🛠️ Installasjon & Forutsetninger

### Krav
* **Python:** v3.10 eller nyere (Python 3.11 / 3.12 anbefales)
* **Operativsystem:** Windows 10 / 11, macOS eller Linux

### Oppsett etter kloning fra GitHub
1. **Opprett og aktiver virtuelt miljø (valgfritt, men anbefalt):**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
2. **Installer Python-pakker:**
   ```powershell
   pip install -r requirements.txt
   ```
3. **Konfigurer miljøvariabler:**
   ```powershell
   Copy-Item .env.example .env
   ```

---

## 🚀 Slik kjører du løsningen (A til Å)

### Alternativ A: Automatisk kjøring via Batch-fil eller PowerShell
Kjør i PowerShell:
```powershell
.\run_pipeline.bat
# eller via PowerShell CLI:
.\run.ps1 -BuildDB -Retrain
```

### Alternativ B: Manuell kjøring steg-for-steg
1. **Bygg DuckDB-databasen fra rådata (`data/raw/`):**
   ```powershell
   python src/db_manager.py
   ```
2. **Kjør ML-omtrening og evaluering:**
   ```powershell
   python src/retrain_pipeline.py
   ```
3. **Start AI Workbench-dashbordet:**
   ```powershell
   streamlit run src/app.py
   ```

---

## 🤖 ML-Modellportefølje & Algoritmer

| Modell / Algoritme | Formål | Målvariabel / Ytelse |
| :--- | :--- | :--- |
| **Random Forest Regressor** | Prognostisere neste måneds regnskapsforbruk | $R^2 = 0.91$, Low MAE |
| **Decision Tree Classifier** | Generere revisjonsgodkjente IF-THEN regler for Early Warning | Status 0 (I RUTE), 1 (ADVARSEL), 2 (KRITISK) |
| **Agglomerative Clustering (`hclust`)** | Gruppere konti i 4 utgiftsprofiler | Unsupervised (4 klynger) |
| **Isolation Forest (`iforest`)** | Detektere føringsfeil og uvanlige beløpshopp | Top 5 % Z-score / avvikskontroll |

---

## 🛡️ Governance, Audit-logging & eInnsyn

I tråd med kommunale retningslinjer for kunstig intelligens og forvaltningsloven har systemet innebygd sporbarhet:

* **Uforanderlig Audit Log (`audit_log`):** Alle spørringer, avvikstiltak og AI-genererte anbefalinger logges automatisk i DuckDB med UUID, tidsstempel og bruker-ID.
* **Ingestion Report (`data/export/INGESTION_REPORT.md`):** Genereres automatisk ved hver kildedataimport og dokumenterer godkjente filer samt eventuelle filer lagt i karantene.

---
*Kristiansand kommune — KOSTRA AI Workbench © 2026*
