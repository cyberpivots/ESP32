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

## Provisional project mapping

This mapping is a design placeholder only. It is not approved for wiring until
the photographed ESP32 board/shield routing, relay board behavior, and XBee
carrier path are verified.

| Function | Provisional GPIO | Direction | Gate |
| --- | --- | --- | --- |
| Relay channel 1 | GPIO25 | Output | Shield routing plus relay trigger voltage/current/polarity verified |
| Relay channel 2 | GPIO26 | Output | Shield routing plus relay trigger voltage/current/polarity verified |
| Relay channel 3 | GPIO27 | Output | Shield routing plus relay trigger voltage/current/polarity verified |
| Relay channel 4 | GPIO33 | Output | Shield routing plus relay trigger voltage/current/polarity verified |
| SPI MicroSD SCK | GPIO18 | Output | Reader identity, 3.3 V power, pull-ups, shield continuity, boot-pin review, and relay/XBee conflict review verified |
| SPI MicroSD MISO | GPIO19 | Input | Reader identity, 3.3 V power, pull-ups, shield continuity, boot-pin review, and relay/XBee conflict review verified |
| SPI MicroSD MOSI | GPIO23 | Output | Reader identity, 3.3 V power, pull-ups, shield continuity, boot-pin review, and relay/XBee conflict review verified |
| SPI MicroSD CS | GPIO32 | Output | Reader identity, 3.3 V power, pull-ups, shield continuity, boot-pin review, and relay/XBee conflict review verified |
| XBee UART TX from ESP32 to DIN | Unassigned | Output | Final carrier, DIN/DOUT routing, and level compatibility verified |
| XBee UART RX from DOUT to ESP32 | Unassigned | Input | Final carrier, DIN/DOUT routing, and level compatibility verified |

Source IDs: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
`SRC-ESP32-WROOM-32-DATASHEET`, `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-UART`,
`SRC-ESP-IDF-SDSPI`, `SRC-ESP-IDF-SD-PULLUP`,
`SRC-DIGI-XBEE-PRO-900HP`, `SRC-WAVESHARE-XBEE-USB-ADAPTER`,
`SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.

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

## Avoided pins for first pass

| Pin group | Reason | Source IDs |
| --- | --- | --- |
| GPIO0, GPIO2, GPIO5, GPIO12, GPIO15 | ESP32 strapping pins need boot-state review before use. | `SRC-ESP-IDF-GPIO` |
| GPIO6 through GPIO11 | Used internally for SPI flash on ESP32-WROOM-32 and not recommended for other uses. | `SRC-ESP32-WROOM-32-DATASHEET`, `SRC-ESP-IDF-GPIO` |
| GPIO1/GPIO3 | UART0 is commonly associated with USB serial flashing/debugging paths; reserve until the photographed board USB-UART circuit is verified. | `SRC-ESP32-WROOM-32-DATASHEET`, `SRC-ESP-IDF-UART` |
| GPIO25, GPIO26, GPIO27, GPIO33 | Current relay candidates; avoid reusing them for MicroSD until relay routing is closed or reassigned. | `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`, `SRC-ESP-IDF-GPIO` |
| GPIO34 through GPIO39 | Input-only pins; not candidates for relay outputs. | `SRC-ESP-IDF-GPIO` |

## Assumptions

- GPIO25, GPIO26, GPIO27, and GPIO33 remain relay candidates because the
  photographed shield labels expose them and they are not in the avoided
  first-pass groups above.
- GPIO18, GPIO19, GPIO23, and GPIO32 are only the preferred SPI MicroSD
  investigation set. They are not approved wiring until the exact MicroSD
  reader, shield continuity, 3.3 V power, pull-ups, and boot-pin risks are
  verified.
- A later firmware pin map can choose XBee UART pins through the GPIO matrix
  after a final carrier and DIN/DOUT path are verified.

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
- Exact MicroSD reader identity, 3.3 V power path, logic-level behavior,
  pull-up population, card-detect/write-protect behavior, and shield continuity
  for the preferred investigation pins.
- Whether a MicroSD reader or inserted card affects boot strapping, UART0
  flashing/debugging, relay candidates, or the future XBee UART path.
- Whether final enclosure routing creates EMI, isolation, or serviceability
  constraints that change the pin plan.
