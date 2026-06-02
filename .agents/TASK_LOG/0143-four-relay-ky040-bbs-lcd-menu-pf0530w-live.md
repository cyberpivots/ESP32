# Four Relay KY-040 BBS LCD Menu PF0530W Live Gate

Status: PF0530W written and verify-flashed on COM6; readiness proof passed; physical ART page visual acceptance pending

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-02

## Routing

- Selected tier: Tier 3 because this task includes same-session COM6 identity,
  rollback backup, write-flash, separate verify-flash, reset/read-only monitor,
  cleanup proof, and durable records.
- Owner role: Firmware live-gate owner with coordinator, QA, LCD UX,
  hardware-safety, and evidence-record lenses.
- Evidence need: reviewer quorum, source preflight, ESP-IDF build, COM6
  redacted identity, 4 MB rollback backup with private hashes retained only in
  ignored local evidence, write-flash, separate verify-flash, reset boot
  transcript, transcript scan, cleanup proof, and durable records.
- Mutation boundary: COM6 bootloader `0x1000`, partition table `0x8000`, and
  app `0x10000` write only, plus PF0530W live records/status updates. No erase,
  serial command writes, XBee/RF writes or tests, relay GPIO writes,
  relay-expander writes, ESP-NOW runtime expansion, wiring changes,
  DMM/current/load/mains, persistent config, external services, release,
  commit, or push.
- Reviewer disposition: the read-only quorum blocked immediate flash until the
  host-only art compiler was made firmware-visible and same-session build,
  COM6 identity, rollback, hashes, write/verify, monitor, cleanup, and closed
  surfaces were proven. Those preconditions were satisfied before the bounded
  COM6 write.
- Gate authority: the user explicitly requested COM6 live flash with the LCD
  menu improvements applied and confirmed authority and safe state.

## Verified Facts

- Same-session COM6 inventory identified a Silicon Labs CP210x USB to UART
  Bridge on `COM6`.
- Same-session esptool identity matched ESP32-D0WDQ6 revision v1.0 with MAC
  `<redacted-mac>`.
- Flash ID reported manufacturer `5e`, device `4016`, detected flash size
  `4MB`, and 3.3 V flash-voltage strap.
- Full rollback backup was captured before writing; its filename and SHA256
  are retained only in ignored local evidence.
- PF0530W staged artifact hashes were pinned before programming and retained
  only in ignored local evidence.
- COM6 write-flash wrote only `0x1000`, `0x8000`, and `0x10000`; each region
  verified during the write.
- Separate parameter-matched `verify-flash` succeeded for bootloader,
  partition table, and app.
- Reset/read-only monitor used `writes_sent=false` and captured `PF0530W`,
  `LCD_INIT_OK addr=0x27`, `PF0530W BBS_LCD_READY`, `PF0530W BBS_INPUT_READY`,
  `pages=15`, `glyph_banks=7`, `cal=pcnt-v1`, `decoder=pcnt`, `irq=pcnt`,
  `poll_decoder=0`, GPIO13/GPIO14/GPIO32 `ENC_GPIO_CONFIG`,
  `PF0530W ENC_PCNT_READY result=ok`, `ENC_LEVEL_HB`, `ENC_PCNT_HB`,
  `BBS_MENU_HB`, `BBS_GLYPH_BANK name=core_status`, and `BBS_LCD_RENDER`.
- Transcript scan counted `BBS_LCD_RENDER=14`, `BBS_MENU_HB=14`,
  `ENC_LEVEL_HB=29`, `ENC_PCNT_HB=28`, one `BBS_GLYPH_BANK`, zero
  `BBS_MENU_STEP`, zero `BBS_MENU_SELECT`, and zero crash/unsafe markers.
- Cleanup proof found no lingering Windows `python` or `esptool` process; the
  Linux process scan only matched the cleanup-check command itself.

## Open Evidence

- Physical LCD readability of the `ART` page is still pending.
- The read-only monitor stayed on HOME because no physical encoder input was
  exercised during this gate; it did not capture ART page render telemetry.
- The app image header reports 2 MB flash size, while the physical chip reports
  4 MB. This matches the existing project `sdkconfig`/build flash-size setting
  and is not changed by this gate.

## Closed Surfaces

No erase-all, serial command writes, XBee/RF writes or tests, ESP-NOW runtime
expansion, relay GPIO writes, relay-expander writes, MicroSD/TFT action,
wiring mutation, DMM/current measurement, relay/load/mains work, persistent
config, external services, GitHub publication, release, commit, or push is
proven or authorized by this record.

## Decision Footer

Decision: `pf0530w_written_verify_flashed_readiness_passed_art_visual_pending`.
Next gate: use the physical encoder to navigate to the ART page and collect
operator visual acceptance, optionally with a read-only monitor showing ART
page render telemetry. Owner: Firmware with Hardware QA, LCD UX, and Evidence
Records. Evidence: source preflight, build, COM6 identity, rollback,
write/verify flash, read-only transcript, scan, cleanup, and live source
ledger.
