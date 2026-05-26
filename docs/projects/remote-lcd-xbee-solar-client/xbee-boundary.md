# XBee Boundary

## Verified facts

- Digi identifies `XBP9B-DPUT-001` as an XBee-PRO 900HP S3B
  Point2Multipoint, 900 MHz, 250 mW, U.FL, 10 kbps model. Source ID:
  `SRC-DIGI-XBP9B-DPUT-001`.
- Digi XBee-PRO 900HP product material lists UART 3 V and SPI data interfaces.
  Source ID: `SRC-DIGI-XBEE-PRO-900HP`.
- Digi documents API mode, API options, delivery methods, and maximum packet
  payload query coverage for XBee-PRO 900HP. Source IDs:
  `SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`,
  `SRC-DIGI-XBEE-900HP-DELIVERY`, `SRC-DIGI-XBEE-900HP-NP`,
  `SRC-DIGI-XBEE-900HP-USER-GUIDE`.
- The current workspace XBee gate is read-only discovery only: passive
  discovery first, then explicitly confirmed fixed AT read queries for `VR`,
  `HV`, `SH`, `SL`, `AP`, `AO`, `BD`, and `NP`. Source ID:
  `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`.

## Assumptions

- This project reuses the existing `XBP9B-DPUT-001` profile until evidence
  proves a different radio.
- Radio serial identifiers, address plans, AES keys, raw passive bytes, and
  setting snapshots remain local/private unless explicitly redacted for
  publication.

## Unknowns

- Current XBee firmware version, hardware version, serial address, API mode,
  baud rate, API options, and maximum payload.
- Final carrier, DIN/DOUT mapping, reset/sleep/associate pins, flow control,
  power budget, antenna, and regulatory deployment context.
- Whether this client lane will be telemetry-only or will later accept radio
  commands.

## Blocked actions

- XBee setting writes, including `WR`, `AC`, factory reset, firmware update, or
  persistent configuration changes.
- API transmit frames or application payload transmission.
- ESP32 DIN/DOUT wiring or carrier mounting.
- Address allowlist, key provisioning, or command acceptance claims.

## Required next evidence

1. Confirm exact radio and carrier identity.
2. Run the existing read-only proof path without setting writes.
3. Record carrier voltage and DIN/DOUT naming while disconnected from ESP32
   GPIO.
4. Create a communications ADR before any payload schema or transmit behavior.
5. Create a hardware carrier review before any ESP32 wiring.
