$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "Kontrollerer DuckDB-database..." -ForegroundColor Cyan
$dbPath = Join-Path $PSScriptRoot "data\database\kostra_prod.duckdb"
if (-not (Test-Path $dbPath)) {
    Write-Error "[FEIL] DuckDB-database ble ikke funnet på $dbPath. Kjør datapipelinen først."
    exit 1
}

Write-Host "DuckDB funnet: $dbPath" -ForegroundColor Green
Write-Host "Starter Web Cockpit (FastAPI + Dashboard)..." -ForegroundColor Cyan

python start_web_cockpit.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "[FEIL] Dashboardet kunne ikke startes. Kontroller feilmeldingen over."
    exit $LASTEXITCODE
}

