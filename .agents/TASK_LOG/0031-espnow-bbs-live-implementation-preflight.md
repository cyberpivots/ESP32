# Task 0031: ESP-NOW BBS Live Implementation Preflight

Status: blocked before backup or flash

Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Continue toward live three-peer ESP-NOW BBS implementation by running the
read-only live gate, recording the current blocker, and improving the preflight
tooling so future live attempts produce a compact operator summary.

## Scope

Included:

- Ran `scripts/live_bench_preflight.py` read-only against expected peers
  `COM4`, `COM5`, and `COM6`, Pi `172.16.0.2`, and coordinator
  `/dev/ttyUSB0`.
- Added accepted forwarded Pi access support for `192.168.137.93` while still
  requiring the expected Pi host-key, hostname, serial, `eth0=172.16.0.2/24`,
  stale listener, stale process, and coordinator gates.
- Added a `--summary` output mode and `--from-record` revalidation mode to the
  preflight tool.
- Added fixture tests for summary readiness, forwarded Pi host profile use, Pi
  identity blocker reporting, and Pi-side esptool blocker reporting.
- Installed Debian Trixie `esptool` `4.7.0+dfsg-0.1` on the verified Pi after
  package-policy and non-interactive sudo checks.
- Updated Pi-side coordinator esptool calls to use `--no-stub` because the
  Debian package's default stub mode failed with a missing
  `stub_flasher_32.json` file.
- Added source-index, source-ledger, and project README entries for the fresh
  live preflight.

Excluded:

- `read-flash` backups, build generation, flash, monitor automation, ESP-NOW
  radio traffic, router mutation, relay, XBee, TFT, MicroSD, load, mains,
  PCAP, packet-driver work, BLE pairing, Android build, or ESP-WIFI-MESH radio
  work.

## Current Evidence

Source ID: `SRC-LOCAL-ESPNOW-LIVE-PREFLIGHT-2026-05-23`.

Verified:

- Windows inventory contains exactly `COM4`, `COM5`, and `COM6` CP210x
  VID:PID `10C4:EA60` peers.
- Read-only esptool identity passed for all three Windows peers:
  `COM4` MAC `94:b9:7e:da:17:d0`, `COM5` MAC `78:e3:6d:0a:90:14`, and
  `COM6` MAC `94:b9:7e:da:9a:50`.
- All three Windows peers reported ESP32-D0WDQ6 profile evidence and 4 MB
  flash.

Earlier blockers:

- Direct Pi `172.16.0.2` returned no SSH host keys and ping/TCP 22 failed.
- Accepted forwarded Pi access at `192.168.137.93` passed Pi identity and
  `/dev/ttyUSB0` presence gates.
- Coordinator `/dev/ttyUSB0` identity was blocked until Pi `esptool` was
  installed and `--no-stub` was used.

Current gate:

- `python3 scripts/live_bench_preflight.py --pi-host 192.168.137.93 --summary`
  now reports `readiness: ready_for_prepare` with coordinator MAC
  `78:e3:6d:10:4d:6c`.
- Backup/manifest preparation still requires same-session physical
  USB-only/no-load/no-relay/no-XBee/no-TFT/no-MicroSD confirmation.

## Validation

- `python3 -m py_compile scripts/live_bench_preflight.py scripts/espnow_bbs_live_gate.py`
- `python3 tests/live_bench/test_multipeer_preflight.py`
- `python3 scripts/live_bench_preflight.py --from-record research/bench-records/live-bench/espnow-bbs-live-preflight-20260523T192610Z.json --summary`
  returned the expected blocked exit code `2` with readiness
  `blocked_pi_identity`.
- `python3 scripts/live_bench_preflight.py --pi-host 192.168.137.93 --summary --out research/bench-records/live-bench/espnow-bbs-live-preflight-forwarded-20260523T1938Z.json`
  returned the expected blocked exit code `2` with readiness
  `blocked_coordinator_identity` before the distinct Pi esptool blocker was
  added.
- `python3 scripts/live_bench_preflight.py --from-record research/bench-records/live-bench/espnow-bbs-live-preflight-forwarded-20260523T1938Z.json --summary`
  returned the expected blocked exit code `2` with readiness
  `blocked_pi_esptool`.
- `python3 scripts/live_bench_preflight.py --pi-host 192.168.137.93 --summary --out research/bench-records/live-bench/espnow-bbs-live-preflight-forwarded-nostub-20260523T1945Z.json`
  passed with readiness `ready_for_prepare`.
- `python3 scripts/verify_scaffold.py`

## Handoff

Use [../handoffs/0021-espnow-bbs-live-implementation-blocker.md](../handoffs/0021-espnow-bbs-live-implementation-blocker.md).
