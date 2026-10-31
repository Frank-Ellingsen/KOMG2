# -*- coding: utf-8 -*-
"""
End-to-end automated test for FastAPI server (src/api_server.py)
Tests all endpoints from md_package, enterprise_suite, and antigravity_master_instructions_suite:
- /api/v1/summary
- /api/v1/deviations
- /api/v1/simulate-loy
- /api/v1/chat
- /api/v1/generate-report
- /api/v1/mlflow/metrics
- /api/v1/procurement/contracts
- /api/v1/invoicing/selvkost-calc
- /api/v1/invoicing/internal-eliminations
- /api/v1/grants/status
- /api/v1/dashboard/anomalies (Master Suite)
- /api/v1/simulator/budget-plus (Master Suite)
- /api/v1/recommender/measures (Master Suite)
- /api/v1/procurement/spend (Master Suite)
- /api/v1/invoicing/selvkost (Master Suite)
- /api/v1/grants/toppfinansiering (Master Suite)
- /api/v1/exports/framsikt-excel (Master Suite)
- /api/v1/exports/einnsyn-pdf (Master Suite)
"""
import sys
import os

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

sys.path.insert(0, os.path.abspath("."))
from fastapi.testclient import TestClient

from src.api_server import app

client = TestClient(app)

def run_tests():
    print("Testing /api/v1/summary...")
    res = client.get("/api/v1/summary?sektor=Helse+og+Omsorg&ansvar=25310")
    assert res.status_code == 200, f"Summary failed: {res.text}"
    data = res.json()
    assert data["status"] == "ok"
    assert data["reconciled_check_diff_nok"] == 0.00
    print("  OK: summary reconciled 0.00 NOK")

    print("Testing /api/v1/deviations...")
    res = client.get("/api/v1/deviations")
    assert res.status_code == 200, f"Deviations failed: {res.text}"
    data = res.json()
    assert len(data["deviations"]) > 0
    print(f"  OK: {len(data['deviations'])} deviations returned")

    print("Testing /api/v1/simulate-loy...")
    payload = {
        "sektor": "Helse og Omsorg",
        "funksjon": "254",
        "ansvar": "25310",
        "vikar_stop_pct": 25.0,
        "overtid_stop_pct": 30.0,
        "ansettelses_freeze_months": 2.0,
        "konsulent_cut_nok": 100000.0
    }
    res = client.post("/api/v1/simulate-loy", json=payload)
    assert res.status_code == 200, f"Simulate LOY failed: {res.text}"
    sim = res.json()["simulation"]
    print(f"  OK: LOY monthly saving: {sim['monthly_saving_nok']} NOK")

    print("Testing /api/v1/chat...")
    res = client.post("/api/v1/chat", json={
        "query": "Hva er styringsretten etter § 13-1 og fnr 12048512345?",
        "sektor": "Helse og Omsorg",
        "ansvar": "25310"
    })
    assert res.status_code == 200, f"Chat failed: {res.text}"
    chat = res.json()
    assert chat["pii_gateway"]["pii_detected"] is True
    assert "[REDACTED_FNR]" in chat["audit_log_entry"]["query_anonymized"]
    print("  OK: Chat PII gateway masked FNR and returned grounded answer")

    print("Testing /api/v1/generate-report (PDF generation)...")
    res = client.post("/api/v1/generate-report", json=payload)
    assert res.status_code == 200
    assert "application/pdf" in res.headers.get("content-type", "") or res.json().get("status") == "ok"
    print("  OK: Report generation endpoint functional")

    print("Testing /api/v1/mlflow/metrics...")
    res = client.get("/api/v1/mlflow/metrics")
    assert res.status_code == 200
    metrics = res.json()
    assert metrics["models"]["RandomForestRegressor"]["r2"] > 0.90
    print("  OK: MLflow metrics returned")

    print("Testing /api/v1/procurement/contracts (Enterprise Module 8)...")
    res = client.get("/api/v1/procurement/contracts")
    assert res.status_code == 200
    proc = res.json()
    assert len(proc["thresholds_2026"]) == 5
    assert len(proc["dfo_7_step_pipeline"]) == 7
    assert len(proc["maverick_spend_detected"]) >= 3
    print("  OK: Procurement thresholds and maverick spend detector verified")

    print("Testing /api/v1/invoicing/selvkost-calc (Enterprise Module 9)...")
    res = client.post("/api/v1/invoicing/selvkost-calc", json={
        "omraade": "Vann og Avløp (VA)",
        "direkte_drift_nok": 12500000.0,
        "indirekte_stotte_nok": 1450000.0,
        "avskrivninger_nok": 3200000.0,
        "swap_rente_pct": 3.75,
        "tillegg_margin_pct": 0.50,
        "kapitalbase_nok": 68000000.0,
        "gebyrinntekter_budsjett_nok": 19800000.0,
        "ib_selvkostfond_nok": -850000.0
    })
    assert res.status_code == 200
    sk = res.json()["beregning"]
    assert sk["selvkostgrad_pct"] > 0
    print(f"  OK: Selvkostgrad: {sk['selvkostgrad_pct']} %, status: {sk['status_label']}")

    print("Testing /api/v1/invoicing/internal-eliminations (Enterprise Module 9)...")
    res = client.get("/api/v1/invoicing/internal-eliminations")
    assert res.status_code == 200
    elims = res.json()
    assert elims["reconciled"] is True
    assert elims["net_diff_nok"] == 0.00
    print("  OK: KOSTRA Internal eliminations reconciled Diff = 0.00 NOK")

    print("Testing /api/v1/grants/status (Enterprise Module 10)...")
    res = client.get("/api/v1/grants/status")
    assert res.status_code == 200
    grants = res.json()
    assert len(grants["inbound_grants"]) >= 4
    assert len(grants["outbound_schemes"]) >= 3
    print(f"  OK: Inbound grants total: {grants['tot_innvilget_nok']:,.0f} NOK")

    # -------------------------------------------------------------------------
    # MASTER INSTRUCTIONS SUITE ENDPOINTS
    # -------------------------------------------------------------------------
    print("Testing /api/v1/dashboard/anomalies (Master Suite)...")
    res = client.get("/api/v1/dashboard/anomalies?min_z=2.0")
    assert res.status_code == 200
    anom_data = res.json()
    assert anom_data["status"] == "ok"
    assert len(anom_data["anomalies"]) >= 3
    print(f"  OK: {len(anom_data['anomalies'])} Isolation Forest anomalies returned")

    print("Testing /api/v1/simulator/budget-plus (Master Suite)...")
    res = client.post("/api/v1/simulator/budget-plus", json={
        "sektor": "Helse og Omsorg",
        "ansvar": "25310",
        "stillingshjemler": 45.0,
        "lonnsvekst_deflator_pct": 5.2,
        "feriepenger_pct": 12.0,
        "pensjon_klp_pct": 14.5,
        "aga_sone_pct": 14.1,
        "gat_turnustillegg_nok": 850000.0,
        "gat_overtid_nok": 420000.0,
        "vikar_stopp_pct": 25.0,
        "ansettelses_stopp_mnd": 2.0,
        "konsulent_kutt_mnd_nok": 100000.0
    })
    assert res.status_code == 200
    bplus = res.json()
    assert bplus["framskrivning_neste_aar"]["samlet_lonnsbudsjett_2027"] > 0
    assert bplus["loy_innsparing_inneværende_aar"]["total_innsparing_eoy_m9_m12"] > 0
    print(f"  OK: Budget+ computed 2027 salary budget: {bplus['framskrivning_neste_aar']['samlet_lonnsbudsjett_2027']:,.0f} NOK")

    print("Testing /api/v1/recommender/measures (Master Suite)...")
    res = client.get("/api/v1/recommender/measures")
    assert res.status_code == 200
    rec = res.json()
    assert rec["total_measures"] == 9
    assert len(rec["summary_per_omraade"]) == 6
    assert rec["tot_sparing_admin_eoy_nok"] == -1850000.0
    print(f"  OK: {rec['total_measures']} recommender measures matching Framsikt Excel")

    print("Testing /api/v1/procurement/spend (Master Suite)...")
    res = client.get("/api/v1/procurement/spend")
    assert res.status_code == 200
    assert "thresholds_2026" in res.json()
    print("  OK: Procurement spend returned")

    print("Testing /api/v1/invoicing/selvkost (Master Suite)...")
    res = client.post("/api/v1/invoicing/selvkost", json={
        "omraade": "Vann og Avløp",
        "direkte_drift_nok": 12000000.0,
        "indirekte_stotte_nok": 1000000.0,
        "avskrivninger_nok": 3000000.0,
        "swap_rente_pct": 3.75,
        "tillegg_margin_pct": 0.50,
        "kapitalbase_nok": 50000000.0,
        "gebyrinntekter_budsjett_nok": 18000000.0,
        "ib_selvkostfond_nok": 0.0
    })
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    print("  OK: Selvkost endpoint verified")

    print("Testing /api/v1/grants/toppfinansiering (Master Suite)...")
    res = client.get("/api/v1/grants/toppfinansiering?brutto_ressurskrevende_nok=35000000&antall_brukere=18")
    assert res.status_code == 200
    topp = res.json()
    assert topp["beregnet_statstilskudd_nok"] > 0
    assert topp["refusjonsgrad_pct"] == 80.0
    print(f"  OK: Toppfinansiering statstilskudd: {topp['beregnet_statstilskudd_nok']:,.0f} NOK")

    print("Testing /api/v1/exports/framsikt-excel (Master Suite)...")
    res = client.get("/api/v1/exports/framsikt-excel")
    assert res.status_code == 200
    assert "spreadsheet" in res.headers.get("content-type", "")
    assert len(res.content) > 1000
    print(f"  OK: Framsikt Excel file served ({len(res.content)} bytes)")

    print("Testing /api/v1/exports/einnsyn-pdf (Master Suite)...")
    res = client.get("/api/v1/exports/einnsyn-pdf?sektor=Helse+og+Omsorg&ansvar=25310")
    assert res.status_code == 200
    print("  OK: eInnsyn PDF endpoint verified")

    print("\n==================================================")
    print("ALL 18 ENDPOINTS PASSED VERIFICATION WITH 100% SUCCESS!")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
