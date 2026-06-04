#!/usr/bin/env python3
"""Generate CBBS RNW product menu data from product XML."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = Path(__file__).resolve().parent
XML_PATH = TOOL_DIR / "cbbs_rnw_menu.v1.xml"
TS_MODEL_PATH = ROOT / "packages/cbbs-product/src/hardwareToolsMenu.generated.ts"

MENU_SCHEMA = "cbbs_rnw_menu.v1"
APP_ID = "hardware-tools"

CAPABILITY_GROUPS = frozenset({"bench", "radio", "mesh", "firmware", "fabrication", "safety", "activity"})
EXECUTION_MODES = frozenset({"localOnly", "artifactReview", "bridgePreviewUnavailable", "tier3Closed"})
ACTION_STATES = frozenset(
    {"ready", "needsDevice", "needsSafetyCheck", "needsConfirmation", "running", "complete", "failed", "unavailable"}
)
VIEW_IDS = frozenset({"home", "messages", "downloads", "peers", "network", "diagnostics", "safety", "config", "evidence"})
INTENT_IDS = frozenset({"refresh", "filter", "open_detail", "compose_draft", "queue_file_request", "ack_local", "view_proof"})
BRIDGE_ACTION_IDS = frozenset(
    {
        "mesh.statusSnapshot",
        "mesh.serviceList",
        "radio.inventorySummary",
        "radio.queryPreview",
        "radio.profileCompare",
        "radio.changePreview",
        "firmware.artifactReview",
        "firmware.installPreview",
        "device.readinessCheck",
    }
)
KNOWN_ACTION_IDS = frozenset(
    {
        "hardware.benchTargetReview",
        "hardware.radioInventory",
        "hardware.radioReadStatusPlan",
        "hardware.radioProfileCompare",
        "hardware.radioChangePlan",
        "hardware.meshSummary",
        "hardware.meshServices",
        "hardware.firmwareBuildReview",
        "hardware.deviceUpdatePlan",
        "hardware.fabricationPrintAsset",
        "hardware.enclosureChecklist",
        "hardware.safetyGates",
        "hardware.recoveryChecklist",
        "hardware.evidencePacket",
    }
)
PAGE_ORDER = ("bench", "radio", "mesh", "firmware", "fabrication", "safety", "activity")

ALLOWED_TAGS = frozenset({"menu", "page", "section", "item"})
MENU_ATTRS = frozenset({"schema", "appId", "menuId", "label"})
PAGE_ATTRS = frozenset(
    {"pageId", "label", "targetPage", "capabilityGroup", "executionMode", "state", "viewId", "evidenceRef"}
)
SECTION_ATTRS = frozenset(
    {
        "sectionId",
        "label",
        "pageId",
        "targetPage",
        "capabilityGroup",
        "executionMode",
        "state",
        "summary",
        "evidenceRef",
    }
)
ITEM_ATTRS = frozenset(
    {
        "itemId",
        "actionId",
        "label",
        "pageId",
        "targetPage",
        "capabilityGroup",
        "executionMode",
        "state",
        "viewId",
        "intent",
        "summary",
        "bridgeActionId",
        "evidenceRef",
    }
)

ID_RE = re.compile(r"^[a-z][a-z0-9-]{1,63}$")
ACTION_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:\.[a-z][A-Za-z0-9]*)+$")
SECRET_MARKERS = frozenset(
    {
        "androidid",
        "credential",
        "deviceid",
        "lmk",
        "location",
        "macaddress",
        "password",
        "pmk",
        "privatekey",
        "secret",
        "token",
    }
)
FORBIDDEN_VISIBLE_PATTERNS = (
    re.compile(r"\badvanced details\b", re.IGNORECASE),
    re.compile(r"\bconfirmation text\b", re.IGNORECASE),
    re.compile(r"\brnw\b", re.IGNORECASE),
    re.compile(r"\bfixture-only\b", re.IGNORECASE),
    re.compile(r"\blocal-only\b", re.IGNORECASE),
    re.compile(r"\bsource[- ]?backed\b", re.IGNORECASE),
    re.compile(r"\bdeveloper\b", re.IGNORECASE),
    re.compile(r"\bschema\b", re.IGNORECASE),
    re.compile(r"\bADR\b", re.IGNORECASE),
    re.compile(r"\btask log\b", re.IGNORECASE),
    re.compile(r"\bCOM\d+\b", re.IGNORECASE),
    re.compile(r"\bserial\b", re.IGNORECASE),
    re.compile(r"\bXBee\b", re.IGNORECASE),
    re.compile(r"\bRF\b", re.IGNORECASE),
    re.compile(r"\bflash\b", re.IGNORECASE),
    re.compile(r"\brelay\b", re.IGNORECASE),
    re.compile(r"\bmains\b", re.IGNORECASE),
    re.compile(r"\bshell\b", re.IGNORECASE),
    re.compile(r"\bexec\b", re.IGNORECASE),
    re.compile(r"\bPowerShell\b", re.IGNORECASE),
    re.compile(r"\bpackage\b", re.IGNORECASE),
    re.compile(r"\bsigning?\b", re.IGNORECASE),
    re.compile(r"\brelease\b", re.IGNORECASE),
    re.compile(r"\bdeploy\b", re.IGNORECASE),
)


class RnwMenuGenerationError(ValueError):
    """Raised when the RNW menu XML contract fails closed."""


@dataclass(frozen=True)
class RnwMenuItem:
    item_id: str
    action_id: str
    label: str
    page_id: str
    target_page: str
    capability_group: str
    execution_mode: str
    state: str
    view_id: str
    intent: str
    summary: str
    bridge_action_id: str
    evidence_ref: str


@dataclass(frozen=True)
class RnwMenuSection:
    section_id: str
    label: str
    page_id: str
    target_page: str
    capability_group: str
    execution_mode: str
    state: str
    summary: str
    evidence_ref: str
    items: tuple[RnwMenuItem, ...]


@dataclass(frozen=True)
class RnwMenuPage:
    page_id: str
    label: str
    target_page: str
    capability_group: str
    execution_mode: str
    state: str
    view_id: str
    evidence_ref: str
    sections: tuple[RnwMenuSection, ...]


@dataclass(frozen=True)
class RnwMenu:
    schema: str
    app_id: str
    menu_id: str
    label: str
    pages: tuple[RnwMenuPage, ...]


def load_menu(xml_path: Path = XML_PATH) -> RnwMenu:
    raw = xml_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(raw)
    try:
        root = ElementTree.fromstring(raw)
    except ElementTree.ParseError as exc:
        raise RnwMenuGenerationError(f"xml_parse_error:{exc}") from exc

    _require_tag(root, "menu")
    _require_attrs(root, MENU_ATTRS, "menu")
    if root.attrib.get("schema") != MENU_SCHEMA:
        raise RnwMenuGenerationError("schema_invalid")
    if root.attrib.get("appId") != APP_ID:
        raise RnwMenuGenerationError("app_id_invalid")
    menu_id = _required_id(root, "menuId")
    label = _required_visible_attr(root, "label")

    page_ids: set[str] = set()
    section_ids: set[str] = set()
    item_ids: set[str] = set()
    action_ids: set[str] = set()
    pages: list[RnwMenuPage] = []

    for page_node in root:
        _require_tag(page_node, "page")
        _require_attrs(page_node, PAGE_ATTRS, "page")
        page_id = _required_id(page_node, "pageId")
        if page_id in page_ids:
            raise RnwMenuGenerationError(f"duplicate_page_id:{page_id}")
        page_ids.add(page_id)
        page = RnwMenuPage(
            page_id=page_id,
            label=_required_visible_attr(page_node, "label"),
            target_page=_required_id(page_node, "targetPage"),
            capability_group=_enum_attr(page_node, "capabilityGroup", CAPABILITY_GROUPS),
            execution_mode=_enum_attr(page_node, "executionMode", EXECUTION_MODES),
            state=_enum_attr(page_node, "state", ACTION_STATES),
            view_id=_enum_attr(page_node, "viewId", VIEW_IDS),
            evidence_ref=_optional_id(page_node, "evidenceRef"),
            sections=tuple(),
        )
        sections: list[RnwMenuSection] = []
        for section_node in page_node:
            _require_tag(section_node, "section")
            _require_attrs(section_node, SECTION_ATTRS, "section")
            section_id = _required_id(section_node, "sectionId")
            if section_id in section_ids:
                raise RnwMenuGenerationError(f"duplicate_section_id:{section_id}")
            section_ids.add(section_id)
            section_page = _required_id(section_node, "pageId")
            section_target = _required_id(section_node, "targetPage")
            items: list[RnwMenuItem] = []
            for item_node in section_node:
                _require_tag(item_node, "item")
                _require_attrs(item_node, ITEM_ATTRS, "item")
                item_id = _required_id(item_node, "itemId")
                if item_id in item_ids:
                    raise RnwMenuGenerationError(f"duplicate_item_id:{item_id}")
                item_ids.add(item_id)
                action_id = _required_action_id(item_node, "actionId")
                if action_id in action_ids:
                    raise RnwMenuGenerationError(f"duplicate_action_id:{action_id}")
                if action_id not in KNOWN_ACTION_IDS:
                    raise RnwMenuGenerationError(f"action_unknown:{action_id}")
                action_ids.add(action_id)
                bridge_action_id = _optional_action_id(item_node, "bridgeActionId")
                if bridge_action_id and bridge_action_id not in BRIDGE_ACTION_IDS:
                    raise RnwMenuGenerationError(f"bridge_action_unknown:{bridge_action_id}")
                item_page = _required_id(item_node, "pageId")
                item_target = _required_id(item_node, "targetPage")
                item = RnwMenuItem(
                    item_id=item_id,
                    action_id=action_id,
                    label=_required_visible_attr(item_node, "label"),
                    page_id=item_page,
                    target_page=item_target,
                    capability_group=_enum_attr(item_node, "capabilityGroup", CAPABILITY_GROUPS),
                    execution_mode=_enum_attr(item_node, "executionMode", EXECUTION_MODES),
                    state=_enum_attr(item_node, "state", ACTION_STATES),
                    view_id=_enum_attr(item_node, "viewId", VIEW_IDS),
                    intent=_enum_attr(item_node, "intent", INTENT_IDS),
                    summary=_required_visible_attr(item_node, "summary"),
                    bridge_action_id=bridge_action_id,
                    evidence_ref=_optional_id(item_node, "evidenceRef"),
                )
                if item_page != page_id or item_target != page_id:
                    raise RnwMenuGenerationError(f"item_page_mismatch:{item_id}")
                if item.capability_group != page.capability_group:
                    raise RnwMenuGenerationError(f"item_group_mismatch:{item_id}")
                items.append(item)
            if not items:
                raise RnwMenuGenerationError(f"section_empty:{section_id}")
            section = RnwMenuSection(
                section_id=section_id,
                label=_required_visible_attr(section_node, "label"),
                page_id=section_page,
                target_page=section_target,
                capability_group=_enum_attr(section_node, "capabilityGroup", CAPABILITY_GROUPS),
                execution_mode=_enum_attr(section_node, "executionMode", EXECUTION_MODES),
                state=_enum_attr(section_node, "state", ACTION_STATES),
                summary=_required_visible_attr(section_node, "summary"),
                evidence_ref=_optional_id(section_node, "evidenceRef"),
                items=tuple(items),
            )
            if section_page != page_id or section_target != page_id:
                raise RnwMenuGenerationError(f"section_page_mismatch:{section_id}")
            if section.capability_group != page.capability_group:
                raise RnwMenuGenerationError(f"section_group_mismatch:{section_id}")
            sections.append(section)
        if not sections:
            raise RnwMenuGenerationError(f"page_empty:{page_id}")
        pages.append(
            RnwMenuPage(
                page_id=page.page_id,
                label=page.label,
                target_page=page.target_page,
                capability_group=page.capability_group,
                execution_mode=page.execution_mode,
                state=page.state,
                view_id=page.view_id,
                evidence_ref=page.evidence_ref,
                sections=tuple(sections),
            )
        )

    if tuple(page.page_id for page in pages) != PAGE_ORDER:
        raise RnwMenuGenerationError("page_order_invalid")
    for page in pages:
        if page.target_page not in page_ids:
            raise RnwMenuGenerationError(f"page_target_unknown:{page.page_id}:{page.target_page}")
    if not KNOWN_ACTION_IDS.issubset(action_ids):
        missing = ",".join(sorted(KNOWN_ACTION_IDS - action_ids))
        raise RnwMenuGenerationError(f"action_missing:{missing}")

    return RnwMenu(schema=MENU_SCHEMA, app_id=APP_ID, menu_id=menu_id, label=label, pages=tuple(pages))


def generate_typescript(menu: RnwMenu, xml_path: Path = XML_PATH) -> str:
    payload = {
        "schema": menu.schema,
        "appId": menu.app_id,
        "menuId": menu.menu_id,
        "label": menu.label,
        "sourceXml": xml_path.name,
        "pages": [
            {
                "id": page.page_id,
                "label": page.label,
                "targetPage": page.target_page,
                "capabilityGroup": page.capability_group,
                "executionMode": page.execution_mode,
                "state": page.state,
                "viewId": page.view_id,
                "summary": page.sections[0].summary,
                "evidenceRef": page.evidence_ref,
                "sections": [
                    {
                        "id": section.section_id,
                        "label": section.label,
                        "pageId": section.page_id,
                        "targetPage": section.target_page,
                        "capabilityGroup": section.capability_group,
                        "executionMode": section.execution_mode,
                        "state": section.state,
                        "summary": section.summary,
                        "evidenceRef": section.evidence_ref,
                        "items": [
                            {
                                "id": item.item_id,
                                "actionId": item.action_id,
                                "label": item.label,
                                "pageId": item.page_id,
                                "targetPage": item.target_page,
                                "capabilityGroup": item.capability_group,
                                "executionMode": item.execution_mode,
                                "state": item.state,
                                "viewId": item.view_id,
                                "intent": item.intent,
                                "summary": item.summary,
                                **({"bridgeActionId": item.bridge_action_id} if item.bridge_action_id else {}),
                                "evidenceRef": item.evidence_ref,
                            }
                            for item in section.items
                        ],
                    }
                    for section in page.sections
                ],
            }
            for page in menu.pages
        ],
    }
    return (
        "// Generated RNW product menu model; do not edit.\n\n"
        f"export const CBBS_RNW_MENU_SCHEMA = {json.dumps(MENU_SCHEMA)} as const;\n"
        "export const hardwareToolsMenu = "
        + json.dumps(payload, indent=2, sort_keys=False)
        + " as const;\n"
    )


def write_generated(check: bool = False) -> int:
    menu = load_menu(XML_PATH)
    content = generate_typescript(menu, XML_PATH)
    current = TS_MODEL_PATH.read_text(encoding="utf-8") if TS_MODEL_PATH.exists() else ""
    if current == content:
        return 0
    if check:
        diff = difflib.unified_diff(
            current.splitlines(),
            content.splitlines(),
            fromfile=str(TS_MODEL_PATH),
            tofile=f"{TS_MODEL_PATH} (expected)",
            lineterm="",
        )
        print("\n".join(diff), file=sys.stderr)
        return 1
    TS_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    TS_MODEL_PATH.write_text(content, encoding="utf-8")
    return 0


def _reject_unsafe_xml(raw: str) -> None:
    upper = raw.upper()
    for marker in ("<!DOCTYPE", "<!ENTITY", "SYSTEM", "PUBLIC"):
        if marker in upper:
            raise RnwMenuGenerationError("xml_external_entity_rejected")
    if "<?" in raw:
        stripped = raw.lstrip()
        if not stripped.startswith("<?xml ") or "?>" not in stripped.splitlines()[0]:
            raise RnwMenuGenerationError("xml_processing_instruction_rejected")


def _require_tag(node: ElementTree.Element, expected: str) -> None:
    if node.tag not in ALLOWED_TAGS:
        raise RnwMenuGenerationError(f"tag_unknown:{node.tag}")
    if node.tag != expected:
        raise RnwMenuGenerationError(f"tag_invalid:{node.tag}:{expected}")


def _require_attrs(node: ElementTree.Element, allowed: Iterable[str], context: str) -> None:
    unknown = sorted(set(node.attrib) - set(allowed))
    if unknown:
        raise RnwMenuGenerationError(f"attribute_unknown:{context}:{','.join(unknown)}")
    for key, value in node.attrib.items():
        _reject_secret_name(key)
        _clean_text(value)


def _required_id(node: ElementTree.Element, attr: str) -> str:
    value = _required_text_attr(node, attr)
    if not ID_RE.match(value):
        raise RnwMenuGenerationError(f"id_invalid:{node.tag}.{attr}:{value}")
    return value


def _optional_id(node: ElementTree.Element, attr: str) -> str:
    value = node.attrib.get(attr, "")
    if value == "":
        return ""
    value = _clean_text(value)
    if not ID_RE.match(value):
        raise RnwMenuGenerationError(f"id_invalid:{node.tag}.{attr}:{value}")
    return value


def _required_action_id(node: ElementTree.Element, attr: str) -> str:
    value = _required_text_attr(node, attr)
    if not ACTION_ID_RE.match(value):
        raise RnwMenuGenerationError(f"action_id_invalid:{value}")
    return value


def _optional_action_id(node: ElementTree.Element, attr: str) -> str:
    value = node.attrib.get(attr, "")
    if value == "":
        return ""
    value = _clean_text(value)
    if not ACTION_ID_RE.match(value):
        raise RnwMenuGenerationError(f"action_id_invalid:{value}")
    return value


def _enum_attr(node: ElementTree.Element, attr: str, allowed: frozenset[str]) -> str:
    value = _required_text_attr(node, attr)
    if value not in allowed:
        raise RnwMenuGenerationError(f"enum_invalid:{node.tag}.{attr}:{value}")
    return value


def _required_visible_attr(node: ElementTree.Element, attr: str) -> str:
    value = _required_text_attr(node, attr)
    _validate_visible_text(value, f"{node.tag}.{attr}")
    return value


def _required_text_attr(node: ElementTree.Element, attr: str) -> str:
    value = node.attrib.get(attr)
    if value is None or value == "":
        raise RnwMenuGenerationError(f"attribute_required:{node.tag}.{attr}")
    return _clean_text(value)


def _clean_text(value: str) -> str:
    text = " ".join(value.split())
    if any(ord(char) < 32 or ord(char) >= 127 for char in text):
        raise RnwMenuGenerationError("text_non_ascii")
    return text


def _validate_visible_text(value: str, context: str) -> None:
    _reject_secret_name(context)
    _reject_secret_name(value)
    for pattern in FORBIDDEN_VISIBLE_PATTERNS:
        if pattern.search(value):
            raise RnwMenuGenerationError(f"visible_copy_forbidden:{context}:{value}")


def _reject_secret_name(value: str) -> None:
    normalized = value.lower().replace("_", "").replace("-", "").replace(" ", "")
    for marker in SECRET_MARKERS:
        if marker in normalized:
            raise RnwMenuGenerationError(f"secret_field_rejected:{value}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated TypeScript is stale")
    args = parser.parse_args(argv)
    try:
        return write_generated(check=args.check)
    except RnwMenuGenerationError as exc:
        print(f"rnw_menu_generation_failed:{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
