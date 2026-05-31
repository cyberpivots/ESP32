# Source Ledger - 2026-05-30 Four Relay LCD I2C Test Firmware

## Scope

Tier 3 LCD-only firmware/docs/audit preparation and COM6-only flash for adding
a display-status test to the existing `four-relay-xbee-wifi` COM6 bridge
firmware.

This record covers the build-only mutation gate and the later same-session
COM6-only LCD flash gate. It does not authorize serial monitor, XBee setting
writes, RF retest, range/throughput, relay/load/mains work, encoder GPIOs, or
exact LCD hardware/electrical acceptance beyond the user visual display proof.

## Sources

- ESP-IDF stable v6.0.1 project target: `SRC-ESP-IDF-STABLE-ESP32`,
  `SRC-ESP-IDF-GET-STARTED`.
- ESP-IDF I2C, UART, and GPIO API context: `SRC-ESP-IDF-I2C`,
  `SRC-ESP-IDF-UART`, `SRC-ESP-IDF-GPIO`.
- ESP32 module/pin context: `SRC-ESP32-WROOM-32-DATASHEET`,
  `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.
- Candidate PCF8574/PCF8574A class context: `SRC-NXP-PCF8574-74A`.
- Current bridge lineage:
  `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`.

## Verified Facts

- The current firmware remains the permanent COM6 raw bridge path:
  UART0 host `115200`, UART2 XBee `9600`, TX GPIO17, RX GPIO16, no hardware
  flow control, and app logging disabled after startup.
- The LCD task uses ESP-IDF v6.0.1 `driver/i2c_master.h` through
  `esp_driver_i2c`.
- The LCD task is display-only and uses I2C0, GPIO21 SDA, GPIO22 SCL, 100 kHz,
  and no internal pullups.
- The LCD task probes only PCF8574/PCF8574A candidate ranges `0x20-0x27` and
  `0x38-0x3f`, requires exactly one detected address, and exits without
  blocking the bridge when zero or multiple candidates are found.
- The LCD task writes HD44780-style 20x4 pages through the requested common
  PCF8574 mapping: P0=RS, P1=RW, P2=E, P3=backlight, P4-P7=D4-D7.
- Display pages include LCD identity, I2C pins/address, bridge baud/counters,
  a full-width character pattern, and safety/no-encoder/no-XBee-write status.
- Firmware source does not configure rotary encoder GPIOs.
- Firmware source does not embed XBee setting-write commands, quoted `WR`,
  quoted `AC`, or quoted `KY`.

## Assumptions

- The physical LCD is HD44780-compatible and uses the requested common PCF8574
  backpack mapping.
- GPIO21/GPIO22 are connected through the installed level shifter, with common
  ground and external pullups in the LCD/level-shifter path.
- LCD backlight/current draw and rail-current margin remain assumed, not
  measured, during the COM6-only flash gate.

## Unknowns

- Exact LCD module, controller, backpack IC, address, pullup voltage, logic
  voltage, contrast, backlight current, and rail-current margin remain
  unresolved.
- Same-session COM6 availability, LCD wiring, and relay/load/mains isolation
  were confirmed by the user for the live LCD-only flash gate, but exact LCD
  electrical details remain unresolved.
- User visual confirmation passed for LCD page cycling, detected-address line
  display, and clean four-row rendering.

## Reviewer Quorum

- Coordinator, weight 5: approved narrowed firmware/docs/audit/build-only
  mutation that preserves COM6 bridge behavior; rejected flash until a fresh
  same-session LCD-only gate exists.
- Live Bench, weight 3: approved narrowed no-flash bridge-preserving mutation;
  required fresh physical confirmation, backup/hash/recovery, COM6-only flash
  proof, and cleanup before live acceptance.
- QA, weight 3: initially rejected until ESP-IDF I2C source coverage, audit
  allowlist, bridge-preservation checks, durable records, and validation were
  added.
- Evidence, weight 3: approved records/audit/build-only preparation after
  durable LCD-only source records and closed-surface wording are added.

Weighted disposition for the narrowed local mutation after the required P2
items are included: `14/14` conditional approval for firmware/docs/audit
preparation only, no live authority.

## Validation Plan

Host/static validation:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py
git diff --check
```

ESP-IDF no-flash build:

```bash
source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh
idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-four-relay-xbee-wifi-lcd-build build
```

Live validation remains closed until same-session facts confirm COM6 is free,
the LCD is connected through the level shifter on GPIO21/GPIO22 with common
ground, and relay/load/mains remain disconnected.

## Validation Results

Build-only validation passed:

- Four-relay safe-core host tests.
- Firmware audit.
- Documentation audit.
- Source audit.
- Agent-process audit.
- Full scaffold audit unittest discovery: 45 tests.
- Scaffold verifier.
- `git diff --check`.
- ESP-IDF v6.0.1 no-flash build using:

```bash
idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-four-relay-xbee-wifi-lcd-build build
```

Generated flash settings from the successful build:

```text
--flash-mode dio --flash-freq 40m --flash-size 2MB
0x1000 bootloader/bootloader.bin
0x8000 partition_table/partition-table.bin
0x10000 four_relay_xbee_wifi.bin
```

Successful build artifact hashes:

```text
ce056ceb001be6bc777e2025fb6206895fd80f91e6492ed5224e596f708bf2db  bootloader.bin
7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820  partition-table.bin
9eff9abd3429c832c41789fda6b989ea2bf890f57b060d676326b82ac7851fe6  four_relay_xbee_wifi.bin
```

## Live LCD-Only Flash Results

Same-session LCD-only authority was received for COM6 backup, COM6 firmware
write/verify, and visual LCD proof request. Local ignored evidence was recorded
under:

```text
research/bench-records/xbee-readonly/local-lcd-flash-20260530T031011Z/
```

Live validation completed:

- Targeted COM6 no-open inventory found the CP210x USB-UART bridge on COM6.
- COM6 esptool identity read succeeded and reported ESP32 with 4MB flash.
- Fresh rollback backup hashes:
  - 2MB:
    `dd664f0906d532f31a13987c60b90b2626efe68948c1de5d743a327dfc9929ba`
  - 4MB:
    `665ea6c7496593776ebcf2e9d737483e2441617b2c2dc2b9be11f3ba2cdc810b`
- Copied flash artifact hashes matched the no-flash build hashes above.
- COM6-only `write-flash` succeeded at `0x1000`, `0x8000`, and `0x10000`.
- COM6-only `verify-flash` succeeded for all three images with matching
  digests.
- User visual acceptance was received as `LCD VISUAL RESULT: PASS`; local
  visual proof note hash:
  `556a88d7f9878ef6893635bd4210ca8cb244e59142a05c2499f5d395d493e920`.
- Evidence manifest: `evidence-manifest.sha256`.

LCD visual acceptance passed: the user confirmed the LCD cycles pages, shows an
`ADDR 0x..` line, and renders all four 20-character rows cleanly. No serial
monitor, XBee local-AT, RF `link_probe`, range, throughput, relay, encoder,
load, or mains test was run during this LCD-only flash gate.

## Closed Surfaces

- No serial monitor, erase, or serial-port write action outside COM6 esptool
  backup/write/verify.
- No XBee setting writes, `WR`, `AC`, or `KY`.
- No RF `link_probe`, range, or throughput retest.
- No relay GPIO writes, relay expander outputs, relay command payloads,
  relay/load/mains action, or mains preparation.
- No encoder GPIO implementation.
- No public raw ESP32 MAC, XBee `SH`/`SL`, AES key, raw radio address, PnP
  mapping, or passive serial-byte disclosure.
