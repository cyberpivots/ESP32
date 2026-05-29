# Task 0087 - XCTU Download And Install

## Triage

- Verified facts: Digi's official XCTU support path still listed the Windows
  6.5.13 asset; parent and XBee submodule worktrees were clean before the
  host-tooling gate; the existing XBee study CLI kept radio write/transmit
  surfaces blocked.
- Assumptions: Installing XCTU and its bundled Digi USB RF host driver is Tier 2
  host-tooling work when no serial/radio operation is used.
- Unknowns: Current XBee adapter identity, current radio settings, future write
  tool, and any future XCTU application or firmware-library update prompt after
  the first-run change-log screen.
- Selected tier: Tier 2 host-tooling/evidence.
- Owner role: Tooling, with Hardware, Communications, Agent Operations, and QA
  lenses.
- Evidence need: Official Digi source path, installer hash, install path,
  first-run prompt/version evidence, post-install inventory, and redacted source
  records.
- Mutation boundary: Download/install Windows XCTU host software, complete the
  bundled Digi USB RF driver prompt, update inventory path detection, and update
  docs/source/task/handoff records. No serial open, radio read/write, firmware
  operation, range test, wiring, relay/load/mains action, or RF evidence.
- Validation plan: Run post-install inventory, focused XBee study tests, full
  scaffold audit tests, scaffold verifiers, and `git diff --check`.

## Work Completed

- Downloaded Digi `40003026_AL.exe` from the official XCTU support download
  path and recorded SHA-256
  `9b6acd16927ee17d4f3a728768cd1c559e09ab6b12470fd6da08e7106fb308e1`.
- Installed XCTU 6.5.13.2 to the Windows per-user Digi `XCTU-NG` path.
- Completed the bundled Digi USB RF Device Drivers installer after Windows
  Security prompts for Digi International device software; persistent trust was
  kept off.
- Launched XCTU once, captured the 6.5.13 change-log first-run screen, observed
  no separate application update prompt, and closed XCTU without adding or
  discovering devices.
- Updated `scripts/xbee_radio_study.py` so `inventory` detects per-user Windows
  `XCTU-NG` installs.

## Reviewer Quorum

- Coordinator: approved Tier 2 host-tooling/evidence boundary only.
- Tooling: no P1/P2 blockers after official URL, hash, signature, install path,
  driver prompt, and post-install inventory evidence were captured.
- Hardware: no P1/P2 blockers because no carrier, antenna, voltage, DIN/DOUT,
  relay/load/mains, or live RF action was performed.
- Communications: no P1/P2 blockers because no serial console, AT command, API
  frame, firmware operation, or range-test path was used.
- QA: no P1/P2 blockers pending scaffold validation; public records stay
  redacted and local evidence remains ignored.

## Closed Gates

- XCTU host install proof is recorded.
- Installer SHA-256 and byte size are recorded.
- First-run change-log evidence is recorded.
- Post-install inventory still has `serialOpenAttempted: false`.

## Still Blocked

Live adapter identity, read-only radio backup/readback, profile write review,
setting writes, `WR`, `AC`, API transmit frames, firmware recovery/update,
range tests, ESP32 carrier wiring, relay/load/mains work, and live RF evidence
remain blocked until a future explicit Tier 3 gate.

## Validation

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py self-test --json`:
  PASS, 21/21.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py list --json`:
  PASS; no serial port opened.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_xbee_radio_study`:
  PASS, 9 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`:
  PASS, 29 tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`: PASS.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`: PASS.
- `git diff --check` and submodule `git diff --check`: PASS.
