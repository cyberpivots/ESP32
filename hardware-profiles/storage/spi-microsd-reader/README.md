# SPI MicroSD Reader Profile

## Scope

This profile covers the first storage expansion path for
`four-relay-xbee-wifi`: a generic SPI MicroSD reader used for static web assets
and append-only event logs. It does not identify or approve a specific reader,
shield header, wiring harness, or firmware implementation.

## Verified facts

- ESP-IDF FatFS support exposes mounted FAT volumes through VFS so standard C
  library and POSIX-style file APIs can access paths under a selected mount
  path such as `/sdcard`. Source ID: `SRC-ESP-IDF-FATFS`.
- ESP-IDF provides SD-card mount helpers for SDMMC and SDSPI-backed FAT
  volumes. Source ID: `SRC-ESP-IDF-FATFS`.
- ESP-IDF SDSPI uses the SPI Master driver and can route SPI signals through
  the GPIO matrix, which makes pin selection more flexible than SDMMC 1-bit or
  4-bit modes. Source ID: `SRC-ESP-IDF-SDSPI`.
- Espressif documents SDSPI as lower-throughput than SDMMC host access. Source
  ID: `SRC-ESP-IDF-SDSPI`.
- Espressif SD pull-up guidance applies to SPI and SDMMC communication with SD
  cards and records required pull-ups and boot/strapping conflicts that must be
  reviewed for ESP32 boards. Source ID: `SRC-ESP-IDF-SD-PULLUP`.
- The ESP-IDF SDSPI example supports SD, SDHC, and SDXC cards and warns that
  formatting can delete card data. Source ID: `SRC-ESP-IDF-SDSPI-EXAMPLE`.
- The current project relay candidates are `GPIO25`, `GPIO26`, `GPIO27`, and
  `GPIO33`, and direct relay wiring remains blocked until relay and shield
  verification close. Source IDs: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
  `SRC-ESP-IDF-GPIO`.
- ESP32 `GPIO6` through `GPIO11` remain avoided because they are flash-related
  pins in the existing project pin plan. Source IDs:
  `SRC-ESP32-WROOM-32-DATASHEET`, `SRC-ESP-IDF-GPIO`.

## Assumptions

- The first reader under investigation is a common SPI MicroSD reader module,
  not an SDMMC socket or a specific vendor shield.
- Static assets are copied to the card by a host computer before insertion; the
  ESP32 serves them read-only during normal operation.
- Event logs are append-only JSONL files written by firmware only after the SD
  card is mounted read/write.
- NVS remains the authoritative store for admin credential state, safety
  settings, relay polarity, and radio allowlists.

## Preferred investigation pins

These pins are only a continuity and risk-review target. They are not approved
for wiring until the exact reader, photographed expansion shield routing,
3.3 V power, pull-ups, boot-pin behavior, and relay/XBee conflicts are verified.

| SPI signal | Investigation GPIO | Status |
| --- | --- | --- |
| SCK | `GPIO18` | Unapproved candidate |
| MISO | `GPIO19` | Unapproved candidate |
| MOSI | `GPIO23` | Unapproved candidate |
| CS | `GPIO32` | Unapproved candidate |

Source IDs: `SRC-ESP-IDF-SDSPI`, `SRC-ESP-IDF-GPIO`,
`SRC-ESP32-WROOM-32-DATASHEET`, `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`,
`SRC-ESP-IDF-SD-PULLUP`.

## Avoided pins

| Pin group | Reason | Status |
| --- | --- | --- |
| `GPIO6` through `GPIO11` | Flash-related pins in the current ESP32-WROOM-32 project plan. | Blocked |
| `GPIO25`, `GPIO26`, `GPIO27`, `GPIO33` | Current relay candidates; keep clear until relay/shield routing closes. | Blocked for MicroSD first pass |
| `GPIO1`, `GPIO3` | UART0 is reserved until the photographed board USB-UART circuit is verified. | Blocked for MicroSD first pass |
| `GPIO0`, `GPIO2`, `GPIO5`, `GPIO12`, `GPIO15` | Strapping pins require boot-state review before use. | Blocked for MicroSD first pass |

Source IDs: `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-UART`,
`SRC-ESP32-WROOM-32-DATASHEET`, `SRC-ESP-IDF-SD-PULLUP`.

## Unknowns

- Exact MicroSD reader vendor, revision, regulator path, logic-level behavior,
  card-detect/write-protect signals, pull-up population, and schematic.
- Whether the reader accepts only 3.3 V signaling or includes level shifting
  that changes signal integrity or boot behavior.
- Whether the photographed ESP32 I/O expansion shield exposes the investigation
  GPIOs and routes them to the expected ESP32 pins without conflicts.
- Whether the shield power tree can supply the reader and card safely from one
  selected 3.3 V source without dual-power risk.
- Whether a card inserted during boot affects ESP32 strapping pins, flash boot,
  UART0 flashing/debugging, or relay/XBee pin reservations.
- Final card capacity, filesystem, and host-preparation process.

## Closure gates

| Gate | Required evidence | Current status |
| --- | --- | --- |
| Reader identity | Photo, exact model/source, schematic or inspection record, and voltage-path notes. | Unresolved gap |
| Power and logic level | Measured reader supply voltage, active power source, no dual-power conflict, and 3.3 V signal compatibility. | Unresolved gap |
| Pull-ups | Reader/source evidence or measurement proving required SD pull-ups and no boot-pin conflict. | Unresolved gap |
| Shield continuity | Continuity record from shield header labels to the ESP32 pins for `GPIO18`, `GPIO19`, `GPIO23`, and `GPIO32`. | Unresolved gap |
| Boot isolation | Boot/flashing check with the reader connected but relay contacts and XBee wiring still disconnected. | Unresolved gap |
| Filesystem policy | Host-prepared FAT card and explicit decision that normal firmware does not auto-format. | Unresolved gap |
