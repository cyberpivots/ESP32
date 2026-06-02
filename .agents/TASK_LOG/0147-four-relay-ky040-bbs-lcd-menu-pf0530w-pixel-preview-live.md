# Four Relay KY-040 BBS LCD Menu PF0530W Pixel Preview Live Gate

Status: Task 0146 pixel-preview LCD menu artifact written and verify-flashed on COM6; readiness proof passed; physical ART acceptance pending

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-02

## Routing

- Verified facts: the user explicitly granted live-flash authority and
  confirmed safe state; Task 0146 was committed on `main`; the preexisting
  PF0530W live gate established the same COM6 LCD/encoder device class; and
  same-session reviewer, build, identity, rollback, write, verify, monitor,
  transcript-scan, and cleanup evidence were collected for this gate.
- Assumptions: COM6 is the intended four-relay KY-040 BBS LCD menu device;
  the requested recent improvement is Task 0146's generated LCD
  pixel-preview/catalog artifact; and physical encoder interaction is outside
  this flash/readiness gate unless separately performed.
- Unknowns: physical LCD ART-page readability, contrast, flicker, exact
  backpack behavior, and ART-page navigation/render telemetry.
- Selected tier: Tier 3 because this task includes same-session COM6 live
  identity, rollback backup, write-flash, separate verify-flash,
  reset/read-only monitor, cleanup proof, and durable records.
- Owner role: Firmware live-gate coordinator with hardware-safety, LCD UX, QA,
  and evidence-record lenses.
- Evidence need: project-local read-only reviewer quorum, host/source
  validation, no-flash ESP-IDF build, COM6 identity, full rollback backup,
  staged artifact hashes, bounded write-flash, separate verify-flash,
  read-only monitor, transcript scan, cleanup proof, and durable records.
- Mutation boundary: COM6 bootloader `0x1000`, partition table `0x8000`, and
  app `0x10000` writes only, plus ignored local evidence and this live-gate
  record set. No erase-all, serial command writes, XBee/RF, ESP-NOW runtime
  expansion, relay GPIO writes, relay-expander writes, MicroSD/TFT, wiring
  mutation, DMM/current/load/mains work, persistent config, external services,
  release, commit, push, PR, or deploy.
- Validation plan: focused LCD generator/tests, firmware boundary tests,
  scaffold audits, ESP-IDF no-flash build, same-session COM6 identity,
  rollback backup, write/verify flash logs, read-only monitor scan, cleanup
  proof, source/docs/records audits, `git diff --check`, and Git status.
- Gate authority: same-session user authority and safe-state confirmation.
- Reviewer disposition: firmware/device, power/wiring/isolation, and QA
  read-only reviewers conditionally approved this COM6-only flash/readiness
  boundary after fresh identity, rollback, hashes, bounded write, separate
  verify, read-only monitor, cleanup, and records. No P1/P2 blockers remained
  for this scoped gate. Reviewer outputs were captured and reviewer agents were
  closed before final record work.

## Verified Facts

- Source HEAD was `9aae6c6e9498` on `main`, matching the app version shown in
  the post-flash monitor.
- Host validation passed before live mutation:
  LCD generator `--check`, focused LCD unittest suite, combined firmware/LCD
  boundary unittest suite, `scripts/scaffold_audit_firmware.py`,
  `scripts/verify_scaffold.py`, and an ESP-IDF v6.0.1 no-flash build to
  `/tmp/esp32-pf0530w-pixel-preview-live-build`.
- Staged artifact sizes were pinned in ignored local evidence:
  bootloader `26128`, partition table `3072`, app `197248`, and ELF
  `3283780` bytes.
- Staged artifact hashes, including the ELF hash, were retained in ignored
  local evidence. The copied ELF was removed from the repo evidence directory
  after Git surfaced it as unignored; text hashes remain in evidence.
- Same-session COM6 inventory identified a Silicon Labs CP210x USB to UART
  Bridge on `COM6` with VID `10C4` and PID `EA60`.
- Same-session esptool identity matched ESP32-D0WDQ6 revision v1.0 with MAC
  `<redacted-mac>`.
- Flash ID reported manufacturer `5e`, device `4016`, detected flash size
  `4MB`, and 3.3 V flash-voltage strap.
- A fresh full rollback backup was captured before writing; it was `4194304`
  bytes and its SHA256 is retained only in ignored local evidence.
- COM6 write-flash wrote only `0x1000`, `0x8000`, and `0x10000`; each region
  reported `Hash of data verified`.
- Separate parameter-matched `verify-flash` succeeded for bootloader,
  partition table, and app.
- Reset/read-only monitor showed `writes_sent=false`, app version `9aae6c6`,
  ELF SHA prefix `41936e573`, `PF0530W LCD_DIAG_READY`, `LCD_BUS result=ok`,
  `LCD_INIT_OK addr=0x27`, `LCD_DEVICE result=ok addr=0x27`,
  `PF0530W ENC_PCNT_READY result=ok`, `PF0530W BBS_LCD_READY`,
  `PF0530W BBS_INPUT_READY`, `pages=15`, `items=65`, `glyph_banks=7`,
  `cal=pcnt-v1`, `decoder=pcnt`, `irq=pcnt`, `poll_decoder=0`, GPIO13/14/32
  input/pullup configuration, `BBS_GLYPH_BANK name=core_status`,
  `BBS_LCD_RENDER`, `BBS_MENU_HB`, `ENC_LEVEL_HB`, and `ENC_PCNT_HB`.
- The first HOME render included Task 0146 generated labels:
  `>BBS Ready {link.sta`, `Messages Custody`, `Peers RSSI`, and
  `Queue Files`.
- Transcript scan counted `line_count=221`, `BBS_LCD_RENDER=16`,
  `BBS_MENU_HB=17`, `ENC_LEVEL_HB=33`, `ENC_PCNT_HB=33`, one
  `BBS_GLYPH_BANK`, zero `BBS_MENU_STEP`, zero `BBS_MENU_SELECT`, and zero
  crash markers for `Guru Meditation`, `panic`, `abort`, `Backtrace`,
  `brownout`, `watchdog`, `WDT`, `assert`, `LoadProhibited`,
  `StoreProhibited`, and `CORRUPT HEAP`.
- Cleanup proof found no matching Windows `pf0530e_serial_pintrace_monitor` or
  `esptool` process and no Linux Python/esptool monitor process.

## Open Evidence

- Physical LCD readability and operator acceptance of the ART page remain
  unproven.
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

## Handoff

Handoff:
[../handoffs/0108-four-relay-ky040-bbs-lcd-menu-pf0530w-pixel-preview-live-to-hardware-qa.md](../handoffs/0108-four-relay-ky040-bbs-lcd-menu-pf0530w-pixel-preview-live-to-hardware-qa.md)

## Decision Footer

Decision: `pf0530w_pixel_preview_written_verify_flashed_readiness_passed_art_visual_pending`.
Next gate: use the physical encoder to navigate to the ART page and collect
operator visual acceptance, optionally with a read-only monitor showing ART
page render telemetry. Owner: Firmware with Hardware QA, LCD UX, and Evidence
Records. Evidence: Task 0146 source/build, COM6 identity, rollback,
write/verify flash, read-only transcript, transcript scan, cleanup proof, and
live source ledger.
