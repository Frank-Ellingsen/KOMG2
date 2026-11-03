# ANTIGRAVITY ENTERPRISE AI SUITE — MASTER DEVELOPER PROMPT & SYSTEM SPECIFICATION (v3.0 Ultimate Dynamic Edition)

## 📌 OVERVIEW & CORE MISSION
You are building **Antigravity Enterprise AI Suite (KOMG2)** — a state-of-the-art, prescriptive enterprise governance, ML analytics & RAG platform for Norwegian municipalities (e.g. Kristiansand kommune).

The system integrates:
1. **ERP / Financials:** Framsikt AS, Visma Enterprise, Unit4 Business World (UBW), GKRS accounting standard.
2. **Workforce & Shift Management:** Visma Gat (Optur Plus automatic roster generator, DIGISYFO, MinGat).
3. **Legal & Regulatory Frameworks:** Kommuneloven (§ 13-1, § 14-3, § 14-6, § 14-10), Anskaffelsesloven (LOA), Selvkostforskriften, KOSTRA Chart of Accounts.

---

## 🔄 100 % DYNAMIC CASCADING FILTER ARCHITECTURE
ALL components, dashboards, Machine Learning models (Random Forest, Decision Tree, Isolation Forest), RAG vector retrieval, Chatbot responses, and export generators (Excel, Word, PowerPoint) MUST be **100 % dynamically driven by active filter selection**.

- **Global State Store:** `useFilterStore.ts` (Zustand) managing `periode`, `sektor`, `ansvar`, `funksjon`, `rag_status`.
- **DuckDB Dynamic SQL Engine:** All metrics (`EAC`, `YTD Variance`, `Rolling 3M Run-Rate`, `Burn Rate`) are computed via parameterized SQL with `WHERE` clauses matching active filters.
- **Dynamic ML & XAI:** Feature Importance, Decision Tree classifications, and Anomaly grids dynamically reflect the filtered slice of data.
- **Dynamic RAG & Chatbot Context:** Active filter metadata is injected into ChromaDB vector searches and LLM system prompts.
- **Dynamic Report Exporters:** Excel (`.xlsx`), Word (`.docx`), and PowerPoint (`.pptx`) exports are scoped strictly to the selected filters.

---

## 🎨 USER-CENTRIC UX & ROLE-BASED NAVIGATION (4 WORKSPACES)
1. **🏠 Min Hverdag (Enhetsleder):** Traffic light status, direct executive action cards (§ 13-1), natural language search.
2. **📊 Budsjett & Simulering (Controller):** EOY trajectory, "What-If" sliders (hiring freezes, vacancy freezes), 1-click Framsikt export.
3. **🛒 Innkjøp, Avtaler & Tilskudd (Procurement):** LOA threshold checks (<500k, 500k-1.3m, EØS 2.5m/62.9m), Selvkost funds, Grants portal.
4. **📑 Saksbehandling & Politikk (Executives):** Political reallocations (§ 14-6), 1-click Saksfremlegg generator for eInnsyn/NOARK 5.

---

## 🔤 USER-FRIENDLY LANGUAGE MAPPING
- `RAG Vector Search Engine` ➔ **Søk i Lovverk & Reglement**
- `Isolation Forest Anomaly Grid` ➔ **Avviksvarsel & Viktige Hendelser**
- `Preskriptiv LOY-Simulator` ➔ **Budsjettsimulator ("Hva skjer hvis...")**
- `Audit Agent (AML § 10-8)` ➔ **Automatisk Lovsjekk (Arbeidsmiljøloven)**
- `Medallion Gold Layer Export` ➔ **Last ned klar fil til Framsikt**

---

## 📦 INCLUDED SPECIFICATION FILES
1. `01_ANTIGRAVITY_APP_VISION_AND_ARCHITECTURE.md`
2. `02_ANTIGRAVITY_FRONTEND_SPEC_AND_COMPONENTS.md`
3. `03_ANTIGRAVITY_BACKEND_API_AND_MLOPS.md`
4. `04_ANTIGRAVITY_AGENTIC_WORKFLOWS_AND_PROMPTS.md`
5. `05_ANTIGRAVITY_DEVELOPER_PROMPT_AND_BUILD_GUIDE.md`
6. `06_MODULE_ENTERPRISE_EXTENSIONS.md`
7. `07_ANTIGRAVITY_USER_CENTRIC_UX_AND_ROLE_NAVIGATION.md`
8. `08_OPTIMERING_OG_MAKS_UTBYTTE_AV_RAG_OG_LOCALBLOB_V2.md`
9. `09_EAC_PROGNOSE_OG_SESONGVEKTING_EXPLAINER.md`
10. `10_ANTIGRAVITY_DYNAMIC_FILTER_CASCADE_SPEC.md`

Use this specification to generate the complete codebase with 100% dynamic filter synchronization, precision, zero hallucinations, and exact legal compliance.
