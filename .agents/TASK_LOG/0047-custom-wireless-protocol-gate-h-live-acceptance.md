# Task Log 0047 - Custom Wireless Protocol Gate H Live Acceptance

## Task

- ID: 0047-custom-wireless-protocol-gate-h-live-acceptance
- Owner role: Communications, QA, Hardware
- Status: accepted with visual-gate manual-review caveat
- Created: 2026-05-25
- Updated: 2026-05-25
- Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Perform authorized Gate H live acceptance on the accepted path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Verified Facts

- Same-session live authorization was present.
- The user restored physical connectivity by reconnecting Pi Ethernet and
  power-cycling the router.
- Windows ICS exposed the Pi/router path at `192.168.137.105`.
- Fresh ready preflight
  `research/bench-records/live-bench/espnow-bbs-gate-h-ready-preflight-20260525T141424Z.json`
  reported `ok:true`.
- Post-run preflight
  `research/bench-records/live-bench/espnow-bbs-gate-h-postrun-preflight-20260525T143511Z.json`
  also reported `ok:true`.
- The ready preflight verified:
  - Pi identity/profile and no stale listeners/processes.
  - Coordinator `/dev/ttyUSB0` MAC `78:e3:6d:10:4d:6c`.
  - Peer remap `COM9`/`COM6`/`COM7` to accepted peer MACs.
- No prepare or flash was run because Gates E-G did not add runtime firmware
  changes requiring reflash.
- The live proof directory is:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-25-gate-h-live/gate-h-live-postack-20260525T142504Z/`.
- Ignored local evidence copy:
  `research/bench-records/live-bench/gate-h-live-postack-20260525T142504Z/`.
- The bridge transcript included:
  `hello`, `state_get`, `peer_list`, `diag_get`, `fw_inventory`,
  `coordinator_state`, `msg_post`, `msg_pull`, `msg_search`, `msg_ack`,
  `download_list`, `download_queue`, `download_status`, `otap_status`, and
  `otap_intent`.
- The proof spool recorded three `espnow-enc` peer rows plus coordinator.
- Cleanup proof showed no remaining DOSBox-X process, `zenity`/modal, bridge
  process, or listeners on `31331`, `31332`, or `8080`.

## Assumptions

- `192.168.137.105` is an ICS DHCP reassignment for the same Pi/router path,
  not a new host, because the Pi identity and host keys matched.

## Unknowns

- The copied-evidence vision gate currently returns `needs_manual_review`
  because the bridge summary does not include full serial-error and
  moving-counter triples, even though screenshots and OCR identify the expected
  views and disabled unsafe controls.
- Gate G analytics retention/export/privacy policy remains unresolved.

## Result

Gate H live acceptance passed for the authorized 2026-05-25 run. The bridge
transcript and spool summary are authoritative; screenshots remain secondary
manual-review corroboration.

## Handoff

Continue with
[../handoffs/0036-custom-wireless-protocol-gate-h-live-acceptance-to-qa.md](../handoffs/0036-custom-wireless-protocol-gate-h-live-acceptance-to-qa.md).
