# ESP-NOW BBS Three-Peer Live Attempt And Resolution

Date: 2026-05-23

Source ID: `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`

## Verified Facts

- Initial fresh read-only preflight passed from `/mnt/h/ESP32`:
  `python3 scripts/live_bench_preflight.py --pi-host 192.168.137.93 --summary --out research/bench-records/live-bench/espnow-bbs-live-preflight-20260523T200026Z.json`.
- The initial `prepare` path reached coordinator backup after two narrow gate
  fixes, then failed before any valid backup hash existed. Pi
  `esptool --no-stub --port /dev/ttyUSB0 read_flash 0 ALL ...` reached about
  50% of the 4 MB read and failed with a CRC/checksum error.
- The coordinator backup blocker was resolved by selecting the proven Pi
  esptool venv/stub runtime for coordinator backup and flash instead of
  forcing Debian esptool `--no-stub`.
- Additional live-gate fixes resolved Windows peer artifact path translation,
  ESP-IDF `idf.py` shell-function resolution, and per-role `SDKCONFIG`
  isolation.
- Corrected fresh read-only preflight passed from `/mnt/h/ESP32`:
  `research/bench-records/live-bench/espnow-bbs-live-preflight-20260523T215548Z.json`
  reported `ok: true` with no failures.
- Corrected Windows peers mapped as:
  `COM4=peer01` MAC `94:b9:7e:da:17:d0`,
  `COM5=peer02` MAC `78:e3:6d:0a:90:14`,
  `COM6=peer03` MAC `94:b9:7e:da:9a:50`.
- Corrected Pi coordinator identity passed on
  `dospi@192.168.137.93:/dev/ttyUSB0` with MAC `78:e3:6d:10:4d:6c`,
  ESP32-D0WDQ6, and 4 MB flash.
- Corrected prepare produced private manifest
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260523T215621Z/manifest.json` with
  four 4,194,304-byte full-flash backups, build hashes, recovery commands, and
  flash order `coordinator`, `peer01`, `peer02`, `peer03`.
- Private backup SHA-256 prefixes recorded in the manifest:
  coordinator `94bceaf611dfde8f`, peer01 `4394250b78783851`,
  peer02 `2dde7afe7cd8ee0b`, peer03 `a5e9aacd520f3ea2`.
- Manifest build config review showed peer-specific `SDKCONFIG` files:
  `peer01` maps to `94:b9:7e:da:17:d0`, `peer02` maps to
  `78:e3:6d:0a:90:14`, and `peer03` maps to `94:b9:7e:da:9a:50`.
- Corrected flash evidence
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260523T215621Z/flash-evidence-20260523T222853Z.json`
  reported `ok: true`, with write and verify return code `0` for
  coordinator, `peer01`, `peer02`, and `peer03`.
- DOS-C runtime was rebuilt and synced to the Pi, then the bridge was started
  on the accepted path:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge :31332 -> /dev/ttyUSB0 -> ESP32 coordinator`.
- Final Pi runtime proof directory:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-23-espnow-bbs-three-peer-live/three-peer-live-final-20260523T223453Z/`.
- Final bridge transcript exercised `hello`, `state_get`, `peer_list`,
  `diag_get`, `fw_inventory`, `msg_post`, `msg_pull`, `msg_search`, and
  `msg_ack`. Response sizes were under the 512-byte line limit.
- Final transcript reported `peer01`, `peer02`, and `peer03` with
  `espnow-enc`; RX/TX/ACK counters moved from `126/126/126` to
  `129/129/129`.
- OPCON dashboard, peers, network, attempted message/firmware/diagnostic/safety
  captures, and Program Manager helper capture were recorded in the Pi runtime
  proof directory. The bridge transcript is the authoritative proof for
  message, firmware inventory, and diagnostic request behavior.
- Cleanup checks found no Pi `dosbox-x`, modal/`zenity`, or
  `espnow_bbs_bridge.py` process after cleanup, and no `31331`, `31332`, or
  `8080` listener.

## Assumptions

- The physical USB-only/no-load/no-relay/no-XBee/no-TFT/no-MicroSD boundary is
  taken from the user-provided execution plan for this task. The preflight
  script cannot independently prove physical wiring state.

## Unknowns

- The initial coordinator readback CRC/checksum failure is not proven to be a
  cable, power, baud, timing, or Pi serial defect. The accepted resolution is
  the proven Pi esptool venv/stub runtime.
- Some later OPCON tab screenshots may be duplicate captures due DOSBox-X input
  capture; protocol proof covers the corresponding request/response behavior.
- Chunked delivery, provisioning UX, BLE, ESP-WIFI-MESH, and physical wiring
  beyond USB-only remain unproven.

## Closed Lanes

No relay, XBee, TFT, MicroSD, load, mains, PCAP, packet-driver, router-admin,
BLE, ESP-WIFI-MESH, erase, monitor, or non-USB physical wiring work was run by
this proof.
