# Four Relay KY-040 BBS LCD Menu PF0530U Live Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530U-LIVE-2026-06-02`

Date: 2026-06-02

## Scope

COM6-only PF0530U live gate for the responsive-v7 rotary encoder LCD menu
image. This record covers identity, rollback, write-flash, separate
verify-flash, reset boot proof, read-only monitor proof, and cleanup scope.

## Verified Facts

- COM6 identified as ESP32-D0WDQ6 revision v1.0 with MAC
  `<redacted-mac>`.
- Flash ID reported manufacturer `5e`, device `4016`, detected flash size
  `4MB`, and 3.3 V flash voltage strap.
- A fresh full rollback backup was captured before PF0530U write; its filename
  and SHA256 are retained only in ignored local evidence.
- PF0530U staged artifact hashes were pinned before programming and retained
  only in ignored local evidence.
- COM6 write-flash wrote only `0x1000`, `0x8000`, and `0x10000`; each region
  verified during the write.
- Separate parameter-matched `verify-flash` succeeded for bootloader,
  partition table, and app.
- Reset boot monitor showed `PF0530U`, `LCD_INIT_OK addr=0x27`,
  `PF0530U BBS_LCD_READY`, `PF0530U BBS_INPUT_READY`, `cal=responsive-v7`,
  `step=1`, `irq=poll`, `queue=0`, `ENC_BASE`, GPIO13/GPIO14/GPIO32
  `ENC_GPIO_CONFIG`, GPIO config dump, and `ENC_LEVEL_HB`.
- The 150 second PF0530U attended read-only monitor stayed stable with
  `ENC_LEVEL_HB=150`, `BBS_MENU_HB=75`, `LCD_RENDER=75`,
  `CRASH_MARKERS=0`, and no serial writes.
- The final 75 second PF0530U read-only monitor stayed stable with
  `ENC_LEVEL_HB=75`, `BBS_MENU_HB=38`, `LCD_RENDER=38`,
  `CRASH_MARKERS=0`, and no serial writes.

## Open Proof Item

- No physical input was captured after PF0530U was flashed:
  `ENC_EV=0`, `STEP_PLUS=0`, `STEP_MINUS=0`, `SELECT=0`,
  `MAX_RAW_AB=0`, and `MAX_RAW_SW=0` in both PF0530U post-flash monitor
  windows. This does not disprove the firmware path; it means the PF0530U live
  monitor windows did not include knob/switch actuation.
- PF0530T immediately before PF0530U did capture physical input on the same
  GPIO path: `ENC_EV=446`, `CLK_EV=198`, `DT_EV=188`, `SW_EV=60`,
  `SELECT=30`, `SELECT_SHORT=21`, `SELECT_LONG=9`, `STEP_PLUS=2`, and
  `STEP_MINUS=2`, but PF0530T was too conservative for rotation.

## Closed Surfaces

No erase-all, serial command writes, XBee/RF writes or tests, ESP-NOW runtime
expansion, relay GPIO writes, relay-expander writes, MicroSD/TFT action,
wiring mutation, DMM/current measurement, relay/load/mains work, persistent
config, external services, GitHub publication, release, commit, or push is
proven or authorized by this record.
