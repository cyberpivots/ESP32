# Win31 Dashboard 1024x600 Gate H Live Proof - 2026-05-26

## Summary

The Win31 OPCON 1024x600 dashboard live proof completed on the accepted
serial-nullmodem path after fresh same-session preflight, backup, flash, live
capture, cleanup, DOS-C vision gate, ESP32 completion audit, and post-run
preflight.

Accepted path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Verified Facts

- The original authorized preflight packet
  `research/bench-records/live-bench/win31-dashboard-1024x600-gate-h-preflight-20260526T202729Z.json`
  existed before this execution.
- Fresh context preflight
  `research/bench-records/live-bench/win31-dashboard-1024x600-gate-h-preflight-20260526T214152Z.json`
  reported `ok:true`, `readiness:ready_for_prepare`, Pi
  `dospi@192.168.200.153`, coordinator `/dev/ttyUSB0` MAC
  `78:e3:6d:10:4d:6c`, and peer remap `peer01=COM6`,
  `peer02=COM10`, `peer03=COM12`.
- Prepare produced private manifest
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260526T211658Z-win31-dashboard-1024x600-gate-h/manifest.json`
  with full-flash backups for coordinator, `peer01`, `peer02`, and `peer03`.
- Flash evidence
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260526T211658Z-win31-dashboard-1024x600-gate-h/flash-evidence-20260526T221511Z.json`
  reported `ok:true`; all four write and verify steps returned `0`.
- Pi proof directory:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-1024x600-gate-h/gate-h-1024x600-20260526T211658Z/`.
- DOS-C ignored local proof copy:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-1024x600-gate-h/gate-h-1024x600-20260526T211658Z/`.
- The packet contains 18 planned screenshots from `00-launch` through
  `17-pre-cleanup`.
- The bridge ran with `--transport serial-nullmodem`,
  `--coordinator-backend serial`, `--device /dev/ttyUSB0`,
  `--allow-physical-serial`, `--read-only`, and
  `--audit-transcript <packet>/bridge-transcript.jsonl`.
- `summary.txt` records request counts for `hello`, `state_get`,
  `coordinator_state`, `peer_list`, `diag_get`, `fw_inventory`, `msg_post`,
  `msg_pull`, `msg_search`, `msg_ack`, `download_list`,
  `download_status`, `download_queue`, `otap_status`, and `otap_intent`.
- Transcript audit in `esp32-completion.json` reports peer IDs
  `peer01`, `peer02`, and `peer03`, 24 `espnow-enc` mentions, serial errors
  all `0`, and moving RX/TX/ACK triples `(164,164,164)`,
  `(394,394,394)`, and `(419,419,419)`.
- `summary.txt` records one posted message, one queued download, three events,
  four peer rows, and three `espnow-enc` peers.
- `cleanup.txt` reports no DOSBox-X process, no zenity modal/warning process,
  no bridge process, and no listeners on `31331`, `31332`, or `8080`.
- DOS-C `vision-gate.json` reported `status: pass`, `ok:true`, and no
  failures.
- ESP32 `esp32-completion.json` reported `status: pass`, `ok:true`, and no
  failures.
- Advisory legibility analysis reported 18 screens, mapped target views
  `10/10`, `visionGateStatus: pass`, median OCR confidence `51.25`, lowest
  OCR confidence `44.65`, and 2690 OCR words.
- The same advisory legibility analysis also reported lowest bottom and right
  margins of `0 px`, `console_fit_risk` on 18 screens,
  `log_region_overflow` on 18 screens, and `navigation_label_gap` on 8
  screens.
- Post-run preflight
  `research/bench-records/live-bench/win31-dashboard-1024x600-gate-h-postrun-preflight-20260526T223810Z.json`
  reported `ok:true`, the same Pi/coordinator/peer map, and no failures.

## Assumptions

- The raw proof packet, private manifest, backups, and flash evidence remain
  local/ignored artifacts and are referenced by path instead of committed.
- The DOS-C vision gate and ESP32 completion gate remain the authoritative
  live Gate H acceptance gates; advisory OCR/legibility output is recorded for
  follow-up but did not weaken the transcript-first acceptance result.

## Unknowns

- Physical wiring outside the same-session USB-only/no-load live-gate boundary
  remains unproven by the scripts.
- The exact cause of the advisory `0 px` margins and fit risks is unresolved.
  A follow-up visual-fit pass must determine whether the finding is source
  layout, Win3.1 chrome, Pi desktop capture geometry, or another display-path
  factor.
- Human operator usability of the 1000x500 client was not measured.

## Validation

- PASS: `scripts/live_bench_preflight.py --current-peer-remap --pi-host 192.168.200.153 --allow-discovered-pi-host`.
- PASS: `scripts/espnow_bbs_live_gate.py prepare ... --confirm-read-flash-backups`.
- PASS: `scripts/espnow_bbs_live_gate.py flash ... --confirm-write-flash`.
- PASS: DOS-C `scripts/win31_dashboard_vision_gate.py ...`, reporting
  `status: pass`.
- PASS: ESP32 `scripts/win31_dashboard_legibility_analyzer.py ...`, advisory
  output generated.
- PASS: ESP32 `scripts/espnow_bbs_live_gate.py complete ...`, reporting
  `status: pass`.
- PASS: Post-run `scripts/live_bench_preflight.py --current-peer-remap
  --pi-host 192.168.200.153 --allow-discovered-pi-host`.

## Result

Gate H live completion passed for the 1024x600 Win31 dashboard packet. The next
work item is visual-fit follow-up on the advisory margin and overflow findings,
not a replay of the live completion gate.
