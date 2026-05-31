# Power And Safety Gates

## Verified facts

- The current photo archive shows an ESP-WROOM-32-family development board on a
  black ESP32 I/O expansion shield with visible `DC6.5-16V`, `USB5V`, `5V`, and
  `3.3V` markings. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Espressif's ESP32-WROOM-32 datasheet gives module-level supply and electrical
  context for ESP32-WROOM-32, but not the photographed dev-board regulator or
  expansion-shield power path. Source ID: `SRC-ESP32-WROOM-32-DATASHEET`.
- Espressif's ESP32 hardware design guidelines provide ESP32 review points for
  3.3 V supply/current, reset timing, UART, strapping pins, and GPIO. Source
  ID: `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.
- A third-party NodeMCU ESP32 expansion-board page is a non-authoritative
  identity candidate for a similar shield class with DC 6.5-16 V, USB 5 V, and
  5 V/3.3 V jumper text; it does not verify the photographed shield. Source ID:
  `SRC-ESP32-IO-SHIELD-CANDIDATE`.
- The relay module photos show a blue `4 Relay Module` populated with Songle
  `SRD-05VDC-SL-C` relay cans and a visible `JD-VCC`/`VCC` area. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- The Songle relay datasheet mirror provides component-level context for
  `SRD-05VDC-SL-C`; it does not verify the photographed module's input trigger
  circuit, jumper behavior, or isolation boundary. Source ID:
  `SRC-SONGLE-SRD-05VDC-SL-C`.
- Digi's 900HP product material lists UART (3V) and SPI data interfaces. Source
  ID: `SRC-DIGI-XBEE-PRO-900HP`.
- ESP-IDF stable v6.0.1 documents the I2C master driver API used by the
  LCD-only display-status firmware test. Source ID: `SRC-ESP-IDF-I2C`.
- ESP-IDF GPIO source coverage and the local encoder-menu firmware record
  bound GPIO34/GPIO35/GPIO13 to input-only LCD menu reads, not relay outputs.
  The KY-040 diagnostic refactor keeps GPIO34/GPIO35 internal pulls disabled
  and enables only the GPIO13 internal pullup for active-low `SW`. Source IDs:
  `SRC-ESP-IDF-GPIO`,
  `SRC-LOCAL-FOUR-RELAY-ENCODER-MENU-FIRMWARE-2026-05-30`,
  `SRC-LOCAL-FOUR-RELAY-KY040-DIAGNOSTIC-REFACTOR-2026-05-30`.
- The selected-module source for the current encoder lane is an independent
  Manuals+ ASIN mirror identifying `B06XQTHDRR` as a Cylewet KY-040 module with
  `CLK`, `DT`, `SW`, `+`, and `GND` pins. Source ID:
  `SRC-MANUALSPLUS-CYLEWET-KY040-B06XQTHDRR`.
- The KY-040 pin-finder diagnostic samples GPIO14, GPIO32, and GPIO33 as
  additional input-only probes with internal pulls disabled. It does not change
  relay, storage, or final encoder pin assignments. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-PIN-FINDER-DIAGNOSTIC-2026-05-30`.
- The KY-040 row-0 diagnostic refactor keeps the same input-only probe set and
  moves the essential raw/count/probe views onto LCD row 0 with firmware ID
  `PF0530B`, so it does not require encoder navigation or lower LCD rows.
  Source ID: `SRC-LOCAL-FOUR-RELAY-KY040-ROW0-DIAGNOSTIC-2026-05-30`.
- The KY-040 GPIO sweep contact tracer adds firmware ID `PF0530C` after the
  user reported no displayed `PF0530B` pins changed. It uses an input-only
  ten-pin allowlist, enables internal pullups only on GPIO13/GPIO14, excludes
  flash/LCD/UART0/XBee/strapping-risk/relay-candidate pins, and closes the
  diagnostic XBee bridge loop. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-GPIO-SWEEP-CONTACT-TRACER-2026-05-30`. The same
  source record now includes the COM6 `PF0530C` write/verify gate for user LCD
  testing.
- The KY-040 DevKitC 13/14/32 diagnostic adds firmware ID `PF0530D` for the
  user-confirmed 3.3 V wiring: `CLK` GPIO13, `DT` GPIO14, `SW` GPIO32, and a
  100 nF capacitor across encoder `+` and `GND`. It keeps the three pins
  input-only, enables internal pullups on all three, locks LCD page 0, and
  closes the diagnostic XBee bridge loop. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-DEVKITC-13-14-32-DIAGNOSTIC-2026-05-30`.
- The KY-040 serial pintrace diagnostic adds firmware ID `PF0530E`, keeps the
  watched GPIOs input-only, enables internal pullups only on GPIO13/GPIO14/
  GPIO32, closes the XBee bridge loop, and uses COM6/UART0 serial output to
  identify which pin changes during live testing. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30`.
- The PF0530F menu-proof refactor keeps GPIO13 `CLK`, GPIO14 `DT`, and GPIO32
  `SW` input-only with internal pullups, closes XBee bridge forwarding, and
  prepares LCD menu navigation plus serial proof events from the same input
  pins. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-2026-05-30`.
- The later PF0530F COM6 live attempt passed write-flash and separate
  verify-flash, but the read-only monitor captured `PF0530F LCD_INIT_FAILED`
  with no `MENU_HB`, `MENU_STEP`, or `MENU_SELECT` proof. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-LIVE-2026-05-30`.
- The PF0530G LCD init diagnostic keeps the bridge closed, uses GPIO21/GPIO22
  I2C only, and emits stage-specific LCD/I2C proof lines before any renewed
  menu proof. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-LCD-INIT-DIAG-PF0530G-2026-05-30`.
- The PF0530G COM6 live gate passed serial LCD init diagnosis with one LCD ACK
  at `0x27`, all HD44780 init steps ok, `LCD_INIT_OK addr=0x27`, and repeated
  ok heartbeats. Physical LCD visual confirmation remains separate.
- The photo archive shows a Waveshare `XBee USB Adapter`; Waveshare documents
  the adapter as a UART communication board with XBee and USB interfaces.
  Source IDs: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
  `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- NIOSH, OSHA, and NEMA sources support a mains-readiness checklist around
  qualified-person review, de-energization, GFCI/grounding context, protective
  devices, and enclosure selection; they do not authorize DIY mains wiring.
  Source IDs: `SRC-NIOSH-ELECTRICAL-SAFETY`, `SRC-OSHA-DEENERGIZED-WORK`,
  `SRC-OSHA-GFCI`, `SRC-OSHA-AEGCP`, `SRC-OSHA-GROUNDING-OVERCURRENT`,
  `SRC-NEMA-ENCLOSURES`.
- CD74HC4067 is source-backed as an analog mux/demux, while TCA9555 and
  MCP23017 are source-backed as GPIO expansion paths. Source IDs:
  `SRC-TI-CD74HC4067`, `SRC-TI-TCA9555`,
  `SRC-ESPRESSIF-MCP23017-COMPONENT`.

## Assumptions

- Bench development uses low-voltage test loads or disconnected relay outputs
  until load safety is reviewed.
- Relay GPIO outputs are configured to the inactive state before relay driver
  enablement.
- The application treats ambiguous relay polarity as a configuration error and
  refuses relay changes until the polarity is verified.
- The Waveshare adapter is a PC-side XBee configuration/debug dock until proven
  safe for any ESP32-mounted role.
- Relay contacts remain disconnected or attached only to a reviewed low-voltage
  dummy load until a mains/load package is separately approved.
- Relay pin relief uses a latched expander path; CD74HC4067 mux channels are
  treated only as input observations.

## Hardware gates before wiring

The public [Prototype Build Packet](prototype-build-packet.md) keeps these
gates visible as stop conditions. A visible public diagram or label does not
close a gate.

| Gate | Required evidence | Owner |
| --- | --- | --- |
| ESP32 board identity | Photo/source/inspection record showing dev-board vendor, revision, USB-UART bridge, regulator, and module variant. | Hardware |
| Expansion shield power and routing | Jumper position, selected input source, regulator output, current limit, shield-to-board continuity, and no dual-power conflict. | Hardware |
| Relay board identity | Board manufacturer/model, schematic or product page, input voltage, trigger polarity, input current, isolation design, `JD-VCC`/`VCC` behavior, and channel/load ratings. | Hardware |
| Relay expander path | Exact expander board, I2C address pins, pullups, power rail, inactive output defaults, latch proof, readback policy, and driver-stage interface. | Hardware + Firmware + QA |
| CD74HC4067 input path | Exact mux breakout, address/enable wiring, ADC1 pin, voltage protection, source impedance, scan cadence, and proof that scans cannot change relay state. | Hardware + Firmware + QA |
| R61509V TFT path | Exact display module, data/control bus, touch interface, power/backlight current, and ESP32 pin-conflict review. | Hardware + Firmware + QA |
| LCD-only status display path | Same-session level-shifter/common-ground evidence, GPIO21/GPIO22 confirmation, pullup-voltage review, one detected PCF8574/PCF8574A candidate address, contrast/backlight observation, and rail-current caution. | Hardware + Firmware + QA |
| Rotary encoder menu input | Same-session evidence for KY-040 `CLK` to GPIO13, `DT` to GPIO14, `SW` to GPIO32, `+` to ESP32 3V3 only, common ground, module/pullup voltage, board/shield continuity, boot behavior, debounce/noise behavior, and UI-intent-only firmware boundary. | Hardware + Firmware + QA |
| XBee adapter identity and PC dock path | Adapter revision, PC serial port, driver path, power source, DIN/DOUT mapping, reset/sleep pins, optional CTS/RTS mapping, and level compatibility. | Hardware |
| Final ESP32-to-XBee carrier | Carrier/socket selection, 3.3 V power budget, DIN/DOUT routing, reset/sleep/associate/flow-control handling, and antenna clearance. | Hardware |
| Power tree | Bench supply limits, shared ground plan, 3.3 V/5 V budget, relay supply path, XBee transmit current budget, and isolation boundary. | Hardware |
| Load design | Load type, voltage/current, fusing, enclosure, grounding, snubber/surge needs, and legal/safety review for mains or inductive loads. | Hardware |
| Mains readiness | Qualified review, load definition, enclosure, overcurrent protection, grounding/bonding, strain relief, GFCI/de-energization, separation, labels/disconnect, and test record. | Hardware + QA |

## Firmware safety requirements

- Boot state: all relay outputs are inactive before any saved state is applied.
- Reset/watchdog recovery: all relay outputs return inactive.
- Invalid HTTP or XBee command: no relay state change; reject reason is logged
  and reported.
- Safety lock closed: relay state-changing commands are rejected; all-off
  remains available through authenticated local control.
- Missing admin credential: relay state-changing HTTP endpoints are disabled.
- Missing XBee allowlist: radio relay commands are rejected.
- Missing relay polarity config: all relay commands are rejected.
- Expander init/write/readback failure: `hardwareGateClosed` is false and relay
  commands are rejected with `hardware_gate_open`.
- Future rotary encoder events are UI intents only and cannot directly trigger
  relay, radio, flash/erase, XBee setting-write, or persistent configuration
  paths.
- TFT touch buttons, mux inputs, HTTP, and XBee commands all use the same
  `relay_manager` plus `safety_supervisor` path before outputs change.

## Bench action status

| Action | Status | Reason |
| --- | --- | --- |
| Power ESP32/shield through barrel jack | Blocked | Expansion-shield jumper state, regulator behavior, and active power source are unverified. |
| Wire ESP32 GPIO to relay inputs | Blocked | Relay trigger voltage/current/polarity and shield routing are unknown. |
| Use CD74HC4067 as relay outputs | Blocked | Analog mux selects input paths and does not provide independent latched relay states. |
| Prove CD74HC4067 on ADC1 test voltages | Allowed after low-voltage source review | Input-only proof; no relay module or safety-critical output connection. |
| Prove relay expander outputs on LEDs or logic analyzer | Allowed after I2C pullup/address/power review | Output-latch proof only; no relay-module inputs or coils. |
| Wire relay expander or driver to relay module inputs | Blocked | Relay trigger polarity/current/voltage/isolation behavior is unresolved. |
| Wire Open-Smart R61509V TFT | Blocked | Exact module, pinout, power/backlight, touch, and pin-conflict evidence are missing. |
| Run LCD-only status display firmware on GPIO21/GPIO22 | Allowed only after LCD-only Tier 3 gate | Display text/status output only; no encoder GPIOs, no relay expander outputs, no XBee setting writes, no relay/load/mains. |
| Run encoder serial pintrace firmware on GPIO13/GPIO14/GPIO32 plus passive candidates | PF0530E named Tier 3 gate | Input-only diagnostic proof; PF0530E uses internal pullups only on GPIO13/GPIO14/GPIO32, closes XBee bridge forwarding, writes no probe GPIO outputs, and emits COM6 serial events only; no relay GPIO writes, no relay expander outputs, no XBee setting writes, no RF/range/throughput, no relay/load/mains, and no further flash without a fresh Tier 3 gate. |
| Run PF0530F encoder menu proof on GPIO13/GPIO14/GPIO32 | LCD-init-blocked | COM6 write-flash and separate verify-flash passed under a named Tier 3 gate, but read-only monitor captured `PF0530F LCD_INIT_FAILED` and no `MENU_HB`, `MENU_STEP`, or `MENU_SELECT`; future LCD diagnosis or live proof requires fresh authority, rollback/recovery review as applicable, no relay/load/mains, and no XBee/RF or serial-write expansion. |
| Run PF0530G LCD init diagnostic on GPIO21/GPIO22 | Completed Tier 3 serial diagnosis | LCD/I2C diagnosis only; bridge closed, no encoder menu acceptance, no relay GPIO writes, no relay expander outputs, no XBee/RF, no relay/load/mains, and no erase/wiring mutation. Serial proof found one ACK at `0x27` and `LCD_INIT_OK addr=0x27`; physical LCD visual confirmation remains separate. |
| Wire rotary encoder A/B/SW inputs | Gate-pending | The KY-040 wiring plan is recorded; acceptance still needs power-off silkscreen/continuity proof, USB-only 3.3 V module voltage, A/B idle/toggle evidence, SW idle high/pulls low evidence, boot proof, and serial pintrace proof. |
| Power relay board from ESP32/shield 5 V | Blocked | Relay module current and `JD-VCC`/`VCC` isolation behavior are unknown. |
| Switch mains or inductive loads | Blocked | Load safety design is unknown. |
| Prepare mains switching steps | Blocked | The approved artifact is only `mains-readiness-gate.md`; no mains wiring procedure is allowed in this phase. |
| Use Waveshare adapter for read-only XBee discovery | Allowed after PC serial/driver check | No ESP32 wiring or XBee setting writes. |
| Write XBee configuration | Blocked | Current settings backup, address plan, AES key process, and rollback are not documented. |
| Connect XBee DIN/DOUT to ESP32 UART | Blocked | Final carrier, voltage path, and DIN/DOUT routing are unknown. |
| Build static UI prototype | Allowed | No hardware mutation. |
| Hardware-facing firmware or live output enablement | Deferred | The project-local disabled ESP-IDF skeleton is separate from relay/load enablement. |

## Unknowns

- Whether the relay board is active-high or active-low.
- Whether relay inputs are compatible with ESP32 3.3 V GPIO levels.
- Relay input current per channel.
- Whether the relay board input side is opto-isolated and how that isolation is
  powered or bypassed by jumper position.
- Whether relay coils share logic supply or use a separate relay supply.
- Exact bench KY-040 module markings, pullup voltage, debounce/noise needs,
  panel ESD exposure, cable length, rail-current impact, continuity, raw
  A/B/SW behavior on GPIO13/GPIO14/GPIO32, boot behavior, LCD init cause, and
  user observation of the `PF0530F` LCD menu-proof diagnostic after LCD init is
  diagnosed.
- Whether the intended load requires snubber, flyback, MOV, fuse, or contactor
  design.
- Whether the Waveshare XBee adapter exposes direct 3.3 V UART, level-shifted
  UART, or selectable power/logic rails on the photographed headers.
- Whether any future load design can satisfy the mains-readiness gate in
  `mains-readiness-gate.md`.
- Exact relay expander board, I2C address/pullups, inactive default behavior,
  output readback, and driver-stage choice.
- Exact CD74HC4067 breakout, input voltage path, ADC protection, and scan
  behavior.
- Exact Open-Smart R61509V TFT module identity, power/backlight current, touch
  interface, and bus pin allocation.
- Exact 20x4 LCD module/backpack identity, I2C address, pullup voltage, logic
  voltage, contrast, backlight current, and rail-current margin for the
  LCD-only status display test.
