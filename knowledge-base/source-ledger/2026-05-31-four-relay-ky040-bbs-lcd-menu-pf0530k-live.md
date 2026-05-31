# Four Relay KY-040 BBS LCD Menu PF0530K Live Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530K-LIVE-2026-05-31`

## Verified Facts

- PF0530K host/scaffold validation and ESP-IDF v6.0.1 no-flash build passed
  before live mutation.
- Fresh COM6 identity matched ESP32 MAC `78:e3:6d:0a:90:14`, 4 MB flash, and
  3.3 V flash voltage.
- A full 4 MB rollback backup was captured before PF0530K write-flash:
  SHA256 `66e2a65cc10ed285d2adbb873828fa8091f5bfc2d61281c3ddc6ae35aeea3674`.
- Staged PF0530K artifacts were hashed:
  bootloader `2a0c5e0eca31aff5cb1b432a37ba62d923c0fb50db473c5056ad8b7c29ac23be`,
  app `4f15a31e4e812d334eab71fdb761ebde2e201ecc449553ff3b072c08a71813b3`,
  partition table
  `7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820`.
- PF0530K write-flash and separate verify-flash succeeded for bootloader,
  partition table, and app.
- The read-only monitor transcript recorded `writes_sent=false`,
  `PF0530K BBS_LCD_READY`, `BBS_INPUT_READY`, `irq=anyedge queue=64`, two
  `BBS_LCD_RENDER` lines, and 59 `BBS_MENU_HB` lines.
- Transcript scan found zero `Backtrace`, `Task watchdog`, `Guru Meditation`,
  `panic`, and `LCD_INIT_FAIL` lines.
- Transcript scan found zero `ENC_RAW`, zero `ENC_EV`, zero `BBS_MENU_STEP`,
  and zero `BBS_MENU_SELECT` lines.

## Result

- PF0530K is flashed and separately verify-flashed on COM6 for user testing.
- PF0530K is not accepted as proven interactive because the read-only monitor
  did not capture physical encoder/button input reaching GPIO13/GPIO14/GPIO32.
- If the controls were physically actuated during the monitor window, the
  evidence points away from LCD-render starvation and toward a physical
  signal/wiring/contact path that did not change the ESP32 input levels.

## Evidence Directory

`research/bench-records/xbee-readonly/local-ky040-pf0530k-bbs-lcd-menu-interrupt-input-live-20260531T031559Z/`

## Authority Limits

- No relay GPIO writes.
- No relay-expander writes.
- No XBee setting writes, XBee/RF, range, throughput, or API transmit frames.
- No MicroSD or TFT action.
- No relay/load/mains action.
- No erase, wiring mutation, commit, or push.
