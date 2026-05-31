# Four Relay KY-040 BBS LCD Menu PF0530H Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-2026-05-31`

## Verified Facts

- PF0530F previously passed COM6 write/verify but blocked menu acceptance on
  `PF0530F LCD_INIT_FAILED` before `MENU_HB`, `MENU_STEP`, or `MENU_SELECT`
  proof.
- PF0530G later passed serial LCD init diagnosis on COM6 with exactly one LCD
  ACK at `0x27`, `LCD_INIT_OK addr=0x27`, and repeated ok diagnostic
  heartbeats.
- PF0530H source now changes the active firmware ID to `PF0530H`, starts
  `fr_lcd_bbs_menu_task`, keeps `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, and preserves
  GPIO13/GPIO14/GPIO32 as input-only encoder lines with internal pullups.
- PF0530H uses the PF0530G LCD init/probe path on I2C0 GPIO21/GPIO22 and then
  renders nine local static/simulated BBS pages: `HOME`, `MESSAGES`, `PEERS`,
  `QUEUE`, `FILES`, `MESH`, `XBEE`, `DIAG`, and `LOCKS`.
- PF0530H source-visible UART0 proof markers are `PF0530H BBS_LCD_READY`,
  `BBS_LCD_RENDER`, `BBS_MENU_HB`, `BBS_MENU_STEP`, and `BBS_MENU_SELECT`.

## Assumptions

- The PF0530H BBS LCD pages are local simulated menu content only. They are not
  a new BBS bridge ABI, coordinator serial ABI, XBee payload, ESP-NOW runtime,
  relay-control surface, or firmware-update surface.
- COM6 remains only a later live target until same-session identity, rollback,
  recovery, flash, verify, and read-only monitor evidence pass.

## Unknowns

- Current COM6 identity, physical LCD visual state, encoder rotation direction,
  boot-held switch behavior, rail margin, and LCD backpack pullup voltage are
  not established by this source update.

## Validation

- Source mutation updates `firmware/projects/four-relay-xbee-wifi/main/main.c`,
  firmware scaffold audits, the encoder pullup boundary test, firmware/project
  documentation, the ESP-NOW BBS LCD field-console plan, this source ledger,
  source index, docs index, task log, and QA handoff.
- Host/scaffold validation and ESP-IDF no-flash build results are recorded in
  `.agents/TASK_LOG/0111-four-relay-ky040-bbs-lcd-menu-pf0530h.md`.

## Authority Limits

- This source record does not authorize or prove live flash, monitor, serial
  writes, XBee/RF, ESP-NOW runtime, relay GPIO writes, relay-expander writes,
  MicroSD/TFT action, wiring mutation, load, mains, erase, commit, or push.
- A live PF0530H COM6 gate requires same-session authority, COM6 identity,
  full rollback backup and recovery command, staged artifact hashes,
  write-flash log, separate verify-flash log, read-only monitor transcript,
  transcript scan, cleanup proof, and reviewer quorum.
