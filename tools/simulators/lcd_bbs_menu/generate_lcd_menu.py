#!/usr/bin/env python3
"""Generate host and firmware LCD menu data from build-time XML."""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[3]
SIM_DIR = Path(__file__).resolve().parent
XML_PATH = SIM_DIR / "bbs_lcd_menu.v1.xml"
PY_MODEL_PATH = SIM_DIR / "generated_menu.py"
FW_HEADER_PATH = ROOT / "firmware/projects/four-relay-xbee-wifi/main/bbs_lcd_menu_generated.h"

MENU_SCHEMA = "bbs_lcd_menu.v1"
RENDER_SCHEMA = "bbs_lcd_render.v2"
FIRMWARE_ID = "PF0530N"
SOURCE_ID = "SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530N-SCROLLING-XML-2026-06-01"

ALLOWED_GLYPH_BANKS = {
    "core_status": 0,
    "horizontal_bar": 1,
    "vertical_chart": 2,
    "big_digits": 3,
    "gauge_demo": 4,
    "table": 5,
}
WIDGET_GLYPH_BANKS = frozenset({"horizontal_bar", "vertical_chart", "big_digits", "gauge_demo"})
ALLOWED_ACTIONS = frozenset({"page", "detail", "edit", "back"})
ALLOWED_MENU_ATTRS = frozenset({"schema", "sourceId"})
ALLOWED_PAGE_ATTRS = frozenset({"id", "title", "glyphBank"})
ALLOWED_ITEM_ATTRS = frozenset({"id", "label", "action", "target", "editable", "rows", "table"})
ALLOWED_TAGS = frozenset({"menu", "page", "item", "row"})
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
ALLOWED_TEXT_TOKENS = frozenset(
    {
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
    }
)
IDENT_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
TOKEN_RE = re.compile(r"\{([^{}]+)\}")


class MenuGenerationError(ValueError):
    """Raised when the build-time XML menu contract fails closed."""


@dataclass(frozen=True)
class MenuItem:
    id: str
    label: str
    rows: tuple[str, ...]
    action: str
    target: str
    editable: bool
    table: bool

    @property
    def row_count(self) -> int:
        return 1 + len(self.rows)


@dataclass(frozen=True)
class MenuPage:
    id: str
    title: str
    glyph_bank: str
    items: tuple[MenuItem, ...]

    @property
    def line_count(self) -> int:
        return sum(item.row_count for item in self.items)


def load_menu(xml_path: Path = XML_PATH) -> tuple[MenuPage, ...]:
    raw = xml_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(raw)
    try:
        root = ElementTree.fromstring(raw)
    except ElementTree.ParseError as exc:
        raise MenuGenerationError(f"xml_parse_error:{exc}") from exc

    _require_tag(root, "menu")
    _require_attrs(root, ALLOWED_MENU_ATTRS, "menu")
    if root.attrib.get("schema") != MENU_SCHEMA:
        raise MenuGenerationError("schema_invalid")
    if root.attrib.get("sourceId") != FIRMWARE_ID:
        raise MenuGenerationError("source_id_invalid")

    page_ids: set[str] = set()
    item_ids: set[str] = set()
    pages: list[MenuPage] = []
    for page_node in root:
        _require_tag(page_node, "page")
        _require_attrs(page_node, ALLOWED_PAGE_ATTRS, "page")
        page_id = _required_id(page_node, "id")
        if page_id in page_ids:
            raise MenuGenerationError(f"duplicate_page_id:{page_id}")
        page_ids.add(page_id)
        title = _required_text_attr(page_node, "title")
        glyph_bank = _required_text_attr(page_node, "glyphBank")
        if glyph_bank not in ALLOWED_GLYPH_BANKS:
            raise MenuGenerationError(f"glyph_bank_unknown:{glyph_bank}")
        items: list[MenuItem] = []
        for item_node in page_node:
            _require_tag(item_node, "item")
            _require_attrs(item_node, ALLOWED_ITEM_ATTRS, "item")
            item_id = _required_id(item_node, "id")
            if item_id in item_ids:
                raise MenuGenerationError(f"duplicate_item_id:{item_id}")
            item_ids.add(item_id)
            label = _required_text_attr(item_node, "label")
            action = _required_text_attr(item_node, "action")
            if action not in ALLOWED_ACTIONS:
                raise MenuGenerationError(f"action_invalid:{item_id}:{action}")
            target = item_node.attrib.get("target", "")
            editable = _bool_attr(item_node.attrib.get("editable", "false"))
            table = _bool_attr(item_node.attrib.get("table", "false"))
            if editable and action != "edit":
                raise MenuGenerationError(f"editable_action_invalid:{item_id}")
            rows_attr = item_node.attrib.get("rows")
            rows = tuple(_clean_text(row_node.text or "") for row_node in item_node)
            if rows_attr is not None and int(rows_attr) != 1 + len(rows):
                raise MenuGenerationError(f"rows_count_mismatch:{item_id}")
            if len(rows) > 3:
                raise MenuGenerationError(f"item_rows_too_tall:{item_id}")
            if table and glyph_bank != "table":
                raise MenuGenerationError(f"table_bank_mismatch:{item_id}")
            if glyph_bank == "table" and any(bank in page_id.lower() for bank in WIDGET_GLYPH_BANKS):
                raise MenuGenerationError(f"table_widget_collision:{page_id}")
            _validate_text(label, f"{item_id}.label")
            for row_index, row_text in enumerate(rows):
                _validate_text(row_text, f"{item_id}.row{row_index}")
                if table and len(_strip_tokens(row_text)) > 19:
                    raise MenuGenerationError(f"table_row_too_wide:{item_id}:{row_index}")
            if table and len(_strip_tokens(label)) > 19:
                raise MenuGenerationError(f"table_label_too_wide:{item_id}")
            items.append(
                MenuItem(
                    id=item_id,
                    label=label,
                    rows=rows,
                    action=action,
                    target=target,
                    editable=editable,
                    table=table,
                )
            )
        if not items:
            raise MenuGenerationError(f"page_empty:{page_id}")
        pages.append(MenuPage(id=page_id, title=title, glyph_bank=glyph_bank, items=tuple(items)))

    for page in pages:
        for item in page.items:
            if item.action == "page":
                if not item.target:
                    raise MenuGenerationError(f"target_required:{item.id}")
                if item.target not in page_ids:
                    raise MenuGenerationError(f"target_unknown:{item.id}:{item.target}")
            elif item.target:
                raise MenuGenerationError(f"target_unexpected:{item.id}")
    return tuple(pages)


def generate_python_model(pages: tuple[MenuPage, ...], xml_path: Path = XML_PATH) -> str:
    page_dicts = [
        {
            "id": page.id,
            "title": page.title,
            "glyph_bank": page.glyph_bank,
            "line_count": page.line_count,
            "items": [
                {
                    "id": item.id,
                    "label": item.label,
                    "rows": item.rows,
                    "action": item.action,
                    "target": item.target,
                    "editable": item.editable,
                    "table": item.table,
                }
                for item in page.items
            ],
        }
        for page in pages
    ]
    return (
        "# Generated by tools/simulators/lcd_bbs_menu/generate_lcd_menu.py; do not edit.\n"
        "from __future__ import annotations\n\n"
        f"MENU_SCHEMA = {MENU_SCHEMA!r}\n"
        f"RENDER_SCHEMA = {RENDER_SCHEMA!r}\n"
        f"FIRMWARE_ID = {FIRMWARE_ID!r}\n"
        f"SOURCE_ID = {SOURCE_ID!r}\n"
        f"SOURCE_XML = {xml_path.name!r}\n"
        f"GLYPH_BANKS = {ALLOWED_GLYPH_BANKS!r}\n"
        f"PAGES = {page_dicts!r}\n"
    )


def generate_firmware_header(pages: tuple[MenuPage, ...]) -> str:
    item_arrays = []
    page_entries = []
    item_count = 0
    for page_index, page in enumerate(pages):
        array_name = f"fr_bbs_menu_items_{_c_ident(page.id)}"
        item_entries = []
        for item in page.items:
            item_count += 1
            rows = (item.rows + ("", "", ""))[:3]
            target_index = _page_index(pages, item.target) if item.target else 0
            item_entries.append(
                "    {"
                f"\"{_c_escape(item.id)}\", "
                f"\"{_c_escape(item.label)}\", "
                "{"
                + ", ".join(f"\"{_c_escape(row)}\"" for row in rows)
                + "}, "
                f"{item.row_count}u, "
                f"FR_BBS_ACTION_{item.action.upper()}, "
                f"{target_index}u, "
                f"{_c_bool(item.editable)}, "
                f"{_c_bool(item.table)}"
                "},"
            )
        item_arrays.append(
            f"static const fr_bbs_menu_item_t {array_name}[] = {{\n"
            + "\n".join(item_entries)
            + "\n};\n"
        )
        page_entries.append(
            "    {"
            f"\"{_c_escape(page.id)}\", "
            f"\"{_c_escape(page.title)}\", "
            f"{ALLOWED_GLYPH_BANKS[page.glyph_bank]}u, "
            f"{len(page.items)}u, "
            f"{page.line_count}u, "
            f"{array_name}"
            "},"
        )
        (void_page_index := page_index)
        _ = void_page_index

    return (
        "/* Generated by tools/simulators/lcd_bbs_menu/generate_lcd_menu.py; do not edit. */\n"
        "#ifndef BBS_LCD_MENU_GENERATED_H\n"
        "#define BBS_LCD_MENU_GENERATED_H\n\n"
        "#include <stdbool.h>\n"
        "#include <stdint.h>\n\n"
        f"#define FR_DIAG_FIRMWARE_ID_VALUE \"{FIRMWARE_ID}\"\n"
        f"#define FR_BBS_MENU_XML_SCHEMA \"{MENU_SCHEMA}\"\n"
        f"#define FR_BBS_MENU_RENDER_SCHEMA \"{RENDER_SCHEMA}\"\n"
        f"#define FR_BBS_MENU_SOURCE_ID \"{SOURCE_ID}\"\n"
        f"#define FR_BBS_MENU_PAGE_COUNT {len(pages)}u\n"
        f"#define FR_BBS_MENU_ITEM_COUNT {item_count}u\n"
        "#define FR_BBS_GLYPH_BANK_COUNT 6u\n"
        "#define FR_BBS_MENU_CONTENT_COLUMNS 19u\n"
        "#define FR_BBS_MENU_MARQUEE_HOLD_MS 750u\n"
        "#define FR_BBS_MENU_MARQUEE_STEP_MS 250u\n"
        "#define FR_BBS_MENU_MARQUEE_GAP 2u\n\n"
        "typedef enum {\n"
        "    FR_BBS_ACTION_PAGE = 0,\n"
        "    FR_BBS_ACTION_DETAIL,\n"
        "    FR_BBS_ACTION_EDIT,\n"
        "    FR_BBS_ACTION_BACK,\n"
        "} fr_bbs_menu_action_t;\n\n"
        "typedef struct {\n"
        "    const char *id;\n"
        "    const char *label;\n"
        "    const char *rows[3];\n"
        "    uint8_t row_count;\n"
        "    fr_bbs_menu_action_t action;\n"
        "    uint8_t target_page;\n"
        "    bool editable;\n"
        "    bool table;\n"
        "} fr_bbs_menu_item_t;\n\n"
        "typedef struct {\n"
        "    const char *id;\n"
        "    const char *title;\n"
        "    uint8_t glyph_bank_index;\n"
        "    uint8_t item_count;\n"
        "    uint8_t line_count;\n"
        "    const fr_bbs_menu_item_t *items;\n"
        "} fr_bbs_menu_page_t;\n\n"
        + "\n".join(item_arrays)
        + "\nstatic const fr_bbs_menu_page_t fr_bbs_generated_pages[FR_BBS_MENU_PAGE_COUNT] = {\n"
        + "\n".join(page_entries)
        + "\n};\n\n"
        "#endif /* BBS_LCD_MENU_GENERATED_H */\n"
    )


def write_generated(check: bool = False) -> int:
    pages = load_menu(XML_PATH)
    expected = {
        PY_MODEL_PATH: generate_python_model(pages, XML_PATH),
        FW_HEADER_PATH: generate_firmware_header(pages),
    }
    failed = False
    for path, content in expected.items():
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        if current == content:
            continue
        if check:
            failed = True
            diff = difflib.unified_diff(
                current.splitlines(),
                content.splitlines(),
                fromfile=str(path),
                tofile=f"{path} (expected)",
                lineterm="",
            )
            print("\n".join(diff), file=sys.stderr)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    return 1 if failed else 0


def _reject_unsafe_xml(raw: str) -> None:
    upper = raw.upper()
    for marker in ("<!DOCTYPE", "<!ENTITY", "SYSTEM", "PUBLIC"):
        if marker in upper:
            raise MenuGenerationError("xml_external_entity_rejected")
    if "<?" in raw:
        stripped = raw.lstrip()
        if not stripped.startswith("<?xml ") or "?>" not in stripped.splitlines()[0]:
            raise MenuGenerationError("xml_processing_instruction_rejected")


def _require_tag(node: ElementTree.Element, expected: str) -> None:
    if node.tag not in ALLOWED_TAGS:
        raise MenuGenerationError(f"tag_unknown:{node.tag}")
    if node.tag != expected:
        raise MenuGenerationError(f"tag_invalid:{node.tag}:{expected}")


def _require_attrs(node: ElementTree.Element, allowed: Iterable[str], context: str) -> None:
    unknown = sorted(set(node.attrib) - set(allowed))
    if unknown:
        raise MenuGenerationError(f"attribute_unknown:{context}:{','.join(unknown)}")
    for key, value in node.attrib.items():
        _reject_secret_name(key)
        _validate_text(value, f"{context}.{key}")


def _required_id(node: ElementTree.Element, attr: str) -> str:
    value = _required_text_attr(node, attr)
    if not IDENT_RE.match(value):
        raise MenuGenerationError(f"id_invalid:{value}")
    return value


def _required_text_attr(node: ElementTree.Element, attr: str) -> str:
    value = node.attrib.get(attr)
    if value is None or value == "":
        raise MenuGenerationError(f"attribute_required:{node.tag}.{attr}")
    return _clean_text(value)


def _clean_text(value: str) -> str:
    text = " ".join(value.split())
    if any(ord(char) < 32 or ord(char) >= 127 for char in text):
        raise MenuGenerationError("text_non_ascii")
    return text


def _validate_text(value: str, context: str) -> None:
    normalized_context = context.lower().replace("_", "").replace("-", "")
    _reject_secret_name(normalized_context)
    clean = _clean_text(value)
    _reject_secret_name(clean.lower().replace("_", "").replace("-", ""))
    for token in TOKEN_RE.findall(clean):
        if token not in ALLOWED_TEXT_TOKENS:
            raise MenuGenerationError(f"token_unknown:{context}:{token}")


def _reject_secret_name(value: str) -> None:
    lowered = value.lower().replace("_", "").replace("-", "")
    for marker in SECRET_FIELD_MARKERS:
        if marker in lowered:
            raise MenuGenerationError(f"secret_field_rejected:{value}")


def _strip_tokens(value: str) -> str:
    return TOKEN_RE.sub("X", value)


def _bool_attr(value: str) -> bool:
    if value == "true":
        return True
    if value == "false":
        return False
    raise MenuGenerationError(f"bool_invalid:{value}")


def _page_index(pages: tuple[MenuPage, ...], target: str) -> int:
    for index, page in enumerate(pages):
        if page.id == target:
            return index
    raise MenuGenerationError(f"target_unknown:{target}")


def _c_ident(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", value.lower())


def _c_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _c_bool(value: bool) -> str:
    return "true" if value else "false"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated files are stale")
    args = parser.parse_args(argv)
    try:
        return write_generated(check=args.check)
    except MenuGenerationError as exc:
        print(f"menu_generation_failed:{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
