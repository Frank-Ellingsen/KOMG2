// src/store/useFilterStore.ts
/**
 * ANTIGRAVITY ENTERPRISE AI SUITE (KOMG2)
 * Global Filter State Management (Zustand Store)
 * Implements 10_ANTIGRAVITY_DYNAMIC_FILTER_CASCADE_SPEC.md & 06_ANTIGRAVITY_MASTER_DEVELOPER_PROMPT_ULTIMATE_V3.md
 * 
 * 100% Dynamic Cascading Filter Architecture across:
 * - 🏠 Min Hverdag (Enhetsleder)
 * - 📊 Budsjett & Simulering (Controller)
 * - 🛒 Innkjøp, Avtaler & Tilskudd (Procurement)
 * - 📑 Saksbehandling & Politikk (Executives)
 */

import { create } from 'zustand';

export interface FilterState {
  // Aktive Filterverdier
  selectedPeriode: string;       // f.eks. "2024_08" eller "ALL" (M01–M08)
  selectedSektor: string;        // f.eks. "Helse og Omsorg" eller "ALL"
  selectedAnsvar: string;        // f.eks. "25310" eller "ALL"
  selectedFunksjon: string;      // f.eks. "254" eller "ALL"
  selectedRagStatus: string;     // f.eks. "0" (Grønn), "1" (Gul), "2" (Rød), "ALL"
  
  // Dynamiske Kaskade-valgmuligheter (Hentes fra DuckDB via /api/v1/analytics/cascading-options)
  availableSektorer: string[];
  availableAnsvarssteder: Array<{ code: string; name: string; sektor: string }>;
  availableFunksjoner: Array<{ code: string; name: string; sektor: string }>;

  // Handlinger (Actions)
  setPeriode: (periode: string) => void;
  setSektor: (sektor: string) => void;
  setAnsvar: (ansvar: string) => void;
  setFunksjon: (funksjon: string) => void;
  setRagStatus: (status: string) => void;
  resetFilters: () => void;
  syncCascadingOptions: () => Promise<void>;
  getActiveFilterPayload: () => Record<string, string>;
}

export const useFilterStore = create<FilterState>((set, get) => ({
  selectedPeriode: 'ALL',
  selectedSektor: 'ALL',
  selectedAnsvar: 'ALL',
  selectedFunksjon: 'ALL',
  selectedRagStatus: 'ALL',

  availableSektorer: ['Helse og Omsorg', 'Oppvekst og Utdanning'],
  availableAnsvarssteder: [],
  availableFunksjoner: [],

  setPeriode: (periode: string) => { 
    set({ selectedPeriode: periode }); 
    get().syncCascadingOptions(); 
  },
  
  setSektor: (sektor: string) => { 
    set({ selectedSektor: sektor, selectedAnsvar: 'ALL', selectedFunksjon: 'ALL' }); 
    get().syncCascadingOptions(); 
  },
  
  setAnsvar: (ansvar: string) => { 
    set({ selectedAnsvar: ansvar, selectedFunksjon: 'ALL' }); 
    get().syncCascadingOptions(); 
  },
  
  setFunksjon: (funksjon: string) => { 
    set({ selectedFunksjon: funksjon }); 
  },
  
  setRagStatus: (status: string) => { 
    set({ selectedRagStatus: status }); 
  },

  resetFilters: () => {
    set({
      selectedPeriode: 'ALL',
      selectedSektor: 'ALL',
      selectedAnsvar: 'ALL',
      selectedFunksjon: 'ALL',
      selectedRagStatus: 'ALL'
    });
    get().syncCascadingOptions();
  },

  syncCascadingOptions: async () => {
    const { selectedPeriode, selectedSektor, selectedAnsvar, selectedFunksjon, selectedRagStatus } = get();
    try {
      const params = new URLSearchParams({
        periode: selectedPeriode,
        sektor: selectedSektor,
        ansvar: selectedAnsvar,
        funksjon: selectedFunksjon,
        rag_status: selectedRagStatus
      });
      const res = await fetch(`/api/v1/analytics/cascading-options?${params.toString()}`);
      if (res.ok) {
        const data = await res.json();
        set({
          availableSektorer: data.sektorer || [],
          availableAnsvarssteder: data.ansvarssteder || [],
          availableFunksjoner: data.funksjoner || []
        });
      }
    } catch (err) {
      console.warn('[useFilterStore] Failed to fetch cascading options from API:', err);
    }
  },

  getActiveFilterPayload: () => {
    const { selectedPeriode, selectedSektor, selectedAnsvar, selectedFunksjon, selectedRagStatus } = get();
    return {
      periode: selectedPeriode,
      sektor: selectedSektor,
      ansvar: selectedAnsvar,
      funksjon: selectedFunksjon,
      rag_status: selectedRagStatus
    };
  }
}));

export default useFilterStore;

