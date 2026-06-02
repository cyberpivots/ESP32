# Four Relay KY-040 BBS LCD Menu PF0530V Live Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-LIVE-2026-06-02`

Date: 2026-06-02

## Scope

COM6-only PF0530V live gate for the PCNT rotary encoder LCD menu image. This
record covers identity, rollback, write-flash, separate verify-flash,
reset/read-only monitor proof, idle read-only proof, transcript scan, cleanup
scope, and the later user confirmation linked in the PF0530V user-acceptance
source ledger.

## Verified Facts

- User explicitly requested and authorized the Tier 3 PF0530V COM6
  flash/verify/read-only live gate and stated `SAFE STATE CONFIRMED`.
- Six read-only reviewers conditionally approved the named boundary with no
  P1/P2 blockers once same-session identity, rollback, hashes, write/verify,
  read-only monitor, cleanup, and durable records were captured.
- Source preflight passed: 60 focused tests, LCD menu generator `--check`,
  firmware scaffold audit, agent-process audit, scaffold verification,
  `git diff --check`, and ESP-IDF v6.0.1 build to
  `/tmp/esp32-pf0530v-live-build`.
- COM6 identified as ESP32-D0WDQ6 revision v1.0 with MAC
  `<redacted-mac>`.
- Flash ID reported manufacturer `5e`, device `4016`, detected flash size
  `4MB`, and 3.3 V flash voltage strap.
- A fresh full rollback backup was captured before PF0530V write; its filename
  and SHA256 are retained only in ignored local evidence.
- PF0530V staged artifact hashes were pinned before programming and retained
  only in ignored local evidence.
- COM6 write-flash wrote only `0x1000`, `0x8000`, and `0x10000`; each region
  verified during the write.
- Separate parameter-matched `verify-flash` succeeded for bootloader,
  partition table, and app.
- Reset boot monitor showed `writes_sent=false`, `PF0530V`,
  `LCD_INIT_OK addr=0x27`, `PF0530V BBS_LCD_READY`,
  `PF0530V BBS_INPUT_READY`, `cal=pcnt-v1`, `decoder=pcnt`, `irq=pcnt`,
  `poll_decoder=0`, `ENC_BASE`, GPIO13/GPIO14/GPIO32 `ENC_GPIO_CONFIG`, GPIO
  config dump, `PF0530V ENC_PCNT_READY result=ok`, `ENC_LEVEL_HB`,
  `ENC_PCNT_HB`, `BBS_MENU_HB`, and `BBS_LCD_RENDER`.
- Idle read-only monitor showed `writes_sent=false`, continued PCNT/menu/render
  heartbeats, and no reset-line toggle.
- Transcript scan counts included `ENC_LEVEL_HB=103`, `ENC_PCNT_HB=103`,
  `BBS_MENU_HB=51`, `BBS_LCD_RENDER=50`, and zero crash/unsafe markers.
- Cleanup proof found no lingering Linux or Windows monitor/esptool/idf
  process.
- After the PF0530V COM6 flash/verify/read-only readiness proof, the user
  stated: `ENCODER FUNCTIONALITY CONFIRMED AND APPROVED BY USER`. This records
  user-confirmed PF0530V encoder/LCD menu functionality acceptance. Source ID:
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-USER-ACCEPTANCE-2026-06-02`.

## User Acceptance And Open Telemetry

PF0530V real LCD menu encoder functionality is user-confirmed and accepted by
operator report. The live gate did not capture post-confirmation transcript
counts, so `BBS_MENU_STEP`, `BBS_MENU_SELECT`, PCNT direction/counts-per-detent
behavior, and quantified runaway tolerance remain telemetry characterization
topics unless a separate read-only proof is requested.

## Closed Surfaces

No erase-all, serial command writes, XBee/RF writes or tests, ESP-NOW runtime
expansion, relay GPIO writes, relay-expander writes, MicroSD/TFT action,
wiring mutation, DMM/current measurement, relay/load/mains work, persistent
config, external services, GitHub publication, release, commit, or push is
proven or authorized by this record.
