# Antigravity Enterprise AI Suite: System Overview & Master Architecture

## 1. Executive Summary & Core Vision
The **Antigravity Enterprise AI Suite** is a next-generation, prescriptive decision support system built specifically for Norwegian municipalities (*kommuner*) and county councils (*fylkeskommuner*). Operating on top of the municipality's core ERP (Visma Enterprise / Unit4 UBW), budgeting system (**Framsikt**), and resource management system (**Visma Gat**), Antigravity bridges the gap between historical financial accounting, real-time operational resource management, procurement compliance, revenue/invoicing, and grant funding management.

### Key Value Drivers
* **0.00 NOK Variance Guarantee:** 100% reconciled financial accounting via Medallion Lakehouse (DuckDB) and automated reconciliation checks (`06_CHECKS`).
* **Source-Grounded AI (Zero Hallucination):** Hybrid RAG architecture (Vector Search + BM25 Lexical + BGE Reranker) referencing *Kommuneloven*, *Anskaffelsesloven*, *KOSTRA-forskriften*, *Selvkostforskriften*, and local municipal regulations.
* **Jurisdictional Boundary Enforcement:** Automatic sorting between *Administrative Emergency Measures* (Municipal Director's authority under *Kommuneloven § 13-1*) and *Political Municipal Council Resolutions* (under *§ 14-6 / § 14-10*).
* **Comprehensive Enterprise Module Coverage:**
  1. **Executive Avviks- & LOY-Cockpit** (Real-time Left-of-Year EOY Balance Engine)
  2. **Prescriptive "Neste Års Budsjett+" Simulator** (Position fremskrivning & Gat turnussimulering)
  3. **Offentlige Anskaffelser & Spend Analytics Modul** (DFØ 7-step process & threshold enforcement)
  4. **Utgående Faktura & Selvkost Modul** (Interne/eksterne tjenester, IKS, utleie & selvkostberegning)
  5. **Søknads- & Tilskuddsmodul** (Statlige/fylkeskommunale søknader & kommunal tilskuddsforvaltning)

---

## 2. Technical Stack & Infrastructure Architecture

```
+-----------------------------------------------------------------------------------+
|                            ANTIGRAVITY ENTERPRISE FRONTEND                        |
|   Next.js 14 (App Router) | React 18 | Tailwind CSS | Shadcn UI | Tremor / Lucide   |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼ REST / WebSocket
+-----------------------------------------------------------------------------------+
|                             FASTAPI ENTERPRISE BACKEND                             |
|   Python 3.12 | Pydantic V2 | AsyncIO | Security Gateway | Presidio PII Masking   |
+-----------------------------------------------------------------------------------+
      │                                   │                                   │
      ▼                                   ▼                                   ▼
+-----------------------+   +---------------------------+   +-----------------------+
|  DUCKDB LAKEHOUSE     |   |   HYBRID RAG ENGINE       |   |   MLOPS ENGINE        |
|  • Bronze (stg_fact)  |   |   • ChromaDB / FAISS      |   |   • Scikit-Learn RF   |
|  • Silver (silver_fact)|  |   • BM25 Lexical Search   |   |   • Isolation Forest  |
|  • Gold (star schema) |   |   • Cross-Encoder Reranker|   |   • MLflow Tracking   |
+-----------------------+   +---------------------------+   +-----------------------+
```

### Data Pipeline & Reconciliation Engine
1. **Bronze Layer:** Raw ingestion of monthly CSV/XLSB files from ERP, KOSTRA dimensions, and Framsikt/Gat extracts with automatic account code padding (4->6 digits for accounts, 3->5 digits for functions) and encoding fixes.
2. **Silver Layer:** Reconciled General Ledger with monthly delta calculation (`monthly_delta = YTD_Current - YTD_Previous`).
3. **Gold Layer:** Star schema data warehouse with 32 enriched dimensional variables and 0.0% null values.
4. **06_CHECKS Reconciliation:** Mandatory automated test asserting that `Sum(Debit - Credit) == 0.00` across all account series and KOSTRA functions.

---

## 3. Security, Governance & GDPR Compliance
* **RBAC (Role-Based Access Control):** Entra ID (Azure AD) Single Sign-On mapped to municipal organizational units (Område 10–99, Ansvar 10000–99999).
* **PII Masking (Presidio Filter):** Automatic sanitization of national identity numbers (*fødselsnummer*), employee IDs, and sensitive health/sick-leave text before entering vector databases or AI models.
* **Audit Trail (NOARK 5 Standard):** Comprehensive event logging of all query timestamps, user IDs, retrieved source chunks, and generated advisory notes.
