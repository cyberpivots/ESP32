# Win31 Dashboard 1024x600 Gate H Live Proof Source Ledger

Date: 2026-05-26

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-WIN31-DASHBOARD-1024X600-2026-05-26`
- `SRC-LOCAL-WIN31-DASHBOARD-1024X600-GATE-H-LIVE-PROOF-2026-05-26`

## Scope

Authorized live Gate H proof for the revised Win31 OPCON 1024x600 dashboard
using the accepted serial-nullmodem path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Evidence

- Ignored original preflight:
  `research/bench-records/live-bench/win31-dashboard-1024x600-gate-h-preflight-20260526T202729Z.json`.
- Ignored fresh preflight:
  `research/bench-records/live-bench/win31-dashboard-1024x600-gate-h-preflight-20260526T214152Z.json`.
- Ignored post-run preflight:
  `research/bench-records/live-bench/win31-dashboard-1024x600-gate-h-postrun-preflight-20260526T223810Z.json`.
- Private manifest:
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260526T211658Z-win31-dashboard-1024x600-gate-h/manifest.json`.
- Private flash evidence:
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260526T211658Z-win31-dashboard-1024x600-gate-h/flash-evidence-20260526T221511Z.json`.
- Pi proof directory:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-1024x600-gate-h/gate-h-1024x600-20260526T211658Z/`.
- DOS-C ignored local proof copy:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-1024x600-gate-h/gate-h-1024x600-20260526T211658Z/`.
- Tracked bench record:
  `research/bench-records/live-bench/2026-05-26-win31-dashboard-1024x600-gate-h-live-proof.md`.
- ESP32 task record:
  `.agents/TASK_LOG/0064-win31-dashboard-1024x600-gate-h-live-proof.md`.
- ESP32 handoff:
  `.agents/handoffs/0053-win31-dashboard-1024x600-gate-h-live-proof-to-qa.md`.
- Paired DOS-C task record:
  `/mnt/h/dos-c/.agents/tasks/0033-win31-dashboard-1024x600-gate-h-live-proof.md`.

## Verified Facts

- Fresh and post-run preflights reported `ok:true` for Pi
  `dospi@192.168.200.153`, coordinator `/dev/ttyUSB0` MAC
  `78:e3:6d:10:4d:6c`, and peer remap `peer01=COM6`,
  `peer02=COM10`, `peer03=COM12`.
- Prepare completed with private full-flash backups and hashed build
  artifacts for coordinator, `peer01`, `peer02`, and `peer03`.
- Flash evidence reported `ok:true`; all four write and verify steps returned
  `0`.
- The Pi bridge ran with structured audit transcript enabled, physical serial
  coordinator backend, `/dev/ttyUSB0`, `--allow-physical-serial`, and
  `--read-only`.
- The proof packet contains 18 retained screenshots from launch through
  pre-cleanup.
- The transcript captured pre/post telemetry plus BBS post/pull/search/ack,
  download list/status/queue, OTAP status, and non-executing OTAP intent.
- Transcript audit found zero serial errors, peer IDs `peer01`, `peer02`, and
  `peer03`, 24 `espnow-enc` mentions, and moving RX/TX/ACK triples.
- Cleanup proof found no DOSBox-X process, zenity modal/warning process,
  bridge process, or relevant listener.
- DOS-C vision gate reported `status: pass`.
- ESP32 completion gate reported `status: pass`.
- Advisory legibility analysis mapped `10/10` target views but recorded
  `0 px` bottom/right margins and overflow/fit risks on the screenshot set.

## Assumptions

- Raw proof screenshots, runtime logs, SQLite spool, private backups, and flash
  evidence stay ignored/private and are referenced by path.
- The advisory analyzer output should drive visual-fit follow-up without
  weakening the passed transcript-first live completion result.

## Unknowns

- Physical wiring outside the USB-only/no-load live-gate boundary remains
  unproven.
- The cause of the advisory margin and overflow findings remains unresolved.

## Result

The 1024x600 Win31 dashboard Gate H live proof passed. Visual-fit remediation
remains a separate QA follow-up.
