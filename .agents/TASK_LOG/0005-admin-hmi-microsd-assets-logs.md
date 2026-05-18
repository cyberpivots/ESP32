# Task 0005 - Admin HMI MicroSD Assets and Logs

## Task

- ID: 0005-admin-hmi-microsd-assets-logs
- Owner role: Architect, QA
- Status: Complete
- Created: 2026-05-18
- Updated: 2026-05-18

## Goal

Replace the simple relay UI with a full static admin HMI and document the
MicroSD static-asset and event-log contract for `four-relay-xbee-wifi`.

## Scope

Included: static HTML/CSS/JS admin HMI, local mock storage/log states,
`manifest.json`, MicroSD source-index entries, storage contract updates,
MicroSD reader profile, storage blocker ledger, pin-plan updates, architecture
and firmware task-model notes, known-gap updates, validation, and handoff.

Excluded: ESP-IDF firmware source, framework project files, live ESP32 flashing,
relay switching, XBee writes, MicroSD wiring, card formatting, and mains/load
wiring.

## Sources

- `SRC-ESP-IDF-FATFS`
- `SRC-ESP-IDF-SDSPI`
- `SRC-ESP-IDF-SDMMC`
- `SRC-ESP-IDF-SD-PULLUP`
- `SRC-ESP-IDF-HTTP-SERVER`
- `SRC-ESP-IDF-RESTFUL-SERVER-EXAMPLE`
- `SRC-ESP-IDF-SDSPI-EXAMPLE`
- `SRC-ESP-IDF-NVS`
- `SRC-ESP-IDF-GPIO`
- `SRC-ESP-IDF-UART`
- `SRC-ESP32-WROOM-32-DATASHEET`
- `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`
- `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`

## Decisions

- MicroSD is documented as the primary static asset and event-log store:
  `/sdcard/www` for assets and `/sdcard/logs` for JSONL logs.
- NVS remains authoritative for admin credential state, safety config, relay
  polarity, and XBee allowlists.
- The preferred SPI MicroSD investigation set is `GPIO18` SCK, `GPIO19` MISO,
  `GPIO23` MOSI, and `GPIO32` CS, but it is not approved wiring.
- Normal firmware should not auto-format the MicroSD card; card preparation
  remains a host-side process until a future source-backed decision changes it.
- The UI remains plain static HTML/CSS/JS with no external fonts, CDNs, build
  pipeline, or bulky assets.

## Validation

- `node --check docs/projects/four-relay-xbee-wifi/ui/app.js`: PASS.
- `python3 -m py_compile scripts/verify_scaffold.py`: PASS.
- `python3 scripts/verify_scaffold.py`: PASS.
- Playwright local-server smoke at `http://127.0.0.1:8765/`: PASS.
- Playwright verified tabs render, relay buttons are gated, storage/log panels
  render mock data, SD missing fallback renders, low-space state renders, and
  log filtering works.
- Playwright console check: PASS, zero warnings and zero errors.
- Mobile viewport check at `390x844`: PASS, no horizontal overflow
  (`scrollWidth` equals viewport width).
- Direct framework-file scan for `CMakeLists.txt`, `sdkconfig*`,
  `platformio.ini`, `idf_component.yml`, and `arduino-cli.yaml`: PASS, none
  found.
- Direct image-binary scan outside `user_uploads/`: PASS, none found after
  generated Playwright screenshots were removed.

## Handoff

Next owners: Hardware, Firmware, and QA.

Next action: Hardware must identify the exact MicroSD reader and close power,
pull-up, shield-continuity, and boot-pin blockers before wiring. Firmware may
use the static contract for future ESP-IDF implementation only after hardware
gates are closed. QA should keep framework-file and no-bulky-asset scans in the
release gate.

See `.agents/handoffs/0005-admin-hmi-to-firmware-hardware-qa.md`.
