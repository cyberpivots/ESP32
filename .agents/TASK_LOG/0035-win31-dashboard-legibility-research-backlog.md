# Task Log 0035 - Win31 Dashboard Legibility Research Backlog

## Task

- ID: 0035-win31-dashboard-legibility-research-backlog
- Owner role: QA, Communications
- Status: implemented advisory backlog
- Created: 2026-05-24
- Updated: 2026-05-24
- Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Add a local-only, source-backed research backlog for the accepted Win31
dashboard screenshot packet, focused first on visual legibility and
intuitiveness.

## Scope

Included:

- `scripts/win31_dashboard_legibility_analyzer.py` reads copied screenshots
  plus `vision-gate.json` and emits deterministic JSON/Markdown advisory
  output.
- The analyzer reports per-screen OCR confidence, OCR word count, foreground
  density, color cluster usage, estimated contrast, edge/noise load,
  decorative OCR noise, and bottom/right bounds risk.
- Fixture tests cover low contrast, excessive density, missing title, cropped
  console, and strong/weak OCR cases.
- The generated backlog ranks implement-later hypotheses and acceptance
  criteria for contrast, bounds, ASCII density, hierarchy, plain task names,
  novice wording, disabled-control explanations, and before/after comparison.

Excluded:

- Firmware changes, bridge wire-protocol changes, live hardware mutation,
  changes to DOS-C `win31_dashboard_vision_gate.py`, changes to ESP32
  completion acceptance, PaddleOCR, hosted vision, live mesh file delivery,
  live flashing, relay, XBee, TFT, MicroSD, load, mains, erase, monitor,
  serial writes, PCAP, packet-driver, or router-admin work.

## Sources

- `SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23`
- `SRC-LOCAL-WIN31-DASHBOARD-LEGIBILITY-RESEARCH-2026-05-24`
- `SRC-OPENCV-TEMPLATE-MATCHING-2026-05-23`
- `SRC-TESSERACT-IMAGE-QUALITY-2026-05-23`
- `SRC-WCAG-CONTRAST-MINIMUM-2026-05-24`
- `SRC-MICROSOFT-WIN32-UI-PRINCIPLES-2026-05-24`
- `SRC-MICROSOFT-MENU-GUIDELINES-2026-05-24`
- `SRC-NNG-HEURISTICS-SUMMARY-2026-05-24`

## Artifacts

- [../../scripts/win31_dashboard_legibility_analyzer.py](../../scripts/win31_dashboard_legibility_analyzer.py)
- [../../tests/live_bench/test_win31_dashboard_legibility_analyzer.py](../../tests/live_bench/test_win31_dashboard_legibility_analyzer.py)
- [../../research/win31-dashboard-legibility/2026-05-24-full-completion-legibility-analysis.json](../../research/win31-dashboard-legibility/2026-05-24-full-completion-legibility-analysis.json)
- [../../docs/projects/espnow-bbs/win31-dashboard-legibility-backlog.md](../../docs/projects/espnow-bbs/win31-dashboard-legibility-backlog.md)
- [../../knowledge-base/source-ledger/2026-05-24-win31-dashboard-legibility-research.md](../../knowledge-base/source-ledger/2026-05-24-win31-dashboard-legibility-research.md)

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

## Handoff

Continue through
[../handoffs/0025-win31-dashboard-legibility-backlog-to-qa.md](../handoffs/0025-win31-dashboard-legibility-backlog-to-qa.md)
before implementing any UI changes from the backlog.
