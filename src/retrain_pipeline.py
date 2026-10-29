import os
import duckdb
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, f1_score

def run_retrain_pipeline(db_path: str = "data/database/kostra_prod.duckdb"):
    """
    Kjører komplett omtrening og evaluering av KOSTRA AI Workbench modellportefølje:
    1. Regresjon: RandomForestRegressor (Prognose for neste måneds regnskap)
    2. Klassifisering: DecisionTreeClassifier (Early Warning status: 🔴 / 🟡 / 🟢)
    3. Unsupervised Clustering: AgglomerativeClustering / hclust (Segmentering i 4 forbruksprofiler)
    4. Anomaly Detection: IsolationForest (Automatisk avviks- og føringskontroll)
    """
    print("🚀 Starter KOSTRA ML Retraining Pipeline...")
    
    # 1. Laste modelready_fact fra DuckDB i read_only modus
    if not os.path.exists(db_path):
        print(f"❌ Finner ikke databasen på {db_path}. Kjøre .\\run.ps1 -BuildDB først.")
        return
        
    conn = duckdb.connect(db_path, read_only=True)
    df = conn.execute("SELECT * FROM modelready_fact").fetchdf()
    conn.close()
    
    print(f"📊 Lastet {len(df)} rader og {len(df.columns)} kolonner fra 'modelready_fact'.")
    
    # Definer feature-sett
    feature_cols = [
        'month', 'quarter', 'is_summer_season', 'is_year_end',
        'ytd_budsjett_nok', 'ytd_regnskap_nok', 'ytd_avvik_nok',
        'monthly_delta_budsjett_nok', 'monthly_delta_regnskap_nok', 'monthly_delta_avvik_nok',
        'lag_1m_regnskap_nok', 'lag_1m_avvik_nok',
        'rolling_3m_avg_regnskap_nok', 'rolling_3m_std_regnskap_nok',
        'burn_rate_pct', 'budget_coverage_ratio',
        'anomaly_z_score_3m', 'abs_monthly_avvik_nok', 'log_monthly_regnskap_nok'
    ]
    
    X = df[feature_cols].copy()
    
    # ----------------------------------------------------
    # 1. REGRESJON: RandomForestRegressor
    # ----------------------------------------------------
    print("\n--- 🌲 1. Regresjon: RandomForestRegressor ---")
    y_reg = df['target_next_month_regnskap']
    
    rf_reg = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    rf_reg.fit(X, y_reg)
    y_reg_pred = rf_reg.predict(X)
    
    rmse = np.sqrt(mean_squared_error(y_reg, y_reg_pred))
    mae = mean_absolute_error(y_reg, y_reg_pred)
    r2 = r2_score(y_reg, y_reg_pred)
    
    print(f"  ✅ RMSE: {rmse:,.2f} NOK")
    print(f"  ✅ MAE:  {mae:,.2f} NOK")
    print(f"  ✅ R²:   {r2:.4f}")
    
    importances = pd.Series(rf_reg.feature_importances_, index=feature_cols).sort_values(ascending=False)
    print("  ⭐ Topp 5 viktigste prognose-variabler:")
    for feat, imp in importances.head(5).items():
        print(f"     - {feat}: {imp:.4f}")

    # ----------------------------------------------------
    # 2. KLASSIFISERING: DecisionTreeClassifier (Early Warning)
    # ----------------------------------------------------
    print("\n--- 🌳 2. Klassifisering: DecisionTreeClassifier ---")
    y_clf = df['target_status_code'] # 0: I RUTE, 1: ADVARSEL, 2: KRITISK
    
    dt_clf = DecisionTreeClassifier(max_depth=4, random_state=42)
    dt_clf.fit(X, y_clf)
    y_clf_pred = dt_clf.predict(X)
    
    acc = accuracy_score(y_clf, y_clf_pred)
    f1_macro = f1_score(y_clf, y_clf_pred, average='macro')
    
    print(f"  ✅ Accuracy: {acc:.4f}")
    print(f"  ✅ F1 (macro): {f1_macro:.4f}")
    
    rules = export_text(dt_clf, feature_names=feature_cols)
    print("  📋 Utdrag av beslutningsregler (IF-THEN):")
    for line in rules.split('\n')[:8]:
        print(f"     {line}")

    # ----------------------------------------------------
    # 3. UNSUPERVISED CLUSTERING: AgglomerativeClustering (hclust)
    # ----------------------------------------------------
    print("\n--- 🧩 3. Clustering: AgglomerativeClustering (hclust) ---")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    hclust = AgglomerativeClustering(n_clusters=4)
    cluster_labels = hclust.fit_predict(X_scaled)
    
    cluster_counts = pd.Series(cluster_labels).value_counts().to_dict()
    print(f"  ✅ Fordeling på 4 klynger: {cluster_counts}")

    # ----------------------------------------------------
    # 4. ANOMALY DETECTION: IsolationForest
    # ----------------------------------------------------
    print("\n--- 🚨 4. Anomaly Detection: IsolationForest ---")
    iso_forest = IsolationForest(contamination=0.05, random_state=42, n_jobs=-1)
    anomaly_labels = iso_forest.fit_predict(X_scaled) # -1: Anomaly, 1: Normal
    
    anomalies_count = (anomaly_labels == -1).sum()
    print(f"  ✅ Identifiserte {anomalies_count} potensielle avvik/føringsfeil ({anomalies_count/len(df)*100:.1f}%).")
    
    print("\n🎉 Omtrening og evaluering av hele modellporteføljen var vellykket!")

if __name__ == "__main__":
    run_retrain_pipeline()
