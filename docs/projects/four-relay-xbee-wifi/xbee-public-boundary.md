# XBee Public Boundary

## Purpose

This is the public-safe XBee summary for the ESP32 four-relay workbench. It
replaces the detailed protocol contract in the public Pages bundle so the
public packet can explain the radio boundary without publishing command
payloads, address plans, key-provisioning details, or future write targets.

The internal protocol design remains in `comm-protocols/wireless/`, but the
public bundle should start here.

## Verified facts

- The photographed radio label includes Digi `XBP9B-DPUT-001 RevF`. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Digi identifies `XBP9B-DPUT-001` as an XBee-PRO 900HP S3B Point2Multipoint
  900 MHz, 250 mW, U.FL, 10 kbps model. Source ID:
  `SRC-DIGI-XBP9B-DPUT-001`.
- Digi XBee-PRO 900HP product material lists UART 3 V and SPI interfaces.
  Source ID: `SRC-DIGI-XBEE-PRO-900HP`.
- Digi documents API mode and API options for XBee-PRO 900HP. Source IDs:
  `SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`.
- The current local XBee proof path is read-only: passive discovery first, then
  explicitly confirmed fixed AT read queries for `VR`, `HV`, `SH`, `SL`, `AP`,
  `AO`, `BD`, and `NP`. Source IDs:
  `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`,
  `SRC-DIGI-XBEE-900HP-NP`, `SRC-DIGI-XBEE-900HP-USER-GUIDE`.
- Waveshare documents the XBee USB Adapter as a UART communication board with
  XBee and USB interfaces. Source ID:
  `SRC-WAVESHARE-XBEE-USB-ADAPTER`.

## Assumptions

- Public review needs to know the boundary and next evidence, not the future
  command schema.
- Radio addresses, serial numbers, AES keys, passive bytes, and setting
  snapshots are local bench evidence unless an owner explicitly classifies a
  redacted record for publication.
- The Waveshare adapter remains a PC dock until a separate carrier review
  closes.

## Unknowns

- Current host serial port, baud rate, API mode, API options, and maximum
  packet payload.
- Current XBee firmware and hardware readback values.
- Adapter header voltage and DIN/DOUT direction naming.
- Whether any final ESP32-mounted carrier will be used.
- Address plan, security provisioning process, telemetry interval, retry
  policy, and final payload schema.

## Public rules

- Allowed publicly: part identity, read-only proof path, source IDs, and the
  fact that radio writes and ESP32 carrier wiring are blocked.
- Not public by default: radio serial identifiers, raw passive bytes, MAC-like
  local device identifiers, AES key values, setting snapshots, address plans,
  and private bench records.
- Not authorized: XBee setting writes, `WR`, `AC`, firmware update actions,
  factory reset actions, API transmit frames, relay commands, or ESP32
  DIN/DOUT carrier wiring.

## Next evidence

1. Run Tier A passive discovery from
   [XBee read-only bench proof](xbee-read-only-bench-proof.md).
2. Record adapter inspection and measured header voltage while disconnected
   from ESP32 GPIO.
3. Run Tier B fixed reads only if the explicit confirmation flag is acceptable
   for the bench record.
4. Keep readbacks redacted unless the evidence stays local-only.
5. Create a separate owner-reviewed protocol and carrier task before any write
   or ESP32 DIN/DOUT action.
