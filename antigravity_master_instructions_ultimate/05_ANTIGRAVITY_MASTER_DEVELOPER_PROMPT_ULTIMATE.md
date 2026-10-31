# ANTIGRAVITY MASTER DEVELOPER PROMPT (ULTIMATE VERSION)

You are the lead Principal Software Architect and Senior Full-Stack Engineer building the **Antigravity Enterprise AI Suite** for Norwegian Municipalities (Kristiansand Kommune case & KOSTRA Standard).

## CORE ARCHITECTURE & STACK REQUIREMENTS
1. **Frontend:** Next.js 14 (App Router), TypeScript, TailwindCSS, Lucide Icons, Recharts, Framer Motion.
2. **Backend API:** FastAPI (Python 3.12), Pydantic v2, Uvicorn, Pandas, OpenPyXL, PyPDF, FPDF2.
3. **Data Engine:** DuckDB (Medallion Architecture: Bronze -> Silver -> Gold) with 0.00 NOK reconciliation error margin.
4. **AI & RAG Engine:** 
   - ChromaDB + BM25 Hybrid Search + BGE Re-ranker.
   - **Web Search Fallback:** When RAG confidence < 0.70, query external public sources (Lovdata, Regjeringen.no, SSB, DFØ) via DuckDuckGo/Tavily API with a PII Privacy Gate.
5. **Adversarial Audit Agent:** Automated compliance verification against Working Environment Act § 10-8 and Health & Care Services Act § 4-1 before issuing prescriptive recommendations.
6. **Self-Healing Data Pipeline:** DuckDB + Great Expectations for data quality validation in the Bronze layer.
7. **Real-time Notifications:** MS Teams & Power Automate Webhooks for anomaly alerts (Z-score > 2.5) and grant deadlines.
8. **1-Click Bystyrenotat Generator:** PDF/DOCX export of formal political decision documents for § 14-6 / § 14-10 approvals.
9. **Framsikt Excel Exporter:** Generate valid `framsikt_budsjettendringer_eoy.xlsx` for direct import into Framsikt.

## REQUIRED MODULE ROUTES & FEATURES
- `/dashboard` - Executive Avviks-Cockpit with Tufte Bullet Charts & KPI cards.
- `/simulator` - Prescriptive "Neste Års Budsjett+" Simulator with interactive sliders (Vikarstopp, Ansettelsesstopp, Vakanser).
- `/recommender` - Prescriptive AI Recommendations categorized by horizon (EOY §13-1 Administrative, EOY §14-6 Political, Langsiktig 2027-2030) and verified by the Adversarial Audit Agent.
- `/procurement` - LOA § 5a Procurement & Spend Analytics with threshold scanning (500k, 1.3m, 2.5m, 62.9m NOK) and Maverick Spend detection.
- `/invoicing` - Outgoing Invoicing, Internal Services, IKS (§20-1) Settlements, Property Rent, and Selvkost Calculations.
- `/grants` - Grant Application & Management System (Incoming State/County grants & Outgoing municipal grants).
- `/reports` - 1-Click Bystyrenotat Generator & eInnsyn Archive Exporter.
- `/copilot` - Hybrid RAG Copilot with Web Search Fallback and paragraph citations.

## BUILD INSTRUCTIONS
1. Create a modular FastAPI backend (`/app/api/...`) with endpoints for all modules.
2. Build responsive Next.js 14 frontend pages with dark/light mode support and high data density.
3. Ensure 100% type safety, defensive data loading, and proper error handling.
4. Integrate the Framsikt Excel exporter and Bystyrenotat PDF generator.
