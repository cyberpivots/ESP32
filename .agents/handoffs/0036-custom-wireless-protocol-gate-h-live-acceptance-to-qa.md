# Handoff 0036 - Custom Wireless Protocol Gate H Live Acceptance To QA

Task:
[../TASK_LOG/0047-custom-wireless-protocol-gate-h-live-acceptance.md](../TASK_LOG/0047-custom-wireless-protocol-gate-h-live-acceptance.md)

## Status

Gate H live acceptance passed on 2026-05-25 for the accepted
serial-nullmodem path after Pi/router reachability was restored at
`192.168.137.105`.

## Verified Facts

- Ready preflight:
  `research/bench-records/live-bench/espnow-bbs-gate-h-ready-preflight-20260525T141424Z.json`.
- Post-run preflight:
  `research/bench-records/live-bench/espnow-bbs-gate-h-postrun-preflight-20260525T143511Z.json`.
- Pi proof directory:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-25-gate-h-live/gate-h-live-postack-20260525T142504Z/`.
- Ignored local evidence copy:
  `research/bench-records/live-bench/gate-h-live-postack-20260525T142504Z/`.
- Transcript request set included `msg_post`, `msg_search`, `msg_ack`,
  `download_queue`, and `otap_intent` in addition to the status and inventory
  requests.
- Spool summary recorded three `espnow-enc` peers:
  `peer01`, `peer02`, and `peer03`.
- Cleanup proof showed no DOSBox-X process, modal/`zenity`, bridge process, or
  relevant listener.

## QA Notes

- For this historical packet, treat `bridge.log` plus `summary.txt` as the
  archived behavior evidence. For future reruns, feed
  `<proof-dir>/bridge-transcript.jsonl` to the DOS-C vision gate and ESP32
  completion gate.
- Treat screenshots as secondary corroboration. The deterministic vision gate
  found all expected views and disabled unsafe controls but returned
  `needs_manual_review` because the archived packet did not carry full
  serial-error/counter triples.
- Future live runs should start the bridge with
  `--audit-transcript <proof-dir>/bridge-transcript.jsonl` and collect one
  telemetry refresh cycle before BBS/download/OTAP actions plus one after.

## Closed Gates

Keep PCAP, router/admin mutation, BLE, ESP-WIFI-MESH live action, relay, XBee,
TFT, MicroSD, load, mains, erase, monitor, and serial-write expansion closed.
