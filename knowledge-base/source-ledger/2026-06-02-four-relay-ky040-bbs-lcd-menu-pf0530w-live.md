# Four Relay KY-040 BBS LCD Menu PF0530W Live Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-LIVE-2026-06-02`

Date: 2026-06-02

## Scope

COM6-only PF0530W live gate for the firmware-visible LCD visual-art menu image.
This record covers identity, rollback, write-flash, separate verify-flash,
reset/read-only monitor proof, transcript scan, cleanup scope, and the open
physical visual-acceptance gate for the ART page.

## Verified Facts

- User explicitly requested COM6 live flash with the LCD menu improvements
  applied and confirmed authority and safe state.
- The read-only reviewer quorum blocked immediate flash until Task 0141's
  host-only art compiler was made firmware-visible and source/build, COM6
  identity, rollback, hashes, write/verify, monitor, cleanup, and closed
  surfaces were proven.
- Source preflight passed: LCD menu generator `--check`, focused LCD tests,
  combined firmware/LCD unittest set, firmware/source/docs/agent audits,
  scaffold verification, custom wireless protocol tests, safe-core host tests,
  scaffold-audit discovery tests, `git diff --check`, and ESP-IDF v6.0.1
  no-flash build to `/tmp/esp32-pf0530w-visual-art-build`.
- COM6 inventory identified a Silicon Labs CP210x USB to UART Bridge on
  `COM6`.
- COM6 identified as ESP32-D0WDQ6 revision v1.0 with MAC
  `<redacted-mac>`.
- Flash ID reported manufacturer `5e`, device `4016`, detected flash size
  `4MB`, and 3.3 V flash-voltage strap.
- A fresh full rollback backup was captured before PF0530W write; its filename
  and SHA256 are retained only in ignored local evidence.
- PF0530W staged artifact hashes were pinned before programming and retained
  only in ignored local evidence.
- COM6 write-flash wrote only `0x1000`, `0x8000`, and `0x10000`; each region
  verified during the write.
- Separate parameter-matched `verify-flash` succeeded for bootloader,
  partition table, and app.
- Reset/read-only monitor showed `writes_sent=false`, `PF0530W`,
  `LCD_INIT_OK addr=0x27`, `PF0530W BBS_LCD_READY`, `PF0530W BBS_INPUT_READY`,
  `pages=15`, `items=65`, `glyph_banks=7`, `cal=pcnt-v1`, `decoder=pcnt`,
  `irq=pcnt`, `poll_decoder=0`, GPIO13/GPIO14/GPIO32 `ENC_GPIO_CONFIG`,
  `PF0530W ENC_PCNT_READY result=ok`, `ENC_LEVEL_HB`, `ENC_PCNT_HB`,
  `BBS_MENU_HB`, `BBS_GLYPH_BANK name=core_status`, and `BBS_LCD_RENDER`.
- Monitor transcript had 205 lines; its filename and SHA256 are retained only
  in ignored local evidence.
- Transcript scan counted `BBS_LCD_RENDER=14`, `BBS_MENU_HB=14`,
  `ENC_LEVEL_HB=29`, `ENC_PCNT_HB=28`, one `BBS_GLYPH_BANK`, zero
  `BBS_MENU_STEP`, zero `BBS_MENU_SELECT`, and zero crash/unsafe markers.
- Cleanup proof found no lingering Windows `python` or `esptool` process; the
  Linux process scan only matched the cleanup-check command itself.

## Open Evidence

- Physical LCD readability of the PF0530W `ART` page remains unproven until
  operator visual acceptance is collected.
- The read-only monitor stayed on HOME because no physical encoder input was
  exercised during this gate; ART page render telemetry remains open.
- The app image header reports 2 MB flash size, while the physical chip reports
  4 MB. This follows the current project `sdkconfig`/build flash-size setting
  and was not changed in this gate.

## Closed Surfaces

No erase-all, serial command writes, XBee/RF writes or tests, ESP-NOW runtime
expansion, relay GPIO writes, relay-expander writes, MicroSD/TFT action,
wiring mutation, DMM/current measurement, relay/load/mains work, persistent
config, external services, GitHub publication, release, commit, or push is
proven or authorized by this record.
