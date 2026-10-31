# Antigravity Module: Web Search Fallback, Self-Healing & Notifications

## 1. Web Search Fallback (DuckDuckGo / Tavily API)
- **Utløser:** Når RAG cosine similarity skår < 0.70 i ChromaDB/BM25.
- **PII Privacy Gate:** Alle fritekstsøk vaskes for ansvarsnummer, personnavn og fødselsnummer via Presidio.
- **Målkilder:** Lovdata.no, Regjeringen.no, SSB.no, DFO.no, KS.no.
- **UI Tagging:** Svar fra websøk merkes tydelig med kildelenke og merket *«Eksternt websøk»*.

## 2. Self-Healing Data Quality Pipeline
- **Validering:** Great Expectations + DuckDB SQL-regler i Bronze-laget.
- **Sjekker:** 
  - Ugyldige 6-sifrede kontokoder mot KOSTRA-kontoplan.
  - Dupliserte bilagsnumre og uavstemte debet/kredit.
  - Manglende ansvarsnummer eller ugyldige funksjonskoder.
- **Self-Healing:** Automatisk korreksjon av periodiseringsfeil og isolering av avviksrader i en avvikstabell uten at hele datalastingen feiler.

## 3. Real-time Notifications (MS Teams / Power Automate)
- **Webhooks:** Senders direkte til kommunens MS Teams-kanal.
- **Triggere:**
  - Utgiftseksplosjon detektert av Isolation Forest (Z-score > 2.5).
  - Søknadsfrist nærmer seg (< 14 dager) for statlige/fylkeskommunale tilskudd.
  - Model Drift overstiger 20 % i MLflow.

## 4. 1-Klikks Bystyrenotat Generator
- **Format:** PDF og DOCX ferdig utformet med kommunens mal og brevhode.
- **Innhold:** Bakgrunn, økonomisk status, Kommunedirektørens forslag til vedtak, konsekvensutredning, og finansiell tabell for Framsikt/eInnsyn.
