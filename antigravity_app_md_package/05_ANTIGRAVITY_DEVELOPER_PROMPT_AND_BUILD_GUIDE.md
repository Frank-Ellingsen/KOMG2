# 🛠️ Antigravity Developer Master Prompt & Build Guide

## 1. Master Prompt for Agentic IDE (Antigravity / Cursor / Windsurf)

Dersom du ønsker at en AI-utviklerassistent (Antigravity IDE / Cursor / Windsurf / Claude Engineer) skal bygge den komplette applikasjonen fra bunnen av, kan du lime inn følgende Master Prompt:

```markdown
PROMPT FOR ANTIGRAVITY AGENTIC IDE:

"Du er en Principal Full-Stack & AI Engineer. Din oppgave er å bygge 'Antigravity KOSTRA AI Workbench' – en produksjonsklar webapplikasjon for kommunal økonomistyring i Kristiansand kommune.

Følg instruksjonene i spesifikasjonsfilene i denne mappen:
- 01_ANTIGRAVITY_APP_VISION_AND_ARCHITECTURE.md
- 02_ANTIGRAVITY_FRONTEND_SPEC_AND_COMPONENTS.md
- 03_ANTIGRAVITY_BACKEND_API_AND_MLOPS.md
- 04_ANTIGRAVITY_AGENTIC_WORKFLOWS_AND_PROMPTS.md

TEKNOLOGISTACK:
- Frontend: Next.js 14 (App Router), React 18, Tailwind CSS, Framer Motion, Lucide-React, Recharts.
- Backend: FastAPI (Python 3.12), DuckDB, ChromaDB, Scikit-Learn, PyCaret, Presidio, MLflow.
- Data Integration: DuckDB Medallion Lakehouse (Bronze -> Silver -> Gold).

KRAV TIL GJENNOMFØRING:
1. Bygg et Tufte-inspirert executive dashboard med mørkt og lyst tema.
2. Implementer preskriptiv 'Hva skjer hvis' LOY-simulator med sanntids slidere.
3. Sett opp kildeforankret RAG Copilot med Hybrid Search (BM25 + Vector) og sidetallshenvisninger.
4. Etabler 1-klikks PDF-generering av tertialnotater med brevhode og avvikstabeller.
5. Sørg for at alle finansielle tall stemmer overens med 0,00 kr feilmargin mot DuckDB."
```

---

## 2. Struktur på Prosjektmappen (Recommended Folder Layout)

```
antigravity-kostra-app/
├── frontend/                     # Next.js 14 Frontend App
│   ├── app/                      # App Router (dashboard, simulator, copilot, reports)
│   ├── components/               # React UI komponenter (TufteCharts, LOYSlider, RAGChat)
│   ├── lib/                      # API-klienter og utility-funksjoner
│   └── public/                   # Statiske ressurser og ikoner
├── backend/                      # FastAPI Python Backend
│   ├── main.py                   # FastAPI Hovedapplikasjon
│   ├── api/                      # REST Endepunkter (finans, RAG, simulering)
│   ├── services/                 # DuckDB engine, Hybrid RAG search, Presidio PII
│   ├── models/                   # RandomForest & Isolation Forest ML-modeller
│   └── data/                     # DuckDB database og ChromaDB vektordatabase
├── docs/                         # Antigravity Spesifikasjonsdokumenter (.md)
├── docker-compose.yml            # Docker orkestrering for full stack
└── README.md                     # Kom i gang-guide for utviklere
```

---

## 3. Kom i Gang på 3 Steg

```bash
# 1. Klon repositoriet og gå til mappen
cd antigravity-kostra-app

# 2. Start hele app-stacken med Docker Compose
docker-compose up --build -d

# 3. Åpne appen i nettleseren
# Frontend: http://localhost:3000
# Backend API (Swagger): http://localhost:8000/docs
# MLflow UI: http://localhost:5000
```
