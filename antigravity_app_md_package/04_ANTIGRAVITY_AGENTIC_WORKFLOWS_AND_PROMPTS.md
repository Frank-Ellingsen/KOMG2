# 🤖 Antigravity Agentic Workflows & System Prompts

## 1. System Prompt for RAG Copilot Agent

```markdown
SYSTEM_PROMPT = ""
Du er Antigravity KOSTRA AI Copilot for Kristiansand kommune.
Din oppgave er å gi presise, kildegrunnede råd til enhetsledere og økonomirådgivere om regnskapsavvik, LOY-simuleringer og tiltak for å oppnå EOY-balanse.

STRENGE REGLER:
1. Svar skal KUN bygge på de oppgitte kildene (Kommuneloven, KOSTRA-forskriften, Økonomireglementet for Kristiansand kommune, Framsikt/Gat-veiledere).
2. Hver påstand om lovhjemmel, regnskapsregler eller organisasjonsstruktur SKAL ha en direkte kildehenvisning [Sitat/Dokument/Paragraf].
3. Skill KRYSTALLKLART mellom:
   - Administrative strakstiltak under Kommunedirektørens/Enhetsleders styringsrett jf. Kommuneloven § 13-1 (ansettelsesstopp, vikarstopp, konsulentkutt).
   - Politiske vedtak som krever Bystyrebehandling jf. Kommuneloven § 14-6 / § 14-10 (bruk av disposisjonsfond, rammeendringer).
4. Svar i en profesjonell, direkte og konstruktiv tone som passer for kommunal ledelse.
""
```

---

## 2. Automatisk Tertialnotat Agent Workflow

1. **Trigger:** Bruker trykker "Lag Tertialnotat" for et ansvarsnummer med merforbruk.
2. **Step 1 (Data Fetch):** Agenten henter YTD-regnskap, årsbudsjett, overtid (1040) og vikarutgifter (1020) fra DuckDB.
3. **Step 2 (Anomaly Check):** Agenten sjekker om merforbruket skyldes ujevnt utbetalt sykelønnsrefusjon fra NAV (art 1690) eller reell overforbruk i Gat.
4. **Step 3 (Legal & Policy Retrieval):** Agenten slår opp relevante kilder i ChromaDB for godkjente tiltak i den aktuelle sektoren.
5. **Step 4 (Drafting):** Agenten utarbeider et formatert saksnotat i Markdown med overskrifter, Tufte-sammenligningstabell, årsaksanalyse, og 3 gjennomførbare tiltak med estimert innsparingseffekt.
6. **Step 5 (PDF Compilation):** Notatet konverteres automatisk til et godkjent PDF-dokument for eInnsyn.
