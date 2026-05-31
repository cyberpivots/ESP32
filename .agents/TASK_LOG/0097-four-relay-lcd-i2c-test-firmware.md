# Task 0097 - Four Relay LCD I2C Test Firmware

## Triage

- Verified facts: ADR-0002 accepts ESP-IDF stable v6.0.1 for
  `four-relay-xbee-wifi`. Source IDs: `SRC-ESP-IDF-STABLE-ESP32`,
  `SRC-ESP-IDF-GET-STARTED`.
- Verified facts: the current COM6 bridge firmware records UART0 host
  `115200`, UART2 XBee `9600`, TX GPIO17, RX GPIO16, no hardware flow control,
  no app logging in the bridge loop, and accepted COM6 bridge flash/RF proof.
  Source ID: `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`.
- Verified facts: ESP-IDF stable v6.0.1 documents `driver/i2c_master.h`,
  `esp_driver_i2c`, `i2c_new_master_bus`, `i2c_master_probe`, and
  `i2c_master_transmit`. Source ID: `SRC-ESP-IDF-I2C`.
- Verified facts: the workspace has only candidate/reference coverage for
  PCF8574/PCF8574A-class I2C expanders and does not verify the exact LCD
  backpack. Source ID: `SRC-NXP-PCF8574-74A`.
- Assumptions: the LCD is HD44780-compatible with a PCF8574/PCF8574A backpack
  using P0=RS, P1=RW, P2=E, P3=backlight, and P4-P7=D4-D7.
- Assumptions: the later live LCD-only gate will use GPIO21 SDA and GPIO22 SCL
  through the installed level shifter with common ground and external pullups.
- Unknowns at preparation time: exact LCD module, controller, backpack IC,
  address, pullup voltage, logic voltage, contrast, backlight current,
  rail-current margin, COM6 availability, and visual LCD page proof. The later
  live gate resolved COM6 availability and visual LCD page proof only.
- Selected tier: Tier 3 overall; this task records a bounded no-flash
  firmware/docs/audit/build-only subgate.
- Owner role: Firmware with Hardware, Communications, Live Bench, Evidence,
  and QA lenses.
- Evidence need: source-backed I2C API coverage, bridge-preservation audit,
  durable LCD-only source records, host/static validation, ESP-IDF v6.0.1
  no-flash build, and later same-session physical/recovery proof before flash.
- Mutation boundary: `firmware/projects/four-relay-xbee-wifi/main/main.c`,
  `main/CMakeLists.txt`, firmware audit scripts, firmware/four-relay docs,
  source/status/index records. No live flash, monitor, serial/RF action, XBee
  setting writes, relay GPIO, relay expander outputs, encoder GPIOs,
  range/throughput, relay/load/mains, or broad COM scan in this subgate.
- Validation plan: safe-core host tests, firmware/docs/source/agent-process
  audits, scaffold verifier, `git diff --check`, and ESP-IDF v6.0.1 no-flash
  build using a temporary build directory.

## Reviewer Quorum

- Coordinator: approved narrowed local firmware/docs/audit/build-only mutation
  that preserves the COM6 bridge; rejected live flash until same-session LCD
  facts and recovery evidence exist. Weight 5.
- Live Bench: approved narrowed no-flash mutation only; required fresh physical
  confirmation, backup/hash/recovery, COM6-only flash evidence, visual LCD
  proof, and cleanup before live acceptance. Weight 3.
- QA: initially rejected until P2 items were added: ESP-IDF I2C source
  coverage, narrow LCD I2C audit allowlist, bridge-preservation checks,
  durable records, and validation. Weight 3.
- Evidence: approved records/audit/build-only preparation after durable records
  and closed-surface wording were added. Weight 3.

Weighted decision for the narrowed local mutation after required P2 conditions
are included: approval weight `14/14`, no live authority.

## Implementation

The firmware keeps the COM6 raw bridge as the default app behavior. It adds a
low-priority LCD task that:

- Uses ESP-IDF v6.0.1 `driver/i2c_master.h` and `esp_driver_i2c`.
- Uses I2C0, GPIO21 SDA, GPIO22 SCL, 100 kHz, and no internal pullups.
- Probes only PCF8574/PCF8574A candidate ranges `0x20-0x27` and `0x38-0x3f`.
- Requires exactly one detected address and exits without blocking the bridge
  when zero or multiple candidates are detected.
- Writes HD44780-style 20x4 pages using the requested P0/P1/P2/P3/P4-P7
  mapping.
- Shows LCD identity, I2C pins/address, bridge baud/counters, a full-width
  character pattern, and safety/no-encoder/no-XBee-write status pages.

The firmware does not implement rotary encoder GPIOs and does not embed XBee
setting-write commands.

## Live Gate Requirements

Before any flash:

- User confirms in this same session that COM6 is free.
- User confirms the 20x4 I2C LCD is connected through the installed level
  shifter on GPIO21/GPIO22 with common ground.
- User confirms relay/load/mains remain disconnected.
- Record a COM6 pre-flash backup with artifact hashes and a rollback path.
- Build with ESP-IDF v6.0.1 and flash only COM6 using generated offsets and
  flash arguments.

Acceptance after flash:

- Flash transcript proves only COM6 was written and verified.
- No XBee local-AT, RF `link_probe`, range, throughput, relay, encoder, load,
  or mains test is run.
- User visually confirms the LCD cycles through the test/status pages and shows
  the detected I2C address.

## Validation Results

Host/static validation passed:

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `git diff --check`

ESP-IDF v6.0.1 no-flash build passed with a temporary build directory:

```bash
source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh
idf.py -C firmware/projects/four-relay-xbee-wifi -B /tmp/esp32-four-relay-xbee-wifi-lcd-build build
```

Generated flash settings from the successful build:

- Flash mode: `dio`
- Flash size: `2MB`
- Flash frequency: `40m`
- Offsets: `0x1000` bootloader, `0x8000` partition table, `0x10000` app
- Artifact hashes:
  - `bootloader.bin`: `ce056ceb001be6bc777e2025fb6206895fd80f91e6492ed5224e596f708bf2db`
  - `partition-table.bin`: `7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820`
  - `four_relay_xbee_wifi.bin`: `9eff9abd3429c832c41789fda6b989ea2bf890f57b060d676326b82ac7851fe6`

## Live LCD-Only Flash Results

Same-session user gate confirmation was received for COM6 availability, LCD
GPIO21/GPIO22 level-shifter/common-ground wiring, and relay/load/mains
disconnect state.

Local ignored evidence directory:
`research/bench-records/xbee-readonly/local-lcd-flash-20260530T031011Z/`.

Live validation completed:

- Targeted COM6 no-open inventory found the CP210x USB-UART bridge on COM6.
- COM6 esptool identity read succeeded and reported ESP32 with 4MB flash.
- Fresh pre-flash rollback backups were recorded:
  - 2MB backup:
    `dd664f0906d532f31a13987c60b90b2626efe68948c1de5d743a327dfc9929ba`
  - 4MB backup:
    `665ea6c7496593776ebcf2e9d737483e2441617b2c2dc2b9be11f3ba2cdc810b`
- Fresh ESP-IDF v6.0.1 build reproduced the prior artifact hashes.
- COM6-only `write-flash` succeeded at offsets `0x1000`, `0x8000`, and
  `0x10000`.
- COM6-only `verify-flash` succeeded for bootloader, partition table, and app
  images with matching digests.
- User visual acceptance was received as `LCD VISUAL RESULT: PASS`; local
  visual proof note hash:
  `556a88d7f9878ef6893635bd4210ca8cb244e59142a05c2499f5d395d493e920`.
- Evidence manifest: `evidence-manifest.sha256`.

LCD visual acceptance passed: the user confirmed the LCD cycles pages, shows an
`ADDR 0x..` line, and renders all four 20-character rows cleanly. No serial
monitor, XBee local-AT, RF `link_probe`, range, throughput, relay, encoder,
load, or mains test was run during this LCD-only flash gate.

## Authority Limits

The completed live authority was limited to COM6 backup, COM6 LCD firmware
write/verify, and visual LCD proof request. No authority is opened for serial
monitor, XBee setting writes, `WR`, `AC`, `KY`, RF retest, range/throughput,
relay command payloads, relay GPIO writes, relay expander outputs, encoder
GPIOs, relay/load/mains action, broad COM-port scans, or public raw identifier
disclosure.
