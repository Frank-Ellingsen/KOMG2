# 🏛️ KOSTRA AI Enterprise Suite — Kristiansand Kommune
### Beslutningsstøtte, Økonomistyring, Månedsavslutning & Framsikt-Integrasjon

> **Utviklet for:** Rådgiver økonomistyring, enhetsledere, kommunalsjefer og økonomidirektøren i Kristiansand kommune.  
> **Formål:** Transformere kommunal økonomistyring fra reaktiv historiefortelling til proaktiv, prediktiv og juridisk forankret virksomhetsstyring.

---

## 🎯 Hva Løser Appen?

I en kommune med milliardomsetning og tusenvis av ansatte er god økonomistyring avgjørende for innbyggernes tjenestetilbud. Likevel møter økonomirådgivere og budsjettansvarlige ofte de samme flaskehalsene:
* **Tunge systemer og forsinkede tall:** Det tar dager å hente ut, rense og koble regnskapsdata fra Agresso og Visma Gat etter månedsslutt.
* **Manuell og tidkrevende avviksoppfølging:** Enhetsledere bruker verdifull tid på å forklare tall de ikke forstår, mens rådgivere må skrive likelydende purringer og månedsnotater fra bunnen av.
* **Uoversiktlig vikarbruk og sykefravær:** Kostbare vikarbyråer (art 1020/1270) og overtid (art 1040) spiser opp rammer uten at kompenserende tiltak iverksettes i tide.
* **Dobbeltarbeid mot Framsikt:** Rådgiveren må manuelt regne ut omdisponeringer i regneark og taste dem inn linje for linje i Framsikt.
* **Frister og lovkrav som glipper:** Komplekse formelle prosesser (tertialrapporter, bystyresaker, revisjonsfrister etter Kommuneloven § 14) koordineres ofte i statiske e-poster og løse notater.

---

### 💡 Løsningen: En Helhetlig Styrings- og Analysearena

Denne applikasjonen fungerer som rådgiverens **digitale co-pilot og operative for-system**. Den automatiserer rutineoppgaver, gir umiddelbar innsikt ved månedsslutt, og bygger bro mellom operative enhetsledere, økonomiavdelingen og politisk ledelse:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        KILDESYSTEMER (Agresso, Visma Gat, Fagsystemer)                 │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Automatisk Ingestion & Avstemming
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               KOSTRA AI DECISION SUITE (Denne Applikasjonen)                           │
│                                                                                        │
│  💼 Månedsavslutning & Rådgiveroversikt   📅 Årshjul & Lovpålagte Frister (§ 14)       │
│  • Ferdige 1-sides lederrapporter         • 12 måneders styringssyklus                 │
│  • Bitemporal låsing (Diff: 0,00 kr)      • Månedsslutt-sjekkliste med fremdrift       │
│                                                                                        │
│  📑 Framsikt Budsjettregulering           📝 Automatisk Saksdokument-Generator         │
│  • 12-kolonners direkte CSV-eksport       • Ferdig utfylte saksfremlegg (Bystyret)     │
│  • Sanntids balansekontroll (§ 13-1 vs 14-6)• Bestillings- og purrenotater til enheter │
│                                                                                        │
│  📈 Prediktiv Analyse & Simulering        📊 Dyp Utforskning (EDA & FT Visual Guide)   │
│  • EAC/ETC årsprognose med 4 kuttspaker   • Sammenhenger, vikarvolatilitet, trender    │
│  • Forklarbar maskinlæring (XAI)          • Muted Tufte design uten unødig støy        │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ 12-kolonners importfil / Ferdige saksnotater
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│          FRAMSIKT (framsikt.no), BYSTYRET OG AGDER KOMMUNEREVISJON                     │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔑 Hovedgevinster i Rådgiverhverdagen

### 1. Lynrask Månedsavslutning mot Budsjettansvarlige
* **3 Predefinerte Standardrapporter:**
  * **1. Enhetslederens Månedsrapport (1 A4-side):** Tilpasset budsjettmøtet. Viser YTD-forbruk, periodisert avvik, vikarandel, overtid, MoM-trend (M08 vs M07) og handlingsrom.
  * **2. Kommunaldirektørens Flash-rapport:** Overordnet sektorstatus, RAG-risikomatrise, de 3 mest kritiske enhetene og anbefalte administrative tiltak.
  * **3. Controllerens Avviks- & Unntaksrapport:** Detaljert revisjonssammendrag for enheter med avvik over 3,0 % eller unormal burn-rate.
* **Automatisert AI-kommentar (NLG):** Tolker tallene i ren tekst etter Kommunelovens prinsipper – sparer rådgiveren for timevis med manuell tekstproduksjon.
* **Bitemporal Snapshot-låsing:** Alle rapporter låses mot DuckDB Gold Layer med revisjonsstempel og `Diff = 0,00 kr`.

### 2. Sømløs Framsikt-Integrasjon (framsikt.no)
* **Predefinerte Reguleringsmaler:**
  * *LOY Helse & Mestring:* Intern omdisponering (kutt i vikar/overtid mot fastlønn, netto 0 kr jf. § 13-1).
  * *LOY Oppvekst & Utdanning:* Vakanssparing og vikardekning i grunnskole (netto 0 kr).
  * *Bystyresak / Disposisjonsfond:* Uforutsett merforbruk finansiert av fond (art 195000 jf. § 14-6).
  * *NAV Refusjonsetterslep:* Teknisk periodisering av sykelønnsrefusjoner (art 1710/1690).
* **Sanntids Balansekontroll:** Viser umiddelbart om en regulering er i balanse (Kommunedirektørens fullmakt) eller krever politisk bystyrevedtak.
* **12-kolonners Eksport:** Genererer ferdig formatert CSV (UTF-8 BOM med semikolon) som importeres direkte i Framsikt uten manuell re-tasting.

### 3. Årshjul for Økonomistyring & Frister
* **Helårlig 12-måneders styringshjul:** Holder oversikt over revisjonsfristen 15. februar (§ 14-8), 1. tertial (T1), 2. tertial (T2), Handlings- og økonomiplan (HØP 2027–2030) og Bystyrets årsbudsjettvedtak før nyttår (§ 14-3).
* **Filtrerbare faser:** Sorter på lovpålagte frister, tertial/årsoppgjør eller politiske bystyremøter.
* **Interaktiv Sjekkliste for Månedsavslutning:** 8 operative kontrollpunkter med sanntids fremdriftsindikator og automatisk lagring i nettleseren (`localStorage`).

### 4. Automatisk Dokument- & Rapportgenerator
* Genererer fullstendige, formelle saksfremlegg og notater med **reelle tall hentet dynamisk fra ditt aktive filter**:
  1. *🏛️ Bystyresak: 2. Tertialrapport og budsjettreguleringer (§ 14-6)* med 4-punkts vedtaksforslag.
  2. *🏢 Bestillingsnotat til Enhetsleder:* Formelt krav om avviksforklaring og EAC-oppdatering ved overskridelse av 3 %-grensen.
  3. *💼 Ledelsesnotat til Kommunalsjef:* Flash-analyse og anbefalte LOY-omdisponeringer.
  4. *📑 Rammebrev HØP 2027–2030:* Deflatorforutsetninger, innsparingskrav og retningslinjer for Framsikt.
  5. *🔒 Årsavslutningsnotat til Revisjon:* Protokoll for overføring og bitemporal avstemming.
* **Handlinger:** Kopier til utklippstavle, last ned som fullverdig Microsoft Word-fil (`.doc`) med brevhode og tabeller, eller skriv ut i A4-format.

### 5. Dyp Datautforskning (EDA) etter Financial Times Visual Guide
* Interaktiv modul basert på *Financial Times Visual Vocabulary*.
* Veileder brukeren i valg av riktig visualisering (Sammenheng, Fordeling, Endring over tid, Avvik, Rangering).
* Inneholder ferdige forslag for kommunale problemstillinger (f.eks. *«Hvordan henger vikarutgifter sammen med overtid og sykefravær i helse og mestring?»*).

---

## 🎛️ Oversikt over Modulene i Appen

Applikasjonen (`index.html`) er bygget som en lynrask, offline-first Single Page Application (SPA):

| # | Modul | Primært formål for rådgiver og leder |
| :-: | :--- | :--- |
| **1** | **💼 Rådgiveroversikt** | Månedsavslutnings-cockpit, 3 predefinerte A4-rapporter, AI-sammendrag, MoM-delta og bitemporalt revisjonsstempel. |
| **2** | **📅 Årshjul, Frister & Dokumenter** | 12-måneders styringshjul, Kommunelov-frister, sjekkliste og 1-klikks generator for formelle saksfremlegg og Word-dokumenter. |
| **3** | **📑 Budsjett & Framsikt Regulering** | Lønns- og rammereguleringer, forhåndsdefinerte kommunale maler, balansekontroll (§ 13-1 vs 14-6) og 12-kolonners CSV-eksport. |
| **4** | **📊 Avviksoversikt (Gold Layer)** | Tufte-bullet charts, RAG-status (rød/gul/grønn), 3M glidende snitt og artsavvik (1010 fastlønn, 1020 vikar, 1040 overtid, 1270 byrå). |
| **5** | **📈 Tidsserie & Årsprognose (EAC)** | 4-slider LOY kutt-simulator, sanntids SVG-trajektorie, månedstak for M9–M12 og juridisk handlingsrom. |
| **6** | **📊 EDA & FT Visual Guide** | Utforskende dataanalyse inspirert av FT Visual Vocabulary med dynamiske scatter-, søyle- og fordelingsgrafer. |
| **7** | **🌲 ML Prognoser & Early Warning** | Forklarbar AI (XAI) basert på Random Forest ($R^2=0.9758$) og beslutningstre med transparente `IF-THEN`-regler for revisjon. |
| **8** | **🚨 Anomaly & Klyngeanalyse** | Klyngeinndeling (Stabil, Vikarvolatil, Sesong, Ekstraordinær) og Isolation Forest for å avdekke bilagsfeil ($Z > 2.5$). |
| **9** | **🎯 Recommender & Tiltaksmatrise** | Konkrete forslag til innsparingstiltak med beregnet sparepotensial, risiko og juridisk hjemmel. |
| **10** | **💬 KI-Saksbehandler & Chatbot** | Presidio PII-sikret rådgiverbot med Hybrid RAG koblet mot Kommuneloven og KOSTRA-veilederen. |
| **11** | **📜 Anskaffelser & Spend (LOA)** | DFØ 7-trinns anskaffelsesprosess, 2026 EØS- og nasjonale terskelverdier og Maverick Spend Detector. |
| **12** | **💳 Faktura, Interne & Selvkost** | Konsolideringseliminering (art 380 vs 780, Diff = 0,00 kr), armlengdes prinsipp (IKS § 20-1) og 5-årig selvkostkalkyle. |
| **13** | **🏛️ Søknader & Tilskudd** | Inbound statlige tilskudd (IMDi, Helsedir, Klimasats) og outbound kommunale tildelinger med 4-trinns utbetalingskontroll. |
| **14** | **⚙️ Modelready Datagrunnlag** | Innsyn i `modelready_fact` og FAST-standardens `06_CHECKS` (11 avstemmingskontroller med Diff = 0,00 kr). |
| **15** | **🎛️ Cockpit & Pipeline Kontroll** | Orkestreringspanel for datastrømmen med live batch-terminal og uforanderlig revisjonslogg. |

---

## 🎨 Design- og Brukergrensesnittstandarder

Applikasjonen følger strenge faglige standarder for datavisualisering og finansiell modellering:

### 1. Edward Tufte Data-Ink Ratio
* **Maksimal Data-Ink:** Ingen unødvendige pynteelementer, tunge skygger eller forstyrrende 3D-effekter.
* **Ingen vertikale tabellinjer:** Bruker diskrete horisontale skillelinjer for å lette lesbarheten.
* **Muted fargepalett:** Nøytrale gråtoner i bakgrunn og struktur. Røde og gule farger reserveres utelukkende for aktive avvik og risikopunkter.
* **Typografi og talljustering:** Tekst er alltid venstrejustert; tall, beløp og prosenter er konsekvent høyrejustert med faste desimaler i monoskrift (`var(--font-mono)`).
* **Tufte Bullet Charts:** Horisontale stolpediagrammer som viser faktisk forbruk mot periodisert budsjett og varslingsterskler på minimal plass.

### 2. FAST Standard Financial Modeling
* **F**lexible, **A**ppropriate, **S**tructured, **T**ransparent.
* Én felles formelstruktur per rad i regnearkmodellene (`Excel-Reporting-Analysis.xlsb`).
* Dedikert **`06_CHECKS`** avstemmingsfane med 11 automatiske kontroller som garanterer at alle konsolideringer og overføringer balanserer til nøyaktig `Diff = 0,00 kr`.

---

# ⚙️ TEKNISK DOKUMENTASJON & ARKITEKTUR

---

## 📐 Medallion Data Lakehouse (DuckDB)

Systemets kjerne er bygget på en **3-lags Medallion Lakehouse-arkitektur** implementert i **DuckDB** (`data/database/kostra_prod.duckdb`):

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        RÅDATA & LOCALBLOB (data/raw & data/localblob)                  │
│                        21 KOSTRA-filer + 42 Blob-filer (CSV, XLSX, TXT)                │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Smart Ingestion, UTF-8/Latin-1, Kodepolstring
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  BRONZE LAYER (stg_fact)                                                               │
│  - Kodepolstring: Konto (4 -> 6 siffer, f.eks. 1010 -> 101000)                         │
│  - Kodepolstring: Funksjon (3 -> 4/5 siffer, f.eks. 120 -> 0120)                       │
│  - Automatisk BOM-stripping, formatvalidering & 0 filer i karantene                    │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ ISO-Datoer & LAG() Window Functions
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  SILVER LAYER (silver_fact & vw_silver_snapshots)                                      │
│  - Avstemt hovedbok over alle regnskapsperioder (M1–M8)                                │
│  - Beregning av reelle månedlige nettotall (monthly_delta)                             │
│  - Bitemporal snapshot-sporing for revisjonskontroll                                   │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Feature Engineering (32 variabler)
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  GOLD LAYER (modelready_fact & Star Schema Dimensjoner)                                │
│  - 2 256 rader × 32 features, 0,0 % nullverdier                                        │
│  - Dimensjoner: dim_date, dim_ansvar, dim_kostra_funksjon, dim_kostra_kontoplan        │
│  - 06_CHECKS: 11/11 kontroller godkjent (MASTER_CHECK Diff = 0,00 kr)                  │
└──────────────────┬────────────────────────┬───────────────────────────┬────────────────┘
                   │                        │                           │
                   ▼                        ▼                           ▼
┌────────────────────────────┐ ┌──────────────────────────┐ ┌────────────────────────────┐
│ FastAPI REST API (:8000)   │ │ Frittstående Web Cockpit │ │ Excel & Power BI Suite     │
│ - 10 REST-endepunkter      │ │ (index.html, 5 700+ l.)  │ │ - Excel-Reporting-         │
│ - Presidio PII Gateway     │ │ - 15 interaktive moduler │ │   Analysis.xlsb (FAST)     │
│ - Hybrid RAG (BM25 + BGE)  │ │ - 100 % dynamisk filter  │ │ - pbi-reporting-project    │
│ - MLOps inferensmotor      │ │ - Framsikt & Årshjul     │ │   (.pbip / TMDL)           │
└────────────────────────────┘ └──────────────────────────┘ └────────────────────────────┘
```

---

## ⚡ FastAPI REST Backend & API-Katalog

FastAPI-serveren (`src/api_server.py`) kjører asynkront og eksponerer produksjonsklare endepunkter dokumentert via Swagger UI (`http://localhost:8000/docs`):

| Endepunkt | Metode | Beskrivelse |
| :--- | :---: | :--- |
| `/api/v1/monthly-report` | `GET` | Henter aggregert månedsrapport: YTD, EOY, månedsserie og artsdrivere. |
| `/api/pipeline/status` | `GET` | Returnerer status for DuckDB, modelltrening og filantall i `data/raw` og `data/localblob`. |
| `/api/pipeline/run` | `POST` | Kjører end-to-end datapipeline (DuckDB Medallion ETL og MLOps retrain). |
| `/api/eac/forecast` | `POST` | Beregner EAC/ETC basert på YTD-tall og simulerte kuttspaker. |
| `/api/notat/generate` | `POST` | Genererer strukturert, eInnsyn-godkjent rådgivnings- og tertialnotat. |
| `/api/presidio/anonymize` | `POST` | Skrubber sensitive personopplysninger (FNR, Ansattnr, Navn) via Presidio Gateway. |
| `/api/rag/search` | `POST` | Hybrid RAG-søk i kommunal kunnskapsbase (BM25 + Dense embeddings + BGE Reranker). |
| `/api/procurement/spend-analysis` | `GET` | Spend analytics og DFØ-terskelkontroll fordelt på leverandører. |
| `/api/procurement/maverick-spend` | `GET` | Detekterer avvikende innkjøp foretatt uten gyldig rammeavtale. |
| `/api/internal-services/elimination-report` | `GET` | Konsolideringsrapport for intern omsetning (art 380 vs 780, Diff = 0,00 kr). |
| `/api/internal-services/selvkost-calc` | `POST` | Beregner lovpålagt selvkost for VAR-sektoren med kalkylerente og fondsoppfølging. |
| `/api/grants/inbound-compliance` | `GET` | Etterlevelsesstatus og refusjonskrav for statlige tilskudd (IMDi, Helsedir, Klimasats). |

---

## 🤖 MLOps & Modellportefølje

Modellene i `models/` overvåkes kontinuerlig mot modelldrift og trenes via `src/retrain_pipeline.py`:

| Modell | Algoritme | Ytelse / Metrikk | Formål |
| :--- | :--- | :--- | :--- |
| **Prognosemodell** | `RandomForestRegressor` | $R^2 = 0.9758$, $\text{MAE} = 1\,655\text{ kr}$ | Predikere neste måneds forbruk per ansvarsenhet og art. |
| **Tidlig Varsling** | `DecisionTreeClassifier` | `100,0 %` Nøyaktighet | Generere transparente `IF-THEN`-regler for revisjon og saksbehandling. |
| **Profilering** | `AgglomerativeClustering` | 4 klynger | Kartlegge utgiftsmønstre (Stabil, Vikar/Volatil, Sesong, Avvik). |
| **Avviksdeteksjon** | `IsolationForest` | 113 flaggede avvik ($Z > 2.5$) | Identifisere potensielle feilkonteringer og bilagsfeil. |

---

## 🛡️ GDPR, Presidio PII Gateway & Juridisk Forankring

### Presidio PII Gateway
For å etterleve GDPR artikkel 9 og personopplysningsloven sluses all fritekst gjennom **Presidio PII Gateway** før den sendes til LLM- eller analysemoduler:
* **Fødselsnummer (11 siffer):** Maskeres til `[FNR]`
* **Ansattnummer (6–8 siffer):** Maskeres til `[ANSATTNR]`
* **Personnavn og sensitiv lokasjonsdata:** Maskeres til `[PERSON]` / `[LOKASJON]`

### Juridisk Forankring
Alle beregninger, notatmaler og saksdokumenter er forankret i gjeldende norsk lovverk:
* **Kommuneloven § 13-1:** Kommunedirektørens administrative fullmakter og interne omdisponeringer.
* **Kommuneloven § 14-3:** Bystyrets vedtak av handlings- og økonomiplan samt årsbudsjett innen årets utløp, inkludert 3 ukers offentlig høringsfrist.
* **Kommuneloven § 14-6:** Krav til budsjettbalanse og Bystyrets bevilgningsmyndighet ved vesentlige reguleringer.
* **Kommuneloven § 14-7:** Forvaltning av bundne og ubundne driftsfond (disposisjonsfond).
* **Kommuneloven § 14-8:** Lovpålagt frist (15. februar) for oversendelse av foreløpig årsregnskap til kommunerevisjonen.
* **KOSTRA-forskriften:** Standardiserte arts- og funksjonskoder for nasjonal rapportering til SSB.

---

## 📂 Mappe- og Filstruktur

```text
Kom - G2/
├── index.html                          # Frittstående Executive Web Cockpit (15 moduler, 5 700+ linjer)
├── README.md                           # Komplett dokumentasjon (forretningsverdi + teknisk)
├── templates/
│   └── index.html                      # Dedikert EOY & LOY Rådgivningscockpit med Chart.js
├── docs/
│   ├── COPILOT_PYTHON_IN_EXCEL_INSTRUCTIONS.md # Instruks for Copilot & Python in Excel (=PY())
│   └── INSTRUKS_EXCEL_DASHBOARD.md     # Instruks for Power Query & Power Pivot
├── .env.example                        # Mal for miljøvariabler
├── .gitignore                          # Git-regler
├── Dockerfile                          # Multi-stage containerdefinisjon
├── docker-compose.yml                  # Streamlit (:8501), FastAPI (:8000), MLflow (:5000)
├── requirements.txt                    # Produksjonsavhengigheter (DuckDB, FastAPI, Scikit-learn, etc.)
├── run.ps1                             # PowerShell CLI (-BuildDB, -Reconcile, -Retrain, -VectorDB, -Up, -All)
├── run_pipeline.bat                    # Master Batch-skript for helhetlig lokal kjøring
├── Excel-Reporting-Analysis.xlsb       # FAST & Power BI-Style Excel-modell (Binær arbeidsbok)
├── Excel-Reporting-Analysis.xlsx       # FAST & Power BI-Style Excel-modell (OpenXML)
├── pbi-reporting-project.pbip          # Power BI Desktop Developer Project
├── pbi-reporting-project.Report/       # Rapportoppsett og visualiseringer
├── pbi-reporting-project.SemanticModel/# TMDL-datamodell og 21 DAX-mål
├── excel.md                            # Retningslinjer for FAST-modellering
├── DAX.md                              # Komplett DAX-målkatalog
├── copilot.md                          # Standard for Copilot i regneark
├── data/
│   ├── raw/                            # Inndata for KOSTRA-CSV (21 filer)
│   ├── localblob/                      # Lokale rådata og vedlegg (42 filer)
│   ├── database/                       # Lokal DuckDB (kostra_prod.duckdb)
│   └── export/                         # Genererte rapporter og avstemmingslogger
├── models/                             # Serialiserte ML-modeller (.pkl / joblib)
└── src/
    ├── app.py                          # Streamlit AI Workbench (8 moduler)
    ├── api_server.py                   # FastAPI REST backend (10 endepunkter, RAG, Presidio)
    ├── test_api_endpoints.py           # Automatisert testsuite for FastAPI (10/10 tester)
    ├── db_manager.py                   # DuckDB Medallion ETL og Ingestion Engine
    ├── canonical.py                    # Pydantic validering og dataskjema
    └── retrain_pipeline.py             # MLOps omtrening og modelldrift-evaluering
```

---

## 🚀 Installasjon & Kjøreveiledning (A til Å)

### Forutsetninger
* **Python:** v3.10, v3.11 eller v3.12 installert.
* **Nettleser:** Chrome, Edge eller Firefox.
* **Docker Desktop:** (Valgfritt, for containerisert drift).

---

### Alternativ 1: Frittstående Web Cockpit (Raskest & Enklest)
Åpne **`index.html`** direkte i nettleseren (støtter også GitHub Pages).  
Appen kjører offline med fulle analytiske kapabiliteter, dynamisk filtrering, Framsikt-eksport, saksdokument-generator og årshjul uten krav til lokal server.

Dersom du ønsker live integrasjon mot FastAPI-backend-en:
Dobbeltklikk **`start_web_cockpit.bat`** eller kjør i PowerShell:
```powershell
.\start_web_cockpit.bat
```

---

### Alternativ 2: Master Batch-fil (`run_pipeline.bat`)
Fra filutforskeren eller ledetekst (CMD / PowerShell):
```cmd
.\run_pipeline.bat
```
Dette skriptet utfører hele produksjonsløpet:
1. Bygger DuckDB Medallion Lakehouse fra `data/raw/*.csv`.
2. Trener og evaluerer alle maskinlæringsmodeller.
3. Indekserer kunnskapsbasen for Hybrid RAG.
4. Starter Streamlit AI Workbench på `http://localhost:8501`.

---

### Alternativ 3: PowerShell CLI (`run.ps1`)
Bruk PowerShell-skriptet for granulær kontroll:
```powershell
# Bygg databasen og tren modeller:
.\run.ps1 -BuildDB -Retrain

# Indekser vektordatabasen for RAG:
.\run.ps1 -VectorDB

# Start Docker-containerne (Streamlit, FastAPI og MLflow):
.\run.ps1 -Up

# Kjør alt i sekvens:
.\run.ps1 -All
```

---

### Alternativ 4: Start FastAPI Backend Standalone
For å starte REST-API-et separat:
```powershell
uvicorn src.api_server:app --host 127.0.0.1 --port 8000 --reload
```
Åpne `http://localhost:8000/docs` i nettleseren for interaktiv Swagger-dokumentasjon.

---

### Alternativ 5: Docker Compose
For komplett containerisering:
```powershell
docker compose up --build -d
```
Tjenester som starter:
* **Streamlit AI Workbench:** `http://localhost:8501`
* **FastAPI Backend:** `http://localhost:8000/docs`
* **MLflow Tracking Server:** `http://localhost:5000`

---

## 🧪 Verifikasjon & Tester

Kjør den automatiserte testsuiten for å verifisere at samtlige 10 REST-endepunkter fungerer:
```powershell
python -m src.test_api_endpoints
```
*Forventet resultat: `Ran 10 tests in 0.45s - OK (10/10 PASS)`.*

For å verifisere databaseavstemmingen og `06_CHECKS`:
```powershell
python -c "import duckdb; con = duckdb.connect('data/database/kostra_prod.duckdb'); print(con.execute('SELECT COUNT(*) FROM modelready_fact').fetchone())"
```
*Forventet resultat: `(2256,)` rader med `0,0 %` nullverdier og differanse `0,00 kr`.*

---

## 🏛️ Forfatter & Ansvarlig

* **Fagansvarlig & Utvikler:** Frank Ellingsen — Financial Controller & Business Intelligence Specialist.
* **Organisasjonskontekst:** Kristiansand kommune / Økonomistyring & Virksomhetskontroll © 2026.
* **Faglige Standarder:** Norsk Lovdata (*Kommuneloven*), Framsikt standarder, DFØ, FAST Standard Organization, Edward Tufte Data-Ink Ratio.
