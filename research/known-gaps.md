# Known Gaps

## High priority

- Confirm exact firmware framework requirements and constraints for projects not
  covered by ADR-0002.
- Install or locate ESP-IDF v6.0.1, `idf.py`, esptool, CMake, and Ninja before
  firmware implementation for `four-relay-xbee-wifi`.
- Identify exact photographed ESP32 development board vendor/revision, USB-UART
  bridge, regulator, expansion-shield schematic, jumper position, and GPIO
  continuity for `four-relay-xbee-wifi`.
- Define source-backed power-entry/protection requirements for
  `four-relay-xbee-wifi`: single selected input source, rail budget, current
  limit, brownout behavior, reverse-protection need, overcurrent protection,
  TVS/ESD placement, and test points.
- Identify exact four-channel relay module manufacturer/model, input voltage,
  trigger polarity, 3.3 V compatibility, `JD-VCC`/`VCC` behavior, isolation
  method, coil/load ratings, and current requirements.
- Close or explicitly block the relay direct-GPIO 3.3 V/current gate for
  `GPIO25`, `GPIO26`, `GPIO27`, and `GPIO33`.
- Verify the exact Open-Smart R61509V TFT module, pinout, power/backlight,
  touch interface, driver path, and conflict with relay, MicroSD, XBee, ADC,
  boot, flash, and UART0 pins.
- Verify exact CD74HC4067 breakout, select/enable wiring, ADC1 input path,
  voltage protection, source impedance, and input-only scan behavior.
- Select and verify exact MCP23017 or TCA9555 expander board, I2C address pins,
  pullups, inactive defaults, output latch behavior, and readback policy.
- Select a relay driver stage only after exact relay-module trigger polarity,
  input current, voltage compatibility, and isolation behavior are verified.
- Confirm Heltec WiFi LoRa 32(V2) physical revision and radio chip variant.
- Verify Waveshare XBee USB Adapter serial port, UART voltage, DIN/DOUT routing,
  and whether it is only a PC dock or also a possible ESP32-mounted carrier.
- Run the XBee read-only bench proof Tier A, then optionally Tier B with
  `--confirm-sends-read-commands`, to capture `VR`, `HV`, `SH`, `SL`, `AP`,
  `AO`, `BD`, and `NP` without setting writes.
- Identify the SPI MicroSD reader module, 3.3 V power path, pull-ups,
  card-detect/write-protect behavior, and shield continuity for candidate
  `GPIO18`, `GPIO19`, `GPIO23`, and `GPIO32` before any storage wiring.
- Define MicroSD card capacity, FAT preparation process, low-space behavior,
  log rotation, and fallback web-serving behavior for
  `four-relay-xbee-wifi`.
- Inventory required bench instruments and fixtures for `four-relay-xbee-wifi`:
  DMM, current-limited supply, logic analyzer or LED proof fixture, USB serial
  tools, labeled harnesses, low-voltage dummy loads, and completed records
  based on `research/bench-records/TEMPLATE.md`.
- Create a separate qualified-review package before any mains switching design:
  load type, enclosure, overcurrent protection, grounding/bonding, strain
  relief, GFCI/de-energization, separation, labels/disconnect, and test record.
- Define first flashing target board and recovery method.

## Medium priority

- Select first protocol to implement.
- Add XBee API parser test vectors beyond the current escaped-frame,
  bad-length, truncated-escape, checksum, transmit-status, AT-response, and
  receive-packet payload host vectors.
- Decide whether modular scaffold audits should become a CI matrix job after
  the local-only verifier proves stable.
- Define CI matrix after the firmware framework is selected.

## Next evidence record required

| Blocker | Required evidence record before closure |
| --- | --- |
| Framework requirements outside ADR-0002 | Accepted ADR or explicit unresolved-gap note naming the project and blocked framework decision. |
| ESP-IDF v6.0.1 toolchain | Local toolchain record covering `idf.py`, esptool, CMake, Ninja, Python, shell path, and failure text if absent. |
| Exact ESP32 board and expansion shield | Physical inspection record with board markings, USB-UART marking, regulator marking, jumper position, continuity notes, and source links where available. |
| Power entry and protection | Bench power record with selected input source, rail measurements, current-limit setting, brownout observation, reverse-protection decision, overcurrent candidate, TVS/ESD candidate, and test points. |
| Four-channel relay module | Module identity record with manufacturer/model markings, input voltage, trigger polarity, 3.3 V input current measurement, `JD-VCC`/`VCC` behavior, isolation notes, and contact-rating source. |
| Direct GPIO relay gate | Low-voltage proof record for `GPIO25`, `GPIO26`, `GPIO27`, and `GPIO33` showing no load/mains connection and measured relay-input behavior. |
| Open-Smart R61509V TFT | Module identity and pin-pressure record with exact pinout, supply/backlight requirements, touch interface, driver path, and shared pin-budget impact. |
| CD74HC4067 mux | Breakout identity and input-only scan record with select/enable wiring, ADC1 path, voltage protection, source impedance, and no relay-output claims. |
| MCP23017 or TCA9555 expander | Expander board identity record with address pins, pullups, inactive default, latch/readback behavior, and driver-stage boundary. |
| Relay driver stage | Driver selection record tied to measured relay input polarity, input current, voltage compatibility, and isolation behavior. |
| Heltec WiFi LoRa 32(V2) | Physical revision record with board photos/markings and radio-chip/source confirmation. |
| Waveshare XBee USB Adapter | Adapter/carrier record with serial port, UART voltage, DIN/DOUT routing, and PC-dock versus ESP32-mounted-carrier decision. |
| XBee read-only bench proof | Tier A passive record and optional Tier B `VR`, `HV`, `SH`, `SL`, `AP`, `AO`, `BD`, `NP` read record with `--confirm-sends-read-commands`. |
| MicroSD reader and card policy | Reader identity and card-prep record with 3.3 V path, pullups, card-detect/write-protect behavior, shield continuity, capacity, FAT preparation, low-space handling, rotation, and fallback behavior. |
| Bench instruments and fixtures | Instrument inventory record covering DMM, current-limited supply, logic analyzer or LED proof fixture, USB serial tools, labeled harnesses, low-voltage dummy loads, and calibration/identity notes. |
| Qualified mains package | Qualified-review package for load type, enclosure, overcurrent protection, grounding/bonding, strain relief, GFCI/de-energization, separation, labels/disconnect, and test record. |
| First flashing target board | Flash target and recovery record with exact board, boot/recovery method, toolchain proof, and rollback path. |

## Closure criteria

Each gap closes only when supported by a source-index entry, physical inspection
record, ADR, or test artifact.
