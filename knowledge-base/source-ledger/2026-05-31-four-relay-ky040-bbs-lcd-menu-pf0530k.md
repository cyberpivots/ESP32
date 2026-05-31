# Four Relay KY-040 BBS LCD Menu PF0530K Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530K-2026-05-31`

## Verified Facts

- PF0530J write-flash and separate verify-flash passed on COM6, and its first
  read-only monitor showed no task-watchdog, backtrace, panic, guru-meditation,
  or LCD-init-failure lines.
- That PF0530J monitor also captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, and zero `BBS_MENU_SELECT` lines, so PF0530J was not
  accepted as a fully proven interactive LCD menu.
- PF0530K changes the active firmware ID to `PF0530K`, keeps
  `FR_MENU_POLL_MS 10`, keeps `fr_delay_ticks_at_least_one()`, and keeps the
  split input/render task design from PF0530J.
- PF0530K adds GPIO any-edge interrupt capture for GPIO13/GPIO14/GPIO32,
  queues input edges with `FR_ENCODER_EVENT_QUEUE_DEPTH 64`, drains up to
  `FR_ENCODER_IRQ_DRAIN_LIMIT 32` queued events per input poll, and decodes
  menu rotation from raw A/B transitions.
- PF0530K keeps `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, keeps GPIO13/GPIO14/GPIO32
  input-only with internal pullups, and keeps LCD writes display-only on
  GPIO21/GPIO22.

## Assumptions

- The first PF0530J no-input monitor may have lacked physical actuation, but
  the unresolved user symptom still justifies a more robust input path before
  the next live proof.
- GPIO any-edge queueing should catch short KY-040 pulses that a 10 ms polling
  loop might otherwise miss.
- The BBS LCD pages remain local simulated menu content only. They are not a
  BBS bridge ABI, coordinator serial ABI, XBee payload, ESP-NOW runtime,
  relay-control surface, or firmware-update surface.

## Unknowns

- Same-session PF0530K live monitor proof, physical LCD visual state, encoder
  direction, `BBS_MENU_STEP`, `BBS_MENU_SELECT`, boot-held switch behavior,
  rail margin, and LCD backpack pullup voltage remain unproven until the
  PF0530K live gate completes.

## Validation

- Source mutation updates `firmware/projects/four-relay-xbee-wifi/main/main.c`,
  firmware scaffold audits, the encoder pullup boundary test, firmware/project
  documentation, this source ledger, source index, docs index, task log, and QA
  handoff.
- Host/scaffold validation and ESP-IDF no-flash build results are recorded in
  `.agents/TASK_LOG/0114-four-relay-ky040-bbs-lcd-menu-pf0530k.md`.
- PF0530K live flash and separate verify-flash completed, and the read-only
  monitor showed no watchdog/backtrace/panic markers. The same monitor captured
  no encoder/button input proof (`ENC_RAW`, `ENC_EV`, `BBS_MENU_STEP`, or
  `BBS_MENU_SELECT`), so PF0530K is flashed for user testing but not accepted
  as proven interactive until physical actuation is captured.

## Authority Limits

- This source record does not by itself prove live flash, monitor, serial
  writes, XBee/RF, ESP-NOW runtime, relay GPIO writes, relay-expander writes,
  MicroSD/TFT action, wiring mutation, load, mains, erase, commit, or push.
- A live PF0530K COM6 gate requires same-session authority, COM6 identity,
  full rollback backup and recovery command, staged artifact hashes,
  write-flash log, separate verify-flash log, read-only monitor transcript,
  transcript scan, cleanup proof, and reviewer quorum.
