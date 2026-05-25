# Custom Wireless Protocol Gate H Live Acceptance - 2026-05-25

## Summary

Gate H live acceptance passed for the accepted serial-nullmodem path after the
Pi/router DHCP lease moved to `192.168.137.105` and fresh read-only preflight
passed. No prepare, flash, erase, monitor, PCAP, router/admin mutation, BLE,
mesh, relay, XBee, TFT, MicroSD, load, mains, or serial-write expansion was
run.

Accepted path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Verified Facts

- Same-session user authorization for live Gate H was present on 2026-05-25.
- The user reported the Pi and router powered and connected, reconnected the
  Pi Ethernet cord, and later power-cycled the router with WAN and LAN LEDs on.
- Windows HNetCfg Internet Connection Sharing was re-applied with `Wi-Fi` as
  public sharing type `0` and `Ethernet 3` as private sharing type `1`.
- The Pi/router DHCP path moved from the stale forwarded address
  `192.168.137.93` to `192.168.137.105`.
- `ssh-keyscan -T 5 192.168.137.105` returned the expected Pi host keys and
  TCP 22 was reachable from the Windows ICS network.
- `scripts/live_bench_preflight.py` now treats `192.168.137.105` as an
  accepted Pi access host for the same expected Pi identity profile.
- Fresh ready preflight:
  `research/bench-records/live-bench/espnow-bbs-gate-h-ready-preflight-20260525T141424Z.json`
  reported `ok:true` and no failures.
- Post-run read-only preflight:
  `research/bench-records/live-bench/espnow-bbs-gate-h-postrun-preflight-20260525T143511Z.json`
  also reported `ok:true` and no failures after cleanup.
- The ready preflight verified:
  - Pi hostname/model/serial/root/eth0 profile matched the live gate.
  - Pi stale listener/process checks were clear after removing an earlier
    stale DOSBox-X process.
  - Coordinator `/dev/ttyUSB0` identity matched MAC `78:e3:6d:10:4d:6c`.
  - Current peer remap matched accepted peer role MACs:
    `peer01` on `COM9` MAC `94:b9:7e:da:17:d0`,
    `peer02` on `COM6` MAC `78:e3:6d:0a:90:14`,
    `peer03` on `COM7` MAC `94:b9:7e:da:9a:50`.
- The accepted live proof ran on the Pi at:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-25-gate-h-live/gate-h-live-postack-20260525T142504Z/`.
- Ignored local evidence copy:
  `research/bench-records/live-bench/gate-h-live-postack-20260525T142504Z/`.
- The Pi bridge ran on `127.0.0.1:31332` with
  `--transport serial-nullmodem --coordinator-backend serial --device /dev/ttyUSB0 --allow-physical-serial --read-only`.
- The Win31 OPCON transcript over COM1 exercised:
  `hello`, `state_get`, `peer_list`, `diag_get`, `fw_inventory`,
  `coordinator_state`, `msg_post`, `msg_pull`, `msg_search`, `msg_ack`,
  `download_list`, `download_queue`, `download_status`, `otap_status`, and
  `otap_intent`.
- The proof spool contained one posted message and one acked message, one
  queued download request, three events, and four peer rows.
- The live peer rows were:
  - `coordinator-01` MAC `78:e3:6d:10:4d:6c`, role `coordinator`, link
    `serial-stub`
  - `peer01` MAC `94:b9:7e:da:17:d0`, role `peer`, link `espnow-enc`, RSSI
    `-37`
  - `peer02` MAC `78:e3:6d:0a:90:14`, role `peer`, link `espnow-enc`, RSSI
    `-32`
  - `peer03` MAC `94:b9:7e:da:9a:50`, role `peer`, link `espnow-enc`, RSSI
    `-47`
- Cleanup proof showed no remaining DOSBox-X process, warning modal/`zenity`,
  bridge process, or listeners on `31331`, `31332`, or `8080`.
- Copied screenshot/OCR review found all expected OPCON views and disabled
  unsafe controls, but the deterministic vision gate reported
  `needs_manual_review` because this historical packet used the older bridge
  summary shape.

## Assumptions

- The DHCP reassignment to `192.168.137.105` is a normal Windows ICS/router
  lease change, not a new device identity, because the expected Pi host keys,
  hostname/profile checks, and coordinator identity passed.
- Gates E through G did not introduce runtime firmware changes, so no
  prepare/flash step was required for this Gate H acceptance pass.

## Unknowns

- Future deterministic screenshot acceptance needs a fresh live packet captured
  with `bridge-transcript.jsonl` so full bridge response payloads,
  serial-error values, and counter triples are available to the machine gate.
- Analytics retention/export/privacy policy remains unresolved; Gate G
  analytics stays simulator-only.

## Result

Gate H live acceptance is accepted for the authorized 2026-05-25 run on the
accepted serial-nullmodem path. The bridge transcript and Pi spool summary are
authoritative for behavior; screenshots are secondary corroboration with a
manual-review OCR caveat.
