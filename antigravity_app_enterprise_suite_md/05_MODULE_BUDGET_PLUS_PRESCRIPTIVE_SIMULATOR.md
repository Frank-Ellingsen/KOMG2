# Antigravity Module: Preskriptiv "Neste Års Budsjett+" Simulator

## 1. Concept & Strategic Purpose
While standard budget tools (like Framsikt) handle annual baseline entry, the **Neste Års Budsjett+ Simulator** introduces a **prescriptive, scenario-based planning engine**. It allows municipal directors, CFOs, and unit managers to stress-test staffing, operational cuts, and structural changes *before* freezing the upcoming budget.

---

## 2. Core Simulation Engines

### Engine A: Automated Position Projection (*Fast Lønn - Stillingsfremskrivning*)
* **Baseline Import:** Direct extract of active position records (*stillingshjemler*) from ERP/Framsikt.
* **Dynamic Indexing:** Automatic recalculation of next year's salary growth (deflator/årslønnsvekst), age-based step increases (*aldersansiennitet*), and updated social cost rates:
  $$K_{	ext{total}} = L_{	ext{brutto}} + FP (12\% / 14.3\%) + P (	ext{KLP/SPK}) + AGA (	ext{Sone 1: } 14.1\%)$$
* **Vakans & Naturally Avgang Simulator:** Model the financial savings of leaving vacated positions unfulfilled for 1–12 months or replacing them at lower salary grades.

### Engine B: Turnus-Synchronized Variable Pot Engine (*Variabel Lønn & Gat*)
* **Optur Plus Integration:** Ingestion of simulated shift schedules (*grunnturnus*) from Visma Gat.
* **Empirical Pot Dimensioning:** Replaces subjective estimates for evening, night, and weekend supplements (art 1090) and overtime (art 1040) with exact shift-generated totals.
* **NAV Sick-Leave Offset (Art 1690):** Simulated sick-leave scenarios paired with automatic NAV reimbursement projections to calculate true net personal costs.

### Engine C: Prescriptive EOY & Multi-Year Balance Engine
* **Innsparingstakt & Handlingsregler:** Direct testing against the municipality's structural saving targets (e.g., 2.0 MNOK annual AI/automation savings requirement from 2029) and net debt limits (< 8.8 BNOK).
* **Interactive Sliders:** Real-time visual feedback on EOY margins when adjusting:
  - Recruitment freeze duration (0–6 months)
  - Substitute/Vikar cap (0–100%)
  - Overtime reduction target
  - Consultant/External service freeze

---

## 3. Output & eInnsyn Export
* **1-Click Budget Note Generator:** Exports a complete, NOARK 5-compliant decision memo (*rådgivernotat/saksutredning*) with brevhode, charts, financial matrices, and legal references to *Kommuneloven § 14-6*, ready for political submission in the Municipal Council (*Bystyret*).
