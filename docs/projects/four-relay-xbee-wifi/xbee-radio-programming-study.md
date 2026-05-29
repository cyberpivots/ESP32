# XBee Radio Programming Study

## Scope

This study turns the existing XBee read-only proof into a staged programming
study path. It does not authorize radio setting writes, `WR`, `AC`, firmware
updates, API transmit frames, range tests, relay actions, ESP32 DIN/DOUT
wiring, or load/mains work.

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

A later write gate must be Tier 3 and must name the exact mutation boundary.
Minimum prerequisites are same-session adapter identity, readback backup,
installer/tool version record, address plan, AES key handling process, antenna
and regulatory review, carrier voltage/DIN/DOUT proof, rollback procedure,
reviewer quorum, and explicit operator authority.

Until that gate exists, `WR`, `AC`, setting-value AT commands, API transmit
frames, firmware recovery/update, range tests, and RF transmit exercises remain
blocked.

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
