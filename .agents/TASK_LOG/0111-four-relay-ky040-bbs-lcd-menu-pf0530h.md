# Four Relay KY-040 BBS LCD Menu PF0530H

## Routing

- Selected tier: Tier 2 source/test/docs implementation, followed by a Tier 3
  live COM6 gate only after validation.
- Owner role: Firmware lead with QA, Evidence Records, Live Bench, and
  Governance lenses.
- Evidence need: source diff, firmware scaffold tests/audits, no-flash
  ESP-IDF build, source-index/source-ledger records, and later private COM6
  identity/backup/flash/verify/monitor evidence if live gate proceeds.
- Mutation boundary: PF0530H firmware source, firmware tests/audits,
  firmware/project documentation, source-index/source-ledger, this task log,
  QA handoff, and private PF0530H bench evidence.
- Gate authority: user authorized live flashing and stated hardware safe state
  in-session. Live action still requires fresh COM6 identity, rollback backup,
  recovery command, staged hashes, write/verify logs, read-only monitor, and
  weighted reviewer quorum.

## Verified Facts

- PF0530F COM6 write/verify passed but menu acceptance blocked on
  `PF0530F LCD_INIT_FAILED`.
- PF0530G COM6 LCD init diagnostic passed serially at address `0x27`.
- PF0530H source now uses firmware ID `PF0530H`, starts
  `fr_lcd_bbs_menu_task`, keeps `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, and combines
  PF0530G LCD init/probe proof with PF0530F input-only GPIO13/GPIO14/GPIO32
  encoder handling.
- PF0530H renders nine static/simulated BBS LCD pages and emits
  `PF0530H BBS_LCD_READY`, `BBS_LCD_RENDER`, `BBS_MENU_HB`,
  `BBS_MENU_STEP`, and `BBS_MENU_SELECT` proof lines.
- PF0530H COM6 live gate passed staged flash readiness, write-flash, separate
  verify-flash, and read-only UART0 monitor. The transcript captured
  `LCD_INIT_OK addr=0x27`, `PF0530H BBS_LCD_READY`, three `BBS_LCD_RENDER`,
  three `BBS_MENU_HB`, `writes_sent=false`, zero LCD init failures, zero
  crash/fault markers, and zero closed-surface violation markers.

## Assumptions

- PF0530H BBS pages are local display/menu proof content only.
- COM6 remains the intended live target only if a fresh esptool identity check
  matches the previous ESP32-D0WDQ6, 4 MB, MAC `78:e3:6d:0a:90:14` evidence.

## Unknowns

- Current COM6 identity, physical LCD visual state, encoder rotation direction,
- Physical LCD visual state, encoder rotation direction, `BBS_MENU_STEP`,
  `BBS_MENU_SELECT`, boot-held switch behavior, rail margin, LCD backpack
  pullup voltage, and user acceptance are unresolved.

## Validation

- Passed after source mutation:
  - `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
    - 10 tests OK.
  - `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
    - 32 tests OK.
  - `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
    - split host tests passed.
  - `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
    - passed.
  - `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
    - passed.
  - `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
    - passed.
  - `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
    - `PASS: ESP32 agent-process audit succeeded`.
  - `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
    - 49 tests OK.
  - `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
    - `PASS: ESP32 scaffold validation succeeded`.
  - `git diff --check`
    - passed.
  - ESP-IDF v6.0.1 no-flash build for
    `firmware/projects/four-relay-xbee-wifi`.
    - passed via `/tmp/esp32-four-relay-xbee-wifi-pf0530h-bbs-menu-build2`.
    - `four_relay_xbee_wifi.bin` size `0x29f20`, app partition `0x100000`,
      `0xd60e0` bytes free.

## Live Gate Status

- Completed for user testing. Evidence directory:
  `research/bench-records/xbee-readonly/local-ky040-pf0530h-bbs-lcd-menu-live-20260531T020501Z/`.
- Fresh COM6 identity matched ESP32-D0WDQ6 MAC `78:e3:6d:0a:90:14` with
  detected 4 MB flash.
- Rollback backup SHA256:
  `50f9d149d73ea2453bcd6abfd75cb7e829ed30f37bc511cec91a83a88f5dced4`.
- Staged artifacts hash check passed; write-flash and separate verify-flash
  passed; read-only monitor and transcript scan passed
  `acceptance=ready_for_user_testing`.

## Decision Footer

- Decision: PF0530H is flashed and ready for user LCD/encoder testing.
- Next gate: user visual confirmation and encoder/pushbutton actions.
- Owner: Firmware lead.
- Evidence: PF0530F/PF0530G records, PF0530H source diff, validations above,
  ESP-IDF v6.0.1 no-flash build, and PF0530H live evidence packet.
- Approved mutation boundary: completed COM6-only PF0530H flash/verify and
  read-only monitor. User testing is now the remaining acceptance gate.
- Authority limits: no XBee/RF, ESP-NOW runtime, relay, relay-expander,
  MicroSD/TFT, wiring, load, mains, erase, commit, or push.
