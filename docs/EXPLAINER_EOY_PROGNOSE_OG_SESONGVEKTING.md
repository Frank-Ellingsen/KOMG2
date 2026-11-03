# 📊 Explainer: EOY-Prognose, Glidende Gjennomsnitt & Sesongvekting i KOSTRA AI Workbench

Dette dokumentet gir en pedagogisk og matematisk forklaring på hvordan **EOY-prognosen** (*Estimate at Completion – EAC*) beregnes i dashbordet, rapportene og KOSTRA AI Workbench, inkludert bruken av rullende 3-måneders snitt og periodevekting.

---

## 1. 🔄 Hva betyr «Glidende 3-måneders snitt» (Rolling 3M Run-Rate)?

### Definisjon
I stedet for å ta et enfoldig snitt av alle gjennomførte måneder hittil i år (M01–M08), måler det glidende gjennomsnittet den faktiske månedlige kostnadstakten i de tre nyeste lukkede regnskapsmånedene:

$$\text{Rolling\_3M\_Avg} = \frac{\text{Netto Regnskap}_{M-2} + \text{Netto Regnskap}_{M-1} + \text{Netto Regnskap}_{M}}{3}$$

**Eksempel ved utgangen av august (M08):**
$$\text{Rolling\_3M\_Avg} = \frac{\text{Regnskap}_{M06\text{ (juni)}} + \text{Regnskap}_{M07\text{ (juli)}} + \text{Regnskap}_{M08\text{ (august)}}}{3}$$

### Hvorfor rullende 3-måneders snitt?
1. **Fanger opp nyeste kostnadsbilde:** Endringer i bemanningsmønster, overtidstrykk eller nye rammeavtaler inngått før sommeren vises umiddelbart i 3M-snittet, i motsetning til et YTD-snitt som vannes ut av gamle tall fra januar og februar.
2. **Demper enkeltstående feil og inntektsstøy:** Én enkelt måned med forsinket bilag eller etterbetaling slår ikke ut med full styrke, da effekten jevnes ut over 90 dager.

---

## 2. ⚖️ Er det vekting av periodene før oss? (Historisk Vekting)

**JA!** Systemet benytter en todelt vektingsmodell:

### A. Tidsvekting av historikken (Fokus på nyeste trend)
Historiske måneder før den rullende 3-måneders perioden (f.eks. M01–M05) gis 0 % direkte vekt i den operative fremtidstakten (*run-rate*), fordi driftssituasjonen i kommunale enheter endrer seg raskt. De nyeste 3 månedene gis 100 % vekt som operativt grunnlag for fremskrivning.

### B. Sesongvekting for gjenstående måneder (Left of Year – LOY M09–M12)
Kommunale utgifter er ikke jevnt fordelt på 12 like måneder:
* **Juni/Juli (M06/M07):** Høyere vikarforbruk i helse og omsorg pga. ferieavvikling.
* **August (M08):** Skolestart, SFO-oppstart og tilhørende materiellinnkjøp.
* **November/Desember (M11/M12):** Ekstrautbetalinger, halv skatt i desember, årsavslutningsfakturaer og feriepengeavsetninger.

Derfor multipliseres 3M-run-raten med historiske sesongindekser ($S_m$) basert på KOSTRA-erfaringstall og kommuneregnskapet:

| Måned (LOY) | Sesongfaktor ($S_m$) | Årsak / Kjennetegn i kommuneregnskapet |
| :--- | :---: | :--- |
| **September (M09)** | **0,98** | Normalisering etter skolestart og ferieavvikling. |
| **Oktober (M10)** | **1,02** | Ordinær stabil drift og full høstaktivitet. |
| **November (M11)** | **1,05** | Høyere fakturainngang mot årsslutt og leverandøravregninger. |
| **Desember (M12)** | **1,12** | Årsavslutning, vaktbukkjøringer, tillegg og skattejusteringer. |

---

## 3. 🧮 Trinnvis Beregning av EOY / EAC per 31.12

Forventet sluttresultat ved årets utgang (**EAC** – *Estimate at Completion*) beregnes etter følgende 3-stegs formel:

$$\text{EAC}_{\text{År}} = \text{YTD}_{\text{Regnskap (M01–M08)}} + \sum_{m=9}^{12} \text{ETC}_m$$

### Steg 1: Bokført YTD (M01–M08)
Eksakt registrert regnskap fra DuckDB OLAP Engine per august cut-off:
$$\text{YTD}_{\text{Regnskap}} = 31\,524\,851\text{ kr}$$

### Steg 2: Beregne Gjenstående Q4 / LOY (Estimate to Complete – ETC)
For hver av månedene September ($m=9$) til Desember ($m=12$) beregnes estimert månedskostnad:
$$\text{ETC}_m = \text{Rolling\_3M\_Avg} \times S_m \times (1 + \text{Param\_Lonnsvekst} - \text{Param\_Effektivisering})$$

$$\text{Projisert Q4 ETC (M09–M12)} = 15\,727\,975\text{ kr}$$

### Steg 3: Summer EAC & Sammenlign mot Årsbudsjett
$$\text{EAC (31.12)} = 31\,524\,851\text{ kr} + 15\,727\,975\text{ kr} = 47\,252\,826\text{ kr}$$

* **Vedtatt helårsbudsjett:** $43\,942\,856\text{ kr}$
* **Forventet Årsavvik (EAC vs. Budsjett):** $-3\,309\,971\text{ kr}$ (🔴 **KRITISK MERFORBRUK**)
* **Forventet Burn Rate:** $107{,}5\text{ \%}$

---

## 💡 Sammendrag for Enhetsleder & Controller

* **Glidende gjennomsnitt:** Viser hvor mye enheten reelt bruker per måned akkurat nå (snitt av de 3 siste lukkede månedene).
* **Vekting:** De nyeste 3 månedene bestemmer fremtidstakten, mens gjenstående måneder (Sep–Des) sesongjusteres fordi desember erfaringsmessig har høyere kostnadsbelastning enn september.
* **EOY (EAC):** Forteller deg hvor regnskapet lander ved årsslutt dersom driftstakten fortsetter uten korrigerende tiltak, og gir et solid grunnlag for å dimensjonere LOY-tiltak (vikarstopp, overtidsbegrensning og vakansdekning).

