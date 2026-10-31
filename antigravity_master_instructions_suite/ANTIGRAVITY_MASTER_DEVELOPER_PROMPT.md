# Antigravity IDE: Master Developer Prompt & Implementation Guide
## Enterprise AI Suite for Kommunal Virksomhetsstyring, Anskaffelser, Fakturering, Tilskudd & Recommender

---

### 🎯 1. System-visjon og Formål

Du skal bygge **Antigravity Enterprise AI Suite (`Kom - G3 / Antigravity Edition`)**, en helhetlig, preskriptiv virksomhetsplattform for norske kommuner. 

Plattformen transformerer kommunal økonomistyring fra reaktiv rapportering til en **proaktiv, kildeforankret AI-cockpit**. Løsningen integrerer regnskapsdata fra ERP (Visma Enterprise / Unit4 UBW), turnus og arbeidstid fra Visma Gat, budsjett og økonomiplan fra Framsikt, samt kildegrunnlag fra lovverk (Kommuneloven, KOSTRA-forskriften, LOA, Selvkostforskriften) og lokale styringsdokumenter.

---

### 🏗️ 2. Målarkitektur og Teknologistack

```
+-----------------------------------------------------------------------------------+
|                        ANTIGRAVITY FRONTEND (Next.js 14 / React)                  |
|  • Dashboard (Tufte Charts)   • Preskriptiv LOY Simulator   • Recommender Matrix   |
|  • Anskaffelser & Spend       • Utgående Faktura & Selvkost • Tilskuddsmodul       |
+-----------------------------------------------------------------------------------+
                                          │ API (REST / WebSockets)
                                          ▼
+-----------------------------------------------------------------------------------+
|                         BACKEND ENGINE (FastAPI / Python 3.12)                    |
|  • DuckDB Medallion Engine    • Hybrid RAG (Vector + BM25) • Isolation Forest ML  |
|  • Framsikt Excel Exporter    • Presidio PII Gateway       • Audit Logger (RBAC)  |
+-----------------------------------------------------------------------------------+
```

* **Frontend:** Next.js 14 (App Router), React 18, Tailwind CSS, Lucide Icons, Recharts / Plotly.js.
* **Backend:** FastAPI (Python 3.12), Pydantic v2, DuckDB (Medallion: Bronze/Silver/Gold), Scikit-Learn, PyCaret, MLflow.
* **RAG & Search Engine:** ChromaDB (Vector DB) + BM25 lexical search + `bge-reranker` (Hybrid Retrieval).
* **Integrasjoner & Eksport:** `openpyxl` (Framsikt Excel Import), `fpdf2` (eInnsyn NOARK 5 saksnotat), REST API mot ERP/Framsikt/Gat.

---

### 📑 3. Modulspesifikasjoner for Antigravity IDE

#### MODUL 1: Preskriptiv LOY-Simulator & "Neste Års Budsjett+" (`/simulator`)
* **Fast lønn (Stillingsfremskrivning):** Importerer stillingshjemler fra ERP/Framsikt, legger inn forventet lønnsvekst (deflator) og rekalkulerer sosiale kostnader (feriepenger 12 % / 14,3 %, KLP/SPK pensjonsinnskudd og AGA ut fra geografisk sone).
* **Variabel lønn (Visma Gat Turnussynkronisering):** Henter vaktmønstre og obskodertid fra Visma Gat (Optur Plus) for å dimensjonere kvelds/helgetillegg (art 1090) og overtid (art 1040) presist før rammene låses.
* **"Hva skjer hvis"-simuleringsmotor:** Interaktive slidere for vikarstopp (0–100 %), ansettelsesstopp (1–6 mnd) og inndragning av vakanser, med sanntidsberegning av Left-of-Year (LOY) kutt-takt og helårseffekt.

#### MODUL 2: Recommender-motor & Tiltaksmatrise (`/recommender`)
Klassifiserer automatiske tiltak ved regnskapsavvik etter **tidshorisont** og **juridisk myndighetsnivå**:
1. **Kortsiktige Administrative Tiltak (EOY / Inneværende år):**
   * *Hjemmel:* Kommunedirektørens og enhetsleders styringsrett jf. *Kommuneloven § 13-1* og kommunens *Økonomireglement*.
   * *Tiltak:* Vikar- og ansettelsesstopp (art 1020), overtidsbegrensning (art 1040), konsulentfrys (art 1270), innkjøps- og utstyrsstopp (art 1200). Kan iverksettes umiddelbart uten bystyrebehandling.
2. **Politiske Vedtak EOY (Inneværende år):**
   * *Hjemmel:* Bystyrets bevilgningsmyndighet jf. *Kommuneloven § 14-6* (disposisjonsfond) og *§ 14-10* (rammeomdisponering).
   * *Tiltak:* Inndragning fra disposisjonsfond (art 1950) eller overføring mellom sektorer (art 1900). Krever formelt Bystyrevedtak før 31.12.
3. **Langsiktige Tiltak (Neste Års Budsjett 2027 & Økonomiplan 2027–2030):**
   * *Hjemmel:* Bystyrets årlige budsjettvedtak jf. *Kommuneloven § 14-3*.
   * *Tiltak:* Bemanningstilpasning ved naturally avgang, KI-gevinstuttak (2,0 mill. kr fra 2029) og endringer i skole-/tjenestestruktur.

#### MODUL 3: Offentlige Anskaffelser & Spend Analytics (`/procurement`)
* **Terskelverdimotor (2026-satser):** Mikroinnkjøp (< 500k kr), Nasjonal terskel (500k–1.3M/2.5M kr jf. LOA Del II) og EØS-terskler (2.5M kr for varer/tjenester, 62.9M kr for bygge/anlegg, 8.7M kr for helse/sosial jf. LOA Del III).
* **Bærekraft & Seriøsitetskrav:** Automatisk innarbeiding av minimum 30 % klima- og miljøvektlegging (LOA § 5), lærlingekrav og seriøsitetsregler mot arbeidslivskriminalitet.
* **Maverick Spend Detection:** Kobler ERP-fakturaer på art 300–380 mot rammeavtale-databasen og flagger kjøp utenfor avtale.

#### MODUL 4: Utgående Faktura, Interne Tjenester & Selvkost (`/invoicing`)
* **Interne Leveranser (Internordre):** Fakturering for interne produksjonsenheter (Byggservice, Renhold, Felleskjøkken, IT-drift) over art 380/780 med automatisk KOSTRA-konserneliminering (0,00 kr feilmargin).
* **Interkommunale Oppgjør (IKS & Vertskommune § 20-1):** Tjenestekjøp/salg mellom kommuner over KOSTRA-funksjon 290/465.
* **Eiendomsleie & Formålsbygg:** Administrasjon av kommunale utleieboliger (Funksjon 265) og formålsbygg (Funksjon 130/221/261) med kostnadsdekkende husleiekalkyle.
* **Selvkostberegning (VA, Renovasjon, Byggesak):** Oppstilling etter *Selvkostforskriften* inkludert direkte/indirekte driftskostnader, kalkulatorisk rente (5-årig swap + 0,5 %) og selvkostfond.

#### MODUL 5: Tilskuddsforvaltning & Søknadsmodul (`/grants`)
* **Inngående Søknader (Kommunen søker Stat/Fylke):** IMDi-integreringstilskudd, Udir-kompetansemidler, Fylkeskommunale regionale utviklingsmidler og Helsedirektoratets *Toppfinansieringsordning for ressurskrevende helse- og omsorgstjenester*.
* **Utgående Tilskudd (Kommunen tildeler midler):** Forvaltning av egne tilskudd til idrett, kultur, frivillighet og bydelsfond med automatisk utbetalingsregel (< 500k kr utbetales 100 % v/start; > 500k kr fordeles over 4 kvartaler).
* **Bundne Driftsfond (Periodisering):** Automatisk avsetning av udisponerte statlige tilskudd til bundne driftsfond jf. *Kommuneloven § 14-7*.

#### MODUL 6: Eksport & Integrasjoner (`/exports`)
* **Framsikt Excel Import Generator:** Ekstraherer godkjente budsjettendringer og Recommender-tiltak direkte til en `openpyxl`-generert `.xlsx`-fil ferdig strukturert for direkte import i Framsikt Årsbudsjett.
* **eInnsyn NOARK 5 Saksnotat Generator:** Genererer PDF-saksnotat med kommunens brevhode, avviksforklaringer, tabeller og juridiske henvisninger for politisk behandling.

---

### 💻 4. Master Developer Prompt for Antigravity / Agentic IDE

Kopier og lim inn følgende prompt direkte i ditt utviklingsmiljø (Antigravity IDE, Cursor, Windsurf, Claude Code):

```text
SYSTEM PROMPT: ANTIGRAVITY ENTERPRISE MUNICIPAL AI SUITE BUILDER

You are an expert Principal Full-Stack Engineer and Municipal Financial Systems Architect. 
Your task is to build the complete, production-ready codebase for the "Antigravity Enterprise AI Suite (Kom - G3)", a prescriptive management system for Norwegian municipalities.

KEY REQUIREMENTS & CONSTRAINTS:
1. STRICT ZERO-HALLUCINATION POLICY: All financial numbers must come directly from DuckDB (Gold Layer). All legal recommendations must be explicitly cited from retrieved sources (Kommuneloven, KOSTRA-forskriften, LOA, Selvkostforskriften, Økonomireglement).
2. BACKEND ARCHITECTURE (FastAPI + Python 3.12):
   - Implement DuckDB database manager for Medallion architecture (Bronze/Silver/Gold).
   - Implement FastAPI REST endpoints for:
     * GET /api/v1/dashboard/anomalies (Isolation Forest + Z-score anomaly detection)
     * POST /api/v1/simulator/budget-plus (Prescriptive "Budget+" simulation with Visma Gat & Framsikt formulas)
     * GET /api/v1/recommender/measures (Categorized measures: EOY Admin §13-1, EOY Political §14-6, Long-term 2027+)
     * GET /api/v1/procurement/spend (LOA thresholds, 30% climate score, maverick spend)
     * POST /api/v1/invoicing/selvkost (Selvkostforskriften calculation & KOSTRA elimination art 380/780)
     * GET /api/v1/grants/toppfinansiering (Innslagspunkt calculation for resource-intensive health services)
     * GET /api/v1/exports/framsikt-excel (Generate openpyxl .xlsx import file)
     * GET /api/v1/exports/einnsyn-pdf (Generate NOARK 5 compliant PDF report)
   - Implement Hybrid RAG Pipeline using ChromaDB + BM25 + Re-ranker.
   - Implement Presidio PII masking on incoming logs and queries.

3. FRONTEND ARCHITECTURE (Next.js 14 + Tailwind CSS + Lucide Icons):
   - Build a modern Edward Tufte-inspired UI dashboard with high data density.
   - Include 5 core views: Dashboard Cockpit, Prescriptive Simulator, Recommender Matrix, Procurement & Invoicing Hub, Grants Manager.
   - Include interactive sliders for LOY cut-rate simulation (overtime, temporary staff, recruitment freeze).

4. MUNICIPAL COMPLIANCE & FORMULAS:
   - Personal costs = Gross Salary + Holiday Pay (12% or 14.3% for 60+) + Pension (KLP/SPK) + AGA (Employer's Tax).
   - KOSTRA elimination: Netting internal sales (art 380) against internal purchase (art 780).
   - Grants payment rule: < 500,000 NOK = 100% upfront; > 500,000 NOK = 4 quarterly installments.

Generate the code structure, backend routers, DuckDB schema, and frontend page components cleanly.
```

---

### 🚀 5. Hurtigstart & Kjøreoppsett

```bash
# 1. Bygg og start hele stacken via Docker
docker-compose -f docker-compose-v2.yml up --build -d

# 2. Re-indekser RAG-databasen med nyeste Markdown-kilder
python ingest_pdf.py

# 3. Kjør om-trening og sjekk Model Drift i MLflow
python retrain_pipeline.py

# 4. Generer Framsikt Excel-importfil
python generate_excel_artifact.py
```
