# ESP-NOW BBS LCD/Encoder Field Console Plan

Source index: [../../../knowledge-base/source-index.md](../../../knowledge-base/source-index.md)

## Scope

This is a Tier 2 host-only design, documentation, and simulator slice for a
20x4 HD44780/PCF8574-class LCD plus rotary encoder local BBS field console.
This plan itself did not authorize live flash, serial monitor, serial writes,
XBee/RF, ESP-NOW runtime traffic, relay GPIO writes, relay-expander writes,
TFT, MicroSD, wiring mutation, load, mains, erase, commit, or push. A later
separate PF0530H COM6 live gate did authorize and complete the local BBS LCD
menu flash/verify/read-only-monitor proof only, but PF0530H was not accepted
as interactive after user testing reported no encoder/button LCD effect.

The console role is read-only local situational awareness for the accepted BBS
path: custody, peers, link health, mesh/service summaries, queue state, files,
XBee closed-surface status, locks, and diagnostics. Rotary input creates local
UI intents only.

## Verified Facts

- The accepted live BBS custody path remains
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
  Source IDs: `SRC-LOCAL-BBS-UI-SYSTEM-OPERATION-PROGRAM-2026-05-28`,
  `SRC-LOCAL-BBS-UI-UI0-M2B-HOST-SLICE-2026-05-28`.
- Gate F/G/M records keep packet jobs, custody, discovery, analytics, and mesh
  summaries host-only or simulator-first unless a later gate opens runtime
  behavior. Source IDs:
  `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`,
  `SRC-LOCAL-ESPNOW-GATE-G-LIVE-EXPORT-IMPLEMENTATION-2026-05-25`,
  `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`.
- The current custom wireless protocol budget keeps 512-byte ASCII bridge
  lines and a 250-byte ESP-NOW v1-compatible packet budget. Source IDs:
  `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-F-OWNER-REVIEW-2026-05-26`,
  `SRC-ESP-IDF-ESPNOW`.
- ESP-NOW send success is MAC-layer status and still needs application-level
  acknowledgement/retry/custody policy. Source ID: `SRC-ESP-IDF-ESPNOW`.
- ESP-WIFI-MESH topology, parent/root selection, routing, and healing remain a
  design/reference path; live ESP-WIFI-MESH is not opened by this plan. Source
  IDs: `SRC-ESP-IDF-WIFI-MESH`,
  `SRC-LOCAL-ESPNOW-FULL-SERVICE-MESH-DISCOVERY-2026-05-27`.
- The current 20x4 LCD lineage uses I2C0 GPIO21/GPIO22 and PF0530G passed
  serial LCD init diagnostics at `0x27`; physical LCD visual confirmation
  remains unresolved. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-LCD-INIT-DIAG-PF0530G-2026-05-30`.
- The current KY-040 menu lineage uses GPIO13/GPIO14/GPIO32 in the 3.3 V
  domain; PF0530F live menu acceptance remains blocked after `LCD_INIT_FAILED`.
- PF0530H later passed the named COM6 flash/verify/read-only-monitor gate for
  local BBS LCD menu user testing, but its transcript showed zero
  `BBS_MENU_STEP` and zero `BBS_MENU_SELECT` proof. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-LIVE-2026-05-31`.
- PF0530I is the source fix for the PF0530H input symptom. It splits input
  polling into `fr_menu_input_task`, keeps GPIO13/GPIO14/GPIO32 input-only,
  renders only dirty LCD rows or a slow idle refresh, emits `BBS_INPUT_READY`
  and `ENC_RAW`, and extends `BBS_LCD_RENDER` with `rows`, `seq`, `dur_ms`,
  and `reason`. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530I-2026-05-31`.
- PF0530I live monitor showed repeated task-watchdog backtraces. PF0530J keeps
  the split input/render design, changes `FR_MENU_POLL_MS` to 10, and adds
  `fr_delay_ticks_at_least_one()` so the input task yields for at least one
  FreeRTOS tick. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530J-2026-05-31`.
- The first PF0530J live monitor showed the watchdog fix working but captured
  no input transitions. PF0530K keeps the watchdog fix, adds GPIO any-edge
  interrupt queueing for GPIO13/GPIO14/GPIO32, decodes rotation from raw A/B
  transitions, and reports `irq=anyedge queue=64` readiness proof. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530K-2026-05-31`.
- PF0530K live write-flash and separate verify-flash passed on COM6. The
  monitor captured ready/render/heartbeat proof and no watchdog/backtrace/
  panic/LCD-init-failure markers, but no encoder/button input proof. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530K-LIVE-2026-05-31`.
  Source IDs:
  `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-2026-05-30`,
  `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-LIVE-2026-05-30`.
- HD44780 CGRAM planning is limited to eight 5x8 custom-character types.
  Source ID: `SRC-HITACHI-HD44780U-CGRAM-2026-05-30`.
- PCF8574/74A is source coverage for an I2C 8-bit GPIO expander class only; it
  does not verify the exact LCD backpack. Source ID: `SRC-NXP-PCF8574-74A`.
- Digi XBee `NP` is a future measured payload-budget input before selecting
  any low-speed XBee payload framing. Source ID: `SRC-DIGI-XBEE-900HP-NP`.
- CBOR, SLIP, PPP HDLC-like framing, and COBS are planning references only for
  future payload/framing evaluation. Source IDs: `SRC-RFC8949-CBOR-2026-05-30`,
  `SRC-RFC1055-SLIP-2026-05-30`, `SRC-RFC1662-PPP-HDLC-2026-05-30`,
  `SRC-CHESHIRE-BAKER-COBS-2026-05-30`.

## Assumptions

- First implementation is read-only/static or simulator-fed.
- `bbs_lcd_state.v1` is a local renderer snapshot schema, not a bridge ABI,
  radio ABI, coordinator serial ABI, firmware ABI, or Win31 transport change.
- Missing values render as `?`; closed surfaces render as `CLOSED`.
- The next renewed firmware proof image name is `PF0530K`, combining PF0530G
  LCD init diagnostics, PF0530F/PF0530H BBS menu content, split input polling,
  a minimum one-tick input task delay, and interrupt-queued KY-040 input
  capture.

## Unknowns

- Physical LCD visual state after PF0530G.
- Rail margin, exact LCD backpack pullup voltage, and exact encoder module
  electrical behavior.
- Encoder rotation sign and boot behavior with the encoder untouched, rotated,
  or held down during reset.
- Any future XBee/ESP-NOW bridge mapping, payload shape, or framing selection.

## Snapshot Schema

`bbs_lcd_state.v1` contains only compact top-level fields:

- `schema`
- `mode`
- `link`
- `peers`
- `queue`
- `custody`
- `messages`
- `files`
- `telemetry`
- `mesh`
- `xbee`
- `locks`
- `last_event`
- `uptime_ms`

Secret-bearing fields are rejected recursively by the host renderer. Message
bodies, raw file names, precise location, PMK/LMK material, pairing tokens,
credentials, and raw identifiers must not enter the LCD snapshot.

## Pages

- `HOME`: BBS mode, link, peer count, queue count, custody owner, last event.
- `MESSAGES`: new/inbox/outbox counts and custody acknowledgement summary.
- `PEERS`: active/known peers, link state, RSSI, ACK, duplicate count, mesh root.
- `QUEUE`: pending/failed/retry counts and non-executing control status.
- `FILES`: queued/done/byte summary; names and transfer surfaces stay closed.
- `MESH`: host-only mesh mode/root/hop/healing summary; live mesh closed.
- `XBEE`: closed UART/TX surface and measured/planned `NP` budget value.
- `DIAG`: uptime, display simulator status, and last event.
- `LOCKS`: relay, XBee, flash, and serial-write lock labels.

## Input Rules

- Rotate changes page in normal view.
- Rotate changes selected row only in detail view.
- Short press enters local detail or acknowledges a local notification.
- Long press returns home.
- Double-click is not part of v1.
- Input events must not directly trigger relay output, XBee transmit, ESP-NOW
  transmit, flash/erase, persistent configuration, serial writes, or bridge
  commands.

## Display Rules

- Every render emits exactly four lines of exactly 20 cells.
- No scrolling is required in v1. Detail-page marquee behavior is future work
  and must update no faster than 250 ms if added.
- Truncated values are safer than guessed values.
- `CLOSED` labels are explicit for locked live surfaces.
- Only eight custom glyph slots are available: lock, warning, envelope, queue
  arrow, ACK mark, radio-low, radio-high, and spinner.

## Host Renderer

The implementation lives under
[lcd_bbs_menu.py](../../../tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py).
It accepts a `bbs_lcd_state.v1` snapshot and emits:

- `schema`
- `page`
- four fixed-width `lines`
- eight-slot `glyph_bank`
- local `view` state

Tests live under
[test_lcd_bbs_menu.py](../../../tests/lcd_bbs_menu/test_lcd_bbs_menu.py).

The graphics/browser continuation is tracked in
[lcd-menu-graphics-browser-agent-plan.md](lcd-menu-graphics-browser-agent-plan.md).
It adds `bbs_lcd_render.v1`, software cursor metadata, named glyph banks,
widget previews, an inert host browser mirror, and a recallable
LCD-menu-operations skill while preserving this plan's closed live surfaces.

## PF0530H Source Gate

PF0530H source work is now prepared in the four-relay XBee Wi-Fi firmware lane
as a local static/simulated BBS LCD menu image. It combines the PF0530G LCD
init/probe path with the PF0530F GPIO13/GPIO14/GPIO32 encoder menu loop. The
required proof strings are:

- `PF0530H BBS_LCD_READY`
- `BBS_MENU_HB`
- `BBS_MENU_STEP`
- `BBS_MENU_SELECT`
- `BBS_LCD_RENDER`

The image keeps `FR_DIAG_XBEE_BRIDGE_CLOSED 1` and does not open XBee/RF,
ESP-NOW runtime, relay, TFT, MicroSD, wiring, load, mains, erase, or serial
write surfaces. Live COM6 flash and user LCD/encoder acceptance remain separate
Tier 3 gates.

## PF0530I Input Responsiveness Gate

PF0530I source work is now prepared in the four-relay XBee Wi-Fi firmware lane
as the bounded fix for PF0530H input starvation. Required proof strings are:

- `PF0530I BBS_LCD_READY`
- `BBS_INPUT_READY`
- `ENC_RAW`
- `ENC_EV`
- `BBS_MENU_HB`
- `BBS_MENU_STEP`
- `BBS_MENU_SELECT`
- `BBS_LCD_RENDER`

`BBS_LCD_RENDER` must include `rows`, `seq`, `dur_ms`, and `reason` fields.
The image keeps `FR_DIAG_XBEE_BRIDGE_CLOSED 1` and does not open XBee/RF,
ESP-NOW runtime, relay, TFT, MicroSD, wiring, load, mains, erase, or serial
write surfaces. Live COM6 flash and user LCD/encoder acceptance remain separate
Tier 3 gates.

## PF0530J Watchdog Fix Gate

PF0530J source work supersedes PF0530I after the first PF0530I monitor showed
task-watchdog backtrace output. Required proof strings are:

- `PF0530J BBS_LCD_READY`
- `BBS_INPUT_READY`
- `ENC_RAW`
- `ENC_EV`
- `BBS_MENU_HB`
- `BBS_MENU_STEP`
- `BBS_MENU_SELECT`
- `BBS_LCD_RENDER`

PF0530J must keep `FR_MENU_POLL_MS 10`, `fr_delay_ticks_at_least_one()`, and
the closed-surface boundaries from PF0530I. Live COM6 proof must show no
watchdog/backtrace/panic/crash markers before the image is accepted.

## PF0530K Interrupt Input Gate

PF0530K source work supersedes PF0530J for the unresolved no-input-transition
proof gap. Required proof strings are:

- `PF0530K BBS_LCD_READY`
- `BBS_INPUT_READY`
- `irq=anyedge queue=64`
- `ENC_RAW`
- `ENC_EV`
- `BBS_MENU_HB`
- `BBS_MENU_STEP`
- `BBS_MENU_SELECT`
- `BBS_LCD_RENDER`

PF0530K must keep the closed-surface boundaries from PF0530J, keep
`FR_MENU_POLL_MS 10`, keep `fr_delay_ticks_at_least_one()`, and report no
watchdog/backtrace/panic/crash markers during live COM6 proof.

## Validation Plan

- Host LCD menu renderer tests.
- Existing custom wireless protocol tests.
- Four-relay host tests.
- Scaffold audits and `verify_scaffold.py`.
- Changed-file source-ID and Markdown link checks.
- Closed-surface scan.
- `git diff --check`.

## Stop Gates

Stop before any live flash, monitor, serial write, XBee/RF action, ESP-NOW live
runtime, relay write, relay-expander write, TFT/MicroSD action, wiring change,
load, mains, erase, framework selection, firmware ABI change, bridge ABI
change, coordinator serial ABI change, Win31 transport change, commit, or push.
