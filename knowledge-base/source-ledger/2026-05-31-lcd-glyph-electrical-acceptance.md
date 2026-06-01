# LCD Glyph And Electrical Acceptance Ledger

Source ID:
`SRC-LOCAL-LCD-GLYPH-ELECTRICAL-ACCEPTANCE-2026-05-31`

## Verified Facts

- The gate ran after a Tier 3 reviewer quorum conditionally approved only the
  read-only COM6 identity/monitor, user visual observation, and DMM measurement
  boundary.
- The previous PF0530L rollback image remained present at
  `<redacted-local-evidence-path>`,
  size 4,194,304 bytes, SHA256
  `<redacted-sha256>`.
- Same-session COM6 read-only identity passed for `chip_id`, `read_mac`, and
  `flash_id`: ESP32-D0WDQ6 revision v1.0, MAC `<redacted-mac>`, 4 MB
  flash, and 3.3 V flash strap.
- The first 150 second read-only monitor used `writes_sent=false`, captured
  PF0530L LCD readiness, one glyph-bank marker, cursor/render/heartbeat proof,
  1,834 `ENC_RAW`, 986 `ENC_EV`, 28 `BBS_MENU_STEP`, and 10
  `BBS_MENU_SELECT` lines with both step directions and short/long
  selections.
- The first monitor found zero watchdog, backtrace, panic, `Guru Meditation`,
  `LCD_INIT_FAILED`, `unsafe-open`, `UNSAFE_OPEN`, or
  `FR_DIAG_XBEE_BRIDGE_OPEN` markers.
- The first monitor did not provide full page/glyph-bank coverage because
  interaction kept the observed page set narrow.
- A second read-only reset/identity command was followed by a 150 second
  auto-demo monitor. It captured `LCD_INIT_FAIL stage=probe detail=scan-error`
  and repeated `LCD_DIAG_HB status=fail` lines, with no BBS LCD readiness or
  render/glyph proof.
- The user subsequently reported the LCD is run through a bi-directional logic
  level converter, LCD-side `VCC`, `SDA`, and `SCL` all read 4.73 V, and the
  LCD is visibly alive.
- The user reported the encoder `+`, `CLK` idle, `DT` idle, and `SW` idle are
  all 3.3 V, with affirmative responses to the drop-low/press-low prompts.
- The user then reported ESP32-side/LV-side `SDA` and `SCL` are both 3.3 V,
  clearing the 5 V I2C-to-ESP32 stop gate for one read-only monitor retry.
- A post-LV-side read-only `read_mac` reset/identity command completed on COM6
  and again reported ESP32-D0WDQ6 revision v1.0 with MAC
  `<redacted-mac>`.
- The post-LV-side 150 second read-only monitor used `writes_sent=false` and
  captured `LCD_INIT_OK`, `PF0530L BBS_LCD_READY`,
  `PF0530L BBS_INPUT_READY`, 77 `BBS_LCD_RENDER`, 77 `BBS_CURSOR`, six
  `BBS_GLYPH_BANK`, 21 `BBS_MENU_AUTO`, 74 `BBS_MENU_HB`, all 13 expected
  page names, all five expected glyph-bank names, and zero watchdog,
  backtrace, panic, `Guru Meditation`, `LCD_INIT_FAILED`, `LCD_INIT_FAIL`,
  `unsafe-open`, `UNSAFE_OPEN`, or `FR_DIAG_XBEE_BRIDGE_OPEN` markers.
- The post-LV-side monitor captured no manual encoder/button events, so it
  proves post-reset LCD/menu readiness and auto-demo coverage but relies on
  the earlier attended proof for physical serial/menu interaction.
- The user then confirmed full visual readability: four rows, visible page
  changes, and readable custom glyph/widget pages all pass.
- The user then confirmed all remaining DMM continuity, KY-040 toggle, and
  current-margin checks are good and no further DMM checks are required for
  this gate.
- Cleanup scans found no lingering WSL monitor/esptool/idf.py process after
  the monitor windows.

## Assumptions

- The first monitor's encoder/button lines reflect physical bench interaction.
- The second monitor's LCD probe failure reflected a real stop-gate symptom
  during that capture, but the later LV-side voltage check and read-only retry
  show the current serial LCD readiness path can recover without firmware
  mutation.
- Final DMM confirmation is recorded as operator pass/fail confirmation without
  numeric current values.

## Unknowns

- The cause of the post-reset LCD probe failure remains unresolved.
- Numeric current values were not retained in the final DMM confirmation.
- Relay/load/mains, XBee/RF expansion, future flash, serial writes,
  wiring-under-power, deployment readiness, and publication remain outside this
  gate.

## Evidence

- Evidence directory:
  `<redacted-local-evidence-dir>/`
- User-reported physical readings:
  `<redacted-local-evidence-dir>/user-reported-lcd-dmm-readings.md`
- Post-LV-side monitor scan:
  `<redacted-local-evidence-dir>/pf0530l-after-lv-i2c-transcript-scan.txt`
- User-reported LCD visual confirmation:
  `<redacted-local-evidence-dir>/user-reported-lcd-visual-confirmation.md`
- User-reported final DMM confirmation:
  `<redacted-local-evidence-dir>/user-reported-dmm-final-confirmation.md`
- Task record:
  `.agents/TASK_LOG/0122-lcd-glyph-electrical-acceptance.md`
- Hardware QA handoff:
  `.agents/handoffs/0089-lcd-glyph-electrical-acceptance-to-hardware-qa.md`
- Source IDs preserved:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530L-2026-05-31`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530L-LIVE-2026-05-31`,
  and `SRC-LOCAL-TIER3-COM6-ATTENDED-INTERACTION-PROOF-2026-05-31`.

## Authority Limits

This record accepts LCD visual/glyph readability, measured 3.3 V low-side I2C
domain, measured 3.3 V KY-040 idle domain, LCD high-side 4.73 V through the
reported bi-directional level converter, read-only serial LCD/menu readiness/
page/glyph proof, and operator-confirmed continuity/toggle/current-margin pass
above. It does not accept relay/load/mains, XBee/RF expansion, future flash,
erase, serial writes, wiring-under-power, persistent config, credentials,
external services, GitHub publication, release, commit, or push.
