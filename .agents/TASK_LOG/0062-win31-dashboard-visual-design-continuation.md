# Task Log 0062 - Win31 Dashboard Visual Design Continuation

## Task

- ID: 0062-win31-dashboard-visual-design-continuation
- Owner role: QA, Communications
- Status: implemented; source-validated; fresh screenshot capture still pending
- Created: 2026-05-26
- Updated: 2026-05-26
- Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Continue the local-only Windows 3.1 OPCON dashboard visual-design loop by
improving navigation labels, action wording, layout height, disabled-control
copy, and high-contrast operational text without changing the bridge protocol,
ESP32 firmware behavior, serial-nullmodem transport, live hardware gates, or
completion semantics.

## Scope

Included:

- Updated `/mnt/h/dos-c/software/win31-operator/src/operator.c`.
- Increased the Win31 operator client height from `330` to `360`.
- Reflowed the fixed viewfinder shell, content panes, action strip, disabled
  footer, and log area within the 640 px client width.
- Replaced the one-row abbreviated navigation strip with two rows using:
  `HOME`, `BBS BOARD`, `DOWNLOADS`, `NETWORK`, `PEERS`, `DEVICES`, `OTAP`,
  `SETTINGS`, `WIZARD`, `DIAGNOSTICS`, and `SAFETY`.
- Replaced abbreviated action captions with `PULL MSG`, `POST`, `SEARCH`,
  `ACK`, `CATALOG`, `QUEUE`, and `OTAP INTENT` while preserving the existing
  request handlers and resource IDs.
- Kept Relay, Flash, Serial, and PCAP footer controls disabled and added Safety
  and Diagnostics text that names the external gate ownership.
- Updated `/mnt/h/dos-c/software/win31-operator/README.md` for the 640x360
  layout and external-gate ownership wording.
- Re-ran copied-evidence DOS-C and ESP32 advisory analysis into `/tmp`.

Excluded:

- No DOSBox-X, Pi desktop, serial port, ESP32 firmware, bridge wire protocol,
  JSON schema, request/response type, PCAP transport, BLE, mesh, router-admin,
  relay/XBee, TFT, MicroSD, load, mains, flash, erase, monitor, or live
  hardware action was changed or driven.

## Verified Facts

- DOS-C working tree was clean before this UI change.
- ESP32 working tree already contained unrelated remote-LCD documentation
  changes; this task did not revert or stage them.
- The latest copied structured Gate H packet at
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-25-gate-h-structured-live/gate-h-structured-live-20260525T155900Z/`
  contains `bridge-transcript.jsonl`, `cleanup.txt`, `vision-gate.json`, and 14
  PNG screenshots.
- A fresh DOS-C vision-gate rerun against that copied packet returned
  `status: pass`, `ok: true`, `failures: []`, 14 screenshots, and 1763 OCR
  words.
- A fresh ESP32 advisory legibility rerun against that copied packet reported
  14 screens, `visionGateStatus: pass`, mapped target views `7/10`, lowest OCR
  confidence `51.42`, median OCR confidence `54.99`, no
  `console_fit_risk`, no `log_region_overflow`, lowest layout bottom margin
  `120 px`, lowest layout right margin `384 px`, 14
  `navigation_label_gap` findings, and 13 `weak_ocr_confidence` findings.
- The mapped-view count is `7/10` because that copied packet does not include
  Settings, Wizard, or Devices screenshots.
- DOS-C host tests and the Open Watcom Win16 build passed after the UI source
  change.

## Assumptions

- The default visual style remains Win3.1-native, dense, and operational.
- OCR/CV remains advisory and secondary to bridge transcript behavior.
- A later live or copied screenshot packet is required to measure the revised
  UI pixels.

## Unknowns

- No fresh screenshot packet exists yet for the revised two-row navigation UI.
- The revised UI has not yet proven mean OCR confidence >= 60, eliminated
  navigation-label gaps, or mapped all 10 target views in copied evidence.
- Human operator usability has not been measured.

## Sources

- `SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23`
- `SRC-LOCAL-WIN31-DASHBOARD-LEGIBILITY-RESEARCH-2026-05-24`
- `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25`
- `SRC-LOCAL-WIN31-DASHBOARD-VISUAL-DESIGN-2026-05-26`

## Validation

- PASS: From `/mnt/h/dos-c`, `bash tests/win31_operator/run_host_tests.sh`.
- PASS: From `/mnt/h/dos-c`, `software/win31-operator/build-watcom.sh`.
- PASS: From `/mnt/h/dos-c`, `python3 tests/test_win31_dashboard_vision_gate.py`.
- PASS: From `/mnt/h/dos-c`, copied-evidence
  `python3 scripts/win31_dashboard_vision_gate.py --screenshot-dir ... --bridge-transcript .../bridge-transcript.jsonl --cleanup-proof .../cleanup.txt --out /tmp/win31-gate-h-structured-vision-after-ui-source.json`.
- PASS: From `/mnt/h/ESP32`,
  `python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py`.
- PASS: From `/mnt/h/ESP32`, copied-evidence
  `python3 scripts/win31_dashboard_legibility_analyzer.py --evidence-root ... --screenshot-dir ... --vision-gate .../vision-gate.json --out-json /tmp/win31-gate-h-structured-legibility-after-ui-source.json --out-report /tmp/win31-gate-h-structured-legibility-after-ui-source.md`.
- PASS: From `/mnt/h/ESP32`, `python3 scripts/verify_scaffold.py`.
- PASS: From `/mnt/h/ESP32`, `git diff --check`.
- PASS: From `/mnt/h/dos-c`, `bash scripts/verify_scaffold.sh`.
- PASS: From `/mnt/h/dos-c`, `git diff --check`.

## Handoff

Continue with
[../handoffs/0051-win31-dashboard-visual-design-continuation-to-qa.md](../handoffs/0051-win31-dashboard-visual-design-continuation-to-qa.md).

## Stop Gates

Do not claim visual-design acceptance until a fresh copied screenshot packet of
the revised UI passes the DOS-C vision gate, maps all required target views in
the advisory analyzer, and demonstrates no layout-fit regression. Keep Relay,
Flash, Serial Write, PCAP, BLE, mesh, router-admin, ESP32 flash/erase/monitor,
relay/XBee, TFT, MicroSD, load, mains, and live serial-write expansion closed
unless a later accepted live gate explicitly opens them.
