// 1.1 Totalt Regnskap (Månedlig Delta)
Sum_Regnskap =
SUM(fact_modelready[YTD regnskap_nok])

// 1.2 Totalt Budsjett (Månedlig Delta)
Sum_Budsjett =
SUM(fact_modelready[YTD budsjett_nok])

// 1.3 Nettovarians / Avvik (Merforbruk er negativt tall)
Sum_Avvik =
[Sum_Budsjett] - [Sum_Regnskap]

Avvik % =
DIVIDE([Sum_Avvik], [Sum_Budsjett], 0)

// 1.4 Forbruksrate (Burn Rate %)
Burn_Rate_Pct =
DIVIDE([Sum_Regnskap], [Sum_Budsjett], 0)

// 2.1 YTD Regnskap (Akkumulert fra 01.01 til valgt dato)
YTD_Regnskap =
TOTALYTD([Sum_Regnskap], dim_date[Dato])

// 2.2 YTD Budsjett
YTD_Budsjett =
TOTALYTD([Sum_Budsjett], dim_date[Dato])

// 2.3 YTD Avvik (Akkumulert mer/mindreforbruk)
YTD_Avvik =
[YTD_Regnskap] - [YTD_Budsjett]

// 2.4 Regnskap Forrige Måned
Regnskap_MoM_Forrige =
CALCULATE(
[Sum_Regnskap],
PREVIOUSMONTH(dim_date[Dato])
)

// 2.5 Endring i NOK fra forrige måned
MoM_Endring_NOK =
IF(
ISBLANK([Regnskap_MoM_Forrige]),
BLANK(),
[Sum_Regnskap] - [Regnskap_MoM_Forrige]
)

// 2.6 Prosentvis endring fra forrige måned
MoM_Endring_Pct =
DIVIDE([MoM_Endring_NOK], [Regnskap_MoM_Forrige], 0)

/ 2.7 Regnskap Samme Periode Forrige År
Regnskap_YoY_ForrigeAar =
CALCULATE(
[Sum_Regnskap],
SAMEPERIODLASTYEAR(dim_date[Dato])
)

// 2.8 YoY Endring i NOK
YoY_Endring_NOK =
[Sum_Regnskap] - [Regnskap_YoY_ForrigeAar]

// 2.9 YoY Endring i %
YoY_Endring_Pct =
DIVIDE([YoY_Endring_NOK], [Regnskap_YoY_ForrigeAar], 0)

// 2.10 Rullende 3-måneders snitt regnskap
Regnskap_Rullende_3M =
CALCULATE(
AVERAGEX(VALUES(dim_date[Ar_Maned]), [Sum_Regnskap]),
DATESINPERIOD(dim_date[Dato], MAX(dim_date[Dato]), -3, MONTH)
)

// 3.1 Statusindikator (Tekst & Emoji)
Status_Indikator =
VAR Avvik = [Sum_Avvik]
VAR BurnRate = [Burn_Rate_Pct]
RETURN
SWITCH(
TRUE(),
Avvik > 200000 || BurnRate > 1.25, "🔴 KRITISK AVVIK",
Avvik > 50000 || BurnRate > 1.10, "🟡 ADVARSEL",
"🟢 I RUTE"
)

// 3.2 Fargekode for Betinget Formatering (Hex)
Status_Fargekode =
VAR Avvik = [Sum_Avvik]
RETURN
SWITCH(
TRUE(),
Avvik > 200000, "#D62728", // Rød
Avvik > 50000, "#FF7F0E", // Gul
"#2CA02C" // Grønn
)

// 3.3 Dynamisk Tittel for Kortvisning
Kort_Tittel_Periode =
"Avviksoversikt for " & SELECTEDVALUE(dim_date[Ar_Maned], "Hele Året")

Aktiv_Filter_Tekst =
// 1. Sjekk filter på År
VAR Valgt_Ar =
IF(
ISFILTERED(dim_date[Ar]),
CONCATENATEX(VALUES(dim_date[Ar]), dim_date[Ar], ", "),
"Alle år"
)

// 2. Sjekk filter på ÅÅÅÅ-MM
VAR Valgt_Maned =
IF(
ISFILTERED(dim_date[Ar_Maned]),
CONCATENATEX(VALUES(dim_date[Ar_Maned]), dim_date[Ar_Maned], ", "),
"Alle måneder"
)

// 3. Sjekk filter på KOSTRA Funksjon (Viser opptil 3 navn, ellers antall)
VAR AntallValgteFunksjoner = COUNTROWS(VALUES(dim_funksjon[Funksjon_Kode_Navn]))
VAR Valgt_Funksjon =
IF(
ISFILTERED(dim_funksjon[KOSTRA_Funksjon_Navn]),
IF(
AntallValgteFunksjoner > 3,
AntallValgteFunksjoner & " funksjoner valgt",
CONCATENATEX(VALUES(dim_funksjon[KOSTRA_Funksjon_Navn]), dim_funksjon[KOSTRA_Funksjon_Navn], ", ")
),
"Alle funksjoner"
)

// 4. Sett sammen sluttteksten med linjeskift (UNICHAR(10))
RETURN
"📅 År: " & Valgt_Ar & UNICHAR(10) &
"📆 Måned: " & Valgt_Maned & UNICHAR(10) &
"🏛️ KOSTRA-funksjon: " & Valgt_Funksjon
