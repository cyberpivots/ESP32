# Custom Wireless Protocol Gate H Structured Live Acceptance Ledger - 2026-05-25

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25`

## Scope

Authorized Gate H live rerun using the accepted serial-nullmodem path and the
structured bridge JSONL transcript:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

Gate G live analytics export remains disabled because `ADR-0005` is proposed,
not accepted.

## Evidence

- Ignored ready preflight:
  `research/bench-records/live-bench/espnow-bbs-gate-h-structured-live-preflight-20260525T155413Z.json`.
- Ignored post-run preflight:
  `research/bench-records/live-bench/espnow-bbs-gate-h-structured-live-postrun-preflight-20260525T160625Z.json`.
- Pi proof directory:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-25-gate-h-structured-live/gate-h-structured-live-20260525T155900Z/`.
- DOS-C ignored local proof copy:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-25-gate-h-structured-live/gate-h-structured-live-20260525T155900Z/`.
- ESP32 ignored local proof copy:
  `research/bench-records/live-bench/gate-h-structured-live-20260525T155900Z/`.
- Tracked bench record:
  `research/bench-records/live-bench/2026-05-25-custom-wireless-protocol-gate-h-structured-live-acceptance.md`.
- Task record:
  `.agents/TASK_LOG/0050-custom-wireless-protocol-gate-h-structured-live-acceptance.md`.
- Handoff:
  `.agents/handoffs/0039-custom-wireless-protocol-gate-h-structured-live-acceptance-to-qa.md`.

## Verified Facts

- Fresh ready and post-run preflights reported `ok:true` with the expected Pi,
  coordinator, and peer identities.
- The Pi bridge ran with `--audit-transcript <proof-dir>/bridge-transcript.jsonl`,
  `--coordinator-backend serial`, `--device /dev/ttyUSB0`,
  `--allow-physical-serial`, and `--read-only`.
- The JSONL transcript captured startup telemetry, a pre-action telemetry
  refresh, `msg_post`, `msg_pull`, `msg_search`, `msg_ack`,
  `download_queue`, `otap_intent`, and a final telemetry refresh.
- Transcript audit found zero serial errors, three `espnow-enc` peers, and
  moving RX/TX/ACK triples.
- Cleanup proof found no DOSBox-X process, modal/warning process, bridge
  process, or relevant listener.
- DOS-C vision gate reported `status: pass`.
- ESP32 completion gate reported `status: pass` using the unchanged accepted
  2026-05-23 manifest and flash evidence.
- No prepare, flash, erase, monitor, PCAP, router/admin mutation, BLE,
  ESP-WIFI-MESH live action, relay, XBee, TFT, MicroSD, load, mains,
  serial-write expansion, or Gate G export action was run.

## Assumptions

- The existing 2026-05-23 firmware manifest and flash evidence remain valid
  for completion auditing because this structured rerun did not change
  firmware runtime behavior.

## Unknowns

- Firmware ABI remains unresolved.
- Gate G live export policy remains unresolved until `ADR-0005` is accepted.
- Physical wiring outside the USB-only/no-load live-gate boundary remains
  unproven.

## Result

Gate H structured live acceptance passed without the prior manual-review
transcript caveat.
