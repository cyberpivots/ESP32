# Handoff 0022: ESP-NOW BBS Three-Peer Backup Blocker

Task: [../TASK_LOG/0032-espnow-bbs-three-peer-live-attempt.md](../TASK_LOG/0032-espnow-bbs-three-peer-live-attempt.md)

Status: closed by corrected 2026-05-23 live proof

## Resolution

- The original blocker was the coordinator full-flash backup using Pi Debian
  `esptool --no-stub`, which failed around 50% with a CRC/checksum error before
  any valid backup, manifest, or flash.
- The gate now prefers the proven Pi esptool venv/stub runtime for coordinator
  backup and flash, translates Windows peer artifact paths for `esptool.exe`,
  resolves activated ESP-IDF `idf.py` paths, and isolates per-role
  `SDKCONFIG` files.
- Corrected preflight, prepare, backup, build, manifest, flash, bridge
  transcript, Win31 screenshot capture, Program Manager helper proof, and
  cleanup all ran on 2026-05-23.

## Current Passing Surface

- Corrected preflight:
  `research/bench-records/live-bench/espnow-bbs-live-preflight-20260523T215548Z.json`.
- Private manifest:
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260523T215621Z/manifest.json`.
- Private flash evidence:
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260523T215621Z/flash-evidence-20260523T222853Z.json`.
- Pi runtime proof directory:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-23-espnow-bbs-three-peer-live/three-peer-live-final-20260523T223453Z/`.
- Final bridge transcript shows `peer01`, `peer02`, and `peer03` as
  `espnow-enc`, response frames under the 512-byte line limit, and RX/TX/ACK
  counters moving from `126/126/126` to `129/129/129`.
- Final cleanup shows no DOSBox-X, modal/`zenity`, bridge process, or
  `31331`/`31332`/`8080` listener.

## Remaining Boundaries

- Do not infer any relay, XBee, TFT, MicroSD, load, mains, PCAP, router admin,
  packet-driver, BLE, ESP-WIFI-MESH, erase, or monitor acceptance from this
  proof.
- Treat chunked message delivery, provisioning UX, mobile/BLE client-node work,
  and any physical wiring beyond USB-only as future separately gated work.
