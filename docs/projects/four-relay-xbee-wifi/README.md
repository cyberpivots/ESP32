# Four Relay XBee Wi-Fi Controller

## Goal

Design the first ESP32 project package around the photographed hardware: an
ESP-WROOM-32 development board on an ESP32 I/O expansion shield, a four-channel
Songle relay module candidate, local Wi-Fi control, and Digi XBee-PRO 900HP S3B
telemetry/control over the photographed `XBP9B-DPUT-001 RevF` radio.

## Package map

- [Architecture](architecture.md)
- [Prototype blueprint](prototype-blueprint.md)
- [Bench bring-up runbook](bench-bring-up-runbook.md)
- [Mains readiness gate](mains-readiness-gate.md)
- [Power and safety gates](power-and-safety.md)
- [Pin plan](pin-plan.md)
- [Firmware task model](firmware-task-model.md)
- [Web interface](web-interface.md)
- [Static admin HMI](ui/index.html)
- [SPI MicroSD reader profile](../../../hardware-profiles/storage/spi-microsd-reader/README.md)
- [SPI MicroSD assets and logs ledger](../../../knowledge-base/source-ledger/2026-05-18-spi-microsd-assets-logs.md)

## Verified facts

- ESP-IDF stable v6.0.1 is the project framework target accepted by ADR-0002.
  Source IDs: `SRC-ESP-IDF-STABLE-ESP32`, `SRC-ESP-IDF-GET-STARTED`.
- ESP-IDF stable documentation covers Wi-Fi AP mode, HTTP server URI handlers,
  GPIO/GPIO matrix, UART controllers, NVS storage, FatFS/VFS, and SDSPI
  storage for the required project surfaces. Source IDs: `SRC-ESP-IDF-WIFI`,
  `SRC-ESP-IDF-HTTP-SERVER`, `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-UART`,
  `SRC-ESP-IDF-NVS`, `SRC-ESP-IDF-FATFS`, `SRC-ESP-IDF-SDSPI`.
- Digi identifies the requested XBee model as `XBP9B-DPUT-001`, an
  XBee-PRO 900HP S3B Point2Multipoint 900 MHz, 250 mW, U.FL, 10 kbps part.
  Source ID: `SRC-DIGI-XBP9B-DPUT-001`.
- The user-uploaded photo archive shows an ESP-WROOM-32-family development
  board, black ESP32 I/O expansion shield, blue `4 Relay Module`, Songle
  `SRD-05VDC-SL-C` relay cans, Digi `XBP9B-DPUT-001 RevF` radio label, and
  Waveshare `XBee USB Adapter`. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Espressif's ESP32-WROOM-32 datasheet is the module-level source for the
  photographed ESP-WROOM-32 module family. Source ID:
  `SRC-ESP32-WROOM-32-DATASHEET`.
- Espressif's ESP32 hardware design guidelines add source-backed review points
  for ESP32 3.3 V supply/current, reset timing, UART, strapping pins, and GPIO.
  Source ID: `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.
- A third-party NodeMCU ESP32 expansion-board page is a non-authoritative
  candidate identity source for a similar shield class only; it does not prove
  the photographed shield revision, schematic, regulator, or safe power path.
  Source ID: `SRC-ESP32-IO-SHIELD-CANDIDATE`.
- Waveshare documents the XBee USB Adapter as a UART communication board with
  XBee and USB interfaces for testing, programming/configuration, and
  USB-to-UART use. Source ID: `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- The Songle `SRD-05VDC-SL-C` relay datasheet mirror provides component-level
  relay context only. Source ID: `SRC-SONGLE-SRD-05VDC-SL-C`.
- NIOSH, OSHA, and NEMA sources support the mains-readiness gate around
  qualified review, de-energization, GFCI/grounding context, overcurrent
  protection review, and enclosure selection. Source IDs:
  `SRC-NIOSH-ELECTRICAL-SAFETY`, `SRC-OSHA-DEENERGIZED-WORK`,
  `SRC-OSHA-GFCI`, `SRC-OSHA-AEGCP`, `SRC-OSHA-GROUNDING-OVERCURRENT`,
  `SRC-NEMA-ENCLOSURES`.

## Assumptions

- The first Wi-Fi control mode is ESP32 SoftAP so a bench browser can connect
  directly without depending on site infrastructure.
- Relay state-changing endpoints remain disabled unless an admin
  token/passphrase is provisioned in NVS and the runtime safety lock is open.
- XBee application payloads start as compact JSON objects inside API RF data;
  parser tests can later replace this with a binary schema if needed.
- DevKitC is no longer the assumed physical target for this project; it remains
  a source-backed reference until the photographed board is matched to a vendor
  or reference schematic.
- The Waveshare XBee USB Adapter is the first PC-side configuration/debug dock,
  not the final ESP32-mounted XBee carrier.
- The DIY prototype path starts with board/shield inspection, then relay-module
  verification with relay contacts disconnected, then XBee read-only discovery
  from the PC dock.

## Unknowns

- Exact ESP32 development board vendor/revision, regulator, USB-UART bridge,
  and expansion-shield schematic.
- Expansion shield jumper position, power input source, and verified routing of
  GPIO labels to the ESP32 board.
- Exact four-channel relay module board manufacturer/model and electrical
  behavior.
- Relay trigger polarity, input current, 3.3 V compatibility, `JD-VCC`/`VCC`
  behavior, and isolation design.
- Whether the Waveshare XBee USB Adapter can be used beyond PC configuration;
  final ESP32-mounted carrier and wiring remain unresolved.
- Load type, load voltage, enclosure, fusing, and isolation design.
- Exact SPI MicroSD reader module, power path, pull-ups, shield continuity,
  boot-pin effects, card format, and log-retention policy.
- Installed ESP-IDF and XBee configuration tooling on the target development
  machine.
- Mains readiness evidence: qualified review, load definition, enclosure,
  overcurrent protection, grounding/bonding, strain relief,
  GFCI/de-energization process, and test record.

## Hard gate

No relay wiring, load switching, XBee configuration writes, or firmware flashing
is approved by this package. Those steps require physical verification records
and owner review.

Mains switching remains hard blocked by
[mains-readiness-gate.md](mains-readiness-gate.md).
