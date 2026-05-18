# ESP32 DevKitC Reference Profile

## Status

Source-backed reference and prior project assumption. The current photographed
`four-relay-xbee-wifi` target is tracked in
`hardware-profiles/esp32/esp-wroom-32-dev-board/README.md`, because the photo
archive does not verify that the physical board is an Espressif ESP32-DevKitC
V4.

## Verified facts

- Espressif's ESP32-DevKitC V4 guide describes a small ESP32-based development
  board with most ESP module I/O pins broken out to side headers. Source ID:
  `SRC-ESP32-DEVKITC`.
- ESP32-DevKitC V4 has multiple ESP32 module variants and male or female header
  configurations. Source ID: `SRC-ESP32-DEVKITC`.
- ESP32-DevKitC V4 power options are mutually exclusive: Micro USB, 5V/GND
  header pins, or 3V3/GND header pins. Source ID: `SRC-ESP32-DEVKITC`.
- Espressif's GPIO documentation identifies ESP32 physical GPIOs and notes GPIO
  matrix routing for peripheral input/output signals. Source ID:
  `SRC-ESP-IDF-GPIO`.
- ESP32-DevKitC V4 documentation marks GPIO6 through GPIO11 flash-related pins
  as pins to avoid because using them may disrupt SPI flash/SPI RAM access.
  Source ID: `SRC-ESP32-DEVKITC`.
- ESP32-DevKitC V4 documentation says GPIO16/GPIO17 availability depends on the
  module variant: available on boards with ESP32-WROOM or ESP32-SOLO-1 modules,
  reserved internally on boards with ESP32-WROVER modules. Source ID:
  `SRC-ESP32-DEVKITC`.

## Prior provisional project use

| Project signal | Provisional pin | Status |
| --- | --- | --- |
| Relay channel 1 | GPIO25 | Prior placeholder; current target blocks wiring on photographed shield and relay verification |
| Relay channel 2 | GPIO26 | Prior placeholder; current target blocks wiring on photographed shield and relay verification |
| Relay channel 3 | GPIO27 | Prior placeholder; current target blocks wiring on photographed shield and relay verification |
| Relay channel 4 | GPIO33 | Prior placeholder; current target blocks wiring on photographed shield and relay verification |
| XBee UART TX | GPIO21 | Prior placeholder; current target has no final ESP32 XBee carrier/pin selection |
| XBee UART RX | GPIO22 | Prior placeholder; current target has no final ESP32 XBee carrier/pin selection |

Source IDs: `SRC-ESP32-DEVKITC`, `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-UART`.

## Assumptions

- This profile remains useful as an Espressif reference when comparing the
  photographed board against DevKitC V4 documentation.
- UART0 remains reserved for USB serial flashing/debugging in the first pass.

## Unknowns

- Whether any physical board in hand is genuine ESP32-DevKitC V4 or compatible
  with this reference.
- Whether the photographed ESP-WROOM-32 development board matches this header
  layout.
- Header gender/layout and breadboard/cable constraints.
- Actual serial port mapping in the development environment.
- Any board-level modifications, damaged pins, or attached peripherals.

## Bring-up blockers

- Do not wire relay inputs until the relay board electrical profile is closed.
- Do not connect XBee DIN/DOUT until the carrier board and voltage path are
  verified.
- Do not power the board from more than one source at a time.
