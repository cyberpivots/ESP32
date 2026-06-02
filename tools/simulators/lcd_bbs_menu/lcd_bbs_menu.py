#!/usr/bin/env python3
"""Host-only 20x4 LCD menu renderer for the ESP-NOW BBS field console."""

from __future__ import annotations

import argparse
import html
import json
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from typing import Any

from generated_menu import (  # noqa: E402
    FIRMWARE_ID,
    GLYPH_BANKS as GENERATED_GLYPH_BANKS,
    MENU_SCHEMA,
    PAGES as GENERATED_PAGES,
    RENDER_SCHEMA,
    SOURCE_ID,
    SOURCE_XML,
)


LCD_COLUMNS = 20
LCD_ROWS = 4
LCD_CONTENT_COLUMNS = 19
LCD_DDRAM_ROW_BASES = (0x00, 0x40, 0x14, 0x54)
SNAPSHOT_SCHEMA = "bbs_lcd_state.v1"
LCD_ART_SCHEMA = "bbs_lcd_art.v1"
LCD_PIXEL_PREVIEW_SCHEMA = "bbs_lcd_pixel_preview.v1"
LCD_ART_CATALOG_SCHEMA = "bbs_lcd_art_catalog.v1"
LCD_ART_TILE_WIDTH = 5
LCD_ART_TILE_HEIGHT = 8
LCD_ART_PIXEL_WIDTH = LCD_COLUMNS * LCD_ART_TILE_WIDTH
LCD_ART_PIXEL_HEIGHT = LCD_ROWS * LCD_ART_TILE_HEIGHT
GLYPH_SWAP_MIN_MS = 250
MARQUEE_HOLD_MS = 750
MARQUEE_STEP_MS = 250
MARQUEE_GAP = 2
MAX_PAGE_STACK = 4
PAGES = tuple(str(page["id"]) for page in GENERATED_PAGES)
NAVIGATION_MODES = frozenset({"scroll", "detail", "edit_lab", "page_browse", "row_browse"})
INPUT_EVENTS = frozenset({"rotate_left", "rotate_right", "short_press", "long_press"})
API_STATE_PATH = "/api/lcd/state"
API_INTENT_PATH = "/api/lcd/intent"
API_INTENT_FIELDS = frozenset({"intent"})
ALLOWED_TOP_LEVEL_FIELDS = frozenset(
    {
        "schema",
        "mode",
        "link",
        "peers",
        "queue",
        "custody",
        "messages",
        "files",
        "telemetry",
        "mesh",
        "xbee",
        "bridge",
        "errors",
        "locks",
        "last_event",
        "uptime_ms",
    }
)
SECRET_FIELD_MARKERS = frozenset(
    {
        "androidid",
        "body",
        "credential",
        "key",
        "latitude",
        "lmk",
        "location",
        "longitude",
        "password",
        "passwd",
        "pairingtoken",
        "pmk",
        "rawbody",
        "secret",
        "token",
    }
)


class LcdMenuError(ValueError):
    """Raised when the host-only LCD menu input is invalid or unsafe."""

    def __init__(self, reason: str, detail: str | None = None) -> None:
        self.reason = reason
        self.detail = detail
        message = reason if detail is None else f"{reason}: {detail}"
        super().__init__(message)


@dataclass(frozen=True)
class Glyph:
    slot: int
    name: str
    rows: tuple[int, ...]


@dataclass(frozen=True)
class GlyphBank:
    name: str
    glyphs: tuple[Glyph, ...]

    def __post_init__(self) -> None:
        if len(self.glyphs) > 8:
            raise LcdMenuError("glyph_bank_overflow", self.name)
        slots = [glyph.slot for glyph in self.glyphs]
        if slots != list(range(len(slots))):
            raise LcdMenuError("glyph_slots_invalid", self.name)
        for glyph in self.glyphs:
            if len(glyph.rows) != 8:
                raise LcdMenuError("glyph_rows_invalid", glyph.name)
            if any(row < 0 or row > 0x1F for row in glyph.rows):
                raise LcdMenuError("glyph_row_byte_invalid", glyph.name)


@dataclass(frozen=True)
class CompiledLcdArt:
    name: str
    preview_lines: tuple[str, ...]
    glyph_bank: GlyphBank
    cell_slots: tuple[tuple[int | None, ...], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": LCD_ART_SCHEMA,
            "name": self.name,
            "pixel_width": LCD_ART_PIXEL_WIDTH,
            "pixel_height": LCD_ART_PIXEL_HEIGHT,
            "tile_width": LCD_ART_TILE_WIDTH,
            "tile_height": LCD_ART_TILE_HEIGHT,
            "columns": LCD_COLUMNS,
            "rows": LCD_ROWS,
            "slot_count": len(self.glyph_bank.glyphs),
            "preview_lines": list(self.preview_lines),
            "cell_slots": [list(row) for row in self.cell_slots],
            "glyph_bank_name": self.glyph_bank.name,
            "glyph_bank": [
                {"slot": glyph.slot, "name": glyph.name, "rows": list(glyph.rows)}
                for glyph in self.glyph_bank.glyphs
            ],
            "pixel_preview": lcd_art_pixel_preview(self),
        }


class GlyphBankManager:
    """Host-side CGRAM bank switch guard for simulator work."""

    def __init__(
        self,
        banks: Mapping[str, GlyphBank] | None = None,
        active: str = "core_status",
        min_swap_ms: int = GLYPH_SWAP_MIN_MS,
    ) -> None:
        self._banks = dict(banks or GLYPH_BANKS)
        if active not in self._banks:
            raise LcdMenuError("glyph_bank_unknown", active)
        self._active_name = active
        self._last_swap_ms = 0
        self._min_swap_ms = min_swap_ms

    @property
    def active_bank(self) -> GlyphBank:
        return self._banks[self._active_name]

    def select(self, name: str, now_ms: int) -> GlyphBank:
        if name not in self._banks:
            raise LcdMenuError("glyph_bank_unknown", name)
        if name == self._active_name:
            return self.active_bank
        if now_ms - self._last_swap_ms < self._min_swap_ms:
            raise LcdMenuError("glyph_bank_swap_throttled", name)
        self._active_name = name
        self._last_swap_ms = now_ms
        return self.active_bank


@dataclass(frozen=True)
class MenuViewState:
    page: str = "HOME"
    selected_item: int = 0
    viewport_top_line: int = 0
    selected_row: int = 0
    art_index: int = 0
    detail: bool = False
    notification_ack: bool = False
    last_intent: str = "home"
    mode: str = "scroll"
    edit_value: int = 0
    page_stack: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "page": self.page,
            "selected_item": self.selected_item,
            "viewport_top_line": self.viewport_top_line,
            "selected_row": self.selected_row,
            "art_index": self.art_index,
            "detail": self.detail,
            "notification_ack": self.notification_ack,
            "last_intent": self.last_intent,
            "mode": self.mode,
            "edit_value": self.edit_value,
            "page_stack": list(self.page_stack),
        }


@dataclass(frozen=True)
class CursorState:
    row: int
    column: int
    ddram_address: int
    focus: str
    dirty_rows: tuple[int, ...]
    dirty_cells: tuple[tuple[int, int], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "row": self.row,
            "column": self.column,
            "ddram_address": self.ddram_address,
            "focus": self.focus,
            "dirty_rows": list(self.dirty_rows),
            "dirty_cells": [
                {"row": row, "column": column} for row, column in self.dirty_cells
            ],
        }


class CursorTracker:
    @staticmethod
    def row_column_to_ddram(row: int, column: int) -> int:
        if not 0 <= row < LCD_ROWS:
            raise LcdMenuError("cursor_row_invalid", str(row))
        if not 0 <= column < LCD_COLUMNS:
            raise LcdMenuError("cursor_column_invalid", str(column))
        return LCD_DDRAM_ROW_BASES[row] + column

    @staticmethod
    def ddram_to_row_column(address: int) -> tuple[int, int]:
        for row, base in enumerate(LCD_DDRAM_ROW_BASES):
            column = address - base
            if 0 <= column < LCD_COLUMNS:
                return row, column
        raise LcdMenuError("ddram_address_invalid", hex(address))

    @classmethod
    def from_lines(
        cls,
        lines: Sequence[str],
        view: MenuViewState,
        previous_lines: Sequence[str] | None = None,
    ) -> CursorState:
        mode = _effective_mode(view)
        if view.page == "ART":
            row = 0
            column = 0
            focus = "art_panel"
        else:
            row = max(0, min(LCD_ROWS - 1, view.selected_row))
            column = 18 if mode == "edit_lab" else 1 if mode == "detail" else 0
            focus = {
                "scroll": "item",
                "detail": "detail",
                "edit_lab": "edit",
            }[_canonical_mode(mode)]
        dirty_rows, dirty_cells = _dirty_metadata(lines, previous_lines)
        return CursorState(
            row=row,
            column=column,
            ddram_address=cls.row_column_to_ddram(row, column),
            focus=focus,
            dirty_rows=dirty_rows,
            dirty_cells=dirty_cells,
        )


@dataclass(frozen=True)
class RenderedLcdMenu:
    schema: str
    source_xml_version: str
    firmware_id: str
    source_id: str
    page: str
    glyph_bank_name: str
    lines: tuple[str, ...]
    glyph_bank: tuple[Glyph, ...]
    view: MenuViewState
    cursor: CursorState
    viewport: Mapping[str, Any]
    widgets: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "source_xml_version": self.source_xml_version,
            "firmware_id": self.firmware_id,
            "source_id": self.source_id,
            "page": self.page,
            "glyph_bank_name": self.glyph_bank_name,
            "lines": list(self.lines),
            "glyph_bank": [
                {"slot": glyph.slot, "name": glyph.name, "rows": list(glyph.rows)}
                for glyph in self.glyph_bank
            ],
            "view": self.view.to_dict(),
            "cursor": self.cursor.to_dict(),
            "viewport": dict(self.viewport),
            "widgets": dict(self.widgets),
        }


GLYPH_BANKS = {
    "core_status": GlyphBank(
        "core_status",
        (
            Glyph(0, "lock", (0x0E, 0x11, 0x11, 0x1F, 0x1B, 0x1B, 0x1F, 0x00)),
            Glyph(1, "warning", (0x04, 0x0E, 0x0E, 0x15, 0x1F, 0x04, 0x00, 0x00)),
            Glyph(2, "envelope", (0x1F, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x1F, 0x00)),
            Glyph(3, "queue_arrow", (0x04, 0x06, 0x1F, 0x06, 0x04, 0x00, 0x1F, 0x00)),
            Glyph(4, "ack_mark", (0x00, 0x01, 0x03, 0x16, 0x1C, 0x08, 0x00, 0x00)),
            Glyph(5, "radio_low", (0x00, 0x04, 0x0A, 0x04, 0x00, 0x04, 0x04, 0x00)),
            Glyph(6, "radio_high", (0x11, 0x0A, 0x04, 0x0A, 0x11, 0x04, 0x04, 0x00)),
            Glyph(7, "select", (0x04, 0x06, 0x1F, 0x06, 0x04, 0x00, 0x00, 0x00)),
        ),
    ),
    "horizontal_bar": GlyphBank(
        "horizontal_bar",
        tuple(
            Glyph(
                slot,
                f"bar_{slot}",
                tuple([((1 << min(slot, 5)) - 1) << max(0, 5 - slot)] * 8),
            )
            for slot in range(6)
        )
        + (
            Glyph(6, "cap_left", (0x1F, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F, 0x00)),
            Glyph(7, "cap_right", (0x1F, 0x01, 0x01, 0x01, 0x01, 0x01, 0x1F, 0x00)),
        ),
    ),
    "vertical_chart": GlyphBank(
        "vertical_chart",
        tuple(
            Glyph(
                slot,
                f"vbar_{slot}",
                tuple(0x1F if row >= 8 - slot else 0x00 for row in range(8)),
            )
            for slot in range(8)
        ),
    ),
    "big_digits": GlyphBank(
        "big_digits",
        (
            Glyph(0, "top", (0x1F, 0x1F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)),
            Glyph(1, "upper_left", (0x18, 0x18, 0x18, 0x18, 0x00, 0x00, 0x00, 0x00)),
            Glyph(2, "upper_right", (0x03, 0x03, 0x03, 0x03, 0x00, 0x00, 0x00, 0x00)),
            Glyph(3, "middle", (0x00, 0x00, 0x1F, 0x1F, 0x00, 0x00, 0x00, 0x00)),
            Glyph(4, "lower_left", (0x00, 0x00, 0x00, 0x00, 0x18, 0x18, 0x18, 0x18)),
            Glyph(5, "lower_right", (0x00, 0x00, 0x00, 0x00, 0x03, 0x03, 0x03, 0x03)),
            Glyph(6, "bottom", (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0x1F)),
            Glyph(7, "blank", (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)),
        ),
    ),
    "gauge": GlyphBank(
        "gauge",
        (
            Glyph(0, "gauge_empty", (0x00, 0x0E, 0x11, 0x11, 0x11, 0x0E, 0x00, 0x00)),
            Glyph(1, "needle_left", (0x00, 0x0E, 0x11, 0x15, 0x19, 0x0E, 0x00, 0x00)),
            Glyph(2, "needle_mid", (0x00, 0x0E, 0x15, 0x15, 0x15, 0x0E, 0x00, 0x00)),
            Glyph(3, "needle_right", (0x00, 0x0E, 0x11, 0x15, 0x13, 0x0E, 0x00, 0x00)),
            Glyph(4, "tick_low", (0x00, 0x00, 0x00, 0x10, 0x18, 0x1C, 0x1E, 0x1F)),
            Glyph(5, "tick_mid", (0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04)),
            Glyph(6, "tick_high", (0x00, 0x00, 0x00, 0x01, 0x03, 0x07, 0x0F, 0x1F)),
            Glyph(7, "dot", (0x00, 0x00, 0x00, 0x04, 0x0E, 0x04, 0x00, 0x00)),
        ),
    ),
    "table": GlyphBank(
        "table",
        (
            Glyph(0, "vertical", (0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04)),
            Glyph(1, "horizontal", (0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00, 0x00)),
            Glyph(2, "corner_tl", (0x00, 0x00, 0x00, 0x07, 0x04, 0x04, 0x04, 0x04)),
            Glyph(3, "corner_tr", (0x00, 0x00, 0x00, 0x1C, 0x04, 0x04, 0x04, 0x04)),
            Glyph(4, "tee_left", (0x04, 0x04, 0x04, 0x07, 0x04, 0x04, 0x04, 0x04)),
            Glyph(5, "tee_right", (0x04, 0x04, 0x04, 0x1C, 0x04, 0x04, 0x04, 0x04)),
            Glyph(6, "cross", (0x04, 0x04, 0x04, 0x1F, 0x04, 0x04, 0x04, 0x04)),
            Glyph(7, "continuation", (0x04, 0x0E, 0x15, 0x04, 0x04, 0x04, 0x04, 0x00)),
        ),
    ),
    "art_panel": GlyphBank(
        "art_panel",
        (
            Glyph(0, "art_frame", (0x1F, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1F, 0x00)),
            Glyph(1, "art_fill", (0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F)),
            Glyph(2, "art_diag", (0x10, 0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08)),
            Glyph(3, "art_blank_3", (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)),
            Glyph(4, "art_blank_4", (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)),
            Glyph(5, "art_blank_5", (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)),
            Glyph(6, "art_blank_6", (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)),
            Glyph(7, "art_blank_7", (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)),
        ),
    ),
}
GLYPH_BANK = GLYPH_BANKS["core_status"].glyphs
SPINNER_FRAMES = ("-", "\\", "|", "/")
ART_BLANK_TILE = (0x00,) * LCD_ART_TILE_HEIGHT


def assert_no_secret_fields(payload: Any, path: tuple[str, ...] = ()) -> None:
    if isinstance(payload, Mapping):
        for key, value in payload.items():
            key_text = str(key).lower().replace("_", "").replace("-", "")
            if any(marker in key_text for marker in SECRET_FIELD_MARKERS):
                dotted = ".".join((*path, str(key)))
                raise LcdMenuError("secret_field_rejected", dotted)
            assert_no_secret_fields(value, (*path, str(key)))
    elif isinstance(payload, Sequence) and not isinstance(payload, (str, bytes, bytearray)):
        for index, value in enumerate(payload):
            assert_no_secret_fields(value, (*path, str(index)))


def validate_snapshot(snapshot: Mapping[str, Any]) -> None:
    schema = snapshot.get("schema")
    if schema != SNAPSHOT_SCHEMA:
        raise LcdMenuError("schema_invalid", str(schema))
    assert_no_secret_fields(snapshot)
    unknown = sorted(set(snapshot) - ALLOWED_TOP_LEVEL_FIELDS)
    if unknown:
        raise LcdMenuError("field_unknown", ",".join(unknown))


def apply_input(view: MenuViewState, event: str) -> MenuViewState:
    if event not in INPUT_EVENTS:
        raise LcdMenuError("unsupported_input", event)
    view = _normalized_view(view)
    page = _page_by_id(view.page)
    selected_item = _selected_item(page, view.selected_item)
    mode = _canonical_mode(_effective_mode(view))

    if event == "long_press":
        if mode == "edit_lab":
            return _normalized_view(replace(view, mode="detail", last_intent="back_detail"))
        if mode == "detail":
            return _normalized_view(replace(view, mode="scroll", detail=False, last_intent="back_list"))
        if view.page_stack:
            previous = view.page_stack[-1]
            return _normalized_view(
                MenuViewState(
                    page=previous,
                    page_stack=view.page_stack[:-1],
                    last_intent="back_page",
                    edit_value=view.edit_value,
                    art_index=view.art_index,
                )
            )
        return _normalized_view(
            MenuViewState(
                page="HOME",
                last_intent="home",
                edit_value=view.edit_value,
                art_index=view.art_index,
            )
        )

    if event == "short_press":
        if mode == "edit_lab":
            return _normalized_view(
                replace(
                    view,
                    mode="detail",
                    detail=True,
                    notification_ack=True,
                    last_intent="local_commit",
                )
            )
        item = page["items"][selected_item]
        action = str(item["action"])
        if action == "page":
            target = str(item["target"])
            stack = (*view.page_stack, view.page)[-MAX_PAGE_STACK:]
            return _normalized_view(
                MenuViewState(
                    page=target,
                    page_stack=stack,
                    last_intent=f"page:{target}",
                    edit_value=view.edit_value,
                    art_index=view.art_index,
                )
            )
        if action == "edit":
            return _normalized_view(
                replace(view, mode="edit_lab", detail=True, last_intent="edit_enter")
            )
        if action == "back":
            return apply_input(view, "long_press")
        return _normalized_view(
            replace(
                view,
                mode="detail",
                detail=True,
                notification_ack=True,
                last_intent=f"detail:{item['id']}",
            )
        )

    delta = 1 if event == "rotate_right" else -1
    if view.page == "ART":
        next_index = _art_index(view.art_index + delta)
        return _normalized_view(
            replace(
                view,
                art_index=next_index,
                notification_ack=False,
                last_intent="art_next" if delta > 0 else "art_previous",
            )
        )
    if mode == "edit_lab":
        value = (view.edit_value + (5 if delta > 0 else -5)) % 105
        return _normalized_view(
            replace(
                view,
                edit_value=value,
                notification_ack=False,
                last_intent="value_up" if delta > 0 else "value_down",
            )
        )
    item_count = max(1, len(page["items"]))
    next_item = (selected_item + delta) % item_count
    return _normalized_view(
        replace(
            view,
            selected_item=next_item,
            detail=mode == "detail",
            notification_ack=False,
            last_intent="item_next" if delta > 0 else "item_previous",
        )
    )


def render(
    snapshot: Mapping[str, Any],
    view: MenuViewState | None = None,
    previous_lines: Sequence[str] | None = None,
    glyph_bank_name: str | None = None,
    now_ms: int = 0,
) -> RenderedLcdMenu:
    validate_snapshot(snapshot)
    view = _normalized_view(view or MenuViewState())
    page = _page_by_id(view.page)
    if glyph_bank_name is None:
        glyph_bank_name = str(page["glyph_bank"])
    if glyph_bank_name not in GLYPH_BANKS:
        raise LcdMenuError("glyph_bank_unknown", glyph_bank_name)
    if glyph_bank_name == "table" and str(page["glyph_bank"]) != "table":
        raise LcdMenuError("table_bank_page_mismatch", str(page["id"]))
    if str(page["id"]) == "ART":
        lines, viewport = _render_art_page_lines(page, view)
    else:
        lines, viewport = _render_page_lines(snapshot, page, view, now_ms)
    lines = tuple(_fit(line) for line in lines)
    if len(lines) != LCD_ROWS or any(len(line) != LCD_COLUMNS for line in lines):
        raise LcdMenuError("render_shape_invalid", str(page["id"]))
    cursor = CursorTracker.from_lines(lines, view, previous_lines)
    return RenderedLcdMenu(
        schema=RENDER_SCHEMA,
        source_xml_version=MENU_SCHEMA,
        firmware_id=FIRMWARE_ID,
        source_id=SOURCE_ID,
        page=str(page["id"]),
        glyph_bank_name=glyph_bank_name,
        lines=lines,
        glyph_bank=GLYPH_BANKS[glyph_bank_name].glyphs,
        view=view,
        cursor=cursor,
        viewport=viewport,
        widgets=render_widgets(snapshot),
    )


def sample_state() -> dict[str, Any]:
    return {
        "schema": SNAPSHOT_SCHEMA,
        "mode": "FIELD",
        "link": {"status": "OK", "rssi": -67, "acks": 7, "dups": 0},
        "peers": {"count": 3, "active": 2},
        "queue": {"pending": 2, "failed": 0, "retry": 1},
        "custody": {"owner": "OPCON", "status": "ACKED", "acked": 12, "failed": 0},
        "messages": {"new": 1, "inbox": 12, "outbox": 4},
        "files": {"queued": 1, "done": 3, "bytes": 4096},
        "telemetry": {"temp_c": 31, "errors": 0, "level": 65, "history": [1, 3, 2, 4]},
        "mesh": {"mode": "sim", "root": "coord01", "hops": 2, "heal": 1},
        "xbee": {"surface": "closed", "np": 256},
        "bridge": {"state": "closed", "host_baud": 115200, "xbee_baud": 9600},
        "errors": {"count": 0, "last": "none"},
        "locks": {"relay": True, "xbee": True, "flash": True, "serial_write": True},
        "last_event": "ACK peer01",
        "uptime_ms": 125000,
    }


def glyph_bank_for_page(page: str) -> str:
    return str(_page_by_id(page)["glyph_bank"])


def render_widgets(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    pending = _safe_int(_get(snapshot, "queue", "pending"), default=0)
    failed = _safe_int(_get(snapshot, "queue", "failed"), default=0)
    retry = _safe_int(_get(snapshot, "queue", "retry"), default=0)
    acked = _safe_int(_get(snapshot, "custody", "acked"), default=0)
    custody_failed = _safe_int(_get(snapshot, "custody", "failed"), default=0)
    level = _safe_int(_get(snapshot, "telemetry", "level"), default=0)
    history = _history_values(snapshot)
    return {
        "queue": queue_indicator(pending=pending, failed=failed, retry=retry),
        "custody": custody_indicator(
            status=_get(snapshot, "custody", "status"),
            acked=acked,
            failed=custody_failed,
        ),
        "horizontal_bar": horizontal_bar(level, 100, width=10),
        "slider": slider(level, 0, 100, width=12),
        "vertical_chart": list(vertical_chart(history, height=4, width=8)),
        "signal": signal_bars(_safe_int(_get(snapshot, "link", "rssi"), default=-100)),
        "spinner": spinner_frame(_safe_int(_get(snapshot, "uptime_ms"), default=0) // 250),
        "big_digits": list(big_digits(_safe_int(_get(snapshot, "messages", "new"), default=0))),
        "gauge": gauge_demo(level, 100),
        "art_panel": sample_art_panel().to_dict(),
    }


def lcd_art_pixel_preview(art: CompiledLcdArt) -> dict[str, Any]:
    rows = _pixel_preview_rows(art)
    return {
        "schema": LCD_PIXEL_PREVIEW_SCHEMA,
        "source_art_schema": LCD_ART_SCHEMA,
        "source_art_name": art.name,
        "pixel_width": LCD_ART_PIXEL_WIDTH,
        "pixel_height": LCD_ART_PIXEL_HEIGHT,
        "glyph_slot_count": len(art.glyph_bank.glyphs),
        "rows": list(rows),
    }


def lcd_art_catalog() -> dict[str, CompiledLcdArt]:
    panels = (
        _bbs_badge_art(),
        _mesh_radar_art(),
        _packet_flow_art(),
        _signal_skyline_art(),
        _link_heat_art(),
    )
    return {panel.name: panel for panel in panels}


def lcd_art_catalog_payload(active: str = "bbs_badge") -> dict[str, Any]:
    catalog = lcd_art_catalog()
    if active not in catalog:
        raise LcdMenuError("art_panel_unknown", active)
    return {
        "schema": LCD_ART_CATALOG_SCHEMA,
        "active": active,
        "names": list(catalog),
        "panels": {name: panel.to_dict() for name, panel in catalog.items()},
    }


def compile_lcd_art_from_pbm(name: str, pbm_text: str) -> CompiledLcdArt:
    tokens = _pbm_tokens(pbm_text)
    if not tokens or tokens[0] != "P1":
        raise LcdMenuError("pbm_magic_invalid", name)
    if len(tokens) < 3:
        raise LcdMenuError("pbm_header_invalid", name)
    try:
        width = int(tokens[1])
        height = int(tokens[2])
    except ValueError as exc:
        raise LcdMenuError("pbm_dimensions_invalid", name) from exc
    if width != LCD_ART_PIXEL_WIDTH or height != LCD_ART_PIXEL_HEIGHT:
        raise LcdMenuError("pbm_dimensions_invalid", f"{width}x{height}")
    pixels = tokens[3:]
    expected = LCD_ART_PIXEL_WIDTH * LCD_ART_PIXEL_HEIGHT
    if len(pixels) != expected:
        raise LcdMenuError("pbm_pixel_count_invalid", f"{len(pixels)}:{expected}")
    if any(pixel not in {"0", "1"} for pixel in pixels):
        raise LcdMenuError("pbm_pixel_invalid", name)

    pixel_rows = [
        [1 if pixel == "1" else 0 for pixel in pixels[row * width : (row + 1) * width]]
        for row in range(height)
    ]
    tile_map: list[list[tuple[int, ...]]] = []
    for cell_row in range(LCD_ROWS):
        tile_row = []
        for cell_column in range(LCD_COLUMNS):
            rows = []
            for tile_y in range(LCD_ART_TILE_HEIGHT):
                row_byte = 0
                for tile_x in range(LCD_ART_TILE_WIDTH):
                    if pixel_rows[cell_row * LCD_ART_TILE_HEIGHT + tile_y][
                        cell_column * LCD_ART_TILE_WIDTH + tile_x
                    ]:
                        row_byte |= 1 << (LCD_ART_TILE_WIDTH - 1 - tile_x)
                rows.append(row_byte)
            tile_row.append(tuple(rows))
        tile_map.append(tile_row)
    return compile_lcd_art_tile_map(name, tile_map)


def compile_lcd_art_tile_map(
    name: str,
    tile_map: Sequence[Sequence[Sequence[int] | None]],
) -> CompiledLcdArt:
    safe_name = _art_name(name)
    if len(tile_map) != LCD_ROWS:
        raise LcdMenuError("art_tile_rows_invalid", str(len(tile_map)))
    slot_by_tile: dict[tuple[int, ...], int] = {}
    tiles_by_slot: list[tuple[int, ...]] = []
    cell_slots: list[tuple[int | None, ...]] = []
    preview_lines: list[str] = []

    for row in tile_map:
        if len(row) != LCD_COLUMNS:
            raise LcdMenuError("art_tile_columns_invalid", str(len(row)))
        row_slots: list[int | None] = []
        preview_cells: list[str] = []
        for cell in row:
            tile = _normalize_art_tile(cell)
            if tile == ART_BLANK_TILE:
                row_slots.append(None)
                preview_cells.append(" ")
                continue
            if tile not in slot_by_tile:
                if len(slot_by_tile) >= 8:
                    raise LcdMenuError("art_glyph_overflow", safe_name)
                slot_by_tile[tile] = len(slot_by_tile)
                tiles_by_slot.append(tile)
            slot = slot_by_tile[tile]
            row_slots.append(slot)
            preview_cells.append(str(slot))
        cell_slots.append(tuple(row_slots))
        preview_lines.append("".join(preview_cells))

    glyphs = tuple(
        Glyph(slot, f"{safe_name}_{slot}", tile)
        for slot, tile in enumerate(tiles_by_slot)
    )
    return CompiledLcdArt(
        name=safe_name,
        preview_lines=tuple(preview_lines),
        glyph_bank=GlyphBank(safe_name, glyphs),
        cell_slots=tuple(cell_slots),
    )


def sample_art_panel() -> CompiledLcdArt:
    return lcd_art_catalog()["bbs_badge"]


def art_panel_for_index(index: int) -> CompiledLcdArt:
    catalog = lcd_art_catalog()
    names = tuple(catalog)
    return catalog[names[_art_index(index)]]


def _bbs_badge_art() -> CompiledLcdArt:
    frame = (0x1F, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1F, 0x00)
    fill = (0x1F,) * LCD_ART_TILE_HEIGHT
    diag = (0x10, 0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08)
    tile_map = [[None for _ in range(LCD_COLUMNS)] for _ in range(LCD_ROWS)]
    for column in range(LCD_COLUMNS):
        tile_map[0][column] = frame
        tile_map[LCD_ROWS - 1][column] = frame
    for row in range(1, LCD_ROWS - 1):
        tile_map[row][0] = frame
        tile_map[row][LCD_COLUMNS - 1] = frame
    for column in range(5, 15):
        tile_map[1][column] = fill
    for column in range(7, 13):
        tile_map[2][column] = diag
    return compile_lcd_art_tile_map("bbs_badge", tile_map)


def _mesh_radar_art() -> CompiledLcdArt:
    ring = (0x0E, 0x11, 0x15, 0x11, 0x15, 0x11, 0x0E, 0x00)
    spoke = (0x04, 0x04, 0x04, 0x1F, 0x04, 0x04, 0x04, 0x00)
    sweep = (0x10, 0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08)
    blip = (0x00, 0x04, 0x0E, 0x04, 0x00, 0x04, 0x00, 0x00)
    tile_map = [[None for _ in range(LCD_COLUMNS)] for _ in range(LCD_ROWS)]
    for row, column in ((0, 4), (0, 15), (1, 9), (2, 8), (3, 13)):
        tile_map[row][column] = blip
    for row in range(LCD_ROWS):
        tile_map[row][0] = spoke
        tile_map[row][LCD_COLUMNS - 1] = spoke
    for column in range(7, 13):
        tile_map[1][column] = ring if column in {8, 11} else sweep
        tile_map[2][column] = sweep if column in {7, 12} else ring
    return compile_lcd_art_tile_map("mesh_radar", tile_map)


def _packet_flow_art() -> CompiledLcdArt:
    node = (0x0E, 0x11, 0x15, 0x15, 0x15, 0x11, 0x0E, 0x00)
    rail = (0x00, 0x00, 0x1F, 0x04, 0x1F, 0x00, 0x00, 0x00)
    arrow = (0x04, 0x06, 0x1F, 0x06, 0x04, 0x00, 0x1F, 0x00)
    pulse = (0x04, 0x0E, 0x1F, 0x0E, 0x04, 0x00, 0x04, 0x00)
    tile_map = [[None for _ in range(LCD_COLUMNS)] for _ in range(LCD_ROWS)]
    for row in (0, 3):
        tile_map[row][1] = node
        tile_map[row][18] = node
        for column in range(3, 17):
            tile_map[row][column] = rail
        tile_map[row][10] = arrow
    for column in (5, 8, 11, 14):
        tile_map[1][column] = pulse
    for column in (4, 9, 13, 16):
        tile_map[2][column] = arrow
    return compile_lcd_art_tile_map("packet_flow", tile_map)


def _signal_skyline_art() -> CompiledLcdArt:
    levels = (
        (0x00, 0x00, 0x00, 0x00, 0x10, 0x10, 0x10, 0x10),
        (0x00, 0x00, 0x00, 0x08, 0x18, 0x18, 0x18, 0x18),
        (0x00, 0x00, 0x04, 0x0C, 0x1C, 0x1C, 0x1C, 0x1C),
        (0x00, 0x02, 0x06, 0x0E, 0x1E, 0x1E, 0x1E, 0x1E),
        (0x01, 0x03, 0x07, 0x0F, 0x1F, 0x1F, 0x1F, 0x1F),
    )
    sparkle = (0x04, 0x0E, 0x15, 0x0E, 0x04, 0x00, 0x00, 0x00)
    tile_map = [[None for _ in range(LCD_COLUMNS)] for _ in range(LCD_ROWS)]
    pattern = (0, 1, 2, 3, 4, 3, 2, 4, 1, 3, 4, 2, 1, 0, 2, 3, 4, 2, 1, 0)
    for column, level in enumerate(pattern):
        tile_map[3][column] = levels[level]
    for column in (2, 9, 15):
        tile_map[0][column] = sparkle
    for column in (5, 12, 18):
        tile_map[1][column] = levels[1]
    return compile_lcd_art_tile_map("signal_skyline", tile_map)


def _link_heat_art() -> CompiledLcdArt:
    cold = (0x00, 0x00, 0x0E, 0x11, 0x11, 0x0E, 0x00, 0x00)
    warm = (0x00, 0x0E, 0x1F, 0x15, 0x15, 0x1F, 0x0E, 0x00)
    hot = (0x1F, 0x1F, 0x1B, 0x15, 0x15, 0x1B, 0x1F, 0x1F)
    guard = (0x1F, 0x10, 0x17, 0x14, 0x17, 0x10, 0x1F, 0x00)
    tile_map = [[None for _ in range(LCD_COLUMNS)] for _ in range(LCD_ROWS)]
    row_patterns = (
        (cold, cold, warm, warm, hot),
        (cold, warm, hot, warm, cold),
        (warm, hot, hot, warm, cold),
        (guard, cold, warm, hot, guard),
    )
    for row, pattern in enumerate(row_patterns):
        for block, tile in enumerate(pattern):
            for offset in range(3):
                column = 1 + block * 4 + offset
                if column < LCD_COLUMNS:
                    tile_map[row][column] = tile
    tile_map[0][0] = guard
    tile_map[3][LCD_COLUMNS - 1] = guard
    return compile_lcd_art_tile_map("link_heat", tile_map)


def _render_art_page_lines(
    page: Mapping[str, Any],
    view: MenuViewState,
) -> tuple[tuple[str, ...], dict[str, Any]]:
    catalog_map = lcd_art_catalog()
    names = tuple(catalog_map)
    active_index = _art_index(view.art_index)
    active_name = names[active_index]
    art = catalog_map[active_name]
    catalog = lcd_art_catalog_payload(active_name)
    selected_id = str(page["items"][view.selected_item]["id"])
    viewport = {
        "source_xml_version": MENU_SCHEMA,
        "source_xml_file": SOURCE_XML,
        "selected_item_id": selected_id,
        "selected_item_index": view.selected_item,
        "visible_item_ids": [selected_id] * LCD_ROWS,
        "physical_indicator_row": 0,
        "viewport_top_line": 0,
        "viewport_top_item": str(page["items"][0]["id"]),
        "viewport_top_item_line": 0,
        "horizontal_scroll_offsets": [0] * LCD_ROWS,
        "marquee_hold_ms": MARQUEE_HOLD_MS,
        "marquee_step_ms": MARQUEE_STEP_MS,
        "marquee_gap": MARQUEE_GAP,
        "logical_line_count": int(page["line_count"]),
        "page_item_count": len(page["items"]),
        "art_active_index": active_index,
        "art_active_name": active_name,
        "art_panel_count": len(names),
        "art_panel": art.to_dict(),
        "art_catalog": catalog,
    }
    return art.preview_lines, viewport


def horizontal_bar(value: int, maximum: int, width: int = 10) -> str:
    width = max(1, width)
    maximum = max(1, maximum)
    filled = round(max(0, min(value, maximum)) * width / maximum)
    return "[" + ("#" * filled).ljust(width, "-") + "]"


def slider(value: int, minimum: int, maximum: int, width: int = 12) -> str:
    width = max(2, width)
    span = max(1, maximum - minimum)
    clamped = max(minimum, min(value, maximum))
    position = round((clamped - minimum) * (width - 1) / span)
    cells = ["-"] * width
    cells[position] = "o"
    return "|" + "".join(cells) + "|"


def vertical_chart(values: Sequence[int], height: int = 4, width: int = 8) -> tuple[str, ...]:
    height = max(1, height)
    width = max(1, width)
    trimmed = list(values)[-width:] or [0]
    maximum = max(1, max(trimmed))
    levels = [
        0 if value <= 0 else max(1, (value * height + maximum - 1) // maximum)
        for value in trimmed
    ]
    levels = ([0] * (width - len(levels)) + levels)[-width:]
    rows = []
    for row in range(height, 0, -1):
        rows.append("".join("#" if level >= row else " " for level in levels))
    return tuple(rows)


def signal_bars(rssi: int) -> str:
    if rssi >= -55:
        bars = 4
    elif rssi >= -70:
        bars = 3
    elif rssi >= -85:
        bars = 2
    elif rssi >= -100:
        bars = 1
    else:
        bars = 0
    return "SIG:" + ("#" * bars).ljust(4, "-")


def queue_indicator(pending: int, failed: int, retry: int) -> str:
    if failed:
        return f"Q! P{pending} F{failed}"
    if retry:
        return f"Q~ P{pending} R{retry}"
    return f"Q= P{pending}"


def custody_indicator(status: str, acked: int, failed: int) -> str:
    label = _upper(status)
    if failed:
        return f"C! {label} F{failed}"
    return f"C= {label} A{acked}"


def validate_intent_payload(payload: Mapping[str, Any]) -> None:
    assert_no_secret_fields(payload)
    unknown = sorted(set(payload) - API_INTENT_FIELDS)
    if unknown:
        raise LcdMenuError("intent_field_unknown", ",".join(unknown))


def spinner_frame(tick: int) -> str:
    return SPINNER_FRAMES[tick % len(SPINNER_FRAMES)]


def gauge_demo(value: int, maximum: int) -> str:
    maximum = max(1, maximum)
    width = 7
    position = round(max(0, min(value, maximum)) * (width - 1) / maximum)
    cells = ["-"] * width
    cells[position] = "^"
    return "G[" + "".join(cells) + "]"


DIGIT_PATTERNS = {
    "0": (" _ ", "| |", "|_|"),
    "1": ("   ", "  |", "  |"),
    "2": (" _ ", " _|", "|_ "),
    "3": (" _ ", " _|", " _|"),
    "4": ("   ", "|_|", "  |"),
    "5": (" _ ", "|_ ", " _|"),
    "6": (" _ ", "|_ ", "|_|"),
    "7": (" _ ", "  |", "  |"),
    "8": (" _ ", "|_|", "|_|"),
    "9": (" _ ", "|_|", " _|"),
}


def big_digits(value: int) -> tuple[str, str, str]:
    text = str(max(0, min(value, 99))).rjust(2)
    rows = ["", "", ""]
    for character in text:
        pattern = DIGIT_PATTERNS.get(character, ("   ", "   ", "   "))
        for index, segment in enumerate(pattern):
            rows[index] += segment
    return tuple(row.rstrip() for row in rows)


@dataclass(frozen=True)
class BrowserApiResponse:
    status: int
    body: Mapping[str, Any]
    headers: Mapping[str, str]


class LcdBrowserMirror:
    """Host-only request shim for browser mirror tests; it opens no socket."""

    def __init__(self, snapshot: Mapping[str, Any], view: MenuViewState | None = None) -> None:
        self.snapshot = snapshot
        self.view = view or MenuViewState()
        self.previous_lines: tuple[str, ...] | None = None
        self.now_ms = 0
        self._closed = False

    @property
    def closed(self) -> bool:
        return self._closed

    def close(self) -> None:
        self._closed = True

    def reopen(
        self,
        snapshot: Mapping[str, Any],
        view: MenuViewState | None = None,
    ) -> "LcdBrowserMirror":
        self.snapshot = snapshot
        self.view = view or MenuViewState()
        self.previous_lines = None
        self.now_ms = 0
        self._closed = False
        return self

    def __enter__(self) -> "LcdBrowserMirror":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()

    def handle_request(
        self,
        method: str,
        path: str,
        body: Mapping[str, Any] | str | bytes | None = None,
    ) -> BrowserApiResponse:
        if self._closed:
            return _api_response(410, {"error": "interface_closed"})
        method = method.upper()
        try:
            if method == "GET" and path == API_STATE_PATH:
                return self._state_response()
            if method == "POST" and path == API_INTENT_PATH:
                payload = _parse_body(body)
                validate_intent_payload(payload)
                intent = str(payload.get("intent", ""))
                if intent not in INPUT_EVENTS:
                    raise LcdMenuError("unsupported_input", intent)
                rendered_before = render(self.snapshot, self.view, now_ms=self.now_ms)
                self.previous_lines = rendered_before.lines
                self.view = apply_input(self.view, intent)
                self.now_ms = 0
                return self._state_response()
            if path in {API_STATE_PATH, API_INTENT_PATH}:
                return _api_response(405, {"error": "method_closed"})
            return _api_response(404, {"error": "route_closed"})
        except (json.JSONDecodeError, LcdMenuError) as exc:
            if isinstance(exc, LcdMenuError):
                return _api_response(400, {"error": exc.reason, "detail": exc.detail})
            return _api_response(400, {"error": "json_invalid", "detail": str(exc)})

    def _state_response(self) -> BrowserApiResponse:
        rendered = render(
            self.snapshot,
            self.view,
            previous_lines=self.previous_lines,
            now_ms=self.now_ms,
        )
        self.previous_lines = rendered.lines
        return _api_response(200, rendered.to_dict())


def build_browser_document(rendered: RenderedLcdMenu) -> str:
    cursor_ddram = f"0x{rendered.cursor.ddram_address:02X}"
    selected_item = str(rendered.viewport.get("selected_item_id", ""))
    lines = "\n".join(
        (
            f'      <div class="lcd-row{" lcd-row-cursor" if index == rendered.cursor.row else ""}" '
            f'data-row="{index}" '
            f'data-item="{html.escape(str(rendered.viewport["visible_item_ids"][index]))}" '
            f'data-scroll-offset="{rendered.viewport["horizontal_scroll_offsets"][index]}" '
            f'data-cursor="{str(index == rendered.cursor.row).lower()}">'
            f"{html.escape(line)}</div>"
        )
        for index, line in enumerate(rendered.lines)
    )
    glyphs = "\n".join(
        f"      <li>{glyph.slot}: {html.escape(glyph.name)}</li>"
        for glyph in rendered.glyph_bank
    )
    payload = (
        json.dumps(rendered.to_dict(), sort_keys=True)
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )
    pixel_preview = _browser_pixel_preview(rendered)
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>BBS LCD Mirror</title>
    <style>
      body {{ background: #111; color: #d7ffd7; font-family: monospace; }}
      .lcd {{ display: inline-block; border: 2px solid #6a8; padding: 12px; }}
      .lcd-row {{ white-space: pre; letter-spacing: 0; }}
      .lcd-row-cursor {{ outline: 1px solid #d7ffd7; }}
      .lcd-status {{ margin-top: 8px; }}
      button {{ font: inherit; }}
    </style>
  </head>
  <body data-schema="{html.escape(rendered.schema)}" data-page="{html.escape(rendered.page)}" data-glyph-bank="{html.escape(rendered.glyph_bank_name)}" data-source-xml="{html.escape(rendered.source_xml_version)}">
    <main class="lcd" aria-label="20 by 4 LCD mirror" data-selected-item="{html.escape(selected_item)}" data-viewport-top-line="{rendered.viewport["viewport_top_line"]}" data-cursor-row="{rendered.cursor.row}" data-cursor-column="{rendered.cursor.column}" data-cursor-ddram="{cursor_ddram}" data-cursor-focus="{html.escape(rendered.cursor.focus)}">
{lines}
    </main>
    <div class="lcd-status" aria-label="Cursor" data-row="{rendered.cursor.row}" data-column="{rendered.cursor.column}" data-ddram="{cursor_ddram}" data-focus="{html.escape(rendered.cursor.focus)}">CUR R{rendered.cursor.row} C{rendered.cursor.column} DDRAM {cursor_ddram} {html.escape(rendered.cursor.focus)}</div>
    <nav aria-label="Local LCD intents">
      <button type="button" data-intent="rotate_left">Left</button>
      <button type="button" data-intent="rotate_right">Right</button>
      <button type="button" data-intent="short_press">Select</button>
      <button type="button" data-intent="long_press">Back</button>
    </nav>
    <section aria-label="Glyph bank" data-glyph-bank="{html.escape(rendered.glyph_bank_name)}">
      <ol>
{glyphs}
      </ol>
    </section>
{pixel_preview}
    <script type="application/json" id="lcd-render-state">{payload}</script>
  </body>
</html>
"""


def _pixel_preview_rows(art: CompiledLcdArt) -> tuple[str, ...]:
    glyph_rows = {glyph.slot: glyph.rows for glyph in art.glyph_bank.glyphs}
    pixel_rows: list[str] = []
    for cell_row in art.cell_slots:
        for tile_y in range(LCD_ART_TILE_HEIGHT):
            pixels: list[str] = []
            for slot in cell_row:
                rows = ART_BLANK_TILE if slot is None else glyph_rows.get(slot)
                if rows is None:
                    raise LcdMenuError("art_slot_unknown", str(slot))
                row_byte = rows[tile_y]
                for tile_x in range(LCD_ART_TILE_WIDTH):
                    mask = 1 << (LCD_ART_TILE_WIDTH - 1 - tile_x)
                    pixels.append("#" if row_byte & mask else ".")
            pixel_rows.append("".join(pixels))
    if len(pixel_rows) != LCD_ART_PIXEL_HEIGHT or any(
        len(row) != LCD_ART_PIXEL_WIDTH for row in pixel_rows
    ):
        raise LcdMenuError("pixel_preview_shape_invalid", art.name)
    return tuple(pixel_rows)


def _browser_pixel_preview(rendered: RenderedLcdMenu) -> str:
    art_panel = rendered.viewport.get("art_panel")
    if not isinstance(art_panel, Mapping):
        return ""
    preview = art_panel.get("pixel_preview")
    if not isinstance(preview, Mapping):
        return ""
    rows = preview.get("rows")
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes, bytearray)):
        return ""
    preview_text = "\n".join(html.escape(str(row)) for row in rows)
    schema = html.escape(str(preview.get("schema", "")))
    art_name = html.escape(str(preview.get("source_art_name", "")))
    return f"""    <section aria-label="LCD pixel preview" data-pixel-preview-schema="{schema}" data-art-name="{art_name}" data-pixel-width="{preview.get("pixel_width", 0)}" data-pixel-height="{preview.get("pixel_height", 0)}">
      <pre>{preview_text}</pre>
    </section>"""


def _render_page_lines(
    snapshot: Mapping[str, Any],
    page: Mapping[str, Any],
    view: MenuViewState,
    now_ms: int,
) -> tuple[tuple[str, ...], dict[str, Any]]:
    visible_lines: list[str] = []
    visible_item_ids: list[str] = []
    scroll_offsets: list[int] = []
    top_line = view.viewport_top_line
    selected_id = str(page["items"][view.selected_item]["id"])
    for physical_row in range(LCD_ROWS):
        logical_line = top_line + physical_row
        item_index, row_offset = _item_for_line(page, logical_line)
        if item_index is None:
            visible_lines.append(" " * LCD_COLUMNS)
            visible_item_ids.append("")
            scroll_offsets.append(0)
            continue
        item = page["items"][item_index]
        item_id = str(item["id"])
        is_selected = item_index == view.selected_item
        indicator = ">" if is_selected and row_offset == 0 else ":" if is_selected else "|"
        if row_offset == 0:
            text = str(item["label"])
        else:
            text = str(item["rows"][row_offset - 1])
        text = _expand_tokens(text, snapshot)
        offset = _marquee_offset(text, now_ms) if is_selected else 0
        content = _marquee_content(text, offset) if is_selected else _content_fit(text)
        visible_lines.append(indicator + content)
        visible_item_ids.append(item_id)
        scroll_offsets.append(offset)
    viewport_top_item, viewport_top_row_offset = _item_for_line(page, top_line)
    viewport = {
        "source_xml_version": MENU_SCHEMA,
        "source_xml_file": SOURCE_XML,
        "selected_item_id": selected_id,
        "selected_item_index": view.selected_item,
        "visible_item_ids": visible_item_ids,
        "physical_indicator_row": view.selected_row,
        "viewport_top_line": top_line,
        "viewport_top_item": ""
        if viewport_top_item is None
        else str(page["items"][viewport_top_item]["id"]),
        "viewport_top_item_line": 0 if viewport_top_item is None else viewport_top_row_offset,
        "horizontal_scroll_offsets": scroll_offsets,
        "marquee_hold_ms": MARQUEE_HOLD_MS,
        "marquee_step_ms": MARQUEE_STEP_MS,
        "marquee_gap": MARQUEE_GAP,
        "logical_line_count": int(page["line_count"]),
        "page_item_count": len(page["items"]),
    }
    return tuple(visible_lines), viewport


def _normalized_view(view: MenuViewState) -> MenuViewState:
    page = _page_by_id(view.page)
    mode = _canonical_mode(_effective_mode(view))
    selected_item = _selected_item(page, view.selected_item)
    art_index = _art_index(view.art_index)
    line_start = _item_start_line(page, selected_item)
    selected_rows = int(page["items"][selected_item]["rows"].__len__()) + 1
    max_top = max(0, int(page["line_count"]) - LCD_ROWS)
    top = max(0, min(view.viewport_top_line, max_top))
    if line_start < top:
        top = line_start
    elif line_start + selected_rows > top + LCD_ROWS:
        top = max(0, line_start + selected_rows - LCD_ROWS)
    top = max(0, min(top, max_top))
    selected_row = max(0, min(LCD_ROWS - 1, line_start - top))
    return replace(
        view,
        page=str(page["id"]),
        selected_item=selected_item,
        viewport_top_line=top,
        selected_row=selected_row,
        art_index=art_index,
        mode=mode,
        detail=mode in {"detail", "edit_lab"},
    )


def _art_index(index: int) -> int:
    count = max(1, len(lcd_art_catalog()))
    return index % count


def _page_by_id(page_id: str) -> Mapping[str, Any]:
    for page in GENERATED_PAGES:
        if page["id"] == page_id:
            return page
    return GENERATED_PAGES[0]


def _selected_item(page: Mapping[str, Any], selected_item: int) -> int:
    item_count = max(1, len(page["items"]))
    return max(0, min(selected_item, item_count - 1))


def _item_start_line(page: Mapping[str, Any], selected_item: int) -> int:
    line = 0
    for index, item in enumerate(page["items"]):
        if index == selected_item:
            return line
        line += 1 + len(item["rows"])
    return 0


def _item_for_line(page: Mapping[str, Any], logical_line: int) -> tuple[int | None, int]:
    line = 0
    for index, item in enumerate(page["items"]):
        row_count = 1 + len(item["rows"])
        if line <= logical_line < line + row_count:
            return index, logical_line - line
        line += row_count
    return None, 0


def _marquee_offset(text: str, now_ms: int) -> int:
    clean = _ascii_clean(text)
    if len(clean) <= LCD_CONTENT_COLUMNS:
        return 0
    if now_ms < MARQUEE_HOLD_MS:
        return 0
    cycle = len(clean) + MARQUEE_GAP
    return ((now_ms - MARQUEE_HOLD_MS) // MARQUEE_STEP_MS) % cycle


def _marquee_content(text: str, offset: int) -> str:
    clean = _ascii_clean(text)
    if len(clean) <= LCD_CONTENT_COLUMNS:
        return clean.ljust(LCD_CONTENT_COLUMNS)
    loop = clean + (" " * MARQUEE_GAP) + clean
    return loop[offset : offset + LCD_CONTENT_COLUMNS].ljust(LCD_CONTENT_COLUMNS)


def _content_fit(text: str) -> str:
    clean = _ascii_clean(text)
    return clean[:LCD_CONTENT_COLUMNS].ljust(LCD_CONTENT_COLUMNS)


def _expand_tokens(text: str, snapshot: Mapping[str, Any]) -> str:
    result = str(text)
    for key in (
        "bridge.state",
        "custody.status",
        "errors.count",
        "errors.last",
        "files.done",
        "files.queued",
        "last_event",
        "link.acks",
        "link.rssi",
        "link.status",
        "mesh.heal",
        "mesh.hops",
        "mesh.mode",
        "mesh.root",
        "messages.inbox",
        "messages.new",
        "messages.outbox",
        "peers.active",
        "peers.count",
        "queue.failed",
        "queue.pending",
        "queue.retry",
        "telemetry.level",
        "uptime_ms",
        "xbee.surface",
    ):
        result = result.replace("{" + key + "}", _get(snapshot, *key.split(".")))
    return result


def _get(snapshot: Mapping[str, Any], *path: str, default: Any = "?") -> str:
    value: Any = snapshot
    for key in path:
        if not isinstance(value, Mapping) or key not in value:
            return str(default)
        value = value[key]
    if value is None or value == "":
        return str(default)
    return str(value)


def _upper(value: str) -> str:
    return value.upper() if value != "?" else value


def _lock(snapshot: Mapping[str, Any], key: str) -> str:
    locks = snapshot.get("locks", {})
    if not isinstance(locks, Mapping) or key not in locks:
        return "?"
    return "LOCK" if bool(locks[key]) else "OPEN"


def _format_uptime(value: str) -> str:
    try:
        milliseconds = int(value)
    except (TypeError, ValueError):
        return "?"
    seconds = max(0, milliseconds // 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h{minutes:02d}m"
    return f"{minutes}m{seconds:02d}s"


def _effective_mode(view: MenuViewState) -> str:
    mode = view.mode
    if mode == "page_browse" or mode == "row_browse":
        mode = "scroll"
    if mode not in NAVIGATION_MODES:
        raise LcdMenuError("navigation_mode_invalid", mode)
    return mode


def _canonical_mode(mode: str) -> str:
    if mode in {"page_browse", "row_browse"}:
        return "scroll"
    return mode


def _dirty_metadata(
    lines: Sequence[str],
    previous_lines: Sequence[str] | None,
) -> tuple[tuple[int, ...], tuple[tuple[int, int], ...]]:
    current = tuple(_fit(line) for line in lines)
    if previous_lines is None:
        return tuple(range(LCD_ROWS)), tuple(
            (row, column) for row in range(LCD_ROWS) for column in range(LCD_COLUMNS)
        )
    previous = tuple(_fit(line) for line in previous_lines)
    dirty_rows = []
    dirty_cells = []
    for row, line in enumerate(current):
        previous_line = previous[row] if row < len(previous) else " " * LCD_COLUMNS
        for column, character in enumerate(line):
            if column >= len(previous_line) or previous_line[column] != character:
                dirty_cells.append((row, column))
        if any(cell_row == row for cell_row, _ in dirty_cells):
            dirty_rows.append(row)
    return tuple(dirty_rows), tuple(dirty_cells)


def _safe_int(value: str, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _history_values(snapshot: Mapping[str, Any]) -> tuple[int, ...]:
    telemetry = snapshot.get("telemetry", {})
    if not isinstance(telemetry, Mapping):
        return (0,)
    history = telemetry.get("history", ())
    if not isinstance(history, Sequence) or isinstance(history, (str, bytes, bytearray)):
        return (0,)
    return tuple(_safe_int(str(value), 0) for value in history)


def _parse_body(body: Mapping[str, Any] | str | bytes | None) -> Mapping[str, Any]:
    if body is None:
        return {}
    if isinstance(body, Mapping):
        return body
    if isinstance(body, bytes):
        body = body.decode("utf-8")
    parsed = json.loads(body)
    if not isinstance(parsed, Mapping):
        raise LcdMenuError("json_object_required")
    return parsed


def _pbm_tokens(pbm_text: str) -> list[str]:
    tokens: list[str] = []
    for line in str(pbm_text).splitlines():
        tokens.extend(line.split("#", 1)[0].split())
    return tokens


def _normalize_art_tile(cell: Sequence[int] | None) -> tuple[int, ...]:
    if cell is None:
        return ART_BLANK_TILE
    tile = tuple(int(row) for row in cell)
    if len(tile) != LCD_ART_TILE_HEIGHT:
        raise LcdMenuError("art_tile_pattern_invalid", str(len(tile)))
    if any(row < 0 or row > 0x1F for row in tile):
        raise LcdMenuError("art_tile_row_byte_invalid")
    return tile


def _art_name(name: str) -> str:
    clean = "".join(char if char.isalnum() or char in {"_", "-"} else "_" for char in str(name))
    clean = clean.strip("_-").lower()
    if not clean:
        raise LcdMenuError("art_name_invalid")
    return clean


def _api_response(status: int, body: Mapping[str, Any]) -> BrowserApiResponse:
    return BrowserApiResponse(
        status=status,
        body=body,
        headers={"content-type": "application/json", "cache-control": "no-store"},
    )


def _fit(text: str) -> str:
    clean = _ascii_clean(text)
    if len(clean) > LCD_COLUMNS:
        return clean[:LCD_COLUMNS]
    return clean.ljust(LCD_COLUMNS)


def _ascii_clean(text: str) -> str:
    return "".join(char if 32 <= ord(char) < 127 else "?" for char in str(text))


def _load_snapshot(path: str | None) -> Mapping[str, Any]:
    if path is None:
        return sample_state()
    if path == "-":
        return json.load(sys.stdin)
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", nargs="?", help="JSON snapshot path, or '-' for stdin")
    parser.add_argument("--page", choices=PAGES, default="HOME")
    parser.add_argument("--now-ms", type=int, default=0, help="deterministic render tick")
    parser.add_argument("--browser-html", action="store_true", help="emit inert browser mirror HTML")
    args = parser.parse_args(argv)
    snapshot = _load_snapshot(args.snapshot)
    rendered = render(snapshot, MenuViewState(page=args.page), now_ms=args.now_ms)
    if args.browser_html:
        print(build_browser_document(rendered), end="")
    else:
        print(json.dumps(rendered.to_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
