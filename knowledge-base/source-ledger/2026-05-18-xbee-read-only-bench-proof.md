# Source Ledger - 2026-05-18 XBee Read-Only Bench Proof

## Scope

Source-backed bench proof lane for identifying the photographed Digi
`XBP9B-DPUT-001 RevF` radio through the Waveshare XBee USB Adapter without
persistent radio setting writes, firmware updates, ESP32 carrier wiring, relay
commands, relay switching, or load wiring.

## Verified facts

- Digi identifies `XBP9B-DPUT-001` as an XBee-PRO 900HP S3B
  Point2Multipoint, 900 MHz, 250 mW, U.FL, 10 kbps model. Source ID:
  `SRC-DIGI-XBP9B-DPUT-001`.
- Digi XBee-PRO 900HP product material lists UART (3V) and SPI data
  interfaces. Source ID: `SRC-DIGI-XBEE-PRO-900HP`.
- Digi documents the `AP` API Mode and `AO` API Options commands. Source IDs:
  `SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`.
- Digi documents the `NP` maximum packet payload query. Source ID:
  `SRC-DIGI-XBEE-900HP-NP`.
- Waveshare documents the XBee USB Adapter as a UART communication board with
  XBee and USB interfaces for testing, programming/configuration, and
  USB-to-UART use. Source ID: `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- The local XBee probe environment on 2026-05-18 is WSL2, Python 3.12.3,
  pyserial 3.5, `lsusb` available at `/usr/bin/lsusb`, PowerShell available at
  `/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`, no `xctu`
  on PATH, no `/dev/ttyUSB*` or `/dev/ttyACM*` visible, and pyserial lists
  `/dev/ttyS0` and `/dev/ttyS1`. Source ID:
  `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`.

## Assumptions

- Tier A passive discovery may list serial devices and open a selected serial
  port for read-only observation.
- Tier B may send the command-mode guard sequence and fixed AT read queries
  only when the operator passes `--confirm-sends-read-commands`.
- The current script does not send `ATCN`; command mode should end by the
  module's configured timeout unless a later owner-approved exit policy changes
  that behavior.
- `SH` and `SL` readbacks are address evidence and remain redacted by default.
- Bench records under `research/bench-records/xbee-readonly/` are local
  evidence and are not automatically part of the public Pages bundle.

## Unresolved gaps

- Which host serial port maps to the physical adapter after USB attachment is
  updated.
- Current XBee baud rate and whether command mode can be entered cleanly.
- Adapter header voltage path, DIN/DOUT direction naming, reset/sleep routing,
  CTS/RTS behavior, and current budget.
- Whether a future configuration/write procedure will use XCTU, scripted AT
  commands, API local AT frames, or another owner-approved path.

## Read-only command boundary

Allowed Tier B AT read queries: `VR`, `HV`, `SH`, `SL`, `AP`, `AO`, `BD`, and
`NP`.

Blocked operations: AT parameter writes, `WR`, `AC`, firmware updates, factory
reset actions, API transmit frames, relay commands, ESP32 DIN/DOUT wiring,
adapter setting changes, radio setting changes, and load wiring.
