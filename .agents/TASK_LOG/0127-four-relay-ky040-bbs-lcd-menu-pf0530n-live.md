# Four Relay KY-040 BBS LCD Menu PF0530N Live

Status: PF0530N written, verify-flashed, and read-only monitor-scanned on COM6

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-01

## Routing

- Selected tier: Tier 3 because this task opened a live COM6 flash/write gate.
- Owner role: Firmware live-gate owner with Hardware-safety, QA, Evidence
  Records, and Risk lenses.
- Evidence need: explicit COM6 flash authority and safe-state confirmation,
  read-only reviewer quorum, fresh static validation, ESP-IDF v6.0.1 no-flash
  build, pinned artifacts and hashes, same-session COM6 identity, full rollback
  backup/hash/recovery command, write-flash log, separate verify-flash log,
  read-only boot monitor transcript, transcript scan, cleanup proof, source
  ledger, status records, and this task log.
- Mutation boundary: COM6-only PF0530N write/verify, read-only boot transcript,
  local evidence directory, source/status/docs records, and hardware QA
  handoff.
- Closed surfaces: no XBee/RF writes or tests, no relay GPIO writes, no
  relay-expander writes, no load/mains work, no wiring mutation, no DMM/current
  measurement, no erase, no persistent configuration, no publication, no
  commit, and no push.

## Verified Facts

- The user requested a live flash of PF0530N on COM6 and confirmed safe state.
- Reviewer quorum was closed after output capture. Weighted disposition was
  14/14 conditional approve for the named COM6 PF0530N gate after fresh
  identity, rollback backup, pinned artifacts, write-flash, separate
  verify-flash, optional read-only scan, cleanup, and records.
- Refreshed validation passed before flash:
  XML generator freshness check, 22 LCD simulator tests, 4 firmware boundary
  tests, 32 custom wireless protocol tests, four-relay safe-core host tests,
  firmware/source/docs/agent/data scaffold audits, `verify_scaffold.py`,
  67 scaffold audit unittests, `git diff --check`, and ESP-IDF v6.0.1
  no-flash build.
- The staged live build generated `four_relay_xbee_wifi.bin` size `0x2d3c0`
  with `0xd2c40` bytes free in the smallest app partition.
- Same-session COM6 identity matched ESP32-D0WDQ6 revision v1.0, detected
  4 MB flash, and detected flash voltage strap 3.3 V. The raw MAC is retained
  only in ignored local evidence and is redacted from this publishable record.
- A full 4 MB rollback backup was captured before write. The exact local path
  and SHA256 are retained only in ignored local evidence and are redacted from
  this publishable record.
- Pinned PF0530N artifact hashes for bootloader, partition table, and app were
  recorded in ignored local evidence and are redacted from this publishable
  record.
- COM6 write-flash passed and esptool verified each written segment.
- Separate COM6 verify-flash passed with digest matches for bootloader,
  partition table, and app.
- The 120 second read-only monitor recorded `writes_sent=false`, one
  `PF0530N BBS_LCD_READY`, one `PF0530N BBS_INPUT_READY`, 61
  `BBS_LCD_RENDER`, 61 `BBS_CURSOR`, 59 `BBS_MENU_HB`, 17
  `BBS_MENU_AUTO`, seven `BBS_GLYPH_BANK`, one `bbs_lcd_menu.v1`, and one
  `bbs_lcd_render.v2`.
- Transcript scan found zero `Guru Meditation`, `Backtrace`, `panic`,
  `watchdog`, `abort()`, `LCD_INIT_FAIL`, `UNSAFE_OPEN`, or `BRIDGE_OPEN`
  markers.
- Cleanup proof found no lingering Windows flash/monitor process and only the
  cleanup command itself in the transient WSL process scan.

## Assumptions

- The user's safe-state confirmation covered this same COM6-only PF0530N flash
  gate and its normal esptool resets.
- The ESP-IDF generated `--flash-size 2MB` argument is the intended project
  flash setting; COM6 still reports a 4 MB physical flash, and the rollback
  backup covers the full detected device.
- The read-only monitor proves boot/runtime serial readiness only. It does not
  prove human-visible LCD readability or physical encoder/button actuation.

## Unknowns

- Physical readability of the PF0530N scroll-list and table page on the actual
  LCD remains unproven until user observation.
- Physical encoder direction and button behavior under PF0530N remain unproven;
  the passive monitor captured zero `ENC_RAW`, zero `ENC_EV`, zero
  `BBS_MENU_STEP`, and zero `BBS_MENU_SELECT`.
- Final BBS/XBee payload mapping, relay/load/mains readiness, and deployment
  acceptance remain future gates.

## Evidence

- Evidence directory: ignored local PF0530N live evidence directory; exact path
  redacted from this publishable record.
- Manifest: `pf0530n-live-manifest.txt`
- Artifact hashes: `pf0530n-artifact-sha256.txt`
- COM6 identity: `com6-esptool-chip-id.txt`,
  `com6-esptool-read-mac.txt`, and `com6-esptool-flash-id.txt`
- Rollback backup/hash/recovery:
  `com6-pre-pf0530n-scrolling-xml-4mb.bin`,
  `com6-pre-pf0530n-read-flash-sha256.txt`, and
  `pf0530n-recovery-command.txt`
- Flash logs: `com6-pf0530n-write-flash.txt` and
  `com6-pf0530n-verify-flash.txt`
- Runtime evidence: `com6-pf0530n-readonly-monitor-120s.txt` and
  `pf0530n-transcript-scan.txt`
- Cleanup proof: `pf0530n-cleanup-summary.txt`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py` (22 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/scaffold_audits/test_firmware_encoder_pullup_boundary.py` (4 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py` (32 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_data.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'` (67 tests)
- PASS: ESP-IDF v6.0.1 no-flash build to an ignored temporary build
  directory.
- PASS: `git diff --check`
- PASS: COM6 write-flash and separate verify-flash.
- PASS: read-only monitor transcript scan.

## Closed Surfaces

This gate does not authorize or prove XBee/RF writes or tests, ESP-NOW runtime,
relay GPIO writes, relay-expander writes, MicroSD/TFT action, wiring mutation,
DMM/current measurement, relay/load/mains work, erase, firmware HTTP/SoftAP/
WebSocket runtime, persistent configuration, external service changes, commit,
or push.

## Decision Footer

Decision: `ready_for_user_visual_test`. PF0530N is now written and
verify-flashed on COM6 with read-only boot evidence. Next useful gate is user
visual observation of the scroll-list/table page and, if requested, a separate
attended encoder/button interaction proof. Live hardware surfaces remain
closed behind fresh Tier 3 gates.
