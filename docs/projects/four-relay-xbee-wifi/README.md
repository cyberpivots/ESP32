# Four Relay XBee Wi-Fi Controller

## Goal

Design the first ESP32 project package around the photographed hardware: an
ESP-WROOM-32 development board on an ESP32 I/O expansion shield, a four-channel
Songle relay module candidate, local Wi-Fi control, and Digi XBee-PRO 900HP S3B
telemetry/control over the photographed `XBP9B-DPUT-001 RevF` radio.

## Package map

- [Build guide](build-guide.md)
- [Architecture](architecture.md)
- [Prototype Build Packet](prototype-build-packet.md)
- [Prototype blueprint](prototype-blueprint.md)
- [Bench bring-up runbook](bench-bring-up-runbook.md)
- [XBee public boundary](xbee-public-boundary.md)
- [XBee read-only bench proof](xbee-read-only-bench-proof.md)
- [Hardware and circuit improvement research](hardware-circuit-improvement-research.md)
- [R&D loop](rd-loop.md)
- [Mains readiness gate](mains-readiness-gate.md)
- [Power and safety gates](power-and-safety.md)
- [Pin plan](pin-plan.md)
- [Rotary encoder menu plan](rotary-encoder-menu-plan.md)
- [ESP-NOW BBS LCD/encoder field console plan](../espnow-bbs/lcd-encoder-field-console-plan.md)
- [ESP-NOW BBS LCD menu graphics/browser/agent plan](../espnow-bbs/lcd-menu-graphics-browser-agent-plan.md)
- [TFT and relay expansion](tft-relay-expansion.md)
- [Firmware task model](firmware-task-model.md)
- [Web interface](web-interface.md)
- [Static admin HMI](ui/index.html)
- [SPI MicroSD reader profile](../../../hardware-profiles/storage/spi-microsd-reader/README.md)
- [SPI MicroSD assets and logs ledger](../../../knowledge-base/source-ledger/2026-05-18-spi-microsd-assets-logs.md)
- [Hardware and circuit improvement ledger](../../../knowledge-base/source-ledger/2026-05-19-four-relay-hardware-circuit-improvement.md)
- [Open-Smart R61509V TFT planning profile](../../../hardware-profiles/displays/open-smart-r61509v/README.md)
- [CD74HC4067 analog mux profile](../../../hardware-profiles/interface-expansion/cd74hc4067/README.md)
- [TCA9555/MCP23017 GPIO expander profile](../../../hardware-profiles/interface-expansion/tca9555-mcp23017/README.md)
- [TPIC6B595 relay driver reference profile](../../../hardware-profiles/interface-expansion/tpic6b595/README.md)

## Verified facts

- ESP-IDF stable v6.0.1 is the project framework target accepted by ADR-0002.
  Source IDs: `SRC-ESP-IDF-STABLE-ESP32`, `SRC-ESP-IDF-GET-STARTED`.
- ESP-IDF stable documentation covers Wi-Fi AP mode, HTTP server URI handlers,
  GPIO/GPIO matrix, UART controllers, NVS storage, FatFS/VFS, and SDSPI
  storage for the required project surfaces. Source IDs: `SRC-ESP-IDF-WIFI`,
  `SRC-ESP-IDF-HTTP-SERVER`, `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-UART`,
  `SRC-ESP-IDF-NVS`, `SRC-ESP-IDF-FATFS`, `SRC-ESP-IDF-SDSPI`.
- ESP-IDF stable v6.0.1 documents the I2C master driver API and
  `esp_driver_i2c` component used for the bounded 20x4 LCD display-status test.
  Source ID: `SRC-ESP-IDF-I2C`.
- ESP-IDF GPIO source coverage and the local encoder-menu firmware record
  bound GPIO34/GPIO35/GPIO13 to input-only LCD menu reads while relay pages
  remain locked UI text only. Source IDs: `SRC-ESP-IDF-GPIO`,
  `SRC-LOCAL-FOUR-RELAY-ENCODER-MENU-FIRMWARE-2026-05-30`.
- The encoder raw diagnostics record adds LCD page-0 raw A/B/SW levels and
  raw A/B plus SW transition counters for the reported encoder nonresponse.
  Source ID: `SRC-LOCAL-FOUR-RELAY-ENCODER-RAW-DIAGNOSTICS-2026-05-30`.
- The user-identified ASIN `B06XQTHDRR` is indexed by an independent Manuals+
  mirror as a Cylewet KY-040 rotary encoder module from Qianxin, with
  `CLK`, `DT`, `SW`, `+`, and `GND` pins, 20 pulses per rotation, and a
  typically active-low `SW` pin. This is selected-module evidence for the
  current diagnostic lane; exact bench wiring and module electrical behavior
  remain unaccepted. Source ID:
  `SRC-MANUALSPLUS-CYLEWET-KY040-B06XQTHDRR`.
- The KY-040 diagnostic refactor preserves the bridge, LCD path, raw page, and
  locked relay UI text while enabling only the GPIO13 internal pullup for
  `SW`; GPIO34/GPIO35 remain internal-pull disabled. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-DIAGNOSTIC-REFACTOR-2026-05-30`. The same source
  record now includes the same-session COM6 KY-040 diagnostic write/verify gate
  for user LCD testing.
- The KY-040 pin-finder diagnostic keeps the raw page and adds firmware ID
  `PF0530A` plus an input-only LCD pin-finder page for GPIO34, GPIO35, GPIO13,
  GPIO14, GPIO32, and GPIO33 live levels and change counts. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-PIN-FINDER-DIAGNOSTIC-2026-05-30`. The same
  source record now includes the COM6 `PF0530A` write/verify gate for user LCD
  testing.
- The KY-040 row-0 diagnostic refactor adds firmware ID `PF0530B` and makes
  LCD row 0 auto-cycle through raw A/B/SW, raw A/B and SW transition counts,
  and each GPIO34/GPIO35/GPIO13/GPIO14/GPIO32/GPIO33 level/change-count view
  so troubleshooting does not require encoder navigation or lower LCD rows.
  Source ID: `SRC-LOCAL-FOUR-RELAY-KY040-ROW0-DIAGNOSTIC-2026-05-30`.
- The KY-040 GPIO sweep contact tracer adds firmware ID `PF0530C` after the
  user reported no displayed `PF0530B` pins changed. It locks the LCD to page
  0, shows row-0 `HIT` on any watched GPIO change, sweeps GPIO34/GPIO35/
  GPIO36/GPIO39/GPIO13/GPIO14/GPIO18/GPIO19/GPIO23/GPIO32, enables internal
  pullups only on GPIO13/GPIO14, excludes flash/LCD/UART0/XBee/strapping-risk/
  relay-candidate pins, and closes the diagnostic XBee bridge loop. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-GPIO-SWEEP-CONTACT-TRACER-2026-05-30`. The same
  source record now includes the COM6 `PF0530C` write/verify gate for user LCD
  testing.
- The KY-040 DevKitC 13/14/32 diagnostic adds firmware ID `PF0530D` after the
  user confirmed `CLK` on GPIO13, `DT` on GPIO14, `SW` on GPIO32, module `+`
  on ESP32 3V3, and a 100 nF capacitor across `+` and `GND`. It locks LCD page
  0, enables internal pullups on GPIO13/GPIO14/GPIO32, shows raw levels and
  transition/position/button counts, and keeps the diagnostic XBee bridge
  closed. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-DEVKITC-13-14-32-DIAGNOSTIC-2026-05-30`. The
  same source record now includes the COM6 `PF0530D` write/verify gate for
  user LCD testing.
- The KY-040 serial pintrace diagnostic adds firmware ID `PF0530E` after the
  LCD-only diagnostics still produced no useful live pin-change evidence. It
  prints live stable GPIO change events and periodic summaries on COM6/UART0,
  watches a DevKitC candidate set as input-only GPIOs, enables internal pullups
  only on GPIO13/GPIO14/GPIO32, and records the DevKitC header-position risk
  that `J2-13` is `IO12` and `J2-14` is `GND`, not `IO13`/`IO14`. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30`.
- The final PF0530E r4 monitor ran for ten minutes without watchdog/backtrace
  output and recorded no encoder-pin `EV` events. User-confirmed physical
  encoder actuation during that window remains unproven. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30`.
- A later PF0530E r5 read-only monitor recorded user-confirmed encoder
  actuation with GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` changing on COM6,
  `writes_sent=false`, and no watchdog/panic/backtrace scan hits. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30`.
- The PF0530F repo-only menu-proof refactor boots the LCD encoder menu path
  instead of the PF0530E serial pintrace path, keeps GPIO13/GPIO14/GPIO32
  input-only with internal pullups, keeps `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, and
  adds serial proof events for menu steps, button selects, invalid/suppressed
  A/B motion, and heartbeats. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-2026-05-30`.
- The later PF0530F COM6 live attempt passed write-flash and separate
  verify-flash, captured `PF0530F MENU_READY`, then captured `PF0530F
  LCD_INIT_FAILED` without `MENU_HB`, `MENU_STEP`, or `MENU_SELECT` proof.
  Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-LIVE-2026-05-30`.
- The PF0530G LCD init diagnostic keeps `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, uses
  GPIO21/GPIO22 I2C only, and emits stage-specific LCD/I2C proof lines before
  any renewed menu proof. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-LCD-INIT-DIAG-PF0530G-2026-05-30`.
- The PF0530G COM6 live gate passed serial LCD init diagnosis with one LCD ACK
  at `0x27`, all HD44780 init steps ok, `LCD_INIT_OK addr=0x27`, and 15
  `LCD_DIAG_HB status=ok` lines. Evidence directory:
  `research/bench-records/xbee-readonly/local-ky040-pf0530g-lcd-init-diag-live-20260530T223218Z/`.
- The ESP-NOW BBS LCD/encoder field-console plan is host-only and reuses the
  current LCD/encoder lineage only as a design boundary. It does not authorize
  PF0530H firmware, flash, monitor, serial writes, XBee/RF, relay writes,
  wiring mutation, or live display acceptance. Source ID:
  `SRC-LOCAL-ESPNOW-BBS-LCD-ENCODER-FIELD-CONSOLE-2026-05-30`.
- The PF0530H source image now implements the first local BBS LCD menu firmware
  slice for this hardware lane. It keeps `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, uses
  the PF0530G LCD init/probe path on GPIO21/GPIO22, uses input-only
  GPIO13/GPIO14/GPIO32 encoder handling, renders nine static/simulated BBS
  pages, and emits `PF0530H BBS_LCD_READY`, `BBS_LCD_RENDER`, `BBS_MENU_HB`,
  `BBS_MENU_STEP`, and `BBS_MENU_SELECT` proof lines. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-2026-05-31`.
- The PF0530H COM6 live gate passed fresh identity, full 4 MB rollback backup,
  write-flash, separate verify-flash, and read-only UART0 monitor. The
  transcript captured `LCD_INIT_OK addr=0x27`, `PF0530H BBS_LCD_READY`, three
  `BBS_LCD_RENDER`, three `BBS_MENU_HB`, and no crash/fault or closed-surface
  markers. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-LIVE-2026-05-31`.
- PF0530H was not accepted as an interactive menu after user testing reported
  no encoder/button LCD effect and the live proof had zero `BBS_MENU_STEP` and
  zero `BBS_MENU_SELECT` lines. PF0530I is the bounded source fix: it keeps
  `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, keeps GPIO13/GPIO14/GPIO32 input-only,
  splits polling into `fr_menu_input_task`, renders only dirty LCD rows or a
  slow idle refresh, emits `BBS_INPUT_READY`, emits `ENC_RAW`, and extends
  `BBS_LCD_RENDER` with `rows`, `seq`, `dur_ms`, and `reason`. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530I-2026-05-31`.
- PF0530I live monitor showed repeated task-watchdog backtrace lines.
  PF0530J keeps the split input/render design, changes `FR_MENU_POLL_MS` to
  10, and uses `fr_delay_ticks_at_least_one()` so the higher-priority input
  task yields for at least one FreeRTOS tick. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530J-2026-05-31`.
- The first PF0530J live monitor showed no watchdog/backtrace output but also
  no `ENC_RAW`, `BBS_MENU_STEP`, or `BBS_MENU_SELECT` input proof. PF0530K
  keeps the watchdog fix, adds GPIO any-edge interrupt queueing for GPIO13/
  GPIO14/GPIO32, decodes rotation from raw A/B transitions, and reports
  `irq=anyedge queue=64` plus heartbeat `irq_drop` proof. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530K-2026-05-31`.
- PF0530K write-flash and separate verify-flash passed on COM6. Its monitor
  showed `PF0530K BBS_LCD_READY`, `BBS_INPUT_READY`, `irq=anyedge queue=64`,
  two `BBS_LCD_RENDER`, and 59 `BBS_MENU_HB` lines with no
  watchdog/backtrace/panic/LCD-init-failure markers, but no encoder/button
  input proof. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530K-LIVE-2026-05-31`.
- PF0530L is the current flashed image for the live LCD menu UX test. It keeps
  PF0530K interrupt input capture and adds local page/row/detail/edit modes,
  software cursor/DDRAM metadata, dirty-cell render metadata, five named
  eight-slot glyph banks, custom bar/chart/digit/gauge demo pages, and a
  seven-second auto-demo cycle. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530L-2026-05-31`.
- PF0530L write-flash and separate verify-flash passed on COM6. Its read-only
  monitor showed `PF0530L BBS_LCD_READY`, `BBS_INPUT_READY`, `LCD_INIT_OK`, all
  13 page names, all five glyph banks, 77 `BBS_LCD_RENDER`, 21 `BBS_MENU_AUTO`,
  and 74 `BBS_MENU_HB` lines with no watchdog/backtrace/panic/LCD-init-failure
  or unsafe-open markers, but no encoder/button input proof. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530L-LIVE-2026-05-31`.
- Digi identifies the requested XBee model as `XBP9B-DPUT-001`, an
  XBee-PRO 900HP S3B Point2Multipoint 900 MHz, 250 mW, U.FL, 10 kbps part.
  Source ID: `SRC-DIGI-XBP9B-DPUT-001`.
- The user-uploaded photo archive shows an ESP-WROOM-32-family development
  board, black ESP32 I/O expansion shield, blue `4 Relay Module`, Songle
  `SRD-05VDC-SL-C` relay cans, Digi `XBP9B-DPUT-001 RevF` radio label, and
  Waveshare `XBee USB Adapter`. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Espressif's ESP32-WROOM-32 datasheet is the module-level source for the
  photographed ESP-WROOM-32 module family. Source ID:
  `SRC-ESP32-WROOM-32-DATASHEET`.
- Espressif's ESP32 hardware design guidelines add source-backed review points
  for ESP32 3.3 V supply/current, reset timing, UART, strapping pins, and GPIO.
  Source ID: `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.
- A third-party NodeMCU ESP32 expansion-board page is a non-authoritative
  candidate identity source for a similar shield class only; it does not prove
  the photographed shield revision, schematic, regulator, or safe power path.
  Source ID: `SRC-ESP32-IO-SHIELD-CANDIDATE`.
- Waveshare documents the XBee USB Adapter as a UART communication board with
  XBee and USB interfaces for testing, programming/configuration, and
  USB-to-UART use. Source ID: `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- The Songle `SRD-05VDC-SL-C` relay datasheet mirror provides component-level
  relay context only. Source ID: `SRC-SONGLE-SRD-05VDC-SL-C`.
- NIOSH, OSHA, and NEMA sources support the mains-readiness gate around
  qualified review, de-energization, GFCI/grounding context, overcurrent
  protection review, and enclosure selection. Source IDs:
  `SRC-NIOSH-ELECTRICAL-SAFETY`, `SRC-OSHA-DEENERGIZED-WORK`,
  `SRC-OSHA-GFCI`, `SRC-OSHA-AEGCP`, `SRC-OSHA-GROUNDING-OVERCURRENT`,
  `SRC-NEMA-ENCLOSURES`.
- TI and Espressif sources support a revised relay-expansion branch using a
  latched GPIO expander path, while CD74HC4067 is documented only as an analog
  mux for input routing. Source IDs: `SRC-TI-CD74HC4067`,
  `SRC-TI-TCA9555`, `SRC-ESPRESSIF-MCP23017-COMPONENT`,
  `SRC-TI-TPIC6B595`.
- External TFT references provide planning context for R61509V parallel-display
  pin pressure, but they do not verify the user's exact Open-Smart module.
  Source IDs: `SRC-NOPNOP2002-ESP-IDF-PARALLEL-TFT`,
  `SRC-LCDWIKI-R61509V-MRB2802`.

## Assumptions

- The first Wi-Fi control mode is ESP32 SoftAP so a bench browser can connect
  directly without depending on site infrastructure.
- Relay state-changing endpoints remain disabled unless an admin
  token/passphrase is provisioned in NVS and the runtime safety lock is open.
- XBee application payloads start as compact JSON objects inside API RF data;
  parser tests can later replace this with a binary schema if needed.
- DevKitC is no longer the assumed physical target for this project; it remains
  a source-backed reference until the photographed board is matched to a vendor
  or reference schematic.
- The Waveshare XBee USB Adapter is the first PC-side configuration/debug dock,
  not the final ESP32-mounted XBee carrier.
- The DIY prototype path starts with board/shield inspection, then relay-module
  verification with relay contacts disconnected, then XBee read-only discovery
  from the PC dock.
- The Open-Smart R61509V TFT remains a requested planning target, but it must be
  treated as unverified hardware until exact module, pinout, power, backlight,
  and touch evidence are recorded.
- Relay pin relief should use a latched I2C GPIO expander branch, not a
  CD74HC4067 analog mux.
- The LCD-only COM6 bridge test assumes one HD44780-compatible 20x4 I2C LCD on
  GPIO21/GPIO22 through a level shifter; exact LCD/backpack voltage, pullups,
  exact detected address value, contrast, and backlight current remain
  unresolved after the accepted same-session COM6-only flash/write-verify and
  visual proof gate.
- The current KY-040 live diagnostic wiring uses `CLK` to GPIO13, `DT` to
  GPIO14, `SW` to GPIO32, `+` to ESP32 3V3 only, and `GND` to ESP32 GND,
  following module silkscreen labels rather than assumed physical order.
  PF0530E is historical serial-pintrace evidence; PF0530F is the menu-proof
  source image. Its COM6 flash/verify gate passed, but live menu
  acceptance is blocked by `PF0530F LCD_INIT_FAILED`. PF0530G later passed
  serial LCD init diagnosis at address `0x27`. Exact pullups, rail margin,
  rotation direction, boot behavior, wire landing, physical LCD visual state,
  and live PF0530F menu behavior remain unresolved.
- The diagnostic-first branch assumes raw GPIO evidence must decide whether
  the next fix is hardware/electrical, switch polarity/debounce, quadrature
  decoding, or cleanup after acceptance.
- The pin-finder and contact-tracer diagnostics assume GPIO observations are
  temporary input-only clues for mislanded encoder wires, not accepted pin
  assignments. In PF0530F, GPIO13/GPIO14/GPIO32 use internal pullups for the
  menu-proof input path. The broader PF0530E watched-pin set is preserved only
  as historical serial-pintrace evidence.

## Unknowns

- Exact ESP32 development board vendor/revision, regulator, USB-UART bridge,
  and expansion-shield schematic.
- Expansion shield jumper position, power input source, and verified routing of
  GPIO labels to the ESP32 board.
- Exact four-channel relay module board manufacturer/model and electrical
  behavior.
- Relay trigger polarity, input current, 3.3 V compatibility, `JD-VCC`/`VCC`
  behavior, and isolation design.
- Whether the Waveshare XBee USB Adapter can be used beyond PC configuration;
  final ESP32-mounted carrier and wiring remain unresolved.
- Load type, load voltage, enclosure, fusing, and isolation design.
- Exact SPI MicroSD reader module, power path, pull-ups, shield continuity,
  boot-pin effects, card format, and log-retention policy.
- Exact Open-Smart R61509V TFT module identity, pinout, power/backlight needs,
  touch behavior, and display-driver path.
- Exact relay GPIO expander board, I2C address/pullups, inactive defaults,
  output latch behavior, and driver-stage fit.
- Installed ESP-IDF and XBee configuration tooling on the target development
  machine.
- Mains readiness evidence: qualified review, load definition, enclosure,
  overcurrent protection, grounding/bonding, strain relief,
  GFCI/de-energization process, and test record.
- Exact bench module markings, onboard pullup values and voltage, PPR/detents,
  switch bounce behavior, rail-current impact, rotation direction, boot
  behavior, and continuity from KY-040 `CLK`/`DT`/`SW` to
  GPIO13/GPIO14/GPIO32.
- User observation after the GPIO13 raw diagnostic flash says the raw LCD page
  is visible but `A/B/SW`, `ABCHG`, and `SWCHG` do not change. The cause is
  unresolved and should be treated as hardware/electrical/pinout first. A fresh
  LCD raw observation is pending after the KY-040 GPIO13-pullup diagnostic flash.
- The `PF0530A` pin-finder diagnostic was written/verified to COM6; the user
  later reported only pin 34 was visible. The `PF0530B` row-0 diagnostic was
  then written/verified to COM6, and the user reported no displayed pins
  changed. The `PF0530C` contact-tracer image and `PF0530D` DevKitC 13/14/32
  LCD image were written/verified to COM6. PF0530E r5 proved GPIO-level changes
  on GPIO13/GPIO14/GPIO32 during user-confirmed actuation. PF0530F is the
  menu-proof image prepared from that evidence; COM6 flash/verify passed, but
  live menu proof is blocked by `PF0530F LCD_INIT_FAILED` and hardware
  acceptance remains open. PF0530G later passed serial LCD init at `0x27`;
  PF0530H COM6 flash/verify and read-only monitor passed with BBS
  ready/render/heartbeat proof but zero step/select proof. PF0530I fixed
  render-starved input polling but showed task-watchdog backtraces; PF0530J
  fixed the watchdog symptom but did not capture input-transition proof;
  PF0530K captured no input events after clean flash/verify, and PF0530L is
  the current flashed image for renewed LCD menu UX testing. Visual LCD
  confirmation, custom glyph readability, auto-demo behavior, and rotary
  acceptance remain user-test evidence gates.

## Hard gate

No relay wiring, relay-expander wiring to relay inputs, load switching, XBee
configuration writes, TFT wiring, or firmware flashing beyond the named COM6
UART bridge gate, named LCD-only flash gate, named encoder-menu COM6
write/verify gate, and named KY-040 diagnostic COM6 write/verify gate is
approved by this package.
The XBee bench lane now has selected-port programming, selected-port OTA
`link_probe`, and permanent bridge flash/retest records; further radio writes,
range/throughput tests, relay payloads, or load/mains steps require new
physical verification records and owner review. The LCD-only gate is
display-status output only: it does not drive a relay expander path and does
not authorize relay/load/mains work. The PF0530F encoder diagnostic is
input-only on GPIO13/GPIO14/GPIO32 and enables internal pullups only on those
three menu inputs; it does not authorize relay GPIO writes, relay
expander writes, XBee setting writes, RF/range/throughput tests,
relay/load/mains work, or future COM6 flash without a fresh live gate. The
KY-040 GPIO13-pullup
diagnostic image, `PF0530A` pin-finder image, `PF0530B` row-0 image, and
`PF0530C` contact tracer are written/verified to COM6 for user LCD testing.
PF0530D is also written/verified to COM6 and closes the diagnostic XBee bridge
loop. PF0530E r5 completed its named read-only serial-monitor gate with
user-confirmed GPIO13/GPIO14/GPIO32 input changes. PF0530F completed its named
COM6 write/verify gate, but read-only live menu acceptance is blocked by
`PF0530F LCD_INIT_FAILED`. PF0530G completed the separately authorized LCD init
diagnostic gate with serial `LCD_INIT_OK addr=0x27`. PF0530H completed the
COM6-only BBS LCD menu flash/verify/read-only-monitor proof, but user testing
reported no encoder/button LCD effect. PF0530I then showed task-watchdog
backtraces, PF0530J showed no input-transition proof, PF0530K captured no
input events after clean flash/verify, and PF0530L is the current flashed
user-test image. It still requires live LCD/encoder observation, page-change
proof, custom glyph readability, encoder direction, and pushbutton proof.
Further flash, monitor,
RF/range/throughput, relay/load/mains work, hardware acceptance, or
direct-stimulus continuity testing outside that named gate needs a separate
fresh gate.

Mains switching remains hard blocked by
[mains-readiness-gate.md](mains-readiness-gate.md).

## Public packet entry point

Start with [Prototype Build Packet](prototype-build-packet.md) before using the
visual blueprint, build guide, pin plan, or XBee documents. The packet is the
public navigation layer for verified facts, assumptions, unknowns, review
sequence, evidence checklist, and stop conditions. It does not close any
hardware, relay, radio, TFT, MicroSD, load, or mains gap.
