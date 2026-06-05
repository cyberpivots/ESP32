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
- PF0530L became the accepted flashed image for renewed live LCD menu UX
  testing. It keeps the PF0530K interrupt input path and adds local page/row/detail/edit
  modes, software cursor/DDRAM tracking, dirty-cell metadata, five named
  eight-slot glyph banks, custom bar/chart/digit/gauge demo pages, and an
  auto-demo cycle. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530L-2026-05-31`.
- PF0530L live write-flash and separate verify-flash passed on COM6; the
  read-only monitor captured auto-demo coverage for all 13 page names and all
  five glyph banks, but no physical encoder/button input proof. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530L-LIVE-2026-05-31`.
- PF0530M is the prior non-live source/test continuation after PF0530L visual
  and electrical acceptance. It kept the closed bridge and input-only GPIO
  boundaries, adds operational status rows, bridge-closed display,
  diagnostic/error rows, row action labels, editable widget rows, and host-side
  menu state tests. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530M-2026-06-01`.
- PF0530N is the scrolling/XML source/test continuation after
  PF0530M. It adds build-time `bbs_lcd_menu.v1` XML, generated static
  firmware/simulator definitions, host render schema `bbs_lcd_render.v2`,
  scroll-list item navigation, grouped multi-row items, selected-row marquee,
  and a separate table glyph bank while preserving the closed bridge,
  input-only GPIO13/GPIO14/GPIO32, and display-only GPIO21/GPIO22 LCD
  boundaries. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530N-SCROLLING-XML-2026-06-01`.
- PF0530N write-flash and separate verify-flash passed on COM6. The read-only
  monitor captured `PF0530N BBS_LCD_READY`, `PF0530N BBS_INPUT_READY`,
  `bbs_lcd_menu.v1`, `bbs_lcd_render.v2`, render/cursor/heartbeat/auto-demo/
  glyph-bank proof, and no crash/unsafe markers. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530N-LIVE-2026-06-01`.
- PF0530O is the prior flashed real-menu calibration image. It keeps the closed
  bridge and input-only/display-only boundaries, changes the active firmware ID
  to `PF0530O`, uses one transition per menu step, two AB stable samples, a
  75 ms switch guard, a 650 ms long press, disables boot auto-cycle, and reports
  `cal=real-menu-v1`. PF0530O write-flash and separate verify-flash passed on
  COM6; reset and attended read-only monitors proved LCD readiness/render/
  heartbeat output with zero crash/unsafe markers, but captured zero input
  events. Source IDs:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530O-REAL-MENU-CAL-2026-06-01`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530O-LIVE-2026-06-01`.
- PF0530P is the previous debounce calibration source/build
  continuation. It keeps the closed bridge and input-only/display-only
  boundaries, changes the active firmware ID to `PF0530P`, keeps one transition
  per menu step and two AB stable samples, adds a 5 ms A/B candidate hold,
  adds a 40 ms step lockout, keeps 30 ms switch debounce, a 75 ms switch guard,
  and a 650 ms long press, and reports
  `cal=debounce-v2 ab_ms=5 step_lockout_ms=40`. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530P-DEBOUNCE-CAL-2026-06-01`.
- PF0530P write-flash and separate verify-flash passed on COM6. Reset and
  attended read-only monitors captured PF0530P LCD/input readiness,
  `cal=debounce-v2`, `ab_ms=5`, `step_lockout_ms=40`, repeated render and
  heartbeat output, zero crash/unsafe markers, and zero input events. User
  visual/input acceptance remains pending. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530P-LIVE-2026-06-01`.
- PF0530Q is the previous quiet-window calibration source/build continuation
  after the user clarified they did not rotate during the PF0530P monitor. It
  keeps the closed bridge and input-only/display-only boundaries, changes the
  active firmware ID to `PF0530Q`, keeps one transition per menu step, two AB
  stable samples, a 5 ms A/B candidate hold, 30 ms switch debounce, a 75 ms
  switch guard, and a 650 ms long press, adds a 10 ms combined A/B pair quiet
  window, raises step lockout to 60 ms, and reports
  `cal=quiet-v3 ab_ms=5 quiet_ms=10 step_lockout_ms=60`. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530Q-QUIET-CAL-2026-06-01`.
- PF0530Q write-flash and separate verify-flash passed on COM6. Reset and idle
  read-only monitors captured PF0530Q LCD/input readiness, `cal=quiet-v3`,
  `ab_ms=5`, `quiet_ms=10`, `step_lockout_ms=60`, repeated render and
  heartbeat output, zero bad render rows, zero crash/unsafe markers, and zero
  input events with no physical actuation expected. Physical input acceptance
  remains pending; the later user report says it works but is not stable.
  Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530Q-LIVE-2026-06-01`.
- PF0530R is the previous detent-gated calibration source/build continuation
  after the PF0530Q user report. It keeps the closed bridge and input-only/
  display-only boundaries, changes the active firmware ID to `PF0530R`, raises
  A/B candidate hold to 8 ms, raises combined A/B quiet time to 15 ms, changes
  `FR_ENCODER_TRANSITIONS_PER_STEP` to 2, raises step lockout to 90 ms, emits
  at most one menu step only when accepted quadrature returns to detent A/B
  `3`, adds detent return/step/partial telemetry, and reports
  `cal=detent-v4 ab_ms=8 quiet_ms=15 step_lockout_ms=90 detent=3`. PF0530R
  is now written and separately verify-flashed on COM6 with readiness/render
  proof, zero crash/unsafe markers, zero bad render rows, and cleanup proof.
  The attended monitor captured zero input events, so physical input
  acceptance remains open. Source IDs:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530R-DETENT-CAL-2026-06-01`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530R-LIVE-2026-06-01`.
- PF0530S is the accepted written/verify-flashed raw-liveness recovery after
  PF0530R captured zero input event lines. It keeps the closed bridge and
  input-only/display-only boundaries, changes the active firmware ID to
  `PF0530S`, changes A/B debounce to 3 ms, quiet time to 0 ms,
  `FR_ENCODER_TRANSITIONS_PER_STEP` to 1, and step lockout to 45 ms, keeps
  detent counters as telemetry, emits steps without requiring return to detent
  A/B `3`, and adds `ENC_BASE`, `ENC_GPIO_CONFIG`, ESP-IDF GPIO config dump,
  one-second `ENC_LEVEL_HB`, raw/ISR/queue/poll heartbeat counters, and
  `cal=raw-live-v5`. COM6 live proof recovered raw A/B and switch liveness,
  both menu directions, short and long selects, and LCD/menu response, but full
  rotary stability remains open due to invalid/suppressed transitions and
  queue drops. Source IDs:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530S-RAW-LIVENESS-CAL-2026-06-01`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530S-LIVE-2026-06-01`.
- PF0530U is the last written/verify-flashed responsive-v7 image; its
  post-flash monitors captured no physical input events, so actuation proof
  remains open. Source IDs:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530U-RESPONSIVE-V7-2026-06-02`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530U-LIVE-2026-06-02`.
- PF0530V is the previous accepted written/verify-flashed PCNT continuation. It
  keeps the closed bridge and input-only/display-only boundaries, changed the
  firmware ID to `PF0530V`, declares `esp_driver_pcnt`, uses ESP-IDF PCNT
  quadrature counting on GPIO13/GPIO14, keeps switch polling/debounce, and
  reports `cal=pcnt-v1`, `decoder=pcnt`, `irq=pcnt`, and `poll_decoder=0`.
  PF0530V COM6 identity, rollback, write-flash, separate verify-flash,
  reset/read-only readiness monitor, idle read-only monitor, scan, and cleanup
  proof passed. The user later stated `ENCODER FUNCTIONALITY CONFIRMED AND
  APPROVED BY USER`, accepting PF0530V real LCD menu encoder functionality.
  Post-confirmation transcript-count characterization remains open. Source IDs:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-PCNT-SOURCE-BUILD-2026-06-02`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-LIVE-2026-06-02`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-USER-ACCEPTANCE-2026-06-02`.
- PF0530W is the active written/verify-flashed firmware-visible LCD visual-art
  continuation. It keeps the PF0530V PCNT encoder path and adds the generated
  `ART` page, seventh `art_panel` glyph bank, and fixed 4x20 custom-character
  tile map. COM6 identity, rollback, write/verify, read-only PF0530W readiness
  monitor, transcript scan, and cleanup proof passed; physical ART page visual
  acceptance and ART render telemetry remain pending. Task 0148 adds
  source/build-only ART-carousel behavior, and Task 0181 accepts host-only
  simulator/catalog/record validation for that carousel without claiming
  physical LCD acceptance. Source IDs:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-VISUAL-ART-2026-06-02`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-LIVE-2026-06-02`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-ART-CAROUSEL-2026-06-02`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-HOST-ONLY-VALIDATION-2026-06-05`.
- Earlier encoder-menu lineage source IDs:
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
- PF0530N keeps `bbs_lcd_state.v1` as renderer input and emits
  `bbs_lcd_render.v2` as host-render output.
- Missing values render as `?`; closed surfaces render as `CLOSED`.
- The current source firmware image name is `PF0530W`, combining
  the PF0530L/PF0530M LCD/menu lineage, PF0530N XML-generated scroll-list/
  table behavior, PF0530O operator-controlled input calibration, PF0530P
  debounce/step-lockout telemetry, PF0530Q combined A/B pair quiet-window
  filtering, PF0530R detent-gated decoding, PF0530S raw-liveness telemetry,
  PF0530U responsive-v7 source/live evidence, PF0530V PCNT source/build
  recovery, PF0530V user-confirmed functional acceptance, PF0530W
  firmware-visible visual-art source integration, and PF0530W COM6
  write/verify/readiness proof.

## Unknowns

- Physical LCD visual state after PF0530G.
- Rail margin, exact LCD backpack pullup voltage, and exact encoder module
  electrical behavior.
- Encoder rotation sign and boot behavior with the encoder untouched, rotated,
  or held down during reset.
- PF0530N serial boot/runtime proof is recorded, but physical readability of
  the scroll-list and table page remains unproven.
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
- `ROUTES`: table-formatted route/peer status summary in PF0530N.

## Input Rules

- PF0530N rotate changes the selected XML-defined item in the active page's
  scroll list, not the page.
- The indicator moves through the four physical LCD rows and the viewport
  scrolls when the selected item reaches a visible edge.
- Short press follows the selected item's XML-defined action: navigate to a
  target page, open local detail, enter local edit mode, or go back.
- Long press exits edit/detail first, then backs through a bounded page stack,
  then returns home.
- Double-click is not part of the current schema.
- Input events must not directly trigger relay output, XBee transmit, ESP-NOW
  transmit, flash/erase, persistent configuration, serial writes, or bridge
  commands.

## Display Rules

- Every render emits exactly four lines of exactly 20 cells.
- The left LCD column is reserved for the selection/continuation indicator; the
  remaining 19 columns are content.
- PF0530N selected overlong item rows marquee after a 750 ms start hold, then
  advance every 250 ms with two spaces between wrap cycles.
- Non-selected overlong text clips to the 19-column content area.
- Grouped multi-row items select only on the group's first row; continuation
  rows scroll with the group.
- Truncated values are safer than guessed values.
- `CLOSED` labels are explicit for locked live surfaces.
- Each page selects one eight-slot glyph bank. The PF0530N `table` bank must
  not be mixed with bar/chart/big-digit/gauge pages.

## Host Renderer

The implementation lives under
[lcd_bbs_menu.py](../../../tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py).
It accepts a `bbs_lcd_state.v1` snapshot and emits:

- `schema`
- `page`
- four fixed-width `lines`
- eight-slot `glyph_bank`
- local `view` state
- PF0530N `bbs_lcd_render.v2` viewport metadata: selected item ID, visible item
  IDs, physical indicator row, viewport top line, horizontal scroll offsets,
  and source XML metadata.

Tests live under
[test_lcd_bbs_menu.py](../../../tests/lcd_bbs_menu/test_lcd_bbs_menu.py).

The graphics/browser continuation is tracked in
[lcd-menu-graphics-browser-agent-plan.md](lcd-menu-graphics-browser-agent-plan.md).
It originally added `bbs_lcd_render.v1`, software cursor metadata, named glyph
banks, widget previews, an inert host browser mirror, and a recallable
LCD-menu-operations skill. PF0530N supersedes the host render output with
`bbs_lcd_render.v2` viewport metadata while preserving this plan's closed live
surfaces.

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

## PF0530L LCD Menu UX Gate

PF0530L source work supersedes PF0530K for the renewed user-test image. Required
proof strings are:

- `PF0530L BBS_LCD_READY`
- `BBS_INPUT_READY`
- `BBS_GLYPH_BANK`
- `BBS_CURSOR`
- `BBS_LCD_RENDER`
- `BBS_MENU_AUTO`
- `BBS_MENU_HB`
- `ENC_RAW`
- `ENC_EV`
- `BBS_MENU_STEP`
- `BBS_MENU_SELECT`

PF0530L must keep the closed-surface boundaries from PF0530K, keep
`FR_MENU_POLL_MS 10`, keep `fr_delay_ticks_at_least_one()`, keep
`irq=anyedge queue=64`, enforce five named eight-slot glyph banks, and report
no watchdog/backtrace/panic/crash markers during live COM6 proof. A live flash
may make PF0530L available for user testing; interactive acceptance still
requires physical actuation proof.

PF0530L COM6 write-flash and separate verify-flash passed on May 31, 2026. The
read-only monitor captured `LCD_INIT_OK`, `PF0530L BBS_LCD_READY`,
`BBS_INPUT_READY`, all 13 page names, all five glyph banks, 77
`BBS_LCD_RENDER`, 21 `BBS_MENU_AUTO`, and 74 `BBS_MENU_HB` lines with no
watchdog/backtrace/panic/LCD-init-failure or unsafe-open markers. It captured
zero `ENC_RAW`, zero `ENC_EV`, zero `BBS_MENU_STEP`, and zero
`BBS_MENU_SELECT`, so PF0530L is flashed for user visual testing but not
accepted as proven physically interactive. Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530L-LIVE-2026-05-31`.

## PF0530M Non-Live Menu Behavior Gate

PF0530M source work superseded PF0530L as the historical non-live development
branch before the PF0530N and PF0530O follow-up gates. Required source/test
markers are:

- `PF0530M BBS_LCD_READY`
- `BBS FIELD STATUS`
- `BRIDGE LOCAL CLOSED`
- `DIAG ERRORS:0`
- `actions=detail,edit,back`
- host-rendered 13-page `PAGES`
- widget-page glyph-bank mapping
- row/detail/edit state-machine tests

PF0530M must keep the PF0530L closed-surface boundaries. It does not authorize
COM6 access, flash, monitor, serial writes, RF/XBee writes, relay/load/mains,
wiring mutation, persistent config, or publication.

## PF0530N Scrolling/XML Gate

PF0530N source work superseded PF0530M as the scrolling/XML development
branch before the PF0530O, PF0530P, and PF0530Q calibration images. Required source/test
markers are:

- `PF0530N BBS_LCD_READY`
- `bbs_lcd_menu.v1`
- `bbs_lcd_render.v2`
- generated static firmware menu definitions
- 14-page generated menu model with 63 generated items
- scroll-list selection and viewport metadata
- selected-row marquee timing
- grouped multi-row item behavior
- table glyph bank within eight HD44780 slots

PF0530N must keep the PF0530L/PF0530M closed-surface boundaries and must not
add an ESP32 runtime XML parser. The later COM6 live gate is recorded under
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530N-LIVE-2026-06-01`; it
authorizes only the completed PF0530N write/verify/read-only monitor evidence
and does not open serial writes, RF/XBee writes, relay/load/mains, wiring
mutation, DMM/current measurement, persistent config, publication, commit, or
push.

## PF0530P Debounce Calibration Gate

PF0530P source/build work supersedes PF0530O as the next image candidate for
KY-040 LCD-menu user testing. Required source/test markers are:

- `PF0530P BBS_LCD_READY`
- `PF0530P BBS_INPUT_READY`
- `cal=debounce-v2`
- `ab_ms=5`
- `step_lockout_ms=40`
- `ENC_FILTER reason=ab_debounce`
- `ENC_FILTER reason=step_lockout`
- `ENC_FILTER reason=invalid`
- `ENC_FILTER reason=sw_guard`
- `BBS_MENU_SELECT` with `held_ms`
- `BBS_MENU_HB` with debounce, stable A/B, lockout, invalid, suppressed, and
  queue-drop counters

PF0530P has COM6 identity, rollback, write/verify, reset monitor, attended
monitor, transcript scan, and cleanup evidence. It is not physically accepted
until a user visual/input report or a later read-only input-capture gate proves
encoder/button behavior.

## PF0530Q Quiet Calibration Gate

PF0530Q source/build work supersedes PF0530P as the next image candidate after
the user clarified they did not rotate during the PF0530P monitor. Required
source/test markers are:

- `PF0530Q BBS_LCD_READY`
- `PF0530Q BBS_INPUT_READY`
- `cal=quiet-v3`
- `ab_ms=5`
- `quiet_ms=10`
- `step_lockout_ms=60`
- `ENC_FILTER reason=ab_debounce`
- `ENC_FILTER reason=ab_quiet`
- `ENC_FILTER reason=step_lockout`
- `ENC_FILTER reason=invalid`
- `ENC_FILTER reason=sw_guard`
- `ENC_RAW` with raw A/B gap and burst counters
- `BBS_MENU_HB` with debounce, quiet-hold, stable A/B, lockout, invalid,
  suppressed, raw-burst, raw-gap, and queue-drop counters

PF0530Q has COM6 identity, rollback, write/verify, reset monitor, idle monitor,
transcript scan, and cleanup evidence. It is not physically accepted until a
live read-only monitor with physical actuation captures encoder/button behavior
and a user visual report confirms the LCD response.

## PF0530R Detent Calibration Live Gate

PF0530R is a recorded written/verify-flashed detent calibration image. Its
live record includes COM6 identity, full rollback backup, artifact hashes,
write-flash, separate verify-flash, reset monitor, 150 second attended
read-only monitor, transcript scan, and cleanup proof. Required live markers
captured by readiness proof include:

- `PF0530R BBS_LCD_READY`
- `PF0530R BBS_INPUT_READY`
- `LCD_INIT_OK addr=0x27`
- `cal=detent-v4`
- `ab_ms=8`
- `quiet_ms=15`
- `step_lockout_ms=90`
- `detent=3`

The PF0530R live scan is readiness proof, not physical input acceptance: it
captured zero `ENC_RAW`, zero `ENC_EV`, zero `BBS_MENU_STEP`, zero
`BBS_MENU_SELECT`, and zero `ENC_FILTER`. Stable physical encoder/button
acceptance still requires confirmed actuation evidence or a user visual/input
report on the currently flashed PF0530R image.

## PF0530S Raw-Liveness Recovery Gate

PF0530S is the accepted raw-liveness recovery image after the PF0530R attended
monitor captured zero input event lines. The PF0530S live gate has proven these
boot/readiness markers:

- `PF0530S BBS_LCD_READY`
- `PF0530S BBS_INPUT_READY`
- `LCD_INIT_OK addr=0x27`
- `cal=raw-live-v5`
- `ab_ms=3`
- `quiet_ms=0`
- `step_lockout_ms=45`
- `raw_hb_ms=1000`
- `gpio_cfg=1`
- `poll_raw=1`
- `ENC_BASE`
- `ENC_GPIO_CONFIG`
- `ENC_LEVEL_HB`

PF0530S accepted raw-liveness evidence includes nonzero `ENC_RAW`, nonzero
`ENC_EV` on GPIO13/GPIO14/GPIO32, menu steps in both directions, short and
long `BBS_MENU_SELECT`, visible LCD/menu response, no serial byte writes,
cleanup proof, and zero crash/unsafe markers. Full rotary stability remains
open because the same attended proof recorded invalid/suppressed transitions
and queue drops. The next gate should tune decoder/queue/debounce behavior
instead of reopening raw input visibility.

## PF0530V PCNT Live Gate

PF0530V is the previous accepted written/verify-flashed PCNT image after
PF0530U was written and verify-flashed but did not capture physical input
events in post-flash monitors. PF0530W now supersedes it as the active
written/verify-flashed visual-art image while preserving the PF0530V PCNT path.
Required PF0530V live/readiness markers were:

- `PF0530V BBS_LCD_READY`
- `PF0530V BBS_INPUT_READY`
- `cal=pcnt-v1`
- `decoder=pcnt`
- `irq=pcnt`
- `poll_decoder=0`
- `ENC_PCNT_READY`
- `ENC_PCNT_HB`

PF0530V keeps GPIO13/GPIO14/GPIO32 input-only, LCD GPIO21/GPIO22 display-only,
and `FR_DIAG_XBEE_BRIDGE_CLOSED 1`. The live gate proved COM6 identity,
rollback, write-flash, separate verify-flash, reset/read-only readiness, idle
read-only PCNT/menu/render heartbeats, scan, and cleanup. After that gate, the
user stated `ENCODER FUNCTIONALITY CONFIRMED AND APPROVED BY USER`, accepting
PF0530V real LCD menu encoder functionality. The gate did not capture
post-confirmation transcript counts, so direction/counts-per-detent,
short/long select counts, and quantified runaway tolerance remain telemetry
characterization topics only.

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
