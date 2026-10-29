# 🏛️ KOSTRA AI Workbench & Financial Controlling Suite — Kristiansand Kommune

**AI-drevet avviksstyring, Workflow Pipeline Cockpit, FAST & Power BI-Style Excel-modellering, ML-prognoser, tidsserieanalyser og automatisk revisjonskontroll**

KOSTRA AI Workbench er en produksjonsklar dataplattform og et helhetlig beslutningsstøttesystem utviklet for økonomiavdelingen, prosjekt-/økonomikontrollere og kommunedirektøren i Kristiansand kommune. Løsningen kombinerer en **Medallion Data Lakehouse-arkitektur** i DuckDB med maskinlæring (MLOps), et interaktivt **Streamlit-dashbord (`src/app.py`)**, et frittstående **HTML5/Tufte Web-UI (`index.html`)** med **Cockpit Pipeline Kontroll**, en **Power BI Semantic Model (`.pbip`)** og en **FAST-strukturert Excel-rapporteringsmodell (`Excel-Reporting-Analysis.xlsb`)**.

---

## 📋 Innholdsfortegnelse
1. [Prosjektarkitektur (Medallion & BI-Stack)](#-prosjektarkitektur-medallion--bi-stack)
2. [Hovedkomponenter & 7 Interaktive Moduler](#-hovedkomponenter--7-interaktive-moduler)
3. [Cockpit & Workflow Pipeline Kontroll](#-cockpit--workflow-pipeline-kontroll)
4. [Excel Financial Modeling & Dashboard (FAST Standard)](#-excel-financial-modeling--dashboard-fast-standard)
5. [Mappe- og Filstruktur](#-mappe--og-filstruktur)
6. [Installasjon & Forutsetninger](#-installasjon--forutsetninger)
7. [Slik kjører du løsningen (A til Å)](#-slik-kjører-du-løsningen-a-til-å)
8. [ML-Modellportefølje & Algoritmer](#-ml-modellportefølje--algoritmer)
9. [Governance, Audit-logging & eInnsyn](#-governance-audit-logging--einnsyn)

---

## 📐 Prosjektarkitektur (Medallion & BI-Stack)

Databehandlingen bygger på en **3-lags Medallion-arkitektur** i DuckDB (`data/database/kostra_prod.duckdb`), som forsyner både Streamlit AI Workbench, det frittstående UX/UI-dashbordet (`index.html`), Power BI og Excel Power Pivot (`ThisWorkbookDataModel`):

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
│  - Renset for BOM-tegn og uønskede kildeavvik (0 filer i karantene)    │
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
│  1. Streamlit AI Workbench (src/app.py — 7 interaktive moduler)        │
│  2. Frittstående UX/UI & Pipeline Cockpit (index.html — Tufte/FAST)    │
│  3. Excel FAST & CUBE Workbook (Excel-Reporting-Analysis.xlsb)         │
│  4. Power BI Project (pbi-reporting-project.pbip / TMDL SemanticModel) │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🎛️ Hovedkomponenter & 7 Interaktive Moduler (`src/app.py` & `index.html`)

Både Streamlit-applikasjonen (`src/app.py`) og det frittstående web-grensesnittet (`index.html`) består av **7 synkroniserte moduler** designet etter Edward Tuftes *Data-Ink Ratio*-prinsipper:

1. **📊 1. Avviksoversikt (Gold Layer):**
   * Månedlige og akkumulerte (YTD M1–M8) sammenligninger av budsjett (`29 295 237 kr`) vs. regnskap (`31 524 851 kr`) og nettoavvik (`-2 229 614 kr`).
   * Dynamiske filtre for perioder, rammeområder/sektorer og avviksstatus (`🔴 KRITISK AVVIK` / `🟡 ADVARSEL` / `🟢 I RUTE`).
   * Tufte Bullet Chart (Forbruksrate vs. 100 % ramme) og Månedlig Combo Chart med 3M rullende trendlinje.

2. **📈 2. Tidsserie & Årsprognose (EAC / ETC per 31.12):**
   * **Bokført YTD (Mnd 1–8):** Faktisk registrert forbruk (`31 524 851 kr`).
   * **Projisert Q4 ETC (Mnd 9–12):** Sesongkorrigert fremskriving (`15 727 975 kr`) med interaktive blå FAST-parametere (`Param_Lonnsvekst_Q4`, `Param_Effektiviseringskrav_Pct`, `Param_Sesongvekt_M12`).
   * **Fullårsprognose EAC (per 31.12):** Estimert årsresultat (`47 252 826 kr`, forventet årsavvik `-3 309 971 kr`) visualisert med direkte-merket S-kurve.

3. **🌲 3. ML Prognoser & Early Warning (XAI):**
   * Forklarbar AI (XAI) som rangerer topp forklarende variabler fra `RandomForestRegressor` ($R^2 = 0.9104$).
   * 100 % revisjonssporbart `IF-THEN` beslutningstre fra `DecisionTreeClassifier` (`Status 0: I RUTE`, `Status 1: ADVARSEL`, `Status 2: KRITISK`).

4. **🚨 4. Anomaly Detection & Klyngeanalyse:**
   * **Hierarkisk Klustering (`hclust`):** Segmenterer kommunale konti i 4 adferdsprofiler (*Klynge 0: Stabil drift* `1 131`, *Klynge 1: Høyvolatil / Vikar* `16`, *Klynge 2: Sesongvariasjon* `1 100`, *Klynge 3: Ekstraordinære avvik* `9`).
   * **Isolation Forest & Z-Score (`Z > 2.5`):** Automatisk flagget sjekkliste for potensielle føringsfeil og bilagskontroll.

5. **⚙️ 5. Modelready Datagrunnlag & `06_CHECKS`:**
   * Full oversikt over `modelready_fact` (`2 256` rader × `32` features, `0,0 %` manglende verdier) og live avstemmingstabell (`06_CHECKS` der samtlige differanser er `0,00 kr`).

6. **💬 6. KI-Saksbehandler & Chatbot (RAG):**
   * Interaktiv KI-assistent med hurtigknapper og fritekstsøk som kombinerer oppslag i `modelready_fact` med Kommuneloven § 14-4, KOSTRA-forskriften og kommunens økonomireglement.

7. **🎛️ 7. Cockpit & Pipeline Kontroll (End-to-End Orchestration):**
   * Sentralt kontrollpanel for kjøring, overvåking og revisjon av hele verdikjeden fra rådata til ferdig avstemte BI- og Excel-modeller.

---

## 🚀 Cockpit & Workflow Pipeline Kontroll

Modulen **`🎛️ 7. Cockpit & Pipeline Kontroll`** (tilgjengelig både via toppbanneret `🎛️ PIPELINE: ONLINE` og i venstremenyen i `index.html` og `src/app.py`) gir ett-klikks orkestrering av de 4 produksjonsstegene:

| Steg | Pipeline-komponent | Nøkkelmetrikk & Kontrollstatus |
| :--- | :--- | :--- |
| **Steg 1: Bronze Layer (`-BuildDB`)** | `src/db_manager.py` (`data/raw/*.csv` → `stg_fact`) | 21 CSV-filer lest (`UTF-8` / `Latin1`), 4→6 siffer kontopolstring, **0 filer i karantene** (`INGESTION_REPORT.md`). |
| **Steg 2: Silver & Gold (`-Reconcile`)** | `silver_fact` → `modelready_fact` | `2 256` rader × `32` variabler (`LAG()` månedlig delta & 3M rullende snitt), **0,0 % null-verdier**. |
| **Steg 3: MLOps & XAI (`-Retrain`)** | `src/retrain_pipeline.py` | Random Forest ($R^2 = 0.9104$), Decision Tree (`100 %` Acc), `hclust` (`4` klynger) og Isolation Forest (`113` avvik flagget). |
| **Steg 4: BI & FAST Sync (`06_CHECKS`)** | `Excel-Reporting-Analysis.xlsb` & `.pbip` | 21 DAX-mål i `ThisWorkbookDataModel` og 11/11 avstemmingskontroller verifisert (**`MASTER_CHECK Diff = 0,00 kr`**). |

Cockpiten inneholder også:
* **Sanntids CLI-konsoll (`#pipeline-console`):** Strømmer statusmeldinger og kjøretider for hvert steg.
* **Ingestion Gate-tabell:** Viser valideringsstatus per kildefilsett (`komskole`, `bomiljo`, `dim_*`).
* **Uforanderlig Revisjonslogg (`audit_log`):** Logger hver kjøring med ISO-tidsstempel, UUIDv4, aktør og verifiseringsresultat.

---

## 📊 Excel Financial Modeling & Dashboard (`Excel-Reporting-Analysis.xlsb`)

Arbeidsboken `Excel-Reporting-Analysis.xlsb` (og `.xlsx`) er bygget etter **FAST-standarden** ([`excel.md`](excel.md)) og **Edward Tuftes Data-Ink Ratio**-prinsipper, koblet direkte til **Power Pivot (`ThisWorkbookDataModel`)** og 21 DAX-mål ([`DAX.md`](DAX.md)):

| Fane | Formål & Innhold |
| :--- | :--- |
| **`01_DASHBOARD`** | Koplingsfritt Power BI-style dashbord med `CUBEVALUE`/`CUBEMEMBER`-formler, sentralisert Slicer-panel (`År`, `Måned`, `KOSTRA Funksjon`, `Ansvarsenhet`), 6 avrundede KPI-kort, Sparklines (M1–M8), Combo Chart (Column + Line) og Bullet Chart. |
| **`02_OUTPUTS`** | Detaljerte finansielle oppstillinger: **Resultatoppstilling (Driftsregnskap & EAC)**, **Kontantstrømoppstilling** og **Balanseoppstilling** med full balanseavstemming (`0,00`). |
| **`03_CALCULATIONS`** | Beregningsmotor med én konsistent horisontal formel per rad (M1–M8 bokført + M9–M12 sesongjustert ETC/EAC-prognose) og CUBE-mellomstasjoner. |
| **`04_INPUTS`** | Dedikert parameterfane der alle hardkodede forutsetninger står i blå tekst (`#0000FF`) med 26 globale navngitte områder (`Param_*`). |
| **`05_DATA_MODEL`** | Stjerneskjema-dokumentasjon og live avstemming av de 5 Power Query-tabellene (`modelready_fact`, `dim_date`, `dim_ansvar`, `dim_kostra_funksjon`, `dim_kostra_kontoplan`). |
| **`06_CHECKS`** | Sentral modellkontroll og feilsjekk (`CHK_01`–`CHK_11` + `MASTER_CHECK`) som verifiserer at samtlige differanser er `0,00`. |

---

## 📂 Mappe- og Filstruktur

```text
Kom - G2/
├── index.html                          # Frittstående Tufte/FAST Web-UI med 7 moduler & Pipeline Cockpit
├── .env.example                        # Mal for miljøvariabler (kopieres til .env)
├── .gitignore                          # Git-ignoreringsregler for sikkerhet og tunge filer
├── Dockerfile                          # Container-definisjon for Streamlit & MLflow
├── docker-compose.yml                  # Multi-container orkestrering
├── requirements.txt                    # Python-avhengigheter
├── run.ps1                             # PowerShell CLI (-BuildDB, -Reconcile, -Retrain, -Up, -Down, -All)
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
│   ├── raw/                            # Inndatamappe for KOSTRA-CSV og dimensjonsfiler (21 filer)
│   ├── database/                       # Lokal DuckDB-database (ignoreres i Git, bygges av ETL)
│   └── export/                         # Automatisk genererte Ingestion- og Exception-rapporter
└── src/
    ├── app.py                          # Streamlit webapplikasjon (7 moduler inkl. Pipeline Cockpit)
    ├── canonical.py                    # Kanonisk datamodell og valideringsregler (Pydantic)
    ├── db_manager.py                   # DuckDB ETL, Medallion-pipeline og Audit Log
    └── retrain_pipeline.py             # Omtrening og evaluering av ML-modellene
```

---

## 🛠️ Installasjon & Forutsetninger

### Krav
* **Python:** v3.10 eller nyere (Python 3.11 / 3.12 anbefales)
* **Nettleser:** Enhver moderne nettleser for direkte åpning av `index.html` (ingen server nødvendig)
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

### Alternativ A: Direkte i nettleser (Zero-Install UX/UI & Cockpit)
Åpne **`index.html`** direkte i nettleseren for umiddelbar tilgang til alle 7 moduler, interaktive prognoseparametere, S-kurver, RAG-chatbot og **Cockpit Pipeline Kontroll**.

### Alternativ B: Automatisk kjøring via Batch-fil eller PowerShell
Kjør i PowerShell:
```powershell
.\run_pipeline.bat
# eller via PowerShell CLI:
.\run.ps1 -BuildDB -Retrain
```

### Alternativ C: Manuell kjøring steg-for-steg
1. **Bygg DuckDB-databasen fra rådata (`data/raw/`):**
   ```powershell
   python src/db_manager.py
   ```
2. **Kjør ML-omtrening og evaluering:**
   ```powershell
   python src/retrain_pipeline.py
   ```
3. **Start Streamlit AI Workbench-dashbordet:**
   ```powershell
   streamlit run src/app.py
   ```

---

## 🤖 ML-Modellportefølje & Algoritmer

| Modell / Algoritme | Formål | Målvariabel / Ytelse |
| :--- | :--- | :--- |
| **Random Forest Regressor** | Prognostisere neste måneds regnskapsforbruk | $R^2 = 0.9104$, Low MAE (`18 420 kr`) |
| **Decision Tree Classifier** | Generere revisjonsgodkjente IF-THEN regler for Early Warning | `100 %` Accuracy — Status 0 (`I RUTE`), 1 (`ADVARSEL`), 2 (`KRITISK`) |
| **Agglomerative Clustering (`hclust`)** | Gruppere konti i 4 utgiftsprofiler | Unsupervised (`4` klynger: `1131 / 16 / 1100 / 9`) |
| **Isolation Forest (`iforest`)** | Detektere føringsfeil og uvanlige beløpshopp | Top 5 % Z-score / avvikskontroll (`113` rader flagget) |

---

## 🛡️ Governance, Audit-logging & eInnsyn

I tråd med kommunale retningslinjer for kunstig intelligens og forvaltningsloven har systemet innebygd sporbarhet:

* **Uforanderlig Audit Log (`audit_log`):** Alle spørringer, pipeline-kjøringer, avvikstiltak og AI-genererte anbefalinger logges automatisk med UUID, ISO-tidsstempel og aktør-ID.
* **Ingestion Report (`data/export/INGESTION_REPORT.md`):** Genereres automatisk ved hver kildedataimport og dokumenterer godkjente filer samt eventuelle filer lagt i karantene.

---
*Kristiansand kommune — KOSTRA AI Workbench © 2026*
