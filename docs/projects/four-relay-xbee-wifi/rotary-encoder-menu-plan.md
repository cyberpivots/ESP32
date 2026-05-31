# Rotary Encoder Menu Plan

## Status

Documentation-only plan for adding a rotary encoder input to LCD menu
navigation on `four-relay-xbee-wifi`, plus the current KY-040 diagnostic and
pin-finder branches.

This document does not by itself authorize wiring, serial monitoring, XBee/RF
action, relay output work, load work, mains work, or live encoder acceptance.
The KY-040 GPIO13-pullup diagnostic image has a separate same-session COM6
write/verify gate recorded under
`SRC-LOCAL-FOUR-RELAY-KY040-DIAGNOSTIC-REFACTOR-2026-05-30`; the `PF0530A`
pin-finder diagnostic has a separate same-session COM6 write/verify gate
recorded under
`SRC-LOCAL-FOUR-RELAY-KY040-PIN-FINDER-DIAGNOSTIC-2026-05-30`. The `PF0530B`
row-0 diagnostic also has a same-session COM6 write/verify gate, followed by a
user no-change report. Further flash or verify-flash still requires a fresh
Tier 3 gate. The `PF0530C` GPIO sweep contact tracer also has a same-session
  COM6 write/verify gate. The `PF0530D` DevKitC 13/14/32 diagnostic also has a
  same-session COM6 write/verify gate for the user-confirmed wiring. The
  `PF0530E` serial pintrace branch completed the current COM6 live-monitor gate
  and proved GPIO-level changes on GPIO13/GPIO14/GPIO32 during r5
  user-confirmed actuation. `PF0530F` is the LCD menu-proof image prepared from
  that evidence; its COM6 flash/verify gate passed, but live menu acceptance is
  blocked by `PF0530F LCD_INIT_FAILED`. `PF0530G` later passed serial LCD init
  diagnosis at address `0x27`. `PF0530H` combined that LCD init path with
  static/simulated BBS pages and the GPIO13/GPIO14/GPIO32 encoder loop, but
  user testing reported no encoder/button LCD effect. `PF0530I` added split
  input polling and dirty-row LCD rendering but showed task-watchdog
  backtraces. `PF0530J` fixed the task-watchdog symptom but its first live
  monitor captured no input transitions. `PF0530K` is the current source fix:
  it keeps the one-tick input-task delay, adds GPIO any-edge interrupt queueing,
  and decodes menu rotation from raw A/B transitions.

## Verified facts

- The accepted LCD display-status proof uses GPIO21 as SDA and GPIO22 as SCL.
  Keep those pins reserved for the LCD path until a later source-backed gate
  changes it. Source ID:
  `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`.
- The accepted COM6 XBee bridge uses UART2 TX on GPIO17 and RX on GPIO16. Keep
  those pins reserved for the bridge. Source ID:
  `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`.
- Espressif's ESP32 GPIO documentation identifies strapping pins and
  flash-related pins that need first-pass avoidance or review before use.
  Source ID: `SRC-ESP-IDF-GPIO`.
- ESP32 GPIO34 through GPIO39 are input-only candidates when they are exposed
  by the exact board and shield. Source ID: `SRC-ESP-IDF-GPIO`.
- GPIO25, GPIO26, GPIO27, and GPIO33 remain relay candidates and should not be
  consumed for this encoder plan. Source IDs:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`, `SRC-ESP-IDF-GPIO`.
- Bourns documents PEC11R as a contacting incremental encoder family with
  detent and switch options, PC pins, 12/18/24 PPR options, and 1 mA at 5 VDC
  circuit compatibility. This is candidate/reference coverage only and does
  not verify the exact encoder. Source ID: `SRC-BOURNS-PEC11R`.
- The user-identified ASIN `B06XQTHDRR` is indexed by an independent Manuals+
  mirror as a Cylewet KY-040 rotary encoder module from Qianxin, with
  `CLK`, `DT`, `SW`, `+`, and `GND` pins, 20 pulses per rotation, and a
  typically active-low `SW` pin. This page recommends 5 V for Arduino-style
  use; the ESP32 diagnostic branch keeps the module in the 3.3 V domain unless
  a later level-shifting plan is accepted. Source ID:
  `SRC-MANUALSPLUS-CYLEWET-KY040-B06XQTHDRR`.
- The Envistia KY-040 guide describes onboard 10 kOhm pullups on `CLK`, `DT`,
  and `SW`, 3.3 V compatibility for the module class, and `SW` returning high
  through the onboard pullup when released. This is module-family support, not
  proof of the exact bench module. Source ID:
  `SRC-ENVISTIA-KY040-GUIDE-2026-05-30`.
- The current diagnostic refactor keeps GPIO34/GPIO35 internal pulls disabled
  and enables the ESP32 internal pullup only on GPIO13 for the KY-040 active-low
  `SW` input. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-DIAGNOSTIC-REFACTOR-2026-05-30`.
- The same source record now includes COM6 write-flash and separate verify-flash
  evidence for user LCD raw testing. User-observed raw transition proof is still
  pending.
- The pin-finder diagnostic keeps the page-0 raw display and adds firmware ID
  `PF0530A` plus an input-only pin-finder page for GPIO34, GPIO35, GPIO13,
  GPIO14, GPIO32, and GPIO33 live levels and change counters. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-PIN-FINDER-DIAGNOSTIC-2026-05-30`.
- The row-0 diagnostic refactor adds firmware ID `PF0530B` and cycles raw
  A/B/SW levels, raw A/B and SW transition counts, and each GPIO34/GPIO35/
  GPIO13/GPIO14/GPIO32/GPIO33 level/change-count view on LCD row 0. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-ROW0-DIAGNOSTIC-2026-05-30`.
- The GPIO sweep contact tracer adds firmware ID `PF0530C` after the user
  reported no displayed `PF0530B` pins changed. It locks LCD page 0, shows
  row-0 `HIT` on any watched GPIO change, sweeps GPIO34/GPIO35/GPIO36/GPIO39/
  GPIO13/GPIO14/GPIO18/GPIO19/GPIO23/GPIO32, enables internal pullups only on
  GPIO13/GPIO14, and closes the diagnostic XBee bridge loop. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-GPIO-SWEEP-CONTACT-TRACER-2026-05-30`.
- The DevKitC 13/14/32 diagnostic adds firmware ID `PF0530D` after the user
  confirmed `CLK` on GPIO13, `DT` on GPIO14, `SW` on GPIO32, module `+` on
  ESP32 3V3, and a 100 nF capacitor across `+` and `GND`. It locks LCD page 0,
  enables internal pullups on GPIO13/GPIO14/GPIO32, shows raw levels plus
  transition/position/button counts, and closes the diagnostic XBee bridge
  loop. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-DEVKITC-13-14-32-DIAGNOSTIC-2026-05-30`.
- The serial pintrace diagnostic adds firmware ID `PF0530E` after the user
  reported the LCD diagnostics still did not show changing pins. It watches a
  DevKitC candidate set as input-only GPIOs, enables internal pullups only on
  GPIO13/GPIO14/GPIO32, prints stable change events on COM6/UART0, and records
  the DevKitC risk that physical `J2-13` is `IO12` and `J2-14` is `GND`.
  Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30`.
- The final PF0530E r4 monitor completed without watchdog/backtrace output and
  without encoder-pin `EV` events; user-confirmed physical actuation during
  that monitor window remains unproven. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30`.
- A later PF0530E r5 read-only monitor recorded user-confirmed physical
  actuation, `writes_sent=false`, no watchdog/panic/backtrace scan hits, and
  GPIO13/GPIO14/GPIO32 count increases. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30`.
- The PF0530F repo-only menu-proof refactor boots the LCD menu path, keeps
  GPIO13/GPIO14/GPIO32 input-only with internal pullups, adds 2 ms A/B polling
  with three stable samples, 30 ms switch debounce, a 150 ms button guard window
  for suppressing A/B motion, invalid-transition counting, and serial proof
  events. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-2026-05-30`.

## Assumptions

- The future encoder is for LCD menu navigation only.
- Firmware should expose encoder activity as UI intents such as
  `rotate_left`, `rotate_right`, `select`, and optionally `long_press` or
  `back`.
- Encoder events must not directly trigger relay outputs, radio transmission,
  flash/erase operations, persistent configuration writes, or XBee setting
  writes.
- The selected KY-040 module will be tested in the ESP32 3.3 V domain. If the
  module only works when powered from 5 V, stop before reconnecting it to ESP32
  GPIO and plan level shifting or a different pullup wiring path.
- GPIO14/GPIO32/GPIO33 are temporary input-only pin-finder probes in PF0530A/B.
  PF0530C drops relay-candidate GPIO33, adds GPIO36/GPIO39 and passive
  GPIO18/GPIO19/GPIO23 beside GPIO32, and uses internal pullups only on
  GPIO13/GPIO14. A changing counter points to a continuity question; it does
  not accept those pins as the encoder wiring.
- PF0530F focuses the next menu-proof image on the user-confirmed wiring,
  using internal pullups only on GPIO13/GPIO14/GPIO32. GPIO32 remains
  unavailable for the provisional MicroSD CS investigation while this encoder
  branch is active.

## Unknowns

- Exact bench module markings and continuity from KY-040 `CLK`/`DT`/`SW` to
  GPIO13/GPIO14/GPIO32.
- Cause of `PF0530F LCD_INIT_FAILED` after the successful COM6 write/verify
  gate; PF0530G did not reproduce it and completed bus, probe, device-add,
  HD44780, display-write, and heartbeat serial proof at address `0x27`.
- Whether PF0530J live proof can show accepted `BBS_MENU_STEP` events in both
  directions, `BBS_MENU_SELECT` button events, matching LCD page/position/button
  changes, and no relay/XBee/unsafe action after LCD init is diagnosed.
- Pullup population, pullup voltage, debounce behavior, series resistance,
  cable length, ESD exposure, and noise risk on the exact KY-040 module.
- Exact exposed GPIO continuity on the installed ESP32 board and expansion
  shield.
- Whether any candidate GPIO choice changes boot behavior when the encoder is
  untouched, rotated, or pressed during reset.
- Rail-current margin after the LCD, XBee bridge, and any future panel wiring.

## Required signals

Use a keyed 5-pin connector or clearly labeled terminal block:

| Signal | Requirement |
| --- | --- |
| `GND` | Common ground with ESP32 logic. |
| `3V3` | ESP32 3.3 V logic domain only. |
| `ENC_A` | Encoder quadrature A input. |
| `ENC_B` | Encoder quadrature B input. |
| `ENC_SW` | Push switch input, if the selected encoder has a switch. |

Planning default for a bare encoder, retained for comparison only:

- 10 kOhm pullup to 3.3 V on `ENC_A`, `ENC_B`, and `ENC_SW`.
- Optional 100-330 ohm series resistors on A/B/SW near the ESP32.
- Start with firmware debounce before adding A/B capacitors.
- Add 0.01-0.1 uF from `ENC_SW` to GND only if switch bounce remains
  excessive.
- Consider a 74LVC14-class Schmitt buffer powered at 3.3 V only for long or
  noisy panel wiring.
- Add ESD protection if the encoder is panel-mounted with a cable leaving the
  PCB area.

These values are planning defaults, not an accepted schematic.

## Candidate GPIO strategy

The current KY-040 diagnostic branch assigns a pending-proof wiring plan:

- KY-040 `GND` to ESP32 `GND`.
- KY-040 `+` to ESP32 `3V3` only, not 5 V.
- KY-040 `CLK` to GPIO13.
- KY-040 `DT` to GPIO14.
- KY-040 `SW` to GPIO32.
- 100 nF capacitor across encoder `+` and `GND`.
- Follow the module silkscreen, not assumed left/right physical order.

This does not accept the wiring until continuity, voltage, boot, and raw LCD
transition evidence are recorded.

The pin-finder diagnostic also samples GPIO14, GPIO32, and GPIO33 as input-only
probes with internal pulls disabled. The `PF0530B` row-0 diagnostic cycles
these same probes on the first LCD row. The `PF0530C` contact tracer takes a
new approach: it locks LCD page 0 and watches GPIO34, GPIO35, GPIO36, GPIO39,
GPIO13, GPIO14, GPIO18, GPIO19, GPIO23, and GPIO32. GPIO13/GPIO14 have
internal pullups for direct-GND stimulus; the other sweep pins have internal
  pulls disabled. PF0530D then focuses on GPIO13/GPIO14/GPIO32 as the live
  encoder diagnostic pins with internal pullups enabled. PF0530E superseded the
  LCD-dependent proof path with serial pintrace events and proved GPIO-level
  changes on GPIO13/GPIO14/GPIO32 during r5 user-confirmed actuation. PF0530F
  returns to LCD menu proof on the same pins; its first COM6 flash/verify gate
  passed, but live menu acceptance is blocked by `PF0530F LCD_INIT_FAILED`.
  These probes exist only to identify continuity, LCD init, and decoder
  questions until a separate live gate accepts the menu behavior.

Preferred candidate class:

- GPIO34 through GPIO39 for `ENC_A`, `ENC_B`, and `ENC_SW` if the exact
  ESP32 board/shield exposes them and external 3.3 V pullups are installed.

Alternate candidate class:

- GPIO13 and GPIO14 plus one other verified non-conflicting input if the
  input-only pins are not exposed.

Do not use these first-pass groups for the encoder:

- GPIO21 and GPIO22, reserved for the accepted LCD path.
- GPIO17 and GPIO16, reserved for the accepted XBee bridge.
- GPIO25, GPIO26, GPIO27, and GPIO33, reserved as relay candidates.
- GPIO0, GPIO2, GPIO5, GPIO12, and GPIO15 until boot-strapping behavior is
  reviewed.
- GPIO6 through GPIO11, which are flash-related on ESP32-WROOM-32 designs.
- GPIO1 and GPIO3 while UART0 remains the USB serial flashing/debugging path.

## Connection planning

Bare encoder planning boundary:

- Encoder common pin to ESP32 GND.
- Encoder A to the future `ENC_A` GPIO with a 10 kOhm pullup to 3.3 V.
- Encoder B to the future `ENC_B` GPIO with a 10 kOhm pullup to 3.3 V.
- Pushbutton common to GND.
- Pushbutton output to the future `ENC_SW` GPIO with a 10 kOhm pullup to 3.3 V.

Module planning boundary:

- `GND` to ESP32 GND.
- `+` or `VCC` to ESP32 3.3 V only, not 5 V.
- `CLK` to `ENC_A`.
- `DT` to `ENC_B`.
- `SW` to `ENC_SW`.
- Stop before connection unless onboard pullups are verified to tie to 3.3 V.

## Gate plan

Bench intake before wiring:

- Record KY-040 module markings, source link, pin labels, pullups, voltage, and
  module silkscreen orientation.
- Record the exact ESP32 board/shield header continuity for the candidate
  encoder pins.

Electrical checks before ESP32 connection:

- Confirm no encoder/module pullup goes to 5 V.
- Confirm common ground.
- Confirm A/B/SW idle at 3.3 V and pull low when actuated.
- Confirm no encoder line is on a boot-sensitive pin.
- Confirm GPIO13/GPIO14/GPIO32 continuity from the KY-040 `CLK`/`DT`/`SW`
  pins before any acceptance claim.

First firmware proof:

- The input-only KY-040 GPIO13-pullup diagnostic image is written/verified to
  COM6 for user testing.
- The `PF0530A` pin-finder diagnostic is written/verified to COM6 for user
  LCD testing.
- The `PF0530B` row-0 diagnostic was written/verified, and the user reported no
  displayed pins changed.
- The `PF0530C` contact tracer was written and separately verify-flashed to
  COM6 under fresh same-session Tier 3 authority and safe-state confirmation.
- The `PF0530D` diagnostic was written and separately verify-flashed to COM6
  for GPIO13/GPIO14/GPIO32.
- The `PF0530E` serial pintrace diagnostic r5 proved GPIO13/GPIO14/GPIO32
  level changes during user-confirmed rotation and button press/release, with
  no writes and no watchdog/panic/backtrace scan hits.
- The `PF0530F` menu-proof image was written and separately verify-flashed to
  COM6; the read-only monitor captured `PF0530F MENU_READY` and then
  `PF0530F LCD_INIT_FAILED`, so live menu acceptance is not accepted.
- The `PF0530G` LCD init diagnostic produced stage-specific `LCD_*` serial
  proof with `LCD_INIT_OK addr=0x27`; renewed menu acceptance remains a
  separate live gate.
- The ESP-NOW BBS LCD/encoder field-console plan adds a host-only
  `bbs_lcd_state.v1` renderer for local BBS status pages. PF0530H now mirrors
  the same page set as static/simulated firmware text. The named PF0530H COM6
  live gate passed flash/verify/read-only-monitor proof and is ready for user
  LCD/encoder testing; it does not open additional flash, serial writes,
  XBee/RF, relay writes, wiring mutation, or broader live
  display acceptance by itself. Source IDs:
  `SRC-LOCAL-ESPNOW-BBS-LCD-ENCODER-FIELD-CONSOLE-2026-05-30`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-LIVE-2026-05-31`.
- The PF0530H source image is recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-2026-05-31`.
- PF0530H was not accepted as an interactive menu because user testing reported
  no encoder/button LCD effect and the live transcript had zero
  `BBS_MENU_STEP` or `BBS_MENU_SELECT` proof. PF0530I is the source fix: input
  polling runs in `fr_menu_input_task`, LCD rendering is dirty-row driven,
  `BBS_INPUT_READY` and `ENC_RAW` are emitted, and `BBS_LCD_RENDER` reports
  `rows`, `seq`, `dur_ms`, and `reason`. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530I-2026-05-31`.
- PF0530I live monitor showed repeated task-watchdog backtraces. PF0530J keeps
  the split input/render design, changes `FR_MENU_POLL_MS` to 10, and adds
  `fr_delay_ticks_at_least_one()`. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530J-2026-05-31`.
- The first PF0530J Tier 3 monitor showed no watchdog/backtrace output but also
  no input-transition proof. PF0530K adds GPIO any-edge interrupt queueing,
  `FR_ENCODER_EVENT_QUEUE_DEPTH 64`, `FR_ENCODER_IRQ_DRAIN_LIMIT 32`, raw A/B
  transition decoding, and `irq_drop` heartbeat proof. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530K-2026-05-31`.
- PF0530K live write-flash and separate verify-flash passed on COM6, and the
  read-only monitor showed no watchdog/backtrace/panic/LCD-init-failure
  markers. The same monitor captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, and zero `BBS_MENU_SELECT`, so interactive input acceptance
  remains blocked until physical actuation is captured. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530K-LIVE-2026-05-31`.
- For the PF0530K Tier 3 gate, confirm the serial monitor shows `PF0530K
  BBS_LCD_READY`, `BBS_INPUT_READY`, `LCD_INIT_OK addr=0x27`,
  `BBS_LCD_RENDER`, `BBS_MENU_HB`, `ENC_RAW`, `ENC_EV`, `BBS_MENU_STEP` in
  both directions, `BBS_MENU_SELECT` button events, and any button-window A/B
  noise only as `AB_SUPPRESS` or raw-only evidence.
- Boot with the encoder untouched, rotated, and switch held down.
- Confirm no boot failure.
- Confirm rotation emits one menu step per detent after debounce.
- Confirm button press emits `select` only.
- Confirm encoder events cannot directly trigger relay, radio, flash, or
  persistent configuration paths.

## Stop conditions

Stop if any of these are true:

- Module pullups are tied to 5 V.
- Pinout is uncertain.
- Candidate GPIO affects boot.
- Relay, load, or mains paths are connected.
- Encoder events can directly trigger relay, radio transmit, flash/erase, XBee
  setting writes, or persistent configuration writes.

## Sources

- `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`
- `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`
- `SRC-ESP-IDF-GPIO`
- `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`
- `SRC-BOURNS-PEC11R`
- `SRC-MANUALSPLUS-CYLEWET-KY040-B06XQTHDRR`
- `SRC-ENVISTIA-KY040-GUIDE-2026-05-30`
- `SRC-LOCAL-FOUR-RELAY-ROTARY-ENCODER-MENU-PLAN-2026-05-30`
- `SRC-LOCAL-FOUR-RELAY-KY040-DIAGNOSTIC-REFACTOR-2026-05-30`
- `SRC-LOCAL-FOUR-RELAY-KY040-PIN-FINDER-DIAGNOSTIC-2026-05-30`
- `SRC-LOCAL-FOUR-RELAY-KY040-ROW0-DIAGNOSTIC-2026-05-30`
- `SRC-LOCAL-FOUR-RELAY-KY040-GPIO-SWEEP-CONTACT-TRACER-2026-05-30`
- `SRC-LOCAL-FOUR-RELAY-KY040-DEVKITC-13-14-32-DIAGNOSTIC-2026-05-30`
- `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30`
- `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-2026-05-30`
- `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-LIVE-2026-05-30`
- `SRC-LOCAL-FOUR-RELAY-KY040-LCD-INIT-DIAG-PF0530G-2026-05-30`
- `SRC-LOCAL-ESPNOW-BBS-LCD-ENCODER-FIELD-CONSOLE-2026-05-30`
- `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-2026-05-31`
- `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530I-2026-05-31`
- `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530J-2026-05-31`
- `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530K-2026-05-31`
- `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530K-LIVE-2026-05-31`
