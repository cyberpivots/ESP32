# Structured Gate H Transcript Ledger - 2026-05-25

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-TRANSCRIPT-2026-05-25`

## Scope

Tooling and procedure update for future Gate H proof packets on the accepted
serial-nullmodem path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

This task did not run live hardware or mutate firmware.

## Verified Facts

- DOS-C `software/espnow-bbs-bridge/espnow_bbs_bridge.py` can append
  structured JSONL audit records with full request and response payloads.
- DOS-C `scripts/win31_dashboard_vision_gate.py` and ESP32
  `scripts/espnow_bbs_live_gate.py complete` already parse JSONL transcript
  input via their existing JSON-or-text loaders; fixture coverage now proves
  the structured transcript shape passes when required evidence is present.
- `bridge.log` remains unchanged for human-readable request summaries.
- `bridge-transcript.jsonl` is intended for ignored proof/runtime directories
  and must not be tracked as live evidence.
- Future Gate H live procedure should collect one OPCON telemetry refresh cycle
  before BBS/download/OTAP actions and one refresh cycle after them.

## Assumptions

- The accepted 2026-05-25 Gate H proof remains accepted; this ledger updates
  future capture shape only.

## Unknowns

- No new live Gate H proof packet has been collected with the structured JSONL
  transcript.
- Analytics retention/export/privacy policy remains unresolved.

## Validation

- ESP32:
- `python3 tests/live_bench/test_espnow_bbs_live_gate.py`
- `python3 scripts/verify_scaffold.py`
- `git diff --check`
- Dry ignored evidence rehearsal:
  - DOS-C `vision-gate.json` reported `status: pass` under
    `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-25-structured-gate-h-dry-run/gate-h-structured-dry-run-20260525T154317Z/`.
  - ESP32 completion output reported `status: pass` under
    `research/bench-records/live-bench/gate-h-structured-dry-run-20260525T154317Z/`.
- DOS-C:
  - `python3 tests/espnow_bbs_bridge/test_bridge_protocol.py`
  - `python3 tests/test_win31_dashboard_vision_gate.py`
  - `bash tests/espnow_bbs_bridge/run_tests.sh`
  - `bash tests/win31_operator/run_host_tests.sh`
  - `bash tests/win31_netstack/run_host_tests.sh`
  - `bash scripts/verify_scaffold.sh`
  - `git diff --check`

## Result

Future Win31 screenshot/OCR and ESP32 completion gates can use
`bridge-transcript.jsonl` as transcript/spool evidence without weakening
existing pass/fail checks.
