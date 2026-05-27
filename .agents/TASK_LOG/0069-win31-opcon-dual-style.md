# Task Log 0069 - Win31 OPCON Dual Visual Style

- ID: 0069-win31-opcon-dual-style
- Date: 2026-05-27
- Contract: `AGENTS.md`
- Status: implemented; live visual packet captured

## Goal

Record the ESP32-side coordination state for the DOS-C Windows 3.1 OPCON dual
visual style implementation while preserving the accepted serial-nullmodem
path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Verified Facts

- DOS-C `operator.c`, `operator.rc`, and `resource.h` now implement a
  Windows 3.1 default style plus selectable ANSI Terminal style.
- Style menu IDs are `118` and `119`; selector controls are `247`, `248`, and
  `249`.
- Style switching is session-only and refreshes fonts, brushes, menu checks,
  selector state, and the current view.
- DOS-C source guard tests verify that style symbols remain scoped out of
  `software/win31-netstack` and `software/espnow-bbs-bridge`.
- Rebuilt ignored DOS-C `OPCON.EXE` SHA-256:
  `ac5d898cf4275548b80e61caddfa3681358f99c90506cdbd600930a14c557620`.
- Rebuilt ignored DOS-C `OPCONPC.EXE` SHA-256:
  `f6c8ae9f227914db53a2c3f91bd861cdbfae5cd9506aebac437e324bffcf5d85`.
- Live visual packet copied from the Pi:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-27-win31-opcon-dual-style/live-dual-style-20260527T040008Z/`.
- The packet contains 14 screenshots at `1024x600`: 11 Windows 3.1 default
  views plus ANSI Terminal Settings, Home, and Safety.
- The bridge ran on the accepted physical serial read-only path with
  `/dev/ttyUSB0`, `--allow-physical-serial`, and `--read-only`.
- Cleanup proof reports no DOSBox-X process, no quit-warning modal, no bridge
  process, and no listeners on `31331`, `31332`, or `8080`.
- `scripts/win31_dashboard_legibility_analyzer.py` now avoids treating an
  interior Windows 3.1 gray footer gap as desktop bleed-through; tests cover
  that fixture.
- No ESP32 firmware, live-gate script, bridge protocol, transport client, PCAP,
  relay/XBee, BLE, mesh, serial-write, or router/admin code was changed in
  this pass.

## Sources

- [../../knowledge-base/source-index.md](../../knowledge-base/source-index.md)
- [../../knowledge-base/source-ledger/2026-05-27-win31-opcon-dual-style.md](../../knowledge-base/source-ledger/2026-05-27-win31-opcon-dual-style.md)
- DOS-C record:
  `/mnt/h/dos-c/knowledge-base/win31-opcon-dual-style-2026-05-27.md`

## Assumptions

- Session-only style switching is the safest v1 path.
- Future live visual proof should use copied evidence and keep transcript proof
  authoritative.

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

## Handoff

Continue with
[../handoffs/0058-win31-opcon-dual-style-to-qa.md](../handoffs/0058-win31-opcon-dual-style-to-qa.md).

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP, packet
driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT, MicroSD, load,
mains, erase, monitor, serial-write expansion, Gate G export, and forced
tracking of ignored runtime artifacts remain closed.
