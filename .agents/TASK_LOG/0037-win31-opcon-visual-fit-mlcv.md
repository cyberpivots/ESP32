# Task Log 0037 - Win31 OPCON Visual Fit ML/CV Pass

## Task

- ID: 0037-win31-opcon-visual-fit-mlcv
- Owner role: QA, Communications
- Status: live visual proof captured; transcript counter gate needs manual review
- Created: 2026-05-24
- Updated: 2026-05-24
- Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Use local ML/CV-style visual analysis to prioritize and implement a Win31
OPCON dashboard layout pass so the console/log region is fully visible in the
1024x600 Pi proof capture.

## Scope

Included:

- Extended `scripts/win31_dashboard_legibility_analyzer.py` with advisory
  layout-fit metrics: estimated frame/client bounds, safe margins, region
  bands, region spacing/overlap, navigation-label OCR checks, and fit risks.
- Added fixture coverage for clipped and safe Win31-like console layouts.
- Regenerated the baseline advisory JSON/Markdown against the existing
  2026-05-24 copied screenshot packet; it now records 17/17 baseline screens
  with `console_fit_risk` and `log_region_overflow`.
- Implemented the paired DOS-C source change in
  `/mnt/h/dos-c/software/win31-operator/src/operator.c`: compact 640x330
  client target, shorter list/detail panes, shorter footer/log strip, corrected
  bottom log frame, and normal top-left launch instead of forced maximize.
- Captured a revised Pi screenshot packet at
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-24-win31-opcon-visual-fit/visual-fit-20260524T175101Z/`
  and reran the DOS-C vision gate plus this advisory analyzer.

Excluded:

- ESP32 firmware changes, live hardware mutation, bridge wire-protocol changes,
  PCAP reopening, packet-driver work, flashing, erase, monitor, serial writes,
  relay, XBee, BLE, mesh, router-admin, MicroSD, load, or mains work.

## Sources

- `SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23`
- `SRC-LOCAL-WIN31-DASHBOARD-LEGIBILITY-RESEARCH-2026-05-24`
- `SRC-OPENCV-TEMPLATE-MATCHING-2026-05-23`
- `SRC-TESSERACT-IMAGE-QUALITY-2026-05-23`
- `SRC-MICROSOFT-WIN32-UI-PRINCIPLES-2026-05-24`
- `SRC-MICROSOFT-MENU-GUIDELINES-2026-05-24`
- `SRC-NNG-HEURISTICS-SUMMARY-2026-05-24`

## Artifacts

- [../../scripts/win31_dashboard_legibility_analyzer.py](../../scripts/win31_dashboard_legibility_analyzer.py)
- [../../tests/live_bench/test_win31_dashboard_legibility_analyzer.py](../../tests/live_bench/test_win31_dashboard_legibility_analyzer.py)
- [../../research/win31-dashboard-legibility/2026-05-24-full-completion-legibility-analysis.json](../../research/win31-dashboard-legibility/2026-05-24-full-completion-legibility-analysis.json)
- [../../docs/projects/espnow-bbs/win31-dashboard-legibility-backlog.md](../../docs/projects/espnow-bbs/win31-dashboard-legibility-backlog.md)
- DOS-C source: `/mnt/h/dos-c/software/win31-operator/src/operator.c`
- DOS-C docs: `/mnt/h/dos-c/software/win31-operator/README.md`
- Revised ignored proof packet:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-24-win31-opcon-visual-fit/visual-fit-20260524T175101Z/`
- Revised advisory analyzer outputs:
  `visual-fit-legibility-analysis.json` and
  `visual-fit-legibility-report.md` under that ignored proof packet.

## Validation

- `python3 -m py_compile scripts/win31_dashboard_legibility_analyzer.py tests/live_bench/test_win31_dashboard_legibility_analyzer.py`
- `python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py`
- `python3 scripts/verify_scaffold.py`
- From `/mnt/h/dos-c`: `bash -n software/win31-operator/build-watcom.sh`
- From `/mnt/h/dos-c`: `bash tests/win31_operator/run_host_tests.sh`
- From `/mnt/h/dos-c`: `bash software/win31-operator/build-watcom.sh`
- From `/mnt/h/dos-c`: `bash scripts/verify_scaffold.sh`
- `git diff --check` in `/mnt/h/ESP32`
- `git diff --check` in `/mnt/h/dos-c`

Live proof notes:

- Pi identity: `dos-pi4-poe`, Raspberry Pi 4 Model B Rev 1.2, revision
  `c03112`, serial `10000000aaaa5b24`.
- Revised packet screenshots: 11; target views mapped: 10/10.
- Advisory analyzer revised-packet metrics: lowest layout bottom margin
  `135 px`, lowest layout right margin `6 px`, no `console_fit_risk`, and no
  `log_region_overflow`.
- DOS-C `win31_dashboard_vision_gate.py` returned
  `status: needs_manual_review`; the only failure was `counters_not_moving`.
- Bridge transcript recorded 35 lines including `hello`, `state_get`,
  `peer_list`, `diag_get`, `fw_inventory`, `coordinator_state`,
  `download_list`, `download_status`, `otap_status`, `msg_pull`, `msg_post`,
  `otap_intent`, `msg_search`, and `msg_ack`.
- Cleanup proof cleared DOSBox-X, the quit modal, bridge process, and
  listeners `31331`, `31332`, `31333`, and `8080`.

Staged ignored DOS-C binary hashes:

- `OPCON.EXE`: `c84e25ba522d90c28d3106c165828597e7a9a863452c5427636f9809e3fdb5a1`
- `OPCONPC.EXE`: `5aeaec8ce89cfe4a939a16dc9f23727623c856ad5fc18062cba51bf73f9a05cd`

## Next Gate

The visual-fit subgoal is measured as improved: the revised packet keeps the
console/log region inside the capture with a 135 px bottom quiet zone and no
layout-fit overflow flags. Full automated screenshot acceptance still needs a
fresh telemetry-refresh proof or reviewer acceptance for the
`counters_not_moving` vision-gate failure.
