# Four Relay KY-040 BBS LCD Menu PF0530K

## Routing

- Selected tier: Tier 2 source/test/docs implementation, followed by a Tier 3
  COM6 live gate only after validation.
- Owner role: Lead LCD Menu Developer with Firmware, QA, Live Bench,
  Hardware-risk, Evidence Records, and Governance lenses.
- Evidence need: PF0530J monitor transcript, source diff, firmware scaffold
  tests/audits, no-flash ESP-IDF build, source records, and later private COM6
  identity/backup/flash/verify/monitor evidence if live gate proceeds.
- Mutation boundary: PF0530K firmware source, firmware tests/audits,
  firmware/project documentation, source-index/source-ledger, this task log,
  QA handoff, and private PF0530K bench evidence.
- Gate authority: user authorized live flashing and stated hardware safe state
  in-session. Live action still requires fresh COM6 identity, rollback backup,
  recovery command, staged hashes, write/verify logs, read-only monitor, and
  weighted reviewer quorum.

## Verified Facts

- PF0530J was written and separately verify-flashed to COM6.
- PF0530J monitor evidence showed `PF0530J BBS_LCD_READY`,
  `BBS_INPUT_READY`, two `BBS_LCD_RENDER` lines, and 44 `BBS_MENU_HB` lines
  with no task-watchdog, backtrace, panic, guru-meditation, or LCD-init-fail
  markers.
- The same PF0530J monitor captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, and zero `BBS_MENU_SELECT` lines, so it did not prove the
  interactive encoder/button path.
- PF0530K source now uses firmware ID `PF0530K`, keeps the PF0530J watchdog
  fix, adds GPIO any-edge interrupt queueing for GPIO13/GPIO14/GPIO32, and
  decodes rotation from raw A/B transitions.
- PF0530K keeps `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, keeps GPIO13/GPIO14/GPIO32
  input-only with internal pullups, and keeps LCD writes display-only on
  GPIO21/GPIO22.

## Assumptions

- The PF0530J no-input transcript may reflect missing physical actuation during
  the monitor, but the open user symptom still warrants a more robust edge
  capture path.
- COM6 remains the intended live target only if a fresh esptool identity check
  matches the previous ESP32-D0WDQ6, 4 MB, MAC `78:e3:6d:0a:90:14` evidence.

## Unknowns

- Current PF0530K COM6 identity, physical LCD visual state, encoder rotation
  direction, `BBS_MENU_STEP`, `BBS_MENU_SELECT`, boot-held switch behavior,
  rail margin, LCD backpack pullup voltage, and user acceptance are unresolved
  until post-fix live proof.

## Validation

- Focused firmware boundary test, firmware/docs/source/scaffold audits,
  custom wireless protocol tests, LCD BBS menu renderer tests, four-relay
  safe-core host tests, full scaffold audit discovery, agent-process audit,
  `verify_scaffold.py`, `git diff --check`, and ESP-IDF v6.0.1 no-flash build
  passed before the PF0530K live gate.
- ESP-IDF v6.0.1 no-flash build produced app size `0x2aa80` with `0xd5580`
  bytes free in the 1 MiB factory app partition.

## Live Gate Status

- PF0530K COM6 identity matched ESP32 MAC `78:e3:6d:0a:90:14`, 4 MB flash,
  and 3.3 V flash voltage.
- PF0530K rollback backup, staged artifact hashes, write-flash, and separate
  verify-flash completed successfully.
- PF0530K read-only monitor captured `PF0530K BBS_LCD_READY`,
  `BBS_INPUT_READY`, `irq=anyedge queue=64`, two `BBS_LCD_RENDER` lines, and
  59 `BBS_MENU_HB` lines with no task-watchdog, backtrace, panic,
  guru-meditation, or LCD-init-fail markers.
- The same monitor captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, and zero `BBS_MENU_SELECT` lines. PF0530K is flashed for
  user testing, but live encoder/button acceptance remains blocked until a
  monitor captures physical actuation reaching GPIO13/GPIO14/GPIO32.

## Decision Footer

- Decision: source mutation ready for validation.
- Next gate: host/scaffold tests, ESP-IDF v6.0.1 no-flash build, then
  same-session COM6 flash/verify/read-only monitor if validation passes.
- Owner: Lead LCD Menu Developer.
- Evidence: PF0530E/PF0530G/PF0530H/PF0530I/PF0530J records, PF0530J live
  transcript, PF0530K source diff, and validation results above.
- Approved mutation boundary: PF0530K source/tests/docs/records, then a
  COM6-only PF0530K flash/verify/read-only-monitor gate after validation.
- Authority limits: no XBee/RF, ESP-NOW runtime, relay, relay-expander,
  MicroSD/TFT, wiring, load, mains, erase, commit, or push.
