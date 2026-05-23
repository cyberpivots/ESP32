# Handoff 0019 - ESP-NOW BBS Live Gate To QA

## From

Tooling, Firmware, Communications

## To

QA, Firmware, Hardware

## Context

The tooling-first three-peer gate is implemented, but no fresh live preflight,
backup, flash, or Win3.1/Pi three-peer acceptance has been run by this task.

## Continue With

- Run `scripts/live_bench_preflight.py --out
  research/bench-records/live-bench/<fresh-name>.json` in the same session as
  any intended live write.
- Confirm the JSON reports `ok: true`, exactly `COM4`, `COM5`, and `COM6`
  CP210x peer identities, distinct peer MACs, Pi `eth0=172.16.0.2/24`, no
  stale DOSBox-X/bridge/modal/listeners, and distinct coordinator
  `/dev/ttyUSB0` identity.
- Confirm physical USB-only/no-load/no-relay/no-XBee/no-TFT/no-MicroSD state
  before backup or flash work.
- Run `scripts/espnow_bbs_live_gate.py prepare --preflight <json>
  --confirm-read-flash-backups` only after the preflight and physical state
  pass.
- Review the generated ignored DOS-C
  `secrets/espnow-bbs/live-<timestamp>/manifest.json` for backup hashes, build
  hashes, recovery commands, flash order, and forbidden argument absence.
- Run `scripts/espnow_bbs_live_gate.py flash --manifest <manifest>
  --confirm-write-flash` only when the manifest still matches current identity
  and the recovery path is acceptable.
- Capture Win3.1 OPCON proof for splash, Program Manager item, Message Board,
  three peers, `espnow-enc`, moving RX/TX/ACK counters, zero serial errors,
  disabled unsafe controls, successful post/pull/search/ack, and cleanup.

## Stop Gates

- Stop on missing/extra peer ports, duplicate peer MACs, unexpected chip/flash
  profile, Pi identity mismatch, stale listeners/processes, missing
  `/dev/ttyUSB0`, failed backup/hash capture, missing recovery path, or changed
  build hashes.
- Do not use `--trust-flash-content`, erase commands, or `--force`.
- Do not open relay, XBee, TFT, MicroSD, load, mains, PCAP, router-admin,
  packet-driver, or Windows COM proxy lanes from this handoff.
