@echo off
chcp 65001 > nul
title KOSTRA AI Workbench - Full Pipeline

echo =======================================================================
echo KOSTRA AI Workbench Pipeline (Kristiansand Kommune)
echo =======================================================================
echo.

echo [1/3] Kjoerer Ingestion og DuckDB Medallion-arkitektur (db_manager.py)...
python src\db_manager.py
if errorlevel 1 (
    echo.
    echo [FEIL] Ingestion feilet!
    pause
    exit /b 1
)
echo [OK] DuckDB-databasen er ferdig oppbygd.
echo.

echo [2/3] Trener om ML-modellene (retrain_pipeline.py)...
python src\retrain_pipeline.py
if errorlevel 1 (
    echo.
    echo [FEIL] ML-omtrening feilet!
    pause
    exit /b 1
)
echo [OK] ML-modellene er re-trente og evaluert!
echo.

echo [3/3] Starter Streamlit AI Workbench (app.py)...
echo.
echo Dashbordet aapnes i nettleseren din paa http://localhost:8501
echo Trykk Ctrl+C i dette vinduet naar du vil avslutte.
echo =======================================================================
echo.

streamlit run src\app.py

pause
