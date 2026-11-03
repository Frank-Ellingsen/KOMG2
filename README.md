# 🏛️ KOSTRA AI Enterprise Suite — Kristiansand Kommune
### Beslutningsstøtte, Økonomistyring, Månedsavslutning & Framsikt-Integrasjon

> **Utviklet for:** Rådgiver økonomistyring, enhetsledere, kommunalsjefer og økonomidirektøren i Kristiansand kommune.  
> **Formål:** Transformere kommunal økonomistyring fra reaktiv historiefortelling til proaktiv, prediktiv og juridisk forankret virksomhetsstyring.

---

## 🎯 Hva Løser Appen?

I en kommune med milliardomsetning og tusenvis av ansatte er god økonomistyring avgjørende for innbyggernes tjenestetilbud. Likevel møter økonomirådgivere og budsjettansvarlige ofte de samme flaskehalsene:
* **Tunge systemer og forsinkede tall:** Det tar dager å hente ut, rense og koble regnskapsdata fra Agresso og Visma Gat etter månedsslutt.
* **Manuell og tidkrevende avviksoppfølging:** Enhetsledere bruker verdifull tid på å forklare tall de ikke forstår, mens rådgivere må skrive likelydende purringer og månedsnotater fra bunnen av.
* **Uoversiktlig vikarbruk og sykefravær:** Kostbare vikarbyråer (art 1020/1270) og overtid (art 1040) spiser opp rammer uten at kompenserende tiltak iverksettes i tide.
* **Dobbeltarbeid mot Framsikt:** Rådgiveren må manuelt regne ut omdisponeringer i regneark og taste dem inn linje for linje i Framsikt.
* **Frister og lovkrav som glipper:** Komplekse formelle prosesser (tertialrapporter, bystyresaker, revisjonsfrister etter Kommuneloven § 14) koordineres ofte i statiske e-poster og løse notater.

---

### 💡 Løsningen: En Helhetlig Styrings- og Analysearena

Denne applikasjonen fungerer som rådgiverens **digitale co-pilot og operative for-system**. Den automatiserer rutineoppgaver, gir umiddelbar innsikt ved månedsslutt, og bygger bro mellom operative enhetsledere, økonomiavdelingen og politisk ledelse:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        KILDESYSTEMER (Agresso, Visma Gat, Fagsystemer)                 │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Automatisk Ingestion & Avstemming
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│               KOSTRA AI DECISION SUITE (Denne Applikasjonen)                           │
│                                                                                        │
│  💼 Månedsavslutning & Rådgiveroversikt   📅 Årshjul & Lovpålagte Frister (§ 14)       │
│  • Ferdige 1-sides lederrapporter         • 12 måneders styringssyklus                 │
│  • Bitemporal låsing (Diff: 0,00 kr)      • Månedsslutt-sjekkliste med fremdrift       │
│                                                                                        │
│  📑 Framsikt Budsjettregulering           📝 Automatisk Saksdokument-Generator         │
│  • 12-kolonners direkte CSV-eksport       • Ferdig utfylte saksfremlegg (Bystyret)     │
│  • Sanntids balansekontroll (§ 13-1 vs 14-6)• Bestillings- og purrenotater til enheter │
│                                                                                        │
│  📈 Prediktiv Analyse & Simulering        📊 Dyp Utforskning (EDA & FT Visual Guide)   │
│  • EAC/ETC årsprognose med 4 kuttspaker   • Sammenhenger, vikarvolatilitet, trender    │
│  • Forklarbar maskinlæring (XAI)          • Muted Tufte design uten unødig støy        │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ 12-kolonners importfil / Ferdige saksnotater
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│          FRAMSIKT (framsikt.no), BYSTYRET OG AGDER KOMMUNEREVISJON                     │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Brukersentrert UX & Rollebasert Navigasjon (De 4 Arbeidsrommene)

For at applikasjonen skal være 100 % intuitiv og handlingsrettet for alle kommunale roller – fra rektorer og pleieledere til økonomicontrollere, kommunalsjefer og bystyremedlemmer – er grensesnittet inndelt i **4 klare arbeidsrom uten teknisk AI-sjargong** (jf. `06_...` og `07_...`):

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 KOMG2 ROLLEBASERT HOVEDNAVIGASJON                                 │
├───────────────────┬────────────────────┬────────────────────────────┬─────────────────────────────┤
│ 🏠 1. MIN HVERDAG │ 📊 2. BUDSJETT &   │ 🛒 3. INNKJØP, AVTALER &   │ 📑 4. SAKSER & POLITIKK     │
│    (Enhetsleder)  │    SIMULERING      │    TILSKUDD                │    (Toppledelse/Politikk)   │
│                   │    (Økonomer)      │    (Fagansvarlige)         │                             │
└───────────────────┴────────────────────┴────────────────────────────┴─────────────────────────────┘
```

### 🏠 Rom 1: «Min Hverdag» (For Enhetsledere & Rektorer)
* **Målgruppe:** Rektorer, avdelingsledere i pleie og omsorg, barnehageledere og enhetsledere.
* **Formål:** Full operasjonell avdelingsstatus, avviksfordeling, refusjonsavstemming og handlingsrom på under ett minutt.
* **Kjernekomponenter:**
  * **Trafikklys-status (RAG):** Grønn (I rute), Gul (Følg med), Rød (Kritisk avvik / tiltak kreves).
  * **«Hva bør jeg gjøre i dag?»:** 3 prioriterte tiltakskort med lovlige, administrative fullmakter jf. Kommuneloven § 13-1 (vikarstopp art 1020, overtidsbegrensning art 1040 via Visma Gat Optur Plus, vakanssparing).
  * **Månedlig Regnskap & Avviksbane (M01–M08):**
    * Dynamisk **Tufte SVG Sparkline** med budsjett- og regnskapskurve, samt direkte annotering av topp- og bunnmåneder (snitt og maks).
    * Månedlig regnskapstabell med **betingede avvikssøyler (conditional bar length)** og MoM-trend (Måned-over-måned) uten formatstøy.
  * **Avviksfordeling pr. Ansvarssted (Bullet Graph):**
    * Sammenligner alle aktive ansvarssteder i valgt sektor (f.eks. Omsorgssentre og Hjemmetjenester i Helse og Omsorg) ved hjelp av Edward Tufte Bullet Graphs med budsjettmålstrek og regnskapssøyle.
  * **Lønns- og Refusjonsprofil (KOSTRA Art 10xx, 127x mot Art 1710 NAV-Refusjoner):**
    * 4-korts KPI: Brutto personalkostnad, NAV Sykelønnsrefusjon (Art 171000), NAV Foreldrepenger (Art 171005) og Netto personalkostnad etter refusjoner.
    * Transparent varsel om NAV Digisyfo 4–6 ukers saksbehandlingstid.
    * Kostnadsdriver-tabell tilpasset uten rullegardin (ingen vertikal scroll), med direkte innrykk og motregning av Art 1710 under vikarlønn (102000) og vikarbyrå (127040), samt beregning av netto fraværsbelastning.
  * **Største Mindreforbruk (Mindreforbruksanalyse & Bullet Graph):**
    * Viser topp 5 kontoer med mindreforbruk som kan omdisponeres administrativt.
    * **Forsiktighetsprinsipp for inntekter/tilskudd (konto 112098 Tilskudd lærlinger):** Negative regnskapstall ekstrapoleres *ikke* ukritisk til årsslutt; prognosen holdes til faktisk bokført beløp for å unngå urealistisk overbudsjettering.
  * **Dynamisk AI-Tiltaksplan & Tiltakskontrakt:**
    * Genererer en helhetlig tiltakspakke med konkrete månedlige omdisponeringer for å bringe enheten i årsbalanse (0 kr avvik) innenfor Arbeidsmiljølovens guardrails (AML § 10-8).

### 📊 Rom 2: «Budsjett & Simulering» (For Økonomirådgivere & Controllere)
* **Målgruppe:** Økonomirådgivere, økonomisjefer, prosjektcontrollere og virksomhetsstyring.
* **Formål:** Modellere helårsprognosen (EAC/ETC), kjøre bakkeforankrede lønnssimuleringer og eksportere reguleringer direkte til Framsikt.
* **Kjernekomponenter:**
  * **Bakkeforankret Lønns- og Stillingsbudsjett (KOSTRA Art 1010–1099, 1270, 1710):**
    * 100 % dynamisk avstemt mot faktiske innleste data (`KOSTRA_ART_SNAPSHOTS` og `DUCKDB_MONTHLY_REPORT_SNAPSHOTS`):
      * *Totalt for kommunen:* Vedtatt lønnsramme **40 549 437 kr**, brutto YTD **31 314 606 kr**, NAV-refusjoner **-2 382 705 kr**, netto personalkostnad YTD **28 931 901 kr**.
      * *Helse og Omsorg:* Vedtatt ramme **17 612 937 kr**, brutto YTD **13 290 606 kr**, NAV-refusjoner **-732 705 kr**, netto YTD **12 557 901 kr** (168,0 planlagte FTE).
      * *Oppvekst og Utdanning:* Vedtatt ramme **22 936 500 kr**, brutto YTD **18 024 000 kr**, NAV-refusjoner **-1 650 000 kr**, netto YTD **16 374 000 kr** (160,0 FTE).
    * Bemanningsramme-tabell med besatte årsverk, planlagte årsverk, vakanser og gjennomsnittlig brutto månedslønn.
  * **Stillingskategori & Lønnsframskriving 2025 (Framsikt):**
    * Syntetisk stillingsstruktur skalert etter det aktive filterets faktiske fastlønnsbudsjett (Art 1010).
    * Differensierte pensjonsordninger: KS HTA Kap. 3.4/4 med KLP 14,8 % (pleie/omsorg) vs. Statens Pensjonskasse SPK 11,2 % (lærere/skole), pluss Arbeidsgiveravgift AGA 14,1 %.
    * Kommunal deflatorsimulering (lønnsvekst 4,2 % – 5,6 %, glidning og pensjonspremieavvik).
  * **Lønns- & Tariffoppgjørssimulator (What-If):**
    * 4 interaktive parametere: KS tariffoppgjør ramme (% fra 01.05), vikardekningsgrad (%), vakanssparing (mnd) og pensjonspremiesats (KLP/SPK %).
    * Sanntids framskriving av Basislønnsmasse 2024, Lønnsvekst 2025, Sosiale kostnader 2025 og Beregnet Lønnsbudsjett 2025 – perfekt avstemt mot beslutningskortene.
  * **Prognoseveien (EAC/ETC) & LOY-Simulator:**
    * 4-slider kutt-simulator for administrative omdisponeringer (vikarer, overtid, konsulenter, driftsanskaffelser) med sanntids SVG-trajektorie mot årsbalanse.
  * **Framsikt 1-Klikks Eksport:** Genererer `framsikt_budsjettendringer_eoy.csv` (12 kolonner UTF-8 BOM) klar for import i Framsikt.

### 🛒 Rom 3: «Innkjøp, Avtaler & Tilskudd» (For Fagansvarlige & Saksbehandlere)
* **Målgruppe:** Anskaffelsesansvarlige, prosjektledere, saksbehandlere for utgående faktura, tilskuddsforvaltning og selvkost.
* **Formål:** LOA-terskelkontroll, avtalesjekk, konsolideringseliminering, preskriptiv selvkost og ad hoc-fakturering.
* **Kjernekomponenter:**
  * **Innkjøpssjekk (LOA):** DFØ 7-trinns anskaffelsesprosess, terskelkontroll (<500k mikroanskaffelser, 1,3 mill. kr nasjonal terskel, EØS 2,5m/62,9m), 30 % miljøvektlegging (LOA § 5) og Maverick spend-deteksjon.
  * **Preskriptiv Selvkostkalkulator (Forskrift om selvkost FOR-2019-12-11-1738):**
    * Formel: $\text{Gebyrkrav} = \text{Direkte Drift} + \text{Indirekte Støtte} + \text{Avskrivninger} + \text{Kalkulatorisk Rente (5-år Swap} + 0{,}5\,\%) \pm 5\text{-års fondsavsetning}$.
    * Utvidet selvkostområde-dropdown med optgroups for:
      * *Lovregulerte gebyrområder:* Vann og Avløp (Fn 340/345), Renovasjon & Avfall (Fn 350), Byggesaksbehandling (pbl § 33-1, Fn 301), Oppmåling & Kart (matrikkelloven § 32), Feiing & Branntilsyn (brannloven § 28).
      * *Ad hoc Selvkost & Lokalleie:* Skole utleie, Helse utleie, Skole intern lønn, Helse intern personell, Eiendom intern drift.
  * **Ad hoc Faktureringskalkulator for Timepris & Lokalleie (Skole & Helse):**
    * **Intern Selvkost Lønn (Art 780/380):**
      * Beregner full selvkost-timesats (1 650 produktive timer) for spesialpedagog/lærer (538,46 kr/t), musikkpedagog (492,41 kr/t), spesialsykepleier (554,99 kr/t), fysioterapeut (511,92 kr/t), helsefagarbeider (434,66 kr/t) og vaktmester (422,98 kr/t).
      * 1-klikks bokføring som legger internordren rett inn i eliminasjonstabellen med status `🟢 Eliminert` og garanterer netto 0 kr på konsernnivå jf. GKRS og KOSTRA.
    * **Ekstern Lokalleie (Art 1650):**
      * Beregner selvkostleie for gymsal/idrettshall (480 kr/t), auditorium/klasserom (300 kr/t), dagsentersal (350 kr/t) og behandlingsrom (400 kr/t), basert på direkte FDV-tilsyn og kapitalandel.
      * 1-klikks generering av EHF 3.0 Peppol BIS-faktura med Modulus 10 KID, 14 dagers forfall og MVA-unntak jf. merverdiavgiftsloven § 3-11 (utleie av fast eiendom).
  * **Konsolideringseliminering (Art 380 vs 780):** Sanntids eliminasjonstabell som sikrer at interne leveranser (byggdrift, felleskjøkken, IT-drift) har differanse `0,00 kr`.
  * **Tilskuddsportal (Stat & Kommune):** Inngående statlige midler (IMDi integreringstilskudd, Udir kompetanseløft, Toppfinansiering ressurskrevende helsetjenester) og utgående kommunale tilskudd med 4-trinns utbetalingskontroll.

### 📑 Rom 4: «Saksbehandling & Politikk» (For Kommunalsjefer & Bystyre)
* **Målgruppe:** Kommunedirektør, kommunalsjefer, politisk sekretariat og bystyremedlemmer.
* **Formål:** Forberede og behandle formelle saker som krever politisk vedtak.
* **Kjernekomponenter:**
  * **Politisk Vedtaksbrett:** Sortering av avvik som krever formelt bystyrevedtak jf. Kommuneloven § 14-6 (bruk av disposisjonsfond) eller § 14-10 (rammeomdisponeringer).
  * **1-Klikks Saksfremlegg Generator:** Formelle saksnotater (Word `.doc` / A4) med brevhode, finansiell tabell og lovhjemler for eInnsyn / NOARK 5.

---

## 🔤 Ordbok for Språkomstilling (Teknisk ➔ Forståelig Norsk)

Alt innhold i grensesnittet er vasket for teknisk AI- og IT-sjargong for å sikre at alle ledere opplever verktøyet som trygt og umiddelbart tilgjengelig:

| Teknisk Utvikleruttrykk ❌ | Forståelig Uttrykk i Appen ✅ | Forklaring for Brukeren |
| :--- | :--- | :--- |
| **RAG Vector Search Engine** | **Søk i Lovverk & Reglement** | Søker i Kommuneloven, KOSTRA-veilederen og lokalt økonomireglement. |
| **Preskriptiv LOY-Simulator** | **Budsjettsimulator («Hva skjer hvis...»)** | Viser effekten av vikarstopp eller stillingsfrys på årets sluttresultat. |
| **Isolation Forest Anomaly Grid** | **Avviksvarsel & Hendelser** | Oppdager unormale utgiftseksplosjoner på konto eller ansvar. |
| **Audit Agent (AML § 10-8)** | **Automatisk Lovsjekk** | Kontrollerer at kuttforslag ikke bryter Arbeidsmiljøloven eller forsvarlighetskrav. |
| **Medallion Gold Layer Export** | **Last ned klar fil til Framsikt** | Eksporterer 12-kolonners importfil klar for direkte innlesning i Framsikt. |
| **Tavily / DuckDuckGo Web Fallback** | **Eksternt Lovdatasøk** | Henter oppdaterte sirkulærer og lovhjemler fra Lovdata, DFØ og Regjeringen. |
| **PII Privacy Gate / Anonymizer** | **Personvernsjekk (GDPR-sikret)** | Skjermer fødselsnumre, ansattnumre og personnavn automatisk før analyse. |

---

## 🔑 Hovedgevinster i Rådgiverhverdagen

### 1. Lynrask Månedsavslutning mot Budsjettansvarlige
* **3 Predefinerte Standardrapporter:**
  * **1. Enhetslederens Månedsrapport (1 A4-side):** Tilpasset budsjettmøtet. Viser YTD-forbruk, periodisert avvik, vikarandel, overtid, MoM-trend (M08 vs M07) og handlingsrom.
  * **2. Kommunaldirektørens Flash-rapport:** Overordnet sektorstatus, RAG-risikomatrise, de 3 mest kritiske enhetene og anbefalte administrative tiltak.
  * **3. Controllerens Avviks- & Unntaksrapport:** Detaljert revisjonssammendrag for enheter med avvik over 3,0 % eller unormal burn-rate.
* **Automatisert AI-kommentar (NLG):** Tolker tallene i ren tekst etter Kommunelovens prinsipper – sparer rådgiveren for timevis med manuell tekstproduksjon.
* **Bitemporal Snapshot-låsing:** Alle rapporter låses mot DuckDB Gold Layer med revisjonsstempel og `Diff = 0,00 kr`.

### 2. Sømløs Framsikt-Integrasjon (framsikt.no)
* **Predefinerte Reguleringsmaler:**
  * *LOY Helse & Mestring:* Intern omdisponering (kutt i vikar/overtid mot fastlønn, netto 0 kr jf. § 13-1).
  * *LOY Oppvekst & Utdanning:* Vakanssparing og vikardekning i grunnskole (netto 0 kr).
  * *Bystyresak / Disposisjonsfond:* Uforutsett merforbruk finansiert av fond (art 195000 jf. § 14-6).
  * *NAV Refusjonsetterslep:* Teknisk periodisering av sykelønnsrefusjoner (art 1710/1690).
* **Sanntids Balansekontroll:** Viser umiddelbart om en regulering er i balanse (Kommunedirektørens fullmakt) eller krever politisk bystyrevedtak.
* **12-kolonners Eksport:** Genererer ferdig formatert CSV (UTF-8 BOM med semikolon) som importeres direkte i Framsikt uten manuell re-tasting.

### 3. Årshjul for Økonomistyring & Frister
* **Helårlig 12-måneders styringshjul:** Holder oversikt over revisjonsfristen 15. februar (§ 14-8), 1. tertial (T1), 2. tertial (T2), Handlings- og økonomiplan (HØP 2027–2030) og Bystyrets årsbudsjettvedtak før nyttår (§ 14-3).
* **Filtrerbare faser:** Sorter på lovpålagte frister, tertial/årsoppgjør eller politiske bystyremøter.
* **Interaktiv Sjekkliste for Månedsavslutning:** 8 operative kontrollpunkter med sanntids fremdriftsindikator og automatisk lagring i nettleseren (`localStorage`).

### 4. Automatisk Dokument- & Rapportgenerator
* Genererer fullstendige, formelle saksfremlegg og notater med **reelle tall hentet dynamisk fra ditt aktive filter**:
  1. *🏛️ Bystyresak: 2. Tertialrapport og budsjettreguleringer (§ 14-6)* med 4-punkts vedtaksforslag.
  2. *🏢 Bestillingsnotat til Enhetsleder:* Formelt krav om avviksforklaring og EAC-oppdatering ved overskridelse av 3 %-grensen.
  3. *💼 Ledelsesnotat til Kommunalsjef:* Flash-analyse og anbefalte LOY-omdisponeringer.
  4. *📑 Rammebrev HØP 2027–2030:* Deflatorforutsetninger, innsparingskrav og retningslinjer for Framsikt.
  5. *🔒 Årsavslutningsnotat til Revisjon:* Protokoll for overføring og bitemporal avstemming.
* **Handlinger:** Kopier til utklippstavle, last ned som fullverdig Microsoft Word-fil (`.doc`) med brevhode og tabeller, eller skriv ut i A4-format.

### 5. Dyp Datautforskning (EDA) etter Financial Times Visual Guide
* Interaktiv modul basert på *Financial Times Visual Vocabulary*.
* Veileder brukeren i valg av riktig visualisering (Sammenheng, Fordeling, Endring over tid, Avvik, Rangering).
* Inneholder ferdige forslag for kommunale problemstillinger (f.eks. *«Hvordan henger vikarutgifter sammen med overtid og sykefravær i helse og mestring?»*).

---

## 🎛️ Oversikt over Modulene i Appen

Applikasjonen (`index.html`) er bygget som en lynrask, offline-first Single Page Application (SPA):

| # | Modul | Primært formål for rådgiver og leder |
| :-: | :--- | :--- |
| **1** | **💼 Rådgiveroversikt** | Månedsavslutnings-cockpit, 3 predefinerte A4-rapporter, AI-sammendrag, MoM-delta og bitemporalt revisjonsstempel. |
| **2** | **📅 Årshjul, Frister & Dokumenter** | 12-måneders styringshjul, Kommunelov-frister, sjekkliste og 1-klikks generator for formelle saksfremlegg og Word-dokumenter. |
| **3** | **📑 Budsjett & Framsikt Regulering** | Lønns- og rammereguleringer, forhåndsdefinerte kommunale maler, balansekontroll (§ 13-1 vs 14-6) og 12-kolonners CSV-eksport. |
| **4** | **📊 Avviksoversikt (Gold Layer)** | Tufte-bullet charts, RAG-status (rød/gul/grønn), 3M glidende snitt og artsavvik (1010 fastlønn, 1020 vikar, 1040 overtid, 1270 byrå). |
| **5** | **📈 Tidsserie & Årsprognose (EAC)** | 4-slider LOY kutt-simulator, sanntids SVG-trajektorie, månedstak for M9–M12 og juridisk handlingsrom. |
| **6** | **📊 EDA & FT Visual Guide** | Utforskende dataanalyse inspirert av FT Visual Vocabulary med dynamiske scatter-, søyle- og fordelingsgrafer. |
| **7** | **🌲 ML Prognoser & Early Warning** | Forklarbar AI (XAI) basert på Random Forest ($R^2=0.9758$) og beslutningstre med transparente `IF-THEN`-regler for revisjon. |
| **8** | **🚨 Anomaly & Klyngeanalyse** | Klyngeinndeling (Stabil, Vikarvolatil, Sesong, Ekstraordinær) og Isolation Forest for å avdekke bilagsfeil ($Z > 2.5$). |
| **9** | **🎯 Recommender & Tiltaksmatrise** | Konkrete forslag til innsparingstiltak med beregnet sparepotensial, risiko og juridisk hjemmel. |
| **10** | **💬 KI-Saksbehandler & Chatbot** | Presidio PII-sikret rådgiverbot med Hybrid RAG koblet mot Kommuneloven og KOSTRA-veilederen. |
| **11** | **📜 Anskaffelser & Spend (LOA)** | DFØ 7-trinns anskaffelsesprosess, 2026 EØS- og nasjonale terskelverdier og Maverick Spend Detector. |
| **12** | **💳 Faktura, Interne & Selvkost** | Konsolideringseliminering (art 380 vs 780, Diff = 0,00 kr), armlengdes prinsipp (IKS § 20-1) og 5-årig selvkostkalkyle. |
| **13** | **🏛️ Søknader & Tilskudd** | Inbound statlige tilskudd (IMDi, Helsedir, Klimasats) og outbound kommunale tildelinger med 4-trinns utbetalingskontroll. |
| **14** | **⚙️ Modelready Datagrunnlag** | Innsyn i `modelready_fact` og FAST-standardens `06_CHECKS` (11 avstemmingskontroller med Diff = 0,00 kr). |
| **15** | **🎛️ Cockpit & Pipeline Kontroll** | Orkestreringspanel for datastrømmen med live batch-terminal og uforanderlig revisjonslogg. |

---

## 🎨 Design- og Brukergrensesnittstandarder

Applikasjonen følger strenge faglige standarder for datavisualisering og finansiell modellering:

### 1. Edward Tufte Data-Ink Ratio
* **Maksimal Data-Ink:** Ingen unødvendige pynteelementer, tunge skygger eller forstyrrende 3D-effekter.
* **Ingen vertikale tabellinjer:** Bruker diskrete horisontale skillelinjer for å lette lesbarheten.
* **Muted fargepalett:** Nøytrale gråtoner i bakgrunn og struktur. Røde og gule farger reserveres utelukkende for aktive avvik og risikopunkter.
* **Typografi og talljustering:** Tekst er alltid venstrejustert; tall, beløp og prosenter er konsekvent høyrejustert med faste desimaler i monoskrift (`var(--font-mono)`).
* **Tufte Bullet Charts:** Horisontale stolpediagrammer som viser faktisk forbruk mot periodisert budsjett og varslingsterskler på minimal plass.

### 2. FAST Standard Financial Modeling
* **F**lexible, **A**ppropriate, **S**tructured, **T**ransparent.
* Én felles formelstruktur per rad i regnearkmodellene (`Excel-Reporting-Analysis.xlsb`).
* Dedikert **`06_CHECKS`** avstemmingsfane med 11 automatiske kontroller som garanterer at alle konsolideringer og overføringer balanserer til nøyaktig `Diff = 0,00 kr`.

---

# ⚙️ TEKNISK DOKUMENTASJON & ARKITEKTUR

---

## 📐 Medallion Data Lakehouse (DuckDB)

Systemets kjerne er bygget på en **3-lags Medallion Lakehouse-arkitektur** implementert i **DuckDB** (`data/database/kostra_prod.duckdb`):

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        RÅDATA & LOCALBLOB (data/raw & data/localblob)                  │
│                        21 KOSTRA-filer + 42 Blob-filer (CSV, XLSX, TXT)                │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Smart Ingestion, UTF-8/Latin-1, Kodepolstring
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  BRONZE LAYER (stg_fact)                                                               │
│  - Kodepolstring: Konto (4 -> 6 siffer, f.eks. 1010 -> 101000)                         │
│  - Kodepolstring: Funksjon (3 -> 4/5 siffer, f.eks. 120 -> 0120)                       │
│  - Automatisk BOM-stripping, formatvalidering & 0 filer i karantene                    │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ ISO-Datoer & LAG() Window Functions
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  SILVER LAYER (silver_fact & vw_silver_snapshots)                                      │
│  - Avstemt hovedbok over alle regnskapsperioder (M1–M8)                                │
│  - Beregning av reelle månedlige nettotall (monthly_delta)                             │
│  - Bitemporal snapshot-sporing for revisjonskontroll                                   │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ Feature Engineering (32 variabler)
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│  GOLD LAYER (modelready_fact & Star Schema Dimensjoner)                                │
│  - 2 256 rader × 32 features, 0,0 % nullverdier                                        │
│  - Dimensjoner: dim_date, dim_ansvar, dim_kostra_funksjon, dim_kostra_kontoplan        │
│  - 06_CHECKS: 11/11 kontroller godkjent (MASTER_CHECK Diff = 0,00 kr)                  │
└──────────────────┬────────────────────────┬───────────────────────────┬────────────────┘
                   │                        │                           │
                   ▼                        ▼                           ▼
┌────────────────────────────┐ ┌──────────────────────────┐ ┌────────────────────────────┐
│ FastAPI REST API (:8000)   │ │ Frittstående Web Cockpit │ │ Excel & Power BI Suite     │
│ - 34 REST-endepunkter      │ │ (index.html, 5 800+ l.)  │ │ - Excel-Reporting-         │
│ - Presidio PII Gateway     │ │ - 15 interaktive moduler │ │   Analysis.xlsb (FAST)     │
│ - Hybrid RAG (BM25 + BGE)  │ │ - 100 % dynamisk filter  │ │ - pbi-reporting-project    │
│ - 4-veis Intent Routing    │ │ - Framsikt & Årshjul     │ │   (.pbip / TMDL)           │
└────────────────────────────┘ └──────────────────────────┘ └────────────────────────────┘
```

---

## ⚡ FastAPI REST Backend & API-Katalog

FastAPI-serveren (`src/api_server.py`) kjører asynkront og eksponerer produksjonsklare endepunkter dokumentert via Swagger UI (`http://localhost:8000/docs`):

| Endepunkt | Metode | Beskrivelse |
| :--- | :---: | :--- |
| `/api/v1/summary` | `GET` | Hovedoversikt med bitemporal avstemming (`Diff = 0,00 kr`), YTD, EOY og RAG-status. |
| `/api/v1/monthly-report` | `GET` | Henter aggregert månedsrapport: YTD, EOY, månedsserie og artsdrivere. |
| `/api/v1/deviations` | `GET` | Sortert avviksliste pr. ansvarssted, funksjon og KOSTRA-art. |
| `/api/v1/simulate-loy` | `POST` | 4-slider kutt-simulator for administrative omdisponeringer (EAC/ETC-bane). |
| `/api/v1/chat` | `POST` | Presidio-sikret AI-rådgiver med 4-veis Intent Routing, hybrid RAG og kildehenvisninger. |
| `/api/v1/generate-report` | `POST` | Genererer 1-sides månedsnotat, rådmannens flashnotat eller avviksnotat. |
| `/api/v1/mlflow/metrics` | `GET` | MLOps driftmetrikker, modellnøyaktighet ($R^2=0.9758$) og treningslogg. |
| `/api/v1/procurement/contracts` | `GET` | Avtaledekning og leverandørkontrakter med utløpsvarsler. |
| `/api/v1/invoicing/selvkost-calc` | `POST` | Lovpålagt VAR-selvkostkalkyle med 5-års fondsoppfølging (FOR-2019-12-11-1738). |
| `/api/v1/invoicing/internal-eliminations` | `GET` | Sanntids eliminering av interne kjøp/salg (art 380 vs 780, Diff = 0,00 kr). |
| `/api/v1/grants/status` | `GET` | Etterlevelsesstatus og refusjonskrav for statlige tilskudd (IMDi, Udir, Toppfinansiering). |
| `/api/v1/dashboard/anomalies` | `GET` | Isolation Forest bilags- og konteringsavvik ($Z > 2.5$). |
| `/api/v1/simulator/budget-plus` | `POST` | Avansert lønns- og rammesimulator inkludert KLP/SPK pensjon og AGA 14,1 %. |
| `/api/v1/recommender/measures` | `GET` | Preskriptiv tiltaksmatrise med lovhjemler (§ 13-1 vs. § 14-6) og spareeffekt. |
| `/api/v1/procurement/spend` | `GET` | Spend analytics og DFØ-terskelkontroll fordelt på leverandører. |
| `/api/v1/invoicing/selvkost` | `POST` | Ad hoc selvkostkalkulator for intern lønn og ekstern lokalleie (EHF 3.0). |
| `/api/v1/grants/toppfinansiering` | `GET` | Beregning og søknadsgrunnlag for ressurskrevende helsetjenester. |
| `/api/v1/exports/framsikt-excel` | `GET` | 12-kolonners importfil for Framsikt (`framsikt_budsjettendringer_eoy.csv`). |
| `/api/v1/exports/einnsyn-pdf` | `GET` | eInnsyn-klart saksnotat i PDF-format med formelt brevhode. |
| `/api/v1/exports/bystyrenotat-pdf` | `GET` | 1-klikks formelt bystyrenotat i PDF-format med vedtaksforslag. |
| `/api/v1/exports/bystyrenotat-docx`| `GET` | 1-klikks formelt bystyrenotat i Word DOCX-format for saksbehandling. |
| `/api/v1/copilot/query` | `POST` | Copilot v2 Intent Router koblet mot ChromaDB (`kostra_knowledge_base`) og DuckDB. |
| `/api/v1/rag/route` | `POST` | 4-veis Intent Router (`CONCEPTUAL_LEGAL`, `DATA_ANALYTICS`, `PRESCRIPTIVE_HYBRID`, `EXTERNAL_LOOKUP`). |
| `/api/v1/rag/hybrid-query` | `POST` | 5-trinns Hybrid RAG-søk (BM25 + Semantic Cosine + RRF Fusion + BGE Cross-Encoder + Parent-Child). |
| `/api/v1/rag/ingest-localblob` | `POST` | Automatisk indekseringspipeline for 50+ kommunale PDF-er og dokumenter i `localblob/`. |
| `/api/v1/rag/corpus-stats` | `GET` | Kunnskapsbase-statistikk over indekserte chunks, kildedokumenter og bitemporale tidsstempler. |
| `/api/v1/rag/evaluation` | `GET` | MLOps evalueringsmetrikker: Faithfulness (>0.95), Answer Relevance og 100 % Zero Hallucination Rate. |
| `/api/pipeline/status` | `GET` | Returnerer status for DuckDB, modelltrening og filantall i `data/raw` og `data/localblob`. |
| `/api/pipeline/run` | `POST` | Kjører end-to-end datapipeline (DuckDB Medallion ETL og MLOps retrain). |
| `/api/eac/forecast` | `POST` | Beregner EAC/ETC basert på YTD-tall og simulerte kuttspaker. |
| `/api/notat/generate` | `POST` | Genererer strukturert, eInnsyn-godkjent rådgivnings- og tertialnotat. |
| `/api/presidio/anonymize` | `POST` | Skrubber sensitive personopplysninger (FNR, Ansattnr, Navn) via Presidio Gateway. |
| `/api/procurement/maverick-spend` | `GET` | Detekterer avvikende innkjøp foretatt uten gyldig rammeavtale. |
| `/api/grants/inbound-compliance` | `GET` | Etterlevelsesstatus og refusjonskrav for statlige tilskudd. |

---


---

## 🔍 Hybrid RAG & Localblob Kunnskapsmotor (`08_OPTIMERING_OG_MAKS_UTBYTTE`)

For å eliminere hallusinasjoner og sikre at enhver rådgivningstakst og budsjettanbefaling er forankret i faktiske kommunale vedtekter og nasjonale lover, er arkitekturen utvidet med en produksjonsklar **Tre-Pillars Datainfrastruktur** (`src/rag_localblob_engine.py`):

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        TRE-PILLARS DATAINFRASTRUKTUR                                   │
├──────────────────────────┬─────────────────────────────┬───────────────────────────────┤
│ 1. DUCKDB OLAP           │ 2. CHROMA / VECTOR INDEX    │ 3. LOCALBLOB INGESTION        │
│    (Strukturert Gullag)  │    (Ustrukturert Kunnskap)  │    (50+ PDF, MD, CSV)         │
│ • 2 256 regnskapsrader   │ • Parent-Child Chunking     │ • Kommuneloven & forskrifter  │
│ • Bokført M01–M08        │ • Dense Cosine Embeddings   │ • Økonomireglement Krs. sand  │
│ • Avvik & EAC-prognoser  │ • Pure Okapi BM25 Index     │ • KS Lønnsavtaler & KLP/SPK   │
└──────────────────────────┴─────────────────────────────┴───────────────────────────────┘
                                           │
                                           ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        4-VEIS INTELLIGENT INTENT ROUTER                                │
├──────────────────────────┬─────────────────────────────┬───────────────────────────────┤
│ ⚖️ CONCEPTUAL_LEGAL      │ 📊 DATA_ANALYTICS           │ 🔀 PRESCRIPTIVE_HYBRID        │
│    Hjemler, definisjoner │    Faktiske regnskapstall,  │    Kobler regnskapsavvik mot  │
│    og lovkrav (f.eks.    │    perioder, KOSTRA-arter   │    lovlige tiltak (§ 13-1     │
│    bruttoprinsippet)     │    og ansvarsavvik          │    adm. kutt vs. § 14-6 sak)  │
├──────────────────────────┴─────────────────────────────┴───────────────────────────────┤
│ 🌐 EXTERNAL_LOOKUP                                                                    │
│    Fallback til offisielle portaler (lovdata.no, dfo.no, regjeringen.no, ssb.no)       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Kjernekomponenter i RAG-motoren:
1. **Parent-Child Chunking & Metadata Injection:**
   * **Parent Chunks (~1200 tokens):** Bevarer full lovmessig kontekst, overskrifter og saksframlegg.
   * **Child Chunks (~250 tokens):** Optimalisert for presis vektorlikhet og semantisk gjenfinning.
   * **Metadata:** Beriket med `paragraf`, `myndighetsnivaa` (Bystyret vs Kommunedirektøren), `kostra_relevans` og `kilde_fil`.
2. **Hybrid Search & Reciprocal Rank Fusion (RRF):**
   * **Pure Okapi BM25:** Eksakt gjenkjenning av norske lovparagrafer (§ 13-1, § 14-6) og KOSTRA-koder (art 1010, 1020, 1710, funksjon 254).
   * **Dense Semantic Matching:** Fanger opp konseptuell mening og synonymer.
   * **RRF ($k=60$):** Kombinerer rangeringene uten skjevhet mot tekstlengde.
   * **BGE Cross-Encoder Reranker:** Finberegner relevansscore og filtrerer bort støy under terskelverdi (0.70).
3. **Presidio PII Privacy Gate:** Skjermer automatisk 11-sifrede fødselsnumre, 8-sifrede telefonnumre og e-poster før spørringen indekseres eller behandles.
4. **MLOps Observability & Continuous Evaluation:**
   * **Faithfulness:** >= 0.95 (alle påstander kan spores direkte til kildedokument eller DuckDB-gullag).
   * **Zero Hallucination Guarantee:** 100,0 % målt mot kommunale kontrollspørsmål.

## 🤖 MLOps & Modellportefølje

Modellene i `models/` overvåkes kontinuerlig mot modelldrift og trenes via `src/retrain_pipeline.py`:

| Modell | Algoritme | Ytelse / Metrikk | Formål |
| :--- | :--- | :--- | :--- |
| **Prognosemodell** | `RandomForestRegressor` | $R^2 = 0.9758$, $\text{MAE} = 1\,655\text{ kr}$ | Predikere neste måneds forbruk per ansvarsenhet og art. |
| **Tidlig Varsling** | `DecisionTreeClassifier` | `100,0 %` Nøyaktighet | Generere transparente `IF-THEN`-regler for revisjon og saksbehandling. |
| **Profilering** | `AgglomerativeClustering` | 4 klynger | Kartlegge utgiftsmønstre (Stabil, Vikar/Volatil, Sesong, Avvik). |
| **Avviksdeteksjon** | `IsolationForest` | 113 flaggede avvik ($Z > 2.5$) | Identifisere potensielle feilkonteringer og bilagsfeil. |

---

## 🛡️ GDPR, Presidio PII Gateway & Juridisk Forankring

### Presidio PII Gateway
For å etterleve GDPR artikkel 9 og personopplysningsloven sluses all fritekst gjennom **Presidio PII Gateway** før den sendes til LLM- eller analysemoduler:
* **Fødselsnummer (11 siffer):** Maskeres til `[FNR]`
* **Ansattnummer (6–8 siffer):** Maskeres til `[ANSATTNR]`
* **Personnavn og sensitiv lokasjonsdata:** Maskeres til `[PERSON]` / `[LOKASJON]`

### Juridisk Forankring
Alle beregninger, notatmaler og saksdokumenter er forankret i gjeldende norsk lovverk:
* **Kommuneloven § 13-1:** Kommunedirektørens administrative fullmakter og interne omdisponeringer.
* **Kommuneloven § 14-3:** Bystyrets vedtak av handlings- og økonomiplan samt årsbudsjett innen årets utløp, inkludert 3 ukers offentlig høringsfrist.
* **Kommuneloven § 14-6:** Krav til budsjettbalanse og Bystyrets bevilgningsmyndighet ved vesentlige reguleringer.
* **Kommuneloven § 14-7:** Forvaltning av bundne og ubundne driftsfond (disposisjonsfond).
* **Kommuneloven § 14-8:** Lovpålagt frist (15. februar) for oversendelse av foreløpig årsregnskap til kommunerevisjonen.
* **KOSTRA-forskriften:** Standardiserte arts- og funksjonskoder for nasjonal rapportering til SSB.

---

## 📂 Mappe- og Filstruktur

```text
Kom - G2/
├── index.html                          # Frittstående Executive Web Cockpit (15 moduler, 5 700+ linjer)
├── README.md                           # Komplett dokumentasjon (forretningsverdi + teknisk)
├── notebooks/
│   ├── explore_duckdb.ipynb            # Interaktiv DuckDB-utforsking og SQL-analyser
│   └── pycaret_rapid_bencmarking.ipynb # ML-modellering og tidsserie-benchmarking
├── templates/
│   └── index.html                      # Dedikert EOY & LOY Rådgivningscockpit med Chart.js
├── docs/
│   ├── COPILOT_PYTHON_IN_EXCEL_INSTRUCTIONS.md # Instruks for Copilot & Python in Excel (=PY())
│   ├── INSTRUKS_EXCEL_DASHBOARD.md     # Instruks for Power Query & Power Pivot
│   ├── EXPLAINER_EOY_PROGNOSE_OG_SESONGVEKTING.md # Matematisk og pedagogisk EOY- og EAC-forklaring
│   └── kostra_okonomi_hub.md           # Rådgiver- og systeminstruks for KOSTRA-analyser
├── .env.example                        # Mal for miljøvariabler
├── .gitignore                          # Git-regler
├── Dockerfile                          # Multi-stage containerdefinisjon
├── docker-compose.yml                  # Streamlit (:8501), FastAPI (:8000), MLflow (:5000)
├── requirements.txt                    # Produksjonsavhengigheter (DuckDB, FastAPI, Scikit-learn, etc.)
├── run.ps1                             # PowerShell CLI (-BuildDB, -Reconcile, -Retrain, -VectorDB, -Up, -All)
├── run_pipeline.bat                    # Master Batch-skript for helhetlig lokal kjøring
├── Excel-Reporting-Analysis.xlsb       # FAST & Power BI-Style Excel-modell (Binær arbeidsbok)
├── Excel-Reporting-Analysis.xlsx       # FAST & Power BI-Style Excel-modell (OpenXML)
├── pbi-reporting-project.pbip          # Power BI Desktop Developer Project
├── pbi-reporting-project.Report/       # Rapportoppsett og visualiseringer
├── pbi-reporting-project.SemanticModel/# TMDL-datamodell og 21 DAX-mål
├── excel.md                            # Retningslinjer for FAST-modellering
├── DAX.md                              # Komplett DAX-målkatalog
├── copilot.md                          # Standard for Copilot i regneark
├── data/
│   ├── raw/                            # Inndata for KOSTRA-CSV (21 filer)
│   ├── localblob/                      # Lokale kunnskapsdokumenter (50+ PDF, MD, CSV)
│   ├── database/                       # Lokal DuckDB (kostra_prod.duckdb)
│   ├── vectorstore/                    # Hybrid RAG Corpus-indeks (Parent-Child JSON)
│   └── export/                         # Genererte rapporter og avstemmingslogger
├── models/                             # Serialiserte ML-modeller (.pkl / joblib)
└── src/
    ├── app.py                          # Streamlit AI Workbench (8 moduler)
    ├── api_server.py                   # FastAPI REST backend (34 endepunkter, 100 % testdekning)
    ├── rag_localblob_engine.py         # Hybrid RAG, Parent-Child Chunking & 4-veis Intent Router
    ├── test_api_endpoints.py           # Automatisert testsuite for FastAPI (34/34 tester)
    ├── db_manager.py                   # DuckDB Medallion ETL og Ingestion Engine
    ├── canonical.py                    # Pydantic validering og dataskjema
    └── retrain_pipeline.py             # MLOps omtrening og modelldrift-evaluering
```

---

## 🚀 Installasjon & Kjøreveiledning (A til Å)

### Forutsetninger
* **Python:** v3.10, v3.11 eller v3.12 installert.
* **Nettleser:** Chrome, Edge eller Firefox.
* **Docker Desktop:** (Valgfritt, for containerisert drift).

---

### Alternativ 1: Frittstående Web Cockpit (Raskest & Enklest)
Åpne **`index.html`** direkte i nettleseren (støtter også GitHub Pages).  
Appen kjører offline med fulle analytiske kapabiliteter, dynamisk filtrering, Framsikt-eksport, saksdokument-generator og årshjul uten krav til lokal server.

Dersom du ønsker live integrasjon mot FastAPI-backend-en:
Dobbeltklikk **`start_web_cockpit.bat`** eller kjør i PowerShell:
```powershell
.\start_web_cockpit.bat
```

---

### Alternativ 2: Master Batch-fil (`run_pipeline.bat`)
Fra filutforskeren eller ledetekst (CMD / PowerShell):
```cmd
.\run_pipeline.bat
```
Dette skriptet utfører hele produksjonsløpet:
1. Bygger DuckDB Medallion Lakehouse fra `data/raw/*.csv`.
2. Trener og evaluerer alle maskinlæringsmodeller.
3. Indekserer kunnskapsbasen for Hybrid RAG.
4. Starter Streamlit AI Workbench på `http://localhost:8501`.

---

### Alternativ 3: PowerShell CLI (`run.ps1`)
Bruk PowerShell-skriptet for granulær kontroll:
```powershell
# Bygg databasen og tren modeller:
.\run.ps1 -BuildDB -Retrain

# Indekser vektordatabasen for RAG:
.\run.ps1 -VectorDB

# Start Docker-containerne (Streamlit, FastAPI og MLflow):
.\run.ps1 -Up

# Kjør alt i sekvens:
.\run.ps1 -All
```

---

### Alternativ 4: Start FastAPI Backend Standalone
For å starte REST-API-et separat:
```powershell
uvicorn src.api_server:app --host 127.0.0.1 --port 8000 --reload
```
Åpne `http://localhost:8000/docs` i nettleseren for interaktiv Swagger-dokumentasjon.

---

### Alternativ 5: Docker Compose
For komplett containerisering:
```powershell
docker compose up --build -d
```
Tjenester som starter:
* **Streamlit AI Workbench:** `http://localhost:8501`
* **FastAPI Backend:** `http://localhost:8000/docs`
* **MLflow Tracking Server:** `http://localhost:5000`

---

## 🧪 Verifikasjon & Tester

### 1. Full E2E Nettlesertest (Playwright E2E Testsuite)
Kjør den fullstendige, automatiserte nettlesertesten som verifiserer samtlige 16 moduler, dynamisk filterkaskadering, EDA FT Visuals, bakkeforankret lønns- og stillingsbudsjett, Ad hoc fakturering & selvkost, Recommender, Årshjul og feilfri konsoll:
```powershell
python test_full_suite.py
```
*Forventet resultat: `97 av 97 tester bestått (100.0 %) — Null console.error, null JavaScript runtime exceptions over 10 testblokker`.*

#### Oversikt over de 10 Testblokkene:
* **Testblokk 1:** Sideoppstart, tittel og feilfri nettleserkonsoll (0 runtime exceptions, 0 console.error).
* **Testblokk 2 & 2B:** SPA-navigasjon mellom 11 views samt rollebasert navigasjon for De 4 Arbeidsrommene.
* **Testblokk 3:** Dynamisk filterkaskadering (Sektor, Ansvar, Funksjon, Periode) og toppbannersynkronisering.
* **Testblokk 4:** EDA & Financial Times Visual Vocabulary (Scatterplot, OLS trendlinje $R^2 = 0{,}94$, Tufte fargekontroll).
* **Testblokk 5:** Lønns- og Stillingsbudsjett (Bakkeforankret mot KOSTRA snapshots, 168,0 FTE, 17,6M ramme, 13,3M YTD brutto, 12,6M YTD netto, 15,0M stillingsbasis).
* **Testblokk 6:** Recommender & Tiltaksmatrise (Lovhjemler, AML § 10-8 guardrail, administrative EOY-tiltak).
* **Testblokk 7:** Årshjul, Kommunelov-frister og 1-klikks dokumentgenerator (Bystyresaker og bestillingsnotater).
* **Testblokk 7B:** Faktura, Selvkost & Ad hoc Utleie og Lønn (Skole utleie 480 kr/t, EHF 3.0 faktura med Art 1650 og KID, Skole intern lønn 538,46 kr/t, 1-klikks bokføring i eliminasjonstabell med Art 780/380).
* **Testblokk 8:** Min Økonomi & Månedsrapport (Tufte SVG Sparkline M01–M08, betingede avvikssøyler, avviksfordeling med Bullet Graphs, lønns- og refusjonsprofil mot Art 1710, mindreforbruksanalyse med forsiktighetsprinsipp for konto 112098, AI-tiltaksplan).
* **Testblokk 9:** Komplett tilbakestilling (Reset) til totalutvalg (328,0 planlagte FTE).
* **Testblokk 10:** Sluttkontroll av feillogg (garanterer 100 % feilfri konsoll gjennom hele testløpet).

### 2. FastAPI Backend REST Testsuite
Kjør den automatiserte enhetstesten for å verifisere at samtlige 10 REST-endepunkter fungerer:
```powershell
python -m src.test_api_endpoints
```
*Forventet resultat: `Ran 10 tests in 0.45s - OK (10/10 PASS)`.*

### 3. DuckDB Medallion Databaseavstemming (06_CHECKS)
For å verifisere databaseavstemmingen og `06_CHECKS`:
```powershell
python -c "import duckdb; con = duckdb.connect('data/database/kostra_prod.duckdb'); print(con.execute('SELECT COUNT(*) FROM modelready_fact').fetchone())"
```
*Forventet resultat: `(2256,)` rader med `0,0 %` nullverdier og differanse `0,00 kr`.*

---

## 🏛️ Forfatter & Ansvarlig

* **Fagansvarlig & Utvikler:** Frank Ellingsen — Financial Controller & Business Intelligence Specialist.
* **Organisasjonskontekst:** Kristiansand kommune / Økonomistyring & Virksomhetskontroll © 2026.
* **Faglige Standarder:** Norsk Lovdata (*Kommuneloven*), Framsikt standarder, DFØ, FAST Standard Organization, Edward Tufte Data-Ink Ratio.
