# Handoff 0096: PF0530Q Input Report To Hardware QA

Date: 2026-06-01

From: Firmware live-gate owner

To: Hardware QA / LCD UX validation

## Summary

PF0530Q was built, written to COM6, and separately verify-flashed under the
authorized Tier 3 COM6 gate. Read-only reset and idle monitor evidence proved
PF0530Q runtime readiness, LCD init on address 0x27, quiet-v3 input metadata,
repeated LCD render and heartbeat output, and zero crash/unsafe markers.

The idle monitor intentionally did not include physical encoder/button
actuation. It is readiness evidence only, not physical input acceptance.

## Evidence

- Task record:
  `.agents/TASK_LOG/0132-four-relay-ky040-bbs-lcd-menu-pf0530q-quiet-calibration.md`
- Source/build ledger:
  `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530q-quiet-cal.md`
- Live ledger:
  `knowledge-base/source-ledger/2026-06-01-four-relay-ky040-bbs-lcd-menu-pf0530q-live.md`
- Evidence directory:
  `<redacted-local-evidence-dir>/`

## Continue With

- Ask the user what the physical 20x4 LCD shows under PF0530Q.
- For physical acceptance, run a separate read-only interaction monitor with
  actual rotation and button presses, then require `ENC_RAW`, `ENC_EV`,
  `BBS_MENU_STEP` in both directions, short and long `BBS_MENU_SELECT`, no
  runaway/double-step pattern beyond tolerance, readable LCD response, and zero
  crash/unsafe markers.
- Keep live hardware mutation, serial command writes, flash, RF/XBee,
  relay/load/mains, wiring mutation, DMM/current measurement, erase, persistent
  configuration, release, commit, and push closed unless a separate fresh gate
  opens them.

## Known Gaps

- User visual acceptance for the physical PF0530Q LCD menu is still pending.
- The PF0530Q idle monitor captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, zero `BBS_MENU_SELECT`, and zero `ENC_FILTER` because no
  physical actuation was expected.
- Physical direction, one-detent behavior, quick-rotation behavior,
  short-button behavior, and long-button behavior under PF0530Q remain
  unaccepted.
