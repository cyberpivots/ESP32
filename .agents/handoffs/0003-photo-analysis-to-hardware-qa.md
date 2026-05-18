# Handoff 0003 - ESP32 Project Photo Analysis

## From

Hardware

## To

Hardware, QA

## Summary

The active `four-relay-xbee-wifi` documentation now targets the photographed
hardware set: ESP-WROOM-32 development board, ESP32 I/O expansion shield,
four-channel relay module with Songle `SRD-05VDC-SL-C` relay cans, Digi
`XBP9B-DPUT-001 RevF`, and Waveshare XBee USB Adapter. The photo ledger is text
only and references the 10 JPEG filenames in `user_uploads/esp32project.zip`;
image binaries were not copied into repository source paths.

## Required next checks

- Hardware must identify the exact ESP32 dev-board vendor/revision, USB-UART
  bridge, regulator, and module variant.
- Hardware must verify expansion-shield jumper position, selected power input,
  regulator output, current limit, and GPIO continuity for `GPIO25`, `GPIO26`,
  `GPIO27`, and `GPIO33`.
- Hardware must identify the exact four-channel relay module source/schematic
  and measure trigger polarity, input current, 3.3 V compatibility, and
  `JD-VCC`/`VCC` behavior before wiring ESP32 GPIO to relay inputs.
- Hardware must verify Waveshare adapter UART voltage, DIN/DOUT routing,
  reset/sleep/flow-control pins, and PC serial-port behavior before XBee use.
- QA must keep firmware and UI checks on mocks until hardware gates are closed.

## Blockers

- Expansion shield power path and jumper behavior are unverified.
- Relay trigger polarity, input current, 3.3 V compatibility, and isolation
  behavior are unverified.
- XBee adapter voltage and DIN/DOUT routing are unverified.
- XBee settings, address allowlist, AES state, antenna path, and regulatory
  constraints are unverified.
- Load type and safety design are unknown.

## Evidence

- Source IDs are recorded in `knowledge-base/source-index.md`.
- Photo evidence is summarized in
  `knowledge-base/source-ledger/2026-05-18-esp32project-photo-analysis.md`.
- Active project gates are in
  `docs/projects/four-relay-xbee-wifi/power-and-safety.md`.
