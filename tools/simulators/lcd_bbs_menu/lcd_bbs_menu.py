#!/usr/bin/env python3
"""Host-only 20x4 LCD menu renderer for the ESP-NOW BBS field console."""

from __future__ import annotations

import argparse
import html
import json
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any


LCD_COLUMNS = 20
LCD_ROWS = 4
LCD_DDRAM_ROW_BASES = (0x00, 0x40, 0x14, 0x54)
SNAPSHOT_SCHEMA = "bbs_lcd_state.v1"
RENDER_SCHEMA = "bbs_lcd_render.v1"
GLYPH_SWAP_MIN_MS = 250
PAGES = (
    "HOME",
    "MESSAGES",
    "PEERS",
    "QUEUE",
    "FILES",
    "MESH",
    "XBEE",
    "DIAG",
    "LOCKS",
)
NAVIGATION_MODES = frozenset({"page_browse", "row_browse", "detail", "edit_lab"})
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
    selected_row: int = 0
    detail: bool = False
    notification_ack: bool = False
    last_intent: str = "home"
    mode: str = "page_browse"
    edit_value: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "page": self.page,
            "selected_row": self.selected_row,
            "detail": self.detail,
            "notification_ack": self.notification_ack,
            "last_intent": self.last_intent,
            "mode": self.mode,
            "edit_value": self.edit_value,
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
        row = view.selected_row if mode in {"row_browse", "detail", "edit_lab"} else 0
        row = max(0, min(LCD_ROWS - 1, row))
        column = 0 if mode != "edit_lab" else min(LCD_COLUMNS - 1, 10)
        focus = {
            "page_browse": "page",
            "row_browse": "row",
            "detail": "detail",
            "edit_lab": "edit",
        }[mode]
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
    page: str
    glyph_bank_name: str
    lines: tuple[str, ...]
    glyph_bank: tuple[Glyph, ...]
    view: MenuViewState
    cursor: CursorState
    widgets: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "page": self.page,
            "glyph_bank_name": self.glyph_bank_name,
            "lines": list(self.lines),
            "glyph_bank": [
                {"slot": glyph.slot, "name": glyph.name, "rows": list(glyph.rows)}
                for glyph in self.glyph_bank
            ],
            "view": self.view.to_dict(),
            "cursor": self.cursor.to_dict(),
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
            Glyph(7, "spinner", (0x04, 0x0E, 0x15, 0x04, 0x15, 0x0E, 0x04, 0x00)),
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
    "gauge_demo": GlyphBank(
        "gauge_demo",
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
}
GLYPH_BANK = GLYPH_BANKS["core_status"].glyphs
SPINNER_FRAMES = ("-", "\\", "|", "/")


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
    page_index = PAGES.index(view.page) if view.page in PAGES else 0
    page = PAGES[page_index]
    mode = _effective_mode(view)
    if event == "long_press":
        if mode == "page_browse":
            return MenuViewState(page="HOME", last_intent="home")
        return MenuViewState(
            page=page,
            selected_row=view.selected_row,
            last_intent="back",
            mode="page_browse",
            edit_value=view.edit_value,
        )
    if event == "short_press":
        if mode == "page_browse":
            return MenuViewState(
                page=page,
                selected_row=0,
                detail=True,
                notification_ack=True,
                last_intent="local_ack",
                mode="row_browse",
                edit_value=view.edit_value,
            )
        if mode == "row_browse":
            return MenuViewState(
                page=page,
                selected_row=view.selected_row,
                detail=True,
                notification_ack=False,
                last_intent="local_select",
                mode="detail",
                edit_value=view.edit_value,
            )
        if mode == "detail":
            return MenuViewState(
                page=page,
                selected_row=view.selected_row,
                detail=True,
                notification_ack=False,
                last_intent="edit_enter",
                mode="edit_lab",
                edit_value=view.edit_value,
            )
        return MenuViewState(
            page=page,
            selected_row=view.selected_row,
            detail=True,
            notification_ack=True,
            last_intent="local_commit",
            mode="row_browse",
            edit_value=view.edit_value,
        )
    if mode in {"row_browse", "detail"}:
        delta = 1 if event == "rotate_right" else -1
        return MenuViewState(
            page=page,
            selected_row=(view.selected_row + delta) % LCD_ROWS,
            detail=True,
            notification_ack=False,
            last_intent="row_next" if delta > 0 else "row_previous",
            mode=mode,
            edit_value=view.edit_value,
        )
    if mode == "edit_lab":
        delta = 5 if event == "rotate_right" else -5
        return MenuViewState(
            page=page,
            selected_row=view.selected_row,
            detail=True,
            notification_ack=False,
            last_intent="value_up" if delta > 0 else "value_down",
            mode="edit_lab",
            edit_value=(view.edit_value + delta) % 105,
        )
    delta = 1 if event == "rotate_right" else -1
    next_page = PAGES[(page_index + delta) % len(PAGES)]
    return MenuViewState(
        page=next_page,
        last_intent="page_next" if delta > 0 else "page_previous",
        mode="page_browse",
        edit_value=view.edit_value,
    )


def render(
    snapshot: Mapping[str, Any],
    view: MenuViewState | None = None,
    previous_lines: Sequence[str] | None = None,
    glyph_bank_name: str = "core_status",
) -> RenderedLcdMenu:
    validate_snapshot(snapshot)
    view = view or MenuViewState()
    if _effective_mode(view) not in NAVIGATION_MODES:
        raise LcdMenuError("navigation_mode_invalid", view.mode)
    if glyph_bank_name not in GLYPH_BANKS:
        raise LcdMenuError("glyph_bank_unknown", glyph_bank_name)
    page = view.page if view.page in PAGES else "HOME"
    renderers = {
        "HOME": _render_home,
        "MESSAGES": _render_messages,
        "PEERS": _render_peers,
        "QUEUE": _render_queue,
        "FILES": _render_files,
        "MESH": _render_mesh,
        "XBEE": _render_xbee,
        "DIAG": _render_diag,
        "LOCKS": _render_locks,
    }
    lines = tuple(_fit(line) for line in renderers[page](snapshot))
    if len(lines) != LCD_ROWS or any(len(line) != LCD_COLUMNS for line in lines):
        raise LcdMenuError("render_shape_invalid", page)
    cursor = CursorTracker.from_lines(lines, view, previous_lines)
    return RenderedLcdMenu(
        schema=RENDER_SCHEMA,
        page=page,
        glyph_bank_name=glyph_bank_name,
        lines=lines,
        glyph_bank=GLYPH_BANKS[glyph_bank_name].glyphs,
        view=view,
        cursor=cursor,
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
        "locks": {"relay": True, "xbee": True, "flash": True, "serial_write": True},
        "last_event": "ACK peer01",
        "uptime_ms": 125000,
    }


def _render_home(snapshot: Mapping[str, Any]) -> tuple[str, str, str, str]:
    return (
        f"BBS {_upper(_get(snapshot, 'mode'))} LINK:{_upper(_get(snapshot, 'link', 'status'))}",
        f"Peers:{_get(snapshot, 'peers', 'count')} Queue:{_get(snapshot, 'queue', 'pending')}",
        f"Cust:{_get(snapshot, 'custody', 'owner')}",
        f"Last:{_get(snapshot, 'last_event')}",
    )


def _render_messages(snapshot: Mapping[str, Any]) -> tuple[str, str, str, str]:
    return (
        f"MSG N:{_get(snapshot, 'messages', 'new')} IN:{_get(snapshot, 'messages', 'inbox')}",
        f"OUT:{_get(snapshot, 'messages', 'outbox')} ACK:{_get(snapshot, 'custody', 'acked')}",
        f"Custody:{_get(snapshot, 'custody', 'status')}",
        f"Last:{_get(snapshot, 'last_event')}",
    )


def _render_peers(snapshot: Mapping[str, Any]) -> tuple[str, str, str, str]:
    return (
        f"PEERS {_get(snapshot, 'peers', 'active')}/{_get(snapshot, 'peers', 'count')}",
        f"Link:{_upper(_get(snapshot, 'link', 'status'))} RSSI:{_get(snapshot, 'link', 'rssi')}",
        f"ACK:{_get(snapshot, 'link', 'acks')} Dup:{_get(snapshot, 'link', 'dups')}",
        f"Mesh:{_get(snapshot, 'mesh', 'root')}",
    )


def _render_queue(snapshot: Mapping[str, Any]) -> tuple[str, str, str, str]:
    return (
        f"QUEUE P:{_get(snapshot, 'queue', 'pending')} F:{_get(snapshot, 'queue', 'failed')}",
        f"Retry:{_get(snapshot, 'queue', 'retry')}",
        f"Cust:{_get(snapshot, 'custody', 'status')}",
        "Control:CLOSED",
    )


def _render_files(snapshot: Mapping[str, Any]) -> tuple[str, str, str, str]:
    return (
        f"FILES Q:{_get(snapshot, 'files', 'queued')} D:{_get(snapshot, 'files', 'done')}",
        f"Bytes:{_get(snapshot, 'files', 'bytes')}",
        "Names:CLOSED",
        "Transfer:CLOSED",
    )


def _render_mesh(snapshot: Mapping[str, Any]) -> tuple[str, str, str, str]:
    return (
        f"MESH {_get(snapshot, 'mesh', 'mode')}",
        f"Root:{_get(snapshot, 'mesh', 'root')}",
        f"Hops:{_get(snapshot, 'mesh', 'hops')} Heal:{_get(snapshot, 'mesh', 'heal')}",
        "Live:CLOSED",
    )


def _render_xbee(snapshot: Mapping[str, Any]) -> tuple[str, str, str, str]:
    surface = _upper(_get(snapshot, "xbee", "surface", default="CLOSED"))
    if surface == "?":
        surface = "CLOSED"
    return (
        f"XBEE {surface}",
        "UART:CLOSED",
        f"NP:{_get(snapshot, 'xbee', 'np')}",
        "TX CLOSED",
    )


def _render_diag(snapshot: Mapping[str, Any]) -> tuple[str, str, str, str]:
    return (
        f"DIAG {_upper(_get(snapshot, 'mode'))}",
        f"Up:{_format_uptime(_get(snapshot, 'uptime_ms'))}",
        f"LCD:{_get(snapshot, 'telemetry', 'lcd', default='sim')}",
        f"Event:{_get(snapshot, 'last_event')}",
    )


def _render_locks(snapshot: Mapping[str, Any]) -> tuple[str, str, str, str]:
    return (
        "LOCKS",
        f"Relay:{_lock(snapshot, 'relay')}",
        f"XBee:{_lock(snapshot, 'xbee')}",
        f"Flash:{_lock(snapshot, 'flash')} Ser:{_lock(snapshot, 'serial_write')}",
    )


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
    }


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

    def handle_request(
        self,
        method: str,
        path: str,
        body: Mapping[str, Any] | str | bytes | None = None,
    ) -> BrowserApiResponse:
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
                rendered_before = render(self.snapshot, self.view)
                self.previous_lines = rendered_before.lines
                self.view = apply_input(self.view, intent)
                return self._state_response()
            if path in {API_STATE_PATH, API_INTENT_PATH}:
                return _api_response(405, {"error": "method_closed"})
            return _api_response(404, {"error": "route_closed"})
        except (json.JSONDecodeError, LcdMenuError) as exc:
            if isinstance(exc, LcdMenuError):
                return _api_response(400, {"error": exc.reason, "detail": exc.detail})
            return _api_response(400, {"error": "json_invalid", "detail": str(exc)})

    def _state_response(self) -> BrowserApiResponse:
        rendered = render(self.snapshot, self.view, previous_lines=self.previous_lines)
        self.previous_lines = rendered.lines
        return _api_response(200, rendered.to_dict())


def build_browser_document(rendered: RenderedLcdMenu) -> str:
    cursor_ddram = f"0x{rendered.cursor.ddram_address:02X}"
    lines = "\n".join(
        (
            f'      <div class="lcd-row{" lcd-row-cursor" if index == rendered.cursor.row else ""}" '
            f'data-row="{index}" '
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
  <body data-schema="{html.escape(rendered.schema)}" data-page="{html.escape(rendered.page)}" data-glyph-bank="{html.escape(rendered.glyph_bank_name)}">
    <main class="lcd" aria-label="20 by 4 LCD mirror" data-cursor-row="{rendered.cursor.row}" data-cursor-column="{rendered.cursor.column}" data-cursor-ddram="{cursor_ddram}" data-cursor-focus="{html.escape(rendered.cursor.focus)}">
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
    <script type="application/json" id="lcd-render-state">{payload}</script>
  </body>
</html>
"""


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
    if mode == "page_browse" and view.detail:
        mode = "row_browse"
    if mode not in NAVIGATION_MODES:
        raise LcdMenuError("navigation_mode_invalid", mode)
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


def _api_response(status: int, body: Mapping[str, Any]) -> BrowserApiResponse:
    return BrowserApiResponse(
        status=status,
        body=body,
        headers={"content-type": "application/json", "cache-control": "no-store"},
    )


def _fit(text: str) -> str:
    clean = "".join(char if 32 <= ord(char) < 127 else "?" for char in str(text))
    if len(clean) > LCD_COLUMNS:
        return clean[:LCD_COLUMNS]
    return clean.ljust(LCD_COLUMNS)


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
    parser.add_argument("--browser-html", action="store_true", help="emit inert browser mirror HTML")
    args = parser.parse_args(argv)
    snapshot = _load_snapshot(args.snapshot)
    rendered = render(snapshot, MenuViewState(page=args.page))
    if args.browser_html:
        print(build_browser_document(rendered), end="")
    else:
        print(json.dumps(rendered.to_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
