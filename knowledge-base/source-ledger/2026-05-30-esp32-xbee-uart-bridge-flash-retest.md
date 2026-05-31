# Source Ledger - 2026-05-30 ESP32 XBee UART Bridge Flash Retest

## Scope

Tier 3 bridge implementation and live-gate packet for making the ESP32 on
`COM6` expose the XBee attached to UART2/GPIO17/GPIO16 as raw USB serial at
host baud `115200`.

This record covers the bounded firmware/docs/audit edit gate and the later
same-session COM6-only flash/RF retest gate. Raw ESP32 MAC, XBee `SH`/`SL`, and
raw radio addresses remain local-only.

## Sources

- ESP-IDF stable v6.0.1 project target: `SRC-ESP-IDF-STABLE-ESP32`,
  `SRC-ESP-IDF-GET-STARTED`.
- UART and GPIO API context: `SRC-ESP-IDF-UART`, `SRC-ESP-IDF-GPIO`.
- ESP32 module/pin context: `SRC-ESP32-WROOM-32-DATASHEET`.
- Flash argument and verification context for a later live gate:
  `SRC-ESPTOOL-BASIC`, `SRC-ESPTOOL-ADVANCED-VERIFY`,
  `SRC-ESP-IDF-BUILD-SYSTEM-FLASH-ARGS`.
- XBee API and readback context: `SRC-DIGI-XBEE-900HP-AP`,
  `SRC-DIGI-XBEE-900HP-AO`, `SRC-DIGI-XBEE-900HP-BD-2026-05-29`,
  `SRC-DIGI-XBEE-900HP-NP`,
  `SRC-DIGI-XBEE-900HP-USER-GUIDE-REFRESH-2026-05-29`.
- Local XBee setup and RF lineage:
  `SRC-LOCAL-XBEE-SELECTED-PORT-PROGRAMMING-2026-05-29`,
  `SRC-LOCAL-XBEE-OTA-LINK-PROOF-2026-05-29`,
  `SRC-LOCAL-CORRECTED-ESP32-COM6-PEER-COM15-LIVE-TEST-2026-05-30`.

## Verified Facts

- Task 0095 identified `COM6` as the ESP32 serial device and `COM15` as the
  healthy XBee API peer at `9600`, but did not prove the ESP32 bridge.
- The bridge firmware initializes safe-core defaults and configures:
  UART0 host `115200 8N1`, UART2 XBee `9600 8N1`, TX GPIO17, RX GPIO16, and no
  UART hardware flow control.
- The bridge disables app logging after startup and does not call `printf` or
  `ESP_LOG*` in the copy loop.
- The firmware source does not embed XBee setting-write commands, `WR`, `AC`,
  or `KY`.
- The main component depends on `safe_core` and `esp_driver_uart`.
- The firmware audit now narrowly permits `uart_write_bytes` only in the bridge
  source and retains blocked markers for relay GPIO, Wi-Fi, storage mount/erase,
  flash/monitor strings, XBee setting writes, relay/load, and mains surfaces.
- Same-session user confirmation for the live gate recorded GPIO17 TX to XBee
  DIN, GPIO16 RX from XBee DOUT, shared 3.3 V UART/common ground, antenna
  attached, relay/load/mains disconnected, and no other program holding `COM6`
  or `COM15`.
- The COM6 flash gate wrote only the ESP32 on `COM6` with generated
  `2MB`/`dio`/`40m` arguments at offsets `0x1000`, `0x8000`, and `0x10000`.
  esptool verified the written hashes after each region.
- Post-flash bridge local-AT readback on `COM6` at host baud `115200` returned
  `AP=2`, `AO=0`, `BD=3`, and `NP=0x0100`; peer `COM15` at `9600` returned
  the same expected API/baud/payload readback values.
- The corrected RF proof passed in both directions after serial-drain handling:
  each benign `link_probe` direction showed source transmit-status delivery OK
  and a matching destination `0x90` receive packet.

## Assumptions

- The XBee associated with the ESP32 remains at `BD=3` / `9600`.
- The user intended the bridge firmware to remain installed after retest.

## Unknowns

- The live gate records shared 3.3 V UART/common ground as operator-confirmed
  wiring state, but it does not establish a measured rail-current margin for
  broader hardware expansion.
- Deployment range, throughput, address allowlisting integration, antenna and
  regulatory deployment review, relay command acceptance, relay/load/mains
  readiness, and future XBee setting-write authority remain separate closed
  gates.

## Redaction Rules

Keep local-only: ESP32 MAC, XBee `SH`/`SL`, raw radio addresses, AES key
material, address plans, raw passive serial bytes, private COM/PnP mappings,
and full setting snapshots.

## Validation Plan

Host/static validation:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py self-test --json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_xbee_radio_study
PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py
git diff --check
```

ESP-IDF no-flash build:

```bash
source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh
idf.py -C firmware/projects/four-relay-xbee-wifi build
```

Live acceptance required COM6-only flash proof, post-reset bridge readback,
peer readback, and bidirectional benign `link_probe` RF proof. The live gate
was opened only after same-session physical confirmation and rollback backups.

## Validation Results

Pre-live validation passed:

- XBee read-only probe self-test.
- XBee radio study unit tests.
- Four-relay safe-core host tests.
- Full scaffold audit unittest discovery.
- Documentation audit.
- Source audit.
- Scaffold verifier.
- `git diff --check`.
- ESP-IDF v6.0.1 no-flash build using:

```bash
idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-four-relay-xbee-wifi-bridge-build build
```

The default ignored build directory had a stale case-variant project path, so
the no-flash validation build used a temporary build directory rather than
cleaning existing artifacts.

Successful build flash settings:

```text
--flash-mode dio --flash-freq 40m --flash-size 2MB
0x1000 bootloader/bootloader.bin
0x8000 partition_table/partition-table.bin
0x10000 four_relay_xbee_wifi.bin
```

Successful build artifact hashes:

```text
40844c13870c2e3103df8c5ffc4da944c5cdca178733188e3d400af02ca2fe9c  bootloader.bin
7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820  partition-table.bin
8e971877fcfb1cb37dea546e0cd8d5acca1b6c7e782a476c0dff896c7cfcc25a  four_relay_xbee_wifi.bin
```

Live evidence was captured under:

```text
research/bench-records/xbee-readonly/local-bridge-flash-20260530T012800Z/
```

Live gate results:

- `com6-preflash-identity.txt`: COM6-only ESP32 identity and flash-id evidence;
  raw MAC remains local-only. The flash-id output reported 4 MB physical flash;
  the project image was still written with generated `2MB` flash arguments.
- `com6-full-flash-pre-bridge.bin` and
  `com6-full-4mb-flash-pre-bridge.bin`: pre-flash rollback backups with
  companion SHA-256 records.
- `com6-bridge-flash.txt`: esptool v5.2.0 wrote only `COM6` and verified hashes
  at offsets `0x1000`, `0x8000`, and `0x10000`.
- `xbee-api-local-at-read-com6-115200.json`: bridge local-AT readback passed
  with `AP=2`, `AO=0`, `BD=3`, `NP=0x0100`, and redacted `SH`/`SL`.
- `xbee-api-local-at-read-com15-9600.json`: peer local-AT readback passed with
  the same expected values and redacted `SH`/`SL`.
- `esp32-xbee-api-link-proof-bridge-redacted.json` and
  `esp32-xbee-api-link-proof-bridge-redacted-retry-reverse-first.json`: initial
  RF proof attempts failed acceptance because the `COM15 -> COM6` destination
  receive packet was not observed.
- `esp32-xbee-api-link-proof-bridge-robust-redacted.json`: corrected proof
  passed both directions with source `0x8b` delivery OK and destination `0x90`
  payload match for benign `link_probe`.
- `evidence-manifest.sha256`: hashes local evidence artifacts.

Post-live validation rerun passed:

- XBee read-only probe self-test.
- XBee radio study unit tests.
- Full scaffold audit unittest discovery.
- Four-relay safe-core host tests.
- Firmware audit.
- Documentation audit.
- Source audit.
- Agent-process audit.
- Scaffold verifier.
- `git diff --check`.

## No-Open Inventory Evidence

Ignored local evidence was captured under:

```text
research/bench-records/xbee-readonly/local-bridge-20260530T012247Z/
```

The `list` and `inventory` records report `serialOpenAttempted: false` or the
equivalent no-open boundary, and no serial writes were attempted. Private PnP
identifiers remain redacted. This evidence confirms current host-visible
selected port names only; it does not prove physical wiring, rail voltage,
common ground, antenna state, relay/load/mains isolation, or bridge operation.

## Closed Surfaces

- No XBee setting writes, `WR`, `AC`, or `KY`.
- No firmware update/recovery or reset/restore beyond the named bridge flash
  and hard reset gate.
- No broad COM-port scan or all-device discovery.
- No range or throughput loop.
- No relay command payloads.
- No relay, load, or mains action.
- No public raw address, key, MAC, PnP, or passive-byte disclosure.
