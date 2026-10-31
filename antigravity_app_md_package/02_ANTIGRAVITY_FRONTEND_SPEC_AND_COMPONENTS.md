# 🎨 Antigravity Frontend Specification & Component Blueprint

## 1. Designfilosofi & Visual Design System
- **Estetikk:** Edward Tufte-inspirert datavisualisering – ekstremt høy datatetthet, minimale støy-elementer, krystallklare fargekontraster.
- **Fargepalett:**
  - *Bakgrunn:* Slate/Zinc dark mode (`#090D16` / `#111827`) og crisp light mode (`#F8FAFC`).
  - *Spenning/Kritisk:* Crimson Red (`#EF4444`) for kritiske avvik (Z-score > 2.5, overskridelse > 10%).
  - *Advarsel:* Amber Yellow (`#F59E0B`) for advarsler (Z-score 1.5–2.5).
  - *I RUTE:* Emerald Green (`#10B981`) for budsjettbalanse.
  - *Primær Accent:* Electric Indigo / Cyan (`#6366F1` / `#06B6D4`).

---

## 2. Nøkkelmoduler i Antigravity Appen

### Modul A: Executive Avviks-Cockpit (`/dashboard`)
- **Tufte Bullet Charts:** Viser YTD Regnskap vs. Vedtatt Budsjett per KOSTRA-funksjon og art (Fast lønn 1010, Vikarer 1020, Overtid 1040, Variable tillegg 1090).
- **KPI Summary Cards:** Total YTD-avvik, Projisert EOY-avvik, Antall rødmerkede enheter, Genererte innsparingskrav.
- **Filter-velger:** Filtrer på Område (10 Kommunedirektøren, 2 Oppvekst, 3 Helse & Mestring, etc.), Ansvar og KOSTRA-funksjon.

### Modul B: Preskriptiv "Hva skjer hvis" LOY-Simulator (`/simulator`)
- **Interaktive Slidere:**
  - `Vikarstopp (%)`: 0% til 100% kutt i art 1020.
  - `Overtidsstopp (%)`: 0% til 100% kutt i art 1040.
  - `Ansettelsesstopp (mnd)`: 1 til 4 måneders frys i ledige stillinger.
  - `Konsulentkutt (kr)`: Inndragning av konsulentrammer.
- **Sanntids EOY-graf:** Viser opprinnelig prognosekurve vs. simulert ny bane frem mot 31.12, med krystallklar markering av om enheten når balanse (0,00 kr).

### Modul C: RAG AI Copilot & Saksbehandler (`/copilot`)
- **Chat-grensesnitt:** Kildeforankret dialogvindu med støtte for hurtigknapper:
  - *"Forklar avviket på pleie og omsorg"*
  - *"Hvilke administrative tiltak kan jeg iverksette jf. § 13-1?"*
  - *"Lag utkast til tertialnotat for enhet 25310"*
- **Kildevisning (Citation Drawer):** Viser eksakte kildedokumenter, sidetall og paragrafer som ligger til grunn for svaret.

### Modul D: Early Warning & Anomalideteksjon Grid (`/anomalies`)
- **Isolation Forest Heatmap:** Liste over alle kontokombinasjoner med Z-score > 2.0.
- **Trend-graf:** 12-måneders historisk utvikling med markering av uvanlige utgiftseksplosjoner på overtid eller vikarer.

### Modul E: 1-Klikks Tertialnotat Generator (`/reports`)
- **Eksporteringsknapp:** Genererer ferdig formatert PDF/DOCX saksnotat til eInnsyn/Framsikt med tabeller, grafiske Tufte-diagrammer, årsaksforklaringer og anbefalte vedtak.
