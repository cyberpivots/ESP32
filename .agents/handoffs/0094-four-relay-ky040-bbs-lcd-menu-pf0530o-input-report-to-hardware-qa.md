# Handoff 0094: PF0530O Input Report To Hardware QA

Date: 2026-06-01

From: Firmware live-gate owner

To: Hardware QA / LCD UX validation

## Summary

PF0530O was built, written to COM6, and separately verify-flashed under the
authorized Tier 3 COM6 gate. Read-only reset and attended monitor evidence
proved PF0530O runtime readiness, LCD init on address 0x27, automatic menu
cycling disabled, real-menu calibration constants, repeated LCD render and
heartbeat output, and zero crash/unsafe markers.

## Evidence

- Task record:
  `.agents/TASK_LOG/0129-four-relay-ky040-bbs-lcd-menu-pf0530o-real-menu-calibration.md`
- Source/build ledger:
  `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530o-real-menu-cal.md`
- Live ledger:
  `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530o-live.md`
- Evidence directory:
  `<redacted-local-evidence-dir>/`

## Continue With

- Ask the user what the physical 20x4 LCD showed during the PF0530O attended
  window and whether they rotated or pressed the encoder during the timed cues.
- If the user confirms physical encoder or button actuation occurred with no
  menu response, open a fresh COM6 read-only physical/input capture gate for
  GPIO13/GPIO14/GPIO32 before any more debounce or transitions-per-step tuning.
- Keep live hardware mutation, serial command writes, flash, RF/XBee,
  relay/load/mains, wiring mutation, DMM/current measurement, erase, persistent
  configuration, release, commit, and push closed unless a separate fresh gate
  opens them.

## Known Gaps

- User visual acceptance for the physical PF0530O LCD menu is still pending.
- The attended monitor captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, and zero `BBS_MENU_SELECT`; without the user report, this is
  an input-evidence gap, not proof that the physical encoder failed.
- Physical quick-rotation behavior, short-button behavior, and long-button
  behavior under PF0530O remain unaccepted.
