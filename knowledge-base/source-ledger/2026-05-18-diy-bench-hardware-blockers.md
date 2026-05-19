# Source Ledger - 2026-05-18 DIY Bench Hardware Blockers

## Scope

This ledger turns the photographed `four-relay-xbee-wifi` hardware set into a
documentation-only blocker list for staged DIY bench work. It does not approve
live wiring, relay switching, firmware flashing, XBee configuration writes, or
mains switching.

## Verified facts

- The current target hardware remains the photographed ESP-WROOM-32-family
  development board on an ESP32 I/O expansion shield, blue four-channel relay
  module with Songle `SRD-05VDC-SL-C` relay cans, Digi `XBP9B-DPUT-001 RevF`,
  and Waveshare XBee USB Adapter. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Espressif's ESP32-WROOM-32 datasheet and ESP32 hardware design guidelines are
  the current source-backed references for ESP32 module supply, GPIO, UART,
  reset, and strapping-pin review. Source IDs:
  `SRC-ESP32-WROOM-32-DATASHEET`,
  `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.
- The TaiwanIOT expansion-board page is only a non-authoritative candidate
  identity source for a similar NodeMCU ESP32 expansion board class; it does
  not verify the photographed shield's exact revision, schematic, regulator, or
  jumper behavior. Source ID: `SRC-ESP32-IO-SHIELD-CANDIDATE`.
- The Songle relay source covers the relay component family only; it does not
  verify the photographed relay module input circuit, trigger polarity, input
  current, `JD-VCC`/`VCC` jumper behavior, or isolation boundary. Source ID:
  `SRC-SONGLE-SRD-05VDC-SL-C`.
- Waveshare documents the XBee USB Adapter as a UART communication board with
  USB and XBee interfaces for testing and configuration/debug use. Source ID:
  `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- Digi identifies the photographed `XBP9B-DPUT-001` radio family and its
  XBee-PRO 900HP context. Source IDs: `SRC-DIGI-XBP9B-DPUT-001`,
  `SRC-DIGI-XBEE-PRO-900HP`.
- NIOSH and OSHA safety references support a hard mains-readiness gate around
  qualified-person work, de-energization, lockout, voltage verification,
  GFCI/grounding concepts, and protective-device review; they are not DIY mains
  wiring instructions. Source IDs: `SRC-NIOSH-ELECTRICAL-SAFETY`,
  `SRC-OSHA-DEENERGIZED-WORK`, `SRC-OSHA-GFCI`, `SRC-OSHA-AEGCP`,
  `SRC-OSHA-GROUNDING-OVERCURRENT`.
- NEMA maintains enclosure standards and enclosure type references for
  electrical equipment; no enclosure type is selected for this project. Source
  ID: `SRC-NEMA-ENCLOSURES`.
- CD74HC4067 is an input-only mux candidate, while TCA9555/MCP23017 provide the
  relay expander planning path and TPIC6B595 remains a driver-stage reference.
  Source IDs: `SRC-TI-CD74HC4067`, `SRC-TI-TCA9555`,
  `SRC-ESPRESSIF-MCP23017-COMPONENT`, `SRC-TI-TPIC6B595`.
- External R61509V sources provide TFT pin-pressure context only. Source IDs:
  `SRC-NOPNOP2002-ESP-IDF-PARALLEL-TFT`,
  `SRC-LCDWIKI-R61509V-MRB2802`.

## Assumptions

- The next useful work is documentation and non-mutating bench inspection, not
  firmware implementation or load wiring.
- Prototype relay contacts remain disconnected or attached only to a reviewed
  low-voltage dummy load until a load safety design is reviewed.
- The Waveshare XBee USB Adapter is a PC-side dock for read-only discovery in
  this pass, not an ESP32-mounted carrier.
- Relay GPIO candidates remain `GPIO25`, `GPIO26`, `GPIO27`, and `GPIO33`
  until shield continuity or board fit evidence invalidates them.
- The relay expansion branch is preferred if TFT pin pressure remains in scope.

## Unknowns

- Exact ESP32 dev-board vendor, revision, USB-UART bridge, regulator, boot/reset
  circuit, and installed module variant.
- Exact expansion-shield revision, schematic, jumper position, power source,
  regulator output/current capability, and shield-to-board GPIO continuity.
- Exact relay module manufacturer/model, input voltage, trigger polarity, input
  current, 3.3 V compatibility, coil supply path, `JD-VCC`/`VCC` behavior, and
  isolation design.
- Exact Waveshare adapter revision, host serial port, driver state, DIN/DOUT
  direction naming, UART voltage, reset/sleep/flow-control routing, and RF
  transmit current budget.
- Final load type, load voltage/current, enclosure, overcurrent protection,
  grounding/bonding, strain relief, GFCI/de-energization process, and qualified
  electrical review outcome.
- Exact Open-Smart R61509V module, pinout, power/backlight, touch interface, and
  driver path.
- Exact CD74HC4067 breakout, ADC protection, input list, and scan behavior.
- Exact relay expander, I2C pullups/address, inactive defaults, output readback,
  and driver-stage choice.

## Closure ledger

| Blocker | Closure evidence required | Current status |
| --- | --- | --- |
| ESP32 board identity | Photo/inspection record or exact vendor source identifying board revision, USB-UART bridge, regulator, boot/reset circuit, and module marking. | Unresolved gap |
| Expansion shield power | Source or measured record for active input, jumper position, no dual-power conflict, output voltage, regulator behavior, and current budget. | Unresolved gap |
| Expansion shield routing | Continuity record proving each candidate shield label reaches the expected ESP32 board pin without shorts or swaps. | Unresolved gap |
| Relay trigger polarity | Source or measured result showing active-high or active-low behavior for each input. | Unresolved gap |
| Relay input current | Source or measured result for input current per channel in the actual drive condition. | Unresolved gap |
| Relay 3.3 V compatibility | Measurement showing direct ESP32 3.3 V GPIO drive is reliable and within a source-backed GPIO current limit; otherwise future driver-stage design is required. | Unresolved gap |
| Relay `JD-VCC`/`VCC` behavior | Source, schematic, or measured result proving coil/logic supply relationship and whether opto-isolation is preserved or bypassed. | Unresolved gap |
| TFT module proof | Exact Open-Smart R61509V module source/inspection, power/backlight, bus width, touch path, and pin-conflict review. | Unresolved gap |
| CD74HC4067 input proof | Exact breakout, select/enable wiring, ADC1 test-voltage proof, voltage protection, and input-only behavior. | Unresolved gap |
| Relay expander proof | Exact MCP23017/TCA9555 board, I2C address/pullups, inactive defaults, LED/logic-analyzer latch proof, and readback/fault policy. | Unresolved gap |
| Relay driver-stage proof | Driver selection after exact relay input polarity/current/voltage/isolation evidence. | Blocked until relay input proof |
| Waveshare PC dock discovery | Host serial-port record, driver/tool record, read-only radio identity, voltage measurement, and no setting-write evidence. | Unresolved gap |
| Waveshare ESP32-mounted role | Carrier decision, voltage/routing/current evidence, and owner review. | Blocked; out of scope for this pass |
| Mains readiness | Enclosure, overcurrent protection, grounding/bonding, strain relief, GFCI/de-energization, load type, and qualified review evidence. | Hard blocked |

## Blocked actions

- Do not wire relay contacts to mains or inductive loads.
- Do not power the expansion shield from barrel jack and USB at the same time.
- Do not wire ESP32 GPIO directly to relay inputs until the relay 3.3 V/current
  gate is closed.
- Do not use CD74HC4067 as direct relay output state holding.
- Do not connect MCP23017/TCA9555 outputs or any driver-stage output to relay
  module inputs before relay trigger/current/voltage/isolation evidence exists.
- Do not wire the Open-Smart R61509V TFT before exact module power/pinout and
  pin-conflict evidence exists.
- Do not move the Waveshare adapter from PC dock role to ESP32 carrier role
  without a separate carrier review.
- Do not write XBee settings during read-only discovery.
