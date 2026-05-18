# Task 0003 - ESP32 Project Photo Analysis Reframe

## Task

- ID: 0003-esp32project-photo-analysis
- Owner role: Hardware
- Status: Complete
- Created: 2026-05-18
- Updated: 2026-05-18

## Goal

Reframe `four-relay-xbee-wifi` around the photographed hardware while preserving
strict evidence boundaries between visible labels, source-backed facts,
assumptions, and unresolved electrical claims.

## Scope

Included: source-index updates, text-only photo ledger, hardware profile
updates, active project documentation updates, XBee dock boundary updates,
validation-script checks, and handoff.

Excluded: copying image binaries into the repository, live relay switching,
load wiring, ESP32 flashing, XBee configuration writes, firmware source, and
framework project files.

## Sources

- `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`
- `SRC-ESP32-WROOM-32-DATASHEET`
- `SRC-WAVESHARE-XBEE-USB-ADAPTER`
- `SRC-SONGLE-SRD-05VDC-SL-C`
- `SRC-DIGI-XBP9B-DPUT-001`
- `SRC-DIGI-XBEE-PRO-900HP`
- `SRC-DIGI-XBEE-900HP-AP`
- `SRC-DIGI-XBEE-900HP-AO`
- `SRC-DIGI-XBEE-900HP-USER-GUIDE`
- `SRC-ESP-IDF-GPIO`
- `SRC-ESP-IDF-UART`

## Decisions

- The current physical target is the photographed ESP-WROOM-32 development board
  plus ESP32 I/O expansion shield.
- ESP32 DevKitC is demoted to source-backed reference and prior assumption.
- Relay GPIO candidates remain `GPIO25`, `GPIO26`, `GPIO27`, and `GPIO33`
  because they are visible shield labels, but they stay blocked until shield
  routing and relay electrical behavior are verified.
- The Waveshare XBee USB Adapter is the first PC configuration/debug dock, not
  the final ESP32-mounted carrier.

## Validation

- `python3 -m py_compile scripts/verify_scaffold.py`: PASS.
- `python3 scripts/verify_scaffold.py`: PASS.
- Framework file scan remains part of `scripts/verify_scaffold.py`.
- Direct framework-file scan for `CMakeLists.txt`, `sdkconfig*`,
  `platformio.ini`, `idf_component.yml`, and `arduino-cli.yaml`: PASS, none
  found.
- Direct image-binary scan outside `user_uploads/`: PASS, none found.

## Handoff

Next owners: Hardware and QA.

Next action: perform non-mutating bench inspection and continuity/voltage
measurements for the expansion shield, relay module, and Waveshare adapter
before any wiring, flashing, relay switching, or XBee writes.

See `.agents/handoffs/0003-photo-analysis-to-hardware-qa.md`.
