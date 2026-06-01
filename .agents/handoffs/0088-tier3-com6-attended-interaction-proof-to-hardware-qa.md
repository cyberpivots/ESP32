# Handoff 0088: Tier 3 COM6 Attended Interaction Proof To Hardware QA

Status: interaction proof accepted; hardware/electrical follow-up remains open

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-31

## Summary

The initial user-authorized Tier 3 COM6 attended proof confirmed PF0530L was
alive on COM6 but missed physical input because the user did not see the start
cue. The restarted read-only proof accepted physical interaction: the retry
captured 768 `ENC_RAW`, 456 `ENC_EV`, six `BBS_MENU_STEP`, and 11
`BBS_MENU_SELECT` lines, including both menu-step directions and both short
and long button selections.

## Evidence

- Task record:
  [../TASK_LOG/0121-tier3-com6-attended-interaction-proof.md](../TASK_LOG/0121-tier3-com6-attended-interaction-proof.md)
- Source ledger:
  [../../knowledge-base/source-ledger/2026-05-31-tier3-com6-attended-interaction-proof.md](../../knowledge-base/source-ledger/2026-05-31-tier3-com6-attended-interaction-proof.md)
- Ignored local evidence:
  `<redacted-local-evidence-path>`
- Ignored retry evidence:
  `<redacted-local-evidence-path>`

## Required Next Evidence

- Power-off visual/continuity confirmation from KY-040 `CLK`, `DT`, `SW`, `+`,
  and `GND` to the ESP32 header positions used by GPIO13, GPIO14, GPIO32, 3V3,
  and GND.
- A/B idle-high and toggle-low evidence while rotating, plus SW idle-high and
  pulls-low evidence while pressing.
- Rail-current margin and LCD backpack pullup-voltage evidence before broader
  hardware acceptance.
- Another attended read-only monitor only if direction calibration, LCD visual
  behavior, or a future firmware change needs fresh proof.

## Stop Gates

Do not flash, erase, write serial commands, transmit RF, change XBee settings,
actuate relays, change wiring under power, attach loads, touch mains, write
persistent configuration, publish to GitHub, or claim hardware acceptance from
the current transcript.
