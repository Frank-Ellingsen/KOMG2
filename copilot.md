# SYSTEM INSTRUCTION: Copilot Standard for Python in Excel (=PY())

## 1. EKSEKVERINGSMILJØ OG SANDKASSE (Cloud Sandbox)
- **Eksekvering:** Python i Excel kjøres i et sikkert Anaconda-sky-miljø (Microsoft Azure).
- **Ingen lokal fildirekte tilgang:** Python har ikke direkte tilgang til lokale filstier (f.eks. `C:\...` eller `.duckdb`-filer). Data må hentes fra Excel-rutenettet via `xl()` eller lastes inn via Power Query først.
- **Tilgjengelige biblioteker:** Bruk standard bibliotekstakk: `pandas` (pd), `numpy` (np), `matplotlib.pyplot` (plt), `seaborn` (sns), `scikit-learn`, `statsmodels`, og `scipy`.

## 2. DATAINNHENTING FRA EXCEL (`xl()`-funksjonen)
- **Formatere som tabeller:** Referer alltid til formaterte Excel-tabeller eller spesifikke områder:
  ```python
  # Best practice for tabeller
  df = xl("Modelready_Fact[#All]", headers=True)
  
  # For celler eller områder
  data = xl("A1:D50")
Datatyper: Sørg for at datatyper konverteres eksplisitt hvis Excel-celler inneholder blandet tekst/tall: df['Belop'] = pd.to_numeric(df['Belop'], errors='coerce')
3. DATATRANSFORMASJON OG PANDAS-STANDARD
Vektorisering: Bruk altid vektoriserte Pandas/NumPy-operasjoner. Unngå eksplisitte Python for-sløyfer over rader.
Divisjonsbeskyttelse: Beskytt mot divisjon med null eller NaN-verdier: df['Margin'] = np.where(df['Budsjett'] != 0, df['Regnskap'] / df['Budsjett'], 0)
Metodekjeding: Foretrekk ren metodekjeding (.assign(), .query(), .groupby()) for lesbarhet.
4. VISUALISERING I CELLER (Matplotlib & Seaborn)
Returverdi: For at diagrammer skal vises som bilde-objekter i cellen, avslutt koden med plt.gca() eller selve fig-objektet:
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(figsize=(8, 4))
sns.barplot(data=df, x='Maaned', y='Regnskap', ax=ax, palette='Blues_d')
ax.set_title("Månedlig Regnskapsutvikling", fontsize=12, fontweight='bold')
plt.tight_layout()
fig  # Returnerer diagrammet direkte til cellen
Designkrav: Bruk alltid ryddige, nøytrale fargepaletter (Blues, Viridis eller gråtoner med fremhevet aksentfarge), tittel, og tydelige akseetiketter utan forstyrrende linjer.
5. MASKINLÆRING OG STATISTIKK (ML & Analytics)
Anomali-deteksjon: For regnskaps- og avviksanalyser, bruk IsolationForest eller Z-score:
from sklearn.ensemble import IsolationForest

model = IsolationForest(contamination=0.05, random_state=42)
df['Anomali_Flagg'] = model.fit_predict(df[['ytd_regnskap_nok', 'monthly_delta_regnskap_nok']])
Prognoser og Trend: Bruk lineær regresjon eller glatting for korte tidsserier:
from statsmodels.tsa.holtwinters import ExponentialSmoothing
# Sesongjustert prognose
6. UT-DATA OG CELLERETUR (Output Formatting)
Excel Values vs. Python Objects:
Når koden skal vise et tabellresultat i arket, sørg for at celletypen i Excel er satt til Excel Value (spiler ut utdata over cellene).
Når koden produserer en intermediate DataFrame eller ML-modell som skal gjenbrukes av andre =PY() celler, behold celletypen som Python Object.
7. FEILHÅNDTERING OG FEILSØKING
Pakke inn i try/except: Ved kompleks logikk, returner en ryddig feilmelding i stedet for at koden krasjer med uleselig stacktrace:
try:
    # Beregning
    result = df.groupby('Funksjon')['Regnskap'].sum().reset_index()
except Exception as e:
    result = f"Feil under beregning: {str(e)}"
result