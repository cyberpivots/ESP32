# Task 0142: Four Relay KY-040 BBS LCD Menu PF0530W Visual Art

Status: source/build integration complete; PF0530W live flash completed; physical art-page visual acceptance pending

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-02

## Goal

Make the LCD visual art improvement firmware-visible before any COM6 flash by
adding a named `PF0530W` LCD menu image with a navigable 4x20 custom-character
art page.

## Routing Packet

- Verified facts: the user requested COM6 live flash and confirmed authority
  and safe state. The Tier 3 reviewer quorum blocked immediate flash because
  Task 0141 `bbs_lcd_art.v1` was host-only and no fresh flashable firmware
  artifact proved those visual improvements were in the image.
- Assumptions: the requested improvement means a firmware-visible HD44780
  custom-character art page while preserving the accepted PF0530V PCNT encoder
  behavior and all closed safety surfaces.
- Unknowns: physical LCD readability of the new art panel after encoder
  navigation and post-flash transcript counts for the ART page.
- Selected tier: Tier 2 for source/build integration, followed by Tier 3 for
  any COM6 write/verify/live monitor.
- Owner role: Firmware LCD-menu owner with live-bench, QA, LCD UX,
  power/wiring, coordinator, and evidence-record lenses.
- Evidence need: read-only reviewer quorum, source/build provenance, generated
  firmware/header parity, focused LCD tests, firmware boundary tests, scaffold
  audits, ESP-IDF no-flash build and hashes, then same-session COM6 identity,
  rollback, write/verify, read-only monitor, cleanup, and physical visual proof.
- Mutation boundary: PF0530W LCD menu firmware/source, generated menu artifacts,
  LCD simulator parity tests, firmware scaffold audit/tests, docs/source
  records, and this task record. No erase, serial command writes, XBee/RF,
  relay GPIO writes, relay-expander writes, MicroSD/TFT, wiring mutation,
  relay/load/mains, persistent config, external services, commit, or push.
- Validation plan: focused generator check, LCD tests, combined firmware/LCD
  unittest set, firmware/source/docs/agent audits, scaffold verify, ESP-IDF
  no-flash build, artifact hash manifest, COM6 live gate after all P1/P2
  blockers closed, and separate physical visual acceptance.

## Reviewer Disposition

- Coordinator/architecture-risk, weight 5: blocked immediate live flash; allowed
  proceed only after exact firmware candidate, source/build validation,
  same-session COM6 identity, rollback, hashes, and recovery path.
- Live-bench gate, weight 5: conditional approval for evidence collection and
  eventual COM6-only write/verify; blocked immediate flash.
- ESP32 firmware/device, weight 3: blocked flash of stale/host-only artifacts;
  conditional approval for a future no-flash build/test gate.
- LCD UX, weight 3: conditional approval for future visual proof; blocked any
  claim that `bbs_lcd_art.v1` was firmware-visible before this task.
- Power/wiring/isolation, weight 3: conditional approval for COM6-only
  low-voltage flash lane; hard block for wiring, relay/load/mains, XBee/RF,
  serial-command writes, DMM/current, or power-supply expansion.
- QA validation, weight 3: conditional approval for a narrowly scoped Tier 3
  gate after source/build provenance and pre-flash evidence.

Weighted disposition for immediate flash: blocked by P1 blockers. Weighted
disposition for this source/build integration path: accepted as the required
next gate to remove the firmware-applicability blocker. Lifecycle state listing
was unavailable; spawned reviewers were waited on and closed after output
capture.

## Implementation Summary

- Bumped active LCD menu source identity to `PF0530W`.
- Added `art_panel` as the seventh generated glyph bank.
- Added HOME navigation to a new `ART` page.
- Added firmware `art_panel` CGRAM rows and a fixed 4x20 custom-character tile
  map that displays the compiler sample art panel on the physical LCD frame.
- Preserved the PF0530V PCNT encoder path, GPIO13/GPIO14/GPIO32 input-only
  policy, GPIO21/GPIO22 LCD display-only policy, closed bridge, and no
  relay/load/mains mutation.
- Added simulator parity for the `ART` page and focused tests for the compiled
  slot preview.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
  (30 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_firmware_encoder_pullup_boundary tests.scaffold_audits.test_firmware_pcnt_accumulator tests.lcd_bbs_menu.test_lcd_bbs_menu`
  (40 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `git diff --check`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
  (32 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
  (85 tests).
- PASS: ESP-IDF v6.0.1 no-flash build to
  `/tmp/esp32-pf0530w-visual-art-build`.
- PASS: build artifact hashes retained in the PF0530W live source ledger:
  bootloader `<redacted-sha256>`,
  partition table `<redacted-sha256>`,
  app `<redacted-sha256>`.
- PASS: PF0530W COM6 live flash gate recorded in
  [2026-06-02-four-relay-ky040-bbs-lcd-menu-pf0530w-live.md](../../knowledge-base/source-ledger/2026-06-02-four-relay-ky040-bbs-lcd-menu-pf0530w-live.md)
  and
  [0143-four-relay-ky040-bbs-lcd-menu-pf0530w-live.md](0143-four-relay-ky040-bbs-lcd-menu-pf0530w-live.md).
- Pending: physical LCD ART page visual acceptance and post-navigation ART
  transcript characterization.

## Closed Surfaces

No physical art-page visual acceptance is claimed by this source/build record
alone. No erase, serial command writes, XBee/RF, ESP-NOW runtime expansion,
relay GPIO writes, relay-expander writes, MicroSD/TFT, wiring mutation,
relay/load/mains, persistent config, external services, release, commit, or
push is authorized.

## Decision Footer

Decision: `pf0530w_live_flashed_art_visual_acceptance_pending`. Next gate:
physical LCD navigation to the ART page, visual acceptance of the 4x20
custom-character art panel, and optional read-only transcript characterization
of ART page render output. Owner: Firmware with Live Bench, QA, LCD UX,
Hardware Safety, and Evidence Records.
