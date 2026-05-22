# Source Ledger - 2026-05-21 Live Bench Toolchain

## Scope

Read-only ESP32/Pi bench identity and ESP-IDF v6.0.1 build proof for
`four-relay-xbee-wifi`. This cycle added a repeatable preflight script,
installed ESP-IDF with EIM, and built the disabled skeleton. It did not flash,
monitor, switch relays, write XBee settings, send ESP-NOW traffic, wire
TFT/MicroSD, attach loads, or perform mains work.

## Sources reviewed

- `SRC-ESP-IDF-GET-STARTED`
- `SRC-ESP-IDF-LINUX-EIM`
- `SRC-ESP-IDF-START-PROJECT`
- `SRC-EIM-CLI-DOCS`
- `SRC-EIM-RELEASE-V0-12-3`
- `SRC-ESPTOOL-BASIC`
- `SRC-RASPBERRY-PI-CONFIGURATION`
- `SRC-LOCAL-LIVE-BENCH-PREFLIGHT-2026-05-21`

## Verified facts

- Windows still reports COM6 as `Silicon Labs CP210x USB to UART Bridge`,
  `USB\VID_10C4&PID_EA60\0001`, status `OK`.
- WSL exposes `/dev/ttyS6` as `root:dialout` with mode `crw-rw----`, and user
  `cyber` is in `dialout`.
- Windows esptool v5.2.0 read-only commands on COM6 reported ESP32-D0WDQ6
  revision v1.0, MAC `78:e3:6d:10:4d:6c`, flash manufacturer `5e`, flash
  device `4016`, 4 MB detected flash size, and 3.3 V flash voltage.
- Fresh Pi SSH fingerprints matched the expected RSA, ECDSA, and ED25519
  fingerprints. SSH identity matched hostname `dos-pi4-poe`, Raspberry Pi 4
  Model B Rev 1.2, serial `10000000aaaa5b24`, root `/dev/mmcblk0p2`,
  address `192.168.200.104`, and no listeners on `31331`, `31332`, or `8080`.
- EIM CLI v0.12.3 was downloaded as `eim-cli-linux-x64.zip`, SHA-256
  `2489cf7f4ea9b09069c6d3d11739eaefba2da43484bd942d619ec166bbfcef46`,
  extracted under `/home/cyber/.local/opt/eim-v0.12.3/`, and used to install
  ESP-IDF v6.0.1 under `/home/cyber/Espressif/v6.0.1/esp-idf`.
- `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh` followed by
  `idf.py --version` reported `ESP-IDF v6.0.1`, and `git describe` in
  `IDF_PATH` reported `v6.0.1`.
- `idf.py -C firmware/projects/four-relay-xbee-wifi build` completed
  successfully and generated `four_relay_xbee_wifi.bin` under ignored
  `firmware/projects/four-relay-xbee-wifi/build/`.

## Assumptions

- COM6 remains a candidate ESP32 target only. USB-UART identity and chip
  identity do not verify carrier-board revision, shield wiring, relay wiring,
  or pinout.
- The Pi target is accepted only while fresh host-key and identity checks match
  the expected evidence.
- Generated `sdkconfig` and `build/` artifacts remain local build products and
  should not be tracked.

## Unknowns

- Physical USB-only, no-load, no relay/TFT/MicroSD/XBee wiring state was not
  proven by the script.
- ESP-IDF activation is not persisted in the shell profile; future builds must
  source the activation script or use EIM run/select explicitly.
- EIM could not copy OpenOCD udev rules to `/etc/udev/rules.d/` without
  elevated permissions; future JTAG/OpenOCD gates need a separate review.
- Flash backup, recovery record, physical no-load evidence, and disabled-image
  static review are still required before any future flash gate can open.

## Workspace updates

- Added `scripts/live_bench_preflight.py`.
- Updated `knowledge-base/source-index.md`.
- Updated `knowledge-base/toolchain/four-relay-xbee-wifi-toolchain.md`.
- Updated `docs/projects/four-relay-xbee-wifi/bench-bring-up-runbook.md`.
- Updated `docs/projects/four-relay-xbee-wifi/rd-loop.md`.
- Updated `docs/index.md`.
- Updated `research/known-gaps.md`.
- Added `.agents/TASK_LOG/0024-live-bench-toolchain.md`.
- Added `.agents/handoffs/0014-live-bench-toolchain-to-firmware-qa.md`.

## Validation

- `python3 scripts/live_bench_preflight.py --out research/bench-records/live-bench/local-preflight-20260521T195100Z.json`: PASS.
- `python3 scripts/live_bench_preflight.py --skip-esp32 --skip-pi --out research/bench-records/live-bench/local-smoke-20260521Tfinal.json`: PASS.
- `/home/cyber/.local/opt/eim-v0.12.3/eim list`: PASS, `v6.0.1 (selected)`.
- `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py --version && git -C "$IDF_PATH" describe --tags --always`: PASS, `ESP-IDF v6.0.1`, `v6.0.1`.
- `idf.py -C firmware/projects/four-relay-xbee-wifi build`: PASS.
- `python3 tests/four_relay_safe_core/run_host_tests.py`: PASS.
- `python3 tests/esp32_gateway_tcp/test_protocol.py`: PASS.
- `python3 scripts/verify_scaffold.py`: PASS.
- `python3 scripts/build_github_pages.py --out build/github-pages`: PASS.
- `python3 scripts/audit_public_manifest.py`: PASS.
- `python3 scripts/smoke_github_pages.py`: PASS.
- `python3 -m py_compile scripts/*.py tests/four_relay_safe_core/run_host_tests.py tests/esp32_gateway_tcp/test_protocol.py`: PASS.
- `git diff --check`: PASS.
