# Master Developer Prompt: Antigravity Enterprise AI Suite

> **Instructions for AI Coding Assistants (Antigravity IDE, Cursor, Windsurf, Claude Code):**
> Copy and paste the prompt below into your workspace to build the complete, production-ready Next.js 14 + FastAPI + DuckDB + ChromaDB application with all 5 core modules.

---

```markdown
You are an expert Principal Software Engineer and Enterprise Architect specializing in Norwegian municipal software (KOSTRA, Framsikt, Visma Gat, Unit4 UBW, Kommuneloven).

Your task is to implement the complete, production-ready codebase for the **Antigravity Enterprise AI Suite** for Norwegian municipalities.

### System Architecture Stack
- **Frontend:** Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, Shadcn UI, Lucide Icons, Tremor Charts.
- **Backend:** FastAPI (Python 3.12), Pydantic V2, AsyncIO, Uvicorn.
- **Database Layer:** DuckDB Medallion Lakehouse (`/data/kostra.duckdb`) with Bronze, Silver, Gold schemas and automated reconciliation (`06_CHECKS`).
- **Vector & RAG Layer:** ChromaDB vector store, BM25 lexical retriever, Cross-Encoder Re-ranker, LangChain / LlamaIndex.
- **ML & Analytics Engine:** Scikit-Learn (RandomForestRegressor, Isolation Forest), MLflow Tracking (`sqlite:///mlflow.db`).
- **Security:** Presidio PII Masking, Entra ID RBAC, NOARK 5 Audit Logger.

---

### Core App Modules to Build:

1. **Executive Avviks- & LOY-Cockpit (`/dashboard`):**
   - YTD Budget vs. Actuals table with Edward Tufte Bullet Charts.
   - Left-of-Year (LOY M9–M12) required monthly cut-rate calculator.
   - Traffic light indicators (🔴 KRITISK / 🟡 ADVARSEL / 🟢 I RUTE).

2. **Prescriptive "Neste Års Budsjett+" Simulator (`/simulator`):**
   - Interactive sliders for position freeze (0–6 months), substitute cap (0–100%), and overtime reduction.
   - Real-time recalculation of next year's salary growth, KLP/SPK pension, and AGA.
   - Prescriptive scenario comparison vs. municipal saving goals.

3. **Offentlige Anskaffelser & Spend Analytics Modul (`/procurement`):**
   - DFØ 7-step process tracker.
   - Threshold enforcer (500k, 1.3M, 2.5M, 62.9M EØS).
   - Maverick spend detector cross-referencing ERP invoices against approved framework contracts.
   - Supplier category management & ESG/Seriøsitetskrav tracking.

4. **Utgående Faktura, Interne Tjenester & Selvkost Modul (`/invoicing`):**
   - Billing engine for internal deliveries (Byggservice, Felleskjøkken, IT), IKS/Vertskommune § 20-1, and property leasing (Function 265/130, Art 630).
   - KOSTRA consolidation elimination generator (art 380/780) with 0.00 NOK error margin.
   - Selvkost formula calculator for Water/Sewerage/Waste, Byggesak, and Oppmåling with selvkostfond tracking.

5. **Søknads- & Tilskuddsmodul (`/grants`):**
   - Inbound State & County Grant Application Tracker (Integrering, Voksenopplæring, Funksjonshemming/Toppfinansiering, Utdanning, Regional utvikling, Klimasats, Statsforvalterens Skjønnstilskudd).
   - Outbound Municipal Grant Manager (< 500k lump-sum vs >= 500k 4-installment rule).
   - Earmarked bound operating funds (*bundne driftsfond*) periodization manager.

6. **RAG AI Copilot (`/copilot`):**
   - Hybrid search (Vector + BM25 + Reranker) with zero-hallucination source grounding.
   - 1-Click Tertialnotat & Saksutredning PDF/DOCX exporter.

---

### Implementation Guidelines
1. Ensure all financial calculations assert `Sum(Debit - Credit) == 0.00` (Zero Margin of Error).
2. All UI text must be in professional Norwegian Bokmål using municipal domain terminology.
3. Every generated advisory note must cite exact document names, chapters, and paragraph numbers (e.g. *Kommuneloven § 13-1*, *Anskaffelsesstrategi 2026–2030*, *KOSTRA-forskriften*).
4. Provide Dockerfile and `docker-compose.yml` for unified single-command orchestration (`docker-compose up --build`).
```
