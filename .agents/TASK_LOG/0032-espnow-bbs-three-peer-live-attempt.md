# Task 0032: ESP-NOW BBS Three-Peer Live Attempt

Status: completed after backup-blocker investigation and corrected proof

Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Run the full live completion path for the ESP-NOW BBS three-peer bench after a
fresh read-only preflight, investigate any backup/manifest/flash blocker, and
record proof or a blocker.

## Scope

Included:

- Fresh read-only preflight against `COM4`, `COM5`, `COM6`,
  `dospi@192.168.137.93`, and coordinator `/dev/ttyUSB0`.
- Gated `prepare` with `--confirm-read-flash-backups`.
- Coordinator and peer full-flash backups before write.
- Manifest review for device identity, backup hashes, build artifacts,
  recovery commands, forbidden flash arguments, and flash order.
- Gated `flash` with `--confirm-write-flash`.
- Bridge protocol proof over the accepted Win31/DOSBox-X serial-nullmodem path.
- Windows 3.1 OPCON dashboard, peer/network, and Program Manager evidence.
- Cleanup checks for DOSBox-X, modal, bridge, and listeners.

Excluded:

- Relay, XBee, TFT, MicroSD, load, mains, PCAP, packet-driver work, BLE,
  ESP-WIFI-MESH, router admin, erase, monitor, or external wiring work.

## Verified Facts

Source ID: `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`.

- The first same-day attempt stopped before any valid backup hash or manifest:
  Pi Debian `esptool --no-stub --port /dev/ttyUSB0 read_flash 0 ALL ...`
  reached about 50% and returned a CRC/checksum error.
- The backup failure was isolated to the Pi esptool path. The corrected gate
  prefers the proven Pi esptool venv at
  `/home/dospi/dos-c/artifacts/runtime/esptool-venv-espnow-encrypted/bin/esptool.py`
  for coordinator backup/flash, and only falls back to Debian esptool with
  `--no-stub`.
- Peer backup and flash arguments now translate WSL `/mnt/h/...` artifact paths
  to Windows `H:\...` paths for Windows-hosted `esptool.exe`.
- ESP-IDF builds now invoke the activated `$IDF_PATH/tools/idf.py` through the
  activated Python environment when `idf.py` is available only as a shell
  function.
- Each role now builds with an isolated private `SDKCONFIG` under the ignored
  live directory. The corrected manifest used distinct peer IDs and MACs for
  `peer01`, `peer02`, and `peer03`.
- Corrected fresh preflight
  `research/bench-records/live-bench/espnow-bbs-live-preflight-20260523T215548Z.json`
  reported `ok: true` with no failures.
- Corrected peer identities:
  `COM4=peer01` MAC `94:b9:7e:da:17:d0`,
  `COM5=peer02` MAC `78:e3:6d:0a:90:14`,
  `COM6=peer03` MAC `94:b9:7e:da:9a:50`.
- Corrected coordinator identity:
  `dospi@192.168.137.93:/dev/ttyUSB0` MAC `78:e3:6d:10:4d:6c`,
  ESP32-D0WDQ6, 4 MB flash.
- Corrected prepare produced private manifest
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260523T215621Z/manifest.json` with
  four 4,194,304-byte full-flash backups, build hashes, recovery commands, no
  forbidden flash arguments, and flash order
  `coordinator`, `peer01`, `peer02`, `peer03`.
- Corrected flash produced private evidence
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260523T215621Z/flash-evidence-20260523T222853Z.json`
  with `ok: true`; all four roles reported `writeFlash.returncode=0` and
  `verifyFlash.returncode=0`.
- Pi bridge protocol transcript
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-23-espnow-bbs-three-peer-live/three-peer-live-final-20260523T223453Z/bridge-json-transcript.json`
  exercised `hello`, `state_get`, `peer_list`, `diag_get`, `fw_inventory`,
  `msg_post`, `msg_pull`, `msg_search`, and `msg_ack` over
  `serial-nullmodem`.
- The final transcript kept each response under the 512-byte line limit,
  reported three peers with `espnow-enc`, and showed RX/TX/ACK counters moving
  from `126/126/126` to `129/129/129`.
- Runtime screenshots were captured on the Pi for OPCON dashboard, peers,
  network, attempted message/firmware/diagnostic/safety views, and Program
  Manager helper evidence. The bridge transcript is the authoritative evidence
  for message, firmware inventory, and diagnostic request behavior.
- Final cleanup proof on the Pi showed no `dosbox-x`, modal/`zenity`, bridge
  process, or `31331`/`31332`/`8080` listener remaining.

## Assumptions

- The physical USB-only/no-load/no-relay/no-XBee/no-TFT/no-MicroSD boundary is
  from the user-provided execution plan for this same bench session. The
  preflight script cannot independently prove external wiring state.

## Unknowns

- The first coordinator readback CRC/checksum failure is not proven to be a
  cable, power, baud, or timing fault. The resolved path is the known-good Pi
  esptool venv/stub runtime, not a physical-cause diagnosis.
- OPCON later-tab screenshots may be duplicate captures because DOSBox-X mouse
  capture made some tab switches unreliable; the JSON transcript proves the
  corresponding bridge protocol behavior.
- Chunked message delivery, provisioning UX, BLE, ESP-WIFI-MESH, and any
  physical wiring beyond USB-only remain separate future work.

## Validation

- `python3 -m py_compile scripts/espnow_bbs_live_gate.py tests/live_bench/test_espnow_bbs_live_gate.py`
- `python3 tests/live_bench/test_espnow_bbs_live_gate.py`
- `python3 tests/live_bench/test_multipeer_preflight.py`
- DOS-C bridge validation recorded in the paired DOS-C task:
  `python3 tests/espnow_bbs_bridge/test_bridge_protocol.py` and
  `python3 tests/espnow_bbs_bridge/test_coordinator_protocol.py`.

## Handoff

Use [../handoffs/0022-espnow-bbs-three-peer-live-backup-blocker.md](../handoffs/0022-espnow-bbs-three-peer-live-backup-blocker.md)
for the closed blocker and remaining non-live-completion boundaries.
