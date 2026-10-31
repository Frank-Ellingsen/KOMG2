# Antigravity Module: Recommender Engine & Adversarial Audit Agent

## 1. Recommender Matrise
Tiltak sorteres etter tidshorisont og juridisk hjemmel:

1. **Kortsiktige Administrative Tiltak (EOY / Inneværende år):**
   - Hjemmel: Kommuneloven § 13-1 (Styringsrett).
   - Tiltak: Vikarstopp (Art 1020), Overtidsfrys (Art 1040), Konsulentfrys (Art 1270), Innkjøpsstopp (Art 1200).
   - Kan gjennomføres umiddelbart av kommunedirektør/enhetsleder utan bystyrevedtak.

2. **Politiske Vedtak før EOY (Inneværende år):**
   - Hjemmel: Kommuneloven § 14-6 (Disposisjonsfond) og § 14-10 (Budsjettendringer).
   - Tiltak: Fondsinndragning (Art 1950), Rammeoverføring mellom sektorer (Art 1900).
   - Krever formelt Bystyrevedtak før 31.12.

3. **Langsiktige Tiltak (Neste års budsjett 2027 & Økonomiplan 2027–2030):**
   - Hjemmel: Kommuneloven § 14-3.
   - Tiltak: Stillingsomstilling ved naturlig avgang (Art 1010), KI-gevinstuttak (2,0 mill. kr fra 2029), Skole-/Tjenestestruktur.

## 2. Adversarial Audit Agent ("Revisor-agenten")
Før et preskriptivt tiltak godkjennes, gjennomfører Audit Agent følgende sjekker:
- **Arbeidsmiljøloven § 10-8:** Sjekker at overtids- eller vikarstopp ikke medfører brudd på hviletid eller maksimal arbeidstid.
- **Helse- og omsorgstjenesteloven § 4-1:** Sjekker at bemanning i omsorgsboliger/sykehjem opprettholder lovpålagt forsvarlighet.
- **Risikoflagg:** Dersom et kutt utløser juridisk eller faglig risiko, merkes det med et rødt advarselsflagg og krever manuell overstyring.

## 3. Framsikt Excel Export Generator
Genererer `framsikt_budsjettendringer_eoy.xlsx` med tre faneblad:
- `Framsikt_Import_Klar`
- `Recommender_Tiltaksmatrise`
- `Oppsummering_Per_Omrade`
