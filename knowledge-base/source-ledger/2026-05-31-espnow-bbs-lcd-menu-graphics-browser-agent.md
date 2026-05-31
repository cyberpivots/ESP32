# ESP-NOW BBS LCD Menu Graphics, Browser Mirror, And Agent Source Ledger - 2026-05-31

Source index: [../source-index.md](../source-index.md)

## Source IDs

- `SRC-LOCAL-ESPNOW-BBS-LCD-MENU-GRAPHICS-BROWSER-AGENT-2026-05-31`
- `SRC-HITACHI-HD44780U-DDRAM-CGRAM-2026-05-31`
- `SRC-NXP-HD44780-4X20-DDRAM-2026-05-31`
- `SRC-LUMA-LCD-HD44780-2026-05-31`
- `SRC-ESPRUINO-HD44780-2026-05-31`
- `SRC-VREMULCD-2026-05-31`
- `SRC-LCDMENU-ROTARY-ENCODER-2026-05-31`
- `SRC-ESP-IDF-HTTP-SERVER`
- `SRC-ESP-IDF-WIFI`
- `SRC-CODEX-CUSTOM-AGENTS-2026-05-23`
- `SRC-CODEX-CONFIG-REFERENCE-2026-05-27`

## Purpose

Record the source basis and validation evidence for the Tier 2 host-only LCD
menu graphics, browser mirror, and recallable-agent continuation.

## Verified Facts

- [repo-verified] The task adds `bbs_lcd_render.v1` as the renderer/browser
  output schema while preserving `bbs_lcd_state.v1` as the input schema.
- [repo-verified] The renderer still emits exactly four 20-character lines and
  rejects secret-bearing fields recursively.
- [repo-verified] The renderer now reports cursor row/column, HD44780 DDRAM
  address, focus state, dirty rows, dirty cells, widgets, and a named glyph
  bank.
- [repo-verified] The host glyph-bank manager defines `core_status`,
  `horizontal_bar`, `vertical_chart`, `big_digits`, and `gauge_demo`, enforces
  eight slots, enforces 5-bit row bytes, and throttles bank swaps at 250 ms.
- [repo-verified] The browser mirror is a Python request shim and static HTML
  generator. It opens no socket, starts no server, and includes no active
  browser network, serial, Bluetooth, GPIO, relay, flash, erase, XBee, or
  ESP-NOW behavior.
- [source-verified] HD44780 CGRAM planning remains limited to eight 5x8 custom
  character types, and `Set DDRAM address` is the source-backed cursor-address
  operation.
- [source-verified] The 20x4 row-base tuple `0x00`, `0x40`, `0x14`, `0x54` is
  retained as a local renderer and firmware-lineage mapping.
- [source-verified] Luma.LCD, Espruino, vrEmuLcd, and LcdMenu are design
  references only; no dependency or framework selection is added.
- [repo-verified] The `lcd-menu-operations` skill and
  `lcd-menu-ux-reviewer` agent profile are advisory. They preserve
  `AGENTS.md`, operator sovereignty, and the no-live-hardware boundary.

## Assumptions

- Browser mirror claims are limited to host/static behavior and unit tests.
- Physical LCD custom-glyph rendering remains unproven until a later live gate.
- Future ESP-IDF HTTP Server/SoftAP/WebSocket work requires a separate gate.
- The current dirty tree contains unrelated prior work; this task preserves it
  and only adds the named Tier 2 continuation.

## Unknowns

- Physical LCD glyph-bank visual behavior.
- Encoder direction/select proof and PF0530K interactivity.
- Target firmware memory budget for any future browser mirror.
- Network/security policy for any future SoftAP or HTTP endpoint.
- Exact LCD backpack electrical behavior, pullup voltage, and rail margin.

## Reviewer Quorum

Read-only subagents and local role lenses approved mutation start before code
edits. No P1/P2 blockers remained inside the host-only boundary.

- Coordinator/Architecture-risk, weight 5: approved host-only mutation.
- Agent Operations/Skill, weight 3: approved skill/agent/config updates with
  operator-sovereignty language.
- UI/Host-Code Protocol, weight 3: approved if browser mirror stays inert and
  local.
- QA, weight 3: approved with browser-specific tests required before browser
  acceptance.
- Evidence Records, weight 2: approved with a new source ledger and
  source-index row.

Weighted approval: 16/16 for mutation start. Browser acceptance is conditioned
on passing focused browser-mirror tests.

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
- this source ledger
- `.codex/skills/lcd-menu-operations/SKILL.md`
- `.codex/agents/lcd-menu-ux-reviewer.toml`
- `.codex/config.toml`
- `.agents/TASK_LOG/0115-espnow-bbs-lcd-menu-graphics-browser-agent.md`
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

## Stop Gates

This source record does not authorize live flash, prepare/flash/complete,
monitor, serial writes, serial-write expansion, XBee/RF, ESP-NOW live runtime,
relay GPIO writes, relay-expander writes, TFT, MicroSD, wiring mutation, load,
mains, erase, firmware ABI changes, bridge ABI changes, coordinator serial ABI
changes, Gate F service-code changes, `mesh_discovery.v1` changes, Win31
transport changes, persistent configuration endpoints, framework changes
outside accepted ADRs, release gating, commit, or push.
