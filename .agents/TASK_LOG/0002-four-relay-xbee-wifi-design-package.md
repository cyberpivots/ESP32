# Task 0002 - Four Relay XBee Wi-Fi Design Package

## Task

- ID: 0002-four-relay-xbee-wifi-design-package
- Owner role: Architect
- Status: Complete
- Created: 2026-05-18
- Updated: 2026-05-18

## Goal

Create a source-backed design package for an ESP32 DevKitC controller with a
four-channel relay module, Digi XBee-PRO 900HP S3B `XBP9B-DPUT-001`, and a local
Wi-Fi HTML/CSS control surface.

## Scope

Included: source-index updates, source ledger, ADR, project architecture docs,
hardware profile updates, XBee API protocol contract, static UI prototype,
toolchain notes, and validation checks.

Excluded: firmware implementation, ESP-IDF project files, live hardware wiring,
relay switching, flashing, XBee configuration writes, and load switching.

## Sources

- `SRC-ESP-IDF-STABLE-ESP32`
- `SRC-ESP-IDF-GET-STARTED`
- `SRC-ESP-IDF-HTTP-SERVER`
- `SRC-ESP-IDF-WIFI`
- `SRC-ESP-IDF-GPIO`
- `SRC-ESP-IDF-UART`
- `SRC-ESP-IDF-NVS`
- `SRC-ESP32-DEVKITC`
- `SRC-DIGI-XBP9B-DPUT-001`
- `SRC-DIGI-XBEE-PRO-900HP`
- `SRC-DIGI-XBEE-900HP-USER-GUIDE`
- `SRC-DIGI-XBEE-900HP-AP`
- `SRC-DIGI-XBEE-900HP-AO`
- `SRC-DIGI-XBEE-900HP-DELIVERY`
- `SRC-DIGI-XBEE-900HP-NP`
- `SRC-DIGI-XCTU`
- `SRC-LOCAL-TOOLCHAIN-PROBE-2026-05-18`

## Decisions

- ADR-0002 accepted ESP-IDF stable v6.0.1 as the project-specific framework
  target.
- Relay output pins are provisional design inputs only and are blocked on
  physical board verification.
- Relay-changing HTTP and XBee commands are blocked unless the safety lock is
  open and an admin credential/allowlisted radio source is verified.

## Validation

- `python3 scripts/verify_scaffold.py`: PASS.
- `node --check docs/projects/four-relay-xbee-wifi/ui/app.js`: PASS.
- Static UI smoke at `http://127.0.0.1:8765/index.html`: PASS, no console
  errors after prototype-mode adjustment.
- Framework-file scan for `CMakeLists.txt`, `sdkconfig*`, `platformio.ini`,
  `idf_component.yml`, and `arduino-cli.yaml`: PASS, none found.

## Handoff

Next owners: Hardware, Firmware, Communications, and QA.

Next action: close physical verification gaps before firmware implementation or
bench wiring. See `.agents/handoffs/0002-design-to-hardware-firmware-qa.md`.

Superseding evidence: task 0003 updates the current hardware target from the
DevKitC reference assumption to the photographed ESP-WROOM-32 board/shield,
Songle relay module candidate, Digi `XBP9B-DPUT-001 RevF`, and Waveshare XBee
USB Adapter.
