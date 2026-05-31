# Four Relay KY-040 BBS LCD Menu PF0530I Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530I-2026-05-31`

## Verified Facts

- PF0530H COM6 proof captured LCD init, BBS ready, LCD render, and menu
  heartbeat lines, but captured zero `BBS_MENU_STEP` and zero
  `BBS_MENU_SELECT` lines.
- The PF0530H read-only transcript showed full `BBS_LCD_RENDER` and
  `BBS_MENU_HB` cadence near 15 seconds, even though the source intended a
  2 ms input poll and 2 second heartbeat in the same task.
- Prior PF0530E r5 read-only monitor proof recorded GPIO13 `CLK`, GPIO14
  `DT`, and GPIO32 `SW` transitions during user-confirmed encoder and
  button actuation.
- PF0530I changes the active firmware ID to `PF0530I`, keeps
  `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, preserves GPIO13/GPIO14/GPIO32 as
  input-only encoder lines with internal pullups, and preserves LCD I2C0
  GPIO21/GPIO22 display-only writes.
- PF0530I separates fast encoder polling into `fr_menu_input_task` at a higher
  task priority than the LCD renderer, renders only dirty rows or a slow idle
  refresh, emits `BBS_INPUT_READY`, emits `ENC_RAW` on raw input transitions,
  and extends `BBS_LCD_RENDER` with row-count, sequence, duration, and reason
  fields.

## Assumptions

- The user-reported PF0530H symptom is caused primarily by LCD render
  starvation of the same-task input poll, not by changed wiring.
- The PF0530I BBS LCD pages remain local simulated menu content only. They are
  not a new BBS bridge ABI, coordinator serial ABI, XBee payload, ESP-NOW
  runtime, relay-control surface, or firmware-update surface.

## Unknowns

- Same-session COM6 identity, physical LCD visual state after PF0530I, encoder
  direction, `BBS_MENU_STEP`, `BBS_MENU_SELECT`, boot-held switch behavior,
  rail margin, and LCD backpack pullup voltage remain unproven until the live
  gate completes.

## Validation

- Source mutation updates `firmware/projects/four-relay-xbee-wifi/main/main.c`,
  firmware scaffold audits, the encoder pullup boundary test, firmware/project
  documentation, this source ledger, source index, docs index, task log, and QA
  handoff.
- Host/scaffold validation and ESP-IDF no-flash build results are recorded in
  `.agents/TASK_LOG/0112-four-relay-ky040-bbs-lcd-menu-pf0530i.md`.
- The first PF0530I live monitor emitted repeated task-watchdog `Backtrace:`
  lines. PF0530I is superseded by PF0530J and is not accepted as the final
  interactive menu image.

## Authority Limits

- This source record does not by itself prove live flash, monitor, serial
  writes, XBee/RF, ESP-NOW runtime, relay GPIO writes, relay-expander writes,
  MicroSD/TFT action, wiring mutation, load, mains, erase, commit, or push.
- A live PF0530I COM6 gate requires same-session authority, COM6 identity,
  full rollback backup and recovery command, staged artifact hashes,
  write-flash log, separate verify-flash log, read-only monitor transcript,
  transcript scan, cleanup proof, and reviewer quorum.
