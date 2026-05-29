# XBee Read-Only Bench Proof

## Goal

Create a concrete, source-backed bench lane for identifying the photographed
Digi XBee radio through the Waveshare USB adapter without changing radio
settings, flashing firmware, wiring the adapter to ESP32 GPIO, switching
relays, or touching load wiring.

For public navigation, use [XBee Public Boundary](xbee-public-boundary.md).
This proof document remains the detailed read-only bench plan.

This proof has two tiers:

- Tier A passive discovery: enumerate host serial devices, inspect adapter
  markings, measure exposed adapter/header voltage, and optionally observe
  incoming bytes without sending serial commands.
- Tier B read-query discovery: send the command-mode guard sequence and then
  only fixed non-persistent AT read queries after an explicit confirmation
  flag.

## Verified facts

- The photographed radio label includes Digi `XBP9B-DPUT-001 RevF`. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Digi identifies `XBP9B-DPUT-001` as an XBee-PRO 900HP S3B
  Point2Multipoint, 900 MHz, 250 mW, U.FL, 10 kbps model. Source ID:
  `SRC-DIGI-XBP9B-DPUT-001`.
- Digi XBee-PRO 900HP product material lists UART (3V) and SPI data
  interfaces. Source ID: `SRC-DIGI-XBEE-PRO-900HP`.
- Digi documents the `AP` API Mode command and `AO` API Options command for
  XBee-PRO 900HP. Source IDs: `SRC-DIGI-XBEE-900HP-AP`,
  `SRC-DIGI-XBEE-900HP-AO`.
- Digi documents the `NP` maximum packet payload command for XBee-PRO 900HP.
  Source ID: `SRC-DIGI-XBEE-900HP-NP`.
- Waveshare documents the XBee USB Adapter as a UART communication board with
  XBee and USB interfaces for testing, programming/configuration, and
  USB-to-UART use. Source ID: `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- The current local XBee probe environment is WSL2 with Python 3.12.3,
  pyserial 3.5, `lsusb` and PowerShell available, no `xctu` on PATH, and only
  redacted serial-device candidates visible at probe time. Source ID:
  `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`.
- Parent host-tooling evidence installed Digi XCTU 6.5.13.2 as a reference GUI
  only. Source ID: `SRC-LOCAL-XCTU-INSTALL-PROOF-2026-05-29`.
- The continued study CLI can save local inventory records, compare inventory
  snapshots with `identity-delta`, and emit a locked XCTU local-discovery
  checklist without opening serial ports or launching XCTU. Source ID:
  `SRC-LOCAL-XBEE-READONLY-LIVE-GATE-2026-05-29`.
- The workspace now records missing evidence as a continuation condition when
  safe no-serial evidence collection remains. Source ID:
  `SRC-LOCAL-MULTI-AGENTIC-CONTINUOUS-ENFORCEMENT-2026-05-29`.

## Assumptions

- Read-only means no persistent XBee configuration changes, no firmware update,
  no relay command, and no hardware-control action.
- Tier B sends the command-mode guard sequence and fixed AT read queries only
  after `--confirm-sends-read-commands`.
- The Waveshare adapter remains a PC dock for this proof. It is not an
  ESP32-mounted carrier.
- Full XBee serial numbers and raw passive bytes are local evidence. They are
  redacted by default and should not be published in the Pages artifact.

## Unknowns

- Which host serial port corresponds to the adapter after the current USB
  attachment state is updated.
- Whether the adapter header `3.3V` and `5V` pins are outputs, inputs,
  selectable rails, or pass-through rails on the photographed board revision.
- Whether `TXD` and `RXD` labels are named from the adapter side, XBee side, or
  host side.
- Whether the radio is already in transparent mode, API mode, or another state
  that affects the command-mode guard sequence.
- Current XBee baud rate and command-mode timeout.

## Hard blocks

The read-only proof does not allow:

- ESP32 DIN/DOUT wiring.
- Relay commands or relay switching.
- API transmit frames.
- AT parameter writes such as `AP2`, `AO0`, `BD7`, `DH`, `DL`, `KY`, or any
  other command with a value.
- `WR`, `AC`, firmware update actions, factory reset actions, or setting
  restore actions.
- Adapter use as an ESP32 carrier before a separate voltage, direction, power,
  and continuity review.
- Any mains/load wiring.

## Continuation Rule

Use `scripts/agent_process_decision.py` or the same weighted-vote packet shape
for this lane. Missing host evidence should route to `continue` when the next
step is no-serial inventory, offline `identity-delta`, redaction review, or
locked checklist generation. Missing physical facts should route to one
specific `ask_user` item, such as adapter markings, antenna state, isolation,
or voltage evidence. Use `blocked` only when the next action would cross into
serial open, XCTU launch, write/apply/transmit/recovery, ESP32 wiring, or
relay/load/mains work without the named Tier 3 prerequisites.

## Tier A - Passive Discovery

Goal: identify the host-side adapter path and collect non-mutating evidence
without sending serial bytes.

Required bench record:

- Adapter disconnected from ESP32 GPIO.
- Adapter revision markings, socket orientation, antenna connection, and header
  labels inspected.
- Header voltage measured with a multimeter before any ESP32 connection.
- Host serial candidates captured with:

```bash
python3 scripts/xbee_read_only_probe.py list --json
python3 scripts/xbee_radio_study.py inventory --json
```

Optional local-only inventory records may use `--out` under
`research/bench-records/xbee-readonly/`. Use `identity-delta` to compare
before/after snapshots from one-at-a-time adapter disconnect/reconnect tests:

```bash
python3 scripts/xbee_radio_study.py identity-delta --before <before.json> --after <after.json> --json
```

The delta is host evidence only. It does not prove radio identity unless the
bench record also contains the matching physical disconnect/reconnect notes.

Optional passive observation:

```bash
python3 scripts/xbee_read_only_probe.py passive --port <serial-port> --baud 9600 --duration 10 --json
```

The passive command opens the serial port and reads only. It does not write
serial data. If bytes are observed, the default JSON includes byte count and a
hash while redacting raw bytes. Use `--show-addresses` only for local-only
bench evidence.

Stop if:

- The adapter voltage path is unclear.
- The serial device is unstable or cannot be opened.
- A tool requires setting writes to identify the radio.
- Anyone proposes connecting adapter `TXD`/`RXD`, `DIN`/`DOUT`, reset, sleep,
  CTS, or RTS to ESP32 before carrier review.

## Tier B - Gated AT Read Queries

Goal: read only identity and current settings needed for the next design
review.

Allowed AT read queries:

| Command | Read purpose |
| --- | --- |
| `VR` | Firmware version readback. |
| `HV` | Hardware version readback. |
| `SH` | Serial number high readback, redacted by default. |
| `SL` | Serial number low readback, redacted by default. |
| `AP` | Current API mode value. |
| `AO` | Current API output option value. |
| `BD` | Current baud-rate setting value. |
| `NP` | Current maximum packet payload value. |

Run only after Tier A records the serial candidate and adapter voltage check:

```bash
python3 scripts/xbee_read_only_probe.py at-query --port <serial-port> --baud 9600 --confirm-sends-read-commands --json
```

The script uses a fixed allowlist. It rejects parameter writes, `WR`, `AC`, and
other commands outside the table. `SH` and `SL` values are redacted by default;
use `--show-addresses` only for local evidence that will stay out of the public
bundle.

The script sends the command-mode guard sequence before the read queries. It
does not send `ATCN`, so the module should leave command mode by its configured
timeout. If that temporary command-mode interval is not acceptable for the
bench, do not run Tier B until an owner-approved exit policy is recorded.

Stop if:

- Command mode cannot be entered cleanly.
- Any response suggests the wrong radio, wrong baud rate, or unstable serial
  link.
- The next proposed action is a setting write instead of a review record.
- XBee discovery is used to justify relay commands, API transmit frames, or
  ESP32 carrier wiring.

## XCTU Local Discovery Gate

XCTU local discovery is blocked until Tier A proves the exact local ports and
the task record includes same-session physical evidence: adapter markings,
antenna state, no ESP32 DIN/DOUT wiring, no relay/load/mains connection, and
adapter voltage/carrier review.

The repo CLI can generate only the locked checklist:

```bash
python3 scripts/xbee_radio_study.py xctu-discovery-plan --ports COMx COMy --json
```

The checklist does not launch XCTU. If a future approved gate uses XCTU, select
only the confirmed ports, use default port parameters only, add selected local
devices only, and capture redacted evidence. Do not use all-port discovery,
broad parameter scans, network discovery, remote devices, AT/API console
transmit actions, write/apply controls, firmware tools, recovery, range test,
or throughput test.

## Evidence Storage

Default output goes to stdout. A local JSON record may be written under:

```text
research/bench-records/xbee-readonly/<timestamp>.json
```

Example:

```bash
python3 scripts/xbee_read_only_probe.py list --json --out research/bench-records/xbee-readonly/2026-05-18-list.json
```

Do not add unredacted serial numbers, raw passive bytes, or private bench records
to the public Pages bundle.

## Acceptance

This proof is accepted only when:

- Tier A captures host serial discovery and voltage evidence.
- Tier B, if used, captures only the allowed AT read query outputs.
- The task record notes whether `SH`/`SL` remained redacted.
- Open blockers stay in `research/known-gaps.md` or a handoff record.

Passing this proof does not approve ESP32 carrier wiring, XBee setting writes,
radio security provisioning, relay switching, firmware flashing, or load
wiring.
