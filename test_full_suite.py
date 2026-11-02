import sys
import os
import re
from playwright.sync_api import sync_playwright

def run_all_tests():
    sys.stdout.reconfigure(encoding='utf-8')
    print("=" * 70)
    print("🚀 STARTER FULL TESTSUITE FOR KOSTRA AI WORKBENCH")
    print("=" * 70)

    html_path = os.path.abspath("index.html").replace("\\", "/")
    file_url = f"file:///{html_path}"

    console_errors = []
    page_errors = []

    test_results = []

    def record_test(name, passed, detail=""):
        status = "✅ PASS" if passed else "❌ FAIL"
        test_results.append((name, passed, detail))
        print(f"[{status}] {name}")
        if detail and not passed:
            print(f"       Detalj: {detail}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Listen for console errors & unhandled exceptions
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: page_errors.append(str(err)))

        print(f"Navigerer til: {file_url}")
        page.goto(file_url, wait_until="networkidle")

        # -------------------------------------------------------------
        # TEST 1: Initial Page Load & Zero Console Errors
        # -------------------------------------------------------------
        print("\n--- TESTBLOKK 1: Sideoppstart & Feilfri Konsoll ---")
        title = page.title()
        record_test("Tittel er lastet korrekt", "KOSTRA AI Workbench" in title, f"Tittel: {title}")
        record_test("Null ubehandlede JavaScript-feil ved oppstart", len(page_errors) == 0, f"Feil: {page_errors}")
        record_test("Null console.error meldinger ved oppstart", len(console_errors) == 0, f"Feil: {console_errors}")

        # -------------------------------------------------------------
        # TEST 2: Navigasjon mellom alle SPA-visninger
        # -------------------------------------------------------------
        print("\n--- TESTBLOKK 2: SPA Navigasjon mellom moduler ---")
        nav_targets = [
            ("view-avvik", "Avviksoversikt"),
            ("view-tidsserie", "Tidsserier"),
            ("view-eda", "EDA FT Vocabulary"),
            ("view-min-okonomi", "Min Økonomi"),
            ("view-budget", "Budsjett & Lønn"),
            ("view-evm", "Prosjektcontrolling EVM"),
            ("view-recommender", "Recommender"),
            ("view-aarshjul", "Årshjul & Frister"),
            ("view-invoicing", "Gebyrer & Faktura"),
            ("view-ml", "Prediktiv ML"),
            ("view-anomaly", "Avviksdeteksjon"),
            ("view-cockpit", "Cockpit Pipeline")
        ]

        for target_id, label in nav_targets:
            btn = page.query_selector(f'.nav-btn[data-target="{target_id}"]')
            if btn:
                btn.click()
                page.wait_for_timeout(50)
                is_active = page.evaluate(f'''() => {{
                    const el = document.getElementById("{target_id}");
                    return el && !el.classList.contains("inactive") && el.getAttribute("aria-hidden") === "false";
                }}''')
                record_test(f"Navigasjon til {label} ({target_id})", bool(is_active))
            else:
                record_test(f"Knapp for {label} finnes", False, f"Mangler .nav-btn for {target_id}")

        # -------------------------------------------------------------
        # TEST 2B: De 4 Arbeidsrommene (Rollebasert Navigasjon & Tiltakskort)
        # -------------------------------------------------------------
        print("\n--- TESTBLOKK 2B: De 4 Arbeidsrommene & Rollebasert Navigasjon ---")
        # 1. Arbeidsrom 1: Min Hverdag (Enhetsleder)
        page.click("#btn-role-hverdag")
        page.wait_for_timeout(100)
        hverdag_active = page.evaluate('''() => {
            const btn = document.getElementById("btn-role-hverdag");
            const view = document.getElementById("view-min-okonomi");
            const hasClass = btn?.classList.contains("active");
            const viewVisible = view && !view.classList.contains("inactive");
            const cards = document.querySelectorAll("#daily-action-card-container .action-task-card").length;
            const navFiltered = document.querySelector(".module-nav")?.classList.contains("filter-active");
            return { hasClass, viewVisible, cards, navFiltered };
        }''')
        record_test("Arbeidsrom 1 (Min Hverdag) aktiverer view-min-okonomi", 
                    hverdag_active["hasClass"] and hverdag_active["viewVisible"], 
                    f"Resultat: {hverdag_active}")
        record_test("Handlingspanelet 'Hva bør jeg gjøre i dag?' har 3 tiltakskort",
                    hverdag_active["cards"] == 3,
                    f"Kort: {hverdag_active['cards']}")
        record_test("Sidebar aktiverer rollefiltrering (.filter-active)",
                    bool(hverdag_active["navFiltered"]))

        # 2. Arbeidsrom 2: Budsjett & Simulering (Økonomirådgiver)
        page.click("#btn-role-budsjett")
        page.wait_for_timeout(100)
        budsjett_active = page.evaluate('''() => {
            const btn = document.getElementById("btn-role-budsjett");
            const view = document.getElementById("view-budget");
            return btn?.classList.contains("active") && view && !view.classList.contains("inactive");
        }''')
        record_test("Arbeidsrom 2 (Budsjett & Simulering) aktiverer view-budget", bool(budsjett_active))

        # 3. Arbeidsrom 3: Innkjøp, Avtaler & Tilskudd (Fagansvarlig)
        page.click("#btn-role-innkjop")
        page.wait_for_timeout(100)
        innkjop_active = page.evaluate('''() => {
            const btn = document.getElementById("btn-role-innkjop");
            const view = document.getElementById("view-procurement");
            return btn?.classList.contains("active") && view && !view.classList.contains("inactive");
        }''')
        record_test("Arbeidsrom 3 (Innkjøp & Avtaler) aktiverer view-procurement", bool(innkjop_active))

        # 4. Arbeidsrom 4: Saksbehandling & Politikk (Kommunalsjef/Bystyre)
        page.click("#btn-role-politikk")
        page.wait_for_timeout(100)
        politikk_active = page.evaluate('''() => {
            const btn = document.getElementById("btn-role-politikk");
            const view = document.getElementById("view-aarshjul");
            return btn?.classList.contains("active") && view && !view.classList.contains("inactive");
        }''')
        record_test("Arbeidsrom 4 (Saksbehandling & Politikk) aktiverer view-aarshjul", bool(politikk_active))

        # 5. Tilbakestill til Alle Verktøy
        page.click("#btn-role-all")
        page.wait_for_timeout(100)
        all_active = page.evaluate('''() => {
            const btn = document.getElementById("btn-role-all");
            const navFiltered = document.querySelector(".module-nav")?.classList.contains("filter-active");
            return btn?.classList.contains("active") && !navFiltered;
        }''')
        record_test("Arbeidsrom 'Alle Verktøy' tilbakestiller filter i sidebar", bool(all_active))

        # -------------------------------------------------------------
        # TEST 3: Global Filterkaskadering & Synkronisering
        # -------------------------------------------------------------
        print("\n--- TESTBLOKK 3: Dynamisk Filterkaskadering & Synkronisering ---")
        # Gå til Avviksoversikt først
        page.click('.nav-btn[data-target="view-avvik"]')

        # Velg Helse og Omsorg i global filter
        page.select_option("#flt-sektor", "Helse og Omsorg")
        page.wait_for_timeout(100)

        # Sjekk kaskadering i flt-ansvar (skal ha 4 helseenheter)
        ansvar_options = page.evaluate('''() => {
            const sel = document.getElementById("flt-ansvar");
            return Array.from(sel.options).map(o => ({ value: o.value, text: o.text }));
        }''')
        has_4_helse = len(ansvar_options) == 5 and any("25310" in o["value"] for o in ansvar_options)
        record_test("flt-ansvar kaskaderer til 4 Helse-enheter", has_4_helse, f"Valg: {len(ansvar_options)}")

        # Sjekk synkronisering i ts-flt-ansvar, rec-flt-ansvar, aarshjul-flt-ansvar
        synced_ansvar = page.evaluate('''() => {
            const ts = document.getElementById("ts-flt-ansvar")?.options.length;
            const rec = document.getElementById("rec-flt-ansvar")?.options.length;
            const aars = document.getElementById("aarshjul-flt-ansvar")?.options.length;
            return { ts, rec, aars };
        }''')
        record_test("Synkronisering av ansvar-dropdowns på tvers av moduler", 
                    synced_ansvar["ts"] == 5 and synced_ansvar["rec"] == 5 and synced_ansvar["aars"] == 5,
                    f"Resultat: {synced_ansvar}")

        # Sjekk at toppbanner oppdateres
        banner_text = page.inner_text("#active-filter-banner")
        record_test("Toppbanner viser Helse og Omsorg", "Helse og Omsorg" in banner_text, f"Banner: {banner_text}")

        # Velg Funksjon 254
        page.select_option("#flt-funksjon", "254")
        page.wait_for_timeout(100)
        status_pill_text = page.inner_text("#header-status-pill")
        record_test("Status-pill viser kritisk avvik (-1 285 614 kr)", "-1 285 614" in status_pill_text, f"Status: {status_pill_text}")

        # -------------------------------------------------------------
        # TEST 4: Modul 2B: EDA Visuals & FT Guide
        # -------------------------------------------------------------
        print("\n--- TESTBLOKK 4: EDA Visuals & FT Visual Vocabulary ---")
        page.click('.nav-btn[data-target="view-eda"]')
        page.wait_for_timeout(150)

        eda_title = page.inner_text("#eda-canvas-title")
        eda_stat = page.inner_text("#eda-canvas-stat")
        eda_tufte = page.inner_text("#eda-guide-tufte")
        record_test("EDA tittel er Helse & Mestring Vikarer vs. Overtid", "Helse & Mestring: Vikarer vs. Overtid" in eda_title, f"Tittel: {eda_title}")
        record_test("EDA OLS Trend R² = 0,94", "0,94" in eda_stat, f"Stat: {eda_stat}")
        record_test("EDA Tufte guide inneholder kontrollør-rød #D62728", "#D62728" in eda_tufte, f"Tufte: {eda_tufte}")

        # Sjekk SVG-sirkler og farger
        circles_count = page.evaluate('''() => {
            return document.querySelectorAll("#eda-chart-canvas circle.eda-point").length;
        }''')
        record_test("EDA spredningsplott har 4 datapunkter for Helse", circles_count == 4, f"Antall: {circles_count}")

        # Test Tilbakestill akser knapp
        page.click("#eda-reset-view-btn")
        page.wait_for_timeout(100)
        eda_stat_after_reset = page.inner_text("#eda-canvas-stat")
        record_test("EDA Tilbakestill akser bevarer R² = 0,94", "0,94" in eda_stat_after_reset)

        # -------------------------------------------------------------
        # TEST 5: Modul 11: Lønns- og Stillingsbudsjett
        # -------------------------------------------------------------
        print("\n--- TESTBLOKK 5: Lønns- og Stillingsbudsjett (Dynamisk) ---")
        page.click('.nav-btn[data-target="view-budget"]')
        page.wait_for_timeout(150)

        # Siden filteret er på Helse og Omsorg (Fn 254):
        fte_val = page.inner_text("#budget-kpi-fte")
        filter_strip_fte = page.inner_text("#budget-active-filter-fte-stat")
        record_test("Budsjett KPI viser 168,0 FTE planlagt for Helse", "168,0" in fte_val, f"FTE: {fte_val}")
        record_test("Filterstripe viser 168,0 FTE • 4 Enheter", "168,0 FTE" in filter_strip_fte and "4 Enheter" in filter_strip_fte, f"Filterstripe: {filter_strip_fte}")

        # Sjekk antall rader i bemanningsramme tabellen
        fte_rows = page.evaluate('''() => {
            return document.querySelectorAll("#salary-fte-table-body tr").length;
        }''')
        record_test("Bemanningsramme-tabell viser nøyaktig 4 helseenheter", fte_rows == 4, f"Rader: {fte_rows}")

        # Sjekk KOSTRA artstabell
        art_rows = page.evaluate('''() => {
            return document.querySelectorAll("#salary-art-table-body tr").length;
        }''')
        record_test("KOSTRA artstabell har 9 kostnadsarter", art_rows == 9, f"Arter: {art_rows}")

        # -------------------------------------------------------------
        # TEST 5B: Modul 13: Prosjektcontrolling & EVM (Umoe Mandal / Maritim)
        # -------------------------------------------------------------
        print("\n--- TESTBLOKK 5B: Prosjektcontrolling & EVM (ANSI/EIA-748) ---")
        page.click('.nav-btn[data-target="view-evm"]')
        page.wait_for_timeout(150)

        evm_bac = page.inner_text("#evm-kpi-bac")
        evm_cpi = page.inner_text("#evm-kpi-cpi")
        evm_spi = page.inner_text("#evm-kpi-spi")
        evm_eac = page.inner_text("#evm-kpi-eac")
        record_test("EVM P-40102 SES Flerbruksfartøy BAC = 120 MNOK", "120 000 000" in evm_bac.replace('\u00a0', ' '), f"BAC: {evm_bac}")
        record_test("EVM Kostnadsindeks CPI = 0,90 (Overskridelse pr krone)", "0,90" in evm_cpi, f"CPI: {evm_cpi}")
        record_test("EVM Fremdriftsindeks SPI = 0,92 (Tidsforsinkelse)", "0,92" in evm_spi, f"SPI: {evm_spi}")
        record_test("EVM Sluttkostnad EAC = 132,6 MNOK", "132" in evm_eac and "631" in evm_eac, f"EAC: {evm_eac}")

        # Sjekk Tufte S-kurve SVG elementer
        scurve_polylines = page.evaluate('''() => {
            return document.querySelectorAll("#evm-scurve-svg polyline").length;
        }''')
        record_test("Tufte S-kurve SVG inneholder PV, EV og AC polylinjer", scurve_polylines >= 3, f"Polylines: {scurve_polylines}")

        # Sjekk WBS tabell for arbeidspakker
        wbs_rows = page.evaluate('''() => {
            return document.querySelectorAll("#tbody-evm-wbs tr").length;
        }''')
        record_test("WBS Nivå 2 har 7 spesifiserte arbeidspakker", wbs_rows == 7, f"WBS rader: {wbs_rows}")

        # Test prosjektbytte til Kystvaktpatrulje (PRJ-KV-02)
        page.select_option("#evm-project-select", "PRJ-KV-02")
        page.wait_for_timeout(150)
        kv_bac = page.inner_text("#evm-kpi-bac")
        kv_cpi = page.inner_text("#evm-kpi-cpi")
        record_test("Prosjektbytte til P-30240 Kystvakt oppdaterer BAC til 45 MNOK", "45 000 000" in kv_bac.replace('\u00a0', ' '), f"KV BAC: {kv_bac}")
        record_test("Kystvaktpatrulje har positiv CPI = 1,05 (Mindreforbruk)", "1,05" in kv_cpi, f"KV CPI: {kv_cpi}")

        # Bytt tilbake til SES for konsistens
        page.select_option("#evm-project-select", "PRJ-SES-01")
        page.wait_for_timeout(100)

        # -------------------------------------------------------------
        # TEST 6: Modul 13: Recommender & Tiltaksmatrise
        # -------------------------------------------------------------
        print("\n--- TESTBLOKK 6: Recommender & Tiltaksmatrise ---")
        page.click('.nav-btn[data-target="view-recommender"]')
        page.wait_for_timeout(150)

        rec_count = page.inner_text("#rec-filter-match-count")
        rec_audit = page.inner_text("#audit-global-status-badge")
        record_test("Recommender filtermatcher viser aktive tiltak", "Viser" in rec_count, f"Matcher: {rec_count}")
        record_test("Revisor-agenten krever overstyring for Helse (AML § 10-8)", "AML § 10-8" in rec_audit, f"Revisor: {rec_audit}")

        # Test filterknapp for Administrative tiltak
        page.click("#btn-rec-filter-admin")
        page.wait_for_timeout(100)
        admin_count_after = page.inner_text("#rec-kpi-count")
        record_test("Filtrering på Administrative EOY oppdaterer KPI", "Tiltak" in admin_count_after, f"KPI: {admin_count_after}")

        # -------------------------------------------------------------
        # TEST 7: Modul 14: Årshjul & Dokumentgenerator
        # -------------------------------------------------------------
        print("\n--- TESTBLOKK 7: Årshjul, Frister & Dokumentgenerator ---")
        page.click('.nav-btn[data-target="view-aarshjul"]')
        page.wait_for_timeout(150)

        # Sjekk månedskort i styringshjulet
        month_cards = page.evaluate('''() => {
            return document.querySelectorAll("#aarshjul-months-grid .panel-card").length;
        }''')
        record_test("Styringshjulet har 12 månedskort", month_cards == 12, f"Måneder: {month_cards}")

        # Sjekk at dokumentgenerator inneholder reelle tall (ikke 165M fallback)
        doc_preview = page.inner_text("#aarshjul-doc-preview-container")
        record_test("Dokumentgenerator inneholder Helse og Omsorg", "Helse og Omsorg" in doc_preview, f"Dokumentpreview: {doc_preview[:150]}...")
        record_test("Dokumentgenerator inneholder reelt YTD avvik (-1 285 614 kr)", "-1 285 614" in doc_preview or "12 622 851" in doc_preview)

        # Test malvelger
        page.select_option("#aarshjul-doc-template-select", "enhetsleder_avvik")
        page.wait_for_timeout(100)
        doc_preview_enhet = page.inner_text("#aarshjul-doc-preview-container")
        record_test("Bestillingsnotat til Enhetsleder generert korrekt", 
                    "bestillingsnotat" in doc_preview_enhet.lower() or "avviksforklaring" in doc_preview_enhet.lower() or "NOT-2026" in doc_preview_enhet)

        # -------------------------------------------------------------
        # TEST 8: Modul 12: Min Økonomi & Månedsrapport
        # -------------------------------------------------------------
        print("\n--- TESTBLOKK 8: Min Økonomi & Predefinerte Rapporter ---")
        page.click('.nav-btn[data-target="view-min-okonomi"]')
        page.wait_for_timeout(150)

        # Test fanevelger
        tabs = page.query_selector_all(".min-tab-btn")
        record_test("Predefinerte rapporter har 3 visningsfaner", len(tabs) == 3, f"Faner: {len(tabs)}")
        if len(tabs) >= 2:
            tabs[1].click() # Flash Ledelsesnotat
            page.wait_for_timeout(100)
            flash_visible = page.is_visible("#min-subview-flash")
            record_test("Fane 2 (Flash Ledelsesnotat) vises ved klikk", bool(flash_visible))

        # -------------------------------------------------------------
        # TEST 9: Nullstill Filter test
        # -------------------------------------------------------------
        print("\n--- TESTBLOKK 9: Komplett Tilbakestilling (Reset) ---")
        # Naviger tilbake til Avviksoversikt hvor det globale filterpanelet vises
        page.click('.nav-btn[data-target="view-avvik"]')
        page.wait_for_timeout(100)
        page.click("#btn-reset-filters")
        page.wait_for_timeout(150)

        reset_sektor = page.input_value("#flt-sektor")
        reset_ansvar = page.input_value("#flt-ansvar")
        record_test("Nullstilling setter flt-sektor til ALL", reset_sektor == "ALL", f"Sektor: {reset_sektor}")
        record_test("Nullstilling setter flt-ansvar til ALL", reset_ansvar == "ALL", f"Ansvar: {reset_ansvar}")

        # Sjekk at total sum stillinger i budsjettmodul tilbakestilles til 328,0 FTE
        page.click('.nav-btn[data-target="view-budget"]')
        page.wait_for_timeout(100)
        fte_after_reset = page.inner_text("#budget-kpi-fte")
        record_test("Budsjettmodul viser 328,0 planlagte FTE etter nullstilling", "328,0" in fte_after_reset, f"FTE: {fte_after_reset}")

        # Sjekk avsluttende console error status
        print("\n--- TESTBLOKK 10: Sluttkontroll av feillogg ---")
        record_test("Ingen uhåndterte runtime page-errors under hele testløpet", len(page_errors) == 0, f"Feil: {page_errors}")
        record_test("Ingen console.error under hele testløpet", len(console_errors) == 0, f"Feil: {console_errors}")

        browser.close()

    print("\n" + "=" * 70)
    passed_count = sum(1 for _, p, _ in test_results if p)
    total_count = len(test_results)
    print(f"📊 TESTOPPSUMMERING: {passed_count} av {total_count} tester bestått ({passed_count/total_count*100:.1f} %)")
    print("=" * 70)

    if passed_count == total_count:
        print("🎉 ALLE FUNKSJONALITETSTESTER BESTÅTT UTEN FEIL!")
        return 0
    else:
        print("⚠️ NOEN TESTER FEILET. SE DETALJER OVER.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())

