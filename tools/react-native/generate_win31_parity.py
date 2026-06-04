#!/usr/bin/env python3
"""Generate CBBS RNW Win31 parity data from a source-backed XML contract."""

from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[2]
TOOL_DIR = Path(__file__).resolve().parent
XML_PATH = TOOL_DIR / "cbbs_rnw_win31_parity.v1.xml"
TS_MODEL_PATH = ROOT / "packages/cbbs-product/src/win31Parity.generated.ts"
DEFAULT_DOSC_ROOT = Path(os.environ.get("DOSC_ROOT", "/mnt/h/dos-c"))

PARITY_SCHEMA = "cbbs_rnw_win31_parity.v1"
PAGE_ORDER = (
    "status",
    "messages",
    "files",
    "devices",
    "help",
    "peers",
    "link",
    "updates",
    "setup",
    "diagnostics",
    "locks",
)
MENU_ORDER = ("session", "views", "messages", "files", "devices", "style", "help")
REQUEST_NAMES = (
    "hello",
    "state_get",
    "peer_list",
    "msg_pull",
    "msg_search",
    "msg_post",
    "msg_ack",
    "diag_get",
    "fw_inventory",
    "coordinator_state",
    "maint_intent",
    "download_list",
    "download_queue",
    "download_status",
    "discovery_snapshot",
    "discovery_events",
    "service_catalog",
    "capability_report",
    "otap_status",
    "otap_intent",
)
VIEW_IDS = frozenset({"home", "messages", "downloads", "peers", "network", "diagnostics", "safety", "config", "evidence"})
INTENT_IDS = frozenset({"refresh", "filter", "open_detail", "compose_draft", "queue_file_request", "ack_local", "view_proof"})
EXECUTION_MODES = frozenset({"localOnly", "artifactReview", "bridgePreviewUnavailable", "tier3Closed"})
ACTION_STATES = frozenset({"ready", "needsDevice", "needsSafetyCheck", "needsConfirmation", "running", "complete", "failed", "unavailable"})
COVERAGE_DISPOSITIONS = frozenset({"represented", "evidenceOnly", "notRenderedRoleBoundary"})
ROLE_IDS = frozenset({"client", "sysop"})

ALLOWED_TAGS = frozenset({
    "parity",
    "sources",
    "sourceRef",
    "marker",
    "status",
    "menus",
    "menu",
    "pages",
    "page",
    "actions",
    "action",
    "requests",
    "request",
    "roleCoverage",
    "coverage",
    "hardwareAdjacency",
    "surface",
})

ID_RE = re.compile(r"^[a-z][a-z0-9-]{1,63}$")
ACTION_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:\.[a-z][A-Za-z0-9]*)+$")
SOURCE_PATH_RE = re.compile(r"^[a-zA-Z0-9_./-]+$")
FORBIDDEN_VISIBLE_PATTERNS = (
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
    re.compile(r"\berase\b", re.IGNORECASE),
    re.compile(r"\bmonitor\b", re.IGNORECASE),
    re.compile(r"\brelay\b", re.IGNORECASE),
    re.compile(r"\bmains\b", re.IGNORECASE),
    re.compile(r"\bload\b", re.IGNORECASE),
    re.compile(r"\bshell\b", re.IGNORECASE),
    re.compile(r"\bexec\b", re.IGNORECASE),
    re.compile(r"\bPowerShell\b", re.IGNORECASE),
    re.compile(r"\bpackage\b", re.IGNORECASE),
    re.compile(r"\bsigning?\b", re.IGNORECASE),
    re.compile(r"\brelease\b", re.IGNORECASE),
    re.compile(r"\bdeploy\b", re.IGNORECASE),
)


class Win31ParityGenerationError(ValueError):
    """Raised when the Win31 parity contract fails closed."""


@dataclass(frozen=True)
class SourceRef:
    ref_id: str
    path: str
    markers: tuple[str, ...]


def load_contract(xml_path: Path = XML_PATH, dosc_root: Path = DEFAULT_DOSC_ROOT) -> dict[str, object]:
    raw = xml_path.read_text(encoding="utf-8")
    _reject_unsafe_xml(raw)
    try:
        root = ElementTree.fromstring(raw)
    except ElementTree.ParseError as exc:
        raise Win31ParityGenerationError(f"xml_parse_error:{exc}") from exc

    _require_tag(root, "parity")
    _require_attrs(root, {"schema", "visiblePlatform", "moduleName", "internalEvidenceRef"}, "parity")
    if root.attrib.get("schema") != PARITY_SCHEMA:
        raise Win31ParityGenerationError("schema_invalid")
    visible_platform = _required_visible_attr(root, "visiblePlatform")
    module_name = _required_visible_attr(root, "moduleName")
    internal_ref = _required_text_attr(root, "internalEvidenceRef")

    source_refs = _load_sources(_require_child(root, "sources"))
    _verify_source_refs(source_refs, dosc_root)
    source_ref_ids = {entry.ref_id for entry in source_refs}

    status = _load_status(_require_child(root, "status"), source_ref_ids)
    menus = _load_menus(_require_child(root, "menus"), source_ref_ids)
    pages = _load_pages(_require_child(root, "pages"), source_ref_ids)
    page_ids = {str(page["id"]) for page in pages}
    requests = _load_requests(_require_child(root, "requests"), source_ref_ids)
    actions = _load_actions(_require_child(root, "actions"), source_ref_ids, page_ids, set(requests))
    role_coverage = _load_role_coverage(root, source_ref_ids, page_ids)
    hardware_adjacency = _load_hardware_adjacency(_require_child(root, "hardwareAdjacency"), source_ref_ids, page_ids)

    return {
        "schema": PARITY_SCHEMA,
        "visiblePlatform": visible_platform,
        "moduleName": module_name,
        "internalEvidenceRef": internal_ref,
        "sourceXml": xml_path.name,
        "doscSourceRoot": str(dosc_root),
        "sourceRefs": [entry.__dict__ for entry in source_refs],
        "status": status,
        "menus": menus,
        "pages": pages,
        "actions": actions,
        "requestNames": requests,
        "roleCoverage": role_coverage,
        "hardwareAdjacency": hardware_adjacency,
    }


def generate_typescript(contract: dict[str, object]) -> str:
    return (
        "// Generated RNW Win31 parity model; do not edit.\n\n"
        f"export const CBBS_RNW_WIN31_PARITY_SCHEMA = {json.dumps(PARITY_SCHEMA)} as const;\n"
        "export const win31ParityContract = "
        + json.dumps(contract, indent=2, sort_keys=False)
        + " as const;\n"
    )


def write_generated(check: bool = False, dosc_root: Path = DEFAULT_DOSC_ROOT) -> int:
    contract = load_contract(XML_PATH, dosc_root)
    content = generate_typescript(contract)
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


def _load_sources(node: ElementTree.Element) -> tuple[SourceRef, ...]:
    _require_tag(node, "sources")
    refs: list[SourceRef] = []
    seen: set[str] = set()
    for source in node:
        _require_tag(source, "sourceRef")
        _require_attrs(source, {"id", "path"}, "sourceRef")
        ref_id = _required_id(source, "id")
        if ref_id in seen:
            raise Win31ParityGenerationError(f"duplicate_source_ref:{ref_id}")
        seen.add(ref_id)
        path = _required_text_attr(source, "path")
        if not SOURCE_PATH_RE.match(path) or ".." in Path(path).parts:
            raise Win31ParityGenerationError(f"source_path_invalid:{path}")
        markers: list[str] = []
        for marker in source:
            _require_tag(marker, "marker")
            _require_attrs(marker, set(), "marker")
            text = (marker.text or "").strip()
            if not text:
                raise Win31ParityGenerationError(f"source_marker_empty:{ref_id}")
            markers.append(_clean_text(text, visible=False))
        if not markers:
            raise Win31ParityGenerationError(f"source_markers_missing:{ref_id}")
        refs.append(SourceRef(ref_id=ref_id, path=path, markers=tuple(markers)))
    return tuple(refs)


def _verify_source_refs(source_refs: tuple[SourceRef, ...], dosc_root: Path) -> None:
    for source_ref in source_refs:
        path = dosc_root / source_ref.path
        if not path.exists():
            raise Win31ParityGenerationError(f"source_ref_missing:{source_ref.ref_id}:{source_ref.path}")
        text = path.read_text(encoding="utf-8", errors="replace")
        for marker in source_ref.markers:
            if marker not in text:
                raise Win31ParityGenerationError(f"source_marker_missing:{source_ref.ref_id}:{marker}")


def _load_status(node: ElementTree.Element, source_ref_ids: set[str]) -> dict[str, object]:
    _require_tag(node, "status")
    _require_attrs(node, {"sourceRef", "label", "counters"}, "status")
    _known_source_ref(node, source_ref_ids)
    label = _required_visible_attr(node, "label")
    counters = tuple(_validate_visible_text(part.strip(), "status.counters") for part in _required_text_attr(node, "counters").split("|"))
    if counters != ("In 0", "Out 0 Err 0", "Queue 0"):
        raise Win31ParityGenerationError("status_counters_invalid")
    return {"label": label, "counters": list(counters)}


def _load_menus(node: ElementTree.Element, source_ref_ids: set[str]) -> list[dict[str, str]]:
    _require_tag(node, "menus")
    _require_attrs(node, {"sourceRef"}, "menus")
    _known_source_ref(node, source_ref_ids)
    menus: list[dict[str, str]] = []
    seen: set[str] = set()
    for menu in node:
        _require_tag(menu, "menu")
        _require_attrs(menu, {"menuId", "label"}, "menu")
        menu_id = _required_id(menu, "menuId")
        if menu_id in seen:
            raise Win31ParityGenerationError(f"duplicate_menu_id:{menu_id}")
        seen.add(menu_id)
        menus.append({"id": menu_id, "label": _required_visible_attr(menu, "label")})
    if tuple(menu["id"] for menu in menus) != MENU_ORDER:
        raise Win31ParityGenerationError("menu_order_invalid")
    return menus


def _load_pages(node: ElementTree.Element, source_ref_ids: set[str]) -> list[dict[str, str]]:
    _require_tag(node, "pages")
    _require_attrs(node, {"sourceRef"}, "pages")
    _known_source_ref(node, source_ref_ids)
    pages: list[dict[str, str]] = []
    seen: set[str] = set()
    for page in node:
        _require_tag(page, "page")
        _require_attrs(page, {"pageId", "label", "viewId", "summary"}, "page")
        page_id = _required_id(page, "pageId")
        if page_id in seen:
            raise Win31ParityGenerationError(f"duplicate_page_id:{page_id}")
        seen.add(page_id)
        pages.append({
            "id": page_id,
            "label": _required_visible_attr(page, "label"),
            "viewId": _enum_attr(page, "viewId", VIEW_IDS),
            "summary": _required_visible_attr(page, "summary"),
        })
    if tuple(page["id"] for page in pages) != PAGE_ORDER:
        raise Win31ParityGenerationError("page_order_invalid")
    return pages


def _load_actions(
    node: ElementTree.Element,
    source_ref_ids: set[str],
    page_ids: set[str],
    request_names: set[str],
) -> list[dict[str, str]]:
    _require_tag(node, "actions")
    _require_attrs(node, {"sourceRef"}, "actions")
    _known_source_ref(node, source_ref_ids)
    actions: list[dict[str, str]] = []
    seen: set[str] = set()
    for action in node:
        _require_tag(action, "action")
        _require_attrs(
            action,
            {"actionId", "label", "menuId", "pageId", "viewId", "intent", "executionMode", "state", "summary", "requestName"},
            "action",
        )
        action_id = _required_action_id(action, "actionId")
        if action_id in seen:
            raise Win31ParityGenerationError(f"duplicate_action_id:{action_id}")
        seen.add(action_id)
        menu_id = _required_id(action, "menuId")
        page_id = _required_id(action, "pageId")
        request_name = _required_text_attr(action, "requestName")
        if menu_id not in MENU_ORDER:
            raise Win31ParityGenerationError(f"action_menu_unknown:{action_id}:{menu_id}")
        if page_id not in page_ids:
            raise Win31ParityGenerationError(f"action_page_unknown:{action_id}:{page_id}")
        if request_name not in request_names:
            raise Win31ParityGenerationError(f"action_request_unknown:{action_id}:{request_name}")
        actions.append({
            "id": action_id,
            "label": _required_visible_attr(action, "label"),
            "menuId": menu_id,
            "pageId": page_id,
            "viewId": _enum_attr(action, "viewId", VIEW_IDS),
            "intent": _enum_attr(action, "intent", INTENT_IDS),
            "executionMode": _enum_attr(action, "executionMode", EXECUTION_MODES),
            "state": _enum_attr(action, "state", ACTION_STATES),
            "summary": _required_visible_attr(action, "summary"),
            "requestName": request_name,
        })
    return actions


def _load_requests(node: ElementTree.Element, source_ref_ids: set[str]) -> list[str]:
    _require_tag(node, "requests")
    _require_attrs(node, {"sourceRef"}, "requests")
    _known_source_ref(node, source_ref_ids)
    requests: list[str] = []
    seen: set[str] = set()
    for request in node:
        _require_tag(request, "request")
        _require_attrs(request, {"name"}, "request")
        name = _required_text_attr(request, "name")
        if name in seen:
            raise Win31ParityGenerationError(f"duplicate_request_name:{name}")
        if name not in REQUEST_NAMES:
            raise Win31ParityGenerationError(f"request_name_unknown:{name}")
        seen.add(name)
        requests.append(name)
    if tuple(requests) != REQUEST_NAMES:
        raise Win31ParityGenerationError("request_order_invalid")
    return requests


def _load_role_coverage(
    root: ElementTree.Element,
    source_ref_ids: set[str],
    page_ids: set[str],
) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {}
    for node in root.findall("roleCoverage"):
        _require_tag(node, "roleCoverage")
        _require_attrs(node, {"role", "sourceRef"}, "roleCoverage")
        _known_source_ref(node, source_ref_ids)
        role = _enum_attr(node, "role", ROLE_IDS)
        if role in result:
            raise Win31ParityGenerationError(f"duplicate_role_coverage:{role}")
        coverage_rows: list[dict[str, str]] = []
        seen_pages: set[str] = set()
        for coverage in node:
            _require_tag(coverage, "coverage")
            _require_attrs(coverage, {"pageId", "disposition", "reason"}, "coverage")
            page_id = _required_id(coverage, "pageId")
            if page_id not in page_ids:
                raise Win31ParityGenerationError(f"coverage_page_unknown:{role}:{page_id}")
            if page_id in seen_pages:
                raise Win31ParityGenerationError(f"duplicate_coverage:{role}:{page_id}")
            seen_pages.add(page_id)
            coverage_rows.append({
                "pageId": page_id,
                "disposition": _enum_attr(coverage, "disposition", COVERAGE_DISPOSITIONS),
                "reason": _required_visible_attr(coverage, "reason"),
            })
        if seen_pages != page_ids:
            raise Win31ParityGenerationError(f"coverage_incomplete:{role}")
        result[role] = coverage_rows
    if set(result) != ROLE_IDS:
        raise Win31ParityGenerationError("role_coverage_incomplete")
    return result


def _load_hardware_adjacency(
    node: ElementTree.Element,
    source_ref_ids: set[str],
    page_ids: set[str],
) -> list[dict[str, str]]:
    _require_tag(node, "hardwareAdjacency")
    _require_attrs(node, {"sourceRef"}, "hardwareAdjacency")
    _known_source_ref(node, source_ref_ids)
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for surface in node:
        _require_tag(surface, "surface")
        _require_attrs(surface, {"pageId", "adjacentTo", "reason"}, "surface")
        page_id = _required_id(surface, "pageId")
        adjacent_to = _required_id(surface, "adjacentTo")
        if page_id in seen:
            raise Win31ParityGenerationError(f"duplicate_hardware_surface:{page_id}")
        if adjacent_to not in page_ids:
            raise Win31ParityGenerationError(f"hardware_adjacent_page_unknown:{page_id}:{adjacent_to}")
        seen.add(page_id)
        rows.append({
            "pageId": page_id,
            "adjacentTo": adjacent_to,
            "reason": _required_visible_attr(surface, "reason"),
        })
    if seen != {"bench", "radio", "mesh", "firmware", "fabrication", "safety", "activity"}:
        raise Win31ParityGenerationError("hardware_adjacency_incomplete")
    return rows


def _reject_unsafe_xml(raw: str) -> None:
    upper = raw.upper()
    for marker in ("<!DOCTYPE", "<!ENTITY", "SYSTEM", "PUBLIC"):
        if marker in upper:
            raise Win31ParityGenerationError("xml_external_entity_rejected")


def _require_child(node: ElementTree.Element, tag: str) -> ElementTree.Element:
    matches = [child for child in node if child.tag == tag]
    if len(matches) != 1:
        raise Win31ParityGenerationError(f"child_required:{node.tag}:{tag}:{len(matches)}")
    return matches[0]


def _require_tag(node: ElementTree.Element, expected: str) -> None:
    if node.tag not in ALLOWED_TAGS:
        raise Win31ParityGenerationError(f"tag_unknown:{node.tag}")
    if node.tag != expected:
        raise Win31ParityGenerationError(f"tag_invalid:{node.tag}:{expected}")


def _require_attrs(node: ElementTree.Element, allowed: Iterable[str], context: str) -> None:
    unknown = sorted(set(node.attrib) - set(allowed))
    if unknown:
        raise Win31ParityGenerationError(f"attribute_unknown:{context}:{','.join(unknown)}")


def _known_source_ref(node: ElementTree.Element, source_ref_ids: set[str]) -> None:
    source_ref = _required_id(node, "sourceRef")
    if source_ref not in source_ref_ids:
        raise Win31ParityGenerationError(f"source_ref_unknown:{node.tag}:{source_ref}")


def _required_id(node: ElementTree.Element, attr: str) -> str:
    value = _required_text_attr(node, attr)
    if not ID_RE.match(value):
        raise Win31ParityGenerationError(f"id_invalid:{node.tag}.{attr}:{value}")
    return value


def _required_action_id(node: ElementTree.Element, attr: str) -> str:
    value = _required_text_attr(node, attr)
    if not ACTION_ID_RE.match(value):
        raise Win31ParityGenerationError(f"action_id_invalid:{value}")
    return value


def _enum_attr(node: ElementTree.Element, attr: str, allowed: frozenset[str]) -> str:
    value = _required_text_attr(node, attr)
    if value not in allowed:
        raise Win31ParityGenerationError(f"enum_invalid:{node.tag}.{attr}:{value}")
    return value


def _required_visible_attr(node: ElementTree.Element, attr: str) -> str:
    return _validate_visible_text(_required_text_attr(node, attr), f"{node.tag}.{attr}")


def _required_text_attr(node: ElementTree.Element, attr: str) -> str:
    value = node.attrib.get(attr)
    if value is None or value == "":
        raise Win31ParityGenerationError(f"attribute_required:{node.tag}.{attr}")
    return _clean_text(value, visible=False)


def _clean_text(value: str, *, visible: bool) -> str:
    text = " ".join(value.split())
    if any(ord(char) < 32 or ord(char) >= 127 for char in text):
        raise Win31ParityGenerationError("text_non_ascii")
    if visible:
        _validate_visible_text(text, "text")
    return text


def _validate_visible_text(value: str, context: str) -> str:
    text = _clean_text(value, visible=False)
    for pattern in FORBIDDEN_VISIBLE_PATTERNS:
        if pattern.search(text):
            raise Win31ParityGenerationError(f"visible_copy_forbidden:{context}:{text}")
    return text


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated TypeScript is stale")
    parser.add_argument("--dosc-root", default=str(DEFAULT_DOSC_ROOT), help="path to the local DOS-C checkout")
    args = parser.parse_args(argv)
    try:
        return write_generated(check=args.check, dosc_root=Path(args.dosc_root))
    except Win31ParityGenerationError as exc:
        print(f"win31_parity_generation_failed:{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
