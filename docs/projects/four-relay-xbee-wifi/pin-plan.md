# Pin Plan

## Verified facts

- The current photo archive shows an ESP-WROOM-32-family development board and
  a black ESP32 I/O expansion shield with visible GPIO labels. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- The photographed expansion shield has visible labels for `GPIO25`, `GPIO26`,
  `GPIO27`, and `GPIO33`. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Espressif's ESP32-WROOM-32 datasheet identifies GPIO25, GPIO26, GPIO27, and
  GPIO33 as module I/O pins. Source ID: `SRC-ESP32-WROOM-32-DATASHEET`.
- Espressif's ESP32 GPIO documentation identifies GPIO0, GPIO2, GPIO5, GPIO12,
  and GPIO15 as strapping pins, and GPIO6 through GPIO11 as SPI0/1 pins used by
  flash-related functions. Source ID: `SRC-ESP-IDF-GPIO`.
- ESP32 GPIO matrix behavior allows peripheral signals to be routed through
  available GPIO pins. Source ID: `SRC-ESP-IDF-GPIO`.
- ESP32 UART documentation identifies three UART controllers. Source ID:
  `SRC-ESP-IDF-UART`.
- ESP-IDF stable v6.0.1 documents the I2C master driver API and the
  `esp_driver_i2c` component used by the LCD-only display-status test. Source
  ID: `SRC-ESP-IDF-I2C`.
- The encoder-menu firmware configures GPIO34, GPIO35, and GPIO13 as
  input-only rotary encoder lines for LCD menu navigation. The KY-040
  diagnostic refactor keeps GPIO34/GPIO35 internal pulls disabled and enables
  only the GPIO13 internal pullup for the active-low switch while relay pages
  stay locked as UI text only. Source IDs:
  `SRC-LOCAL-FOUR-RELAY-ENCODER-MENU-FIRMWARE-2026-05-30`,
  `SRC-LOCAL-FOUR-RELAY-KY040-DIAGNOSTIC-REFACTOR-2026-05-30`.
- The user-identified ASIN `B06XQTHDRR` is indexed by an independent Manuals+
  mirror as a Cylewet KY-040 module with `CLK`, `DT`, `SW`, `+`, and `GND`
  pins. Source ID: `SRC-MANUALSPLUS-CYLEWET-KY040-B06XQTHDRR`.
- The KY-040 pin-finder diagnostic adds input-only probes on GPIO14, GPIO32,
  and GPIO33 beside the intended GPIO34/GPIO35/GPIO13 encoder pins. It does
  not accept those probes as wiring assignments or relay/storage reassignments.
  Source ID: `SRC-LOCAL-FOUR-RELAY-KY040-PIN-FINDER-DIAGNOSTIC-2026-05-30`.
- The KY-040 row-0 diagnostic refactor keeps the same input-only probe set and
  firmware ID `PF0530B`, with raw levels, transition counts, and each probe's
  live level/change count cycling on LCD row 0. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-ROW0-DIAGNOSTIC-2026-05-30`.
- The KY-040 GPIO sweep contact tracer adds firmware ID `PF0530C` after the
  user reported no displayed `PF0530B` pins changed. It sweeps GPIO34,
  GPIO35, GPIO36, GPIO39, GPIO13, GPIO14, GPIO18, GPIO19, GPIO23, and GPIO32
  as input-only diagnostic probes, enables internal pullups only on GPIO13 and
  GPIO14, excludes flash, LCD, UART0, XBee UART, strapping-risk, and
  relay-candidate pins, and closes the diagnostic XBee bridge loop. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-GPIO-SWEEP-CONTACT-TRACER-2026-05-30`. The same
  source record now includes the COM6 `PF0530C` write/verify gate for user LCD
  testing.
- The KY-040 DevKitC 13/14/32 diagnostic adds firmware ID `PF0530D` for the
  user-confirmed wiring: `CLK` GPIO13, `DT` GPIO14, `SW` GPIO32, module `+` on
  ESP32 3V3, and a 100 nF capacitor across `+` and `GND`. It keeps the pins
  input-only, enables internal pullups on all three, locks LCD page 0, and
  closes the diagnostic XBee bridge loop. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-DEVKITC-13-14-32-DIAGNOSTIC-2026-05-30`.
- The KY-040 serial pintrace diagnostic adds firmware ID `PF0530E` and watches
  GPIO0/GPIO2/GPIO4/GPIO5/GPIO12/GPIO13/GPIO14/GPIO15/GPIO16/GPIO17/GPIO18/
  GPIO19/GPIO21/GPIO22/GPIO23/GPIO25/GPIO26/GPIO27/GPIO32/GPIO33/GPIO34/
  GPIO35/GPIO36/GPIO39 as input-only live probes on COM6. Internal pullups are
  enabled only on GPIO13/GPIO14/GPIO32. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30`.
- The PF0530F menu-proof refactor keeps GPIO13 `CLK`, GPIO14 `DT`, and GPIO32
  `SW` input-only with internal pullups, boots the LCD menu path instead of the
  PF0530E serial pintrace path, and keeps XBee bridge forwarding closed. Source
  ID: `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-2026-05-30`.
- ESP-IDF SDSPI documentation records that SD-over-SPI has lower throughput
  than SDMMC access but allows flexible pin routing through the GPIO matrix.
  Source ID: `SRC-ESP-IDF-SDSPI`.
- Espressif SD pull-up guidance applies to ESP32 SD-card use over SPI or SDMMC
  and documents pull-up and boot/strapping conflicts that require review before
  wiring. Source ID: `SRC-ESP-IDF-SD-PULLUP`.
- Espressif hardware design guidance is the review source for ESP32 power,
  UART, strapping-pin, and GPIO hardware constraints before bench wiring.
  Source ID: `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.
- The photographed Waveshare XBee USB Adapter has visible UART/control/power
  header labels, but final ESP32 DIN/DOUT wiring is not selected. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- CD74HC4067 is a 16:1, one-channel analog mux/demux and is not a latched
  relay-output expander. Source ID: `SRC-TI-CD74HC4067`.
- TCA9555 and MCP23017 are documented 16-bit I/O expansion paths for future
  relay-output latching. Source IDs: `SRC-TI-TCA9555`,
  `SRC-ESPRESSIF-MCP23017-COMPONENT`.
- External R61509V TFT references show that parallel display modules can require
  a large data/control pin set. Source IDs:
  `SRC-NOPNOP2002-ESP-IDF-PARALLEL-TFT`,
  `SRC-LCDWIKI-R61509V-MRB2802`.

## Revised pin strategy

The public [Prototype Build Packet](prototype-build-packet.md) exposes this
pin plan as a pin-pressure review surface. The map is provisional and does not
authorize final wiring.

The relay pin-relief path is now a latched output-expander branch, not an
analog-mux branch. `GPIO25`, `GPIO26`, `GPIO27`, and `GPIO33` remain historical
direct-relay candidates only; they should be freed if the R61509V TFT branch
needs those pins.

Preferred relay path:

```text
ESP32 I2C pins -> MCP23017 or TCA9555 -> verified driver stage -> relay module inputs
```

Allowed mux path:

```text
ESP32 mux address pins + ADC1 input -> CD74HC4067 -> slow input source
```

The mux path may support resistive touch, buttons, potentiometers, status
inputs, or low-rate sensors after voltage and ADC protection are verified. It is
not approved for relay state holding, TFT data-bus reduction, or
safety-critical output selection.

## Legacy direct-GPIO mapping

This mapping is a design placeholder only. It is not approved for wiring until
the photographed ESP32 board/shield routing, relay board behavior, and XBee
carrier path are verified. It is superseded by the expander branch when TFT pin
pressure is active.

| Function | Provisional GPIO | Direction | Gate |
| --- | --- | --- | --- |
| Relay channel 1 | GPIO25 | Output | Shield routing plus relay trigger voltage/current/polarity verified |
| Relay channel 2 | GPIO26 | Output | Shield routing plus relay trigger voltage/current/polarity verified |
| Relay channel 3 | GPIO27 | Output | Shield routing plus relay trigger voltage/current/polarity verified |
| Relay channel 4 | GPIO33 | Output | Shield routing plus relay trigger voltage/current/polarity verified |
| Relay expander SDA/SCL | Unassigned | Bidirectional | Exact expander board, pullups, address pins, default state, and bus conflict review verified |
| CD74HC4067 select and enable | Unassigned | Output | Exact mux breakout, voltage, enable behavior, and input-only use verified |
| CD74HC4067 signal to ADC1 | Unassigned | Input | ADC1 pin, voltage range, source impedance, protection, and Wi-Fi/ADC conflict review verified |
| R61509V TFT data/control bus | Unassigned | Mixed | Exact Open-Smart module pinout, power/backlight, bus width, and boot/flash/UART conflicts verified |
| SPI MicroSD SCK | GPIO18 | Output | Reader identity, 3.3 V power, pull-ups, shield continuity, boot-pin review, and relay/XBee conflict review verified |
| SPI MicroSD MISO | GPIO19 | Input | Reader identity, 3.3 V power, pull-ups, shield continuity, boot-pin review, and relay/XBee conflict review verified |
| SPI MicroSD MOSI | GPIO23 | Output | Reader identity, 3.3 V power, pull-ups, shield continuity, boot-pin review, and relay/XBee conflict review verified |
| SPI MicroSD CS | GPIO32 | Output | Reader identity, 3.3 V power, pull-ups, shield continuity, boot-pin review, and relay/XBee conflict review verified |
| XBee UART TX from ESP32 to DIN | Unassigned | Output | Final carrier, DIN/DOUT routing, and level compatibility verified |
| XBee UART RX from DOUT to ESP32 | Unassigned | Input | Final carrier, DIN/DOUT routing, and level compatibility verified |
| LCD-only test SDA | GPIO21 | Bidirectional | Same-session LCD level-shifter/common-ground/pullup confirmation; display-status output only |
| LCD-only test SCL | GPIO22 | Output | Same-session LCD level-shifter/common-ground/pullup confirmation; display-status output only |
| Encoder diagnostic CLK/A | GPIO13 | Input | KY-040 `CLK`; internal pullup enabled for PF0530F; requires live `MENU_STEP` proof and boot behavior before acceptance |
| Encoder diagnostic DT/B | GPIO14 | Input | KY-040 `DT`; internal pullup enabled for PF0530F; requires live `MENU_STEP` proof and boot behavior before acceptance |
| Encoder diagnostic switch | GPIO32 | Input | KY-040 `SW`; internal pullup enabled for PF0530F; conflicts with the provisional MicroSD CS investigation until one path is retired |

Source IDs: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
`SRC-ESP32-WROOM-32-DATASHEET`, `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-UART`,
`SRC-ESP-IDF-I2C`, `SRC-ESP-IDF-SDSPI`, `SRC-ESP-IDF-SD-PULLUP`,
`SRC-DIGI-XBEE-PRO-900HP`, `SRC-WAVESHARE-XBEE-USB-ADAPTER`,
`SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`, `SRC-TI-CD74HC4067`,
`SRC-TI-TCA9555`, `SRC-ESPRESSIF-MCP23017-COMPONENT`,
`SRC-NOPNOP2002-ESP-IDF-PARALLEL-TFT`, `SRC-LCDWIKI-R61509V-MRB2802`,
`SRC-BOURNS-PEC11R`,
`SRC-MANUALSPLUS-CYLEWET-KY040-B06XQTHDRR`,
`SRC-LOCAL-FOUR-RELAY-ROTARY-ENCODER-MENU-PLAN-2026-05-30`,
`SRC-LOCAL-FOUR-RELAY-ENCODER-MENU-FIRMWARE-2026-05-30`,
`SRC-LOCAL-FOUR-RELAY-KY040-DIAGNOSTIC-REFACTOR-2026-05-30`,
`SRC-LOCAL-FOUR-RELAY-KY040-PIN-FINDER-DIAGNOSTIC-2026-05-30`,
`SRC-LOCAL-FOUR-RELAY-KY040-ROW0-DIAGNOSTIC-2026-05-30`,
`SRC-LOCAL-FOUR-RELAY-KY040-GPIO-SWEEP-CONTACT-TRACER-2026-05-30`,
  `SRC-LOCAL-FOUR-RELAY-KY040-DEVKITC-13-14-32-DIAGNOSTIC-2026-05-30`,
  `SRC-LOCAL-FOUR-RELAY-KY040-SERIAL-PINTRACE-PF0530E-2026-05-30`,
  `SRC-LOCAL-FOUR-RELAY-KY040-ENCODER-MENU-PF0530F-2026-05-30`.

## Future rotary encoder menu input

The rotary encoder menu implementation keeps the accepted LCD path on
GPIO21/GPIO22, the accepted XBee bridge on GPIO17/GPIO16, and the relay
candidates GPIO25/GPIO26/GPIO27/GPIO33 reserved. The current PF0530F
menu-proof branch maps module `CLK` to GPIO13, `DT` to GPIO14, `SW` to GPIO32,
`+` to ESP32 3V3 only, and `GND` to ESP32 GND. GPIO13/GPIO14/GPIO32 use
internal pullups in this diagnostic. GPIO32 remains a provisional MicroSD CS
investigation pin outside this encoder proof and cannot be accepted for both
uses.
Encoder events are UI intents only: rotation changes pages, short press shows
`SELECT BLOCKED` on relay UI pages or `SELECT ACK` elsewhere, and long press
returns to the status page. Encoder events must not directly trigger relay,
radio, flash/erase, XBee setting-write, or persistent configuration paths.

The pin-finder and `PF0530B` row-0 diagnostics also sampled GPIO14, GPIO32,
and GPIO33 as input-only probes with internal pulls disabled. The `PF0530C`
contact tracer dropped relay-candidate GPIO33, added GPIO36/GPIO39 and passive
GPIO18/GPIO19/GPIO23 beside GPIO32, and enabled internal pullups only on
GPIO13/GPIO14. PF0530D then focused on GPIO13/GPIO14/GPIO32. PF0530E
superseded it for serial-first troubleshooting and proved GPIO-level changes
on GPIO13/GPIO14/GPIO32 during r5 user-confirmed actuation. PF0530F uses that
same three-pin mapping for the next LCD menu-proof image, but final wiring
acceptance still requires a separate live gate.

## Direct GPIO drive gate

Direct ESP32 GPIO drive to the relay inputs is allowed only after all of these
are recorded:

- Shield continuity proves `GPIO25`, `GPIO26`, `GPIO27`, and `GPIO33` route to
  the expected ESP32 board pins.
- Relay trigger polarity is identified by exact-module source evidence or
  controlled measurement.
- Relay input current per channel is measured or source-backed.
- The measured relay input behavior passes a source-backed 3.3 V/current gate
  for the ESP32 output pin.
- `JD-VCC`/`VCC` behavior and the isolation boundary are documented.

If any item fails or remains unknown, relay input wiring stays blocked and a
future driver-stage design is required.

## Relay expander gate

A latched expander path is required before relay commands are accepted when the
project needs to free direct ESP32 GPIOs for the TFT branch.

- Expander pins initialize inactive on boot before relay commands are accepted.
- I2C address, pullups, selected ESP32 pins, and default pin state must be
  verified on the exact expander board.
- First proof drives LEDs or a logic analyzer only.
- If expander init, write, or required readback fails, `hardwareGateClosed` stays
  false and relay commands return `hardware_gate_open`.
- The relay driver stage is selected only after the exact relay module trigger
  polarity, input current, voltage compatibility, and isolation behavior are
  verified.

## Avoided pins for first pass

| Pin group | Reason | Source IDs |
| --- | --- | --- |
| GPIO0, GPIO2, GPIO5, GPIO12, GPIO15 | ESP32 strapping pins need boot-state review before use. | `SRC-ESP-IDF-GPIO` |
| GPIO6 through GPIO11 | Used internally for SPI flash on ESP32-WROOM-32 and not recommended for other uses. | `SRC-ESP32-WROOM-32-DATASHEET`, `SRC-ESP-IDF-GPIO` |
| GPIO1/GPIO3 | UART0 is commonly associated with USB serial flashing/debugging paths; reserve until the photographed board USB-UART circuit is verified. | `SRC-ESP32-WROOM-32-DATASHEET`, `SRC-ESP-IDF-UART` |
| GPIO25, GPIO26, GPIO27, GPIO33 | Current relay candidates; avoid reusing them for MicroSD or encoder inputs until relay routing is closed or reassigned. | `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`, `SRC-ESP-IDF-GPIO` |
| GPIO34 through GPIO39 | Input-only pins; not candidates for relay outputs. | `SRC-ESP-IDF-GPIO` |

## Assumptions

- GPIO25, GPIO26, GPIO27, and GPIO33 remain relay candidates because the
  photographed shield labels expose them and they are not in the avoided
  first-pass groups above.
- GPIO18, GPIO19, GPIO23, and GPIO32 are only the preferred SPI MicroSD
  investigation set. They are not approved wiring until the exact MicroSD
  reader, shield continuity, 3.3 V power, pull-ups, and boot-pin risks are
  verified. PF0530F temporarily consumes GPIO32 as the encoder switch
  diagnostic input, so MicroSD CS on GPIO32 is blocked until one path is
  retired.
- A later firmware pin map can choose XBee UART pins through the GPIO matrix
  after a final carrier and DIN/DOUT path are verified.
- The LCD-only test temporarily uses GPIO21/GPIO22 for one display-status LCD
  and does not convert those pins into the relay-expander path.
- The rotary encoder is a menu input only and does not consume LCD pins, XBee
  bridge pins, or relay candidates.
- A later firmware pin map can choose relay expander I2C pins only after TFT,
  MicroSD, XBee, boot, UART0, and shield-routing conflicts are reviewed.
- CD74HC4067 mux channels are input observations only; any touch-derived relay
  request remains a UI intent routed through `relay_manager` and
  `safety_supervisor`.

## Unknowns

- Exact photographed ESP32 board vendor/revision and whether its header layout
  matches the expansion shield labels.
- Whether the expansion shield actually routes every visible GPIO label to the
  expected ESP32 module pin.
- Expansion shield jumper position, active power source, and regulator/current
  limits.
- Whether relay input circuitry is compatible with ESP32 logic.
- Whether the XBee carrier needs CTS/RTS, reset, sleep, or associate pins wired.
- Whether the Waveshare XBee USB Adapter header labels are safe for direct
  ESP32 connection.
- Exact LCD module, backpack IC, detected address, pullup voltage, logic
  voltage, contrast, backlight current, level-shifter direction behavior, and
  bus conflict evidence for the LCD-only test.
- Exact bench KY-040 module markings, onboard pullup values and voltage,
  debounce/noise behavior, exposed header continuity, rail-current impact,
  PF0530F live LCD menu behavior, rotation direction, and boot behavior.
- Exact MicroSD reader identity, 3.3 V power path, logic-level behavior,
  pull-up population, card-detect/write-protect behavior, and shield continuity
  for the preferred investigation pins.
- Whether a MicroSD reader or inserted card affects boot strapping, UART0
  flashing/debugging, relay candidates, or the future XBee UART path.
- Whether final enclosure routing creates EMI, isolation, or serviceability
  constraints that change the pin plan.
- Exact Open-Smart R61509V TFT pinout, power/backlight behavior, touch interface,
  bus width, and GPIO needs.
- Exact GPIO expander board, I2C address, pullups, default state, readback
  behavior, and driver-stage interface.
- Exact CD74HC4067 breakout, select/enable pins, ADC input, voltage protection,
  source impedance, and scan cadence.
