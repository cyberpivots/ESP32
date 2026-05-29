# Task 0086 - XBee Radio Programming Study

## Triage

- Verified facts: Existing XBee read-only proof and source-index coverage are
  present; Digi support currently lists XCTU 6.5.13 assets; the plan keeps
  radio writes out of v1.
- Assumptions: This pass is Tier 2 docs/tooling only and may add offline CLI
  behavior, tests, source records, and skill guidance.
- Unknowns: Current host XCTU/XBee Studio install state, exact XBee adapter
  port, current radio settings, installer SHA-256, first-run XCTU version, and
  update prompts.
- Selected tier: Tier 2.
- Owner role: Tooling, with Communications, Hardware, Agent Operations, and QA
  lenses.
- Evidence need: Official Digi current-source refresh, source-index entries,
  hardware-free tests, and scaffold validation.
- Mutation boundary: Add `scripts/xbee_radio_study.py`, tests, XBee study docs,
  source records, repo-local skill, private XBee submodule notes, task log, and
  handoff. No live serial probe, radio setting write, firmware change, GUI
  install, or hardware action.
- Validation plan: Run the existing XBee self-test/list checks, new wrapper
  tests, scaffold audits, and `git diff --check`.

## Work Completed

- Added `scripts/xbee_radio_study.py` with `inventory`, `readonly`,
  `profile-diff`, and `write-plan`.
- Added `tests/scaffold_audits/test_xbee_radio_study.py` for no-serial-open,
  confirmation, redaction, blocked-write, and no-apply behavior.
- Added [XBee radio programming study](../../docs/projects/four-relay-xbee-wifi/xbee-radio-programming-study.md).
- Added `.codex/skills/xbee-radio-integration/SKILL.md`.
- Updated parent source/index/status records and the private
  `rlxsc-xbee-pro-s3b` submodule study notes.

## Reviewer Quorum

- Coordinator: approved Tier 2 docs/tooling boundary.
- Hardware/live-gate review: no P1/P2 blockers; adapter/carrier/voltage,
  DIN/DOUT, antenna/regulatory, and privacy risks remain open.
- Communications review: no P1/P2 blockers after clarifying that `readonly`
  sends non-persistent serial read-query bytes after confirmation.
- Skill/source review: no P1/P2 blockers for the skill and skills inventory
  update, with redaction and source-citation constraints.
- QA review: no P1/P2 blockers; requested hardware-free tests for no-write and
  redaction guarantees.

## Closed Gates

- No XBee setting write.
- No `WR` or `AC`.
- No API transmit frame.
- No firmware update/recovery.
- No range test or RF transmit exercise.
- No ESP32 DIN/DOUT wiring.
- No relay/load/mains action.
- No Windows GUI installer launch.

## Continuation

- Task 0087 records the later Tier 2 host-tooling gate that downloaded and
  installed XCTU as a reference GUI tool. That continuation did not open serial
  ports, add/discover XBee devices, or authorize any radio write/transmit
  operation.

## Validation

Validation commands and results are recorded in the final task response for
this pass.
