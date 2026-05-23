# Handoff 0022: ESP-NOW BBS Three-Peer Backup Blocker

Task: [../TASK_LOG/0032-espnow-bbs-three-peer-live-attempt.md](../TASK_LOG/0032-espnow-bbs-three-peer-live-attempt.md)

## Continue With

- Preserve the accepted SSH-forwarded Pi access path `dospi@192.168.137.93`
  unless direct `172.16.0.2` routing is deliberately restored and reverified.
- Rerun fresh read-only preflight before any future backup or flash attempt.
- Investigate the coordinator full-flash backup failure before rerunning
  `prepare`. The failed command was Pi `esptool --no-stub --port /dev/ttyUSB0
  read_flash 0 ALL ...`, which stopped around 50% with CRC/checksum failure.
- Consider a source-backed, read-only backup retry plan before mutation, such
  as shorter read ranges, slower baud settings, cable/power inspection, or
  other esptool-supported readback options. Do not flash without a complete
  backup and manifest.

## Current Passing Surface

- Fresh preflight passed on 2026-05-23 with `ok: true` and
  `readiness: ready_for_prepare`.
- Peer map:
  `COM4=peer01` MAC `94:b9:7e:da:17:d0`,
  `COM5=peer02` MAC `78:e3:6d:0a:90:14`,
  `COM6=peer03` MAC `94:b9:7e:da:9a:50`.
- Coordinator map:
  `/dev/ttyUSB0` MAC `78:e3:6d:10:4d:6c`, ESP32-D0WDQ6, 4 MB flash.
- Live-gate tooling now generates config before writing `known_hosts`, and uses
  Pi-compatible `read_flash` for remote coordinator backup.

## Stop Gate

- No valid coordinator full-flash backup exists for the 2026-05-23 three-peer
  attempt.
- No complete manifest exists.
- Do not run `scripts/espnow_bbs_live_gate.py flash` until a future prepare run
  records complete backups, build hashes, recovery commands, and a reviewed
  manifest.

## Closed Lanes

No peer backup, build, flash, bridge launch, DOSBox-X launch, Win31 OPCON
proof, Program Manager proof, ESP-NOW three-peer radio acceptance, relay, XBee,
TFT, MicroSD, load, mains, PCAP, packet-driver work, BLE, ESP-WIFI-MESH, router
admin, erase, or monitor work was completed by this attempt.
