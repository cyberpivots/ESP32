# ESP-NOW BBS Live Gate Tooling Source Ledger

Accessed: 2026-05-23

Source index: [../source-index.md](../source-index.md)

## Sources Used

- `SRC-ESP-IDF-ESPNOW`
- `SRC-ESPTOOL-BASIC`
- `SRC-ESPTOOL-ADVANCED-VERIFY`
- `SRC-ESP-IDF-BUILD-SYSTEM-FLASH-ARGS`
- `SRC-DOSBOX-SERIAL-CONFIG`
- `SRC-LOCAL-ESPNOW-MULTIPEER-DASHBOARD-2026-05-23`
- `SRC-LOCAL-ESPNOW-LIVE-GATE-TOOLING-2026-05-23`

## Verified Facts

- ESP-NOW encrypted unicast requires paired-device LMK handling; encrypted
  multicast is not supported by the cited ESP-IDF ESP-NOW guide.
- ESP-NOW send status is MAC-layer status only; application-level ACK,
  timeout/retry, sequence-number, and duplicate-drop behavior remain required
  for BBS custody proof.
- esptool `read-flash 0 ALL` is the source-backed full-flash backup command
  shape used by the prepare gate.
- esptool `write-flash` performs write verification, while optional
  `verify-flash` must use matching flash mode, size, and frequency arguments
  when checking default boot images.
- ESP-IDF build outputs include `flash_project_args` and `flasher_args.json`;
  the live gate captures both and hashes the referenced binaries before any
  flash action.
- DOSBox serial documentation supports `nullmodem` as a serial mode, but the
  accepted Win3.1/DOSBox-X/Pi bridge path still depends on local runtime proof.

## Tooling Added

- `scripts/live_bench_preflight.py` now gates exactly three Windows CP210x
  peers on `COM4`, `COM5`, and `COM6`, derives `/dev/ttyS4` through
  `/dev/ttyS6`, runs read-only esptool identity commands, checks duplicate
  MACs, and maps `peer01` through `peer03` by port order only after pass.
- The preflight now targets `dospi@172.16.0.2`, checks the expected Pi host
  fingerprints, hostname, model, serial, root filesystem, `eth0`
  `172.16.0.2/24`, stale bridge/DOSBox/modal processes, stale listeners on
  `31331`, `31332`, and `8080`, and Pi `/dev/ttyUSB0` coordinator identity.
- `scripts/espnow_bbs_live_gate.py prepare` requires
  `--confirm-read-flash-backups`, consumes a passing preflight JSON, generates
  ignored live config under DOS-C `secrets/espnow-bbs/live-<timestamp>/`, runs
  full-flash backups, builds coordinator and peer images with ignored overrides,
  hashes backups/build outputs, and writes a manifest with recovery commands.
- `scripts/espnow_bbs_live_gate.py flash` requires `--confirm-write-flash`,
  refuses changed preflight/build/backup hashes or identity mismatches, uses
  flash order `coordinator`, `peer01`, `peer02`, `peer03`, rejects
  `--trust-flash-content`, erase, and `--force`, and records write/optional
  verify output.

## Unknowns

- Fresh same-session COM4/COM5/COM6 identities have not been captured by this
  task.
- No new `read-flash` backups, live config directory, live builds, flashing, or
  three-peer ESP-NOW radio acceptance were run by this task.
- Physical USB-only/no-load/no-relay/XBee/TFT/MicroSD state still requires
  same-session human or bench evidence before any live write.

## Stop Gate

Do not run `espnow_bbs_live_gate.py flash` until preflight, backup, build hash,
manifest, recovery, and physical bench-state evidence all pass in the same live
session.
