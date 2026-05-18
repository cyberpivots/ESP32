# Handoff 0002 - Four Relay XBee Wi-Fi Design

## From

Architect

## To

Hardware, Firmware, Communications, QA

## Summary

The project design package is in `docs/projects/four-relay-xbee-wifi/`.
ADR-0002 accepts ESP-IDF stable v6.0.1 for this project only. No firmware source,
framework files, flashing, relay wiring, or XBee configuration writes were added.

Superseding evidence: task 0003 reframed the active physical target around the
photographed ESP-WROOM-32 development board, ESP32 I/O expansion shield,
four-channel Songle relay module candidate, Digi `XBP9B-DPUT-001 RevF`, and
Waveshare XBee USB Adapter. Use
`.agents/handoffs/0003-photo-analysis-to-hardware-qa.md` for current hardware
gates.

## Required next checks

- Hardware must identify the exact ESP32 DevKitC module/header variant and the
  exact four-channel relay board before any pinout or wiring is final.
- Hardware must identify the XBee carrier/adapter and confirm power, DIN/DOUT,
  reset, sleep, and optional flow-control wiring before radio bench use.
- Hardware must identify load type and complete mains/inductive-load safety
  review before switching real loads.
- Firmware must install/verify ESP-IDF v6.0.1 tooling before creating framework
  files or running `idf.py build`.
- Communications must add parser test vectors for XBee API escaped frames before
  accepting radio relay commands.
- QA must keep relay-changing tests on mocks until relay board behavior and
  safety lock behavior are verified.

## Blockers

- Relay module model and electrical behavior are unknown.
- ESP32 DevKitC physical variant is unknown.
- XBee carrier/adapter is unknown.
- Load type and safety design are unknown.
- ESP-IDF, esptool, CMake, Ninja, and XBee GUI tooling were not found on PATH in
  the current shell.

## Evidence

Source IDs are recorded in `knowledge-base/source-index.md` and summarized in
`knowledge-base/source-ledger/2026-05-18-four-relay-xbee-wifi-design.md`.
