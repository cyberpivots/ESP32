# Four Relay KY-040 BBS LCD Menu PF0530W Pixel Preview Live Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-PIXEL-PREVIEW-LIVE-2026-06-02`

Date: 2026-06-02

## Scope

COM6-only live gate for the Task 0146 LCD pixel-preview/catalog generated menu
artifact under the existing PF0530W firmware identity. This record covers
reviewer disposition, host validation, COM6 identity, rollback, write-flash,
separate verify-flash, reset/read-only monitor proof, transcript scan, cleanup
scope, and the open physical ART-page visual-acceptance gate.

## Verified Facts

- User explicitly granted same-session live-flash authority and confirmed safe
  state.
- Project-local read-only reviewers conditionally approved the COM6-only
  flash/readiness boundary after same-session identity, rollback, artifact
  hashes, bounded write, separate verify, read-only monitor, cleanup, and
  records. No P1/P2 blockers remained for this scoped gate.
- Source HEAD was `9aae6c6e9498` on `main`, matching post-flash app version
  `9aae6c6`.
- Host validation passed before live mutation: LCD generator `--check`,
  focused LCD tests, combined firmware/LCD boundary tests,
  `scripts/scaffold_audit_firmware.py`, `scripts/verify_scaffold.py`, and an
  ESP-IDF v6.0.1 no-flash build to
  `/tmp/esp32-pf0530w-pixel-preview-live-build`.
- Staged artifact sizes were pinned in ignored local evidence: bootloader
  `26128`, partition table `3072`, app `197248`, and ELF `3283780` bytes.
- Staged artifact hashes, including the ELF hash, are retained in ignored
  local evidence. The copied ELF was removed from the repo evidence directory
  after Git surfaced it as unignored; text hashes remain in evidence.
- Same-session COM6 inventory identified a Silicon Labs CP210x USB to UART
  Bridge on `COM6` with VID `10C4` and PID `EA60`.
- COM6 identified as ESP32-D0WDQ6 revision v1.0 with MAC `<redacted-mac>`.
- Flash ID reported manufacturer `5e`, device `4016`, detected flash size
  `4MB`, and 3.3 V flash-voltage strap.
- A fresh full rollback backup was captured before write; it was `4194304`
  bytes and its SHA256 is retained only in ignored local evidence.
- COM6 write-flash wrote only `0x1000`, `0x8000`, and `0x10000`; each region
  reported `Hash of data verified`.
- Separate parameter-matched `verify-flash` succeeded for bootloader,
  partition table, and app.
- Reset/read-only monitor showed `writes_sent=false`, `PF0530W`,
  `LCD_INIT_OK addr=0x27`, `LCD_BUS result=ok`, `LCD_DEVICE result=ok`,
  `PF0530W BBS_LCD_READY`, `PF0530W BBS_INPUT_READY`, `pages=15`,
  `items=65`, `glyph_banks=7`, `cal=pcnt-v1`, `decoder=pcnt`, `irq=pcnt`,
  `poll_decoder=0`, `PF0530W ENC_PCNT_READY result=ok`, `ENC_LEVEL_HB`,
  `ENC_PCNT_HB`, `BBS_MENU_HB`, `BBS_GLYPH_BANK name=core_status`, and
  `BBS_LCD_RENDER`.
- The first HOME render included Task 0146 generated labels:
  `>BBS Ready {link.sta`, `Messages Custody`, `Peers RSSI`, and
  `Queue Files`.
- Transcript scan counted `line_count=221`, `BBS_LCD_RENDER=16`,
  `BBS_MENU_HB=17`, `ENC_LEVEL_HB=33`, `ENC_PCNT_HB=33`, one
  `BBS_GLYPH_BANK`, zero `BBS_MENU_STEP`, zero `BBS_MENU_SELECT`, and zero
  crash markers.
- Cleanup proof found no matching Windows `pf0530e_serial_pintrace_monitor` or
  `esptool` process and no Linux Python/esptool monitor process.

## Open Evidence

- Physical LCD readability and operator acceptance of the Task 0146 ART panels
  remain unproven.
- The read-only monitor stayed on HOME because no physical encoder input was
  exercised during this gate; ART-page render telemetry remains open.
- The app image header reports 2 MB flash size while the physical chip reports
  4 MB. This follows the current project `sdkconfig`/build flash-size setting
  and was not changed in this gate.
- The monitor helper filename/header still contains the older `PF0530E`
  script label, but the captured firmware telemetry identifies the flashed
  runtime as `PF0530W`.

## Closed Surfaces

No erase-all, serial command writes, XBee/RF writes or tests, ESP-NOW runtime
expansion, relay GPIO writes, relay-expander writes, MicroSD/TFT action,
wiring mutation, DMM/current measurement, relay/load/mains work, persistent
config, external services, GitHub publication, release, commit, push, PR, or
deploy is proven or authorized by this record.
