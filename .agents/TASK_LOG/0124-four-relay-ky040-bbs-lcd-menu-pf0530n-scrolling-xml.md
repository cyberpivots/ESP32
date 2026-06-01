# Four Relay KY-040 BBS LCD Menu PF0530N Scrolling/XML

Status: PF0530N non-live scrolling/XML source/test update validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-01

## Routing

- Selected tier: Tier 2 because this changes firmware source, generated static
  firmware data, host simulator behavior, XML tooling, tests, audits, docs, and
  durable records, but does not touch live hardware.
- Owner role: Firmware with LCD UI/UX, QA, Evidence Records, and
  Hardware-safety lenses.
- Evidence need: source diff, XML parser/generator tests, host LCD/menu
  scrolling tests, firmware audit tests, scaffold audits, optional ESP-IDF
  v6.0.1 no-flash build, source ledger, docs/status updates, and this task log.
- Mutation boundary: firmware source/generated header, host LCD menu
  simulator/XML/tooling/tests, focused scaffold audits, ESP-NOW/four-relay LCD
  docs, source-index/source-ledger, status records, and this task/handoff pair.
- Gate authority: non-live source/test/docs only.

## Verified Facts

- PF0530N changes the active firmware ID to `PF0530N`, keeps
  `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, keeps GPIO13/GPIO14/GPIO32 input-only, and
  keeps LCD writes display-only on GPIO21/GPIO22.
- PF0530N adds `bbs_lcd_menu.v1` XML as the build-time menu source and
  generated static firmware/simulator menu definitions.
- The firmware source includes the generated header and advertises
  `bbs_lcd_menu.v1`, `bbs_lcd_render.v2`, generated item count, scroll-list
  behavior, marquee timing, and table glyph readiness.
- The host renderer emits `bbs_lcd_render.v2` with viewport metadata, selected
  item ID, visible item IDs, physical indicator row, viewport top line,
  horizontal scroll offsets, and source XML metadata.
- The host menu supports more than four options per page, moving indicator row
  behavior, viewport scrolling at edges, grouped multi-row items, selected-row
  marquee, XML-defined page targets, local detail/edit modes, and table glyph
  bank rendering.

## Assumptions

- PF0530N remains source/test-only until a separate Tier 3 live gate is opened.
- The host simulator is an acceptance aid for XML, menu state behavior, and
  display bounds; it does not prove physical LCD rendering.
- Closed bridge text means local display of bridge state only. It does not
  open XBee/RF, ESP-NOW runtime, serial-write expansion, or bridge ABI changes.

## Unknowns

- PF0530N live behavior if flashed remains unknown.
- Physical LCD readability of the scroll-list and table page remains unknown.
- Final runtime BBS/XBee payload mapping remains a future integration lane.

## Reviewer Quorum

- Coordinator/Architecture-risk, weight 5: approve Tier 2 non-live mutation
  start; block live hardware authority.
- Firmware, weight 3: approve bounded source/test mutation if the generated
  firmware data stays static and no runtime XML parser is added.
- LCD UX/model, weight 3: deny v2 acceptance before implementation; required
  XML/list/marquee/table tests before acceptance.
- QA, weight 3: approve implementation start and require XML/scroll tests,
  generated freshness checks, and durable records before acceptance.
- Evidence Records, weight 2: approve records/source-index mutation if claims
  stay source/test-only.
- Security/Safety, weight 3: deny acceptance before generated artifacts exist;
  required fail-closed XML and closed live-surface controls.

Weighted disposition for mutation start: 16/19 approve with the denials scoped
to acceptance of not-yet-existing PF0530N artifacts. No substantive P1/P2
blocker remained inside the non-live implementation boundary after XML,
generator, tests, generated artifacts, and records were added. No live
authority is granted.

## Implementation

- Added `bbs_lcd_menu.v1.xml` under the LCD simulator area.
- Added `generate_lcd_menu.py` with fail-closed XML validation and `--check`.
- Generated host model `generated_menu.py` and firmware static header
  `bbs_lcd_menu_generated.h`.
- Updated the host renderer to emit `bbs_lcd_render.v2`, consume generated
  XML model data, scroll item lists vertically, render grouped multi-row items,
  horizontally marquee selected overlong rows, and expose viewport metadata.
- Added a `table` glyph bank and `ROUTES` page while keeping bar/chart/digit/
  gauge banks separate.
- Updated firmware source to use generated static page/item metadata, firmware
  ID `PF0530N`, the generated 14-page/63-item menu counts, scroll-list
  selection state, a bounded page stack, table glyph bank, and v2 readiness
  proof strings.
- Updated focused host and firmware audit tests for XML parsing, generated
  freshness, scroll-list behavior, marquee timing, table glyph constraints,
  browser inertness, firmware ID, generated static definitions, and closed
  GPIO/I2C boundaries.

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/scaffold_audits/test_firmware_encoder_pullup_boundary.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_data.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `git diff --check`
- ESP-IDF v6.0.1 no-flash build if the local activation script/toolchain is
  available.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/simulators/lcd_bbs_menu/generate_lcd_menu.py --check`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py` (22 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'` (22 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/scaffold_audits/test_firmware_encoder_pullup_boundary.py` (4 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_firmware.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py` (32 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_data.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'` (55 tests)
- PASS: ESP-IDF v6.0.1 no-flash build:
  `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh && idf.py -C firmware/projects/four-relay-xbee-wifi -B <redacted-temp-build-dir> build`
  generated `four_relay_xbee_wifi.bin` size `0x2d3c0`, with `0xd2c40` bytes
  (82 percent) free in the smallest app partition.
- PASS: `git diff --check`

## Closed Surfaces

No COM6 access, flash, monitor, serial write, RF/XBee write, ESP-NOW live
runtime, relay GPIO write, relay-expander write, MicroSD/TFT action, wiring
mutation, DMM/current measurement, load, mains, erase, firmware HTTP/SoftAP/
WebSocket runtime, persistent configuration endpoint, external service change,
GitHub publication, release, commit, or push is opened by this task.

## Decision Footer

Decision: `ready_for_mutation` within the non-live PF0530N source/test/docs
boundary. Next useful gate is QA review of PF0530N, or a fresh Tier 3 gate for
any live device action. Authority limits remain no COM6, flash, monitor,
serial writes, RF/XBee writes, relay/load/mains, wiring, DMM, persistent
config, publication, commit, or push.
