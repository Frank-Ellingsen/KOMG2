# Antigravity Module: Utgående Faktura, Interne Tjenester & Selvkost

## 1. Scope & Functional Overview
The Outgoing Invoicing & Revenue Module (*Utgående Faktura og Inntektsstyring*) manages all outward billing, internal cost reallocations, inter-municipal invoicing, property rentals, and fee-based self-cost services (*selvkost*) in full compliance with *God Kommunal Regnskapsskikk (GKRS)* and *KOSTRA kontoplan*.

---

## 2. Core Billing Categories & KOSTRA Revenue Mapping

### A. Internal Deliveries & Inter-departmental Orders (*Internordre / Oppdragsutgifter*)
* **Scope:** Internal services delivered by municipal production units such as *Byggservice* (janitorial, technical maintenance, cleaning), *Felleskjøkken* (catering to other units), and *IT & Digitalization*.
* **KOSTRA Accounting Rule:** Internal reallocations use dummy account series (art 780 for seller, art 380 for buyer) within the same function or across functions.
* **Automated KOSTRA Consolidation Elimination:** The module automatically generates elimination entries for consolidated reporting to SSB, ensuring internal revenues/expenses do not inflate municipal gross figures.

### B. Inter-municipal Collaboration & Joint Undertakings (*IKS & Vertskommune § 20-1*)
* **Scope:** Services delivered to or received from Inter-municipal Companies (*IKS* - e.g., Fire & Rescue, Waste Management, Audit), Municipal Task Fellowships (*Kommunalt oppgavefelleskap § 19*), and Host Municipality Agreements (*Vertskommunesamarbeid § 20-1*).
* **Billing Flow:**
  - Invoicing for host municipality services (art 350 / 750 or art 330 / 730 for counties).
  - Joint funding contributions (*finansieringsbidrag*) mapped to KOSTRA Function 290 / 465, with mandatory zero-balance reconciliation (`Sum(Expense) == Sum(Revenue)`).

### C. Municipal Property Rental & Facility Leasing (*Kommunal Eiendomsleie*)
* **Scope:**
  1. **Kommunalt disponerte boliger (Function 265, Art 630):** Lease contracts for social housing, refugee housing, and care-home apartments. Automatic indexation according to CPI and Husbanken subsidy integration.
  2. **Formålsbygg & Utleielokaler (Function 130, 221, 222, 261, 381, 386, Art 630/620):** Commercial leasing of municipal facilities, sports halls, cultural centers, and short-term venue rentals.
  3. **Cost-covering Lease Model (*Kostnadsdekkende husleie*):** Full calculation of direct O&M costs, depreciation, and interest to ensure compliance with municipal council yield targets.

### D. Self-Cost Services (*Selvkostområder*)
* **Regulated Fee Areas:** Water (VA), Sewerage, Waste Management, Building Applications (*Byggesak* pbl § 33-1), Property Surveys (*Oppmåling* matrikkelloven § 32), and Zoning Plans (*Regulering*).
* **Selvkost Calculation Formula:**
  $$	ext{Gebyrinntekt} = 	ext{Direkte Driftsutgifter} + 	ext{Indirekte Utgifter (Støttefunksjoner)} + 	ext{Avskrivninger} + 	ext{Kalkulatorisk Rente (5-årig Swap + 0.5\%)}$$
* **Selvkostfond Management:** Automatic allocation of surpluses/deficits to dedicated selvkost funds (*selvkostfond*), with 5-year carry-forward limit enforcement and interest calculation.

---

## 3. Technical Integration & Billing Execution
* **E-Invoicing Standard:** Generation and dispatch of EHF 3.0 (*Elektronisk Handelsformat*) invoices directly to the ELMA registry.
* **Periodization Engine:** Incomes are recognized on the transaction date (*transaksjonstidspunktet* jf. GKRS 11.4), regardless of payment timing or advance billing.
* **Automatic ERP Ledger Postings:** Real-time generation of balanced journal vouchers sent directly to Visma Enterprise / Unit4 UBW via REST APIs.
