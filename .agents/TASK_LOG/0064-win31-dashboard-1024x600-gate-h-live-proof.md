# Task Log 0064 - Win31 Dashboard 1024x600 Gate H Live Proof

## Task

- ID: 0064-win31-dashboard-1024x600-gate-h-live-proof
- Owner role: QA, Communications, Hardware
- Status: accepted; advisory visual-fit follow-up required
- Created: 2026-05-26
- Updated: 2026-05-26
- Contract: [../../AGENTS.md](../../AGENTS.md)

## Goal

Run the authorized same-session backup, flash, Win31 dashboard proof,
CV/OCR gate, completion audit, cleanup, and records for the 1024x600 Gate H
dashboard packet.

Accepted path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Scope

Included:

- Fresh context read-only preflight against current LAN-DHCP/remapped bench
  state.
- Full-flash backups and fresh build/manifest preparation.
- Confirmed coordinator and peer flash writes with verify evidence.
- Pi bridge and DOSBox-X Win31 OPCON run using the accepted serial-nullmodem
  path and structured `bridge-transcript.jsonl`.
- Screenshots for launch, Home, BBS, Downloads, Network, Peers, Devices,
  OTAP, Settings, Wizard, Diagnostics, Safety, final refresh, and cleanup.
- DOS-C copied-evidence vision gate.
- ESP32 advisory legibility analyzer.
- ESP32 completion audit.
- Post-run preflight and cleanup proof.

Excluded:

- No PCAP proof, packet-driver path, router/admin mutation, BLE, mesh,
  relay/XBee, TFT, MicroSD, load, mains, erase, monitor, serial-write
  expansion, or Gate G export action was opened.

## Verified Facts

- Fresh preflight
  `research/bench-records/live-bench/win31-dashboard-1024x600-gate-h-preflight-20260526T214152Z.json`
  reported `ok:true` with Pi `dospi@192.168.200.153`, coordinator
  `/dev/ttyUSB0` MAC `78:e3:6d:10:4d:6c`, and peer remap
  `peer01=COM6`, `peer02=COM10`, `peer03=COM12`.
- Prepare wrote private manifest
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260526T211658Z-win31-dashboard-1024x600-gate-h/manifest.json`
  with four full-flash backups and hashed build artifacts.
- Flash evidence
  `/mnt/h/dos-c/secrets/espnow-bbs/live-20260526T211658Z-win31-dashboard-1024x600-gate-h/flash-evidence-20260526T221511Z.json`
  reported `ok:true`; all writes and verifies returned `0`.
- Pi proof directory:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-1024x600-gate-h/gate-h-1024x600-20260526T211658Z/`.
- DOS-C ignored local proof copy:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-26-win31-dashboard-1024x600-gate-h/gate-h-1024x600-20260526T211658Z/`.
- `scrot` captured a blank X root, so `grim` was used for the 18 retained
  proof screenshots.
- `bridge-transcript.jsonl` SHA-256:
  `e857f325ecbbedb5a66023cba8ba72f00a82db29628de90de277b30ad550aa37`.
- `spool.sqlite3` SHA-256:
  `01f0265a2500b91234cea067ad5299240ec07467d4ce81e0722ca14bab31e0ef`.
- The transcript included `hello`, `state_get`, `coordinator_state`,
  `peer_list`, `diag_get`, `fw_inventory`, `msg_post`, `msg_pull`,
  `msg_search`, `msg_ack`, `download_list`, `download_status`,
  `download_queue`, `otap_status`, and `otap_intent`.
- Transcript audit found `peer01`, `peer02`, `peer03`, 24 `espnow-enc`
  mentions, serial errors all `0`, and moving RX/TX/ACK triples.
- Cleanup proof showed no DOSBox-X, zenity modal/warning, bridge process, or
  `31331`/`31332`/`8080` listener.
- DOS-C `vision-gate.json` reported `status: pass`, `ok:true`, and no
  failures.
- ESP32 `esp32-completion.json` reported `status: pass`, `ok:true`, and no
  failures.
- Advisory legibility analysis mapped target views `10/10`, but reported
  lowest bottom/right margins of `0 px`, `console_fit_risk` on 18 screens,
  `log_region_overflow` on 18 screens, and `navigation_label_gap` on 8
  screens.
- Post-run preflight
  `research/bench-records/live-bench/win31-dashboard-1024x600-gate-h-postrun-preflight-20260526T223810Z.json`
  reported `ok:true` with no failures.

## Assumptions

- Ignored/private runtime evidence remains path-addressed and should not be
  force-added to Git.
- The completion and vision gates are the pass/fail gates for this live proof;
  advisory legibility findings become follow-up visual-fit work.

## Unknowns

- Physical wiring outside the USB-only/no-load proof boundary remains
  unverified.
- The display-path cause of the advisory margin and overflow findings remains
  unresolved.
- Human usability of the revised layout remains unmeasured.

## Sources

- `SRC-LOCAL-WIN31-DASHBOARD-1024X600-2026-05-26`
- `SRC-LOCAL-WIN31-DASHBOARD-1024X600-GATE-H-LIVE-PROOF-2026-05-26`

## Validation

- PASS: Fresh `scripts/live_bench_preflight.py --current-peer-remap
  --pi-host 192.168.200.153 --allow-discovered-pi-host`.
- PASS: `scripts/espnow_bbs_live_gate.py prepare ... --confirm-read-flash-backups`.
- PASS: `scripts/espnow_bbs_live_gate.py flash ... --confirm-write-flash`.
- PASS: DOS-C `scripts/win31_dashboard_vision_gate.py ...`: `status: pass`.
- PASS: ESP32 `scripts/win31_dashboard_legibility_analyzer.py ...`: advisory
  report generated.
- PASS: ESP32 `scripts/espnow_bbs_live_gate.py complete ...`: `status: pass`.
- PASS: Post-run `scripts/live_bench_preflight.py --current-peer-remap
  --pi-host 192.168.200.153 --allow-discovered-pi-host`.

## Handoff

Continue with
[../handoffs/0053-win31-dashboard-1024x600-gate-h-live-proof-to-qa.md](../handoffs/0053-win31-dashboard-1024x600-gate-h-live-proof-to-qa.md).

## Stop Gates

Do not reopen flash, erase, monitor, serial-write expansion, PCAP,
router/admin mutation, BLE, mesh, relay/XBee, TFT, MicroSD, load, mains, or
Gate G export from this task. Treat the advisory visual-fit findings as a
source/layout/display QA issue until a later scoped task opens changes.
