#!/usr/bin/env python3
"""Managed ESP32 Codex yolo-compatible lifecycle policy."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


HOOK_DIR = Path(__file__).resolve().parent
ROOT = Path(__file__).resolve().parents[3]
for import_dir in [ROOT / "scripts", HOOK_DIR]:
    if import_dir.exists():
        import_path = str(import_dir)
        if import_path in sys.path:
            sys.path.remove(import_path)
        sys.path.insert(0, import_path)

from agent_process_classifiers import (  # noqa: E402
    BYPASS_RE,
    FOOTER_PATTERNS,
    MUTATION_CLAIM_RE,
    REVIEWER_PATTERNS,
    ROUTING_PATTERNS,
    TIER3_AUTH_PATTERNS,
    footer_semantic_failure,
    has_open_p1_p2_findings,
    has_reject_vote,
    is_bypass_permission_mode,
    is_live_tier3_tool,
    is_mutating_tool,
    missing,
    stringify,
    visible_context,
)
from agent_process_contracts import BYPASS_ADVISORY, ROUTING_PACKET, SUBAGENT_BOUNDARY  # noqa: E402


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


def _handle_user_prompt(payload: dict[str, Any], shape_unknown: bool) -> int:
    message = ROUTING_PACKET
    if is_bypass_permission_mode(payload):
        _context("UserPromptSubmit", BYPASS_ADVISORY + "\n" + message)
        return 0
    prompt = stringify(payload.get("prompt"))
    if prompt and BYPASS_RE.search(prompt):
        _block("ESP32 managed-hook policy blocks attempts to bypass workspace governance or safety gates.")
        return 0
    if shape_unknown:
        message += "\nHook input shape was unknown; require explicit coordinator triage before mutation."
    _context("UserPromptSubmit", message)
    return 0


def _handle_pre_tool(payload: dict[str, Any], shape_unknown: bool) -> int:
    if is_bypass_permission_mode(payload):
        return 0
    if shape_unknown:
        _deny_pretool("ESP32 managed-hook policy denies mutating tool use when hook input is malformed.")
        return 0
    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input")
    if not is_mutating_tool(tool_name, tool_input) and not is_live_tier3_tool(tool_name, tool_input):
        return 0

    context = visible_context(payload)
    if is_live_tier3_tool(tool_name, tool_input):
        missing_auth = missing(TIER3_AUTH_PATTERNS, context)
        if missing_auth:
            _deny_pretool("ESP32 Tier 3 command denied; missing " + ", ".join(missing_auth) + ".")
            return 0
    missing_routing = missing(ROUTING_PATTERNS, context)
    if missing_routing:
        _deny_pretool(
            "ESP32 mutating tool call denied; missing routing packet fields: "
            + ", ".join(missing_routing)
            + "."
        )
    return 0


def _handle_permission(payload: dict[str, Any], shape_unknown: bool) -> int:
    if is_bypass_permission_mode(payload):
        return 0
    if shape_unknown:
        _deny_permission("ESP32 managed-hook policy denies approval with malformed hook input.")
        return 0
    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input")
    context = visible_context(payload)
    if is_live_tier3_tool(tool_name, tool_input):
        missing_auth = missing(TIER3_AUTH_PATTERNS, context)
        if missing_auth:
            _deny_permission("ESP32 Tier 3 approval denied; missing " + ", ".join(missing_auth) + ".")
            return 0
    if is_mutating_tool(tool_name, tool_input):
        missing_routing = missing(ROUTING_PATTERNS, context)
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
    if is_bypass_permission_mode(payload):
        return 0
    if shape_unknown:
        _block("Continue subagent: hook input was malformed, so reviewer output cannot be validated.")
        return 0
    message = stringify(payload.get("last_assistant_message"))
    missing_fields = missing(REVIEWER_PATTERNS, message)
    if missing_fields:
        _block("Continue subagent: reviewer output missing " + ", ".join(missing_fields) + ".")
        return 0
    if has_open_p1_p2_findings(message):
        _block("Continue subagent: reviewer output reports open P1/P2 findings.")
        return 0
    if has_reject_vote(message):
        _block("Continue subagent: reviewer output rejected or vetoed the gate.")
    return 0


def _handle_stop(payload: dict[str, Any], shape_unknown: bool) -> int:
    if is_bypass_permission_mode(payload):
        return 0
    if shape_unknown:
        _block("Continue turn: hook input was malformed, so final decision footer cannot be validated.")
        return 0
    message = stringify(payload.get("last_assistant_message"))
    if not MUTATION_CLAIM_RE.search(message):
        return 0
    missing_fields = missing(FOOTER_PATTERNS, message)
    if missing_fields:
        _block("Continue turn: non-trivial mutation summary missing decision footer fields: " + ", ".join(missing_fields) + ".")
        return 0
    semantic_failure = footer_semantic_failure(message)
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
