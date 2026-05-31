# Four Relay KY-040 BBS LCD Menu PF0530H Live Source Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530H-LIVE-2026-05-31`

## Verified Facts

- PF0530H source validation passed before live action: LCD menu tests,
  custom wireless protocol tests, four-relay safe-core host tests, scaffold
  audits, scaffold unittest discovery, `verify_scaffold.py`, `git diff
  --check`, and ESP-IDF v6.0.1 no-flash build.
- Weighted live-gate quorum approved conditional staged proceed with approved
  weight 18 of 18 and no P1/P2 blockers.
- Fresh COM6 identity matched ESP32-D0WDQ6, MAC `78:e3:6d:0a:90:14`,
  detected 4 MB flash, and reported the flash voltage strap as 3.3 V.
- A full 4 MB rollback backup was captured before write-flash:
  `research/bench-records/xbee-readonly/local-ky040-pf0530h-bbs-lcd-menu-live-20260531T020501Z/com6-pre-pf0530h-bbs-lcd-menu-4mb.bin`.
- Rollback backup SHA256:
  `50f9d149d73ea2453bcd6abfd75cb7e829ed30f37bc511cec91a83a88f5dced4`.
- PF0530H write-flash completed on COM6, and a separate verify-flash matched
  the staged bootloader, partition table, and app images.
- The read-only UART0 monitor transcript recorded `writes_sent=false`,
  `LCD_INIT_OK addr=0x27`, `PF0530H BBS_LCD_READY`, three
  `BBS_LCD_RENDER` lines, and three `BBS_MENU_HB` lines.
- The transcript scan recorded zero LCD init failures, zero crash/fault
  markers, and zero closed-surface violation markers.

## Assumptions

- The evidence directory remains private/local bench evidence.
- PF0530H is a local simulated BBS LCD/menu proof and not ESP-NOW runtime or
  full BBS bridge acceptance.

## Unknowns

- Physical LCD readability, page transitions from user rotation, encoder
  direction, `BBS_MENU_STEP`, `BBS_MENU_SELECT`, boot-held switch behavior,
  rail-current margin, and LCD backpack pullup voltage remain unverified.

## Evidence Packet

- Evidence directory:
  `research/bench-records/xbee-readonly/local-ky040-pf0530h-bbs-lcd-menu-live-20260531T020501Z/`
- Evidence manifest:
  `research/bench-records/xbee-readonly/local-ky040-pf0530h-bbs-lcd-menu-live-20260531T020501Z/evidence-manifest.md`
- Transcript scan:
  `research/bench-records/xbee-readonly/local-ky040-pf0530h-bbs-lcd-menu-live-20260531T020501Z/pf0530h-transcript-scan.txt`

## Validation

- COM6 identity: passed.
- Rollback backup: passed, 4,194,304 bytes.
- Staged artifact hash check: passed.
- Write-flash: passed.
- Separate verify-flash: passed.
- Read-only monitor: passed with `writes_sent=false`.
- Transcript scan: `acceptance=ready_for_user_testing`.

## Authority Limits

- This live record does not authorize or prove XBee/RF transmit, ESP-NOW
  runtime, relay GPIO writes, relay-expander writes, MicroSD/TFT action,
  wiring mutation, load, mains, erase, commit, or push.
- Physical LCD visual acceptance and encoder step/select acceptance remain
  user-test evidence items.
