# Win31 Dashboard Legibility Research Source Ledger

Date: 2026-05-24

Source index: [../source-index.md](../source-index.md)

## Sources Used

- `SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23`
- `SRC-LOCAL-WIN31-DASHBOARD-LEGIBILITY-RESEARCH-2026-05-24`
- `SRC-OPENCV-TEMPLATE-MATCHING-2026-05-23`
- `SRC-TESSERACT-IMAGE-QUALITY-2026-05-23`
- `SRC-WCAG-CONTRAST-MINIMUM-2026-05-24`
- `SRC-MICROSOFT-WIN32-UI-PRINCIPLES-2026-05-24`
- `SRC-MICROSOFT-MENU-GUIDELINES-2026-05-24`
- `SRC-NNG-HEURISTICS-SUMMARY-2026-05-24`

## Verified Facts

- The accepted baseline packet is copied local evidence at
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-24-win31-viewfinder-full-completion/full-completion-20260524T135020Z/`.
- The baseline DOS-C `vision-gate.json` status is `pass` with no failures.
- The advisory analyzer measured 17 screenshots and mapped all 10 target
  views: Home, BBS, Downloads, Network, Peers, OTAP, Settings, Wizard,
  Diagnostics, and Safety.
- The analyzer reports OCR confidence and word count from copied
  `vision-gate.json`, plus local pixel metrics for foreground density, color
  clusters, estimated contrast, edge load, decorative OCR noise, estimated
  layout regions, navigation-label readability, and client/log safe margins.
- The generated backlog ranks full Win31 console fit, contrast, and
  bottom/status overflow pressure as the top three implementation evidence
  items for the baseline packet.
- A revised visual-fit packet was later analyzed at
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-24-win31-opcon-visual-fit/visual-fit-20260524T175101Z/`.
  The revised analyzer output measured 11 screenshots, mapped 10/10 target
  views, and reported lowest layout bottom margin `135 px`, lowest layout
  right margin `6 px`, no `console_fit_risk`, and no `log_region_overflow`.
- The revised DOS-C vision gate returned `needs_manual_review` with the single
  failure `counters_not_moving`; cleanup evidence cleared DOSBox-X, the modal,
  bridge process, and listeners `31331`, `31332`, `31333`, and `8080`.

## Assumptions

- Tesseract OCR confidence and word counts are useful local proxies for
  legibility comparison, not independent acceptance proof.
- Pixel-level contrast and density heuristics should be compared between
  revisions and should not replace human review or the existing pass/fail
  gate.

## Unknowns

- No user study, PaddleOCR benchmark, or hosted vision critique is approved by
  this task.
- The current revised packet did not prove moving counter values between
  screenshots; a fresh telemetry-refresh capture or reviewer acceptance is
  needed before full automated screenshot acceptance is claimed.

## Stop Gate

This ledger does not authorize firmware changes, bridge wire-protocol changes,
live hardware mutation, live mesh file delivery, live flashing, relay, XBee,
TFT, MicroSD, load, mains, erase, monitor, serial writes, PCAP, packet-driver,
or router-admin work.

The DOS-C vision gate and ESP32 completion gate remain transcript-first and
unchanged by this advisory research backlog.

## Validation

- `python3 -m py_compile scripts/win31_dashboard_legibility_analyzer.py tests/live_bench/test_win31_dashboard_legibility_analyzer.py`
- `python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py`
- `python3 scripts/win31_dashboard_legibility_analyzer.py --evidence-root /mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-24-win31-viewfinder-full-completion/full-completion-20260524T135020Z --analysis-date 2026-05-24 --out-json research/win31-dashboard-legibility/2026-05-24-full-completion-legibility-analysis.json --out-report docs/projects/espnow-bbs/win31-dashboard-legibility-backlog.md`
- Deterministic output check: two `/tmp` analyzer runs byte-matched for JSON
  and Markdown via `cmp -s`.
- `python3 tests/live_bench/test_espnow_bbs_live_gate.py`
- `python3 tests/live_bench/test_multipeer_preflight.py`
- `python3 scripts/verify_scaffold.py`
- From `/mnt/h/dos-c`: `python3 tests/test_win31_dashboard_vision_gate.py`
- From `/mnt/h/dos-c`: `tests/espnow_bbs_bridge/run_tests.sh`
- From `/mnt/h/dos-c`: `tests/win31_operator/run_host_tests.sh`
- From `/mnt/h/dos-c`: `tests/win31_netstack/run_host_tests.sh`
- `git diff --check`
