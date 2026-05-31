---
name: lcd-menu-operations
description: Use for ESP32 workspace LCD menu, rotary encoder, HD44780/PCF8574, custom glyph bank, browser mirror, copied LCD/browser evidence review, and host-only LCD simulator work.
---

# LCD Menu Operations

1. Re-read `AGENTS.md`, `.agents/GOVERNANCE.md`, `.agents/OWNERSHIP.md`,
   `.agents/ROLES.md`, `docs/index.md`, and `knowledge-base/source-index.md`
   before edits.
2. Keep verified facts, assumptions, unknowns, and stop gates separate in
   routing packets and durable records.
3. Use `docs/projects/espnow-bbs/lcd-encoder-field-console-plan.md` for the
   base `bbs_lcd_state.v1` contract and
   `docs/projects/espnow-bbs/lcd-menu-graphics-browser-agent-plan.md` for
   `bbs_lcd_render.v1`, cursor, glyph, widget, and browser-mirror work.
4. Treat `tools/simulators/lcd_bbs_menu/lcd_bbs_menu.py` and
   `tests/lcd_bbs_menu/test_lcd_bbs_menu.py` as the first validation surface
   for host-only LCD UX behavior.
5. Preserve the local UI-intent boundary: rotate and press events may change
   pages, rows, detail state, or local edit/demo state only.
6. Keep closed lanes closed unless a later explicit gate opens them: relay,
   XBee/RF, ESP-NOW runtime, flash/erase, monitor, serial-write, MicroSD, TFT,
   wiring, load, mains, persistent configuration endpoints, release gating,
   commit, and push.
7. Do not claim physical LCD custom-glyph readability, encoder direction,
   button select, rail margin, LCD backpack electrical behavior, SoftAP, or
   firmware browser behavior without same-session evidence and the relevant
   Tier 3 gate.
8. For repeated work, run the focused LCD tests first, then broader scaffold and
   source/docs audits if docs, records, skills, agents, or config changed.
