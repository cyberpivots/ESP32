# Waveshare XBee USB Adapter Profile

## Status

Photographed PC configuration/debug dock for the Digi XBee module. This adapter
is not approved as the final ESP32-mounted carrier until UART voltage,
DIN/DOUT routing, reset/sleep behavior, power path, and continuity are verified.

## Verified facts

- The photo archive shows a blue board labeled `XBee USB Adapter` and
  `Waveshare`. Source ID: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- The adapter photos show header labels including `CTS`, `RTS`, `RXD`, `TXD`,
  `GND`, `3.3V`, and `5V`. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Waveshare identifies the XBee USB Adapter as a UART communication board with
  XBee and USB interfaces. Source ID: `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- Waveshare describes use cases for testing, programming/configuring XBee
  modules, and USB-to-UART use with CP2102. Source ID:
  `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- Digi source material identifies the current radio family for read-only
  discovery checks. Source IDs: `SRC-DIGI-XBP9B-DPUT-001`,
  `SRC-DIGI-XBEE-PRO-900HP`.

## Project role

| Role | Status | Gate |
| --- | --- | --- |
| PC XBee configuration dock | First photographed candidate | Verify driver, serial port, power, and radio detection before writes |
| ESP32-mounted carrier | Not selected | Verify UART voltage, DIN/DOUT routing, power path, reset/sleep pins, and mechanical fit |
| USB-to-UART tool | Candidate only | Verify header voltage and signal direction before connecting to ESP32 |

## Read-only discovery gate

| Item | Closure evidence |
| --- | --- |
| Host serial path | OS/device-manager or shell record identifying the adapter serial port. |
| Driver/tool state | Record showing the adapter can be opened without forcing setting writes. |
| Radio identity | Read-only record confirming or rejecting the expected `XBP9B-DPUT-001 RevF` radio. |
| Header voltage | Multimeter record for exposed power/signal headers before any ESP32 connection. |
| DIN/DOUT direction | Source, schematic, or continuity/loopback evidence explaining label direction from adapter, XBee, and host perspectives. |

This gate keeps the adapter in PC dock role only. ESP32-mounted use requires a
separate carrier review.

## Assumptions

- The first XBee configuration path uses this adapter from a PC-side tool after
  read-only discovery confirms the serial port and module identity.
- XBee configuration writes remain blocked until there is an explicit
  configuration procedure, backup/readback plan, and owner approval.

## Unknowns

- Exact adapter revision and schematic match.
- Whether the pictured header `3.3V`/`5V` labels are selectable outputs,
  pass-through rails, or alternate supply inputs.
- Whether `TXD` and `RXD` labels are named from the adapter side, XBee side, or
  host side.
- Whether reset, boot, sleep, associate, CTS, and RTS are routed to the XBee
  socket as needed for this Digi module.
- Which host serial port appears when the adapter is connected.
- Whether read-only discovery can be completed without writing settings.

## Bring-up blockers

- Do not wire the adapter to ESP32 GPIO until voltage and signal direction are
  measured.
- Do not write XBee settings until read-only identification, current settings
  export, and rollback procedure are documented.
- Do not assume this adapter can power the XBee under RF transmit load until
  current budget and USB power behavior are verified.
