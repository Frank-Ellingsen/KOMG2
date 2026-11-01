@echo off
setlocal
cd /d "%~dp0"

python start_web_cockpit.py
if errorlevel 1 (
    echo.
    echo [FEIL] Dashboardet kunne ikke startes. Kontroller feilmeldingen over.
    pause
    exit /b 1
)
