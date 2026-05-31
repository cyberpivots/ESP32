# Four Relay KY-040 BBS LCD Menu PF0530J

## Routing

- Selected tier: Tier 2 source/test/docs implementation, followed by a Tier 3
  COM6 live gate only after validation.
- Owner role: Lead LCD Menu Developer with Firmware, QA, Live Bench,
  Hardware-risk, Evidence Records, and Governance lenses.
- Evidence need: PF0530I blocker transcript, decoded backtrace, source diff,
  firmware scaffold tests/audits, no-flash ESP-IDF build, source records, and
  later private COM6 identity/backup/flash/verify/monitor evidence if live gate
  proceeds.
- Mutation boundary: PF0530J firmware source, firmware tests/audits,
  firmware/project documentation, source-index/source-ledger, this task log,
  QA handoff, and private PF0530J bench evidence.
- Gate authority: user authorized live flashing and stated hardware safe state
  in-session. Live action still requires fresh COM6 identity, rollback backup,
  recovery command, staged hashes, write/verify logs, read-only monitor, and
  weighted reviewer quorum.

## Verified Facts

- PF0530I write-flash and verify-flash passed, but its first read-only monitor
  emitted repeated task-watchdog backtrace lines.
- Decoding PF0530I backtrace addresses against the PF0530I ELF mapped the
  runtime warning to `fr_menu_input_task`, `fr_menu_poll`, GPIO reads, and
  ESP-IDF task-watchdog handling.
- PF0530J source now uses firmware ID `PF0530J`, keeps the split input task and
  dirty-row LCD renderer, changes `FR_MENU_POLL_MS` to 10, and adds
  `fr_delay_ticks_at_least_one()` for the input/render task delays.
- PF0530J keeps `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, keeps GPIO13/GPIO14/GPIO32
  input-only with internal pullups, and keeps LCD writes display-only on
  GPIO21/GPIO22.

## Assumptions

- The PF0530I task-watchdog blocker is caused by the higher-priority input task
  yielding with a zero-tick delay at the current FreeRTOS tick rate.
- COM6 remains the intended live target only if a fresh esptool identity check
  matches the previous ESP32-D0WDQ6, 4 MB, MAC `78:e3:6d:0a:90:14` evidence.

## Unknowns

- Current PF0530J COM6 identity, physical LCD visual state, encoder rotation
  direction, `BBS_MENU_STEP`, `BBS_MENU_SELECT`, boot-held switch behavior,
  rail margin, LCD backpack pullup voltage, and user acceptance are unresolved
  until post-fix live proof.

## Validation

- Focused firmware boundary test, firmware/docs/source/scaffold audits,
  custom wireless protocol tests, LCD BBS menu renderer tests, four-relay
  safe-core host tests, `verify_scaffold.py`, `git diff --check`, and
  ESP-IDF v6.0.1 no-flash build passed before the PF0530J live gate.

## Live Gate Status

- PF0530J COM6 identity matched ESP32 MAC `78:e3:6d:0a:90:14`, 4 MB flash,
  and 3.3 V flash voltage.
- PF0530J rollback backup, staged artifact hashes, write-flash, and separate
  verify-flash completed successfully.
- PF0530J read-only monitor captured `PF0530J BBS_LCD_READY`,
  `BBS_INPUT_READY`, two `BBS_LCD_RENDER` lines, and 44 `BBS_MENU_HB` lines
  with no task-watchdog, backtrace, panic, guru-meditation, or LCD-init-fail
  markers.
- The same monitor captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, and zero `BBS_MENU_SELECT` lines. PF0530J is therefore not
  accepted as a fully proven interactive encoder/button menu and is superseded
  by PF0530K source work.

## Decision Footer

- Decision: source mutation ready for validation.
- Next gate: host/scaffold tests, ESP-IDF v6.0.1 no-flash build, then
  same-session COM6 flash/verify/read-only monitor if validation passes.
- Owner: Lead LCD Menu Developer.
- Evidence: PF0530E/PF0530G/PF0530H/PF0530I records, decoded PF0530I
  backtrace, PF0530J source diff, and validation results above.
- Approved mutation boundary: PF0530J source/tests/docs/records, then a
  COM6-only PF0530J flash/verify/read-only-monitor gate after validation.
- Authority limits: no XBee/RF, ESP-NOW runtime, relay, relay-expander,
  MicroSD/TFT, wiring, load, mains, erase, commit, or push.
