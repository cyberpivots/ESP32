# Task 0096 - ESP32 XBee UART Bridge Flash Retest

## Triage

- Verified facts: ADR-0002 accepts ESP-IDF stable v6.0.1 for
  `four-relay-xbee-wifi`. Source IDs: `SRC-ESP-IDF-STABLE-ESP32`,
  `SRC-ESP-IDF-GET-STARTED`.
- Verified facts: Task 0095 corrected the local mapping to `COM6` as the ESP32
  target and `COM15` as the peer XBee, but `COM6` did not expose XBee API
  frames before this bridge implementation. Source ID:
  `SRC-LOCAL-CORRECTED-ESP32-COM6-PEER-COM15-LIVE-TEST-2026-05-30`.
- Verified facts: ESP-IDF UART APIs and GPIO routing are source-backed for
  this project. Source IDs: `SRC-ESP-IDF-UART`, `SRC-ESP-IDF-GPIO`,
  `SRC-ESP32-WROOM-32-DATASHEET`.
- Verified facts: XBee API mode, API options, baud, payload size, local AT
  responses, transmit requests, transmit status, and receive packet frames are
  source-backed. Source IDs: `SRC-DIGI-XBEE-900HP-AP`,
  `SRC-DIGI-XBEE-900HP-AO`, `SRC-DIGI-XBEE-900HP-BD-2026-05-29`,
  `SRC-DIGI-XBEE-900HP-NP`,
  `SRC-DIGI-XBEE-900HP-USER-GUIDE-REFRESH-2026-05-29`.
- Assumptions: User-selected bridge mapping is `COM6` host USB serial at
  `115200 8N1`, ESP32 UART2 at `9600 8N1`, ESP32 GPIO17 TX to XBee DIN, and
  ESP32 GPIO16 RX from XBee DOUT.
- Assumptions: Relay/load/mains remain disconnected, and the XBee side remains
  configured for escaped API mode with `BD=3`.
- Initial unknowns before live execution: same-session physical UART rail/common
  ground, DIN/DOUT direction, antenna state, relay/load/mains isolation,
  pre-flash backup, and rollback evidence still had to be recorded for the
  flash/retest gate.
- Selected tier: Tier 3 overall, with a bounded firmware/docs/audit edit
  subgate before live flash or RF retest.
- Owner role: Firmware with XBee/radio, live-bench, evidence, and QA lenses.
- Evidence need: Source-backed firmware implementation, static audit update,
  ESP-IDF v6.0.1 no-flash build, then same-session live-gate evidence before
  flashing or RF acceptance.
- Mutation boundary: `firmware/projects/four-relay-xbee-wifi/main/main.c`,
  `main/CMakeLists.txt`, firmware audit/docs/status/source records. No live
  flash, serial/RF retest, XBee setting writes, `WR`, `AC`, `KY`,
  reset/restore, broad scan, relay command payload, relay/load/mains action,
  or public raw identifier exposure in the edit subgate.
- Validation plan: Run safe-core host tests, scaffold audits, `git diff
  --check`, and ESP-IDF v6.0.1 build. Live acceptance requires post-flash
  `COM6` local-AT readback and bidirectional benign `link_probe` proof.

## Reviewer Quorum

- Coordinator: approved bounded bridge firmware/docs/audit edits; rejected live
  flash/RF until same-session physical and recovery evidence exists. Weight 5.
- Live Bench: approved bounded edits only; required physical confirmation,
  backup/hash/rollback, COM6-only flash evidence, redacted bridge transcripts,
  and cleanup before live acceptance. Weight 3.
- QA: approved bounded firmware/docs/audit edits; required `esp_driver_uart`,
  a narrow `uart_write_bytes` audit allowlist, static markers, host/static
  tests, and ESP-IDF no-flash build. Weight 3.
- Evidence: approved bounded docs/evidence edits; required source-index/source
  ledger coverage and redaction of raw ESP32 MAC, XBee `SH`/`SL`, keys, PnP
  mappings, and raw passive bytes. Weight 3.

Weighted decision for bounded edits: approval ratio `1.0`, approval weight
`14/14`, no P1/P2 blockers for the named edit boundary.

Initial weighted decision for live flash/RF retest: rejected until the
same-session physical and recovery prerequisites were recorded. After the user
confirmed the physical boundary in this same session, the local live-gate
reviewer quorum approved the named COM6-only bridge flash/retest boundary:
coordinator 5, firmware 3, live-bench 3, comms 3, QA 3, evidence 3; approval
weight `20/20`, no P1/P2 blockers.

## Implementation

The bridge app keeps safe-core defaults initialized but does not touch relay
hardware. UART0 remains the host USB serial path at `115200 8N1`; UART2 is
configured at `9600 8N1` on TX GPIO17 and RX GPIO16 with RTS/CTS disabled.
After app start, ESP-IDF logging is disabled and the bridge loop copies raw
bytes in both directions without printing, parsing, or generating XBee
commands.

The firmware audit now allows `uart_write_bytes` only in
`firmware/projects/four-relay-xbee-wifi/main/main.c` and continues to forbid
relay GPIO writes, Wi-Fi startup, storage mount/erase markers, flash/monitor
strings in firmware source, and embedded XBee setting-write strings.

## Live Gate Requirements

Before any flash:

- Record same-session physical confirmation: ESP32/XBee 3.3 V UART domain,
  common ground, GPIO17 to DIN, GPIO16 from DOUT, antenna attached, and
  relay/load/mains disconnected.
- Record `COM6` identity without broad scans and keep raw MAC local-only.
- Record pre-flash backup or explicit no-backup acceptance, firmware artifact
  hashes, flash command, and rollback/reflash path.

Acceptance after flash:

- Flash output proves only `COM6` was written.
- After hard reset and boot-settle/flush, `COM6` at `115200` returns XBee API
  local-AT readback for `AP=2`, `AO=0`, `BD=3`, `NP=0x0100`; `SH`/`SL`
  remain redacted.
- Peer `COM15` at `9600` returns the expected XBee API local-AT readback.
- `COM6 -> COM15` and `COM15 -> COM6` each show source transmit status
  delivery OK plus a matching destination `0x90` receive packet for the benign
  `link_probe` payload.

## Validation Results

Host/static validation passed:

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py self-test --json`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_xbee_radio_study`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `git diff --check`

ESP-IDF v6.0.1 no-flash build passed with a temporary build directory:

```bash
source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh
idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-four-relay-xbee-wifi-bridge-build build
```

The existing in-repo ignored build directory was configured with a different
case-normalized project path, so the validation build used `/tmp` instead of
running `idf.py fullclean`.

Generated flash settings from the successful build:

- Flash mode: `dio`
- Flash size: `2MB`
- Flash frequency: `40m`
- Offsets: `0x1000` bootloader, `0x8000` partition table, `0x10000` app
- Artifact hashes:
  - `bootloader.bin`: `40844c13870c2e3103df8c5ffc4da944c5cdca178733188e3d400af02ca2fe9c`
  - `partition-table.bin`: `7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820`
  - `four_relay_xbee_wifi.bin`: `8e971877fcfb1cb37dea546e0cd8d5acca1b6c7e782a476c0dff896c7cfcc25a`

## Live Flash and RF Retest Results

Ignored local evidence directory:

```text
research/bench-records/xbee-readonly/local-bridge-flash-20260530T012800Z/
```

Same-session physical confirmation from the user:

- GPIO17 TX to XBee DIN.
- GPIO16 RX from XBee DOUT.
- Shared 3.3 V UART/common ground.
- Antenna attached.
- Relay/load/mains disconnected.
- No other program had `COM6` or `COM15` open.

Recovery and flash evidence:

- `com6-preflash-identity.txt` records COM6-only ESP32 identity and flash-id
  evidence. Raw MAC remains local-only; the flash-id output reported a 4 MB
  physical flash while the generated project flash arguments remained
  `2MB`/`dio`/`40m`.
- `com6-full-flash-pre-bridge.bin` and
  `com6-full-4mb-flash-pre-bridge.bin` are pre-flash rollback backups with
  companion SHA-256 files.
- `com6-bridge-flash.txt` records esptool v5.2.0 writing only `COM6` at
  offsets `0x1000`, `0x8000`, and `0x10000`, followed by hash verification at
  each written region and hard reset.
- `flash-artifacts/` and `flash-artifacts.sha256` preserve the exact binaries
  written during the COM6 flash.

Post-flash bridge/readback evidence:

- `no-open-inventory-com6-com15.txt` records a filtered no-open Windows serial
  inventory showing the two requested port names.
- `passive-com6-115200-after-flash.json` records that WSL Python could not open
  raw `COM6`; `windows-python-pyserial-version.txt` records Windows Python
  pyserial `3.5`; `passive-com6-115200-after-flash-winpy.json` records the
  successful redacted passive COM6 observation through Windows Python.
- `xbee-api-local-at-read-com6-115200.json` records bridge readback on `COM6`
  at host baud `115200` with `AP=2`, `AO=0`, `BD=3`, and `NP=0x0100`;
  `SH`/`SL` remain redacted.
- `xbee-api-local-at-read-com15-9600.json` records peer readback on `COM15` at
  `9600` with the same `AP`, `AO`, `BD`, and `NP` expectations; `SH`/`SL`
  remain redacted.
- The first two RF proof attempts
  `esp32-xbee-api-link-proof-bridge-redacted.json` and
  `esp32-xbee-api-link-proof-bridge-redacted-retry-reverse-first.json` did not
  meet acceptance because the `COM15 -> COM6` destination `0x90` receive packet
  was not observed even though source delivery status was OK.
- The corrected proof
  `esp32-xbee-api-link-proof-bridge-robust-redacted.json` drained both serial
  ports after open, sent benign `link_probe` payloads in both directions, and
  passed acceptance: each direction shows source transmit-status delivery OK
  plus a matching destination `0x90` receive packet. Raw source identifiers
  remain redacted.
- `evidence-manifest.sha256` records hashes for the local evidence artifacts.

Post-live validation rerun passed:

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py self-test --json`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_xbee_radio_study`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `python3 tests/four_relay_safe_core/run_host_tests.py`
- `python3 scripts/scaffold_audit_firmware.py`
- `python3 scripts/scaffold_audit_docs.py`
- `python3 scripts/scaffold_audit_sources.py`
- `python3 scripts/scaffold_audit_agent_process.py`
- `python3 scripts/verify_scaffold.py`
- `git diff --check`

## No-Open Inventory Evidence

Ignored local evidence directory:

```text
research/bench-records/xbee-readonly/local-bridge-20260530T012247Z/
```

Files:

- `list.json`
- `inventory.json`
- `manifest.sha256`

The inventory commands did not open serial ports and did not write serial data.
They confirmed that the expected selected Windows port names are present in the
current host inventory, while keeping private PnP identifiers redacted. Exact
physical wiring and safety state are not proven by no-open inventory.

## Authority Limits

No authority is opened for XBee setting writes, `WR`, `AC`, `KY`, firmware
update/recovery, reset/restore beyond named flash/reset behavior, range or
throughput tests, relay command payloads, relay/load/mains action, public
key/address/MAC exposure, broad COM-port scans, Wi-Fi, storage, TFT, MicroSD,
or release gates.
