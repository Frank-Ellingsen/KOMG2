# 10_ANTIGRAVITY_DYNAMIC_FILTER_CASCADE_SPEC.md — Fullstendig Dynamisk Filter- og Kaskadearkitektur

## 📌 FORMÅL OG PRINSIPP
I **Antigravity Enterprise AI Suite (KOMG2)** skal **ALLE** moduler, dashbord, maskinlæringsmodeller (XAI), RAG-vektorsøk, rapportgeneratorer (Excel, Word, PowerPoint) og chatbot-responser være **100 % dynamisk synkronisert** mot brukerens aktive filtervalg.

Når brukeren endrer et filter i topplinjen (f.eks. velger *«M01–M08»*, *«Helse og mestring»* eller *«Ansvar 2540»*), skal hele applikasjonen kaskadere og omkalkulere sine data i sanntid.

---

## 🎛️ 1. GLOBAL FILTER STATE MANAGEMENT (Zustand Store)

Frontend benytter en global, reaktiv Zustand-store (`useFilterStore.ts`) som abonneres på av samtlige 4 arbeidsrom (`Min Hverdag`, `Budsjett & Simulering`, `Innkjøp & Tilskudd`, `Saksbehandling & Politikk`) samt chatboten.

```typescript
// src/store/useFilterStore.ts
import { create } from 'zustand';

export interface FilterState {
  // Aktive Filterverdier
  selectedPeriode: string;       // f.eks. "2024_08" (M01–M08)
  selectedSektor: string;        // f.eks. "Helse og mestring" eller "ALL"
  selectedAnsvar: string;        // f.eks. "2540 Pleie og omsorg" eller "ALL"
  selectedFunksjon: string;      // f.eks. "2540" eller "ALL"
  selectedRagStatus: string;     // f.eks. "0" (Grønn), "1" (Gul), "2" (Rød), "ALL"
  
  // Dynamiske Kaskade-valgmuligheter (Hentes fra DuckDB)
  availableSektorer: string[];
  availableAnsvarssteder: string[];
  availableFunksjoner: string[];

  // Handlinger (Actions)
  setPeriode: (periode: string) => void;
  setSektor: (sektor: string) => void;
  setAnsvar: (ansvar: string) => void;
  setFunksjon: (funksjon: string) => void;
  setRagStatus: (status: string) => void;
  resetFilters: () => void;
  syncCascadingOptions: () => Promise<void>;
}

export const useFilterStore = create<FilterState>((set, get) => ({
  selectedPeriode: '2024_08',
  selectedSektor: 'ALL',
  selectedAnsvar: 'ALL',
  selectedFunksjon: 'ALL',
  selectedRagStatus: 'ALL',

  availableSektorer: [],
  availableAnsvarssteder: [],
  availableFunksjoner: [],

  setPeriode: (periode) => { set({ selectedPeriode: periode }); get().syncCascadingOptions(); },
  setSektor: (sektor) => { set({ selectedSektor: sektor, selectedAnsvar: 'ALL', selectedFunksjon: 'ALL' }); get().syncCascadingOptions(); },
  setAnsvar: (ansvar) => { set({ selectedAnsvar: ansvar, selectedFunksjon: 'ALL' }); get().syncCascadingOptions(); },
  setFunksjon: (funksjon) => { set({ selectedFunksjon: funksjon }); },
  setRagStatus: (status) => { set({ selectedRagStatus: status }); },

  resetFilters: () => {
    set({
      selectedPeriode: '2024_08',
      selectedSektor: 'ALL',
      selectedAnsvar: 'ALL',
      selectedFunksjon: 'ALL',
      selectedRagStatus: 'ALL'
    });
    get().syncCascadingOptions();
  },

  syncCascadingOptions: async () => {
    const { selectedPeriode, selectedSektor, selectedAnsvar } = get();
    const res = await fetch(`/api/v1/analytics/cascading-options?periode=${selectedPeriode}&sektor=${selectedSektor}&ansvar=${selectedAnsvar}`);
    const data = await res.json();
    set({
      availableSektorer: data.sektorer,
      availableAnsvarssteder: data.ansvarssteder,
      availableFunksjoner: data.funksjoner
    });
  }
}));
```

---

## ⚡ 2. DYNAMISK BACKEND ENGINE (DuckDB SQL + Parameterized Filters)

Hvert API-kall mot backend tar imot filterparameterne og genererer parametriserte DuckDB SQL-spørringer mot `modelready_fact`.

### Dynamic Query Builder (FastAPI / Python)

```python
# backend/services/duckdb_engine.py
import duckdb
from typing import Dict, Any, Optional

conn = duckdb.connect("./data/modelready_fact.duckdb", read_only=True)

def get_filtered_fact_data(
    periode: str = "2024_08",
    sektor: Optional[str] = None,
    ansvar: Optional[str] = None,
    funksjon: Optional[str] = None,
    rag_status: Optional[str] = None
) -> Dict[str, Any]:
    
    where_conditions = ["periode = ?"]
    params = [periode]

    if sektor and sektor != "ALL":
        where_conditions.append("omrade_navn = ?")
        params.append(sektor)
    
    if ansvar and ansvar != "ALL":
        where_conditions.append("ansvar_kode = ?")
        params.append(ansvar)

    if funksjon and funksjon != "ALL":
        where_conditions.append("funksjon_kode = ?")
        params.append(funksjon)

    if rag_status and rag_status != "ALL":
        where_conditions.append("rag_status = ?")
        params.append(int(rag_status))

    where_clause = " WHERE " + " AND ".join(where_conditions)

    query = f"""
        SELECT 
            COUNT(*) AS total_linjer,
            COALESCE(SUM(budsjett_ytd), 0) AS total_budsjett_ytd,
            COALESCE(SUM(regnskap_ytd), 0) AS total_regnskap_ytd,
            COALESCE(SUM(regnskap_ytd - budsjett_ytd), 0) AS total_avvik_ytd,
            COALESCE(SUM(eac_prognose), 0) AS total_eac,
            COALESCE(AVG(burn_rate_pct), 0) AS avg_burn_rate
        FROM modelready_fact
        {where_clause}
    """
    
    row = conn.execute(query, params).fetchone()
    
    return {
        "total_linjer": row[0],
        "total_budsjett_ytd": row[1],
        "total_regnskap_ytd": row[2],
        "total_avvik_ytd": row[3],
        "total_eac": row[4],
        "avg_burn_rate": row[5]
    }
```

---

## 🧠 3. DYNAMISK ML & XAI (Feature Importance & Decision Tree Filtering)

Maskinlæringsmodellene (Random Forest, Decision Tree, Isolation Forest) tilpasser sine forklaringer dynamisk til det valgte utvalget:

1. **Random Forest Feature Importance:** Når brukeren filtrerer på en enkelt sektor (f.eks. *Helse og omsorg*), rekalkuleres variablenes forklaringstakt (`monthly_delta_regnskap_nok`, `rolling_3m_avg`, etc.) spesifikt for denne sektoren.
2. **Decision Tree Regeltre:** Treet (2 328 rader) filtreres slik at antall linjer i 🟢 Status 0, 🟡 Status 1 og 🔴 Status 2 teller nøyaktig det filtrerte utvalget.
3. **Isolation Forest Avviksdeteksjon:** Flagger de topp 5 % mest unormale føringene *innenfor den valgte sektoren/ansvaret*.

---

## 🤖 4. DYNAMISK CHATBOT & CHROMA RAG CONTEXT INJECTION

Når brukeren stiller et spørsmål til **KOSTRA KI-Saksbehandleren**, sendes gjeldende filtertilstand med i oppslaget:

1. **Metadata-filtrering i ChromaDB:**
   ```python
   # ChromaDB hybrid search filter
   chroma_filter = {}
   if selected_funksjon != "ALL":
       chroma_filter["funksjon_kode"] = selected_funksjon
   ```
2. **System Prompt Dynamic Injection:**
   ```text
   [AKTIV FILTERTILSTAND]:
   • Periode: YTD M01–M08
   • Sektor: Helse og mestring
   • Ansvarssted: 2540 Pleie og omsorg (23 linjer)
   • Avvik i utvalg: -1 393 495 kr (🔴 KRITISK AVVIK)
   ```
   Dette sikrer at chatboten svarer med full forankring i de tallene og kildene brukeren har foran seg på skjermen.

---

## 📑 5. DYNAMISK RAPPORTGENERERING (Excel, Word, PowerPoint)

Rapportgeneratorene (`/api/v1/export/excel`, `/api/v1/export/word`, `/api/v1/export/pptx`) genererer filene ut fra **aktive filtervalg**:

* **Excel Importmal (`framsikt_budsjettendringer_filtered.xlsx`):** Inneholder kun tiltak og budsjettendringer for det valgte ansvarsstedet.
* **Word Saksfremlegg (`saksfremlegg_filtered.docx`):** Skreddersyr politisk innstilling for det spesifikke rammeområdet.
* **PowerPoint Ledelsesdeck (`ledelsespresentasjon_filtered.pptx`):** Genererer 16:9-slider basert på de filtrerte nøkkeltallene.

---

## 🔄 6. REAKTIV SKJERMOPPDATERING PÅ TVERS AV 4 ARBEIDSROM

```
                                [ TOPP-FILTERLINJE ]
            (Periode | Sektor | Ansvarssted | KOSTRA-Funksjon | RAG-Status)
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
         [ useFilterStore ]                           [ DuckDB & FastAPI ]
                   │                                           │
 ┌─────────────────┼─────────────────┬─────────────────┐      │
 ▼                 ▼                 ▼                 ▼      │
🏠 Min Hverdag  📊 Budsjett      🛒 Innkjøp        📑 Saksbeh.│
(Kort & Avvik)  (Simulering)     (LOA/Selvkost)    (Bystyre)  │
 │                 │                 │                 │      │
 └─────────────────┴─────────────────┴─────────────────┘      │
                                   │                          │
                                   ▼                          ▼
                           [ KOSTRA Copilot ] ◄─────── [ ML & RAG Engine ]
```

Når brukeren endrer et filter på én fane (f.eks. i *Budsjett & Simulering*), er filteret umiddelbart aktivt når brukeren veksler over til *Min Hverdag* eller *Saksbehandling & Politikk*.

---
