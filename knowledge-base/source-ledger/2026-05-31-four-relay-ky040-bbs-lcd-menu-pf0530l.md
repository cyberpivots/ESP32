# Four Relay KY-040 BBS LCD Menu PF0530L Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530L-2026-05-31`

## Verified Facts

- PF0530K write-flash and separate verify-flash passed on COM6, and its
  read-only monitor showed `PF0530K BBS_LCD_READY`, `BBS_INPUT_READY`,
  `irq=anyedge queue=64`, two `BBS_LCD_RENDER`, and 59 `BBS_MENU_HB` lines
  with no watchdog/backtrace/panic/LCD-init-failure markers.
- The PF0530K monitor captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, and zero `BBS_MENU_SELECT`, so PF0530K was flashed for user
  testing but not accepted as proven interactive.
- PF0530L changes the active firmware ID to `PF0530L`, keeps
  `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, keeps the PF0530K GPIO any-edge queue for
  GPIO13/GPIO14/GPIO32, and keeps LCD writes display-only on GPIO21/GPIO22.
- PF0530L adds local menu modes `page_browse`, `row_browse`, `detail`, and
  `edit_lab`; software cursor/DDRAM metadata; dirty-cell render metadata; five
  named HD44780 glyph banks; custom bar/chart/digit/gauge demo pages; and a
  seven-second auto-demo page cycle.
- PF0530L emits source-visible UART0 proof strings `PF0530L BBS_LCD_READY`,
  `BBS_INPUT_READY`, `BBS_GLYPH_BANK`, `BBS_CURSOR`, `BBS_LCD_RENDER`,
  `BBS_MENU_AUTO`, `BBS_MENU_HB`, `ENC_RAW`, `ENC_EV`, `BBS_MENU_STEP`, and
  `BBS_MENU_SELECT`.
- The separate live source ledger
  `knowledge-base/source-ledger/2026-05-31-four-relay-ky040-bbs-lcd-menu-pf0530l-live.md`
  records the same-session COM6 identity, rollback backup, write-flash,
  verify-flash, read-only monitor, transcript scan, and cleanup proof.

## Assumptions

- The PF0530L auto-demo path is a local display proof surface only; it does not
  prove encoder direction, switch behavior, or physical LCD readability.
- The custom glyph banks use the HD44780 eight-slot CGRAM budget and are kept
  to a 250 ms minimum bank-swap interval.
- Browser mirror and glyph/widget planning records remain design inputs only;
  PF0530L does not open firmware HTTP, SoftAP, WebSocket, persistent
  configuration, or network gates.

## Unknowns

- Physical LCD readability, custom glyph appearance, encoder direction,
  `ENC_RAW`, `ENC_EV`, `BBS_MENU_STEP`, `BBS_MENU_SELECT`, boot-held switch
  behavior, rail margin, and LCD backpack pullup voltage remain unproven until
  attended physical testing captures interaction evidence.

## Validation

- Source mutation updates `firmware/projects/four-relay-xbee-wifi/main/main.c`,
  firmware scaffold audits, the encoder pullup boundary test, firmware/project
  documentation, ESP-NOW LCD menu plans, this source ledger, source index, docs
  index, task log, and QA handoff.
- Focused firmware scaffold validation and ESP-IDF v6.0.1 no-flash build
  results are recorded in
  `.agents/TASK_LOG/0118-four-relay-ky040-bbs-lcd-menu-pf0530l.md`.

## Authority Limits

- This source record does not by itself prove physical interaction, serial
  writes beyond the named flash/verify gate, XBee/RF, ESP-NOW runtime, relay
  GPIO writes, relay-expander writes, MicroSD/TFT action, wiring mutation, load,
  mains, erase, commit, or push.
