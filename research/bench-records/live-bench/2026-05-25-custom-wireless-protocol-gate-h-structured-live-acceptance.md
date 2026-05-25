# Custom Wireless Protocol Gate H Structured Live Acceptance - 2026-05-25

## Summary

Gate H live acceptance was rerun with fresh same-session authorization and the
structured bridge transcript enabled. The DOS-C vision gate and ESP32
completion gate both passed from `bridge-transcript.jsonl`.

Accepted path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

Gate G live export was not opened during this Gate H proof. At that time,
`ADR-0005` remained proposed, so live analytics export was disabled.

## Verified Facts

- Same-session authorization for live Gate H was present on 2026-05-25.
- Same-session authorization for Gate G did not accept `ADR-0005` during this
  Gate H proof; no live export surface, export artifact, bridge export request,
  Win31 export control, or firmware export ABI was added.
- Fresh ready preflight:
  `research/bench-records/live-bench/espnow-bbs-gate-h-structured-live-preflight-20260525T155413Z.json`
  reported `ok:true`.
- Post-run preflight:
  `research/bench-records/live-bench/espnow-bbs-gate-h-structured-live-postrun-preflight-20260525T160625Z.json`
  reported `ok:true`.
- The preflights verified Pi host `192.168.137.105`, coordinator
  `/dev/ttyUSB0` MAC `78:e3:6d:10:4d:6c`, and current accepted peer remap:
  `COM9`/`COM6`/`COM7` for `peer01`/`peer02`/`peer03`.
- The Pi bridge script was updated from the paired DOS-C structured transcript
  commit so `--audit-transcript` was available. The prior Pi copy was backed up
  as:
  `/home/dospi/dos-c/software/espnow-bbs-bridge/espnow_bbs_bridge.py.pre-structured-20260525T155838Z`.
- Pi proof directory:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-25-gate-h-structured-live/gate-h-structured-live-20260525T155900Z/`.
- DOS-C ignored local proof copy:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-25-gate-h-structured-live/gate-h-structured-live-20260525T155900Z/`.
- ESP32 ignored local proof copy:
  `research/bench-records/live-bench/gate-h-structured-live-20260525T155900Z/`.
- The JSONL transcript included one telemetry refresh before actions, BBS post,
  pull, search, ack, download queue, OTAP intent, and a final telemetry
  refresh after actions.
- `summary.txt` recorded one posted and acked message, one queued download,
  three events, and four peer rows with three `espnow-enc` peers.
- Cleanup proof showed no DOSBox-X process, no modal/warning process, no bridge
  process, and no listeners on `31331`, `31332`, or `8080`.
- DOS-C `vision-gate.json` reported `status: pass`.
- ESP32 `esp32-completion.json` reported `status: pass`.

## Assumptions

- No prepare or flash was required for this rerun because no runtime firmware
  change occurred after the accepted 2026-05-23 manifest/flash evidence.
- The 2026-05-23 manifest and flash evidence remain the appropriate paired
  completion inputs for the unchanged live firmware.

## Unknowns

- Firmware ABI remains unresolved.
- Gate G live export remained unresolved during this Gate H proof until
  `ADR-0005` accepted retention, privacy/redaction, format, storage, access,
  and cleanup policy. It was later opened only for local-admin redacted JSON by
  task 0051.
- Physical wiring beyond the USB-only/no-load live-gate boundary remains
  unproven.

## Validation

- DOS-C vision gate:
  `python3 scripts/win31_dashboard_vision_gate.py --screenshot-dir <packet> --bridge-transcript <packet>/bridge-transcript.jsonl --cleanup-proof <packet>/cleanup.txt --out <packet>/vision-gate.json`
  reported `status: pass`.
- ESP32 completion gate:
  `python3 scripts/espnow_bbs_live_gate.py complete --manifest /mnt/h/dos-c/secrets/espnow-bbs/live-20260523T215621Z/manifest.json --flash-evidence /mnt/h/dos-c/secrets/espnow-bbs/live-20260523T215621Z/flash-evidence-20260523T222853Z.json --bridge-transcript <packet>/bridge-transcript.jsonl --cleanup-proof <packet>/cleanup.txt --vision-gate <packet>/vision-gate.json --out <packet>/esp32-completion.json`
  reported `status: pass`.
- Post-run preflight reported `ok:true` with no failures.

## Result

Gate H structured live acceptance passed. The structured transcript removed the
old manual-review transcript caveat for this run.
