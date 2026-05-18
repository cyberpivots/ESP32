# Source Ledger - 2026-05-18 ESP32 Project Photo Analysis

## Scope

This ledger records visible facts from the local user upload archive
`user_uploads/esp32project.zip`. The archive was inspected in a temporary
working directory only; no JPEG binaries are copied into the repository.

Source ID: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.

## Photo inventory

| Filename | Visible facts | Unresolved electrical claims |
| --- | --- | --- |
| `IMG_5678.jpeg` | Overview showing an ESP32 development board beside a black ESP32 I/O expansion shield. | No board vendor, shield schematic, power path, or jumper behavior is proven. |
| `IMG_5679.jpeg` | ESP32 development board with a metal-can module and pin labels around the board edge. The module label is treated as ESP-WROOM-32 family evidence only. | Exact dev-board vendor/revision, USB-UART bridge, regulator, and safe power input are not proven. |
| `IMG_5680.jpeg` | Black ESP32 I/O expansion shield with barrel jack, USB connector, header sockets, `DC6.5-16V`, `USB5V`, `5V`, `3.3V`, and GPIO labels including relay-candidate GPIOs. | External input range, jumper routing, regulator current, and shield-to-board pin mapping require source or measurement. |
| `IMG_5681.jpeg` | Blue `4 Relay Module` with four blue relay cans, screw terminals, input header labels, and channel indicator components. | Trigger polarity, input current, isolation, relay supply split, and safe load limits are not proven. |
| `IMG_5682.jpeg` | Another view of the same `4 Relay Module`, showing input-side components and relay channel markings. | Board schematic, optocoupler behavior, jumper behavior, and ESP32 compatibility remain unresolved. |
| `IMG_5683.jpeg` | Relay module view showing Songle relay cans marked `SRD-05VDC-SL-C` and a `JD-VCC`/`VCC` area. | Relay board `JD-VCC`/`VCC` jumper function and isolated-power behavior require bench verification. |
| `IMG_5684.jpeg` | Waveshare `XBee USB Adapter` shown with a Digi XBee-PRO S3B radio module. | Adapter voltage selection, socket wiring, DIN/DOUT routing, and radio configuration are not proven. |
| `IMG_5685.jpeg` | Front of the Waveshare `XBee USB Adapter` with reset/boot buttons and LED labels visible; XBee-PRO S3B radio also visible. | Button behavior and usable PC serial port still require source/driver/bench verification. |
| `IMG_5686.jpeg` | Radio label shows Digi XBee-PRO S3B form factor and exact model text `XBP9B-DPUT-001 RevF`. | Firmware settings, 64-bit address, antenna path, regulatory constraints, and AES state are not proven. |
| `IMG_5687.jpeg` | Back of the Waveshare adapter shows `Waveshare` and headers labeled with UART/control/power signals including `CTS`, `RTS`, `RXD`, `TXD`, `GND`, `3.3V`, and `5V`. | Whether those headers are safe for direct ESP32 connection needs voltage and continuity verification. |

## Visible facts

- The current photographed ESP32 target is an ESP32 development board populated
  with an ESP-WROOM-32-family module, not a verified Espressif ESP32-DevKitC V4.
- The photographed expansion shield exposes labeled GPIO positions including
  `GPIO25`, `GPIO26`, `GPIO27`, and `GPIO33`, so those relay GPIO candidates
  remain plausible but provisional.
- The relay hardware is a blue four-channel module populated with Songle
  `SRD-05VDC-SL-C` relay cans.
- The radio hardware label visibly identifies Digi `XBP9B-DPUT-001 RevF`.
- The first photographed XBee PC dock is a Waveshare `XBee USB Adapter`.

Source ID: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.

## Source-backed context

- Espressif's ESP32-WROOM-32 datasheet is the module-level source for
  ESP32-WROOM-32 supply, pin, GPIO, boot, and electrical constraints. Source ID:
  `SRC-ESP32-WROOM-32-DATASHEET`.
- Waveshare documents the XBee USB Adapter as a UART communication board with
  USB and XBee interfaces for testing, programming, configuring, and debugging.
  Source ID: `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- The Songle datasheet mirror covers the `SRD-05VDC-SL-C` relay component
  family and contact-rating context. Source ID: `SRC-SONGLE-SRD-05VDC-SL-C`.

## Assumptions

- The user-selected active target for this documentation pass is the
  photographed hardware set.
- The local upload archive remains a user-provided evidence artifact and should
  not be committed as repository source.
- The Waveshare adapter is the first PC configuration/debug dock for the XBee
  module, not the final ESP32-mounted carrier.

## Unresolved gaps

- Exact ESP32 dev-board vendor, revision, USB-UART bridge, regulator, and
  reset/boot circuit.
- Expansion-shield jumper position, power input source, regulator capability,
  and whether the shield routes every visible GPIO to the expected board pin.
- Relay module trigger polarity, 3.3 V logic compatibility, input current,
  `JD-VCC`/`VCC` behavior, isolation boundary, and safe load design.
- XBee adapter UART voltage, DIN/DOUT continuity, reset/sleep/flow-control
  routing, and whether it should ever be used as an ESP32-mounted carrier.
- XBee radio firmware state, API settings, AES state, 64-bit address, antenna
  path, and regulatory constraints.
