import json
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
import webbrowser
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent
API_HOST = "127.0.0.1"
API_PORT = 8000
API_BASE = f"http://{API_HOST}:{API_PORT}"
REPORT_URL = f"{API_BASE}/api/v1/monthly-report?sektor=ALL&ansvar=ALL"


def report_api_is_ready() -> bool:
    try:
        with urllib.request.urlopen(REPORT_URL, timeout=2) as response:
            report = json.load(response)
        return report.get("status") == "ok"
    except (OSError, urllib.error.URLError, json.JSONDecodeError):
        return False


def port_is_in_use() -> bool:
    try:
        with socket.create_connection((API_HOST, API_PORT), timeout=1):
            return True
    except OSError:
        return False


def main() -> int:
    server = None
    if not report_api_is_ready():
        if port_is_in_use():
            print(
                f"Port {API_PORT} er opptatt, men månedsrapport-API-et svarer ikke. "
                "Kontroller tjenesten på porten før du prøver igjen.",
                file=sys.stderr,
            )
            return 1

        print("Starter FastAPI i et eget konsollvindu ...", flush=True)
        server = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "src.api_server:app",
                "--host",
                API_HOST,
                "--port",
                str(API_PORT),
            ],
            cwd=PROJECT_DIR,
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0,
        )

        for _ in range(30):
            if server.poll() is not None:
                print(
                    "FastAPI avsluttet under oppstart. Se API-konsollvinduet for feilen.",
                    file=sys.stderr,
                )
                return 1
            if report_api_is_ready():
                break
            time.sleep(1)
        else:
            print(
                "FastAPI svarte ikke innen 30 sekunder. Se API-konsollvinduet for feilmeldinger.",
                file=sys.stderr,
            )
            return 1
        print(
            f"FastAPI startet (PID {server.pid}). La API-konsollvinduet stå åpent.",
            flush=True,
        )
    else:
        print(f"Fant et fungerende månedsrapport-API på port {API_PORT}.", flush=True)

    dashboard_url = f"{API_BASE}/"
    webbrowser.open(dashboard_url)
    print(f"Dashboard åpnet: {dashboard_url}")
    print("Stopp API-et med Ctrl+C i API-konsollvinduet når du er ferdig.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
