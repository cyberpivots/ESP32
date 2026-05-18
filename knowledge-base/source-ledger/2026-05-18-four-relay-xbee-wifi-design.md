# Source Ledger - 2026-05-18 Four Relay XBee Wi-Fi Design

## Scope

Source-backed design package for the photographed ESP-WROOM-32 development
board plus ESP32 I/O expansion shield, a four-channel Songle relay module
candidate, Digi XBee-PRO 900HP S3B `XBP9B-DPUT-001 RevF`, Waveshare XBee USB
Adapter PC dock, and a local Wi-Fi HTML control surface.

## Verified facts

- ESP-IDF stable documentation for ESP32 resolves to v6.0.1 and identifies
  ESP-IDF as Espressif's official development framework for ESP32-series SoCs.
  Source IDs: `SRC-ESP-IDF-STABLE-ESP32`, `SRC-ESP-IDF-GET-STARTED`.
- ESP-IDF stable documentation covers Wi-Fi AP mode, HTTP server URI handlers,
  GPIO/GPIO matrix, UART controllers, and NVS key-value storage. Source IDs:
  `SRC-ESP-IDF-WIFI`, `SRC-ESP-IDF-HTTP-SERVER`, `SRC-ESP-IDF-GPIO`,
  `SRC-ESP-IDF-UART`, `SRC-ESP-IDF-NVS`.
- ESP32-DevKitC V4 exposes many ESP32 I/O pins on headers and exists in
  multiple module/header variants. It remains a prior reference, not the current
  photographed target. Source ID: `SRC-ESP32-DEVKITC`.
- The photo archive identifies an ESP-WROOM-32-family development board, ESP32
  I/O expansion shield, blue `4 Relay Module`, Songle `SRD-05VDC-SL-C` relay
  cans, Digi `XBP9B-DPUT-001 RevF` radio label, and Waveshare `XBee USB
  Adapter`. Source ID: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Espressif's ESP32-WROOM-32 datasheet supplies module-level context for the
  photographed ESP-WROOM-32 module family. Source ID:
  `SRC-ESP32-WROOM-32-DATASHEET`.
- Waveshare documents the XBee USB Adapter as a UART communication board with
  USB and XBee interfaces. Source ID: `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- The Songle datasheet mirror provides component-level context for
  `SRD-05VDC-SL-C` relays. Source ID: `SRC-SONGLE-SRD-05VDC-SL-C`.
- Digi identifies `XBP9B-DPUT-001` as an XBee-PRO 900HP S3B Point2Multipoint,
  900 MHz, 250 mW, U.FL, 10 kbps model. Source ID:
  `SRC-DIGI-XBP9B-DPUT-001`.
- Digi's 900HP product material lists UART (3V) and SPI data interfaces and
  includes point-to-multipoint as a supported topology. Source ID:
  `SRC-DIGI-XBEE-PRO-900HP`.
- Digi AP command documentation defines API mode values 0, 1, and 2; value 2 is
  API mode with escaped sequences. Source ID: `SRC-DIGI-XBEE-900HP-AP`.
- Digi AO command documentation identifies standard receive output as API Rx
  Indicator `0x90` when AO is 0. Source ID: `SRC-DIGI-XBEE-900HP-AO`.
- Digi's user guide covers Transmit Request `0x10`, Transmit Status `0x89`,
  Receive Packet `0x90`, checksum behavior, and AES security commands. Source
  ID: `SRC-DIGI-XBEE-900HP-USER-GUIDE`.
- Current shell probe found Python 3.12.3 and Git 2.43.0; `idf.py`,
  `esptool.py`, CMake, Ninja, and XCTU were not found on PATH. Source ID:
  `SRC-LOCAL-TOOLCHAIN-PROBE-2026-05-18`.

## Assumptions

- The first firmware implementation can target ESP-IDF v6.0.1 for this project
  without adding firmware source or framework project files in this design
  pass.
- The photographed ESP-WROOM-32 board plus expansion shield replaces DevKitC as
  the active physical target, while DevKitC remains a reference profile.
- Relay-changing HTTP endpoints should be treated as disabled until an admin
  token/passphrase is provisioned in NVS and confirmed by firmware tests.
- The first radio payload format can be a compact JSON object carried inside
  XBee API RF data until parser tests prove a smaller binary encoding is needed.
- The Waveshare XBee USB Adapter is a PC configuration/debug dock candidate, not
  the final ESP32-mounted XBee carrier.

## Unresolved gaps

- Exact ESP32 dev-board vendor/revision, USB-UART bridge, regulator, expansion
  shield schematic, jumper position, power path, and GPIO continuity.
- Exact four-channel relay module board manufacturer/model, input voltage,
  trigger polarity, input current, `JD-VCC`/`VCC` behavior, isolation design,
  coil/current path, and load rating.
- Whether the Waveshare XBee USB Adapter is only a PC dock or can be used as any
  ESP32-mounted carrier; adapter power feed, reset/sleep pins, DIN/DOUT wiring,
  UART voltage, and optional CTS/RTS wiring.
- Load type, load voltage, enclosure, fusing, snubber/surge suppression,
  earthing/grounding, and mains/inductive-load safety design.
- ESP-IDF, esptool, CMake, Ninja, and Digi XBee tooling installation path on the
  intended development shell.
