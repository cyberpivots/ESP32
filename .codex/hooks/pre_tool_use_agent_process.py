#!/usr/bin/env python3
"""Warn on mutating tool calls when the triage packet is not visible."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


MUTATING_SHELL_RE = re.compile(
    r"(^|\s)(apply_patch|rm|mv|cp|touch|mkdir|chmod|chown|truncate|dd|tee|"
    r"git\s+(add|commit|push|merge|rebase|reset|checkout|switch|branch\s+-D)|"
    r"sed\s+-i|find\s+.*\s-delete|"
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
TIER_RE = re.compile(r"\bTier\s*[0-3]\b", re.IGNORECASE)
VALIDATION_RE = re.compile(r"\b(validation plan|validate|verification|tests?|audit|gate)\b", re.IGNORECASE)
BOUNDARY_RE = re.compile(r"\b(mutation boundary|write scope|scope boundary|read-only|no mutation)\b", re.IGNORECASE)
VERIFIED_RE = re.compile(r"\bverified facts?\b", re.IGNORECASE)
ASSUMPTIONS_RE = re.compile(r"\bassumptions?\b", re.IGNORECASE)
UNKNOWNS_RE = re.compile(r"\bunknowns?\b", re.IGNORECASE)
OWNER_RE = re.compile(r"\b(owner role|owner)\b", re.IGNORECASE)
EVIDENCE_RE = re.compile(r"\bevidence need\b|\bevidence\s*:\b", re.IGNORECASE)


def _load_payload() -> tuple[dict[str, Any], bool]:
    try:
        raw = json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}, True
    if not isinstance(raw, dict):
        return {}, True
    return raw, False


def _extract_command(tool_input: Any) -> str:
    if isinstance(tool_input, dict):
        for key in ("command", "cmd"):
            value = tool_input.get(key)
            if isinstance(value, str):
                return value
    if isinstance(tool_input, str):
        return tool_input
    return ""


def _latest_prompt_from_transcript(path: str | None) -> str:
    if not path:
        return ""
    transcript = Path(path)
    if not transcript.exists() or not transcript.is_file():
        return ""
    try:
        lines = transcript.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""

    for line in reversed(lines[-300:]):
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        text = _prompt_text_from_item(item)
        if text:
            return text
    return ""


def _prompt_text_from_item(item: Any) -> str:
    if not isinstance(item, dict):
        return ""
    candidates: list[Any] = []
    candidates.append(item.get("prompt"))
    candidates.append(item.get("user_prompt"))
    payload = item.get("payload")
    if isinstance(payload, dict):
        candidates.append(payload.get("prompt"))
        candidates.append(payload.get("text"))
        if payload.get("role") == "user":
            candidates.append(payload.get("content"))
    if item.get("role") == "user":
        candidates.append(item.get("content"))
    for candidate in candidates:
        text = _stringify_content(candidate)
        if text:
            return text
    return ""


def _stringify_content(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts: list[str] = []
        for entry in value:
            if isinstance(entry, str):
                parts.append(entry)
            elif isinstance(entry, dict):
                text = entry.get("text") or entry.get("content")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(parts)
    return ""


def _is_mutating(tool_name: str, tool_input: Any) -> bool:
    normalized = tool_name.lower()
    if normalized in {"apply_patch", "edit", "write"}:
        return True
    if normalized in {"bash", "shell", "functions.exec_command"}:
        command = _extract_command(tool_input)
        if READ_ONLY_SHELL_RE.search(command) and not MUTATING_SHELL_RE.search(command):
            return False
        return bool(MUTATING_SHELL_RE.search(command))
    if normalized.startswith("mcp__"):
        return bool(MUTATING_MCP_RE.search(tool_name))
    return False


def _emit_warning(missing: list[str]) -> None:
    shape_note = ""
    if "valid hook input shape" in missing:
        shape_note = "Hook input shape was unknown; "
    message = (
        f"{shape_note}ESP32 agent-process warning: this mutating tool call is starting before "
        f"the hook can see {', '.join(missing)} in the prompt context. "
        "Before continuing, state verified facts, assumptions, unknowns, selected "
        "tier, owner role, evidence need, mutation boundary, and validation plan. "
        "Project-local hooks and prompt packets are advisory aids; source-backed "
        "records and explicit gate authority remain authoritative."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "additionalContext": message,
        }
    }))


def main() -> int:
    payload, shape_unknown = _load_payload()
    if shape_unknown:
        _emit_warning(["valid hook input shape"])
        return 0

    tool_name = str(payload.get("tool_name") or "")
    tool_input = payload.get("tool_input")
    if not _is_mutating(tool_name, tool_input):
        return 0

    prompt = str(payload.get("prompt") or "") or _latest_prompt_from_transcript(
        payload.get("transcript_path")
    )
    missing = []
    if not VERIFIED_RE.search(prompt):
        missing.append("verified facts")
    if not ASSUMPTIONS_RE.search(prompt):
        missing.append("assumptions")
    if not UNKNOWNS_RE.search(prompt):
        missing.append("unknowns")
    if not TIER_RE.search(prompt):
        missing.append("selected tier")
    if not OWNER_RE.search(prompt):
        missing.append("owner role")
    if not EVIDENCE_RE.search(prompt):
        missing.append("evidence need")
    if not VALIDATION_RE.search(prompt):
        missing.append("validation path")
    if not BOUNDARY_RE.search(prompt):
        missing.append("mutation boundary")
    if not missing:
        return 0

    _emit_warning(missing)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
