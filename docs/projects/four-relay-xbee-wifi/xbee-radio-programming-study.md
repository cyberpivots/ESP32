# XBee Radio Programming Study

## Scope

This study turns the existing XBee read-only proof into a staged programming
study path. The study document itself does not authorize radio writes. Task
0091 records one completed selected-port programming gate for user-named
`COM15` and `COM6`; later named gates accepted bounded benign `link_probe` API
transmit proof and the permanent ESP32 bridge retest. All other setting writes,
`AC`, firmware updates, range tests, relay actions, and load/mains work remain
closed.

The current implementation includes host/tool inventory, inventory-delta
comparison, offline profile comparison, a locked XCTU discovery checklist, and
a blocked write-plan packet. The only command that can touch a serial port is
`readonly`, which delegates to the existing fixed AT read-query probe and still
requires `--confirm-sends-read-commands`.

## Verified facts

- Digi identifies `XBP9B-DPUT-001` as an XBee-PRO 900HP S3B
  Point2Multipoint model. Source ID: `SRC-DIGI-XBP9B-DPUT-001`.
- Existing repo evidence keeps the XBee bench path read-only and limits Tier B
  AT reads to `VR`, `HV`, `SH`, `SL`, `AP`, `AO`, `BD`, and `NP`. Source ID:
  `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`.
- Digi documents XCTU as a free Windows, macOS, and Linux GUI for managing,
  configuring, and testing XBee modules, with API frame builder/interpreter,
  AT/API consoles, firmware explorer, recovery, range test, and update
  features. Source ID: `SRC-DIGI-XCTU-FEATURES-2026-05-29`.
- Digi's support page currently lists XCTU 6.5.13 assets for Windows, macOS,
  and Linux; the Windows detail page lists `40003026_AL.exe`, 230.5 MB, version
  date 2023-07-17. Source ID: `SRC-DIGI-XCTU-SUPPORT-2026-05-29`.
- Digi documents XBee Studio as a multi-platform GUI that can discover,
  configure, communicate with, and recover XBee devices. Source ID:
  `SRC-DIGI-XBEE-STUDIO-2026-05-29`.
- Digi's `xbee-python` GitHub release API reports latest release `1.5.0`,
  published 2024-08-27, and PyPI reports `digi-xbee` version `1.5.0`. Source
  ID: `SRC-DIGI-XBEE-PYTHON-2026-05-29`.
- The v1 CLI is implemented as `scripts/xbee_radio_study.py`. Source ID:
  `SRC-LOCAL-XBEE-RADIO-STUDY-2026-05-29`.
- Pre-install same-session `inventory --json` validation found no `xctu`
  command or known XCTU install path, no XBee Studio command or known install
  path, and no installed/importable `digi-xbee` package. Source ID:
  `SRC-LOCAL-XBEE-RADIO-STUDY-2026-05-29`.
- Same-session host-tooling evidence downloaded Digi's Windows XCTU installer
  from the official support path, recorded SHA-256
  `9b6acd16927ee17d4f3a728768cd1c559e09ab6b12470fd6da08e7106fb308e1`, installed
  XCTU 6.5.13.2 to the Windows per-user Digi `XCTU-NG` path, completed the
  bundled Digi USB RF driver installer, and launched XCTU only to capture the
  6.5.13 change-log first-run screen. Source ID:
  `SRC-LOCAL-XCTU-INSTALL-PROOF-2026-05-29`.
- The continued read-only gate added `--out`, `identity-delta`, and
  `xctu-discovery-plan`, captured host-only WSL/Windows inventories, and
  stopped before opening any serial port. Source ID:
  `SRC-LOCAL-XBEE-READONLY-LIVE-GATE-2026-05-29`.
- The two-device read-only Stage A1 packet captured fresh no-serial WSL and
  Windows inventories, local physical-fact placeholders, recovery/cleanup
  rules, a manifest, and a weighted `ask_user` decision. Source ID:
  `SRC-LOCAL-XBEE-TWO-DEVICE-READONLY-STUDY-2026-05-29`.
- Task 0091 selected-port programming wrote only `AO=0`, `KY=<redacted>`,
  `EE=1`, `AP=2`, and `WR` to user-named `COM15` and `COM6`, then validated
  both ports with escaped API local-AT readback showing `AP=02`, `AO=00`, and
  `EE=01`. Source ID:
  `SRC-LOCAL-XBEE-SELECTED-PORT-PROGRAMMING-2026-05-29`.
- Task 0095 corrected the ESP32/XBee mapping to `COM6` as ESP32 and `COM15`
  as the peer XBee, and showed the ESP32 did not expose XBee API frames before
  bridge firmware. Source ID:
  `SRC-LOCAL-CORRECTED-ESP32-COM6-PEER-COM15-LIVE-TEST-2026-05-30`.
- Task 0096 implements and flashes the permanent ESP32 UART bridge: UART0 host
  `115200`, UART2 XBee `9600`, TX GPIO17, RX GPIO16, no hardware flow control,
  and no app logging in the bridge loop. The named retest accepted redacted
  COM6 bridge local-AT readback, COM15 peer readback, and corrected
  bidirectional benign `link_probe` RF proof. Source ID:
  `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`.

## Assumptions

- XCTU and XBee Studio are reference tools only until a later gate names a live
  operation and captures same-session evidence.
- Public documents may describe part identity, safety boundaries, source IDs,
  and redacted workflow shape, but not serial identifiers, raw passive bytes,
  AES keys, address plans, private COM mappings, or full setting snapshots.
- A target profile is review evidence. A target profile is not an apply
  procedure.
- `digi-xbee` is a candidate future dependency. It is not required by the
  current CLI and is not installed by this task.

## Unknowns

- Whether any visible Windows COM port maps to the physical XBee adapter.
- Current radio firmware, hardware, baud, API mode, API options, payload limit,
  address, security, channel/network, antenna, and carrier state.
- Whether a future write procedure will use XCTU, XBee Studio, scripted AT
  command mode, API local AT frames, or the Digi Python library.
- Whether future XCTU application or firmware-library update prompts appear
  after the first-run change-log prompt. No application update prompt was
  observed during the install proof.
- Whether the programmed radios can communicate over the air with the selected
  security settings.

## CLI surface

| Command | Behavior | Serial boundary |
| --- | --- | --- |
| `inventory --json` | Reports host environment, WSL serial candidates, Windows COM/PnP hints, XCTU/XBee Studio presence, including per-user Windows `XCTU-NG` installs, and `digi-xbee` import status. | Does not open serial ports. |
| `identity-delta --before FILE --after FILE --json` | Compares two inventory JSON snapshots, hashes or omits raw PnP/hardware IDs, and reports added/removed/changed host candidates. | Does not open serial ports or write bytes. |
| `readonly --port <port> --baud <baud> --confirm-sends-read-commands --json` | Delegates to `scripts/xbee_read_only_probe.py at-query` for the fixed read allowlist. | Sends non-persistent serial read-query bytes only after explicit confirmation. |
| `profile-diff --readback FILE --target FILE --json` | Compares readback JSON to target JSON offline and redacts `SH`, `SL`, and `KY` by default. | Does not open serial ports or write bytes. |
| `write-plan --diff FILE --json` | Emits a blocked review packet with ordered prerequisites and no apply path. | Does not open serial ports or write bytes. |
| `xctu-discovery-plan --ports COMx COMy --json` | Emits a locked GUI checklist for selected local-port discovery only. | Does not launch XCTU, discover devices, open serial ports, or write bytes. |

The CLI has no `apply` command.

## XCTU and CLI mapping

| XCTU or XBee Studio operation | Current status | CLI mapping or gap |
| --- | --- | --- |
| Discover/add local devices | Reference only. Do not use to prove a radio without a bench gate. | `inventory` can report host candidates without opening serial ports; physical identity remains unresolved. |
| Selected-port local discovery checklist | Locked until two ports are proven by physical one-at-a-time disconnect/reconnect deltas plus physical safety evidence. | `xctu-discovery-plan` emits the checklist only; it does not launch XCTU. |
| AT console reads | Allowed only as the existing Tier B fixed read-query gate with explicit confirmation. | `readonly` delegates to the fixed `VR/HV/SH/SL/AP/AO/BD/NP` allowlist. |
| AT setting writes | Blocked. | `profile-diff` and `write-plan` identify review items but cannot apply them. |
| API frame builder/interpreter | Offline reference only. | CLI gap: no API-frame builder; no transmit frame generation. |
| API console/transmit | Blocked. | No CLI transmit command. |
| Firmware explorer | Reference only. | No CLI firmware operation. |
| Firmware update/recovery | Blocked. | No CLI firmware operation. |
| Range test/throughput test | Blocked because it creates live RF behavior. | No CLI range or throughput command. |
| Application update prompts | Host-tool maintenance only after a host install record. First-run evidence showed the 6.5.13 change-log screen and no separate application update prompt. | No repo write/apply action. |

## Future write gate

A later write gate beyond Task 0091 must be Tier 3 and must name the exact
mutation boundary. Minimum prerequisites are same-session adapter identity,
readback backup, installer/tool version record, address plan, AES key handling
process, antenna and regulatory review, carrier voltage/DIN/DOUT proof,
rollback procedure, reviewer quorum, and explicit operator authority.

Outside the Task 0091 selected-port boundary, `WR`, `AC`, setting-value AT
commands, API transmit frames, firmware recovery/update, range tests, and RF
transmit exercises remain blocked.

## Selected-port programming gate

Task 0091 accepted only a local selected-port configuration result. The key
material was not stored in repo records. The accepted post-write state is:

| Port | Accepted local state |
| --- | --- |
| `COM15` | `AP=02`, `AO=00`, `EE=01`, `BD=00000003`, `NP=0100` |
| `COM6` | `AP=02`, `AO=00`, `EE=01`, `BD=00000003`, `NP=0100` |

This gate does not prove over-the-air communication, address allowlisting,
relay command acceptance, ESP32 carrier wiring, adapter voltage, DIN/DOUT
routing, antenna/regulatory deployment state, range, throughput, or
load/mains readiness.

## Continued read-only gate

Task 0088 extends the host-only study with safe `--out` records,
`identity-delta`, and `xctu-discovery-plan`. Host-only WSL and Windows
inventory records were captured under ignored local bench evidence with
`serialOpenAttempted: false`.

The live-radio portion stopped before any serial port was opened. Reviewer
quorum required same-session physical isolation, adapter identity, voltage and
carrier evidence, antenna state, and recovery/cleanup notes before Tier B reads
or XCTU discovery could proceed. No XBee adapter port is confirmed by this
continuation, and the local example XCTU checklist remains locked pending those
prerequisites.

Task 0090 adds a two-device Stage A1/A2 packet. The current accepted result is
still no-serial evidence only: the first disconnect produced one local-only
candidate removal delta, but exact two-adapter identity is not accepted. The
next action is to reconnect the first disconnected adapter, disconnect exactly
the other adapter, and then run another no-serial inventory delta. Tier B reads
and XCTU selected-port discovery remain blocked until both exact ports and
same-session physical evidence are recorded.

Task 0091 supersedes that stop condition only for the user-selected `COM15`
and `COM6` programming gate. It does not close physical adapter marking,
voltage, carrier, antenna/regulatory, ESP32 wiring, or RF communication gaps.

## OTA link proof gate

Task 0092 accepted a minimal bidirectional RF proof for the selected `COM15`
and `COM6` radios. The proof sent one benign `link_probe` payload in each
direction and observed both a source transmit-status frame and a destination
`0x90` receive packet with the matching payload.

This gate does not prove deployment range, throughput, relay command
acceptance, source address allowlisting integration, ESP32 carrier wiring,
adapter voltage, DIN/DOUT routing, antenna/regulatory deployment readiness, or
load/mains readiness.

## ESP32 UART bridge gate

Task 0095 superseded the earlier ambiguous ESP32-connected test by identifying
`COM6` as the ESP32 serial device and `COM15` as the healthy peer XBee. That
test did not prove the ESP32 bridge because `COM6` returned ESP32 serial output
but did not return XBee API local-AT responses or a complete `link_probe`
receive proof.

Task 0096 implements and flashed the permanent raw bridge in firmware after
same-session physical confirmation and rollback backups were recorded. The live
acceptance criteria were:

- `COM6` is flashed only after physical rail/wiring/no-load confirmation and a
  backup or explicit no-backup acceptance.
- After boot-settle and host buffer flush, `COM6` at `115200` returns XBee API
  local-AT readback for `AP=2`, `AO=0`, `BD=3`, and `NP=0x0100`, with
  `SH`/`SL` redacted.
- Peer `COM15` at `9600` returns the expected XBee API local-AT readback.
- Both directions of benign `link_probe` proof show source transmit status
  delivery OK and matching destination `0x90` receive payload.

The accepted evidence directory is
`research/bench-records/xbee-readonly/local-bridge-flash-20260530T012800Z/`.
The first two RF proof helpers failed to observe the `COM15 -> COM6`
destination receive frame; the corrected helper drained the serial ports after
open and then passed both directions with source delivery OK and matching
destination `0x90` payloads.

The bridge gate does not authorize XBee setting writes, `WR`, `AC`, `KY`,
firmware update/recovery beyond the named bridge flash, range/throughput loops,
relay command payloads, relay/load/mains work, broad COM-port scans, or public
raw identifier exposure.

## Validation

The current validation target is:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py self-test --json
PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py list --json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_xbee_radio_study
PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py
git diff --check
```
