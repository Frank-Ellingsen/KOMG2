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
        # Bekreft at globalt filterpanel er synlig på tvers av menyer
        page.click('.nav-btn[data-target="view-min-okonomi"]')
        page.wait_for_timeout(50)
        filter_in_min_okonomi = page.is_visible("#global-filter-panel")
        page.click('.nav-btn[data-target="view-budget"]')
        page.wait_for_timeout(50)
        filter_in_budget = page.is_visible("#global-filter-panel")
        record_test("Globalt filterpanel er synlig i Min Hverdag (view-min-okonomi)", bool(filter_in_min_okonomi))
        record_test("Globalt filterpanel er synlig i Budsjett (view-budget)", bool(filter_in_budget))

        # Gå til Avviksoversikt og velg Helse og Omsorg
        page.click('.nav-btn[data-target="view-avvik"]')
        page.wait_for_timeout(50)

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

        # Sjekk at KPI-tallene er dynamisk avstemt mot regnskap og DuckDB (ikke syntetiske 161M / 71M)
        ramme_val = page.inner_text("#budget-kpi-ramme")
        bokfort_val = page.inner_text("#budget-kpi-bokfort")
        eac_kpi_val = page.inner_text("#budget-kpi-eac")
        sosial_val = page.inner_text("#budget-kpi-sosial")
        refusjon_val = page.inner_text("#budget-kpi-refusjon")

        record_test("Budsjett KPI Vedtatt Lønnsramme er dynamisk avstemt (17 612 937 kr)",
                    "17 612 937 kr" in ramme_val and "161 719 916" not in ramme_val,
                    f"Ramme: {ramme_val}")
        record_test("Budsjett KPI Bokført Lønn YTD er dynamisk avstemt (13 290 606 kr)",
                    "13 290 606 kr" in bokfort_val and "71 745 459" not in bokfort_val,
                    f"Bokført: {bokfort_val}")
        record_test("Budsjett KPI Forventet Årsavvik Lønn er dynamisk avstemt (+2 322 973 kr)",
                    "+2 322 973 kr" in eac_kpi_val and "+12 484 662" not in eac_kpi_val,
                    f"EAC: {eac_kpi_val}")
        record_test("Budsjett KPI NAV-refusjon er dynamisk avstemt (-732 705 kr)",
                    "-732 705 kr" in refusjon_val and "-5 296 676" not in refusjon_val,
                    f"Refusjon: {refusjon_val}")
        record_test("Budsjett KPI Sosiale kostnader er dynamisk avstemt (3 738 319 kr)",
                    "3 738 319 kr" in sosial_val and "40 098 215" not in sosial_val,
                    f"Sosial: {sosial_val}")

        # Sjekk Stillingskategorier & Lønnsbudsjettering Neste År (Framsikt)
        pos_rows = page.evaluate('''() => {
            return document.querySelectorAll("#salary-positions-table-body tr").length;
        }''')
        record_test("Stillingskategori-tabell har 6 stillinger for Helse og Omsorg", pos_rows == 6, f"Stillinger: {pos_rows}")

        pos_badge = page.inner_text("#positions-fte-badge")
        record_test("Stillingskategori FTE-badge viser 168,0 FTE", "168,0 FTE" in pos_badge, f"Badge: {pos_badge}")

        sum_basis = page.inner_text("#pos-sum-basis")
        record_test("Basislønnsmasse 2024 er bakkeforankret (15 015 731 kr)", "15 015 731 kr" in sum_basis, f"Basis: {sum_basis}")

        # Test deflator slider interaksjon
        page.evaluate('''() => {
            const el = document.getElementById("pos-sim-deflator");
            if (el) {
                el.value = "5.0";
                el.dispatchEvent(new Event("input"));
            }
        }''')
        page.wait_for_timeout(100)
        deflator_stat = page.inner_text("#pos-stat-deflator")
        record_test("Deflator-slider oppdaterer samlet vekst til 5,6 %", "5,6 %" in deflator_stat, f"Stat: {deflator_stat}")

        # Sett deflator tilbake til 4.2
        page.evaluate('''() => {
            const el = document.getElementById("pos-sim-deflator");
            if (el) {
                el.value = "4.2";
                el.dispatchEvent(new Event("input"));
            }
        }''')
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
        # TEST 8: Modul 12: Min Økonomi & Månedsrapport (Inkl. Tufte Sparklines)
        # -------------------------------------------------------------
        print("\n--- TESTBLOKK 8: Min Økonomi & Predefinerte Rapporter (Inkl. Sparkline) ---")
        page.click('.nav-btn[data-target="view-min-okonomi"]')
        page.wait_for_timeout(150)

        # Sjekk dynamisk Tufte sparkline over månedstabellen
        sparkline_info = page.evaluate('''() => {
            const box = document.getElementById("min-trend-sparkline-box");
            const svg = document.querySelector("#min-trend-sparkline-svg-wrap svg");
            const circles = document.querySelectorAll("#min-trend-sparkline-svg-wrap circle").length;
            const paths = document.querySelectorAll("#min-trend-sparkline-svg-wrap path").length;
            const kpiText = document.getElementById("min-trend-sparkline-kpi")?.textContent || "";
            const tableRows = document.querySelectorAll("#min-trend-body tr").length;
            const tableBars = document.querySelectorAll("#min-trend-body tr svg rect").length;
            const hasAvvikHeader = (document.querySelector(".data-table th:last-child")?.textContent || "").includes("Avvikssøyle");
            const tableText = document.getElementById("min-trend-body")?.innerText || "";
            const hasDoubleKr = tableText.includes("kr kr");
            return {
                boxVisible: box && getComputedStyle(box).display !== "none",
                hasSvg: !!svg,
                circles,
                paths,
                kpiText,
                tableRows,
                tableBars,
                hasAvvikHeader,
                hasDoubleKr
            };
        }''')
        record_test("Dynamisk Tufte Sparkline-boks er synlig", bool(sparkline_info["boxVisible"]))
        record_test("Sparkline SVG inneholder 8 månedspunkter (M01-M08)", sparkline_info["circles"] == 8, f"Sirkler: {sparkline_info['circles']}")
        record_test("Sparkline SVG inneholder budsjett- og regnskapskurver", sparkline_info["paths"] >= 2, f"Paths: {sparkline_info['paths']}")
        record_test("Månedstabell har 8 rader med betinget avvikssøyle (conditional bar length of avvik)", 
                    sparkline_info["tableRows"] == 8 and sparkline_info["tableBars"] == 8,
                    f"Rader: {sparkline_info['tableRows']}, Avvikssøyler: {sparkline_info['tableBars']}")
        record_test("Kolonnetittel til høyre for MoM er 'Avvikssøyle'", bool(sparkline_info["hasAvvikHeader"]))
        record_test("Fjernet overflødig 'kr kr' i MoM trend-kolonne", not sparkline_info["hasDoubleKr"])

        # Sjekk Avviksfordeling pr ansvarssted i valgt sektor (Horisontal bar length)
        unit_variance_info = page.evaluate('''() => {
            const box = document.getElementById("min-unit-variance-box");
            const title = document.getElementById("min-unit-variance-title")?.textContent || "";
            const kpi = document.getElementById("min-unit-variance-kpi")?.textContent || "";
            const rows = document.querySelectorAll("#min-unit-variance-tbody tr").length;
            const rects = document.querySelectorAll("#min-unit-variance-tbody svg rect").length;
            const bulletLines = document.querySelectorAll("#min-unit-variance-tbody svg line").length;
            const has25310 = (document.getElementById("min-unit-variance-tbody")?.innerText || "").includes("25310");
            return {
                boxVisible: box && getComputedStyle(box).display !== "none",
                title,
                kpi,
                rows,
                rects,
                bulletLines,
                has25310
            };
        }''')
        record_test("Avviksfordeling pr ansvarssted-boks er synlig under månedstabellen", bool(unit_variance_info["boxVisible"]))
        record_test("Avviksfordeling viser 4 ansvarssteder for Helse og Omsorg",
                    unit_variance_info["rows"] == 4 and unit_variance_info["rects"] == 4 and unit_variance_info["has25310"],
                    f"Rader: {unit_variance_info['rows']}, Søyler: {unit_variance_info['rects']}")
        record_test("Avviksfordeling KPI viser samlet YTD avvik (+1 285 614 kr)",
                    "1 285 614" in unit_variance_info["kpi"] or "1285614" in unit_variance_info["kpi"],
                    f"KPI: {unit_variance_info['kpi']}")
        record_test("Avviksfordeling er utformet som Bullet Graph med Budsjett-målstrek og Regnskapssøyle",
                    unit_variance_info["rects"] == 4 and unit_variance_info["bulletLines"] >= 8)

        # Sjekk Lønns- og Refusjonsprofil (Brutto vs. Netto & NAV sykelønnsrefusjon)
        sal_refund_info = page.evaluate('''() => {
            const panel = document.getElementById("min-salary-refund-panel");
            const brutto = document.getElementById("min-sal-brutto-reg")?.textContent || "";
            const sykelonn = document.getElementById("min-sal-syke-reg")?.textContent || "";
            const foreldre = document.getElementById("min-sal-foreldre-reg")?.textContent || "";
            const netto = document.getElementById("min-sal-netto-reg")?.textContent || "";
            const fravarsvikar = document.getElementById("min-sal-fravarsvikar-nok")?.textContent || "";
            const dekningsgrad = document.getElementById("min-sal-dekningsgrad-pct")?.textContent || "";
            const driversText = document.getElementById("min-drivers-body")?.innerText || "";
            const hasArt1710Badge = document.querySelector("#min-drivers-body .badge") !== null;
            const hasArt1710Subrow = document.querySelector("#min-drivers-body tr.driver-subrow-art1710") !== null;
            const hasNettoSubrow = document.querySelector("#min-drivers-body tr.driver-subrow-netto") !== null;
            return {
                panelVisible: panel && getComputedStyle(panel).display !== "none",
                brutto,
                sykelonn,
                foreldre,
                netto,
                fravarsvikar,
                dekningsgrad,
                hasArt1710Badge,
                hasArt1710Subrow,
                hasNettoSubrow,
                driversText
            };
        }''')
        record_test("Lønns- og Refusjonsprofil-panel er synlig", bool(sal_refund_info["panelVisible"]))
        record_test("Brutto og Netto personalkostnad er beregnet", 
                    sal_refund_info["brutto"] != "—" and sal_refund_info["netto"] != "—",
                    f"Brutto: {sal_refund_info['brutto']}, Netto: {sal_refund_info['netto']}")
        record_test("NAV Sykelønnsrefusjon (art 1710) vises i lønnsprofilen",
                    sal_refund_info["sykelonn"] != "—",
                    f"Sykelønnsrefusjon: {sal_refund_info['sykelonn']}, Dekningsgrad: {sal_refund_info['dekningsgrad']}")
        record_test("Kostnadsdriver-tabell har merknad eller badge for motregning mot art 1710",
                    sal_refund_info["hasArt1710Badge"] or "102000" in sal_refund_info["driversText"],
                    f"Badge: {sal_refund_info['hasArt1710Badge']}")
        record_test("Art 1710 er postet direkte under 102000 med motpost NAV refusjon", bool(sal_refund_info["hasArt1710Subrow"]))
        record_test("Netto fraværsbelastning etter Art 1710 er beregnet i tabellen", bool(sal_refund_info["hasNettoSubrow"]))
        has_ytd_col = page.evaluate('() => (document.querySelector("#min-drivers-caption")?.closest("table")?.querySelector("thead")?.innerText || "").includes("Regnskap YTD")')
        record_test("Kostnadsdriver-tabell inneholder kolonnen Regnskap YTD", bool(has_ytd_col))

        driver_layout_info = page.evaluate('''() => {
            const wrapper = document.getElementById("min-drivers-wrapper");
            const panel = document.getElementById("min-drivers-panel");
            const style = wrapper ? window.getComputedStyle(wrapper) : {};
            const isNoScroll = wrapper ? (wrapper.scrollHeight <= wrapper.clientHeight + 2) : false;
            const overflowY = style.overflowY || "";
            return {
                wrapperExists: !!wrapper,
                isNoScroll,
                overflowY
            };
        }''')
        record_test("Kostnadsdriver-tabell er tilpasset uten rullegardin (uten vertikal scrollbar)",
                    driver_layout_info["wrapperExists"] and (driver_layout_info["overflowY"] == "visible" or driver_layout_info["isNoScroll"]))

        # Sjekk Mindreforbruksanalyse (Horisontal bar chart til høyre for TOP 5 konti med mindreforbruk)
        fav_chart_info = page.evaluate('''() => {
            const panel = document.getElementById("min-favorable-panel");
            const svg = document.querySelector("#min-favorable-tbody svg");
            const rects = document.querySelectorAll("#min-favorable-tbody svg rect").length;
            const bulletLines = document.querySelectorAll("#min-favorable-tbody svg line").length;
            const tableRows = document.querySelectorAll("#min-favorable-tbody tr").length;
            const kpiText = document.getElementById("min-favorable-kpi")?.textContent || "";
            return {
                panelVisible: panel && getComputedStyle(panel).display !== "none",
                hasSvg: !!svg,
                rects,
                bulletLines,
                tableRows,
                kpiText
            };
        }''')
        record_test("Mindreforbruksanalyse-panel er synlig", bool(fav_chart_info["panelVisible"]))
        record_test("Horisontal bar chart har 5 grønne søyler for topp 5 mindreforbruk", 
                    fav_chart_info["hasSvg"] and fav_chart_info["rects"] == 5,
                    f"SVG: {fav_chart_info['hasSvg']}, Søyler: {fav_chart_info['rects']}")
        record_test("Mindreforbruksanalyse er utformet som Bullet Graph med Budsjett-målstrek og Regnskapssøyle",
                    fav_chart_info["rects"] == 5 and fav_chart_info["bulletLines"] >= 10)
        record_test("Mindreforbruk data-tabell har 5 rader", fav_chart_info["tableRows"] == 5, f"Rader: {fav_chart_info['tableRows']}")

        # Sjekk forsiktighetsprinsipp for negative regnskapstall (inntekt/tilskudd ekstrapoleres ikke i prognose)
        k112098_info = page.evaluate('''() => {
            const trs = Array.from(document.querySelectorAll("#min-favorable-tbody tr"));
            for (const tr of trs) {
                const tds = Array.from(tr.querySelectorAll("td")).map(td => td.textContent.trim());
                if (tds[0] === "112098") {
                    return {
                        code: tds[0],
                        name: tds[1],
                        ytdActual: tds[2],
                        budget: tds[3],
                        forecast: tds[4],
                        variance: tds[5]
                    };
                }
            }
            return null;
        }''')
        record_test("Forsiktighetsprinsipp: Negative inntekts-/tilskuddstall (Konto 112098) ekstrapoleres ikke (Prognose = -160 447 kr)",
                    k112098_info is not None and "-160 447 kr" in k112098_info["forecast"] and "-240 670 kr" not in k112098_info["forecast"],
                    f"Konto 112098: {k112098_info}")

        # Sjekk Dynamisk AI-Tiltaksplan & Omdisponering mot Årsbalanse (EOY)
        turnaround_info = page.evaluate('''() => {
            const panel = document.getElementById("min-ai-turnaround-panel");
            const guardBadge = document.getElementById("min-ai-guardrail-badge");
            const btn = document.getElementById("btn-apply-ai-turnaround");
            const tableRows = document.querySelectorAll("#min-ai-turnaround-body table tbody tr").length;
            const kpiText = document.getElementById("min-ai-turnaround-kpi")?.textContent || "";
            return {
                panelVisible: panel && getComputedStyle(panel).display !== "none",
                hasBadge: !!guardBadge && (guardBadge.innerText || "").toLowerCase().includes("guardrails"),
                hasBtn: !!btn,
                tableRows,
                kpiText
            };
        }''')
        record_test("Dynamisk AI-Tiltaksplan panel er synlig", bool(turnaround_info["panelVisible"]))
        record_test("AI-Tiltaksplan verifiserer lovpålagte guardrails (AML § 10-8, § 13-1)", bool(turnaround_info["hasBadge"]))
        record_test("AI-Tiltaksplan har konkrete månedlige tiltak og omdisponeringer", turnaround_info["tableRows"] >= 2, f"Rader: {turnaround_info['tableRows']}")

        # Test overføringsknapp: overfør til tiltaksavtale
        page.click("#btn-apply-ai-turnaround")
        page.wait_for_timeout(100)
        adj_text = page.inner_text("#min-adjusted-forecast")
        record_test("AI-tiltakspakke overføres til tiltakskontrakt og oppnår årsbalanse (0 kr avvik)", 
                    "0 kr" in adj_text or "balanse" in adj_text.lower(),
                    f"Justert prognose: {adj_text}")
        # Test dynamisk respons i Mindreforbruksanalyse ved filterbytte til 25310
        page.select_option("#flt-ansvar", "25310")
        page.wait_for_timeout(150)
        fav_25310_info = page.evaluate('''() => {
            const caption = document.getElementById("min-favorable-caption")?.textContent || "";
            const firstRowCode = document.querySelector("#min-favorable-tbody tr td")?.textContent || "";
            const rects = document.querySelectorAll("#min-favorable-tbody svg rect").length;
            const kpiText = document.getElementById("min-favorable-kpi")?.textContent || "";
            return { caption, firstRowCode, rects, kpiText };
        }''')
        record_test("Mindreforbruksanalyse oppdateres dynamisk ved valg av enhet 25310",
                    "25310" in fav_25310_info["caption"] and fav_25310_info["firstRowCode"] == "101031",
                    f"Caption: {fav_25310_info['caption']}, Toppkonto: {fav_25310_info['firstRowCode']}")

        # Tilbakestill ansvar til ALL (beholder Helse og Omsorg sektor)
        page.select_option("#flt-ansvar", "ALL")
        page.wait_for_timeout(150)

        # Test fanevelger
        tabs = page.query_selector_all(".min-tab-btn")
        record_test("Predefinerte rapporter har 3 visningsfaner", len(tabs) == 3, f"Faner: {len(tabs)}")
        if len(tabs) >= 3:
            tabs[1].click() # Flash Ledelsesnotat
            page.wait_for_timeout(100)
            flash_visible = page.is_visible("#min-subview-flash")
            record_test("Fane 2 (Flash Ledelsesnotat) vises ved klikk", bool(flash_visible))

            tabs[2].click() # Eksepsjonsrapport
            page.wait_for_timeout(100)
            exc_visible = page.is_visible("#min-subview-exception")
            record_test("Fane 3 (Controllerens Eksepsjonsrapport) vises ved klikk", bool(exc_visible))
            exc_text = page.inner_text("#exception-report-tbody")
            has_helse_exc = "25310" in exc_text
            has_oppvekst_exc = "20210" in exc_text or "22110" in exc_text
            record_test("Eksepsjonsrapport filtrerer dynamisk på Helse og Omsorg", has_helse_exc and not has_oppvekst_exc, f"Helse: {has_helse_exc}, Oppvekst: {has_oppvekst_exc}")

            # Gå tilbake til første fane for eventuelle videre tester
            tabs[0].click()
            page.wait_for_timeout(100)

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

