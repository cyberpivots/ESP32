# Pin Risk Matrix

## Verified facts

- ESP32 GPIO source coverage identifies GPIO review requirements, strapping
  considerations, input-only pins, flash/PSRAM caveats, and UART0 flashing/debug
  context. Source ID: `SRC-ESP-IDF-GPIO`.
- ESP32 UART source coverage exists for UART controller review. Source ID:
  `SRC-ESP-IDF-UART`.
- The exact ESP32 board and carrier are unresolved, so no pin assignment is
  accepted for this project. Source ID:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`.

## Assumptions

- The pin plan should preserve boot/recovery first, then low-risk observability,
  then optional peripherals.
- Pullups, level domains, and default states matter as much as signal count.

## Matrix

| Interface | Candidate signals | Primary risk | Required evidence before assignment |
| --- | --- | --- | --- |
| 20x4 I2C LCD | SDA, SCL, backlight control if exposed | Pullup voltage, I2C address conflict, backlight current, boot-pin effects | Exact LCD/backpack profile and board pin map |
| Rotary encoder | A, B, switch, optional common | Pullup/down choice, debounce, boot-pin interaction, wake behavior | Exact encoder profile and low-voltage input plan |
| XBee UART | DIN, DOUT, reset/sleep/CTS/RTS if used | DIN/DOUT naming ambiguity, UART voltage, boot/debug conflict, carrier power | Carrier source, adapter/carrier inspection, read-only proof |
| Charger status | Status, power-good, fault pins if exposed | Logic voltage, open-drain behavior, pullups, charger-board variation | Exact charger module schematic/source |
| Fuel gauge | SDA, SCL, alert if used | I2C pullup sharing, address conflict, chemistry configuration | Exact gauge selection and battery source |
| Battery measurement | ADC or gauge path | Divider leakage, maximum voltage, calibration, unsafe direct cell connection | Exact measurement design and safety review |
| Boot/recovery | EN, BOOT, UART0, strapping pins | Bricked or unreliable boot if peripherals force states | Exact ESP32 board source and recovery record |

## Unknowns

- Final ESP32 board pinout, exposed headers, and carrier constraints.
- Whether LCD and fuel gauge share an I2C bus.
- Whether XBee uses hardware flow control.
- Whether charger status pins or fuel gauge are required at all.

## Stop gates

No GPIO, I2C, ADC, or UART pin is assigned by this matrix. Do not wire any
peripheral until the exact board, exact module, pullup/voltage state, and
boot/recovery review exist.
