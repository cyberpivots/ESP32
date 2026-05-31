# Task 0115: ESP-NOW BBS LCD Menu Graphics, Browser Mirror, And Agent

Status: implemented; validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-05-31

## Goal

Implement the Tier 2 host-only LCD menu graphics/browser/agent continuation:
renderer output schema, cursor and dirty metadata, named glyph banks, widgets,
inert browser mirror, focused tests, source records, docs, and recallable
skill/agent configuration.

## Verified Facts

- `bbs_lcd_state.v1` remains the host renderer input schema.
- `bbs_lcd_render.v1` is now the host renderer/browser output schema.
- The renderer still emits exactly four 20-character LCD lines and rejects
  secret-bearing fields recursively.
- PF0530K is flashed/verify-flashed for user testing but is not accepted as
  interactive because the live transcript captured zero `ENC_RAW`, `ENC_EV`,
  `BBS_MENU_STEP`, and `BBS_MENU_SELECT`.
- The browser mirror is host-only: a Python request shim plus static HTML
  generator, not a live server.

## Assumptions

- Custom glyph and browser work remain simulator-first until a later live gate.
- Rotary events produce local UI intent only.
- Future ESP32 HTTP/SoftAP/WebSocket work requires a separate network,
  security, selected-board, and live proof gate.

## Unknowns

- Physical LCD visual behavior under custom glyph bank swaps.
- Encoder direction/select proof after PF0530K.
- Firmware memory budget for a future browser mirror.
- Exact LCD backpack electrical behavior, pullup voltage, and rail margin.
- Whether live firmware should expose SoftAP before a separate security gate.

## Reviewer Quorum

Read-only reviewer quorum approved the named Tier 2 boundary before mutation.

- Coordinator/Architecture-risk, weight 5: approved.
- Agent Operations/Skill, weight 3: approved.
- UI/Host-Code Protocol, weight 3: approved.
- QA, weight 3: approved with browser-specific tests required.
- Evidence Records, weight 2: approved with new source records.

Weighted approval: 16/16. No P1/P2 blockers remained for mutation start.

## Mutation Boundary

- `tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py`
- `tools/simulators/lcd_bbs_menu/README.md`
- `tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `tests/README.md`
- `docs/projects/espnow-bbs/lcd-menu-graphics-browser-agent-plan.md`
- `docs/projects/espnow-bbs/lcd-encoder-field-console-plan.md`
- `docs/projects/espnow-bbs/README.md`
- `docs/projects/four-relay-xbee-wifi/README.md`
- `docs/index.md`
- `knowledge-base/source-index.md`
- `knowledge-base/source-ledger/2026-05-31-espnow-bbs-lcd-menu-graphics-browser-agent.md`
- `.codex/skills/lcd-menu-operations/SKILL.md`
- `.codex/agents/lcd-menu-ux-reviewer.toml`
- `.codex/config.toml`
- this task record
- `.agents/handoffs/0085-espnow-bbs-lcd-menu-graphics-browser-agent-to-qa.md`

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- Changed-file source-ID scan.
- Changed-file Markdown link check.
- Closed-surface scan.
- `git diff --check`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/lcd_bbs_menu/test_lcd_bbs_menu.py` (16 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'` (16 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/custom_wireless_protocol/test_espnow_bbs_custom_protocol.py` (32 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'` (49 tests)
- PASS: `.codex/config.toml` and `.codex/agents/*.toml` parse check.
- PASS: changed-file source-ID scan over 11 Markdown/skill files.
- PASS: changed-file Markdown link scan over 10 Markdown files.
- PASS: closed-surface scan reviewed expected closed/no-authority hits.
- PASS: `git diff --check`

## Handoff

Continue with
[../handoffs/0085-espnow-bbs-lcd-menu-graphics-browser-agent-to-qa.md](../handoffs/0085-espnow-bbs-lcd-menu-graphics-browser-agent-to-qa.md).

## Closed Surfaces

Live flash, prepare/flash/complete, monitor, serial writes, serial-write
expansion, XBee/RF, ESP-NOW live runtime, relay GPIO writes,
relay-expander writes, TFT, MicroSD, wiring mutation, load, mains, erase,
firmware ABI changes, bridge ABI changes, coordinator serial ABI changes, Gate
F service-code changes, `mesh_discovery.v1` changes, Win31 transport changes,
persistent configuration endpoints, framework changes outside accepted ADRs,
release gating, commit, and push remain closed.
