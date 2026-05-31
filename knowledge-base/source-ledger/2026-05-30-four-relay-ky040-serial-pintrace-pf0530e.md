# Source Ledger - 2026-05-30 Four Relay KY-040 Serial Pintrace PF0530E

## Verified facts

- `PF0530D` was the prior focused LCD diagnostic for KY-040 `CLK` on GPIO13,
  `DT` on GPIO14, and `SW` on GPIO32. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-DEVKITC-13-14-32-DIAGNOSTIC-2026-05-30`.
- ESP-IDF GPIO documentation covers input reads, GPIO34-GPIO39 software-pull
  limitations, strapping-pin review, and GPIO configuration behavior. Source
  ID: `SRC-ESP-IDF-GPIO`.
- Espressif DevKitC source coverage is the pin-layout source for the DevKitC
  header-position warning used by PF0530E. Source ID: `SRC-ESP32-DEVKITC`.
- KY-040 module-family behavior is recorded from Manuals+ and Envistia sources:
  `CLK`, `DT`, `SW`, `+`, and `GND` pins, 3.3 V compatibility for the module
  class, quadrature A/B, and active-low pushbutton behavior. Source IDs:
  `SRC-MANUALSPLUS-CYLEWET-KY040-B06XQTHDRR`,
  `SRC-ENVISTIA-KY040-GUIDE-2026-05-30`.

## Local changes

- Firmware ID changed to `PF0530E`.
- `main/main.c` adds `FR_DIAG_SERIAL_PINTRACE 1` and an input-only serial
  contact tracer for GPIO0/GPIO2/GPIO4/GPIO5/GPIO12/GPIO13/GPIO14/GPIO15/
  GPIO16/GPIO17/GPIO18/GPIO19/GPIO21/GPIO22/GPIO23/GPIO25/GPIO26/GPIO27/
  GPIO32/GPIO33/GPIO34/GPIO35/GPIO36/GPIO39.
- Internal pullups are enabled only on GPIO13/GPIO14/GPIO32; all other watched
  pins have internal pulls disabled.
- COM6/UART0 output prints a firmware ID, DevKitC header-position warning,
  initial `PIN` levels, stable `EV` events, and periodic `HB`/`ST` summaries.
- The serial pintrace loop runs in a dedicated FreeRTOS task with a tick-safe
  10 ms poll delay. This supersedes the initial shorter-poll r2 build, whose
  live monitor showed task-watchdog backtraces.
- `tools/pf0530e_serial_pintrace_monitor.py` is a pyserial read-only transcript
  helper for the live monitor gate.

## Live results

- COM6 r4 write-flash and separate verify-flash passed for bootloader,
  partition table, and app.
- The final r4 serial transcript ran from `2026-05-30T18:53:41.080+00:00` to
  `2026-05-30T19:03:41.111+00:00` with `writes_sent=false`.
- The r4 transcript contains no watchdog, backtrace, panic, or guru-meditation
  lines.
- The r4 transcript contains stable `EV` events only for boot-settling
  GPIO0/GPIO5/GPIO15. It contains no `EV` event for GPIO13, GPIO14, GPIO32,
  GPIO12, or the other watched pins.
- The final r4 heartbeat kept GPIO13 `CLK` level 1 count 0, GPIO14 `DT`
  level 1 count 0, and GPIO32 `SW` level 1 count 0.
- The user did not confirm in chat that the encoder was physically actuated
  during the r4 monitor window, so this record does not claim hardware
  acceptance or a proven actuated-failure condition.
- The later r5 read-only monitor restarted on the already-flashed PF0530E r4
  image and captured user-confirmed actuation with `writes_sent=false`.
- R5 recorded GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` count increases during
  the user action window, and its scan recorded no watchdog, panic, backtrace,
  or guru-meditation hits.
- R5 proves GPIO-level input changes on the accepted GPIO13/GPIO14/GPIO32
  wiring. It does not prove LCD menu navigation, final hardware acceptance, or
  relay/XBee behavior.

## Assumptions

- The user's same-thread safe-state and COM6 flash/monitor request apply to the
  named PF0530E gate.
- KY-040 `+` remains on ESP32 3V3 and not 5 V.
- Relay/load/mains remain disconnected.

## Unknowns

- Exact wire landing and continuity from KY-040 `CLK`/`DT`/`SW`.
- Exact module pullup values and voltage on the bench unit.
- Whether a later PF0530F menu image accepts those GPIO13/GPIO14 transitions as
  bidirectional menu steps and suppresses button-window A/B noise.

## Closed surfaces

- No relay GPIO writes.
- No relay-expander writes.
- No XBee setting writes, XBee/RF, range, throughput, or API transmit frames.
- No MicroSD or TFT action.
- No relay/load/mains action.
- No erase.
- No wiring mutation by the agent.
- No hardware acceptance, final pin reassignment, commit, or push.
