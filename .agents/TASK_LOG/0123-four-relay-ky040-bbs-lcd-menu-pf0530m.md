# Four Relay KY-040 BBS LCD Menu PF0530M

Status: PF0530M non-live menu behavior source/test update validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-01

## Routing

- Selected tier: Tier 2 because this changes firmware source, host simulator
  behavior, tests, audits, and durable records, but does not touch live
  hardware.
- Owner role: Firmware with LCD UI/UX, QA, Evidence Records, and
  Hardware-safety lenses.
- Evidence need: PF0530L accepted visual/electrical record, source diff,
  host-side LCD/menu state-machine tests, firmware audit tests, scaffold audits,
  optional ESP-IDF v6.0.1 no-flash build, source ledger, docs/status updates,
  and this task log.
- Mutation boundary: `firmware/projects/four-relay-xbee-wifi/`, host LCD menu
  simulator/tests, focused scaffold audits, ESP-NOW/four-relay LCD docs,
  source-index/source-ledger, status records, and this task/handoff pair.
- Gate authority: non-live source/test/docs only.

## Verified Facts

- PF0530L serial/menu physical interaction, LCD visual readability, glyph/page
  readability, and user-confirmed electrical/DMM acceptance are recorded under
  `SRC-LOCAL-TIER3-COM6-ATTENDED-INTERACTION-PROOF-2026-05-31` and
  `SRC-LOCAL-LCD-GLYPH-ELECTRICAL-ACCEPTANCE-2026-05-31`.
- PF0530M changes the active firmware ID to `PF0530M`, keeps
  `FR_DIAG_XBEE_BRIDGE_CLOSED 1`, keeps GPIO13/GPIO14/GPIO32 input-only, and
  keeps LCD writes display-only on GPIO21/GPIO22.
- PF0530M replaces the PF0530L demo-heavy page text with operational 20x4 BBS
  pages: status, messages, peers, queue/files, mesh, local bridge closed,
  diagnostics/errors, locks, and widget pages.
- PF0530M adds source-visible detail/action labeling and row editability so
  short press enters edit mode only on named widget rows.
- The host simulator now mirrors the 13-page PF0530M page set, page-specific
  glyph bank selection, detail/edit/back behavior, and 20-character text bounds.
- Focused validation passed for the LCD/menu tests, firmware encoder boundary
  tests, and firmware scaffold audit.

## Assumptions

- PF0530M remains source/test-only until a separate Tier 3 live gate is opened.
- The host simulator is an acceptance aid for menu state behavior and display
  bounds; it does not prove physical LCD rendering.
- Closed bridge text means local display of bridge state only. It does not open
  XBee/RF, ESP-NOW runtime, serial-write expansion, or bridge ABI changes.

## Unknowns

- PF0530M live behavior if flashed remains unknown.
- Final runtime BBS/XBee payload mapping remains a future integration lane.
- Clockwise/counter-clockwise human direction labeling remains a user preference
  issue unless a later gate defines the required mapping.

## Reviewer Quorum

- Coordinator/Architecture-risk, weight 5: approve Tier 2 non-live boundary;
  block live hardware authority.
- Firmware, weight 5: approve source/test update because it stays inside the
  existing PF0530L/PF0530K architecture and keeps closed surfaces closed.
- Hardware/Safety, weight 3: approve because no wiring, DMM, relay, RF, flash,
  or live monitor action occurs.
- QA, weight 3: approve with focused host state-machine tests, firmware audit
  tests, scaffold audits, and no-flash build where available.
- Evidence Records, weight 2: approve if source-index, ledger, docs index, task
  log, and handoff are updated.

Weighted disposition: 18/18 pass for the named Tier 2 mutation boundary. No
P1/P2 blocker remains inside the non-live boundary. No live authority is
granted.

## Implementation

- Changed active firmware ID from `PF0530L` to `PF0530M`.
- Added firmware helpers for editable rows, action labels, and context/status
  line formatting.
- Changed non-editable detail short press to return to row browsing with a
  `DETAIL OK` acknowledgement instead of entering edit mode.
- Restricted edit mode to the widget rows intended to be locally editable:
  `BARS` row 3 and `GAUGE` row 1.
- Updated firmware LCD rows to operational BBS status, message, peer, bridge,
  diagnostic/error, and widget content.
- Updated `BBS_INPUT_READY` to advertise `actions=detail,edit,back`.
- Expanded host simulator `PAGES` to all 13 firmware pages and added
  `bridge`/`errors` snapshot fields.
- Added host simulator page-specific glyph-bank selection, detail/edit/back
  state behavior, editable-row limits, and 20-character render checks.

## Validation Plan

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

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py` (20 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'` (20 tests)
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
- PASS: `git diff --check`
- PASS: ESP-IDF v6.0.1 no-flash build to
  `<redacted-temp-build-dir>`; app binary size
  `0x2bbf0`, with `0xd4410` bytes free in the 1 MiB factory app partition.

## Closed Surfaces

No COM6 access, flash, monitor, serial write, RF/XBee write, ESP-NOW live
runtime, relay GPIO write, relay-expander write, MicroSD/TFT action, wiring
mutation, DMM/current measurement, load, mains, erase, firmware HTTP/SoftAP/
WebSocket runtime, persistent configuration endpoint, external service change,
GitHub publication, release, commit, or push is opened by this task.

## Decision Footer

Decision: `ready_for_mutation` within the non-live PF0530M source/test
boundary. Next useful gate is continued non-live BBS/XBee payload display or
SoftAP/browser mirror work, or a fresh Tier 3 gate for any live device action.
Authority limits remain no COM6, flash, monitor, serial writes, RF/XBee writes,
relay/load/mains, wiring, DMM, persistent config, publication, commit, or push.
