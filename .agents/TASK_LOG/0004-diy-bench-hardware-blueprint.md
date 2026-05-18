# Task 0004 - DIY Bench Hardware Blueprint

## Task

- ID: 0004-diy-bench-hardware-blueprint
- Owner role: Hardware
- Status: Complete
- Created: 2026-05-18
- Updated: 2026-05-18

## Goal

Create a source-backed documentation package that turns the photographed ESP32,
relay, and XBee hardware set into a simple staged DIY bench plan with hard
blockers for unsafe or unverified work.

## Scope

Included: source-index updates, hardware blocker ledger, prototype blueprint,
bench bring-up runbook, mains-readiness gate, hardware-profile closure evidence,
project documentation links, validation-script updates, and handoff.

Excluded: live bench action, relay switching, ESP32 flashing, firmware source,
framework project files, XBee setting writes, mains wiring, and relay load
wiring.

## Sources

- `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`
- `SRC-ESP32-WROOM-32-DATASHEET`
- `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`
- `SRC-ESP32-IO-SHIELD-CANDIDATE`
- `SRC-SONGLE-SRD-05VDC-SL-C`
- `SRC-WAVESHARE-XBEE-USB-ADAPTER`
- `SRC-DIGI-XBP9B-DPUT-001`
- `SRC-DIGI-XBEE-PRO-900HP`
- `SRC-NIOSH-ELECTRICAL-SAFETY`
- `SRC-OSHA-DEENERGIZED-WORK`
- `SRC-OSHA-GFCI`
- `SRC-OSHA-AEGCP`
- `SRC-OSHA-GROUNDING-OVERCURRENT`
- `SRC-NEMA-ENCLOSURES`

## Decisions

- Prototype defaults to low-voltage or disconnected relay contacts only.
- Relay GPIO candidates remain `GPIO25`, `GPIO26`, `GPIO27`, and `GPIO33`.
- Direct ESP32 GPIO drive remains blocked unless measured relay input behavior
  passes the documented 3.3 V/current gate.
- Waveshare XBee USB Adapter is PC dock only for this pass; no XBee setting
  writes are approved.
- Mains switching remains hard blocked by `mains-readiness-gate.md`.

## Validation

- `python3 -m py_compile scripts/verify_scaffold.py`: PASS.
- `python3 scripts/verify_scaffold.py`: PASS.
- Direct framework-file scan for `CMakeLists.txt`, `sdkconfig*`,
  `platformio.ini`, `idf_component.yml`, and `arduino-cli.yaml`: PASS, none
  found.
- Direct image-binary scan outside `user_uploads/`: PASS, none found.

## Handoff

Next owners: Hardware and QA.

Next action: execute only non-mutating bench inspection and measurement steps
from `bench-bring-up-runbook.md`, then record results as source/inspection
evidence before any firmware or wiring work.

See `.agents/handoffs/0004-blueprint-to-hardware-qa.md`.
