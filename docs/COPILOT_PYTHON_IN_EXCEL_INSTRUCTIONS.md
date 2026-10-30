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
  ```
- **Datatyper:** Sørg for at datatyper konverteres eksplisitt hvis Excel-celler inneholder blandet tekst/tall:
  `df['Belop'] = pd.to_numeric(df['Belop'], errors='coerce')`

## 3. DATATRANSFORMASJON OG PANDAS-STANDARD
- **Vektorisering:** Bruk altid vektoriserte Pandas/NumPy-operasjoner. Unngå eksplisitte Python `for`-sløyfer over rader.
- **Divisjonsbeskyttelse:** Beskytt mot divisjon med null eller `NaN`-verdier:
  `df['Margin'] = np.where(df['Budsjett'] != 0, df['Regnskap'] / df['Budsjett'], 0)`
- **Metodekjeding:** Foretrekk ren metodekjeding (`.assign()`, `.query()`, `.groupby()`) for lesbarhet.

## 4. VISUALISERING I CELLER (Matplotlib & Seaborn)
- **Returverdi:** For at diagrammer skal vises som bilde-objekter i cellen, avslutt koden med `plt.gca()` eller selve `fig`-objektet.

## 5. MASKINLÆRING OG STATISTIKK (ML & Analytics)
- **Anomali-deteksjon:** For regnskaps- og avviksanalyser, bruk `IsolationForest` eller Z-score.

