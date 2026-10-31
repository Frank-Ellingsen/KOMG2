# 🚀 Antigravity AI Workbench: App Vision & System Architecture

## 1. Executive Summary & App Vision
**Antigravity KOSTRA AI Workbench** er en neste-generasjons, AI-native virksomhetsstyrings- og økonomiapplikasjon skreddersydd for Kristiansand kommune og norske kommuner. 

Applikasjonen transformerer tradisjonell, reaktiv økonomirapportering til en **proaktiv, kontinuerlig og preskriptiv styringsplattform**. Ved å kombinere et lynraskt 3-lags Medallion Lakehouse (DuckDB), hybride RAG-søkemotorer (ChromaDB + BM25 + BGE Re-ranker), uovervåket maskinlæring (Isolation Forest & Random Forest) og et Tufte-inspirert executive brukergrensesnitt, gir appen enhetsledere, økonomirådgivere og kommunalsjefer krystallklart besluttelsesgrunnlag for å **snu hver eneste sten** innenfor trygge juridiske rammer.

---

## 2. Overordnet Systemarkitektur

```
+-----------------------------------------------------------------------------------+
|                            ANTIGRAVITY FRONTEND (UX/UI)                          |
|  • Next.js 14 / React 18 / Tailwind CSS / Framer Motion / Lucide Icons           |
|  • Executive Cockpit  • "Hva skjer hvis" LOY-Simulator  • RAG Copilot Chatbot    |
|  • Tufte Bullet Charts  • 1-Klikks Tertialnotat Generator  • Early Warning Grid   |
+-----------------------------------------------------------------------------------+
                                          │
                                 REST / WebSocket API
                                          ▼
+-----------------------------------------------------------------------------------+
|                         ANTIGRAVITY BACKEND (FastAPI / MLOps)                     |
|  • FastAPI (Python 3.12)  • PII Anonymizer (Presidio)  • AI Gateway / Control Plane |
|  • Hybrid RAG Engine (Vector + BM25 + BGE Reranker)  • Isolation Forest Anomaly  |
|  • Random Forest LOY Forecast Engine  • MLflow Observability & Audit Logger       |
+-----------------------------------------------------------------------------------+
                                          │
                                          ▼
+-----------------------------------------------------------------------------------+
|                        DATA & VECTOR LAYER (Medallion DB)                        |
|  • DuckDB (Bronze stg_fact -> Silver silver_fact -> Gold modelready_fact)         |
|  • ChromaDB / FAISS Vektordatabase (Kildedokumenter, Lover & Økonomireglement)     |
+-----------------------------------------------------------------------------------+
```

---

## 3. Nøkkelprinsipper for Antigravity-plattformen

1. **0,00 kr Feilmargin (Reconciled Balance):** Alle finansielle aggregeringer og nøkkeltall hentes direkte fra det avstemte DuckDB Gold-skjemaet med automatiske masterkontroller (`06_CHECKS`).
2. **Kildeforankret AI (Zero Hallucination Guarantee):** AI Copilot og rapportgeneratorer tvinges til å bygge 100 % på verifiserte kilder (Kommuneloven, KOSTRA-forskriften, Økonomireglement for Kristiansand kommune).
3. **Preskriptiv "Hva skjer hvis"-simulering:** Dynamisk LOY-motor (Left-of-Year M9-M12) som beregner eksakt påkrevd kutt-takt og lar lederen simulere vikar- og ansettelsesstopp i sanntid.
4. **Juridisk Myndighetssortering:** Automatisk kildebasert sortering av tiltak:
   - *Administrative strakstiltak* jf. Kommuneloven § 13-1 (styringsrett).
   - *Politiske vedtak* jf. Kommuneloven § 14-6 / § 14-10 (bystyrebehandling).
5. **GDPR & PII-skjerming by Design:** All innkommende tekst filtreres gjennom Presidio anonymiserings-gateway før behandling.
