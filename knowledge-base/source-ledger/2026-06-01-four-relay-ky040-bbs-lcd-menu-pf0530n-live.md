# Four Relay KY-040 BBS LCD Menu PF0530N Live Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530N-LIVE-2026-06-01`

## Verified Facts

- The user requested live COM6 flashing for PF0530N and confirmed safe state.
- PF0530N source validation had already recorded the build-time XML/generated
  static menu model, `bbs_lcd_render.v2`, scroll-list navigation, grouped
  multi-row items, selected-row marquee timing, table glyph bank constraints,
  bridge-closed boundary, input-only GPIO13/GPIO14/GPIO32, and display-only
  GPIO21/GPIO22.
- Same-session reviewer quorum conditionally approved the named COM6-only gate
  after fresh identity, rollback backup, pinned artifacts, write-flash,
  separate verify-flash, read-only scan, cleanup, and records. Weighted
  disposition was 14/14.
- Fresh COM6 identity matched ESP32-D0WDQ6 revision v1.0, detected 4 MB flash,
  and detected 3.3 V flash strap. The raw MAC is retained only in ignored local
  evidence and is redacted from this publishable ledger.
- Full 4 MB rollback backup was captured before write. The exact local path and
  SHA256 are retained only in ignored local evidence and are redacted from this
  publishable ledger.
- Staged PF0530N bootloader, partition table, and app hashes were recorded in
  ignored local evidence and are redacted from this publishable ledger.
- COM6 write-flash passed and esptool verified each written segment.
- Separate COM6 verify-flash passed with digest matches for bootloader,
  partition table, and app.
- The 120 second read-only monitor used `writes_sent=false` and captured one
  `PF0530N BBS_LCD_READY`, one `PF0530N BBS_INPUT_READY`, 61
  `BBS_LCD_RENDER`, 61 `BBS_CURSOR`, 59 `BBS_MENU_HB`, 17
  `BBS_MENU_AUTO`, seven `BBS_GLYPH_BANK`, one `bbs_lcd_menu.v1`, and one
  `bbs_lcd_render.v2`.
- Transcript scan captured zero `Guru Meditation`, `Backtrace`, `panic`,
  `watchdog`, `abort()`, `LCD_INIT_FAIL`, `UNSAFE_OPEN`, or `BRIDGE_OPEN`
  markers.
- Cleanup proof found no lingering Windows flash/monitor process after the
  run.

## Assumptions

- The user's same-session safe-state confirmation applied to this COM6-only
  PF0530N write/verify/read-only monitor gate.
- The project-generated `--flash-size 2MB` setting remains intentional for
  this ESP-IDF project; COM6 reports 4 MB physical flash and the rollback
  image covers the full detected size.
- Read-only serial boot evidence proves PF0530N runtime readiness only. It
  does not prove physical LCD readability or physical input actuation.

## Unknowns

- Physical readability of the scroll-list and table page remains unproven.
- Physical encoder direction and switch behavior under PF0530N remain
  unproven; the passive transcript captured zero `ENC_RAW`, zero `ENC_EV`,
  zero `BBS_MENU_STEP`, and zero `BBS_MENU_SELECT`.
- Final BBS/XBee payload mapping, relay/load/mains readiness, and deployment
  acceptance remain future gates.

## Evidence

Evidence directory: ignored local PF0530N live evidence directory; exact path
redacted from this publishable ledger.

Key files:

- `pf0530n-live-manifest.txt`
- `pf0530n-artifact-sha256.txt`
- `com6-esptool-chip-id.txt`
- `com6-esptool-read-mac.txt`
- `com6-esptool-flash-id.txt`
- `com6-pre-pf0530n-scrolling-xml-4mb.bin`
- `com6-pre-pf0530n-read-flash-sha256.txt`
- `pf0530n-recovery-command.txt`
- `com6-pf0530n-write-flash.txt`
- `com6-pf0530n-verify-flash.txt`
- `com6-pf0530n-readonly-monitor-120s.txt`
- `pf0530n-transcript-scan.txt`
- `pf0530n-cleanup-summary.txt`

## Authority Limits

This record does not authorize or prove XBee/RF writes or tests, ESP-NOW
runtime, relay GPIO writes, relay-expander writes, MicroSD/TFT action, wiring
mutation, DMM/current measurement, relay/load/mains work, erase, firmware
HTTP/SoftAP/WebSocket runtime, persistent configuration, external service
changes, commit, or push.
