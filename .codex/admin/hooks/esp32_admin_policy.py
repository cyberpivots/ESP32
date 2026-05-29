#!/usr/bin/env python3
"""Managed ESP32 Codex yolo-compatible lifecycle policy."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROUTING_PACKET = """ESP32 yolo-compatible routing packet advisory before Tier 1+ mutation:
- Verified facts: state only facts verified from the current workspace, official docs, or same-session evidence.
- Assumptions: state any accepted assumptions separately.
- Unknowns: state unresolved gaps separately.
- Selected tier: Tier 0, Tier 1, Tier 2, or Tier 3.
- Owner role: name the responsible workspace role.
- Evidence need: local, official source, web, same-session bench, or physical.
- Mutation boundary: exact files, system paths, or no-mutation boundary.
- Validation plan: commands or evidence required before completion.
- Reviewer quorum: required for Tier 2 and Tier 3 before mutation.
- Weighted veto: coordinator/architecture-risk weight 5, high-reasoning specialist 3, medium specialist 2, low-risk helper 1; pass requires required roles, at least 70 percent weighted approval, and no P1/P2 blockers.
- Tier 3 remains closed unless explicit live-gate authority, same-session evidence, recovery path, reviewer quorum, and closed-surface review are present.
- Missing evidence is a continuation state when the next evidence step is automatable; ask the user only for one irreducible physical fact, and block only at a hard safety or authority boundary.
"""

SUBAGENT_BOUNDARY = """ESP32 yolo-compatible subagent boundary:
- Re-read AGENTS.md and required governance files before making claims.
- Stay read-only unless the parent prompt gives an explicit disjoint write scope.
- Keep verified facts, assumptions, and unknowns separate.
- Reviewer outputs must include role, evidence reviewed, P1/P2 findings, vote, conditions, and confidence.
- Reviewer outputs must preserve the weighted-vote model and must not mark a gate accepted while P1/P2 blockers remain.
- Do not run live hardware, flash, erase, monitor, serial-write, BLE, mesh, PCAP, relay, XBee write, TFT, MicroSD, load, wiring, mains, router/admin, or release-gate actions.
- Do not commit or push unless the user explicitly requested it and validation passed.
"""

ROUTING_PATTERNS = {
    "verified facts": re.compile(r"\bverified facts?\b", re.IGNORECASE),
    "assumptions": re.compile(r"\bassumptions?\b", re.IGNORECASE),
    "unknowns": re.compile(r"\bunknowns?\b", re.IGNORECASE),
    "selected tier": re.compile(r"\b(selected tier|Tier\s*[0-3])\b", re.IGNORECASE),
    "owner role": re.compile(r"\bowner role\b", re.IGNORECASE),
    "evidence need": re.compile(r"\bevidence need\b", re.IGNORECASE),
    "mutation boundary": re.compile(r"\b(mutation boundary|write scope|no-mutation boundary)\b", re.IGNORECASE),
    "validation plan": re.compile(r"\bvalidation plan\b", re.IGNORECASE),
}
TIER3_AUTH_PATTERNS = {
    "explicit Tier 3 gate authority": re.compile(r"\b(explicit .*gate authority|live-gate authority)\b", re.IGNORECASE),
    "same-session evidence": re.compile(r"\bsame-session evidence\b", re.IGNORECASE),
    "recovery path": re.compile(r"\brecovery path\b", re.IGNORECASE),
    "reviewer quorum": re.compile(r"\breviewer quorum\b", re.IGNORECASE),
    "closed-surface review": re.compile(r"\bclosed-surface review\b", re.IGNORECASE),
}
REVIEWER_PATTERNS = {
    "role": re.compile(r"\brole\b", re.IGNORECASE),
    "evidence reviewed": re.compile(r"\bevidence reviewed\b", re.IGNORECASE),
    "P1/P2 findings": re.compile(r"\bP1/P2 findings\b|\bP1\b.*\bP2\b", re.IGNORECASE | re.DOTALL),
    "vote": re.compile(r"\bvote\b", re.IGNORECASE),
    "conditions": re.compile(r"\bconditions\b", re.IGNORECASE),
    "confidence": re.compile(r"\bconfidence\b", re.IGNORECASE),
}
FOOTER_PATTERNS = {
    "decision": re.compile(r"\bdecision\s*:", re.IGNORECASE),
    "next gate": re.compile(r"\bnext (gate|slice)\s*:", re.IGNORECASE),
    "owner role": re.compile(r"\bowner role\s*:", re.IGNORECASE),
    "evidence": re.compile(r"\bevidence\s*:", re.IGNORECASE),
    "validation": re.compile(r"\bvalidation\s*:", re.IGNORECASE),
    "durable records": re.compile(r"\bdurable records\s*:", re.IGNORECASE),
    "authority limits": re.compile(r"\bauthority limits\s*:", re.IGNORECASE),
}
FIELD_PATTERNS = {
    "decision": re.compile(r"^\s*decision\s*:\s*(.*)$", re.IGNORECASE | re.MULTILINE),
    "validation": re.compile(r"^\s*validation\s*:\s*(.*)$", re.IGNORECASE | re.MULTILINE),
    "durable records": re.compile(r"^\s*durable records\s*:\s*(.*)$", re.IGNORECASE | re.MULTILINE),
    "P1/P2 findings": re.compile(r"^\s*P1/P2 findings\s*:\s*(.*)$", re.IGNORECASE | re.MULTILINE),
    "vote": re.compile(r"^\s*vote\s*:\s*(.*)$", re.IGNORECASE | re.MULTILINE),
}
NON_TERMINAL_DECISIONS = {"continue", "ready_for_mutation"}
TERMINAL_DECISIONS = {"ask_user", "blocked", "handoff", "complete"}
PENDING_OR_MISSING_RE = re.compile(r"\b(pending|missing|not run|not performed|todo|tbd)\b", re.IGNORECASE)
NO_BLOCKERS_RE = re.compile(r"\b(none|no p1/p2|no blockers|no p1|no p2|n/a|na)\b", re.IGNORECASE)
BYPASS_RE = re.compile(
    r"\b(ignore|bypass|disable|skip|override)\b.{0,80}\b(AGENTS\.md|governance|hook|requirements|reviewer quorum|Tier 3|safety gate)\b",
    re.IGNORECASE | re.DOTALL,
)
MUTATING_SHELL_RE = re.compile(
    r"(^|\s)(apply_patch|rm|mv|cp|touch|mkdir|chmod|chown|truncate|dd|tee|"
    r"git\s+(add|commit|push|merge|rebase|reset|checkout|switch|branch\s+-D|clean)|"
    r"sed\s+-i|find\s+.*\s-delete|install\s+|"
    r"python3?\s+.*(write|update|generate|build|package|install|deploy|flash))\b|"
    r"(>>|>\s*[^&]|\|\s*tee\b)",
    re.IGNORECASE | re.DOTALL,
)
READ_ONLY_SHELL_RE = re.compile(
    r"^\s*(pwd|ls|find|rg|sed|cat|nl|wc|git\s+(status|diff|show|log)|"
    r"python3?\s+-m\s+json\.tool|python3?\s+scripts/(verify|scaffold_audit)[\w_./-]*\.py)\b",
    re.IGNORECASE,
)
MUTATING_MCP_RE = re.compile(
    r"(write|edit|delete|remove|create|update|patch|apply|commit|push|merge|"
    r"flash|erase|deploy|upload)",
    re.IGNORECASE,
)
LIVE_TIER3_COMMAND_RE = re.compile(
    r"\b(esptool|idf\.py\s+(-p|flash|erase|monitor)|flash|erase|monitor|"
    r"serial[-_ ]?write|minicom|picocom|screen\s+/dev/|ble|bluetooth|"
    r"esp[-_]?wifi[-_]?mesh|mesh|pcap|tcpdump|wireshark|relay|xbee|tft|"
    r"microsd|micro[-_ ]?sd|load|wiring|mains|router admin|router-admin)\b",
    re.IGNORECASE,
)
LIVE_TIER3_TOOL_RE = re.compile(
    r"(flash|erase|monitor|serial|ble|mesh|pcap|relay|xbee|tft|microsd|load|wiring|mains)",
    re.IGNORECASE,
)
MUTATION_CLAIM_RE = re.compile(
    r"\b(implemented|updated|changed|created|installed|wrote|modified|validated|ran tests|patched)\b",
    re.IGNORECASE,
)
BYPASS_PERMISSION_MODE = "bypassPermissions"
BYPASS_ADVISORY = (
    "ESP32 operator sovereignty: permission_mode=bypassPermissions was detected. "
    "Hooks must not deny, block, or override the user-intended --yolo full-access launch."
)


def _load_payload() -> tuple[dict[str, Any], bool]:
    try:
        raw = json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}, True
    if not isinstance(raw, dict):
        return {}, True
    return raw, False


def _json(data: dict[str, Any]) -> None:
    print(json.dumps(data, separators=(",", ":")))


def _context(event: str, message: str) -> None:
    _json({"hookSpecificOutput": {"hookEventName": event, "additionalContext": message}})


def _block(reason: str) -> None:
    _json({"decision": "block", "reason": reason})


def _deny_pretool(reason: str) -> None:
    _json({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    })


def _deny_permission(reason: str) -> None:
    _json({
        "hookSpecificOutput": {
            "hookEventName": "PermissionRequest",
            "decision": {"behavior": "deny", "message": reason},
        }
    })


def _is_yolo(payload: dict[str, Any]) -> bool:
    return payload.get("permission_mode") == BYPASS_PERMISSION_MODE


def _extract_command(tool_input: Any) -> str:
    if isinstance(tool_input, dict):
        for key in ("command", "cmd"):
            value = tool_input.get(key)
            if isinstance(value, str):
                return value
    if isinstance(tool_input, str):
        return tool_input
    return ""


def _stringify(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts: list[str] = []
        for item in value:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text") or item.get("content")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(parts)
    if isinstance(value, dict):
        text = value.get("text") or value.get("content")
        if isinstance(text, str):
            return text
    return ""


def _latest_text_from_transcript(path: str | None, role: str | None = None) -> str:
    if not path:
        return ""
    transcript = Path(path)
    if not transcript.exists() or not transcript.is_file():
        return ""
    try:
        lines = transcript.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""
    for line in reversed(lines[-500:]):
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        text = _text_from_item(item, role)
        if text:
            return text
    return ""


def _text_from_item(item: Any, role: str | None = None) -> str:
    if not isinstance(item, dict):
        return ""
    candidates: list[Any] = []
    if role is None:
        candidates.extend([item.get("prompt"), item.get("user_prompt"), item.get("content")])
    elif item.get("role") == role:
        candidates.append(item.get("content"))
    payload = item.get("payload")
    if isinstance(payload, dict):
        if role is None or payload.get("role") == role:
            candidates.extend([payload.get("prompt"), payload.get("text"), payload.get("content")])
    for candidate in candidates:
        text = _stringify(candidate)
        if text:
            return text
    return ""


def _visible_context(payload: dict[str, Any]) -> str:
    pieces = [
        _stringify(payload.get("prompt")),
        _stringify(payload.get("last_assistant_message")),
        _latest_text_from_transcript(payload.get("transcript_path")),
    ]
    return "\n".join(piece for piece in pieces if piece)


def _missing(patterns: dict[str, re.Pattern[str]], text: str) -> list[str]:
    return [name for name, pattern in patterns.items() if not pattern.search(text)]


def _field_value(text: str, name: str) -> str:
    pattern = FIELD_PATTERNS[name]
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def _open_p1_p2_findings(text: str) -> bool:
    value = _field_value(text, "P1/P2 findings")
    if not value:
        return False
    if NO_BLOCKERS_RE.search(value):
        return False
    return True


def _reject_vote(text: str) -> bool:
    value = _field_value(text, "vote").lower()
    return "reject" in value or "veto" in value


def _footer_semantic_failure(message: str) -> str | None:
    decision = _field_value(message, "decision").lower()
    if decision in NON_TERMINAL_DECISIONS:
        return f"decision {decision!r} is not terminal; continue the turn."
    if decision and decision not in TERMINAL_DECISIONS:
        return f"decision {decision!r} is not a recognized final decision."

    validation = _field_value(message, "validation")
    if PENDING_OR_MISSING_RE.search(validation):
        return "validation is pending or missing."

    durable_records = _field_value(message, "durable records")
    if PENDING_OR_MISSING_RE.search(durable_records) or durable_records.lower() in {"none", "n/a", "na"}:
        return "durable records are pending or missing."
    return None


def _is_mutating(tool_name: str, tool_input: Any) -> bool:
    normalized = tool_name.lower()
    if normalized in {"apply_patch", "edit", "write"}:
        return True
    command = _extract_command(tool_input)
    if normalized in {"bash", "shell", "functions.exec_command"}:
        if READ_ONLY_SHELL_RE.search(command) and not MUTATING_SHELL_RE.search(command):
            return False
        return bool(MUTATING_SHELL_RE.search(command))
    if normalized.startswith("mcp__"):
        return bool(MUTATING_MCP_RE.search(tool_name))
    return False


def _is_live_tier3(tool_name: str, tool_input: Any) -> bool:
    return bool(LIVE_TIER3_TOOL_RE.search(tool_name) or LIVE_TIER3_COMMAND_RE.search(_extract_command(tool_input)))


def _handle_user_prompt(payload: dict[str, Any], shape_unknown: bool) -> int:
    if _is_yolo(payload):
        _context("UserPromptSubmit", BYPASS_ADVISORY + "\n" + ROUTING_PACKET)
        return 0
    prompt = _stringify(payload.get("prompt"))
    if prompt and BYPASS_RE.search(prompt):
        _block("ESP32 managed-hook policy blocks attempts to bypass workspace governance or safety gates.")
        return 0
    message = ROUTING_PACKET
    if shape_unknown:
        message += "\nHook input shape was unknown; require explicit coordinator triage before mutation."
    _context("UserPromptSubmit", message)
    return 0


def _handle_pre_tool(payload: dict[str, Any], shape_unknown: bool) -> int:
    if _is_yolo(payload):
        return 0
    if shape_unknown:
        _deny_pretool("ESP32 managed-hook policy denies mutating tool use when hook input is malformed.")
        return 0
    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input")
    if not _is_mutating(tool_name, tool_input) and not _is_live_tier3(tool_name, tool_input):
        return 0
    context = _visible_context(payload)
    if _is_live_tier3(tool_name, tool_input):
        missing_auth = _missing(TIER3_AUTH_PATTERNS, context)
        if missing_auth:
            _deny_pretool(
                "ESP32 Tier 3 command denied; missing "
                + ", ".join(missing_auth)
                + "."
            )
            return 0
    missing_routing = _missing(ROUTING_PATTERNS, context)
    if missing_routing:
        _deny_pretool(
            "ESP32 mutating tool call denied; missing routing packet fields: "
            + ", ".join(missing_routing)
            + "."
        )
    return 0


def _handle_permission(payload: dict[str, Any], shape_unknown: bool) -> int:
    if _is_yolo(payload):
        return 0
    if shape_unknown:
        _deny_permission("ESP32 managed-hook policy denies approval with malformed hook input.")
        return 0
    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input")
    context = _visible_context(payload)
    if _is_live_tier3(tool_name, tool_input):
        missing_auth = _missing(TIER3_AUTH_PATTERNS, context)
        if missing_auth:
            _deny_permission(
                "ESP32 Tier 3 approval denied; missing "
                + ", ".join(missing_auth)
                + "."
            )
            return 0
    if _is_mutating(tool_name, tool_input):
        missing_routing = _missing(ROUTING_PATTERNS, context)
        if missing_routing:
            _deny_permission(
                "ESP32 approval denied; missing routing packet fields: "
                + ", ".join(missing_routing)
                + "."
            )
    return 0


def _handle_subagent_start(payload: dict[str, Any], shape_unknown: bool) -> int:
    message = SUBAGENT_BOUNDARY
    if shape_unknown:
        message += "\nHook input shape was unknown; require explicit coordinator triage before mutation."
    _context("SubagentStart", message)
    return 0


def _handle_subagent_stop(payload: dict[str, Any], shape_unknown: bool) -> int:
    if _is_yolo(payload):
        return 0
    if shape_unknown:
        _block("Continue subagent: hook input was malformed, so reviewer output cannot be validated.")
        return 0
    message = _stringify(payload.get("last_assistant_message"))
    missing = _missing(REVIEWER_PATTERNS, message)
    if missing:
        _block("Continue subagent: reviewer output missing " + ", ".join(missing) + ".")
        return 0
    if _open_p1_p2_findings(message):
        _block("Continue subagent: reviewer output reports open P1/P2 findings.")
        return 0
    if _reject_vote(message):
        _block("Continue subagent: reviewer output rejected or vetoed the gate.")
    return 0


def _handle_stop(payload: dict[str, Any], shape_unknown: bool) -> int:
    if _is_yolo(payload):
        return 0
    if shape_unknown:
        _block("Continue turn: hook input was malformed, so final decision footer cannot be validated.")
        return 0
    message = _stringify(payload.get("last_assistant_message"))
    if not MUTATION_CLAIM_RE.search(message):
        return 0
    missing = _missing(FOOTER_PATTERNS, message)
    if missing:
        _block("Continue turn: non-trivial mutation summary missing decision footer fields: " + ", ".join(missing) + ".")
        return 0
    semantic_failure = _footer_semantic_failure(message)
    if semantic_failure:
        _block("Continue turn: " + semantic_failure)
    return 0


def main() -> int:
    payload, shape_unknown = _load_payload()
    event = str(payload.get("hook_event_name") or "")
    if not event and shape_unknown:
        event = "UserPromptSubmit"

    handlers = {
        "UserPromptSubmit": _handle_user_prompt,
        "PreToolUse": _handle_pre_tool,
        "PermissionRequest": _handle_permission,
        "SubagentStart": _handle_subagent_start,
        "SubagentStop": _handle_subagent_stop,
        "Stop": _handle_stop,
    }
    handler = handlers.get(event)
    if handler is None:
        return 0
    return handler(payload, shape_unknown)


if __name__ == "__main__":
    raise SystemExit(main())
