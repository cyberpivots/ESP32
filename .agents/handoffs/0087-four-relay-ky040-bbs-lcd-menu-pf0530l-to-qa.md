# PF0530L BBS LCD Menu Handoff To QA

PF0530L supersedes PF0530K for the next user-test firmware image and is now
written and separately verify-flashed on COM6. PF0530K flashed and verified
cleanly but did not capture encoder/button input events. PF0530L keeps the
PF0530K interrupt input path and adds the LCD menu UX surface:
page/row/detail/edit modes, software cursor/DDRAM metadata, dirty-cell metadata,
five named eight-slot glyph banks, custom widget pages, and a seven-second
auto-demo cycle.

## Review Focus

- Confirm the active firmware ID is `PF0530L`.
- Confirm required proof strings are source-visible: `PF0530L BBS_LCD_READY`,
  `BBS_INPUT_READY`, `irq=anyedge queue=64`, `BBS_GLYPH_BANK`, `BBS_CURSOR`,
  `BBS_LCD_RENDER`, `BBS_MENU_AUTO`, `BBS_MENU_HB`, `ENC_RAW`, `ENC_EV`,
  `BBS_MENU_STEP`, and `BBS_MENU_SELECT`.
- Confirm GPIO13/GPIO14/GPIO32 stay input-only with internal pullups and no
  GPIO outputs are added.
- Confirm LCD writes remain display-only on GPIO21/GPIO22 and only load one
  detected HD44780 backpack.
- Confirm glyph banks stay within eight slots and 0..31 row-byte bounds.
- Confirm `FR_DIAG_XBEE_BRIDGE_CLOSED 1` remains set.
- Confirm the live evidence packet has fresh COM6 identity, rollback backup,
  recovery command, staged hashes, write-flash, separate verify-flash,
  read-only monitor, transcript scan, cleanup proof, and no
  watchdog/backtrace/panic/LCD-init-failure or closed-surface markers.
- Confirm the read-only monitor evidence is interpreted narrowly: it captured
  all 13 page names and all five glyph banks via auto-demo, but it captured zero
  `ENC_RAW`, zero `ENC_EV`, zero `BBS_MENU_STEP`, and zero `BBS_MENU_SELECT`.

## Live Evidence

- Evidence directory:
  `research/bench-records/xbee-readonly/local-ky040-pf0530l-bbs-lcd-menu-ux-live-20260531T141121Z/`
- Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530L-LIVE-2026-05-31`
- Rollback backup SHA256:
  `82c99ba16940144f1a3eac1fdceb767f9208c5c9aff76e30623ab44ed08a230f`
- Monitor scan summary: `writes_sent=false`, `LCD_INIT_OK`, one
  `PF0530L BBS_LCD_READY`, one `BBS_INPUT_READY`, six `BBS_GLYPH_BANK`, 77
  `BBS_CURSOR`, 77 `BBS_LCD_RENDER`, 21 `BBS_MENU_AUTO`, and 74 `BBS_MENU_HB`
  lines; no fault or unsafe-open markers.

## Closed Surfaces

- No XBee/RF transmit or configuration writes.
- No ESP-NOW runtime.
- No firmware HTTP, SoftAP, WebSocket, or persistent configuration endpoint.
- No relay GPIO or relay-expander writes.
- No MicroSD/TFT action.
- No wiring, load, mains, erase, commit, or push.
