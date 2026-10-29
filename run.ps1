# Master Powershell CLI for Kom - G2
param (
    [switch]$BuildDB,
    [switch]$Reconcile,
    [switch]$Retrain,
    [switch]$Up,
    [switch]$Down,
    [switch]$All
)

$ProjectPath = $PSScriptRoot

if ($BuildDB -or $All) {
    Write-Host " [🚀] Bygger DuckDB og oppretter Bitemporal Reconciliation Views..." -ForegroundColor Yellow
    python "$ProjectPath\src\db_manager.py"
}

if ($Retrain -or $All) {
    Write-Host " [🧠] Kjører ML-omtrening og sjekker Model Drift..." -ForegroundColor Yellow
    python "$ProjectPath\src\retrain_pipeline.py"
}

if ($Up -or $All) {
    Write-Host " [🐳] Starter Docker Compose (Streamlit + MLflow UI)..." -ForegroundColor Yellow
    try {
        docker compose -f "$ProjectPath\docker-compose.yml" up --build -d
    } catch {
        Write-Host " [i] 'docker compose' feilet. Prøver 'docker-compose'..." -ForegroundColor DarkGray
        docker-compose -f "$ProjectPath\docker-compose.yml" up --build -d
    }
    Start-Process "http://localhost:8501"
    Start-Process "http://localhost:5000"
}

if ($Down) {
    Write-Host " [🛑] Stopper Docker-containerne..." -ForegroundColor Red
    docker compose -f "$ProjectPath\docker-compose.yml" down
}