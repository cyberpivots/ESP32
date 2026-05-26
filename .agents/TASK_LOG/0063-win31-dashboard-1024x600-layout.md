# Task Log 0063 - Win31 Dashboard 1024x600 Layout

## Task

- ID: 0063-win31-dashboard-1024x600-layout
- Owner role: QA, Communications
- Status: implemented; source-validated; fresh screenshot capture still pending
- Created: 2026-05-26
- Updated: 2026-05-26
- Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Refactor the Windows 3.1 OPCON dashboard for the actual 1024x600 proof screen
without changing the bridge protocol, ESP32 firmware behavior, serial-nullmodem
transport, PCAP transport, live hardware gates, or completion semantics.

## Scope

Included:

- Updated `/mnt/h/dos-c/software/win31-operator/src/operator.c`.
- Changed the Win31 operator client target from `640x360` to `1000x500`.
- Reflowed the top status strip, two-row navigation strip, carousel controls,
  list/detail panes, action strip, disabled footer, and log area for the 1024 px
  proof-screen width.
- Preserved stable navigation labels:
  `HOME`, `BBS BOARD`, `DOWNLOADS`, `NETWORK`, `PEERS`, `DEVICES`, `OTAP`,
  `SETTINGS`, `WIZARD`, `DIAGNOSTICS`, and `SAFETY`.
- Preserved existing action labels and request handlers:
  `PULL MSG`, `POST`, `SEARCH`, `ACK`, `CATALOG`, `QUEUE`, and `OTAP INTENT`.
- Kept Relay, Flash, Serial, and PCAP footer controls disabled and retained
  external live-gate ownership wording.
- Updated `/mnt/h/dos-c/software/win31-operator/README.md`.
- Added DOS-C task record
  `/mnt/h/dos-c/.agents/tasks/0032-win31-dashboard-1024x600-layout.md`.

Excluded:

- No DOSBox-X, Pi desktop, serial port, ESP32 firmware, bridge wire protocol,
  JSON schema, request/response type, PCAP transport, BLE, mesh, router-admin,
  relay/XBee, TFT, MicroSD, load, mains, flash, erase, monitor, or live
  hardware action was changed or driven.

## Verified Facts

- DOS-C working tree was clean before this 1024x600 layout change.
- ESP32 working tree already contained unrelated remote-LCD documentation
  changes and prior Win31 task records; this task did not revert or stage them.
- `OPCON_CLIENT_WIDTH` is now `1000`.
- `OPCON_CLIENT_HEIGHT` is now `500`.
- Existing Win31 resource IDs and request handlers were preserved.
- No bridge request type, JSON field, transport API, PCAP profile, ESP32
  firmware interface, or live-gate contract was changed.
- DOS-C host tests and the Open Watcom Win16 build passed after the 1024x600
  layout source change.
- A fresh DOS-C vision-gate rerun against the latest copied structured Gate H
  packet returned `status: pass`, `ok: true`, `failures: []`, 14 screenshots,
  and 1763 OCR words.
- A fresh ESP32 advisory legibility rerun against that same copied packet
  reported 14 screens, `visionGateStatus: pass`, mapped target views `7/10`,
  lowest OCR confidence `51.42`, median OCR confidence `54.99`, no
  `console_fit_risk`, no `log_region_overflow`, lowest layout bottom margin
  `120 px`, and lowest layout right margin `384 px`.
- The mapped-view count remains `7/10` because that copied packet predates the
  1000x500 layout and does not include Settings, Wizard, or Devices screenshots.

## Assumptions

- A 1000x500 client is the safer 1024x600 target because Win3.1 frame and menu
  chrome are added around the client rectangle.
- The default visual style remains Win3.1-native, dense, and operational.
- OCR/CV remains advisory and secondary to bridge transcript behavior.
- A later live or copied screenshot packet is required to measure the revised
  UI pixels.

## Unknowns

- No fresh screenshot packet exists yet for the 1000x500 layout.
- The revised UI has not yet proven mean OCR confidence >= 60, eliminated
  navigation-label gaps, or mapped all 10 target views in copied evidence.
- Human operator usability has not been measured.

## Sources

- `SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23`
- `SRC-LOCAL-WIN31-DASHBOARD-LEGIBILITY-RESEARCH-2026-05-24`
- `SRC-LOCAL-WIN31-DASHBOARD-VISUAL-DESIGN-2026-05-26`
- `SRC-LOCAL-WIN31-DASHBOARD-1024X600-2026-05-26`

## Validation

- PASS: From `/mnt/h/dos-c`, `bash tests/win31_operator/run_host_tests.sh`.
- PASS: From `/mnt/h/dos-c`, `software/win31-operator/build-watcom.sh`.
- PASS: From `/mnt/h/dos-c`, `python3 tests/test_win31_dashboard_vision_gate.py`.
- PASS: From `/mnt/h/dos-c`, copied-evidence
  `python3 scripts/win31_dashboard_vision_gate.py --screenshot-dir ... --bridge-transcript .../bridge-transcript.jsonl --cleanup-proof .../cleanup.txt --out /tmp/win31-gate-h-structured-vision-after-1024-layout.json`.
- PASS: From `/mnt/h/ESP32`,
  `python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py`.
- PASS: From `/mnt/h/ESP32`, copied-evidence
  `python3 scripts/win31_dashboard_legibility_analyzer.py --evidence-root ... --screenshot-dir ... --vision-gate .../vision-gate.json --out-json /tmp/win31-gate-h-structured-legibility-after-1024-layout.json --out-report /tmp/win31-gate-h-structured-legibility-after-1024-layout.md`.
- PASS: From `/mnt/h/ESP32`, `python3 scripts/verify_scaffold.py`.
- PASS: From `/mnt/h/dos-c`, `bash scripts/verify_scaffold.sh`.
- PASS: From `/mnt/h/dos-c`, `git diff --check`.
- PASS: From `/mnt/h/ESP32`, `git diff --check`.

## Handoff

Continue with
[../handoffs/0052-win31-dashboard-1024x600-layout-to-qa.md](../handoffs/0052-win31-dashboard-1024x600-layout-to-qa.md).

## Stop Gates

Do not claim visual-design acceptance until a fresh copied screenshot packet of
the revised UI passes the DOS-C vision gate, maps all required target views in
the advisory analyzer, and demonstrates no layout-fit regression. Keep Relay,
Flash, Serial Write, PCAP, BLE, mesh, router-admin, ESP32 flash/erase/monitor,
relay/XBee, TFT, MicroSD, load, mains, and live serial-write expansion closed
unless a later accepted live gate explicitly opens them.
