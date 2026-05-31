# Source Ledger - 2026-05-30 Four Relay KY-040 Encoder Menu PF0530F

## Verified facts

- PF0530E r5 is the prior live evidence for GPIO-level KY-040 input changes on
  GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW`. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30`.
- ESP-IDF GPIO documentation covers GPIO input configuration, pullup/pulldown
  configuration, and `gpio_get_level()`. Source ID: `SRC-ESP-IDF-GPIO`.
- KY-040 module-family behavior is recorded from the Manuals+ and Envistia
  sources for `CLK`, `DT`, `SW`, `+`, `GND`, quadrature A/B, 3.3 V module-class
  compatibility, onboard pullups, and active-low switch behavior. Source IDs:
  `SRC-MANUALSPLUS-CYLEWET-KY040-B06XQTHDRR`,
  `SRC-ENVISTIA-KY040-GUIDE-2026-05-30`.

## Local changes

- Firmware ID changed to `PF0530F`.
- The current diagnostic boot path now starts the LCD encoder menu proof instead
  of the PF0530E serial pintrace task.
- `FR_DIAG_XBEE_BRIDGE_CLOSED 1` remains set, so the UART0-to-UART2 bridge loop
  is not run by this diagnostic image.
- GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` are configured input-only with
  internal pullups enabled and pulldowns disabled.
- A/B sampling uses a 2 ms poll and three stable samples before a level is
  accepted.
- The quadrature decoder keeps the 16-state table and four transitions per menu
  step, counts invalid jumps, and resets the accumulator on invalid transitions.
- Switch handling uses 30 ms debounce and opens a 150 ms guard window on
  press/release. A/B changes during the guard are counted and printed as
  suppressed, and they do not move the menu.
- The LCD menu rotates through `ENCODER`, `RELAY LOCK`, `COMMS LOCK`, `SAFETY`,
  and `COUNTERS` text-only views. Line 0 always shows `PF0530F`, page, and
  signed position.
- UART0 proof output uses `printf` lines for `MENU_READY`, `ENC_EV`,
  `MENU_STEP`, `MENU_SELECT`, `AB_SUPPRESS`, `AB_INVALID`, and `MENU_HB`.

## Assumptions

- KY-040 `+` remains on ESP32 3V3 and not 5 V.
- GPIO13/GPIO14/GPIO32 remain the intended menu-proof wiring from PF0530E r5.
- Relay/load/mains, XBee/RF, MicroSD, TFT, erase, flash, monitor, and serial
  write expansion remain closed.

## Unknowns

- During the later PF0530F Tier 3 live attempt, PF0530F flashed and
  verify-flash matched on COM6, but live menu acceptance was blocked by
  `PF0530F LCD_INIT_FAILED`. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-LIVE-2026-05-30`.
- Whether PF0530F produces accepted `MENU_STEP` events in both directions and
  `MENU_SELECT` events for the physical button remains unknown after LCD init
  is restored.
- Exact bench pullup values, rail margin, rotation direction, boot behavior, and
  final wiring acceptance remain unresolved.

## Closed surfaces

- No relay GPIO writes.
- No relay-expander writes.
- No XBee setting writes, XBee/RF, range, throughput, or API transmit frames.
- No MicroSD or TFT action.
- No relay/load/mains action.
- No further flash, monitor, erase, or serial write beyond the later named
  PF0530F COM6 live attempt.
- No hardware acceptance, final pin reassignment, commit, or push.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `git diff --check`.
- PASS: ESP-IDF v6.0.1 no-flash build with
  `idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-four-relay-xbee-wifi-pf0530f-menu-build build`.
- The first ESP-IDF no-flash build caught a `-Werror=format-truncation` issue in
  the LCD `ENCODER` level line. The source was narrowed to fixed-width `0`/`1`
  level characters and the validation set above was rerun successfully.
- Required repo validation is also recorded in task
  `.agents/TASK_LOG/0107-four-relay-ky040-encoder-menu-pf0530f.md`.

## Decision footer

- Decision: PF0530F repo-only firmware/docs/tests implementation complete.
  A later live attempt is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-LIVE-2026-05-30`: COM6
  write/verify passed, but live menu acceptance is blocked by `PF0530F
  LCD_INIT_FAILED`.
- Next gate: diagnose `PF0530F LCD_INIT_FAILED` before another live menu proof;
  any further flash or monitor action needs fresh authority, rollback/recovery
  review as applicable, and closed-surface review.
- Owner: Firmware with QA, Hardware, Agent Operations, and Live Bench lenses.
- Authority limits: no flash, monitor, serial write, XBee/RF, relay/load/mains,
  erase, wiring mutation, commit, or push.
