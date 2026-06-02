# Four Relay XBee Wi-Fi Firmware

This directory contains the project-local ESP-IDF firmware allowed by ADR-0002.
The current app is a permanent, minimal USB-to-XBee UART bridge for the
four-relay XBee lane. The reusable core remains tested on the host before any
ESP-IDF build or bench step.

## Verified facts

- ADR-0002 accepts ESP-IDF stable v6.0.1 for `four-relay-xbee-wifi` only.
  Source IDs: `SRC-ESP-IDF-STABLE-ESP32`, `SRC-ESP-IDF-GET-STARTED`.
- ESP-IDF stable v6.0.1 includes the APIs planned for Wi-Fi, HTTP server, GPIO,
  UART, NVS, FatFS/VFS, and SDSPI. Source IDs: `SRC-ESP-IDF-WIFI`,
  `SRC-ESP-IDF-HTTP-SERVER`, `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-UART`,
  `SRC-ESP-IDF-NVS`, `SRC-ESP-IDF-FATFS`, `SRC-ESP-IDF-SDSPI`.
- The selected XBee ports were previously programmed to API escaped mode and
  validated locally, then proven with a benign selected-port OTA `link_probe`
  exchange. Source IDs:
  `SRC-LOCAL-XBEE-SELECTED-PORT-PROGRAMMING-2026-05-29`,
  `SRC-LOCAL-XBEE-OTA-LINK-PROOF-2026-05-29`,
  `SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`,
  `SRC-DIGI-XBEE-900HP-BD-2026-05-29`, `SRC-DIGI-XBEE-900HP-NP`.
- ESP-IDF UART configuration and ESP32 GPIO routing are source-backed for this
  project; current hardware proof remains limited to the user-selected bridge
  gate. Source IDs: `SRC-ESP-IDF-UART`, `SRC-ESP-IDF-GPIO`,
  `SRC-ESP32-WROOM-32-DATASHEET`.
- ESP-IDF stable v6.0.1 documents the new I2C master driver API through
  `driver/i2c_master.h` and the `esp_driver_i2c` component. Source ID:
  `SRC-ESP-IDF-I2C`.
- The current bridge implementation and live-gate packet are recorded under
  source ID:
  `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`.
- The LCD-only firmware test adds display-status writes on I2C0 GPIO21/GPIO22
  while preserving the COM6 raw bridge behavior. Source ID:
  `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`.
- The encoder-menu firmware adds input-only reads on GPIO34/GPIO35/GPIO13 and
  keeps relay pages as locked UI text while preserving the COM6 bridge and LCD
  I2C paths. Source ID:
  `SRC-LOCAL-FOUR-RELAY-ENCODER-MENU-FIRMWARE-2026-05-30`.
- The encoder raw diagnostics build adds page-0 raw A/B/SW level display and
  A/B plus SW raw transition counters before any decoder or switch fix is
  selected. Source ID:
  `SRC-LOCAL-FOUR-RELAY-ENCODER-RAW-DIAGNOSTICS-2026-05-30`.
- The user-identified ASIN `B06XQTHDRR` is indexed by an independent Manuals+
  mirror as a Cylewet KY-040 rotary encoder module from Qianxin, with
  `CLK`, `DT`, `SW`, `+`, and `GND` pins, 20 pulses per rotation, and a
  typically active-low `SW` pin. This is selected-module evidence for this
  diagnostic lane, not bench acceptance of the exact module or wiring. Source
  ID: `SRC-MANUALSPLUS-CYLEWET-KY040-B06XQTHDRR`.
- The KY-040 GPIO13 diagnostic refactor keeps GPIO34/GPIO35 internal pulls
  disabled and enables the ESP32 internal pullup only on GPIO13 for the
  active-low `SW` input. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-DIAGNOSTIC-REFACTOR-2026-05-30`. The same source
  record now includes the same-session COM6 KY-040 diagnostic write/verify gate
  for user LCD testing.
- The KY-040 pin-finder diagnostic adds firmware ID `PF0530A` and an
  input-only pin-finder LCD page for GPIO34, GPIO35, GPIO13, GPIO14, GPIO32,
  and GPIO33 change counters. It keeps GPIO34/GPIO35 internal pulls disabled
  and keeps GPIO13 as the only internally pulled-up probe. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-PIN-FINDER-DIAGNOSTIC-2026-05-30`. The same
  source record now includes the COM6 `PF0530A` write/verify gate for user LCD
  testing.
- The KY-040 row-0 diagnostic refactor adds firmware ID `PF0530B` and cycles
  raw levels, raw transition counters, and GPIO34/GPIO35/GPIO13/GPIO14/
  GPIO32/GPIO33 live level/change-count diagnostics on LCD row 0 so the
  diagnostic does not require encoder navigation or lower LCD rows. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-ROW0-DIAGNOSTIC-2026-05-30`.
- The KY-040 GPIO sweep contact tracer adds firmware ID `PF0530C` after the
  user reported no displayed `PF0530B` pins changed. It locks the LCD to page
  0, shows row-0 `HIT` on any watched GPIO change, sweeps GPIO34/GPIO35/
  GPIO36/GPIO39/GPIO13/GPIO14/GPIO18/GPIO19/GPIO23/GPIO32, enables internal
  pullups only on GPIO13/GPIO14, and closes the diagnostic XBee bridge loop.
  Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-GPIO-SWEEP-CONTACT-TRACER-2026-05-30`. The same
  source record now includes the COM6 `PF0530C` write/verify gate for user LCD
  testing.
- The KY-040 DevKitC 13/14/32 diagnostic adds firmware ID `PF0530D` after the
  user confirmed the new wiring: `CLK` to GPIO13, `DT` to GPIO14, `SW` to
  GPIO32, and module `+` to ESP32 3V3 with a 100 nF capacitor across `+` and
  `GND`. It locks LCD page 0, shows raw `CLK`/`DT`/`SW` levels, transition
  counts, position/button counts, and per-pin `HIT` changes, enables internal
  pullups on GPIO13/GPIO14/GPIO32, and keeps the diagnostic XBee bridge loop
  closed. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-DEVKITC-13-14-32-DIAGNOSTIC-2026-05-30`. The
  same source record now includes the COM6 `PF0530D` write/verify gate for
  user LCD testing.
- The KY-040 serial pintrace diagnostic adds firmware ID `PF0530E` after the
  user reported the LCD diagnostics still did not expose a changing pin. It
  disables the LCD-dependent diagnostic path, prints live GPIO change events on
  COM6/UART0 at 115200, monitors common DevKitC candidate GPIOs as input-only,
  enables internal pullups only on GPIO13/GPIO14/GPIO32, warns that DevKitC
  physical `J2-13` is `IO12` and `J2-14` is `GND`, and keeps the diagnostic
  XBee bridge loop closed. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30`.
- The final PF0530E r4 monitor completed without watchdog/backtrace output and
  without encoder-pin `EV` events. User-confirmed physical encoder actuation
  during that monitor remains unproven. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30`.
- A later PF0530E r5 read-only monitor recorded user-confirmed encoder
  actuation with GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` changing on COM6,
  `writes_sent=false`, and no watchdog/panic/backtrace scan hits. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30`.
- The PF0530F repo-only menu-proof refactor changes the current firmware ID to
  `PF0530F`, boots the LCD encoder menu path instead of the PF0530E serial
  pintrace task, keeps `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, configures GPIO13
  `CLK`, GPIO14 `DT`, and GPIO32 `SW` input-only with internal pullups, and
  emits concise `printf` proof events for boot, encoder levels, menu steps,
  button selects, suppressed A/B motion, invalid quadrature jumps, and
  heartbeats. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-2026-05-30`.
- The later PF0530F COM6 live attempt flashed and separately verify-flashed
  PF0530F, captured `PF0530F MENU_READY`, then captured `PF0530F
  LCD_INIT_FAILED` with no `MENU_HB`, `MENU_STEP`, or `MENU_SELECT` proof.
  Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-LIVE-2026-05-30`.
- The PF0530G LCD init diagnostic changes the current firmware ID to
  `PF0530G`, keeps `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, uses GPIO21/GPIO22 I2C
  only, and emits stage-specific `LCD_DIAG_READY`, `LCD_BUS`, `LCD_PROBE`,
  `LCD_PROBE_SUMMARY`, `LCD_DEVICE`, `LCD_HD44780`, `LCD_INIT_OK` or
  `LCD_INIT_FAIL`, and `LCD_DIAG_HB` proof lines before any renewed menu
  proof. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-LCD-INIT-DIAG-PF0530G-2026-05-30`.
- The PF0530G COM6 live gate passed serial LCD init diagnosis: COM6 identity
  matched ESP32-D0WDQ6 MAC `<redacted-mac>`, write-flash and separate
  verify-flash succeeded, and the read-only monitor captured one LCD ACK at
  `0x27`, `LCD_INIT_OK addr=0x27`, and 15 `LCD_DIAG_HB status=ok` lines with
  no crash or closed-surface violation markers. Evidence directory:
  `<redacted-local-evidence-path>`.
- The PF0530H source image combines the PF0530G detailed LCD init/probe path
  with the PF0530F GPIO13/GPIO14/GPIO32 encoder menu loop, changes the active
  task to a nine-page static BBS LCD console, and emits `PF0530H
  BBS_LCD_READY`, `BBS_LCD_RENDER`, `BBS_MENU_HB`, `BBS_MENU_STEP`, and
  `BBS_MENU_SELECT` proof lines. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-2026-05-31`.
- The PF0530H COM6 live gate passed fresh identity, full 4 MB rollback backup,
  write-flash, separate verify-flash, and read-only UART0 monitor. The
  transcript captured `LCD_INIT_OK addr=0x27`, `PF0530H BBS_LCD_READY`, three
  `BBS_LCD_RENDER`, three `BBS_MENU_HB`, and no crash/fault or closed-surface
  markers. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-LIVE-2026-05-31`.
- The PF0530H image was not accepted as an interactive menu after user testing
  reported no encoder/button LCD effect; its proof had zero `BBS_MENU_STEP`
  and zero `BBS_MENU_SELECT` lines. PF0530I changes the active firmware ID to
  `PF0530I`, splits input polling into `fr_menu_input_task`, keeps
  GPIO13/GPIO14/GPIO32 input-only with pullups, keeps XBee and relay surfaces
  closed, renders only dirty LCD rows or a slow idle refresh, emits
  `BBS_INPUT_READY`, emits `ENC_RAW`, and adds `rows`, `seq`, `dur_ms`, and
  `reason` to `BBS_LCD_RENDER`. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530I-2026-05-31`.
- PF0530I live monitor showed repeated task-watchdog backtrace lines after the
  split input task. PF0530J keeps the split input/render design, changes
  `FR_MENU_POLL_MS` to 10, and uses `fr_delay_ticks_at_least_one()` so the
  higher-priority input task yields for at least one FreeRTOS tick. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530J-2026-05-31`.
- The first PF0530J read-only monitor passed the watchdog/crash side of the
  gate but captured no GPIO13/GPIO14/GPIO32 input transitions. PF0530K keeps
  the one-tick delay fix, adds GPIO any-edge interrupt queueing for the KY-040
  lines, decodes rotation from raw A/B transitions, and emits
  `BBS_INPUT_READY ... irq=anyedge queue=64` plus `irq_drop` heartbeat proof.
  Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530K-2026-05-31`.
- PF0530K was written and separately verify-flashed to COM6. Its read-only
  monitor captured `PF0530K BBS_LCD_READY`, `BBS_INPUT_READY`, `irq=anyedge
  queue=64`, two `BBS_LCD_RENDER`, and 59 `BBS_MENU_HB` lines with no
  watchdog/backtrace/panic/LCD-init-failure markers, but zero `ENC_RAW`,
  `ENC_EV`, `BBS_MENU_STEP`, or `BBS_MENU_SELECT` lines. PF0530K is flashed
  for user testing but not accepted as proven interactive until physical
  actuation is captured. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530K-LIVE-2026-05-31`.
- PF0530L became the accepted flashed image for the live LCD menu UX test. It
  keeps the PF0530K interrupt input queue, adds four local UI modes
  `page_browse`/`row_browse`/`detail`/`edit_lab`, software cursor/DDRAM
  tracking, dirty-cell metadata, five named eight-slot glyph banks, custom
  bar/chart/digit/gauge demo pages, and a seven-second auto-demo page cycle so
  the full menu surface is visible before encoder interaction is proven.
  Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530L-2026-05-31`.
- PF0530L was written and separately verify-flashed to COM6. Its read-only
  monitor captured `PF0530L BBS_LCD_READY`, `BBS_INPUT_READY`, `LCD_INIT_OK`,
  six `BBS_GLYPH_BANK`, 77 `BBS_CURSOR`, 77 `BBS_LCD_RENDER`, 21
  `BBS_MENU_AUTO`, and 74 `BBS_MENU_HB` lines with all 13 page names and all
  five glyph banks covered, no watchdog/backtrace/panic/LCD-init-failure or
  unsafe-open scan hits, and zero `ENC_RAW`, `ENC_EV`, `BBS_MENU_STEP`, or
  `BBS_MENU_SELECT` lines. PF0530L is flashed for user visual testing but not
  accepted as proven physically interactive until actuation is captured. Source
  ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530L-LIVE-2026-05-31`.
- PF0530M is a non-live source/test continuation after PF0530L LCD visual and
  electrical acceptance. It keeps the same closed bridge and input-only GPIO
  boundary, changes the active firmware ID to `PF0530M`, replaces demo-only
  labels with operational status rows, adds local bridge-closed display,
  diagnostic/error rows, row action labels, and editable widget rows, and
  extends host-side LCD menu tests for page wrapping, glyph-bank selection,
  selection/detail/edit behavior, and 20-character display bounds. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530M-2026-06-01`.
- PF0530N is the LCD/menu scrolling/XML source/test continuation. It keeps the
  closed bridge, GPIO13/GPIO14/GPIO32 input-only, and GPIO21/GPIO22
  display-only LCD boundaries, changes the active firmware ID to `PF0530N`,
  adds build-time `bbs_lcd_menu.v1` XML, generated static firmware/simulator
  menu definitions, `bbs_lcd_render.v2` host metadata, scroll-list item
  navigation, grouped multi-row items, selected-row marquee timing, and a
  separate table glyph bank. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530N-SCROLLING-XML-2026-06-01`.
- PF0530N was written and separately verify-flashed to COM6. Its read-only
  monitor captured `PF0530N BBS_LCD_READY`, `PF0530N BBS_INPUT_READY`,
  `bbs_lcd_menu.v1`, `bbs_lcd_render.v2`, 61 `BBS_LCD_RENDER`, 61
  `BBS_CURSOR`, 59 `BBS_MENU_HB`, 17 `BBS_MENU_AUTO`, and seven
  `BBS_GLYPH_BANK` lines with no watchdog/backtrace/panic/LCD-init-failure or
  unsafe-open markers. Physical scroll-list/table readability and physical
  encoder/button input remain unproven. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530N-LIVE-2026-06-01`.
- PF0530O is the prior flashed real-menu calibration source/build continuation. It
  keeps GPIO13/GPIO14/GPIO32 input-only, keeps GPIO21/GPIO22 display-only LCD
  boundaries, changes the active firmware ID to `PF0530O`, decodes quadrature
  on stable-level acceptance, uses one transition per menu step, two AB stable
  samples, a 75 ms switch guard, a 650 ms long press, disables boot auto-cycle,
  and reports `cal=real-menu-v1`. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530O-REAL-MENU-CAL-2026-06-01`.
- PF0530O was written and separately verify-flashed to COM6. Its reset and
  attended read-only monitors captured `PF0530O BBS_LCD_READY`,
  `PF0530O BBS_INPUT_READY`, `LCD_INIT_OK addr=0x27`, `auto_cycle=off`,
  repeated `BBS_LCD_RENDER` and `BBS_MENU_HB` output, no crash/unsafe markers,
  and zero `ENC_RAW`, `ENC_EV`, `BBS_MENU_STEP`, or `BBS_MENU_SELECT` lines.
  User visual/input acceptance remains pending. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530O-LIVE-2026-06-01`.
- PF0530P is the previous debounce calibration source/build
  continuation. It keeps GPIO13/GPIO14/GPIO32 input-only, keeps GPIO21/GPIO22
  display-only LCD boundaries, changes the active firmware ID to `PF0530P`,
  keeps one transition per menu step and two AB stable samples, adds a 5 ms
  A/B candidate hold, adds a 40 ms step lockout, keeps 30 ms switch debounce,
  a 75 ms switch guard, and a 650 ms long press, and reports
  `cal=debounce-v2 ab_ms=5 step_lockout_ms=40`. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530P-DEBOUNCE-CAL-2026-06-01`.
- PF0530P was written and separately verify-flashed to COM6. Its reset and
  attended read-only monitors captured `PF0530P BBS_LCD_READY`,
  `PF0530P BBS_INPUT_READY`, `LCD_INIT_OK addr=0x27`,
  `cal=debounce-v2`, `ab_ms=5`, `step_lockout_ms=40`, repeated
  `BBS_LCD_RENDER` and `BBS_MENU_HB` output, no crash/unsafe markers, and zero
  `ENC_RAW`, `ENC_EV`, `BBS_MENU_STEP`, `BBS_MENU_SELECT`, or `ENC_FILTER`
  lines. User visual/input acceptance remains pending. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530P-LIVE-2026-06-01`.
- PF0530Q is the previous quiet-window calibration source/build continuation
  after the user clarified they did not rotate during the PF0530P monitor. It
  keeps GPIO13/GPIO14/GPIO32 input-only, keeps GPIO21/GPIO22 display-only LCD
  boundaries, changes the active firmware ID to `PF0530Q`, keeps one
  transition per menu step, two AB stable samples, a 5 ms A/B candidate hold,
  30 ms switch debounce, 75 ms switch guard, and 650 ms long press, adds a
  combined A/B pair quiet window of 10 ms, raises step lockout to 60 ms, and
  reports `cal=quiet-v3 ab_ms=5 quiet_ms=10 step_lockout_ms=60`. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530Q-QUIET-CAL-2026-06-01`.
- PF0530Q was written and separately verify-flashed to COM6. Its reset boot and
  idle read-only monitors captured `PF0530Q BBS_LCD_READY`,
  `PF0530Q BBS_INPUT_READY`, `LCD_INIT_OK addr=0x27`, `cal=quiet-v3`,
  `ab_ms=5`, `quiet_ms=10`, `step_lockout_ms=60`, repeated
  `BBS_LCD_RENDER` and `BBS_MENU_HB` output, no crash/unsafe markers, zero bad
  render rows, and zero input events with no physical actuation expected.
  Physical input acceptance remains pending; the later user report says the
  menu works but is not stable. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530Q-LIVE-2026-06-01`.
- PF0530R is the previous detent-gated calibration source/build continuation.
  It keeps GPIO13/GPIO14/GPIO32 input-only, keeps GPIO21/GPIO22 display-only
  LCD boundaries, changes the active firmware ID to `PF0530R`, raises A/B
  candidate hold to 8 ms, raises combined A/B quiet time to 15 ms, changes
  `FR_ENCODER_TRANSITIONS_PER_STEP` to 2, raises step lockout to 90 ms, emits
  at most one menu step only when accepted quadrature returns to detent A/B
  `3`, and reports
  `cal=detent-v4 ab_ms=8 quiet_ms=15 step_lockout_ms=90 detent=3`. PF0530R
  is now written and separately verify-flashed on COM6 with readiness/render
  proof, zero crash/unsafe markers, zero bad render rows, and cleanup proof.
  The attended monitor captured zero input events, so physical input
  acceptance remains open. Source IDs:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530R-DETENT-CAL-2026-06-01`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530R-LIVE-2026-06-01`.
- PF0530S is the accepted written/verify-flashed raw-liveness recovery after
  PF0530R captured zero input event lines. It keeps GPIO13/GPIO14/GPIO32
  input-only, keeps GPIO21/GPIO22 display-only LCD boundaries, changes the
  active firmware ID to `PF0530S`, uses 3 ms A/B debounce, 0 ms quiet time, one
  transition per step, and 45 ms step lockout, and does not require return to
  detent A/B `3` before emitting a step. It adds `ENC_BASE`,
  `ENC_GPIO_CONFIG`, ESP-IDF GPIO config dump, one-second `ENC_LEVEL_HB`, and
  raw/ISR/queue/poll counters in `BBS_MENU_HB`, and reports
  `cal=raw-live-v5 ab_ms=3 quiet_ms=0 step_lockout_ms=45`, plus
  `raw_hb_ms=1000 gpio_cfg=1 poll_raw=1`. PF0530S COM6 live proof recovered
  raw A/B and switch liveness, both menu directions, short and long selects,
  and LCD/menu response, but full rotary stability remains open due to
  invalid/suppressed transitions and queue drops. Source IDs:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530S-RAW-LIVENESS-CAL-2026-06-01`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530S-LIVE-2026-06-01`.
- PF0530T is the historical responsive source/build recovery after PF0530S proved
  raw liveness but left stability open. It keeps GPIO13/GPIO14/GPIO32
  input-only and GPIO21/GPIO22 display-only, changes the active firmware ID to
  `PF0530T`, makes polling authoritative at 2 ms, disables interrupt-fed
  decoding and per-edge raw serial logging, uses one A/B stable sample, 1 ms
  A/B hold, 0 ms quiet time, two transitions per detent-gated step, 25 ms step
  lockout, 25 ms switch guard, and reports `cal=responsive-v6`,
  `detent_gate=1`, `raw_log=0`, and `poll_decoder=1`. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530T-RESPONSIVE-2026-06-02`.
- PF0530U is the previous written/verify-flashed responsive-v7 continuation after PF0530T restored raw
  input and select proof but emitted too few rotation steps for a usable menu.
  It keeps the same closed GPIO/LCD surfaces, polling-authoritative decoder,
  detent gate, raw edge logging disabled, and 25 ms step lockout, changes the
  active firmware ID to `PF0530U`, changes the detent-return step threshold to
  one transition, and reports `cal=responsive-v7`. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530U-RESPONSIVE-V7-2026-06-02`.
- PF0530V is the previous accepted written/verify-flashed PCNT continuation
  after PF0530U was written and verify-flashed but post-flash monitors captured
  no physical input events. It keeps GPIO13/GPIO14/GPIO32 input-only and
  GPIO21/GPIO22 display-only, changed the firmware ID to `PF0530V`, declares
  `esp_driver_pcnt`, uses ESP-IDF PCNT quadrature counting on GPIO13/GPIO14,
  keeps the switch path poll/debounce based with a 40 ms guard, and reports
  `cal=pcnt-v1`, `decoder=pcnt`, `irq=pcnt`, and `poll_decoder=0`. PF0530V
  COM6 identity, rollback, write-flash, separate verify-flash, reset/read-only
  readiness monitor, idle read-only monitor, scan, and cleanup proof passed.
  The user later stated `ENCODER FUNCTIONALITY CONFIRMED AND APPROVED BY USER`,
  accepting PF0530V real LCD menu encoder functionality. Post-confirmation
  transcript-count characterization remains open. Source IDs:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-PCNT-SOURCE-BUILD-2026-06-02`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-LIVE-2026-06-02`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-USER-ACCEPTANCE-2026-06-02`.
- PF0530W is the active written/verify-flashed firmware-visible LCD visual-art
  continuation. It preserves the PF0530V PCNT encoder path, input-only
  GPIO13/GPIO14/GPIO32 policy, display-only GPIO21/GPIO22 LCD policy, and
  closed bridge/relay/load/mains boundaries while adding a generated `ART`
  page, seventh `art_panel` glyph bank, and fixed 4x20 custom-character tile
  map. COM6 identity, rollback, write-flash, separate verify-flash, read-only
  PF0530W readiness monitor, transcript scan, and cleanup proof passed; physical
  ART page visual acceptance remains pending. Source IDs:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-VISUAL-ART-2026-06-02`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-LIVE-2026-06-02`.

## Assumptions

- `safe_core` stays pure C so it can be compiled by host tests without ESP-IDF
  tools.
- The normal bridge image initializes in-memory safe-core defaults, configures
  UART0 for host USB serial at `115200 8N1`, configures UART2 for XBee DIN/DOUT
  at `9600 8N1` on GPIO17/GPIO16, and copies raw bytes in both directions. The
  current `PF0530W` source image sets `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, so it
  runs LCD init diagnosis and local BBS menu display without running the UART
  bridge loop; PF0530P, PF0530Q, PF0530R, and PF0530S are written and
  verify-flashed on COM6 with read-only LCD readiness proof. PF0530Q has a
  user report of working but unstable physical interaction, PF0530R physical
  input acceptance stayed open because its 150 second attended monitor captured
  zero input events, and PF0530S recovered raw input/menu/select liveness while
  leaving full rotary stability open. PF0530U is the previous written and
  verify-flashed responsive-v7 image with post-flash actuation proof pending.
  PF0530V is the previous accepted PCNT image with user-confirmed encoder/LCD
  menu functionality; transcript-count characterization remains open. PF0530W
  is the active written/verify-flashed visual-art image with readiness proof
  passed; physical ART page visual acceptance remains pending.
- The bridge does not parse, generate, or persist XBee setting writes. In
  `PF0530G`, it does not forward host or XBee bytes at runtime.
- The LCD path assumes one HD44780-compatible 20x4 LCD backpack using a
  PCF8574/PCF8574A-class expander, GPIO21 SDA, GPIO22 SCL, a level shifter,
  common ground, external pullups through the LCD/level-shifter path, and the
  common P0=RS/P1=RW/P2=E/P3=backlight/P4-P7=data mapping. PF0530G serial
  diagnosis detected exactly one candidate at `0x27` and completed HD44780
  initialization.
- The encoder menu assumes the KY-040 module is tested in the ESP32 3.3 V
  logic domain with `+` tied to 3V3, not 5 V. The historical `PF0530F`
  diagnostic wiring mapped KY-040 `CLK` to GPIO13, `DT` to GPIO14, `SW` to
  GPIO32, and `GND` to ESP32 GND, following the module silkscreen rather than
  physical pin order. GPIO13/GPIO14/GPIO32 use ESP32 internal pullups for this
  menu-proof branch. PF0530S is the accepted raw-liveness LCD menu UX image after
  PF0530H showed no user-visible encoder/button effect, PF0530I showed
  task-watchdog backtraces, PF0530J showed no input-transition proof, and
  PF0530K flashed cleanly but captured no input events. PF0530L later accepted
  physical serial/menu interaction and LCD visual/glyph/electrical behavior;
  PF0530M added operational non-live menu behavior; PF0530N added build-time
  XML, scroll-list navigation, v2 host metadata, and table formatting;
  PF0530O adds real-menu calibration with COM6 flash/verify and read-only boot
  proof; PF0530P adds debounce/step-lockout calibration; PF0530Q adds
  quiet-window calibration and was later reported as working but unstable;
  PF0530R adds detent-gated decoding with COM6 write/verify/readiness proof;
  PF0530S adds raw-liveness heartbeats and COM6 attended proof of raw
  input/menu/select response; PF0530T/PF0530U record responsive polling
  follow-ups; PF0530V is the accepted PCNT encoder baseline; and PF0530W is
  the current visual-art image pending physical ART-page acceptance.
- The encoder diagnostics path assumes page-0 raw levels and transition
  counters are used only to decide the next branch: hardware/electrical gap,
  switch polarity/debounce fix, quadrature decoder fix, or acceptance cleanup.
- The pin-finder and contact-tracer diagnostics assume GPIO observations are
  temporary input-only clues for mislanded wires; a changing counter is a clue
  for continuity review, not accepted wiring evidence by itself.
- Future ESP-IDF work must preserve the relay manager and safety supervisor as
  the only path to relay state changes.

## Unknowns

- The named COM6 bridge flash/retest gate recorded same-session UART
  rail/common-ground, DIN/DOUT direction, antenna, and relay/load/mains
  isolation confirmation. Measured rail-current margin for broader hardware
  expansion remains unresolved.
- Board/shield power, relay input polarity/current, MicroSD wiring, TFT wiring,
  mux wiring, expander wiring, and load/enclosure evidence remain blocked.
- Exact LCD module, backpack IC, pullup voltage, logic voltage, contrast
  setting, backlight current, rail-current margin, bus-sharing conflicts, and
  physical LCD visual state remain unresolved. PF0530G serial diagnosis found
  one I2C candidate at `0x27` and completed the LCD init/write path.
- Exact bench module markings, onboard pullup values and voltage, rail-current
  impact, switch bounce behavior, rotation direction, boot behavior, and
  continuity from KY-040 `CLK`/`DT`/`SW` to GPIO34/GPIO35/GPIO13 remain
  unresolved after the COM6 KY-040 diagnostic write/verify gate.
- User observation after the GPIO13 raw diagnostic flash says the raw page is
  visible but `A/B/SW`, `ABCHG`, and `SWCHG` do not change. Treat that as a
  hardware/electrical/pinout failure first, not a decoder failure. A fresh LCD
  raw observation is pending after the KY-040 GPIO13-pullup diagnostic flash.
- The `PF0530A` pin-finder diagnostic image was written/verified to COM6, and
  the user reported only pin 34 was displayed. The `PF0530B` row-0 diagnostic
  image was later written/verified to COM6, and the user reported no displayed
  pins changed. The `PF0530C` contact-tracer image and `PF0530D` DevKitC
  13/14/32 LCD image were written/verified to COM6. `PF0530E` r5 proved
  GPIO-level input changes on GPIO13/GPIO14/GPIO32, and `PF0530F` is the
  menu-proof image prepared from that evidence. PF0530F flash/verify passed on
  COM6, but live menu proof is blocked by `PF0530F LCD_INIT_FAILED`; final
  hardware acceptance remains open. PF0530G serial LCD init diagnosis later
  passed at address `0x27`; PF0530H COM6 flash/verify and read-only monitor
  passed with BBS ready/render/heartbeat proof but zero step/select proof.
  PF0530I is the source fix for render-starved input polling, PF0530J fixes
  the PF0530I task-watchdog delay issue, PF0530K adds interrupt-queued GPIO
  input capture, PF0530L adds the source-level LCD menu UX/glyph/browser-plan
  visual surface, PF0530M adds non-live operational menu behavior plus
  host-side state-machine tests, and PF0530N adds non-live XML-generated
  scroll-list/table menu behavior. PF0530O then adds real-menu calibration plus
  COM6 write/verify/read-only monitor proof; PF0530P/PF0530Q continue the
  debounce/quiet-window calibration lineage; PF0530R is the prior
  written/verify-flashed image with readiness proof; PF0530S is the accepted
  written/verify-flashed raw-liveness image with live input/menu/select proof
  and stability still open; PF0530U is a previous written/verify-flashed
  responsive-v7 image with post-flash actuation proof pending; PF0530V is the
  accepted PCNT encoder baseline with readiness proof passed and
  user-confirmed encoder/LCD menu functionality accepted while transcript-count
  characterization remains open; and PF0530W is the current visual-art image
  pending physical ART-page acceptance.
- Final FreeRTOS task layout, pins, authentication, telemetry cadence, storage
  policy, and rollback behavior are unresolved.

## Hard gates

- No GPIO writes to relay pins.
- Encoder GPIO reads are allowed only for this input-only menu/diagnostic work
  in `main/main.c`; `PF0530F` watches GPIO13/GPIO14/GPIO32 as input-only GPIOs
  and enables internal pullups only on those three encoder lines. Firmware
  must keep these inputs input-only and must not write relay GPIO levels.
- No expander writes to relay hardware.
- UART bridge writes are allowed only for the normal bridge feature and only in
  `main/main.c`; they are raw UART0 to UART2 copies, not relay or XBee setting
  writes. PF0530F closes that loop with `FR_DIAG_XBEE_BRIDGE_CLOSED 1`.
- LCD I2C writes are allowed only for this display-only menu feature and only
  in `main/main.c`; they may probe PCF8574/PCF8574A candidate address ranges
  and write status/menu text to one detected LCD backpack, not relay expander
  outputs.
- No XBee setting writes, `WR`, `AC`, or `KY` are embedded in firmware.
- No flash or monitor step in automated validation.
- No live bench mutation outside accepted named gates. The encoder menu gate,
  KY-040 diagnostic gate, PF0530A pin-finder gate, PF0530B row-0 gate, PF0530C
  contact-tracer gate, and PF0530D DevKitC 13/14/32 diagnostic gate have
  completed COM6-only write/verify. PF0530E r5 completed its named read-only
  serial monitor with user-confirmed GPIO13/GPIO14/GPIO32 input changes.
  PF0530F completed its named COM6 write/verify gate, but the read-only monitor
  blocked live menu acceptance on `PF0530F LCD_INIT_FAILED`. PF0530G completed
  the separately authorized LCD init diagnostic gate with `LCD_INIT_OK
  addr=0x27`. PF0530H completed the named COM6 BBS LCD menu flash/verify and
  read-only monitor gate, but user testing reported no encoder/button LCD
  effect. PF0530I then showed task-watchdog backtraces, PF0530J showed no
  input-transition proof, PF0530K captured no input events after clean
  flash/verify, PF0530L became the accepted LCD visual/electrical image,
  PF0530M remained source/test-only, PF0530N added the non-live scrolling/XML
  source/test branch, PF0530O flashed but captured zero input events, PF0530P
  is written/verify-flashed with LCD readiness proof but zero captured input
  events, PF0530Q is written/verify-flashed with LCD readiness proof and a
  user report of working but unstable behavior, PF0530R is written/
  verify-flashed with readiness proof but zero captured input events, and
  PF0530S is the accepted raw-liveness recovery image with live input/menu/select
  proof and stability still open, PF0530U is a previous written/verify-flashed
  responsive-v7 image with post-flash actuation proof pending, PF0530V is the
  accepted PCNT encoder baseline, and PF0530W is the current visual-art image
  pending physical ART-page acceptance. Any further flash, monitor,
  direct-stimulus continuity test, RF, relay, load, or mains action outside
  that named gate needs a separate fresh gate.

## Layout

- `CMakeLists.txt` and `main/` form the minimal ESP-IDF project shell.
- `main/main.c` is the bridge app when the bridge loop is open: UART0 host
  `115200`, UART2 XBee `9600`, TX GPIO17 to XBee DIN, RX GPIO16 from XBee DOUT,
- no flow control, and no app logging during bridge operation. The current
  PF0530W BBS LCD menu source closes that bridge loop, preserves the PF0530V
  PCNT encoder baseline on GPIO13/GPIO14/GPIO32, runs LCD output on
  GPIO21/GPIO22, adds the generated `ART` page plus the `art_panel` glyph bank,
  renders XML-generated local BBS status, bridge, error, widget, route table,
  and visual-art pages with dirty-cell LCD updates, loads named HD44780 glyph
  banks, tracks cursor/DDRAM metadata, supports scroll-list/detail/edit local
  UI modes, and keeps auto-demo page cycling disabled at boot. It
  consumes generated static menu definitions rather than parsing XML at
  runtime. It prints
  `LCD_DIAG_READY`, `LCD_BUS`,
  `LCD_PROBE`, `LCD_PROBE_SUMMARY`, `LCD_DEVICE`, `LCD_HD44780`,
  `LCD_INIT_OK` or `LCD_INIT_FAIL`, `PF0530W BBS_LCD_READY`,
  `PF0530W BBS_INPUT_READY`, `ENC_BASE`, `ENC_GPIO_CONFIG`, `ENC_LEVEL_HB`,
  `ENC_PCNT_READY`, `ENC_PCNT_HB`, `BBS_GLYPH_BANK`,
  `BBS_CURSOR`, `BBS_LCD_RENDER`, `BBS_MENU_HB`, `ENC_FILTER`,
  `BBS_MENU_AUTO_CYCLE`, `BBS_MENU_STEP`, and
  `BBS_MENU_SELECT` proof lines on UART0 when the corresponding local event
  occurs.
- `components/safe_core/` contains host-testable state, safety, config, API,
  storage, pure-C API payload validation, normalized state snapshots, and XBee
  frame logic.
- Public relay channels are `1..4`; `safe_core` maps those public numbers to
  zero-based internal relay-state indexes before touching desired-state arrays.
  Source ID: `SRC-LOCAL-FOUR-RELAY-SAFE-CORE-CONTRACT-2026-05-19`.
- `tests/four_relay_safe_core/` compiles split host-test binaries for relay and
  safety gates, HTTP/API contracts, storage contracts, and the XBee frame codec.
