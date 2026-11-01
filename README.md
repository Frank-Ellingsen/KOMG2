# 🏛️ KOSTRA AI Enterprise Lakehouse & Decision Support Suite — Kristiansand Kommune

**Helhetlig Enterprise AI-plattform for kommunal økonomistyring, MLOps, automatisert avvikskontroll, DFØ-anskaffelser, selvkostkalkyler, tilskuddsforvaltning og prescriptive tertialprognoser.**

---

## 📌 Om Prosjektet

**KOSTRA AI Enterprise Suite** er en produksjonsklar dataplattform og et strategisk beslutningsstøttesystem utviklet for økonomiavdelingen, prosjekt- og økonomikontrollere, samt kommunedirektøren i Kristiansand kommune. Løsningen transformerer tradisjonell, reaktiv KOSTRA-rapportering til en proaktiv, prediktiv og juridisk forankret styringsarena.

Plattformen forener:
* **DuckDB Medallion Lakehouse** (`Bronze -> Silver -> Gold`) med sanntids avstemmingskontroller (`Diff = 0,00 kr`).
* **Maskinlæring & XAI** (Random Forest $R^2=0.9758$, Decision Tree regler, Agglomerative Clustering og Isolation Forest).
* **FastAPI Produksjonsbackend** (`src/api_server.py`) med 10 REST-endepunkter, Presidio PII-anonymisering og Hybrid RAG (BM25 + Vektorsøk + BGE Reranker).
* **Frittstående Executive Web Cockpit (`index.html`)** med 10 interaktive moduler, 100 % dynamisk filtermotor, RAG betinget formatering, Edward Tufte Data-Ink bullet charts, 4-slider LOY-simulator, sanntids SVG-trajektorie og 1-klikks automatisert tertialnotatgenerator.
* **FAST-modellert Excel-arkitektur** (`Excel-Reporting-Analysis.xlsb`) og **Power BI Semantic Model** (`pbi-reporting-project.pbip`).

---

## 📋 Innholdsfortegnelse

1. [Prosjektarkitektur & Medallion Data Lakehouse](#-prosjektarkitektur--medallion-data-lakehouse)
2. [Oversikt over de 10 Interaktive Modulene](#-oversikt-over-de-10-interaktive-modulene)
3. [Prescriptive LOY-Simulator & Automatisert Tertialnotat](#-prescriptive-loy-simulator--automatisert-tertialnotat)
4. [Enterprise AI Suite: Anskaffelser, Selvkost & Tilskudd](#-enterprise-ai-suite-anskaffelser-selvkost--tilskudd)
5. [FastAPI REST Backend & API-Katalog](#-fastapi-rest-backend--api-katalog)
6. [Designstandarder: Edward Tufte & FAST Modeling](#-designstandarder-edward-tufte--fast-modeling)
7. [MLOps & Modellportefølje](#-mlops--modellportefølje)
8. [GDPR, Presidio PII Gateway & Juridisk Forankring](#-gdpr-presidio-pii-gateway--juridisk-forankring)
9. [Mappe- og Filstruktur](#-mappe--og-filstruktur)
10. [Installasjon & Kjøreveiledning (A til Å)](#-installasjon--kjøreveiledning-a-til-å)
11. [Verifikasjon & Tester](#-verifikasjon--tester)

---

## 📐 Prosjektarkitektur & Medallion Data Lakehouse

Systemet er bygget på en **3-lags Medallion Lakehouse-arkitektur** i **DuckDB** (`data/database/kostra_prod.duckdb`), med sømløs integrasjon mot analytiske motorer og brukerflater:

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
│ - 10 REST-endepunkter      │ │ (index.html, 5 300+ l.)  │ │ - Excel-Reporting-         │
│ - Presidio PII Gateway     │ │ - 10 interaktive moduler │ │   Analysis.xlsb (FAST)     │
│ - Hybrid RAG (BM25 + BGE)  │ │ - 100 % dynamisk filter  │ │ - pbi-reporting-project    │
│ - MLOps inferensmotor      │ │ - LOY-simulator & SVG    │ │   (.pbip / TMDL)           │
└────────────────────────────┘ └──────────────────────────┘ └────────────────────────────┘
```

---

## 🎛️ Oversikt over de 10 Interaktive Modulene

Det frittstående web-grensesnittet (`index.html`) inneholder **10 spesialiserte styringsmoduler** og en arbeidsflate for budsjettansvarlige. Streamlit-applikasjonen (`src/app.py`) har en tilsvarende arbeidsflate:

| Modul | Tittel & Fokus | Nøkkelinnhold & Analytiske Kapabiliteter |
| :---: | :--- | :--- |
| **Web** | **💼 Rådgiveroversikt** | Filtrer månedsrapporten på rammeområde og ansvarssted. Viser YTD-status, vedtatt årsbudsjett, EOY-prognose og prognoseavvik, månedstrend, prognosedrivere og møteoppfølging. Tilgjengelige sektorer hentes fra DuckDB og datadekningen vises eksplisitt. Møteoppfølging lagres lokalt i nettleseren, ikke som delt saksbehandling. |
| **Streamlit** | **💼 Rådgiveroversikt** | Filtrer på rammeområde, ansvarssted og tilgjengelig regnskapsperiode fra DuckDB. Viser regnskap og budsjett hittil i år, årsprognose, prognoseavvik og drivere. Grensesnittet viser hvilke sektorer datagrunnlaget inneholder og ber brukeren kontrollere fullstendighet mot autoritative kildesystemer. Prognosen er et estimat, ikke et vedtak. |
| **1** | **📊 Avviksoversikt (Gold Layer)** | 100 % dynamisk multi-slicer filtrering (Periode, Sektor, Ansvar, Funksjon, Status). RAG betinget formatering (`🔴 Kritiske avvik > 5 %`, `🟡 Advarsel 2–5 %`, `🟢 I rute < 2 %`). Edward Tufte Data-Ink bullet charts for KOSTRA-funksjoner og utgiftsarter (1010, 1020, 1040, 1090, 1270). 3M rullende glidende snitt. |
| **2** | **📈 Tidsserie & Årsprognose (EAC)** | Dedikert, toveissynkronisert filterpanel. YTD M1–M8 (Bokført `31 524 851 kr`) vs. Årsbudsjett (`29 295 237 kr`), nettoavvik (`-2 229 614 kr`), LOY gjenstående ramme M9–M12 og påkrevd månedstak (`2 281 890 kr/mnd`). Prescriptive 4-slider simulator, real-time SVG-trajektorie og 1-klikks automatisert tertialnotatgenerator. |
| **3** | **🌲 ML Prognoser & Early Warning (XAI)** | Forklarbar maskinlæring (XAI) basert på `RandomForestRegressor` ($R^2 = 0.9758$, $\text{MAE} = 1\,655\text{ NOK}$). 100 % revisjonsgodkjent beslutningstre (`DecisionTreeClassifier`) med eksplisitte `IF-THEN`-regler for tidlig varsling. |
| **4** | **🚨 Anomaly Detection & Klyngeanalyse** | Hierarkisk klustering (`AgglomerativeClustering`) med 4 adferdsklynger (*Klynge 0: Stabil drift* `1 131`, *Klynge 1: Høyvolatil / Vikar* `16`, *Klynge 2: Sesongvariasjon* `1 100`, *Klynge 3: Ekstraordinære avvik* `9`). Isolation Forest og Z-score ($Z > 2.5$) for bilagskontroll (113 flaggede avvik). |
| **5** | **⚙️ Modelready Datagrunnlag & `06_CHECKS`** | Full innsynskontroll i `modelready_fact` (2 256 rader × 32 features, 0,0 % nuller). Avstemmingsarkitektur etter FAST-standardens `06_CHECKS` med 11 kontroller der samtlige differanser er verifisert til nøyaktig `0,00 kr`. |
| **6** | **💬 KI-Saksbehandler & Chatbot (RAG)** | Presidio PII-beskyttet KI-saksbehandler for kommunal økonomi. Hybrid RAG (BM25 + Dense embeddings + BGE Reranker) koblet mot Kommuneloven, KOSTRA-veilederen og DFØ-regelverket. Inkluderer kildehenvisningsskuff (Citation Drawer) med full transparens. |
| **7** | **🎛️ Cockpit & Pipeline Kontroll** | Sentralt orkestreringspanel for datastrømmen. Viser sanntidsstatus for rådatafiler (`data/raw`: 21 filer, `data/localblob`: 42 filer), live ANSI-terminalkonsoll for batch-kjøring og uforanderlig `audit_log` med UUIDv4 og ISO-tidsstempler. |
| **8** | **🛒 Offentlige Anskaffelser & Spend Analytics** | DFØ 7-trinns anskaffelsesprosess, 2026 EØS- og nasjonale terskelverdier (EØS vare/tjeneste `1,5 mill. kr`, stat `2,3 mill. kr`, bygg/anlegg `57 mill. kr`, nasjonal kunngjøringsterskel `100 000 kr`). Automatisk *Maverick Spend Detector* for fakturaer uten gyldig rammeavtale. |
| **9** | **📑 Utgående Faktura, Interne Tjenester & Selvkost** | KOSTRA art 380 (salg til andre kommunale avdelinger) vs art 780 (kjøp fra andre kommunale avdelinger) konsolideringseliminering med verifisert netto `Diff = 0,00 kr`. IKS-forskriften § 20-1 armlengdes prinsipp for interkommunale selskaper, formålsbyggutleie og selvkostformel med 5-årig fremføring. |
| **10** | **🏛️ Søknader om Midler & Tilskuddsforvaltning** | Inbound statlige tilskudd (IMDi integreringstilskudd år 1–5, Helsedirektoratets toppfinansiering av ressurskrevende tjenester, Miljødirektoratets Klimasats). Outbound kommunale nærings- og kulturtilskudd med 4-trinns utbetalingskontroll og bundne driftsfond jf. Kommuneloven § 14-7. |

---

## 📈 Prescriptive LOY-Simulator & Automatisert Tertialnotat

I **Modul 2 (Tidsserie & Årsprognose)** har systemet en unik prescriptive simulerings- og rapporteringsmotor skreddersydd for økonomikontrollere:

### 1. Left of Year (LOY M9–M12) 4-Slider Kutt- & Tiltakssimulator
Kontrolleren kan justere 4 operative tiltaksspaker i sanntid:
* **Vikar- & Lønnsstopp (0–30 %):** Reduserer personalkostnader på art 1010/1020/1040.
* **Kjøp av Tjenester & Konsulentkutt (0–40 %):** Reduserer art 1270/1300.
* **Aktivitetsreduksjon & Driftskutt (0–25 %):** Reduserer operative variable poster.
* **Direkte Månedlig Fast Kutt (0–500 000 kr/mnd):** Innsparingskrav per måned.

### 2. Sanntids SVG Trajektoriekurve
En Edward Tufte-inspirert SVG-kurve viser den historiske banen fra januar til august (M1–M8), og simulerer to parallelle fremtidige baner frem til 31.12:
1. **Ujustert bane (Status Quo):** Ender i et forventet underskudd på `-3 344 421 kr`.
2. **Tiltaksjustert bane (Prescriptive):** Beregner ny kurve og viser nøyaktig nødvendig innsparing for å lande i balanse.

### 3. Juridisk Handlingsrom: § 14-2 vs. § 14-4 / § 14-6
Tiltakene klassifiseres automatisk etter Kommuneloven:
* **Administrative tiltak (Kommuneloven § 14-2):** Ansettelsesstopp, vikarreduksjon, reise- og kursstopp og restriktiv innkjøpspraksis (innenfor kommunedirektørens fullmakt).
* **Politiske tiltak (Kommuneloven § 14-4 / § 14-6):** Tilleggsbevilgninger, endring av tjenestenivå, nedleggelse av tilbud eller bruk av disposisjonsfond (krever vedtak i Bystyret).

### 4. 5-Stegs Automatisert Tertialnotat Agent
Ved et enkelt klikk genererer systemet et fullstendig, profesjonelt tertialnotat gjennom en 5-trinns prosess:
1. *Aggregerer regnskapstall YTD M1–M8 og LOY-beregninger.*
2. *Ekstraherer aktive simulator-parametere og beregner netto effekt per 31.12.*
3. *Strukturerer saksutredning med hjemmelsforankring etter Kommuneloven § 14-2 og § 14-4.*
4. *Formaterer eInnsyn-godkjent rådgivningsnotat med tabeller og konklusjon.*
5. *Eksportmulighet til 1-klikks PDF (`window.print()`) eller Microsoft Word (`.doc`).*

---

## 🏢 Enterprise AI Suite: Anskaffelser, Selvkost & Tilskudd

Modul 8, 9 og 10 utgjør en fullverdig **Enterprise Suite** for kommunal økonomistyring:

### Offentlige Anskaffelser (Modul 8)
* Følger **DFØs 7-trinnsmodell**: *1. Planlegge -> 2. Konkurransegrunnlag -> 3. Kunngjøre -> 4. Tilbudsåpning -> 5. Tildeling -> 6. Kontrakt -> 7. Kontraktoppfølging*.
* **Terskelverdier 2026**: EØS vare- og tjenestekontrakter (1,5 mill. kr), statlige myndigheter (2,3 mill. kr), bygg- og anleggskontrakter (57 mill. kr), og nasjonal terskelverdi (100 000 kr eks. mva).
* **Maverick Spend Detector**: Identifiserer innkjøp foretatt utenfor inngåtte rammeavtaler for å sikre lojalitet til kommunens innkjøpsavtaler.

### Interne Tjenester & Selvkost (Modul 9)
* **Konsolideringseliminering**: I kommuneregnskapet skal intern omsetning elimineres. Systemet validerer at summen av art **380** (salg internt) og art **780** (kjøp internt) balanserer med netto **0,00 kr**.
* **IKS-forskriften § 20-1**: Sikrer at transaksjoner med interkommunale selskaper (f.eks. IKT, avfall, revisjon) skjer etter armlengdes prinsipp.
* **Selvkostberegning**: Lovpålagt selvkostkalkyle (Vann, Avløp, Renovasjon, Feiing) etter formelen:
  $$\text{Selvkost} = \text{Direkte driftskostnader} + \text{Indirekte kostnader} + \text{Kapitalkostnader (avskrivninger + kalkylerente)}$$
  Inkluderer automatisk oppfølging av selvkostfond og 5-årig fremføringsregel.

### Tilskuddsforvaltning (Modul 10)
* **Inbound Grants**:
  * *IMDi Integreringstilskudd*: 5-årig tilskuddsmodell per bosatt flyktning.
  * *Helsedirektoratet Toppfinansiering*: Ressurskrevende helse- og omsorgstjenester med innslagspunkt (ca. 1,6 mill. kr) og 80 % statlig dekning av overskytende.
  * *Miljødirektoratet Klimasats*: Prosjektbasert investerings- og omstillingstilskudd.
* **Outbound Grants**: Kommunale nærings- og kulturtilskudd med 4-trinns utbetalingskontroll (Vedtak -> Dokumentert fremdrift -> Sluttregnskap -> Utbetaling).
* **Bundne driftsfond (§ 14-7)**: Sikrer at ubrukte øremerkede midler avsettes til bundet fond og ikke blandes med fritt disposisjonsfond.

---

## ⚡ FastAPI REST Backend & API-Katalog

FastAPI-backend-en (`src/api_server.py`) kjører asynkront på port 8000 og leverer 10 produksjonsklare endepunkter dokumentert via Swagger UI (`http://localhost:8000/docs`):

| Endepunkt | Metode | Beskrivelse |
| :--- | :---: | :--- |
| `/api/v1/monthly-report` | `GET` | Henter siste månedsrapport for valgt utvalg: YTD, EOY, månedsserie, konto-/funksjonsdrivere og tilgjengelige sektor-/ansvarsstedsvalg. Parametrene `sektor` og `ansvar` kan settes til `ALL` eller avgrenses til én verdi. Dette er kun en oppsummering av sektorene som faktisk finnes i DuckDB; den skal ikke tolkes som garanti for full kommunedekning. |
| `/api/pipeline/status` | `GET` | Returnerer status for DuckDB, modelltrening og filantall i `data/raw` (21) og `data/localblob` (42). |
| `/api/pipeline/run` | `POST` | Kjører end-to-end datapipeline (DuckDB Medallion ETL og MLOps retrain). |
| `/api/eac/forecast` | `POST` | Beregner EAC/ETC basert på YTD-tall og simulerte kuttspaker (vikar, kjøp, drift, fast kutt). |
| `/api/notat/generate` | `POST` | Genererer strukturert, eInnsyn-godkjent rådgivnings- og tertialnotat. |
| `/api/presidio/anonymize` | `POST` | Skrubber sensitive personopplysninger (Fødselsnummer, Ansattnummer, Navn) via Presidio Gateway. |
| `/api/rag/search` | `POST` | Hybrid RAG-søk i kommunal kunnskapsbase (BM25 + Vektor + BGE Reranker). |
| `/api/procurement/spend-analysis` | `GET` | Spend analytics og DFØ-terskelkontroll fordelt på leverandører og kontrakter. |
| `/api/procurement/maverick-spend` | `GET` | Detekterer avvikende innkjøp utenom rammeavtale. |
| `/api/internal-services/elimination-report` | `GET` | Konsolideringsrapport for art 380 vs. 780 (`Diff = 0,00 kr`). |
| `/api/internal-services/selvkost-calc` | `POST` | Beregner lovpålagt selvkost for VAR-sektoren med kalkylerente og fondsavsetning. |
| `/api/grants/inbound-compliance` | `GET` | Etterlevelsesstatus og refusjonskrav for statlige tilskudd (IMDi, Helsedir, Klimasats). |
| `/api/grants/outbound-status` | `GET` | Status og utbetalingskontroll for kommunale tildelinger. |

---

## 🎨 Designstandarder: Edward Tufte & FAST Modeling

Prosjektet er bygget strengt etter to kompromissløse standarder for finansiell analyse og brukergrensesnitt:

### 1. Edward Tufte Data-Ink Ratio
* **Maksimal Data-Ink**: Ingen unødvendige dekorative ikoner, ingen tunge bakgrunnsskygger eller unødvendige fargeblokker.
* **Ingen vertikale rutenettlinjer**: Tabeller og oversikter benytter subtile horisontale skillelinjer (`#1E293B` / `#E2E8F0`).
* **Muted fargepalett**: Nøytrale skifer- og gråtoner i bakgrunn og struktur. Sterke farger (rødt og gult) reserveres eksklusivt for aktive avvik og risikopunkter.
* **Typografi & Justering**: Tekst- og kodekolonner er alltid venstrejustert. Tall og beløp er konsekvent høyrejustert med faste desimaler.
* **Tufte Bullet Charts**: Kompakte, horisontale stolpediagrammer som erstatter tradisjonelle overlessede målere.
* **Tema-støtte**: Sømløs veksling mellom **Slate Dark Mode** (`#090D16`) og **Crisp Light Mode** (`#F8FAFC`).

### 2. FAST Standard Financial Modeling (`Excel-Reporting-Analysis.xlsb`)
* **F**lexible, **A**ppropriate, **S**tructured, **T**ransparent:
* Én felles beregningsformel per rad som kopieres konsistent på tvers av tidsaksen.
* Tydelig fargekoding: Hardkodede forutsetninger i blå skrift (`#0000FF`), beregninger i sort (`#000000`).
* **`06_CHECKS` fane**: 11 uavhengige kontroller og en `MASTER_CHECK` som verifiserer balanse- og konsolideringslikheter (`Diff = 0,00 kr`).

---

## 🤖 MLOps & Modellportefølje

Modellene i `models/` overvåkes kontinuerlig mot modelldrift og trenes via `src/retrain_pipeline.py`:

| Modell | Algoritme | Ytelse / Metrikk | Formål |
| :--- | :--- | :--- | :--- |
| **Prognosemodell** | `RandomForestRegressor` | $R^2 = 0.9758$, $\text{MAE} = 1\,655\text{ kr}$ | Predikere neste måneds forbruk per ansvarsenhet og art. |
| **Tidlig Varsling** | `DecisionTreeClassifier` | `100,0 %` Nøyaktighet | Generere transparente `IF-THEN`-regler for revisjon og politisk saksbehandling. |
| **Profilering** | `AgglomerativeClustering` | 4 klynger | Kartlegge kommunale utgiftsmønstre (Stabil, Vikar/Volatil, Sesong, Avvik). |
| **Avviksdeteksjon** | `IsolationForest` | 113 flaggede avvik ($Z > 2.5$) | Identifisere potensielle feilkonteringer, uforklarte hopp og bilagsfeil. |

---

## 🛡️ GDPR, Presidio PII Gateway & Juridisk Forankring

### Presidio PII Gateway
For å etterleve GDPR artikkel 9 og personopplysningsloven sluses all tekst gjennom **Presidio PII Gateway** før den sendes til LLM- eller analysemoduler:
* **Fødselsnummer (11 siffer)** -> Maskeres til `[FNR]`
* **Ansattnummer (6–8 siffer)** -> Maskeres til `[ANSATTNR]`
* **Personnavn og sensitiv lokasjonsdata** -> Maskeres til `[PERSON]` / `[LOKASJON]`

### Juridisk Forankring
Alle beregninger og notatmaler refererer til gjeldende norsk lovverk:
* **Kommuneloven § 14-2**: Kommunedirektørens administrative budsjettfullmakt.
* **Kommuneloven § 14-4**: Bystyrets bevilgningsmyndighet ved budsjettendringer.
* **Kommuneloven § 14-6**: Krav til årsbudsjettets og handlingsplanens realisme.
* **Kommuneloven § 14-7**: Bundne og ubundne driftsfond.
* **Forskrift om økonomiplan og årsbudsjett (KOSTRA-forskriften)**: Standardiserte arts- og funksjonsinndelinger.

---

## 📂 Mappe- og Filstruktur

```text
Kom - G3/
├── index.html                          # Frittstående Tufte/FAST Web-UI Cockpit (10 moduler, 5 300+ linjer)
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

### Alternativ 1: Web Cockpit med live månedsrapport (Anbefalt)
Dobbeltklikk **`start_web_cockpit.bat`** fra prosjektmappen, eller kjør den i PowerShell:
```powershell
.\start_web_cockpit.bat
```
Skriptet gjenbruker et fungerende månedsrapport-API på `127.0.0.1:8000`; hvis det ikke kjører, starter det FastAPI i et eget konsollvindu. Det venter på at rapportendepunktet svarer før dashboardet åpnes. La API-konsollvinduet stå åpent mens rapporten brukes; stopp serveren med `Ctrl+C` i dette vinduet. Hvis port 8000 er opptatt av en annen tjeneste, viser skriptet en tydelig feil i stedet for å åpne en rapport som ikke kan hente data.

`index.html` kan også åpnes direkte, men den dynamiske månedsrapporten krever at FastAPI kjører. Åpning direkte som `file://` bruker `http://localhost:8000` for API-kall.

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
For å starte REST-API-et separat for testing av integrasjoner:
```powershell
uvicorn src.api_server:app --host 127.0.0.1 --port 8000 --reload
```
Åpne deretter `http://localhost:8000/docs` i nettleseren for interaktiv Swagger-dokumentasjon.

---

### Alternativ 5: Docker Compose
For komplett containerisering i produksjons- eller testmiljø:
```powershell
docker compose up --build -d
```
Tjenester som starter:
* **Streamlit AI Workbench:** `http://localhost:8501`
* **FastAPI Backend:** `http://localhost:8000/docs`
* **MLflow Tracking Server:** `http://localhost:5000`

---

## 🧪 Verifikasjon & Tester

Kjør den automatiserte testsuiten for å verifisere at samtlige 10 REST-endepunkter fungerer 100 %:
```powershell
python -m src.test_api_endpoints
```
*Forventet resultat: `Ran 10 tests in 0.45s - OK (10/10 PASS)`.*

For å verifisere databaseavstemmingen og `06_CHECKS`:
```powershell
python -c "import duckdb; con = duckdb.connect('data/database/kostra_prod.duckdb'); print(con.execute('SELECT COUNT(*) FROM modelready_fact').fetchone())"
```
*Forventet resultat: `(2256,)` rader med `0,0 %` nullverdier.*

---

## 🏛️ Forfatter & Ansvarlig

* **Utvikler & Fagansvarlig:** Frank Ellingsen — Financial Controller & Business Intelligence Specialist.
* **Organisasjon:** Kristiansand kommune / KOSTRA AI Analytics Initiative © 2026.
* **Standarder:** Norsk Lovdata (*Kommuneloven*), DFØ, FAST Standard Organization, Edward Tufte Data-Ink.
