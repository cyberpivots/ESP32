# ESP-NOW BBS Three-Peer Live Attempt

Date: 2026-05-23

Source ID: `SRC-LOCAL-ESPNOW-THREE-PEER-LIVE-ATTEMPT-2026-05-23`

## Verified Facts

- Fresh read-only preflight passed from `/mnt/h/ESP32`:
  `python3 scripts/live_bench_preflight.py --pi-host 192.168.137.93 --summary --out research/bench-records/live-bench/espnow-bbs-live-preflight-20260523T200026Z.json`.
- Preflight summary reported `ok: true` and `readiness: ready_for_prepare`.
- Windows peers mapped by the gate as:
  `COM4=peer01` MAC `94:b9:7e:da:17:d0`,
  `COM5=peer02` MAC `78:e3:6d:0a:90:14`,
  `COM6=peer03` MAC `94:b9:7e:da:9a:50`.
- Pi coordinator identity passed on `dospi@192.168.137.93:/dev/ttyUSB0` with
  MAC `78:e3:6d:10:4d:6c`, ESP32-D0WDQ6, and 4 MB flash.
- The first `prepare` run stopped before backup because the gate wrote
  `known_hosts` before invoking the DOS-C live-config generator, making the
  generated live directory non-empty.
- The second `prepare` run stopped before backup because Pi `esptool` 4.7.0
  accepts `read_flash`, not `read-flash`.
- The third `prepare` run generated ignored live config under
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260523T200237Z/` and then stopped
  during the coordinator full-flash backup. Pi `esptool --no-stub --port
  /dev/ttyUSB0 read_flash 0 ALL ...` reached about 50% of the 4 MB read and
  failed with `A fatal error occurred: Failed to read flash block (result was
  01090000: CRC or checksum was invalid)`.
- No peer backup, build manifest, flash, bridge launch, Win31 OPCON proof, or
  ESP-NOW three-peer radio acceptance ran after the failed coordinator backup.
- Cleanup checks found no local or Pi `espnow_bbs_bridge`, `dosbox-x`,
  `zenity`, `yad`, `esp32_gateway_sim`, `esptool`, `read_flash`, or `ttyUSB0`
  process after cleanup, and no `31331`, `31332`, or `8080` listener on the
  checked local/Pi paths.

## Assumptions

- The physical USB-only/no-load/no-relay/no-XBee/no-TFT/no-MicroSD boundary is
  taken from the user-provided execution plan for this task. The preflight
  script cannot independently prove physical wiring state.

## Unknowns

- Whether the coordinator readback CRC failure is transient, cable/power
  related, baud/timing related, or caused by Pi-side serial behavior.
- Whether a slower or chunked coordinator backup strategy would pass. No retry
  or workaround was run after the backup gate failed.
- Three-peer encrypted radio behavior remains unproven.

## Closed Lanes

No relay, XBee, TFT, MicroSD, load, mains, PCAP, packet-driver, router-admin,
BLE, ESP-WIFI-MESH, erase, monitor, bridge, DOSBox-X, or Win31 dashboard
mutation was run by this attempt.
