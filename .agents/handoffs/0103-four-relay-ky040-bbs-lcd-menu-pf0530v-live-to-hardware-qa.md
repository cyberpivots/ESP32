# PF0530V Live Gate To Hardware QA

Status: PF0530V written and verify-flashed on COM6; readiness proof passed; encoder functionality user-confirmed; telemetry characterization open

Date: 2026-06-02

## Context

PF0530V is now the flashed COM6 image. It moves A/B rotation decoding to
ESP-IDF PCNT quadrature on GPIO13/GPIO14 and keeps the switch on the
poll/debounce path. The live gate proved write/verify/readiness. After that
gate, the user confirmed real LCD menu encoder functionality on the flashed
PF0530V image.

## Verified Facts

- COM6 identity: ESP32-D0WDQ6 revision v1.0, MAC `<redacted-mac>`.
- Flash ID: manufacturer `5e`, device `4016`, detected flash size `4MB`, 3.3 V
  flash-voltage strap.
- Rollback backup exists before PF0530V write; its filename and SHA256 are
  retained only in ignored local evidence.
- Staged PF0530V hashes were pinned before programming and retained only in
  ignored local evidence.
- COM6 write-flash and separate verify-flash succeeded for only the three
  normal image regions.
- Reset/read-only transcript proved `PF0530V`, `LCD_INIT_OK`,
  `BBS_LCD_READY`, `BBS_INPUT_READY`, `cal=pcnt-v1`, `decoder=pcnt`,
  `irq=pcnt`, `poll_decoder=0`, `ENC_BASE`, GPIO13/GPIO14/GPIO32 config,
  GPIO config dump, `ENC_PCNT_READY result=ok`, `ENC_LEVEL_HB`,
  `ENC_PCNT_HB`, `BBS_MENU_HB`, and `BBS_LCD_RENDER`.
- Idle read-only transcript stayed alive with PCNT/menu/render heartbeats.
- Transcript scan and cleanup proof passed with no crash/unsafe markers and no
  lingering monitor/esptool/idf process.
- User confirmation after the PF0530V gate: `ENCODER FUNCTIONALITY CONFIRMED
  AND APPROVED BY USER`.

## Accepted User Evidence And Open Telemetry

User/operator acceptance is recorded for PF0530V rotary encoder LCD menu
functionality. No post-confirmation transcript counts are claimed for
`BBS_MENU_STEP` in both directions, short and long `BBS_MENU_SELECT`,
PCNT direction/counts per detent, or quantified runaway tolerance unless a
future read-only proof captures them.

## Stop Gates

Do not erase, reflash, send serial commands, write XBee/RF settings, perform
relay/load/mains work, mutate wiring, perform DMM/current measurement, persist
config, release, commit, or push without a separate explicit gate.
