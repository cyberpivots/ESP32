# Four Relay KY-040 BBS LCD Menu PF0530V Live Gate

Status: PF0530V written and verify-flashed on COM6; readiness proof passed; encoder functionality user-confirmed; telemetry characterization open

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-02

## Routing

- Selected tier: Tier 3 because this continuation includes COM6 identity,
  rollback backup, write-flash, separate verify-flash, reset/read-only monitor,
  cleanup proof, and durable records.
- Owner role: Firmware live-gate owner with coordinator, QA, LCD UX,
  hardware-safety, and evidence-record lenses.
- Evidence need: reviewer quorum, source preflight, ESP-IDF build, COM6
  identity, 4 MB rollback backup and hash, staged artifact hashes, write-flash,
  separate verify-flash, reset boot transcript, idle read-only transcript,
  transcript scan, cleanup proof, and durable records.
- Mutation boundary: COM6 bootloader `0x1000`, partition table `0x8000`, and
  app `0x10000` write only, plus PF0530V live records/status updates. No erase,
  serial command writes, XBee/RF writes or tests, relay GPIO writes,
  relay-expander writes, ESP-NOW runtime expansion, wiring changes,
  DMM/current/load/mains, persistent config, external services, release,
  commit, or push.
- Reviewer disposition: six read-only subagents approved the named PF0530V
  boundary with conditions and no P1/P2 blockers. Conditions were satisfied in
  this same session before flash: explicit user authority, safe state, COM6
  identity, rollback backup, staged hashes, matched write/verify plan,
  read-only monitor plan, cleanup plan, and closed-surface preservation.
- Gate authority: user explicitly requested and authorized the Tier 3 PF0530V
  COM6 flash/verify/read-only live gate and stated `SAFE STATE CONFIRMED`.

## Verified Facts

- Same-session COM6 identity matched ESP32-D0WDQ6 revision v1.0 with MAC
  `<redacted-mac>`.
- Flash ID reported manufacturer `5e`, device `4016`, detected flash size
  `4MB`, and 3.3 V flash-voltage strap.
- Full rollback backup was captured before writing; its filename and SHA256
  are retained only in ignored local evidence.
- PF0530V staged artifact hashes were pinned before programming and retained
  only in ignored local evidence.
- COM6 write-flash wrote only `0x1000`, `0x8000`, and `0x10000`; each region
  verified during the write.
- Separate parameter-matched `verify-flash` succeeded for bootloader,
  partition table, and app.
- Reset boot monitor used `writes_sent=false` and captured `PF0530V`,
  `LCD_INIT_OK`, `BBS_LCD_READY`, `BBS_INPUT_READY`, `cal=pcnt-v1`,
  `decoder=pcnt`, `irq=pcnt`, `poll_decoder=0`, `ENC_BASE`,
  GPIO13/GPIO14/GPIO32 `ENC_GPIO_CONFIG`, GPIO config dump, `ENC_PCNT_READY`,
  `ENC_LEVEL_HB`, `ENC_PCNT_HB`, `BBS_MENU_HB`, and `BBS_LCD_RENDER`.
- Additional idle read-only monitor used `writes_sent=false`, did not toggle
  reset, and continued `ENC_LEVEL_HB`, `ENC_PCNT_HB`, `BBS_MENU_HB`, and
  `BBS_LCD_RENDER` output.
- Transcript scan counted zero `Guru Meditation`, `Backtrace`, `panic`,
  `abort`, `WDT`, `watchdog`, `brownout`, `LCD_INIT_FAIL`,
  `GPIO_CONFIG_FAILED`, `INPUT_TASK_FAILED`, unsafe, relay-open, XBee-open, or
  erase-all markers.
- Cleanup proof found no lingering Linux or Windows monitor/esptool/idf
  process after the read-only monitors completed.
- After the PF0530V COM6 flash/verify/read-only readiness proof, the user
  stated: `ENCODER FUNCTIONALITY CONFIRMED AND APPROVED BY USER`. This records
  user-confirmed PF0530V encoder/LCD menu functionality acceptance.

## Telemetry Characterization Open

- The live monitor gate intentionally did not capture post-confirmation
  actuation counts. Therefore transcript-level `BBS_MENU_STEP` direction
  behavior, short/long `BBS_MENU_SELECT` counts, PCNT direction/counts per
  detent, and quantified runaway tolerance remain uncharacterized unless a
  separate read-only monitor is requested.

## Decision Footer

Decision: `pf0530v_user_confirmed_functional_telemetry_characterization_open`.
Next gate: use PF0530V as the accepted functional LCD menu encoder image, or run
a separate read-only monitor only if transcript-count characterization is
requested. Owner: Firmware with Hardware QA and Evidence Records. Evidence:
source preflight, build, COM6 identity, rollback, write/verify flash, read-only
transcripts, scan, cleanup, live source ledger, and user acceptance source
ledger. Authority limits: no erase, serial command writes, XBee/RF,
relay/load/mains, wiring, DMM/current, persistent config, external services,
release, commit, or push.
