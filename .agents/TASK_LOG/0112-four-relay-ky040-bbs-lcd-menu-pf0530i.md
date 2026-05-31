# Four Relay KY-040 BBS LCD Menu PF0530I

## Routing

- Selected tier: Tier 2 source/test/docs implementation, followed by a Tier 3
  COM6 live gate only after validation.
- Owner role: Lead LCD Menu Developer with Firmware, QA, Live Bench,
  Hardware-risk, Evidence Records, and Governance lenses.
- Evidence need: reviewer quorum, source diff, firmware scaffold tests/audits,
  no-flash ESP-IDF build, source-index/source-ledger records, and later private
  COM6 identity/backup/flash/verify/monitor evidence if live gate proceeds.
- Mutation boundary: PF0530I firmware source, firmware tests/audits,
  firmware/project documentation, source-index/source-ledger, this task log,
  QA handoff, and private PF0530I bench evidence.
- Gate authority: user authorized live flashing and stated hardware safe state
  in-session. Live action still requires fresh COM6 identity, rollback backup,
  recovery command, staged hashes, write/verify logs, read-only monitor, and
  weighted reviewer quorum.

## Verified Facts

- PF0530H COM6 live proof captured `LCD_INIT_OK addr=0x27`,
  `PF0530H BBS_LCD_READY`, three `BBS_LCD_RENDER`, and three `BBS_MENU_HB`
  lines, but no `BBS_MENU_STEP` or `BBS_MENU_SELECT` proof.
- PF0530H transcript timing showed full LCD render/heartbeat intervals near
  15 seconds, while the source had input polling and LCD rendering in the same
  task.
- PF0530E r5 previously proved GPIO13/GPIO14/GPIO32 transitions during
  user-confirmed encoder and button actuation.
- Read-only reviewer quorum approved a bounded source fix and denied accepting
  PF0530H as an interactive menu.
- PF0530I source now uses firmware ID `PF0530I`, starts
  `fr_lcd_bbs_menu_task`, keeps `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, keeps
  GPIO13/GPIO14/GPIO32 input-only with internal pullups, and keeps LCD writes
  display-only on GPIO21/GPIO22.
- PF0530I splits input polling into `fr_menu_input_task`, renders only dirty
  rows or a slow idle refresh, adds `BBS_INPUT_READY`, adds `ENC_RAW`, and
  records `BBS_LCD_RENDER` row count, sequence, duration, and reason fields.

## Assumptions

- The PF0530H no-effect symptom is primarily LCD-render starvation of input
  polling, not a new wiring failure.
- COM6 remains the intended live target only if a fresh esptool identity check
  matches the previous ESP32-D0WDQ6, 4 MB, MAC `78:e3:6d:0a:90:14` evidence.

## Unknowns

- Current COM6 identity, physical LCD visual state, encoder rotation
  direction, `BBS_MENU_STEP`, `BBS_MENU_SELECT`, boot-held switch behavior,
  rail margin, LCD backpack pullup voltage, and user acceptance are
  unresolved until post-fix live proof.

## Validation

- Pending after source mutation.

## Live Gate Status

- Attempted and blocked. PF0530I write-flash and separate verify-flash passed,
  but the read-only monitor emitted repeated task-watchdog `Backtrace:` lines.
  Address decoding mapped the blocker to the higher-priority input task using a
  zero-tick poll delay. PF0530J supersedes PF0530I.

## Decision Footer

- Decision: superseded by PF0530J.
- Next gate: PF0530J validation and same-session COM6 flash/verify/read-only
  monitor if validation passes.
- Owner: Lead LCD Menu Developer.
- Evidence: PF0530E/PF0530G/PF0530H records, reviewer quorum, PF0530I source
  diff, and validation results above.
- Approved mutation boundary: PF0530I source/tests/docs/records, then a
  COM6-only PF0530I flash/verify/read-only-monitor gate after validation.
- Authority limits: no XBee/RF, ESP-NOW runtime, relay, relay-expander,
  MicroSD/TFT, wiring, load, mains, erase, commit, or push.
