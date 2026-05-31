# Four Relay KY-040 BBS LCD Menu PF0530L Live Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530L-LIVE-2026-05-31`

## Verified Facts

- PF0530L source validation passed host LCD menu tests, custom wireless
  protocol tests, four-relay safe-core host tests, scaffold audits,
  `verify_scaffold.py`, `git diff --check`, and an ESP-IDF v6.0.1 no-flash
  build. The staged app image size was `0x2ba60`.
- Same-session COM6 identity matched ESP32-D0WDQ6 MAC `78:e3:6d:0a:90:14`,
  detected 4 MB flash, and detected the flash voltage strap at 3.3 V.
- A full 4 MB rollback image was saved at
  `research/bench-records/xbee-readonly/local-ky040-pf0530l-bbs-lcd-menu-ux-live-20260531T141121Z/com6-pre-pf0530l-bbs-lcd-menu-4mb.bin`
  with SHA256
  `82c99ba16940144f1a3eac1fdceb767f9208c5c9aff76e30623ab44ed08a230f`.
- Staged PF0530L artifact hashes were recorded:
  bootloader `53981f7105431369842b9bb572680decff343f13022eb045ff2d9f70cba99e0d`,
  partition table
  `7f00b6c042a89b15b0cac534f82ed988caf29278ff5700b0c511eb1b5bb7c820`,
  and app
  `058c0e49abfc582bc3920e894a9d5e1df05c9d5deb4aba1db7bafdb2fbd0a947`.
- PF0530L write-flash on COM6 passed, and the separate verify-flash pass
  reported digest matches for bootloader, partition table, and app.
- The read-only monitor transcript used `writes_sent=false` and captured
  `LCD_INIT_OK`, one `PF0530L BBS_LCD_READY`, one `BBS_INPUT_READY`, six
  `BBS_GLYPH_BANK`, 77 `BBS_CURSOR`, 77 `BBS_LCD_RENDER`, 21
  `BBS_MENU_AUTO`, and 74 `BBS_MENU_HB` lines.
- The monitor scan captured auto-demo coverage for all 13 PF0530L page names
  and all five glyph banks: `core_status`, `horizontal_bar`, `vertical_chart`,
  `big_digits`, and `gauge_demo`.
- The monitor scan found no watchdog, backtrace, panic, LCD-init-failure, or
  unsafe-open markers.
- Cleanup proof found no remaining WSL monitor/esptool/idf.py monitor process
  and no Windows Python monitor process.

## Assumptions

- The live gate covered COM6-only identity, backup, write-flash, verify-flash,
  and read-only monitoring under the user's same-session live authorization.
- The captured auto-demo page/glyph coverage makes PF0530L available for user
  visual testing, but it does not prove physical knob or switch behavior.

## Unknowns

- Physical LCD readability, custom glyph appearance on the actual display,
  encoder direction, switch behavior, `ENC_RAW`, `ENC_EV`, `BBS_MENU_STEP`,
  `BBS_MENU_SELECT`, boot-held switch behavior, rail margin, and LCD backpack
  pullup voltage remain unproven until physical user testing or an attended
  monitor captures interaction proof.

## Evidence

- Evidence directory:
  `research/bench-records/xbee-readonly/local-ky040-pf0530l-bbs-lcd-menu-ux-live-20260531T141121Z/`
- Live manifest:
  `research/bench-records/xbee-readonly/local-ky040-pf0530l-bbs-lcd-menu-ux-live-20260531T141121Z/pf0530l-live-manifest.txt`
- Transcript scan:
  `research/bench-records/xbee-readonly/local-ky040-pf0530l-bbs-lcd-menu-ux-live-20260531T141121Z/pf0530l-transcript-scan.txt`
- Recovery command:
  `research/bench-records/xbee-readonly/local-ky040-pf0530l-bbs-lcd-menu-ux-live-20260531T141121Z/pf0530l-recovery-command.txt`

## Authority Limits

- This live record does not authorize or prove XBee/RF transmit or
  configuration writes, ESP-NOW runtime, relay GPIO writes, relay-expander
  writes, MicroSD/TFT action, wiring mutation, load, mains, erase, firmware
  HTTP/SoftAP/WebSocket, persistent configuration endpoints, commit, or push.
