# Four Relay KY-040 BBS LCD Menu PF0530J Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530J-2026-05-31`

## Verified Facts

- PF0530I fixed PF0530H LCD render starvation by splitting input polling from
  LCD rendering, but the first PF0530I read-only monitor emitted repeated
  task-watchdog backtrace lines.
- Address decoding mapped PF0530I backtraces to `fr_menu_input_task`,
  `fr_menu_poll`, and ESP-IDF task-watchdog handling. The root cause was the
  new higher-priority input task using a 2 ms delay that can collapse to zero
  ticks on the current FreeRTOS tick rate.
- PF0530J changes the active firmware ID to `PF0530J`, keeps the PF0530I split
  input/render architecture, changes `FR_MENU_POLL_MS` to 10, and adds
  `fr_delay_ticks_at_least_one()` so the input task always yields for at least
  one FreeRTOS tick.
- PF0530J keeps `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, preserves GPIO13/GPIO14/GPIO32
  as input-only encoder lines with internal pullups, and preserves LCD I2C0
  GPIO21/GPIO22 display-only writes.

## Assumptions

- PF0530J should preserve PF0530I responsiveness while avoiding idle-task
  starvation and task-watchdog backtraces.
- The BBS LCD pages remain local simulated menu content only. They are not a
  new BBS bridge ABI, coordinator serial ABI, XBee payload, ESP-NOW runtime,
  relay-control surface, or firmware-update surface.

## Unknowns

- Same-session PF0530J live monitor proof, physical LCD visual state, encoder
  direction, `BBS_MENU_STEP`, `BBS_MENU_SELECT`, boot-held switch behavior,
  rail margin, and LCD backpack pullup voltage remain unproven until the
  PF0530J live gate completes.

## Validation

- Source mutation updates `firmware/projects/four-relay-xbee-wifi/main/main.c`,
  firmware scaffold audits, the encoder pullup boundary test, firmware/project
  documentation, this source ledger, source index, docs index, task log, and QA
  handoff.
- Host/scaffold validation and ESP-IDF no-flash build results are recorded in
  `.agents/TASK_LOG/0113-four-relay-ky040-bbs-lcd-menu-pf0530j.md`.
- PF0530J live flash and separate verify-flash completed, and the read-only
  monitor showed no watchdog/backtrace/panic markers. The same monitor captured
  no encoder/button input proof (`ENC_RAW`, `ENC_EV`, `BBS_MENU_STEP`, or
  `BBS_MENU_SELECT`), so PF0530J is superseded by PF0530K for the next input
  proof gate.

## Authority Limits

- This source record does not by itself prove live flash, monitor, serial
  writes, XBee/RF, ESP-NOW runtime, relay GPIO writes, relay-expander writes,
  MicroSD/TFT action, wiring mutation, load, mains, erase, commit, or push.
- A live PF0530J COM6 gate requires same-session authority, COM6 identity,
  full rollback backup and recovery command, staged artifact hashes,
  write-flash log, separate verify-flash log, read-only monitor transcript,
  transcript scan, cleanup proof, and reviewer quorum.
