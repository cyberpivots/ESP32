# Source Ledger - 2026-05-18 SPI MicroSD Assets and Logs

## Scope

This ledger defines the source-backed storage plan for serving a full static
admin HMI from a MicroSD card and writing local event logs for
`four-relay-xbee-wifi`. It does not approve MicroSD wiring, card formatting by
normal firmware, live ESP32 flashing, relay switching, or load wiring.

## Verified facts

- ESP-IDF FatFS support can mount FAT volumes through VFS and expose file paths
  under a mount point such as `/sdcard` to standard C/POSIX-style file APIs.
  Source ID: `SRC-ESP-IDF-FATFS`.
- ESP-IDF FatFS includes SD-card mount helpers for SDMMC and SDSPI-backed cards.
  Source ID: `SRC-ESP-IDF-FATFS`.
- ESP-IDF SDSPI uses SPI mode, is lower-throughput than SDMMC host access, and
  allows flexible pin routing through the GPIO matrix. Source ID:
  `SRC-ESP-IDF-SDSPI`.
- ESP-IDF SD/MMC APIs can initialize a card and report card information after
  initialization. Source ID: `SRC-ESP-IDF-SDMMC`.
- ESP-IDF HTTP Server provides URI handlers and file-serving examples for
  building a local web interface on ESP32. Source ID:
  `SRC-ESP-IDF-HTTP-SERVER`.
- The ESP-IDF RESTful server example combines REST-style APIs with web assets
  in an ESP32 application. Source ID: `SRC-ESP-IDF-RESTFUL-SERVER-EXAMPLE`.
- The ESP-IDF SDSPI example mounts an SD card over SPI, prints card
  information, performs file write/read operations, supports customizable pin
  assignments, and warns that formatting can delete data. Source ID:
  `SRC-ESP-IDF-SDSPI-EXAMPLE`.
- Espressif SD pull-up guidance applies to ESP32 SD-card SPI and SDMMC use and
  records pull-up and boot/strapping concerns that must be reviewed before
  wiring. Source ID: `SRC-ESP-IDF-SD-PULLUP`.
- ESP-IDF NVS is already the planned source for credential/token and safety
  configuration state. Source ID: `SRC-ESP-IDF-NVS`.

## Assumptions

- MicroSD is the primary static asset and event-log store for this project:
  UI assets under `/sdcard/www` and logs under `/sdcard/logs`.
- NVS remains authoritative for admin credential state, safety config, relay
  polarity, and XBee allowlists because those are safety-critical runtime
  settings.
- A missing or failed MicroSD mount should degrade to a tiny embedded fallback
  page in a later firmware implementation.
- The first card-preparation path is host-side copy and validation, not device
  auto-formatting during normal firmware boot.
- FAT32 is the first operational target for common removable-card
  interoperability; exact card capacity and formatting workflow remain open
  until a real card and host process are selected.

## Unknowns

- Exact MicroSD reader module identity, schematic, regulator, logic-level path,
  pull-ups, and card-detect/write-protect behavior.
- Exact MicroSD card capacity, filesystem, sector size, and host-preparation
  procedure.
- Final firmware memory limits for static file buffering, JSON response size,
  log rotation, and directory listing behavior.
- Final storage failure policy for read-only cards, low free space, corrupt
  filesystems, and card removal during operation.
- Final integrity policy for manifest verification, asset version display, and
  admin-visible storage warnings.

## Planned card layout

| Path | Owner | Purpose | Source status |
| --- | --- | --- | --- |
| `/sdcard/www/index.html` | Static asset bundle | Admin HMI entry point | Planned path, source-backed by FATFS/VFS and HTTP server docs |
| `/sdcard/www/styles.css` | Static asset bundle | UI styling | Planned path, source-backed by FATFS/VFS and HTTP server docs |
| `/sdcard/www/app.js` | Static asset bundle | Browser-side HMI logic | Planned path, source-backed by FATFS/VFS and HTTP server docs |
| `/sdcard/www/assets/` | Static asset bundle | Optional small local assets only | Planned path; no bulky assets approved |
| `/sdcard/www/manifest.json` | Static asset bundle | Asset version and file inventory | Planned path |
| `/sdcard/logs/events/YYYY-MM-DD.jsonl` | Firmware logger | General events and rejects | Planned path |
| `/sdcard/logs/relay/YYYY-MM-DD.jsonl` | Firmware logger | Relay command/reject/audit entries | Planned path |

Source IDs: `SRC-ESP-IDF-FATFS`, `SRC-ESP-IDF-HTTP-SERVER`,
`SRC-ESP-IDF-RESTFUL-SERVER-EXAMPLE`.

## Blocker ledger

| Blocker | Closure evidence required | Current status |
| --- | --- | --- |
| Reader identity | Exact reader source or inspection record including voltage path, logic-level path, pull-ups, and CD/WP pins. | Unresolved gap |
| SPI wiring | Shield continuity and boot-pin review for `GPIO18`, `GPIO19`, `GPIO23`, and `GPIO32`; no relay, UART0, or flash-pin conflict. | Unresolved gap |
| Power | Single selected 3.3 V source, measured reader/card draw, no dual-power path, and shield regulator review. | Unresolved gap |
| Pull-ups | Source or measurement proving required SD pull-ups and no strapping conflict. | Unresolved gap |
| Filesystem | Host-prepared FAT card process and normal-firmware no-auto-format policy. | Unresolved gap |
| Logging | Low-space behavior, append failure handling, log rotation, and JSONL schema. | Unresolved gap |
| Fallback serving | Embedded fallback page content and activation condition. | Unresolved gap |

## Blocked actions

- Do not wire the MicroSD reader to the photographed ESP32 shield until the
  reader identity, power, pull-ups, shield continuity, and boot-pin risks are
  documented.
- Do not use `GPIO6` through `GPIO11`, UART0 pins, existing relay candidates,
  or unresolved strapping pins for the first MicroSD wiring pass.
- Do not enable normal-firmware auto-format for the event-log card.
- Do not move admin credentials, relay polarity, safety config, or XBee
  allowlists from NVS to MicroSD.
