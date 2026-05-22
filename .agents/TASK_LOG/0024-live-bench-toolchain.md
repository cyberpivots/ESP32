# Task 0024 - Live Bench Toolchain

## Task

- ID: 0024-live-bench-toolchain
- Owner role: Firmware, Hardware, Communications, QA, Release
- Status: complete
- Created: 2026-05-21
- Updated: 2026-05-21

## Goal

Close the next reversible live-bench gap for `four-relay-xbee-wifi` by
recording fresh read-only ESP32/Pi identity evidence, installing or locating
ESP-IDF v6.0.1, and proving the disabled skeleton builds without flashing or
mutating hardware state.

## Scope

Included:

- Repeatable read-only preflight script for Windows COM6, WSL `/dev/ttyS6`,
  ESP32 esptool identity, Pi SSH identity, listener checks, and toolchain
  inventory.
- Local ESP-IDF v6.0.1 install via EIM CLI and activation proof.
- Disabled `four-relay-xbee-wifi` ESP-IDF build proof.
- Source-index, toolchain ledger, runbook, R&D loop, known-gaps, source-ledger,
  task-record, and handoff updates.

Excluded:

- Firmware flashing, serial monitor automation, relay switching, XBee writes,
  ESP-NOW radio traffic, TFT/MicroSD wiring, load wiring, mains work, Pi
  capability changes, persistent Pi bridge services, and public deployment.

## Sources

- `SRC-ESP-IDF-GET-STARTED`
- `SRC-ESP-IDF-LINUX-EIM`
- `SRC-ESP-IDF-START-PROJECT`
- `SRC-EIM-CLI-DOCS`
- `SRC-EIM-RELEASE-V0-12-3`
- `SRC-ESPTOOL-BASIC`
- `SRC-RASPBERRY-PI-CONFIGURATION`
- `SRC-LOCAL-LIVE-BENCH-PREFLIGHT-2026-05-21`

## Decisions

- COM6 remains only a candidate ESP32 target. USB-UART and chip identity do not
  prove carrier-board revision, shield wiring, relay wiring, or final pinout.
- The preflight script allows only read-only esptool identity commands:
  `chip_id`, `read_mac`, and `flash_id`.
- Pi SSH is gated by fresh host-key fingerprint comparison and then limited to
  identity, root source, address, listener, and process checks.
- Generated `sdkconfig` and `build/` output from the ESP-IDF build are ignored
  local artifacts and must not be tracked.
- Future flashing remains blocked until physical no-load evidence, candidate
  identity, a private recovery record, and disabled-image static review are all
  satisfied.

## Validation

- `python3 scripts/live_bench_preflight.py --out research/bench-records/live-bench/local-preflight-20260521T195100Z.json`:
  PASS.
- `python3 scripts/live_bench_preflight.py --skip-esp32 --skip-pi --out research/bench-records/live-bench/local-smoke-20260521Tfinal.json`:
  PASS.
- `/home/cyber/.local/opt/eim-v0.12.3/eim list`: PASS, `v6.0.1 (selected)`.
- `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py --version && git -C "$IDF_PATH" describe --tags --always`:
  PASS, `ESP-IDF v6.0.1`, `v6.0.1`.
- `idf.py -C firmware/projects/four-relay-xbee-wifi build`: PASS.
- `python3 tests/four_relay_safe_core/run_host_tests.py`: PASS.
- `python3 tests/esp32_gateway_tcp/test_protocol.py`: PASS.
- `python3 scripts/verify_scaffold.py`: PASS.
- `python3 scripts/build_github_pages.py --out build/github-pages`: PASS.
- `python3 scripts/audit_public_manifest.py`: PASS.
- `python3 scripts/smoke_github_pages.py`: PASS.
- `python3 -m py_compile scripts/*.py tests/four_relay_safe_core/run_host_tests.py tests/esp32_gateway_tcp/test_protocol.py`:
  PASS.
- `git diff --check`: PASS.

## Handoff

Continue through
`.agents/handoffs/0014-live-bench-toolchain-to-firmware-qa.md`. Firmware and
QA now have a buildable disabled skeleton, but no live flash, monitor, relay,
radio, storage, load, or mains gate was opened.
