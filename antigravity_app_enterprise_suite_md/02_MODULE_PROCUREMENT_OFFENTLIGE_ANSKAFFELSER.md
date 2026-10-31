# Antigravity Module: Offentlige Anskaffelser & Spend Analytics

## 1. Regulatory Framework & Municipal Strategy
The Procurement Module is built to enforce compliance with Norwegian public procurement law (*Lov om offentlige anskaffelser - LOA*) § 5a, *Anskaffelsesforskriften*, and local municipal procurement strategies (e.g. *Anskaffelsesstrategi Kristiansand Kommune 2026–2030* for NOK 2.6B annual volume).

### Threshold Values (Terskelverdier - Updated 2026)
| Contract Category | Value Range (excl. VAT) | Applicable Part | Procedure Rules |
| :--- | :--- | :--- | :--- |
| **Micro-procurements** | < 500,000 NOK | Internal Guidelines | Direct purchase with market check |
| **National Threshold (Del I)** | 500,000 NOK – 1.3 MNOK | LOA Part I | Basic principles, non-discrimination |
| **National Threshold (Del II)** | 1.3 MNOK – EØS Threshold | LOA Part I + II | Open / restricted tender competition (§ 8-3) |
| **EØS Goods & Services (Del III)** | >= 2.5 MNOK | LOA Part I + III | EØS publication, open/restricted tender, negotiated |
| **EØS Building & Construction** | 1.3 MNOK – 62.9 MNOK (Del II) / >= 62.9 MNOK (Del III) | LOA Part I + II / III | Open/restricted tender, competitive dialogue |
| **Health & Social Services** | 500,000 NOK – 8.7 MNOK (Del I) / >= 8.7 MNOK (Del IV) | LOA Part I / IV | Dedicated social services procedure |

---

## 2. DFØ 7-Step Standard Process Integration
The module digitizes the official DFØ (*Direktoratet for forvaltning og økonomistyring*) 7-step procurement model:

```
[1. Avklare Behov] ──> [2. Konkurransestrategi] ──> [3. Konkurransegrunnlag] ──> [4. Klargjøre Konkurranse]
                                                                                        │
[7. Følge opp Kontrakt] <── [6. Implementere Kontrakt] <── [5. Gjennomføre Konkurranse] ◄─┘
```

### Core Features
1. **Automated Need & Strategy Builder (Step 1–3):**
   * AI-assisted drafting of open, functional requirements (*åpne behovsbeskrivelser*) to encourage innovation and SME participation.
   * Automatic inclusion of mandatory climate & environmental criteria (minimum 30% weighting or strict environmental specifications jf. LOA § 5).
   * Integration of municipal social responsibility requirements (*seriøsitetskrav* against work crime, apprentice requirements, and human rights in supply chains).

2. **KGS / KAS Integration (Step 4–5):**
   * Seamless API connection to the municipality's Competition & Contract Management System (*Konkurransegjennomførings- og kontraktsadministrasjonsverktøy*).
   * Automated qualification check and ESPD validation.

3. **Active Contract Follow-Up & Audit Trail (Step 6–7):**
   * Price adjustment monitoring according to CPI (*konsumprisindeks*) and contractual index clauses.
   * Whistleblowing channel integration for reporting vendor non-compliance or breach of seriøsitetskrav.

---

## 3. Spend Analytics & Contract Loyalty Engine
* **Maverick Spend Detection:** Real-time cross-referencing between ERP supplier invoices (art 300–380) and approved framework agreements (*rammeavtaler*). Non-contract purchases are flagged immediately.
* **Category Management Dashboard:** Interactive breakdown of spending across supplier categories (IT/Digitalization, Building & Maintenance, Health Services, Consultants, Transportation).
* **Risk & Supplier Analytics:** Vendor concentration risk, financial solidity checks, and ESG compliance scoring.
