# Win31 OPCON Dual Visual Style Source Ledger

Date: 2026-05-27

Source index ID: `SRC-LOCAL-WIN31-OPCON-DUAL-STYLE-2026-05-27`

## Sources

- DOS-C operator source:
  `/mnt/h/dos-c/software/win31-operator/src/operator.c`.
- DOS-C resource files:
  `/mnt/h/dos-c/software/win31-operator/src/operator.rc` and
  `/mnt/h/dos-c/software/win31-operator/include/resource.h`.
- DOS-C operator README:
  `/mnt/h/dos-c/software/win31-operator/README.md`.
- DOS-C source guard:
  `/mnt/h/dos-c/tests/win31_operator/test_visual_style_sources.sh`.
- DOS-C knowledge record:
  `/mnt/h/dos-c/knowledge-base/win31-opcon-dual-style-2026-05-27.md`.
- DOS-C source index entries for the UI research basis:
  `/mnt/h/dos-c/knowledge-base/source-index.md`.
- DOS-C task and handoff records:
  `/mnt/h/dos-c/.agents/tasks/0037-win31-opcon-dual-style.md` and
  `/mnt/h/dos-c/.agents/handoffs/0034-win31-opcon-dual-style-to-qa.md`.
- ESP32 task and handoff records:
  `.agents/TASK_LOG/0069-win31-opcon-dual-style.md` and
  `.agents/handoffs/0058-win31-opcon-dual-style-to-qa.md`.
- ESP32 advisory analyzer source and fixture test:
  `scripts/win31_dashboard_legibility_analyzer.py` and
  `tests/live_bench/test_win31_dashboard_legibility_analyzer.py`.

## Verified Facts

- The accepted path remains:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- DOS-C source changed only the Win31 OPCON UI/resource/test/documentation
  surface for dual visual style support.
- `OPCON_STYLE_WIN31` is the default; `OPCON_STYLE_ANSI` remains selectable.
- Windows 3.1 style uses system colors and stock Win16 fonts. ANSI Terminal
  keeps the prior black/cyan/amber owner-drawn shell.
- Style menu IDs are `118` and `119`; selector control IDs are `247`, `248`,
  and `249`.
- Settings and Wizard expose the selector; other views hide it while preserving
  header geometry.
- `GetTextMetrics` now supplies the active mono-font average character width
  for list truncation and detail wrapping.
- Rebuilt ignored `OPCON.EXE` SHA-256:
  `ac5d898cf4275548b80e61caddfa3681358f99c90506cdbd600930a14c557620`.
- Rebuilt ignored `OPCONPC.EXE` SHA-256:
  `f6c8ae9f227914db53a2c3f91bd861cdbfae5cd9506aebac437e324bffcf5d85`.
- Live copied packet:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-27-win31-opcon-dual-style/live-dual-style-20260527T040008Z/`.
- The packet contains 14 screenshots at `1024x600`: 11 Windows 3.1 default
  views plus ANSI Terminal Settings, Home, and Safety.
- The bridge ran on the accepted physical serial read-only path with
  `/dev/ttyUSB0`, `--allow-physical-serial`, and `--read-only`.
- Cleanup proof reports no DOSBox-X process, no quit-warning modal, no bridge
  process, and no listeners on `31331`, `31332`, or `8080`.
- The ESP32 advisory analyzer now avoids treating an interior Windows 3.1 gray
  footer gap as desktop bleed-through.

## Assumptions

- Session-only style switching is the safest v1 path because local INI
  persistence is already a later slice.
- A live visual packet should use copied screenshots and transcript/cleanup
  proof rather than weakening the transcript-first gate.

## Unknowns

- Human physical-panel confirmation remains pending.

## Validation

- PASS: `/mnt/h/dos-c` `bash tests/win31_operator/run_host_tests.sh`
- PASS: `/mnt/h/dos-c` `bash software/win31-operator/build-watcom.sh`
- PASS: `/mnt/h/dos-c` `python3 tests/test_win31_dashboard_vision_gate.py`
- PASS: `python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py`
- PASS: ESP32 visual-only analyzer on the copied live packet reported
  `visual_only_pass`, mapped target views `10/10`, lowest layout margins
  bottom `29 px` and right `15 px`, no `console_fit_risk`, no
  `log_region_overflow`, and no `proof_capture_size_mismatch`.

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP, packet
driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT, MicroSD, load,
mains, erase, monitor, serial-write expansion, Gate G export, and forced
tracking of ignored runtime artifacts remain closed.
