#!/usr/bin/env python3
"""Tests for the host-only LCD BBS menu renderer."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SIM_DIR = ROOT / "tools" / "simulators" / "lcd_bbs_menu"
sys.path.insert(0, str(SIM_DIR))

from generate_lcd_menu import (  # noqa: E402
    FIRMWARE_ID,
    MENU_SCHEMA,
    RENDER_SCHEMA,
    FW_HEADER_PATH,
    MenuGenerationError,
    load_menu,
)
from generated_menu import PAGES as GENERATED_PAGES, SOURCE_ID  # noqa: E402
from lcd_bbs_menu import (  # noqa: E402
    API_INTENT_PATH,
    API_STATE_PATH,
    GLYPH_BANK,
    GLYPH_BANKS,
    INPUT_EVENTS,
    LCD_ART_PIXEL_HEIGHT,
    LCD_ART_PIXEL_WIDTH,
    LCD_ART_SCHEMA,
    LCD_COLUMNS,
    LCD_CONTENT_COLUMNS,
    LCD_DDRAM_ROW_BASES,
    LCD_ROWS,
    MARQUEE_HOLD_MS,
    MARQUEE_STEP_MS,
    PAGES,
    SNAPSHOT_SCHEMA,
    CursorTracker,
    Glyph,
    GlyphBank,
    GlyphBankManager,
    LcdBrowserMirror,
    LcdMenuError,
    MenuViewState,
    apply_input,
    big_digits,
    build_browser_document,
    compile_lcd_art_from_pbm,
    compile_lcd_art_tile_map,
    gauge_demo,
    glyph_bank_for_page,
    horizontal_bar,
    render,
    sample_art_panel,
    sample_state,
    signal_bars,
    slider,
    spinner_frame,
    vertical_chart,
)


class LcdBbsMenuTests(unittest.TestCase):
    def test_home_lines_are_exactly_20_cells_and_v2(self) -> None:
        rendered = render(sample_state())
        self.assertEqual(rendered.schema, RENDER_SCHEMA)
        self.assertEqual(rendered.source_xml_version, MENU_SCHEMA)
        self.assertEqual(rendered.firmware_id, FIRMWARE_ID)
        self.assertEqual(rendered.source_id, SOURCE_ID)
        self.assertEqual(len(rendered.lines), LCD_ROWS)
        self.assertTrue(all(len(line) == LCD_COLUMNS for line in rendered.lines))
        self.assertEqual(rendered.lines[0], ">BBS FIELD STATUS RE")
        self.assertEqual(rendered.viewport["selected_item_id"], "home-status")
        self.assertEqual(rendered.viewport["visible_item_ids"][0], "home-status")

    def test_generated_menu_files_are_fresh(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SIM_DIR / "generate_lcd_menu.py"), "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('FR_DIAG_FIRMWARE_ID_VALUE "PF0530W"', FW_HEADER_PATH.read_text(encoding="utf-8"))

    def test_xml_source_generates_pages_and_table_bank(self) -> None:
        pages = load_menu()
        self.assertEqual(len(pages), 15)
        self.assertEqual(PAGES[0], "HOME")
        self.assertIn("ROUTES", PAGES)
        routes = next(page for page in GENERATED_PAGES if page["id"] == "ROUTES")
        self.assertEqual(routes["glyph_bank"], "table")
        self.assertEqual(routes["items"][0]["id"], "routes-table")
        self.assertEqual(routes["items"][0]["rows"][0], "coord01|-67 |2")

    def test_xml_rejections_fail_closed(self) -> None:
        cases = {
            "target_unknown": '<menu schema="bbs_lcd_menu.v1" sourceId="PF0530W"><page id="HOME" title="H" glyphBank="core_status"><item id="i1" label="Bad" action="page" target="NOPE" /></page></menu>',
            "duplicate_item": '<menu schema="bbs_lcd_menu.v1" sourceId="PF0530W"><page id="HOME" title="H" glyphBank="core_status"><item id="dup" label="A" action="detail" /><item id="dup" label="B" action="detail" /></page></menu>',
            "bad_glyph": '<menu schema="bbs_lcd_menu.v1" sourceId="PF0530W"><page id="HOME" title="H" glyphBank="bad"><item id="i1" label="A" action="detail" /></page></menu>',
            "wide_table": '<menu schema="bbs_lcd_menu.v1" sourceId="PF0530W"><page id="HOME" title="H" glyphBank="table"><item id="i1" label="12345678901234567890" action="detail" table="true" /></page></menu>',
            "bad_token": '<menu schema="bbs_lcd_menu.v1" sourceId="PF0530W"><page id="HOME" title="H" glyphBank="core_status"><item id="i1" label="{secret.value}" action="detail" /></page></menu>',
            "secret_attr": '<menu schema="bbs_lcd_menu.v1" sourceId="PF0530W"><page id="HOME" title="H" glyphBank="core_status"><item id="i1" label="A" action="detail" pairing_token="x" /></page></menu>',
            "doctype": '<!DOCTYPE menu [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]><menu schema="bbs_lcd_menu.v1" sourceId="PF0530W"><page id="HOME" title="H" glyphBank="core_status"><item id="i1" label="A" action="detail" /></page></menu>',
        }
        for name, xml in cases.items():
            with self.subTest(name=name), tempfile.NamedTemporaryFile("w", suffix=".xml", delete=False) as handle:
                handle.write(xml)
                path = Path(handle.name)
            try:
                with self.assertRaises(MenuGenerationError):
                    load_menu(path)
            finally:
                path.unlink(missing_ok=True)

    def test_glyph_bank_bounds_include_table(self) -> None:
        rendered = render(sample_state())
        self.assertEqual(rendered.glyph_bank_name, "core_status")
        self.assertEqual(rendered.glyph_bank, GLYPH_BANK)
        self.assertEqual(set(GLYPH_BANKS), set(["core_status", "horizontal_bar", "vertical_chart", "big_digits", "gauge", "table", "art_panel"]))
        for bank in GLYPH_BANKS.values():
            self.assertLessEqual(len(bank.glyphs), 8)
            for expected_slot, glyph in enumerate(bank.glyphs):
                self.assertEqual(glyph.slot, expected_slot)
                self.assertEqual(len(glyph.rows), 8)
                self.assertTrue(all(0 <= row <= 0x1F for row in glyph.rows))

        manager = GlyphBankManager()
        with self.assertRaisesRegex(LcdMenuError, "glyph_bank_swap_throttled"):
            manager.select("table", now_ms=100)
        self.assertEqual(manager.select("table", now_ms=250).name, "table")
        with self.assertRaisesRegex(LcdMenuError, "glyph_bank_overflow"):
            GlyphBank("too_many", tuple(Glyph(index, f"g{index}", (0,) * 8) for index in range(9)))
        with self.assertRaisesRegex(LcdMenuError, "glyph_row_byte_invalid"):
            GlyphBank("bad_row", (Glyph(0, "bad", (0x20,) * 8),))

    def test_all_xml_pages_render_with_expected_glyph_bank(self) -> None:
        self.assertEqual(len(PAGES), 15)
        for page in PAGES:
            rendered = render(sample_state(), MenuViewState(page=page))
            self.assertEqual(len(rendered.lines), LCD_ROWS)
            self.assertTrue(all(len(line) == LCD_COLUMNS for line in rendered.lines))
            self.assertEqual(rendered.glyph_bank_name, glyph_bank_for_page(page))
            self.assertEqual(rendered.schema, "bbs_lcd_render.v2")

    def test_art_page_renders_compiled_slot_preview(self) -> None:
        rendered = render(sample_state(), MenuViewState(page="ART"))
        art = sample_art_panel()
        self.assertEqual(rendered.firmware_id, "PF0530W")
        self.assertEqual(rendered.glyph_bank_name, "art_panel")
        self.assertEqual(rendered.lines, art.preview_lines)
        self.assertEqual(rendered.viewport["art_panel"]["schema"], LCD_ART_SCHEMA)
        self.assertEqual(rendered.viewport["art_panel"]["cell_slots"], [list(row) for row in art.cell_slots])

    def test_more_than_four_options_scroll_vertically(self) -> None:
        view = MenuViewState(page="HOME")
        for _ in range(4):
            view = apply_input(view, "rotate_right")
        self.assertEqual(view.selected_item, 4)
        self.assertEqual(view.viewport_top_line, 1)
        self.assertEqual(view.selected_row, 3)
        rendered = render(sample_state(), view)
        self.assertEqual(rendered.viewport["selected_item_id"], "home-mesh")
        self.assertEqual(rendered.lines[3], ">Mesh routes table  ")

    def test_indicator_moves_before_viewport_scrolls(self) -> None:
        view = MenuViewState(page="HOME")
        rows = []
        tops = []
        for _ in range(4):
            rendered = render(sample_state(), view)
            rows.append(rendered.viewport["physical_indicator_row"])
            tops.append(rendered.viewport["viewport_top_line"])
            view = apply_input(view, "rotate_right")
        self.assertEqual(rows, [0, 1, 2, 3])
        self.assertEqual(tops, [0, 0, 0, 0])

    def test_short_press_follows_xml_target_and_long_press_backs_stack(self) -> None:
        view = MenuViewState(page="HOME")
        view = apply_input(view, "rotate_right")
        view = apply_input(view, "short_press")
        self.assertEqual(view.page, "MESSAGES")
        self.assertEqual(view.page_stack, ("HOME",))
        self.assertEqual(view.last_intent, "page:MESSAGES")
        view = apply_input(view, "long_press")
        self.assertEqual(view.page, "HOME")
        self.assertEqual(view.page_stack, ())
        view = apply_input(view, "long_press")
        self.assertEqual(view.page, "HOME")
        self.assertEqual(view.last_intent, "home")

    def test_detail_and_edit_modes_are_local_only(self) -> None:
        detail = apply_input(MenuViewState(page="HOME"), "short_press")
        self.assertEqual(detail.mode, "detail")
        self.assertEqual(detail.last_intent, "detail:home-status")
        back = apply_input(detail, "long_press")
        self.assertEqual(back.mode, "scroll")

        edit = MenuViewState(page="BARS", selected_item=2)
        edit = apply_input(edit, "short_press")
        self.assertEqual(edit.mode, "edit_lab")
        edit = apply_input(edit, "rotate_right")
        self.assertEqual(edit.edit_value, 5)
        edit = apply_input(edit, "short_press")
        self.assertEqual(edit.mode, "detail")
        self.assertEqual(edit.last_intent, "local_commit")

    def test_grouped_multirow_item_selects_only_first_row(self) -> None:
        rendered = render(sample_state(), MenuViewState(page="ROUTES"))
        self.assertEqual(rendered.glyph_bank_name, "table")
        self.assertEqual(rendered.viewport["selected_item_id"], "routes-table")
        self.assertEqual(rendered.lines[0], ">NODE |RSSI|Q       ")
        self.assertEqual(rendered.lines[1], ":coord01|-67 |2     ")
        self.assertEqual(rendered.lines[2], ":peer02 |-71 |0     ")
        self.assertEqual(rendered.lines[3], ":peer03 |-82 |1     ")

        moved = apply_input(MenuViewState(page="ROUTES"), "rotate_right")
        self.assertEqual(moved.selected_item, 1)
        self.assertEqual(moved.selected_row, 3)
        self.assertEqual(render(sample_state(), moved).lines[3], ">Back mesh          ")

    def test_selected_overlong_text_scrolls_and_unselected_clips(self) -> None:
        view = MenuViewState(page="MESSAGES", selected_item=3)
        at_start = render(sample_state(), view, now_ms=0)
        after_hold = render(sample_state(), view, now_ms=MARQUEE_HOLD_MS + MARQUEE_STEP_MS)
        self.assertEqual(at_start.viewport["horizontal_scroll_offsets"][3], 0)
        self.assertEqual(after_hold.viewport["horizontal_scroll_offsets"][3], 1)
        self.assertNotEqual(at_start.lines[3], after_hold.lines[3])
        self.assertEqual(at_start.lines[1], "|Outbox pending ackn")
        self.assertEqual(after_hold.lines[1], "|Outbox pending ackn")
        self.assertEqual(len(after_hold.lines[3]), LCD_COLUMNS)
        self.assertEqual(LCD_CONTENT_COLUMNS, 19)

    def test_marquee_resets_on_selection_change(self) -> None:
        selected = render(sample_state(), MenuViewState(page="MESSAGES", selected_item=3), now_ms=2000)
        moved = apply_input(MenuViewState(page="MESSAGES", selected_item=3), "rotate_right")
        moved_render = render(sample_state(), moved, now_ms=0)
        self.assertGreater(selected.viewport["horizontal_scroll_offsets"][3], 0)
        self.assertEqual(moved_render.viewport["horizontal_scroll_offsets"][3], 0)

    def test_missing_data_and_secret_fields(self) -> None:
        state = {"schema": SNAPSHOT_SCHEMA}
        rendered = render(state)
        self.assertEqual(rendered.lines[0], ">BBS FIELD STATUS RE")

        state = sample_state()
        state["mesh"] = {"pairing_token": "do-not-render"}
        with self.assertRaisesRegex(LcdMenuError, "secret_field_rejected"):
            render(state)

        state = sample_state()
        state["extra"] = "not in bbs_lcd_state.v1"
        with self.assertRaisesRegex(LcdMenuError, "field_unknown"):
            render(state)

    def test_double_click_is_not_a_v2_input(self) -> None:
        with self.assertRaisesRegex(LcdMenuError, "unsupported_input"):
            apply_input(MenuViewState(), "double_click")

    def test_closed_surface_labels_do_not_emit_commands(self) -> None:
        rendered = render(sample_state(), MenuViewState(page="LOCKS"))
        self.assertEqual(rendered.lines[0], ">Relay LOCK         ")
        self.assertIn("XBee LOCK", rendered.lines[1])
        self.assertIn("Flash LOCK", rendered.lines[2])
        self.assertIn("Serial write LOCK", rendered.lines[3])

    def test_cursor_ddram_mapping_and_dirty_metadata(self) -> None:
        self.assertEqual(LCD_DDRAM_ROW_BASES, (0x00, 0x40, 0x14, 0x54))
        self.assertEqual(CursorTracker.row_column_to_ddram(2, 3), 0x17)
        self.assertEqual(CursorTracker.ddram_to_row_column(0x54), (3, 0))

        base = render(sample_state())
        changed = render(sample_state(), MenuViewState(selected_item=1), previous_lines=base.lines)
        self.assertEqual(changed.cursor.dirty_rows, (0, 1))
        self.assertIn((1, 0), changed.cursor.dirty_cells)

    def test_widget_renderers_are_stable_and_ascii(self) -> None:
        self.assertEqual(horizontal_bar(50, 100, width=10), "[#####-----]")
        self.assertEqual(slider(50, 0, 100, width=5), "|--o--|")
        self.assertEqual(vertical_chart([1, 2, 4], height=2, width=3), ("  #", "###"))
        self.assertEqual(signal_bars(-67), "SIG:###-")
        self.assertEqual(spinner_frame(5), "\\")
        self.assertEqual(gauge_demo(50, 100), "G[---^---]")
        self.assertEqual(big_digits(12), ("    _", "  | _|", "  ||_"))

        rendered = render(sample_state())
        self.assertEqual(rendered.widgets["queue"], "Q~ P2 R1")
        self.assertIn("vertical_chart", rendered.widgets)
        self.assertEqual(rendered.widgets["art_panel"]["schema"], LCD_ART_SCHEMA)
        self.assertEqual(len(rendered.widgets["art_panel"]["preview_lines"]), LCD_ROWS)

    def test_lcd_art_tile_map_dedupes_into_safe_metadata(self) -> None:
        frame = (0x1F, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1F, 0x00)
        diag = (0x10, 0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08)
        tile_map = [[None for _ in range(LCD_COLUMNS)] for _ in range(LCD_ROWS)]
        tile_map[0][0] = frame
        tile_map[0][1] = frame
        tile_map[1][0] = diag

        art = compile_lcd_art_tile_map("BBS Panel", tile_map)
        payload = art.to_dict()

        self.assertEqual(payload["schema"], LCD_ART_SCHEMA)
        self.assertEqual(payload["name"], "bbs_panel")
        self.assertEqual(payload["preview_lines"][0], "00" + (" " * 18))
        self.assertEqual(payload["preview_lines"][1], "1" + (" " * 19))
        self.assertEqual(payload["cell_slots"][0][0], 0)
        self.assertEqual(payload["cell_slots"][0][1], 0)
        self.assertEqual(payload["cell_slots"][1][0], 1)
        self.assertIsNone(payload["cell_slots"][1][1])
        self.assertEqual(payload["slot_count"], 2)
        self.assertEqual(payload["glyph_bank"][0]["rows"], list(frame))
        self.assertEqual(payload["glyph_bank"][1]["rows"], list(diag))

    def test_lcd_art_pbm_maps_pixels_to_5x8_row_bytes(self) -> None:
        tile_rows = (
            "10001",
            "01010",
            "00100",
            "11111",
            "00000",
            "10101",
            "01010",
            "10001",
        )
        rows = []
        for y in range(LCD_ART_PIXEL_HEIGHT):
            if y < len(tile_rows):
                rows.append(tile_rows[y] + ("0" * (LCD_ART_PIXEL_WIDTH - 5)))
            else:
                rows.append("0" * LCD_ART_PIXEL_WIDTH)
        pbm = _pbm_from_rows(rows)

        art = compile_lcd_art_from_pbm("pixel badge", pbm)

        self.assertEqual(art.preview_lines[0], "0" + (" " * 19))
        self.assertEqual(art.cell_slots[0][0], 0)
        self.assertEqual(
            art.glyph_bank.glyphs[0].rows,
            (0x11, 0x0A, 0x04, 0x1F, 0x00, 0x15, 0x0A, 0x11),
        )

    def test_lcd_art_rejections_fail_closed(self) -> None:
        good_rows = ["0" * LCD_ART_PIXEL_WIDTH for _ in range(LCD_ART_PIXEL_HEIGHT)]
        cases = {
            "bad_magic": "P4 100 32 0",
            "bad_dimensions": "P1 5 8 " + ("0 " * 40),
            "bad_pixel": "P1 100 32 " + ("0 " * 100) + "2 " + ("0 " * 3099),
            "bad_count": "P1 100 32 0 1 0",
        }
        for name, pbm in cases.items():
            with self.subTest(name=name), self.assertRaises(LcdMenuError):
                compile_lcd_art_from_pbm(name, pbm)

        with self.assertRaisesRegex(LcdMenuError, "art_tile_rows_invalid"):
            compile_lcd_art_tile_map("bad", [])
        with self.assertRaisesRegex(LcdMenuError, "art_tile_columns_invalid"):
            compile_lcd_art_tile_map("bad", [[None], [None], [None], [None]])
        with self.assertRaisesRegex(LcdMenuError, "art_tile_row_byte_invalid"):
            compile_lcd_art_tile_map(
                "bad",
                [[(0x20,) * 8 for _ in range(LCD_COLUMNS)] for _ in range(LCD_ROWS)],
            )

        overflow_map = [[None for _ in range(LCD_COLUMNS)] for _ in range(LCD_ROWS)]
        for column in range(9):
            overflow_map[0][column] = tuple([column + 1] * 8)
        with self.assertRaisesRegex(LcdMenuError, "art_glyph_overflow"):
            compile_lcd_art_tile_map("overflow", overflow_map)

        self.assertEqual(
            compile_lcd_art_from_pbm("blank", _pbm_from_rows(good_rows)).to_dict()["slot_count"],
            0,
        )

    def test_browser_mirror_api_and_static_html_are_host_only_v2(self) -> None:
        mirror = LcdBrowserMirror(sample_state())
        state_response = mirror.handle_request("GET", API_STATE_PATH)
        self.assertEqual(state_response.status, 200)
        self.assertEqual(state_response.body["schema"], RENDER_SCHEMA)
        self.assertEqual(state_response.body["viewport"]["selected_item_id"], "home-status")
        self.assertEqual(state_response.body["cursor"]["focus"], "item")

        intent_response = mirror.handle_request("POST", API_INTENT_PATH, {"intent": "rotate_right"})
        self.assertEqual(intent_response.status, 200)
        self.assertEqual(intent_response.body["view"]["selected_item"], 1)

        bad_intent = mirror.handle_request("POST", API_INTENT_PATH, {"intent": "relay_toggle"})
        self.assertEqual(bad_intent.status, 400)
        self.assertEqual(bad_intent.body["error"], "unsupported_input")

        closed_route = mirror.handle_request("POST", "/api/relay/toggle", {"intent": "short_press"})
        self.assertEqual(closed_route.status, 404)
        self.assertEqual(closed_route.body["error"], "route_closed")

        html = build_browser_document(render(sample_state()))
        self.assertIn('class="lcd-row"', html)
        self.assertIn('class="lcd-row lcd-row-cursor"', html)
        self.assertIn('data-selected-item="home-status"', html)
        self.assertIn('data-viewport-top-line="0"', html)
        self.assertIn('data-cursor-ddram="0x00"', html)
        self.assertIn('data-cursor-focus="item"', html)
        self.assertIn('data-glyph-bank="core_status"', html)
        self.assertIn('data-source-xml="bbs_lcd_menu.v1"', html)
        self.assertIn('data-intent="rotate_right"', html)
        for forbidden in (
            "fetch(",
            "XMLHttpRequest",
            "WebSocket",
            "EventSource",
            "localStorage",
            "navigator.serial",
            "Bluetooth",
            "gpio_set_level",
            "uart_write",
            "relay_toggle",
        ):
            self.assertNotIn(forbidden, html)

    def test_browser_mirror_accepts_only_v2_intents(self) -> None:
        for intent in sorted(INPUT_EVENTS):
            mirror = LcdBrowserMirror(sample_state())
            response = mirror.handle_request("POST", API_INTENT_PATH, {"intent": intent})
            self.assertEqual(response.status, 200, intent)
            self.assertEqual(response.body["schema"], RENDER_SCHEMA)
            self.assertIn(
                response.body["view"]["last_intent"],
                {
                    "back_list",
                    "home",
                    "item_next",
                    "item_previous",
                    "detail:home-status",
                },
            )

    def test_browser_mirror_rejects_closed_methods_and_bad_payloads(self) -> None:
        mirror = LcdBrowserMirror(sample_state())

        method_closed = mirror.handle_request("POST", API_STATE_PATH)
        self.assertEqual(method_closed.status, 405)
        self.assertEqual(method_closed.body["error"], "method_closed")

        intent_get = mirror.handle_request("GET", API_INTENT_PATH)
        self.assertEqual(intent_get.status, 405)
        self.assertEqual(intent_get.body["error"], "method_closed")

        bad_json = mirror.handle_request("POST", API_INTENT_PATH, "{")
        self.assertEqual(bad_json.status, 400)
        self.assertEqual(bad_json.body["error"], "json_invalid")

        non_object = mirror.handle_request("POST", API_INTENT_PATH, "[]")
        self.assertEqual(non_object.status, 400)
        self.assertEqual(non_object.body["error"], "json_object_required")

        unknown = mirror.handle_request(
            "POST",
            API_INTENT_PATH,
            {"intent": "rotate_right", "command": "relay_toggle"},
        )
        self.assertEqual(unknown.status, 400)
        self.assertEqual(unknown.body["error"], "intent_field_unknown")

        secret = mirror.handle_request(
            "POST",
            API_INTENT_PATH,
            {"intent": "rotate_right", "pairing_token": "closed"},
        )
        self.assertEqual(secret.status, 400)
        self.assertEqual(secret.body["error"], "secret_field_rejected")

    def test_browser_mirror_rejects_secret_snapshot(self) -> None:
        state = sample_state()
        state["messages"] = {"raw_body": "secret"}
        response = LcdBrowserMirror(state).handle_request("GET", API_STATE_PATH)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.body["error"], "secret_field_rejected")

    def test_browser_mirror_close_rejects_all_requests_without_side_effects(self) -> None:
        mirror = LcdBrowserMirror(sample_state())
        initial = mirror.handle_request("GET", API_STATE_PATH)
        self.assertEqual(initial.status, 200)
        previous_lines = mirror.previous_lines
        view = mirror.view
        mirror.now_ms = 1234

        mirror.close()

        cases = [
            ("GET", API_STATE_PATH, None),
            ("POST", API_INTENT_PATH, {"intent": "rotate_right"}),
            ("POST", API_INTENT_PATH, "{"),
            ("POST", API_INTENT_PATH, {"intent": "rotate_right", "pairing_token": "closed"}),
            ("DELETE", API_STATE_PATH, None),
            ("POST", "/api/relay/toggle", {"intent": "short_press"}),
        ]
        for method, path, body in cases:
            with self.subTest(method=method, path=path):
                response = mirror.handle_request(method, path, body)
                self.assertEqual(response.status, 410)
                self.assertEqual(dict(response.body), {"error": "interface_closed"})

        self.assertTrue(mirror.closed)
        self.assertIs(mirror.view, view)
        self.assertEqual(mirror.previous_lines, previous_lines)
        self.assertEqual(mirror.now_ms, 1234)

    def test_browser_mirror_reopen_resets_dirty_view_and_time_state(self) -> None:
        mirror = LcdBrowserMirror(sample_state())
        self.assertEqual(mirror.handle_request("GET", API_STATE_PATH).status, 200)
        self.assertEqual(
            mirror.handle_request("POST", API_INTENT_PATH, {"intent": "rotate_right"}).status,
            200,
        )
        mirror.now_ms = 2000
        mirror.close()

        returned = mirror.reopen(sample_state())
        response = mirror.handle_request("GET", API_STATE_PATH)

        self.assertIs(returned, mirror)
        self.assertFalse(mirror.closed)
        self.assertEqual(mirror.now_ms, 0)
        self.assertEqual(mirror.view, MenuViewState())
        self.assertEqual(response.status, 200)
        self.assertEqual(response.body["view"], MenuViewState().to_dict())
        self.assertEqual(response.body["cursor"]["dirty_rows"], [0, 1, 2, 3])
        self.assertEqual(len(response.body["cursor"]["dirty_cells"]), LCD_ROWS * LCD_COLUMNS)

    def test_browser_mirror_reopen_accepts_explicit_view_without_previous_leakage(self) -> None:
        mirror = LcdBrowserMirror(sample_state())
        self.assertEqual(mirror.handle_request("GET", API_STATE_PATH).status, 200)
        mirror.reopen(sample_state(), MenuViewState(page="ROUTES"))

        response = mirror.handle_request("GET", API_STATE_PATH)

        self.assertEqual(response.status, 200)
        self.assertEqual(response.body["page"], "ROUTES")
        self.assertEqual(response.body["glyph_bank_name"], "table")
        self.assertEqual(response.body["viewport"]["selected_item_id"], "routes-table")
        self.assertEqual(response.body["cursor"]["dirty_rows"], [0, 1, 2, 3])

    def test_browser_mirror_context_manager_closes_on_exit(self) -> None:
        with LcdBrowserMirror(sample_state()) as mirror:
            response = mirror.handle_request("GET", API_STATE_PATH)
            self.assertEqual(response.status, 200)
            self.assertFalse(mirror.closed)

        response = mirror.handle_request("GET", API_STATE_PATH)
        self.assertTrue(mirror.closed)
        self.assertEqual(response.status, 410)
        self.assertEqual(dict(response.body), {"error": "interface_closed"})


def _pbm_from_rows(rows: list[str]) -> str:
    return "P1\n{} {}\n{}\n".format(
        LCD_ART_PIXEL_WIDTH,
        LCD_ART_PIXEL_HEIGHT,
        "\n".join(" ".join(row) for row in rows),
    )


if __name__ == "__main__":
    unittest.main()
