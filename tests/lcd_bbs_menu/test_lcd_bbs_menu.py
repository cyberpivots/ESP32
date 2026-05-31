#!/usr/bin/env python3
"""Tests for the host-only LCD BBS menu renderer."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "simulators" / "lcd_bbs_menu"))

from lcd_bbs_menu import (  # noqa: E402
    API_INTENT_PATH,
    API_STATE_PATH,
    GLYPH_BANK,
    GLYPH_BANKS,
    LCD_COLUMNS,
    LCD_DDRAM_ROW_BASES,
    LCD_ROWS,
    RENDER_SCHEMA,
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
    gauge_demo,
    horizontal_bar,
    render,
    sample_state,
    signal_bars,
    slider,
    spinner_frame,
    vertical_chart,
)


class LcdBbsMenuTests(unittest.TestCase):
    def test_home_lines_are_exactly_20_cells(self) -> None:
        rendered = render(sample_state())
        self.assertEqual(rendered.schema, RENDER_SCHEMA)
        self.assertEqual(len(rendered.lines), LCD_ROWS)
        self.assertTrue(all(len(line) == LCD_COLUMNS for line in rendered.lines))

    def test_page_snapshots_are_stable(self) -> None:
        home = render(sample_state(), MenuViewState(page="HOME"))
        self.assertEqual(
            home.lines,
            (
                "BBS FIELD LINK:OK   ",
                "Peers:3 Queue:2     ",
                "Cust:OPCON          ",
                "Last:ACK peer01     ",
            ),
        )

        mesh = render(sample_state(), MenuViewState(page="MESH"))
        self.assertEqual(
            mesh.lines,
            (
                "MESH sim            ",
                "Root:coord01        ",
                "Hops:2 Heal:1       ",
                "Live:CLOSED         ",
            ),
        )

        xbee = render(sample_state(), MenuViewState(page="XBEE"))
        self.assertEqual(
            xbee.lines,
            (
                "XBEE CLOSED         ",
                "UART:CLOSED         ",
                "NP:256              ",
                "TX CLOSED           ",
            ),
        )

    def test_glyph_bank_bounds(self) -> None:
        rendered = render(sample_state())
        self.assertEqual(rendered.glyph_bank, GLYPH_BANK)
        self.assertEqual(len(rendered.glyph_bank), 8)
        for expected_slot, glyph in enumerate(rendered.glyph_bank):
            self.assertEqual(glyph.slot, expected_slot)
            self.assertEqual(len(glyph.rows), 8)
            self.assertTrue(all(0 <= row <= 0x1F for row in glyph.rows))

    def test_named_glyph_banks_and_swap_throttle(self) -> None:
        self.assertEqual(
            set(GLYPH_BANKS),
            {"core_status", "horizontal_bar", "vertical_chart", "big_digits", "gauge_demo"},
        )
        manager = GlyphBankManager()
        with self.assertRaisesRegex(LcdMenuError, "glyph_bank_swap_throttled"):
            manager.select("horizontal_bar", now_ms=100)
        selected = manager.select("horizontal_bar", now_ms=250)
        self.assertEqual(selected.name, "horizontal_bar")

        with self.assertRaisesRegex(LcdMenuError, "glyph_bank_overflow"):
            GlyphBank(
                "too_many",
                tuple(Glyph(index, f"g{index}", (0,) * 8) for index in range(9)),
            )
        with self.assertRaisesRegex(LcdMenuError, "glyph_row_byte_invalid"):
            GlyphBank("bad_row", (Glyph(0, "bad", (0x20,) * 8),))

    def test_truncates_long_lines(self) -> None:
        state = sample_state()
        state["last_event"] = "ACK peer01 with an intentionally overlong event"
        rendered = render(state)
        self.assertEqual(rendered.lines[3], "Last:ACK peer01 with")
        self.assertEqual(len(rendered.lines[3]), LCD_COLUMNS)

    def test_missing_data_renders_unknown_or_closed(self) -> None:
        state = {"schema": SNAPSHOT_SCHEMA}
        home = render(state)
        self.assertIn("LINK:?", home.lines[0])
        self.assertEqual(home.lines[1], "Peers:? Queue:?     ")
        self.assertEqual(home.lines[2], "Cust:?              ")

        xbee = render(state, MenuViewState(page="XBEE"))
        self.assertEqual(xbee.lines[0], "XBEE CLOSED         ")
        self.assertEqual(xbee.lines[2], "NP:?                ")

    def test_secret_fields_are_rejected(self) -> None:
        state = sample_state()
        state["mesh"] = {"pairing_token": "do-not-render"}
        with self.assertRaisesRegex(LcdMenuError, "secret_field_rejected"):
            render(state)

    def test_unknown_top_level_fields_are_rejected(self) -> None:
        state = sample_state()
        state["extra"] = "not in bbs_lcd_state.v1"
        with self.assertRaisesRegex(LcdMenuError, "field_unknown"):
            render(state)

    def test_input_event_transitions_are_ui_only(self) -> None:
        view = MenuViewState()
        view = apply_input(view, "rotate_right")
        self.assertEqual(view.page, "MESSAGES")
        self.assertEqual(view.last_intent, "page_next")

        view = apply_input(view, "short_press")
        self.assertTrue(view.detail)
        self.assertTrue(view.notification_ack)
        self.assertEqual(view.last_intent, "local_ack")
        self.assertEqual(view.mode, "row_browse")

        view = apply_input(view, "rotate_right")
        self.assertEqual(view.page, "MESSAGES")
        self.assertEqual(view.selected_row, 1)
        self.assertEqual(view.last_intent, "row_next")

        view = apply_input(view, "long_press")
        self.assertEqual(view.page, "MESSAGES")
        self.assertEqual(view.last_intent, "back")
        view = apply_input(view, "long_press")
        self.assertEqual(view, MenuViewState(page="HOME", last_intent="home"))

    def test_edit_lab_mode_changes_local_value_only(self) -> None:
        view = MenuViewState(page="DIAG", selected_row=2, detail=True, mode="edit_lab", edit_value=10)
        view = apply_input(view, "rotate_right")
        self.assertEqual(view.edit_value, 15)
        self.assertEqual(view.last_intent, "value_up")
        view = apply_input(view, "short_press")
        self.assertEqual(view.last_intent, "local_commit")
        self.assertEqual(view.mode, "row_browse")

    def test_double_click_is_not_a_v1_input(self) -> None:
        with self.assertRaisesRegex(LcdMenuError, "unsupported_input"):
            apply_input(MenuViewState(), "double_click")

    def test_closed_surface_labels_do_not_emit_commands(self) -> None:
        rendered = render(sample_state(), MenuViewState(page="LOCKS"))
        self.assertEqual(
            rendered.lines,
            (
                "LOCKS               ",
                "Relay:LOCK          ",
                "XBee:LOCK           ",
                "Flash:LOCK Ser:LOCK ",
            ),
        )

    def test_cursor_ddram_mapping_and_dirty_metadata(self) -> None:
        self.assertEqual(LCD_DDRAM_ROW_BASES, (0x00, 0x40, 0x14, 0x54))
        self.assertEqual(CursorTracker.row_column_to_ddram(2, 3), 0x17)
        self.assertEqual(CursorTracker.ddram_to_row_column(0x54), (3, 0))

        base = render(sample_state())
        changed_state = sample_state()
        changed_state["last_event"] = "ACK peer02"
        changed = render(changed_state, previous_lines=base.lines)
        self.assertEqual(changed.cursor.dirty_rows, (3,))
        self.assertIn((3, 14), changed.cursor.dirty_cells)

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

    def test_browser_mirror_api_and_static_html_are_host_only(self) -> None:
        mirror = LcdBrowserMirror(sample_state())
        state_response = mirror.handle_request("GET", API_STATE_PATH)
        self.assertEqual(state_response.status, 200)
        self.assertEqual(state_response.body["schema"], RENDER_SCHEMA)
        self.assertEqual(len(state_response.body["lines"]), LCD_ROWS)
        self.assertEqual(state_response.body["cursor"]["focus"], "page")

        intent_response = mirror.handle_request("POST", API_INTENT_PATH, {"intent": "rotate_right"})
        self.assertEqual(intent_response.status, 200)
        self.assertEqual(intent_response.body["view"]["page"], "MESSAGES")

        bad_intent = mirror.handle_request("POST", API_INTENT_PATH, {"intent": "relay_toggle"})
        self.assertEqual(bad_intent.status, 400)
        self.assertEqual(bad_intent.body["error"], "unsupported_input")

        closed_route = mirror.handle_request("POST", "/api/relay/toggle", {"intent": "short_press"})
        self.assertEqual(closed_route.status, 404)
        self.assertEqual(closed_route.body["error"], "route_closed")

        html = build_browser_document(render(sample_state()))
        self.assertIn('class="lcd-row"', html)
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
        ):
            self.assertNotIn(forbidden, html)

    def test_browser_mirror_rejects_secret_snapshot(self) -> None:
        state = sample_state()
        state["messages"] = {"raw_body": "secret"}
        response = LcdBrowserMirror(state).handle_request("GET", API_STATE_PATH)
        self.assertEqual(response.status, 400)
        self.assertEqual(response.body["error"], "secret_field_rejected")


if __name__ == "__main__":
    unittest.main()
