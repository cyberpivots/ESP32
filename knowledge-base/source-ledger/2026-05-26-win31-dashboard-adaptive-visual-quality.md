# Win31 Dashboard Adaptive Visual Quality Source Ledger

Date: 2026-05-26

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-WIN31-DASHBOARD-ADAPTIVE-VISUAL-QUALITY-2026-05-26`
- `SRC-LOCAL-WIN31-DASHBOARD-1024X600-2026-05-26`
- `SRC-LOCAL-WIN31-DASHBOARD-1024X600-GATE-H-LIVE-PROOF-2026-05-26`
- `SRC-SUNFOUNDER-7INCH-HDMI-1024X600-2026-05-26`
- `SRC-RASPBERRY-PI-CONFIGURATION`
- `SRC-DOSBOX-X-REFERENCE-CONFIG-2026-05-26`
- `SRC-MICROSOFT-WIN32-GEOMETRY-2026-05-26`

## Scope

Adaptive visual-quality follow-up for the Win31 OPCON dashboard, preserving the
accepted serial-nullmodem path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Evidence

- DOS-C source changes:
  `/mnt/h/dos-c/software/win31-operator/src/operator.c` and
  `/mnt/h/dos-c/software/win31-operator/README.md`.
- ESP32 analyzer changes:
  `scripts/win31_dashboard_legibility_analyzer.py` and
  `tests/live_bench/test_win31_dashboard_legibility_analyzer.py`.
- Process document:
  `docs/projects/espnow-bbs/win31-dashboard-adaptive-visual-quality.md`.
- Current copied Gate H proof packet:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-1024x600-gate-h/gate-h-1024x600-20260526T211658Z/`.
- Temporary validation outputs:
  `/tmp/win31-dashboard-adaptive-legibility.json`,
  `/tmp/win31-dashboard-adaptive-legibility.md`, and
  `/tmp/win31-dashboard-adaptive-vision-gate.json`.

## Verified Facts

- The current copied Gate H proof packet still reports DOS-C vision gate
  `status: pass` and paired ESP32 completion `status: pass`.
- The current copied Gate H screenshots are `1920x1080`, not the intended
  `1024x600` proof target.
- The analyzer now reports `captureSizes`, `coordinateStack`,
  `normalizedSafeMarginsPx`, `proof_capture_size_mismatch`, and
  `advisoryVisualFitStatus`.
- The current copied packet remains advisory visual-fit `fail` because it still
  has `console_fit_risk` and `log_region_overflow` on 18 screens plus
  `proof_capture_size_mismatch` on 18 screens.
- The Win31 operator now computes startup client size with screen/window
  metrics, reuses one computed layout for shell drawing, and moves child
  controls on resize.
- The Win31 operator protocol, request set, queue behavior, disabled controls,
  COM1/nullmodem default, PCAP alternate build boundary, and firmware/live-gate
  contracts were not intentionally changed.

## Weighted Review Vote

| Role | Weight | Vote | Evidence reviewed |
| --- | ---: | --- | --- |
| Win31 UI/protocol analyst | 3 | Approve | DOS-C operator source, README, host tests, protocol invariants. |
| Win31 vision-gate analyst | 3 | Approve with proof condition | Analyzer, tests, Gate H packet, visual-fit comparison packet. |
| Evidence record auditor | 3 | Approve with record condition | ESP32 and DOS-C source indexes, task logs, handoffs, proof records. |
| Coordinator | 5 | Approve | Full implementation scope, validation, and stop gates. |

Weighted result: `14/14`, above the `70%` threshold. Conditions: keep live
hardware mutation closed and require a fresh copied proof packet before claiming
adaptive visual-fit acceptance.

## Assumptions

- The user-stated SunFounder display class is relevant to the 1024x600 target,
  but this ledger does not independently prove the exact installed LCD model.
- A fresh live capture will be needed to verify whether the adaptive source
  change resolves the `1920x1080` capture mismatch and fit risks.

## Unknowns

- Whether the capture mismatch comes from Pi display mode, DOSBox-X fullscreen
  behavior, remote capture geometry, or a stale proof packet.
- Human usability and touch ergonomics of the adaptive layout.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile scripts/win31_dashboard_legibility_analyzer.py tests/live_bench/test_win31_dashboard_legibility_analyzer.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py`.
- PASS: DOS-C `bash tests/win31_operator/run_host_tests.sh`.
- PASS: DOS-C `software/win31-operator/build-watcom.sh`.
- PASS: DOS-C `PYTHONDONTWRITEBYTECODE=1 python3 tests/test_win31_dashboard_vision_gate.py`.
- PASS: DOS-C copied-evidence `scripts/win31_dashboard_vision_gate.py ...` against the current Gate H packet.
- PASS: ESP32 analyzer rerun against the current Gate H packet generated advisory output and separated gate pass from visual-fit fail.
- PASS: ESP32 `scripts/espnow_bbs_live_gate.py complete ... --out /tmp/win31-dashboard-adaptive-esp32-completion.json`.

## Stop Gates

Do not reopen flash, erase, monitor, serial-write expansion, PCAP,
packet-driver, router/admin mutation, BLE, mesh, relay/XBee, TFT, MicroSD,
load, mains, Gate G export, or forced tracking of ignored runtime artifacts
from this visual-quality task.
