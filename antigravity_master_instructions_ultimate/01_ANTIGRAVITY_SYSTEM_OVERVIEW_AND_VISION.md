# Antigravity Enterprise AI Suite: Systemoversikt og Målarkitektur

## 1. Visjon
Antigravity Enterprise AI Suite transformerer kommunal virksomhetsstyring fra reaktiv avviksrapportering til proaktiv, preskriptiv og kildeforankret virksomhetsstyring. Løsningen integrerer regnskapsdata (ERP/DuckDB), turnusdata (Visma Gat/Optur Plus), planlegging (Framsikt) og juridisk regelverk (Kommuneloven, KOSTRA, LOA) i én helhetlig plattform.

## 2. Arkitektur og Hovedkomponenter
- **Frontend:** Next.js 14 (App Router), React 18, TailwindCSS, Lucide Icons, Recharts, Framer Motion.
- **Backend API:** FastAPI (Python 3.12), Pydantic v2, Uvicorn.
- **Data Engine:** DuckDB (Medallion Lakehouse: Bronze -> Silver -> Gold) med 0,00 kr feilmargin og automatisk reconciliasjon.
- **AI & RAG Engine:** 
  - **ChromaDB + BM25 Hybrid Search:** Vektorsøk kombinert med leksikalsk søk for 100 % treffsikkerhet på kontokoder og paragrafer.
  - **BGE Re-ranker:** Re-rangering av søkeresultater.
  - **Web Search Fallback:** Automatisk oppslag mot eksterne offentlige kilder (Lovdata, Regjeringen.no, SSB, DFØ) via DuckDuckGo/Tavily API når interne RAG-treff har skår < 0.70.
  - **PII Privacy Gate:** Presidio/regex-vasking av alle utgående spørringer før de sendes ut av kommunens nettverk.
- **Adversarial Audit Agent ("Revisor-agenten"):** Automatisk juridisk og faglig kontroll av alle preskriptive anbefalinger mot Arbeidsmiljøloven § 10-8 (hviletid), Helse- og omsorgstjenesteloven § 4-1 (forsvarlighet) og KOSTRA-forskriften.
- **Self-Healing Data Quality Pipeline:** DuckDB + Great Expectations for automatisk validering av innkommende CSV/ERP-filer i Bronze-laget.
- **Notification Engine:** Webhooks mot MS Teams og Power Automate for real-time varsling ved utgiftseksplosjoner (Isolation Forest Z-score > 2.5), frister for statlige tilskudd og Model Drift > 20 %.
- **1-Klikks Saksnotat Generator:** Automatisk generering av formelle bystyrenotater (PDF/DOCX) for § 14-6 / § 14-10 vedtak.
