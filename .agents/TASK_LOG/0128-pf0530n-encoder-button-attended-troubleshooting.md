# Task 0128: PF0530N Encoder/Button Attended Troubleshooting

Status: retry captured encoder and short-button proof; long press and user
visual report pending

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-01

## Routing

- Selected tier: Tier 3 because the task opened a live bench serial monitor on
  COM6 and required human encoder/button actuation.
- Owner role: Firmware live-gate owner with LCD UX, Hardware-safety, QA, and
  Evidence Records lenses.
- Evidence need: same-session safe-state confirmation, reviewer quorum,
  recovery reference, Windows Python/pyserial read-only COM6 transcript,
  cue notes, transcript marker scan, cleanup proof, artifact hashes, and this
  task record.
- Mutation boundary: evidence capture and durable records only.
- Live boundary: COM6 read-only monitor only at 115200 baud with
  `writes_sent=false`. No serial input, serial writes, flash, erase, XBee/RF,
  relay/load/mains, wiring, DMM/current measurement, persistent configuration,
  commit, or push.

## Verified Facts

- The user explicitly confirmed: `SAFE STATE CONFIRMED for COM6 PF0530N
  read-only attended monitor`.
- Prior PF0530N live records show PF0530N was written and verify-flashed on
  COM6, with rollback backup
  `<redacted-local-evidence-dir>/com6-pre-pf0530n-scrolling-xml-4mb.bin`
  and SHA256
  `<redacted-sha256>`.
- Reviewer quorum was completed and closed before the monitor. Weighted
  disposition was 17/17 conditional approve for the named COM6 read-only
  attended monitor after same-session safe-state confirmation.
- The first 120 second Windows Python/pyserial monitor used COM6 at 115200 baud and
  recorded `writes_sent=false`.
- The first transcript captured 60 `BBS_MENU_HB`, 60 `BBS_LCD_RENDER`, and 60
  `BBS_CURSOR` lines.
- The first transcript captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, and zero `BBS_MENU_SELECT`.
- The first transcript scan captured zero `Guru Meditation`, `Backtrace`, `panic`,
  `watchdog`, `abort()`, `LCD_INIT_FAIL`, `UNSAFE_OPEN`, `BRIDGE_OPEN`,
  `FR_DIAG_XBEE_BRIDGE_OPEN`, or `unsafe-open` markers.
- Cleanup proof found no lingering monitor/esptool/idf.py process; process
  scan matches were the cleanup commands themselves or unrelated system
  Python.
- The user reported missing the first action window and requested restart.
- The retry used the same read-only COM6 boundary, added a 20 second idle
  lead-in, and recorded `writes_sent=false`.
- The retry transcript captured 489 `ENC_RAW`, 316 `ENC_EV`, 12
  `BBS_MENU_STEP`, five `BBS_MENU_SELECT`, 129 `BBS_LCD_RENDER`, 75
  `BBS_MENU_HB`, and 129 `BBS_CURSOR` lines.
- The retry transcript captured both step directions: three
  `BBS_MENU_STEP dir=+` and nine `BBS_MENU_STEP dir=-`.
- The retry transcript captured five `BBS_MENU_SELECT kind=short` lines and
  zero `BBS_MENU_SELECT kind=long` lines.
- The retry transcript scan captured zero `Guru Meditation`, `Backtrace`,
  `panic`, `watchdog`, `abort()`, `LCD_INIT_FAIL`, `UNSAFE_OPEN`,
  `BRIDGE_OPEN`, `FR_DIAG_XBEE_BRIDGE_OPEN`, or `unsafe-open` markers.
- Final retry cleanup proof found no lingering monitor/esptool/idf.py process;
  process scan matches were cleanup commands themselves or unrelated system
  Python.

## Assumptions

- COM6 still refers to the same ESP32 target proven by the previous PF0530N
  write/verify gate.
- The read-only monitor attached to an already-running PF0530N image; lack of
  boot readiness/schema lines in this transcript does not contradict prior
  PF0530N boot proof.
- Cue delivery was chat-guided and slightly drifted while live output was
  polled. User visual/actuation report is required before classifying the
  zero-input result as hardware/input capture failure instead of missed cues.

## Unknowns

- Whether the user completed the encoder rotations and button presses during
  the first timed window is resolved: the user missed it.
- What the LCD did visibly during the retry cue windows.
- Whether the intended long press happened during the retry but was
  misclassified/missed, or whether the long-press cue arrived too late for a
  complete hold/release cycle before monitor end.

## Evidence

- Evidence directory:
  `<redacted-local-evidence-path>`
- Cue plan: `cue-plan.txt`
- Monitor metadata: `attended-monitor-metadata.txt`
- Transcript: `attended-monitor-transcript-windows.txt`
- Transcript scan: `attended-transcript-scan.txt` and
  `attended-transcript-scan.json`
- Cue notes: `operator-cue-notes.txt`
- Cleanup proof: `cleanup-proof.txt`, `cleanup-wsl-process-scan.txt`, and
  `cleanup-windows-process-scan.json`
- Hash manifest: `sha256-manifest.json`
- Retry evidence directory:
  `<redacted-local-evidence-path>`
- Retry cue plan: `cue-plan.txt`
- Retry monitor metadata: `attended-monitor-metadata.txt`
- Retry transcript: `attended-monitor-transcript-windows.txt`
- Retry console copy: `monitor-console.txt`
- Retry transcript scan: `attended-transcript-scan.txt` and
  `attended-transcript-scan.json`
- Retry cue notes: `operator-cue-notes.txt`
- Retry cleanup proof: `cleanup-proof.txt`, `cleanup-wsl-process-scan.txt`,
  `cleanup-windows-process-scan.json`, `final-cleanup-proof.txt`,
  `final-cleanup-wsl-process-scan.txt`, and
  `final-cleanup-windows-process-scan.json`
- Retry hash manifest: `sha256-manifest.json`

## Validation

- PASS: read-only transcript was captured with `writes_sent=false`.
- PASS: transcript scan completed.
- PASS: unsafe-marker scan found zero unsafe markers.
- PASS: cleanup proof was captured.
- PASS: retry read-only transcript captured raw encoder events, decoded
  encoder events, menu steps in both directions, five short button selections,
  continuing heartbeats, and continuing renders.
- PARTIAL: retry did not capture a long button selection.
- PENDING: user visual report, especially whether the LCD movement was timely
  and whether a long press was attempted long enough to cross the firmware
  threshold.

## Diagnosis State

The first serial transcript proves PF0530N stayed alive and rendering during
the attended window, but it was inconclusive for encoder/button interaction
because the user missed the action window. The retry proves physical encoder
capture, decoded menu steps in both directions, render continuation, and five
short button selections. Long press remains unproven in the retry: either the
long-press cue/hold did not complete before monitor end, or long-press
classification needs follow-up.

## Follow-Up

The user then rejected simulator/mock acceptance and requested real-menu
calibration for the programmed LCD review path. PF0530O source/build follow-up
is recorded in
`.agents/TASK_LOG/0129-four-relay-ky040-bbs-lcd-menu-pf0530o-real-menu-calibration.md`.
That follow-up was later authorized for COM6 write/verify/read-only monitor
proof and remains open only for user visual/input acceptance.

## Decision Footer

Decision: `superseded_by_pf0530o_live_calibration`. Next gate: user
visual/input report for PF0530O, then a COM6 read-only physical/input capture
gate if the user confirms actuation occurred without LCD/menu response. Owner:
Firmware live-gate owner with LCD UX and Hardware QA lenses. Evidence: first
and retry read-only COM6 transcripts, scans, cleanup, this task record, and
PF0530O source/live records. Approved mutation boundary: evidence records only
for this task; PF0530O source/build/live work is tracked separately. Authority
limits: no flash, erase, serial writes, XBee/RF, relay/load/mains, wiring,
DMM/current, persistent configuration, commit, or push.
