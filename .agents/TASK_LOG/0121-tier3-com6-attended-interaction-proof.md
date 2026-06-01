# Task 0121: Tier 3 COM6 Attended Interaction Proof

Status: completed; physical interaction accepted on retry

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-31

## Goal

Run the user-authorized Tier 3 COM6 attended interaction proof for the current
PF0530L LCD/menu firmware without opening flash, serial-write, RF/XBee-write,
relay, wiring, persistent configuration, credential, external-service,
destructive, GitHub publication, or release surfaces.

## Routing

- Selected tier: Tier 3 because the task touched a live bench serial device.
- Owner role: Live Bench Gate Reviewer with Firmware, Hardware-risk, QA,
  Evidence Records, and Governance lenses.
- Evidence need: same-session COM6 identity, recovery reference, read-only
  attended monitor transcript, transcript scan, unsafe-marker scan, cleanup
  proof, and durable source/index/task records.
- Mutation boundary: source/index/task/handoff/status records, scaffold audit
  expectation updates, and ignored local evidence under
  `research/bench-records/xbee-readonly/`.
- Live boundary: COM6 read-only identity and read-only monitor only. No
  flashing, erase, serial writes, XBee/RF transmit or setting writes, relay
  action, wiring, load, mains, persistent configuration, or external services.

## Verified Facts

- User provided explicit Tier 3 COM6 attended proof authority and confirmed
  the bench safe state.
- The previous PF0530L live gate recorded a valid rollback image at
  `<redacted-local-evidence-path>`
  with SHA256
  `<redacted-sha256>`.
- Same-session Windows esptool read-only identity on COM6 passed:
  ESP32-D0WDQ6, MAC `<redacted-mac>`, detected 4 MB flash, and 3.3 V flash
  strap.
- WSL `/dev/ttyS6` monitor setup failed with a pyserial input/output error, so
  the attended proof used Windows Python pyserial on COM6.
- The initial 90 second Windows COM6 monitor used `writes_sent=false`,
  captured 23,667 bytes and 135 metadata-counted lines, and saved both
  transcript and raw bytes.
- The initial transcript scan found 45 `BBS_MENU_HB`, 45 `BBS_LCD_RENDER`, and
  45 `BBS_CURSOR` lines with zero watchdog, backtrace, panic,
  LCD-init-failure, or unsafe-open markers, but zero `ENC_RAW`, zero `ENC_EV`,
  zero `BBS_MENU_STEP`, and zero `BBS_MENU_SELECT`.
- The user reported missing the initial start cue and requested a restarted
  attended proof.
- The retry read-only identity on COM6 passed again for `chip_id`, `read_mac`,
  and `flash_id`.
- The retry 120 second Windows COM6 monitor used `writes_sent=false`, captured
  137,059 bytes and 3,445 metadata-counted lines, and saved both transcript
  and raw bytes.
- The retry transcript scan found 768 `ENC_RAW`, 456 `ENC_EV`, six
  `BBS_MENU_STEP`, 11 `BBS_MENU_SELECT`, 59 `BBS_MENU_HB`, 135
  `BBS_LCD_RENDER`, 135 `BBS_CURSOR`, one `LCD_INIT_OK`, one
  `PF0530L BBS_LCD_READY`, and one `BBS_INPUT_READY`.
- The retry event proof included both menu-step directions and both short and
  long button selections.
- Both scans found zero watchdog, backtrace, panic, LCD-init-failure, or
  unsafe-open markers.
- Cleanup proof found no lingering monitor/esptool/idf.py processes after the
  retry proof window.

## Assumptions

- The retry capture reflects the user's physical rotation and button actions
  during the attended 120 second monitor window.
- Cumulative heartbeat counters such as `steps=1/3`, `buttons=2`, and
  `invalid=5` can reflect prior runtime history and do not substitute for
  timestamped event lines during the attended capture.

## Unknowns

- Physical LCD/glyph readability, precise direction-label expectation,
  rail margin, LCD backpack pullup voltage, and boot-held switch behavior
  remain unaccepted.
- Hardware/electrical acceptance still needs continuity, idle/toggle levels,
  pullup behavior, and rail-current evidence; the serial/menu interaction proof
  is accepted separately.

## Reviewer Quorum

- Coordinator/Architecture-risk local lens, weight 5: approved the named
  COM6 read-only proof boundary.
- Live Bench local lens, weight 5: approved only after same-session identity,
  recovery reference, read-only monitor, transcript scan, and cleanup proof.
- QA local lens, weight 3: approved records-only follow-up; blocked physical
  interaction acceptance without event lines.
- Evidence Records local lens, weight 2: approved source/index/task linkage.
- Hardware-risk local lens, weight 3: conditional approve with relay, RF,
  wiring, load, and mains surfaces closed.

Weighted disposition: 18/18 pass for the named read-only proof and records
boundary. No P1/P2 blocker remained inside that boundary. Physical interaction
failed closed on the initial capture and passed on the retry capture.

## Evidence

- Evidence directory:
  `<redacted-local-evidence-path>`
- Identity summary: `identity-summary.json`
- Monitor metadata: `attended-monitor-metadata-windows.json`
- Transcript scan: `attended-transcript-scan.txt` and
  `attended-transcript-scan.json`
- Cleanup proof: `cleanup-proof.json`
- Evidence hash manifest: `sha256-manifest.json`
- Retry evidence directory:
  `<redacted-local-evidence-path>`
- Retry identity summary: `identity-summary.json`
- Retry monitor metadata: `attended-monitor-metadata-windows.json`
- Retry transcript scan: `attended-transcript-scan.txt` and
  `attended-transcript-scan.json`
- Retry cleanup proof: `cleanup-proof.json`
- Retry evidence hash manifest: `sha256-manifest.json`
- Scaffold audit updates:
  `scripts/scaffold_audit_agent_process.py` and
  `tests/scaffold_audits/test_comprehensive_bench_process.py`

## Result

COM6 is alive as the PF0530L LCD/menu firmware and continues to emit cursor,
render, and heartbeat proof with no crash or unsafe-open markers. The attended
physical interaction proof is accepted on the retry because the transcript
captured raw input, pin events, menu steps in both directions, and short/long
button selections.

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `git diff --check`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'` (55 tests)
- PASS: `git diff --check`

## Closed Surfaces

No flashing, erase, serial writes, XBee/RF transmit or setting writes, relay
GPIO writes, relay-expander writes, wiring mutation, MicroSD/TFT action,
relay/load/mains work, persistent configuration writes, credential access,
external service changes, GitHub publication, release gate, or destructive
operation was opened by this proof.
