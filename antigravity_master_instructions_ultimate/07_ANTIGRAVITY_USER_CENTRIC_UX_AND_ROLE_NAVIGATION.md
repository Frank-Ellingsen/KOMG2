# Antigravity Enterprise AI Suite: Brukersentrert UX, Rollebasert Navigasjon og Språkomstilling

## 1. Visjon for Brukervennlighet og Tilgjengelighet
I kommunal virksomhetsstyring er brukerne mangfoldige – fra rektorer, enhetsledere i pleie og omsorg, og kultursjefer, til økonomicontrollere, kommunalsjefer og politikere. De færreste har interesse for teknisk AI-sjargong som «RAG», «MLOps», «Vector Store» eller «Isolation Forest». 

Formålet med denne brukerarkitekturen er å **avmystifisere verktøyet**, fjerne alle tekniske barrierer, og gi hver enkelt bruker en intuitiv, trygg og handlingsrettet opplevelse tilpasset deres rolle og oppgaver i hverdagen.

---

## 2. Rollebasert Navigasjonsstruktur (De 4 Arbeidsrommene)

Applikasjonens hovedmeny struktureres i fire klare arbeidsrom basert på brukerens rolle og formål:

```
+---------------------------------------------------------------------------------------------------+
|                                  ANTIGRAVITY / KOMG2 APP-NAVIGASJON                               |
+-------------------+--------------------+----------------------------+-----------------------------+
| 🏠 1. MIN HVERDAG | 📊 2. BUDSJETT &   | 🛒 3. INNKJØP, AVTALER &   | 📑 4. SAKSER & POLITIKK     |
|    (Enhetsleder)  |    SIMULERING      |    TILSKUDD                |    (Toppledelse/Politikk)   |
|                   |    (Økonomer)      |    (Fagansvarlige)         |                             |
+-------------------+--------------------+----------------------------+-----------------------------+
```

### 🏠 Rom 1: «Min Hverdag» (For Enhetsledere & Virksomhetsledere)
* **Målgruppe:** Rektorer, avdelingsledere i pleie og omsorg, barnehageledere, enhetsledere.
* **Formål:** Gi full oversikt over egen avdeling på 30 sekunder uten kompliserte tabeller.
* **Nøkkelkomponenter:**
  * **Trafikklys-status:** Visualiserer om enheten er i rute (Grønn), har avvik å følge med på (Gul), eller krever umiddelbare tiltak (Rød).
  * **«Hva bør jeg gjøre i dag?»:** Liste med lovlige, administrative tiltak som lederen selv har fullmakt til å gjennomføre strakts (f.eks. *«Inndra ledig stilling på avdeling B»* eller *«Begrens overtid i helgen»* jf. Kommuneloven § 13-1).
  * **Søkefelt i naturlig språk:** Et enkelt tekstfelt på norsk: *«Spør assistenten om din avdeling»* (f.eks. *«Hvorfor har vi merforbruk på vikarer i mars?»*).

---

### 📊 Rom 2: «Budsjett & Simulering» (For Økonomirådgivere & Controllers)
* **Målgruppe:** Økonomirådgivere, økonomisjefer og ledere i planleggingsfasen.
* **Formål:** Analysere helårsprognosen (EOY), kjøre preskriptive simuleringer og eksportere avstemte rammer til Framsikt.
* **Nøkkelkomponenter:**
  * **Prognoseveien (EAC):** Interaktiv graf som viser bokført regnskap YTD mot forventet årsresultat ved årets slutt.
  * **Spaker for «Hva skjer hvis...»:** Interaktive slidere for å teste tiltak:
    * *Vikar- og ansettelsesstopp (0–100 % / 1–6 måneder)*
    * *Overtidsbegrensning og vaktomfordeling via Visma Gat Optur Plus*
    * *Konsulentfrys og utsettelse av driftstiltak*
  * **Framsikt 1-Klikks Eksport:** Genererer ferdig formatert Excel-importfil (`framsikt_budsjettendringer_eoy.xlsx`) med 0,00 kr feilmargin.

---

### 🛒 Rom 3: «Innkjøp, Avtaler & Tilskudd» (For Fagansvarlige & Saksbehandlere)
* **Målgruppe:** Anskaffelsesansvarlige, prosjektledere, saksbehandlere for tilskudd og eiendomsforvaltning.
* **Formål:** Sikre at innkjøp følger regelverket (LOA), maksimere inngående statstilskudd og styre utgående fakturering.
* **Nøkkelkomponenter:**
  * **Avtalekontroll & Terskelverdier:** Automatisk sjekk om et innkjøp krever rammeavtale, nasjonal anbudskonkurranse eller EØS-utlysning.
  * **Søknadsportal (Inngående & Utgående):** Oversikt over statlige/fylkeskommunale midler kommunen kan søke om (f.eks. *Toppfinansiering for ressurskrevende tjenester*, IMDi-integrering), samt utbetalingskontroll for kommunens egne tilskudd.
  * **Selvkost & Eiendomsleie:** Enkel oversikt over husleiekontrakter (formålsbygg og bolig) og selvkostfartøyer (VA/Renovasjon) etter Selvkostforskriften.

---

### 📑 Rom 4: «Saksbehandling & Politikk» (For Kommunalsjefer & Toppledelse)
* **Målgruppe:** Kommunedirektør, kommunalsjefer, politisk sekretariat og bystyremedlemmer.
* **Formål:** Forberede og behandle formelle saker som krever politisk vedtak.
* **Nøkkelkomponenter:**
  * **Saker til politisk behandling:** Oversikt over merforbruk som ikke kan løses administrativt, og som krever formelt bystyrevedtak jf. Kommuneloven § 14-6 (disposisjonsfond) eller § 14-10 (rammeomdisponeringer).
  * **1-Klikks Bystyrenotat Generator:** Utforming av formelt saksfremlegg (PDF/DOCX) med brevhode, juridiske vurderinger og finansielle tabeller, ferdig klargjort for eInnsyn / NOARK 5.

---

## 3. Ordbok for Språkomstilling (Teknisk vs. Brukervennlig)

For å sikre at alle brukere opplever systemet som tilgjengelig, er grensesnittet vasket for teknisk AI- og IT-jargon:

| Tekniske Utvikleruttrykk ❌ | Brukervennlige Uttrykk i Appen ✅ | Forklaring for Brukeren |
| :--- | :--- | :--- |
| **RAG Vector Search Engine** | **Søk i Lovverk & Reglement** | Søker i kommuneloven, KOSTRA, lokal rådsstruktur og økonomireglement. |
| **Preskriptiv LOY-Simulator** | **Budsjettsimulator ("Hva skjer hvis...")** | Viser effekten av ansettelsesstopp eller vikarkutt på årets sluttresultat. |
| **Isolation Forest Anomaly Grid** | **Avviksvarsel & Hendelser** | Oppdager unormale utgiftseksplosjoner på konto eller ansvar. |
| **Audit Agent (AML § 10-8)** | **Automatisk Lovsjekk** | Kontrollerer at kuttforslag ikke bryter Arbeidsmiljøloven eller helselovgivning. |
| **Medallion Gold Layer Export** | **Last ned klar fil til Framsikt** | Eksporterer ferdig Excel-fil klar for innlesning i Framsikt. |
| **Tavily / DuckDuckGo Web Fallback** | **Eksternt Lovdatasøk** | Henter oppdaterte sirkulærer og lovhjemler fra offentlige nettsteder. |
| **PII Privacy Gate / Anonymizer** | **Personvernsjekk (GDPR)** | Skjermer fødselsnumre og navn automatisk før behandling. |

---

## 4. Frontend Mappestruktur (Next.js 14 App Router)

```
src/
├── app/
│   ├── (dashboard)/
│   │   ├── min-hverday/           # Rom 1: Enhetsleder Cockpit
│   │   │   └── page.tsx
│   │   ├── budsjett-simulering/   # Rom 2: Simulator & Framsikt Eksport
│   │   │   └── page.tsx
│   │   ├── innkjop-tilskudd/      # Rom 3: LOA, Faktura & Tilskudd
│   │   │   └── page.tsx
│   │   └── politikk-saksbehandling/ # Rom 4: Bystyrenotater & eInnsyn
│   │       └── page.tsx
│   ├── layout.tsx                 # Hovedlayout med brukersentrert meny
│   └── page.tsx                   # Automatisk omdirigering basert på brukerrolle
```

---

## 5. Designprinsipper & Universell Utforming (WCAG 2.1 AAA)

1. **Klare fargekodede indikatorer:** Grønn, Gul og Rød med tydelige tekstikoner for tilgjengelighet (fargeblindvennlig).
2. **Kildemerking:** Alt innhold fra RAG og AI er merket med *«Hentet fra KOSTRA / Økonomireglementet § X»* for 100 % sporbarhet.
3. **Null hallusinasjon-garanti:** Dersom systemet mangler kildegrunnlag, oppgis det at kilden ikke finnes i kommunens baser, og brukeren tilbys et eksternt Lovdatasøk.
