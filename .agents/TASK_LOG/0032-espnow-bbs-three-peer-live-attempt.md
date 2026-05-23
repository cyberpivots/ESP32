# Task 0032: ESP-NOW BBS Three-Peer Live Attempt

Status: blocked before backup, build, flash, or Win31 proof

Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Run the full live completion path for the ESP-NOW BBS three-peer bench after a
fresh read-only preflight, then record proof or a blocker.

## Scope

Included:

- Fresh read-only preflight against `COM4`, `COM5`, `COM6`,
  `dospi@192.168.137.93`, and coordinator `/dev/ttyUSB0`.
- Gated `prepare` attempts with `--confirm-read-flash-backups`.
- Two narrow live-gate tooling fixes:
  - generate ignored live config before writing `known_hosts` into the live
    directory,
  - use Pi-compatible `read_flash` for remote coordinator backups and
    `write_flash` in the coordinator recovery command text.
- Cleanup checks after the failed backup.

Excluded:

- Peer full-flash backups, build manifest completion, write flash, verify
  flash, ESP-NOW radio acceptance, bridge launch, DOSBox-X launch, Win31 OPCON
  proof, Program Manager proof, relay, XBee, TFT, MicroSD, load, mains, PCAP,
  packet-driver work, BLE, ESP-WIFI-MESH, router admin, erase, or monitor work.

## Verified Facts

Source ID: `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`.

- Preflight `research/bench-records/live-bench/espnow-bbs-live-preflight-20260523T200026Z.json`
  reported `ok: true` and `readiness: ready_for_prepare`.
- Peer identities from the fresh preflight:
  `COM4=peer01` MAC `94:b9:7e:da:17:d0`,
  `COM5=peer02` MAC `78:e3:6d:0a:90:14`,
  `COM6=peer03` MAC `94:b9:7e:da:9a:50`.
- Coordinator identity from the fresh preflight:
  `/dev/ttyUSB0` MAC `78:e3:6d:10:4d:6c`, ESP32-D0WDQ6, 4 MB flash.
- The successful config-generation portion of prepare wrote ignored live
  overrides under `/mnt/h/dos-c/secrets/espnow-bbs/live-20260523T200237Z/`.
- The coordinator backup failed before any valid backup hash existed:
  Pi `esptool --no-stub --port /dev/ttyUSB0 read_flash 0 ALL ...` reached
  about 50% and returned `A fatal error occurred: Failed to read flash block
  (result was 01090000: CRC or checksum was invalid)`.
- Cleanup found no relevant local or Pi process/listener left behind and the
  failed remote temporary `/tmp` readback file was removed.

## Validation

- `python3 -m py_compile scripts/espnow_bbs_live_gate.py scripts/live_bench_preflight.py`
- `python3 tests/live_bench/test_multipeer_preflight.py`

## Handoff

Use [../handoffs/0022-espnow-bbs-three-peer-live-backup-blocker.md](../handoffs/0022-espnow-bbs-three-peer-live-backup-blocker.md).
