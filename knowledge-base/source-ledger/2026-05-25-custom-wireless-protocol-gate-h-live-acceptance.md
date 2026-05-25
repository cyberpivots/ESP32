# Custom Wireless Protocol Gate H Live Acceptance Ledger - 2026-05-25

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-ESPNOW-CUSTOM-WIRELESS-PROTOCOL-GATE-H-LIVE-ACCEPTANCE-2026-05-25`

## Scope

Authorized Gate H live acceptance after the Pi/router path was restored and
the Pi received a new Windows ICS lease at `192.168.137.105`.

Accepted path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

No prepare, flash, erase, monitor, PCAP, router/admin mutation, BLE,
ESP-WIFI-MESH live action, relay, XBee, TFT, MicroSD, load, mains, or
serial-write expansion was run.

## Evidence

- Preflight host allow-list update:
  `scripts/live_bench_preflight.py`.
- Preflight host profile test:
  `tests/live_bench/test_multipeer_preflight.py`.
- Ignored ready preflight:
  `research/bench-records/live-bench/espnow-bbs-gate-h-ready-preflight-20260525T141424Z.json`.
- Ignored post-run preflight:
  `research/bench-records/live-bench/espnow-bbs-gate-h-postrun-preflight-20260525T143511Z.json`.
- Pi proof directory:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-25-gate-h-live/gate-h-live-postack-20260525T142504Z/`.
- Ignored local evidence copy:
  `research/bench-records/live-bench/gate-h-live-postack-20260525T142504Z/`.
- Tracked bench record:
  `research/bench-records/live-bench/2026-05-25-custom-wireless-protocol-gate-h-live-acceptance.md`.
- Task record:
  `.agents/TASK_LOG/0047-custom-wireless-protocol-gate-h-live-acceptance.md`.
- Handoff:
  `.agents/handoffs/0036-custom-wireless-protocol-gate-h-live-acceptance-to-qa.md`.

## Verified Facts

- `192.168.137.105` exposed the expected Pi host keys and passed the same Pi
  identity profile used by prior live gates.
- Ready preflight reported `ok:true`, with coordinator MAC
  `78:e3:6d:10:4d:6c` on Pi `/dev/ttyUSB0` and accepted peer MAC remap:
  `COM9` = `peer01`, `COM6` = `peer02`, `COM7` = `peer03`.
- Post-run preflight also reported `ok:true` after the live proof cleanup.
- The bridge listener used `serial-nullmodem` on `127.0.0.1:31332` and the
  physical serial coordinator backend in `--read-only` mode.
- The Win31 OPCON request transcript included the required status, BBS,
  download, and OTAP-intent request set, including `msg_post`, `msg_search`,
  `msg_ack`, `download_queue`, and `otap_intent`.
- The proof spool recorded one posted and acked message, one download request,
  and four peer rows with three `espnow-enc` peers.
- Cleanup proof after the corrected run showed no DOSBox-X process, modal,
  bridge process, or relevant listener.
- The screenshot/OCR gate found all expected views and disabled unsafe
  controls, but returned `needs_manual_review` because this historical packet
  used the older transcript summary shape.

## Assumptions

- The `.105` lease is the same bench Pi behind the same router path because
  SSH host keys, Pi identity checks, and `/dev/ttyUSB0` coordinator identity
  matched.
- Since Gates E-G were simulator/documentation/build-only for runtime
  behavior, no flash gate was needed for this live run.

## Unknowns

- Future deterministic screenshot acceptance needs a fresh live packet captured
  with the structured bridge JSONL transcript so serial-error and counter
  triples are machine-readable.
- Analytics retention/export/privacy remains unresolved and simulator-only.

## Result

Gate H is accepted for the 2026-05-25 authorized live run. The prior blocked
attempt and troubleshooting records remain as history; this ledger supersedes
their blocked state for the current restored Pi/router path.
