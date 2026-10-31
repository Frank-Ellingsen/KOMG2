# ⚙️ Antigravity Backend API & MLOps Infrastructure Specification

## 1. REST API Endepunkter (FastAPI)

### A. Data & Finans Endepunkter
- `GET /api/v1/summary`: Henter overordnet YTD- og EOY-status for kommunen/området.
- `GET /api/v1/deviations`: Henter KOSTRA-avviksliste med Z-score og statusflagg.
- `POST /api/v1/simulate-loy`: Mottar simuleringsparametere (vikarstopp, ansettelsesstopp) og returnerer ny EOY-prognosevektor.

### B. AI & RAG Endepunkter
- `POST /api/v1/chat`: Mottar brukerens spørring, kjører PII-anonymisering, utfører Hybrid RAG-søk (ChromaDB + BM25 + BGE Reranker), og strømmer kildegrunnet svar.
- `POST /api/v1/generate-report`: Genererer et ferdig tertialnotat (PDF/DOCX) for en valgt enhet.

### C. MLOps & Observability Endepunkter
- `POST /api/v1/retrain`: Utløser om-trening av RandomForestRegressor og Isolation Forest på nye regnskapsfiler.
- `GET /api/v1/mlflow/metrics`: Returnerer feilmarginer ($R^2$, RMSE) og Model Drift status.

---

## 2. Hybrid RAG Pipeline Specification

```python
# Hybrid Search Logic: BM25 + Vector + BGE Reranker
def hybrid_rag_query(query_text: str, top_k: int = 5):
    # 1. PII Anonymization
    clean_query = presidio_anonymize(query_text)
    
    # 2. Vector Search (ChromaDB)
    vector_results = vector_db.similarity_search(clean_query, k=20)
    
    # 3. BM25 Lexical Search (Exact match on accounts, statutes, articles)
    bm25_results = bm25_index.search(clean_query, top_k=20)
    
    # 4. Merge & Reciprocal Rank Fusion (RRF)
    candidate_chunks = combine_rrf(vector_results, bm25_results)
    
    # 5. Cross-Encoder Re-ranking (bge-reranker-large)
    final_chunks = bge_reranker.rank(query=clean_query, documents=candidate_chunks, top_n=top_k)
    
    return final_chunks
```

---

## 3. Security, PII & Audit Logging
- **Entra ID (Azure AD) SSO:** Rollebasert tilgangskontroll (RBAC) der enhetsledere kun ser sine egne ansvarsnumre, mens direktører ser hele konsernet.
- **Audit Logging:** Hver eneste AI-spørring logges til `data/logs/audit_trail.json` med tidsstempel, bruker-ID, uthentede kildedokumenter og benyttet tokenforbruk.
