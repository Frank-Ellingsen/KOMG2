# 🚀 ANTIGRAVITY ENTERPRISE AI SUITE — MASTER DEVELOPER PROMPT (v2.0 Ultimate)

> **Instruksjon for AI-kodingsassistent (Cursor / Antigravity IDE / Windsurf / Claude Code):**  
> Lim inn hele denne spesifikasjonen i Agent/Composer-panelet for å opprette eller oppdatere hele kildekoden til Antigravity Enterprise AI Suite (KOMG2).

---

## 📌 OVERSIKT OG VISJON

Du skal bygge **Antigravity Enterprise AI Suite (KOMG2)** — en uovervinnelig, preskriptiv virksomhetsstyrings- og RAG-plattform for kommunal sektor (eksempelvis Kristiansand kommune).

Systemet kobler sammen tre tidligere adskilte verdikjeder:
1. **Regnskap & Økonomi:** Framsikt AS, Visma Enterprise, Unit4 Business World (UBW), GKRS regnskapsstandard.
2. **Turnus & Bemanningsplanlegging:** Visma Gat (Optur Plus automatisk turnusgenerator, DIGISYFO, MinGat).
3. **Lovverk & Kommunal Styring:** Kommuneloven (§ 13-1 styringsrett, § 14-3 økonomiplan, § 14-6 disposisjonsfond, § 14-10 rammeomdisponering), Anskaffelsesloven (LOA), Selvkostforskriften og KOSTRA-kontoplanen.

---

## 🎨 BRUKERSENTRERT UX & ROLLEBASERT NAVIGASJON (4 ARBEIDSROM)

For at applikasjonen skal være 100 % intuitiv for alle brukere (rektorer, enhetsledere i helse/omsorg, økonomicontrollere, kommunalsjefer), er grensesnittet delt i **4 klare arbeidsrom uten teknisk sjargong**:

```
+---------------------------------------------------------------------------------------------------+
|                                  ANTIGRAVITY / KOMG2 APP-NAVIGASJON                               |
+-------------------+--------------------+----------------------------+-----------------------------+
| 🏠 1. MIN HVERDAG | 📊 2. BUDSJETT &   | 🛒 3. INNKJØP, AVTALER &   | 📑 4. SAKSER & POLITIKK     |
|    (Enhetsleder)  |    SIMULERING      |    TILSKUDD                |    (Toppledelse/Politikk)   |
|                   |    (Økonomer)      |    (Fagansvarlige)         |                             |
+-------------------+--------------------+----------------------------+-----------------------------+
```

### 1. 🏠 Min Hverdag (For Enhetsledere / Virksomhetsledere)
- **Målgruppe:** Rektorer, avdelingsledere i pleie og omsorg, barnehageledere.
- **Formål:** Full operasjonell status på 30 sekunder.
- **Kjernekomponenter:**
  - **Trafikklys-status:** Grønn (I rute), Gul (Følg med), Rød (Tiltak kreves).
  - **«Hva bør jeg gjøre i dag?»:** Praktiske tiltakskort innenfor leders styringsrett (§ 13-1) slik som vikarstopp (*art 1020*), overtidsbegrensning (*art 1040*) og inndragning av ledige hjemler.
  - **Søk i naturlig norsk:** Fritekstfelt for vanlige spørsmål (f.eks. *«Hvorfor har jeg merforbruk på vikarer i mars?»*).

### 2. 📊 Budsjett & Simulering (For Økonomer & Controllere)
- **Målgruppe:** Økonomirådgivere, controllere og ledere som planlegger neste års rammer.
- **Formål:** Modellere helårsprognosen (EOY), kjøre preskriptive «Hva skjer hvis...»-scenarier og eksportere til Framsikt.
- **Kjernekomponenter:**
  - **EOY Prognosebane (EAC):** Visuell graf over forventet balanse ved årets slutt.
  - **Interaktive Slidere («Hva skjer hvis...»):** Test ansettelsesstopp (1–6 mnd), vikar- og overtidsstopp i sanntid.
  - **1-Klikks Framsikt Eksport:** Genererer `framsikt_budsjettendringer_eoy.xlsx` ferdig formatert for direkte import til Framsikt.

### 3. 🛒 Innkjøp, Avtaler & Tilskudd (For Innkjøpere & Fagansvarlige)
- **Målgruppe:** Innkjøpere, prosjektledere, saksbehandlere for tilskudd og selvkost.
- **Formål:** LOA-terskelkontroll, avtalesjekk, tilskuddsforvaltning og selvkostberegninger.
- **Kjernekomponenter:**
  - **Innkjøpssjekk (LOA):** Terskelkontroll (<500k, 500k–1,3m, EØS 2,5m/62,9m), 30 % miljøvektlegging og Maverick spend-deteksjon.
  - **Tilskuddsportal:** Inngående statlige/fylkeskommunale midler (IMDi, Udir, Toppfinansiering for ressurskrevende tjenester) og utgående kommunale tilskudd (500k-regel for utbetaling).
  - **Fakturering & Selvkost:** Selvkostfond (VA/Renovasjon), husleie for formålsbygg og interkommunal KOSTRA-konserneliminering (IKS / Vertskommune § 20-1).

### 4. 📑 Saksbehandling & Politikk (For Toppledelse & Bystyre)
- **Målgruppe:** Kommunedirektør, kommunalsjefer og politisk sekretariat.
- **Formål:** Forberede og eksportere formelle saker til politisk behandling (Formannskap / Bystyret).
- **Kjernekomponenter:**
  - **Politisk Vedtaksbrett:** Sortering av avvik som krever bystyrevedtak (§ 14-6 bruk av disposisjonsfond, § 14-10 rammeomdisponering).
  - **1-Klikks Saksfremlegg Generator:** Genererer ferdige DOCX/PDF-saksnotater med kommunalt brevhode, finansiell tabell og lovhjemler ferdig for eInnsyn / NOARK 5.

---

## 🔤 SPRÅKOMFORKLARING I BRUKERGRENSESNITTET

Alle knapper og etiketter skal benytte forståelig norsk:
- `RAG Vector Search Engine` ➔ **Søk i Lovverk & Reglement**
- `Isolation Forest Anomaly Grid` ➔ **Avviksvarsel & Viktige Hendelser**
- `Preskriptiv LOY-Simulator` ➔ **Budsjettsimulator ("Hva skjer hvis...")**
- `Audit Agent (AML § 10-8)` ➔ **Automatisk Lovsjekk (Arbeidsmiljøloven)**
- `Medallion Gold Layer Export` ➔ **Last ned klar fil til Framsikt**

---

## 🏗️ TEKNISK ARKITEKTUR OG MAPPESKEMA

- **Frontend:** Next.js 14 App Router, Tailwind CSS, Shadcn UI, Lucide Icons, Recharts (Tufte Bullet Charts).
  - Mappestruktur:
    - `/src/app/(dashboard)/my-day/` (Min Hverdag)
    - `/src/app/(dashboard)/budget/` (Budsjett & Simulering)
    - `/src/app/(dashboard)/procurement/` (Innkjøp & Tilskudd)
    - `/src/app/(dashboard)/governance/` (Saksbehandling & Politikk)
- **Backend:** FastAPI (Python 3.12), Pydantic v2, DuckDB Medallion Lakehouse (Bronze / Silver / Gold).
- **Søk & RAG:** ChromaDB + BM25 Hybrid Search + BGE Re-ranker.
- **Eksternt Søk:** DuckDuckGo / Tavily API Fallback med PII Privacy Gate ved lav treffskår (< 0.70).
- **Sikkerhet & Revisjon:** Revisor-agent (krasjtester kutt mot AML § 10-8 hviletid og Helse- og omsorgsloven § 4-1 forsvarlighet) og Presidio PII-skjerming.

---

## 📋 DEVELOPMENT INSTRUCTIONS FOR CODE AGENT
1. Generate the Next.js 14 frontend route structure matching the 4 workspaces.
2. Build FastAPI endpoints for `/api/v1/recommendations`, `/api/v1/simulator`, `/api/v1/procurement`, `/api/v1/grants`, and `/api/v1/export/framsikt`.
3. Configure DuckDB pipelines to process KOSTRA fact CSVs and generate Medallion Gold tables with 0.00 NOK error margin.
4. Include docker-compose.yml for 1-command startup (`docker-compose up --build`).
