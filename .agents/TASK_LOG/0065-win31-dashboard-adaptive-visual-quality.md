# Task Log 0065 - Win31 Dashboard Adaptive Visual Quality

## Task

- ID: 0065-win31-dashboard-adaptive-visual-quality
- Owner role: QA, Communications
- Status: implemented; fresh visual proof required
- Created: 2026-05-26
- Updated: 2026-05-26
- Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Implement the adaptive visual-quality plan for the Win31 OPCON dashboard:
weighted review process, source-backed records, analyzer coordinate-stack
output, and DOS-C adaptive layout source changes.

Accepted path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Verified Facts

- The current Gate H packet remains a functional pass: DOS-C vision gate
  `status: pass`, paired ESP32 completion `status: pass`, and cleanup clean.
- Current Gate H screenshots in the copied packet are `1920x1080`; the intended
  proof target is `1024x600`.
- The ESP32 analyzer now records `captureSizes`, `coordinateStack`,
  `normalizedSafeMarginsPx`, `proof_capture_size_mismatch`, and
  `advisoryVisualFitStatus`.
- Analyzer rerun on the current Gate H packet reports visual-fit `fail` because
  the old evidence still has `console_fit_risk`, `log_region_overflow`, and
  `proof_capture_size_mismatch` on all 18 screenshots.
- DOS-C Win31 operator source now computes startup client size from screen and
  window metrics and reflows controls on `WM_SIZE`.
- No bridge protocol, ESP32 firmware behavior, flash path, serial transport,
  PCAP path, or unsafe hardware-control authority was intentionally changed.

## Weighted Review Vote

| Role | Weight | Vote | Conditions |
| --- | ---: | --- | --- |
| Win31 UI/protocol analyst | 3 | Approve | Preserve protocol invariants and build with Open Watcom. |
| Win31 vision-gate analyst | 3 | Approve with proof condition | Report capture-size mismatch and keep visual fit advisory until fresh proof. |
| Evidence record auditor | 3 | Approve with record condition | Add source index, ledger, task, handoff, and paired DOS-C records. |
| Coordinator | 5 | Approve | Keep live mutation closed and require later copied proof. |

Weighted result: `14/14`, pass above the `70%` threshold.

## Sources

- `SRC-LOCAL-WIN31-DASHBOARD-ADAPTIVE-VISUAL-QUALITY-2026-05-26`
- `SRC-LOCAL-WIN31-DASHBOARD-1024X600-GATE-H-LIVE-PROOF-2026-05-26`
- `SRC-SUNFOUNDER-7INCH-HDMI-1024X600-2026-05-26`
- `SRC-RASPBERRY-PI-CONFIGURATION`
- `SRC-DOSBOX-X-REFERENCE-CONFIG-2026-05-26`
- `SRC-MICROSOFT-WIN32-GEOMETRY-2026-05-26`

## Assumptions

- The user-stated SunFounder display class is relevant to the 1024x600 target,
  but this task does not independently prove the exact installed LCD model.
- A fresh copied proof packet is required before claiming adaptive visual-fit
  acceptance.

## Unknowns

- Whether the `1920x1080` captured packet reflects current Pi display mode,
  DOSBox-X fullscreen scaling, capture tool behavior, or stale proof context.
- Human usability and touchscreen ergonomics.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile scripts/win31_dashboard_legibility_analyzer.py tests/live_bench/test_win31_dashboard_legibility_analyzer.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py`.
- PASS: DOS-C `bash tests/win31_operator/run_host_tests.sh`.
- PASS: DOS-C `software/win31-operator/build-watcom.sh`.
- PASS: DOS-C `PYTHONDONTWRITEBYTECODE=1 python3 tests/test_win31_dashboard_vision_gate.py`.
- PASS: DOS-C copied-evidence `scripts/win31_dashboard_vision_gate.py ...` against the current Gate H packet.
- PASS: ESP32 analyzer rerun against the current Gate H packet.
- PASS: ESP32 `scripts/espnow_bbs_live_gate.py complete ... --out /tmp/win31-dashboard-adaptive-esp32-completion.json`.

## Handoff

Continue with
[../handoffs/0054-win31-dashboard-adaptive-visual-quality-to-qa.md](../handoffs/0054-win31-dashboard-adaptive-visual-quality-to-qa.md).

## Stop Gates

Do not reopen flash, erase, monitor, serial-write expansion, PCAP,
packet-driver, router/admin mutation, BLE, mesh, relay/XBee, TFT, MicroSD,
load, mains, Gate G export, or forced tracking of ignored runtime artifacts
from this task.
