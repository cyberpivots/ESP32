# Digi XBee Pro S3B - XBP9B-DPUT-001

## Verified facts

- Requested exact part: `XBP9B-DPUT-001`.
- The photo archive shows a Digi XBee-PRO S3B radio label with exact model text
  `XBP9B-DPUT-001 RevF`. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Digi identifies this model as XBee-PRO 900HP S3B Point2Multipoint, 900 MHz,
  250 mW, U.FL, 10 kbps.
- Digi XBee-PRO 900HP product material lists UART (3V) and SPI data interfaces.
- Digi documents XBee-PRO 900HP API mode command `AP`; `AP=2` is API mode with
  escaped sequences.
- Digi documents AO API Options for XBee-PRO 900HP; `AO=0` emits API Rx
  Indicator `0x90` for standard data frames.
- Digi delivery-method documentation lists point-to-multipoint, repeater, and
  DigiMesh delivery methods for XBee-PRO 900HP.
- Digi NP documentation defines the maximum packet payload query and notes
  encryption can reduce maximum payload size.

## Source IDs

- `SRC-DIGI-XBP9B-DPUT-001`
- `SRC-DIGI-XBEE-PRO-900HP`
- `SRC-DIGI-XBEE-900HP-AP`
- `SRC-DIGI-XBEE-900HP-AO`
- `SRC-DIGI-XBEE-900HP-DELIVERY`
- `SRC-DIGI-XBEE-900HP-NP`
- `SRC-DIGI-XBEE-900HP-USER-GUIDE`
- `SRC-DIGI-XCTU`
- `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`
- `SRC-WAVESHARE-XBEE-USB-ADAPTER`

## Project design settings

| Setting | Target | Status |
| --- | --- | --- |
| API mode | `AP=2` escaped API mode | Source-backed design target |
| API output | `AO=0` standard receive packet `0x90` | Source-backed design target |
| Delivery | Point-to-multipoint for the 10 kbps requested part | Source-backed by exact model and delivery docs |
| Security | AES enabled with a provisioned key before accepting relay commands | Source-backed command family; key value not stored in repo |
| Address filter | Allowlist 64-bit radio sources before accepting relay commands | Project safety requirement |
| PC configuration dock | Waveshare XBee USB Adapter | Photographed candidate only; read-only discovery required before writes |

## Read-only discovery boundary

The next bench step is identity and current-settings discovery only through
the project [XBee read-only bench proof](../../../docs/projects/four-relay-xbee-wifi/xbee-read-only-bench-proof.md).
Tier A is passive discovery. Tier B may send only fixed non-persistent AT read
queries for `VR`, `HV`, `SH`, `SL`, `AP`, `AO`, `BD`, and `NP` after
`--confirm-sends-read-commands`.

XBee setting writes, `WR`, `AC`, firmware updates, API transmit frames, relay
commands, and ESP32 DIN/DOUT carrier wiring are blocked until a
backup/readback plan, address plan, AES key process, carrier review, and
rollback procedure are documented.

Source IDs: `SRC-DIGI-XBP9B-DPUT-001`, `SRC-DIGI-XBEE-PRO-900HP`,
`SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`,
`SRC-DIGI-XBEE-900HP-USER-GUIDE`, `SRC-WAVESHARE-XBEE-USB-ADAPTER`.

## Assumptions

- The first configuration/debug workflow uses the photographed Waveshare XBee
  USB Adapter from a PC before any ESP32-mounted carrier is selected.
- The eventual host ESP32 communication path is UART unless a later ADR or
  bench result changes the interface.
- XBee command acceptance is disabled until the configured source address is
  allowlisted and the safety lock is open.

## Unresolved

- Whether the Waveshare adapter is only a PC configuration dock or also a safe
  ESP32-mounted carrier.
- Power source and current budget for the module plus adapter/carrier.
- DIN/DOUT wiring and signal naming from adapter, XBee, and ESP32 perspectives.
- Reset, sleep, associate, and optional flow-control pins.
- Antenna and regulatory constraints for intended deployment.
- Exact serial baud rate and command-mode workflow.
- Exact 64-bit addresses for source allowlisting.
- Secure handling process for AES key provisioning.
- Whether the PC dock can complete identity discovery without any setting
  writes.
