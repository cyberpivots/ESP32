# ESP-NOW BBS Three-Peer Live Attempt And Resolution Source Ledger

Source ID: `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`

## Evidence

- Initial ignored preflight JSON:
  `research/bench-records/live-bench/espnow-bbs-live-preflight-20260523T200026Z.json`
- Corrected ignored preflight JSON:
  `research/bench-records/live-bench/espnow-bbs-live-preflight-20260523T215548Z.json`
- Tracked bench summary:
  `research/bench-records/live-bench/2026-05-23-espnow-bbs-three-peer-live-attempt.md`
- Initial ignored partial live directories from failed prepare attempts:
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260523T200125Z/`,
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260523T200209Z/`, and
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260523T200237Z/`
- Corrected private manifest and backups:
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260523T215621Z/manifest.json`
- Corrected private flash evidence:
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260523T215621Z/flash-evidence-20260523T222853Z.json`
- Pi runtime proof directory:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-23-espnow-bbs-three-peer-live/three-peer-live-final-20260523T223453Z/`

## Supported Facts

- The initial three-peer live attempt stopped at coordinator full-flash backup
  because Pi Debian `esptool --no-stub --port /dev/ttyUSB0 read_flash 0 ALL`
  failed around 50% with a CRC/checksum error before any valid backup, build
  manifest, flash evidence, bridge transcript, Win31 screenshot, or three-peer
  radio acceptance was produced.
- The corrected gate uses the proven Pi esptool venv/stub runtime for
  coordinator backup and flash, translates Windows peer artifact paths for
  Windows-hosted `esptool.exe`, resolves activated ESP-IDF `idf.py` paths, and
  isolates per-role private `SDKCONFIG` files.
- The corrected fresh preflight passed with peers
  `COM4=peer01` MAC `94:b9:7e:da:17:d0`,
  `COM5=peer02` MAC `78:e3:6d:0a:90:14`,
  `COM6=peer03` MAC `94:b9:7e:da:9a:50`, and coordinator
  `/dev/ttyUSB0` MAC `78:e3:6d:10:4d:6c`.
- The corrected manifest records four 4,194,304-byte full-flash backups,
  build artifacts and hashes, recovery commands, and flash order
  `coordinator`, `peer01`, `peer02`, `peer03`.
- The corrected flash evidence reports `ok: true` with `writeFlash` and
  `verifyFlash` return code `0` for all four roles.
- The final Pi bridge transcript exercised `hello`, `state_get`, `peer_list`,
  `diag_get`, `fw_inventory`, `msg_post`, `msg_pull`, `msg_search`, and
  `msg_ack` over `serial-nullmodem`, kept responses under the 512-byte line
  limit, reported three `espnow-enc` peers, and showed RX/TX/ACK counters
  moving from `126/126/126` to `129/129/129`.
- Runtime evidence includes OPCON dashboard, peers, network, attempted
  message/firmware/diagnostic/safety captures, Program Manager helper capture,
  and cleanup proof showing no DOSBox-X, modal/`zenity`, bridge process, or
  `31331`/`31332`/`8080` listener remaining.

## Boundary

This ledger proves the USB-only three-peer encrypted ESP-NOW BBS bench path for
backup, build, flash, bridge protocol, and dashboard runtime evidence. It does
not prove relay, XBee, TFT, MicroSD, load, mains, PCAP, packet-driver, BLE,
ESP-WIFI-MESH, erase, monitor, provisioning UX, chunked delivery, or physical
wiring beyond the USB-only boundary stated in the user-provided plan.
