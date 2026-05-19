# Known Gaps

## High priority

- Confirm exact firmware framework requirements and constraints for projects not
  covered by ADR-0002.
- Install or locate ESP-IDF v6.0.1, `idf.py`, esptool, CMake, and Ninja before
  firmware implementation for `four-relay-xbee-wifi`.
- Identify exact photographed ESP32 development board vendor/revision, USB-UART
  bridge, regulator, expansion-shield schematic, jumper position, and GPIO
  continuity for `four-relay-xbee-wifi`.
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
- Create a separate qualified-review package before any mains switching design:
  load type, enclosure, overcurrent protection, grounding/bonding, strain
  relief, GFCI/de-energization, separation, labels/disconnect, and test record.
- Define first flashing target board and recovery method.

## Medium priority

- Select first protocol to implement.
- Add XBee API parser test vectors for escaped API frames, status frames, and
  reject reasons.
- Define CI matrix after the firmware framework is selected.

## Closure criteria

Each gap closes only when supported by a source-index entry, physical inspection
record, ADR, or test artifact.
