#!/usr/bin/env python3
"""Shared ESP32 agent-process hook classifiers.

The helpers in this module are stdlib-only so project-local hooks and managed
admin hook copies can import the same command and text classifiers.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


BYPASS_PERMISSION_MODE = "bypassPermissions"

ROUTING_PATTERNS = {
    "verified facts": re.compile(r"\bverified facts?\b", re.IGNORECASE),
    "assumptions": re.compile(r"\bassumptions?\b", re.IGNORECASE),
    "unknowns": re.compile(r"\bunknowns?\b", re.IGNORECASE),
    "selected tier": re.compile(r"\b(selected tier|Tier\s*[0-3])\b", re.IGNORECASE),
    "owner role": re.compile(r"\bowner role\b", re.IGNORECASE),
    "evidence need": re.compile(r"\bevidence need\b", re.IGNORECASE),
    "mutation boundary": re.compile(
        r"\b(mutation boundary|write scope|scope boundary|read-only|no mutation|no-mutation boundary)\b",
        re.IGNORECASE,
    ),
    "validation plan": re.compile(r"\b(validation plan|validation path|validate|verification|tests?|audit|gate)\b", re.IGNORECASE),
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
MUTATION_CLAIM_RE = re.compile(
    r"\b(implemented|updated|changed|created|installed|wrote|modified|ran tests|patched)\b",
    re.IGNORECASE,
)
BYPASS_RE = re.compile(
    r"\b(ignore|bypass|disable|skip|override)\b.{0,80}\b"
    r"(AGENTS\.md|governance|hook|requirements|reviewer quorum|Tier 3|safety gate)\b",
    re.IGNORECASE | re.DOTALL,
)

READ_ONLY_SHELL_START_RE = re.compile(
    r"^\s*(pwd|ls|find|rg|grep|sed|cat|nl|wc|head|tail|sort|uniq|git\s+(status|diff|show|log)|"
    r"python3?\s+-m\s+(json\.tool|unittest)|"
    r"python3?\s+scripts/(verify|scaffold_audit|agent_process_decision|agent_scheduler)[\w_./-]*\.py)\b",
    re.IGNORECASE,
)
READ_ONLY_FOR_LOOP_RE = re.compile(
    r"^\s*for\s+\w+\s+in\s+.+;\s*do\s+"
    r"(sed|cat|nl|wc|rg|grep|head|tail|git\s+(status|diff|show|log))\b.+;\s*done\s*$",
    re.IGNORECASE | re.DOTALL,
)
MUTATING_SHELL_RE = re.compile(
    r"(^|[;&|()\s])("
    r"apply_patch|rm|mv|cp|touch|mkdir|chmod|chown|truncate|dd|install|"
    r"git\s+(add|commit|push|merge|rebase|reset|checkout|switch|clean|tag|branch\s+-D)|"
    r"gh\s+(pr\s+create|pr\s+merge|pr\s+close|repo|release|workflow\s+run)|"
    r"sed\s+-i|find\s+.*\s-delete|"
    r"python3?\s+.*(write|update|generate|build|package|install|deploy|flash)"
    r")\b|"
    r"(>>|>\s*[^&]|\|\s*tee\b)",
    re.IGNORECASE | re.DOTALL,
)
MUTATING_MCP_RE = re.compile(
    r"(write|edit|delete|remove|create|update|patch|apply|commit|push|merge|"
    r"flash|erase|deploy|upload)",
    re.IGNORECASE,
)
LIVE_TIER3_COMMAND_RE = re.compile(
    r"\b(esptool|idf\.py\s+(-p|flash|erase|monitor)|flash|erase|monitor|"
    r"serial[-_ ]?write|minicom|picocom|screen\s+/dev/|ble|bluetooth|"
    r"esp[-_]?wifi[-_]?mesh|mesh|pcap|tcpdump|wireshark|relay|xbee[\w_-]*|tft|"
    r"microsd|micro[-_ ]?sd|load|wiring|mains|router admin|router-admin)\b",
    re.IGNORECASE,
)
LIVE_TIER3_TOOL_RE = re.compile(
    r"(flash|erase|monitor|serial|ble|mesh|pcap|relay|xbee|tft|microsd|load|wiring|mains)",
    re.IGNORECASE,
)
SYSTEM_CODEX_RE = re.compile(r"(^|[^A-Za-z0-9_./-])/etc/codex\b", re.IGNORECASE)
ENV_PREFIX_RE = re.compile(r"^\s*(?:[A-Za-z_][A-Za-z0-9_]*=[^\s]+)\s+")
PUBLICATION_SHELL_RE = re.compile(
    r"\b(git\s+push|gh\s+(pr\s+create|pr\s+merge|repo|release|workflow\s+run)|"
    r"deploy|release|pages\s+deploy)\b",
    re.IGNORECASE,
)
DESTRUCTIVE_GIT_RE = re.compile(
    r"\bgit\s+(reset\s+--hard|clean\b|checkout\b|switch\b|branch\s+-D|rebase\b|merge\b)",
    re.IGNORECASE,
)
REDIRECTION_OR_TEE_RE = re.compile(r"(>>|>\s*[^&]|\|\s*tee\b)", re.IGNORECASE)


@dataclass(frozen=True)
class ClassificationResult:
    """Structured classification for hook-facing command decisions."""

    category: str
    reasons: tuple[str, ...]
    read_only: bool = False
    mutation: bool = False
    tier3: bool = False
    system_codex: bool = False
    publication: bool = False
    destructive_git: bool = False
    redirection_or_tee: bool = False


def extract_command(tool_input: Any) -> str:
    if isinstance(tool_input, dict):
        for key in ("command", "cmd"):
            value = tool_input.get(key)
            if isinstance(value, str):
                return value
    if isinstance(tool_input, str):
        return tool_input
    return ""


def stringify(value: Any) -> str:
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


def text_from_item(item: Any, role: str | None = None) -> str:
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
        text = stringify(candidate)
        if text:
            return text
    return ""


def latest_text_from_transcript(path: str | None, role: str | None = None, limit: int = 500) -> str:
    if not path:
        return ""
    transcript = Path(path)
    if not transcript.exists() or not transcript.is_file():
        return ""
    try:
        lines = transcript.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""
    for line in reversed(lines[-limit:]):
        try:
            item = json.loads(line)
        except json.JSONDecodeError:
            continue
        text = text_from_item(item, role)
        if text:
            return text
    return ""


def visible_context(payload: dict[str, Any]) -> str:
    pieces = [
        stringify(payload.get("prompt")),
        stringify(payload.get("last_assistant_message")),
        latest_text_from_transcript(payload.get("transcript_path")),
    ]
    return "\n".join(piece for piece in pieces if piece)


def missing(patterns: dict[str, re.Pattern[str]], text: str) -> list[str]:
    return [name for name, pattern in patterns.items() if not pattern.search(text)]


def field_value(text: str, name: str) -> str:
    pattern = FIELD_PATTERNS[name]
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def has_open_p1_p2_findings(text: str) -> bool:
    value = field_value(text, "P1/P2 findings")
    if not value:
        return False
    return not bool(NO_BLOCKERS_RE.search(value))


def has_reject_vote(text: str) -> bool:
    value = field_value(text, "vote").lower()
    return "reject" in value or "veto" in value


def footer_semantic_failure(message: str) -> str | None:
    decision = field_value(message, "decision").lower()
    if decision in NON_TERMINAL_DECISIONS:
        return f"decision {decision!r} is not terminal; continue the turn."
    if decision and decision not in TERMINAL_DECISIONS:
        return f"decision {decision!r} is not a recognized final decision."

    validation = field_value(message, "validation")
    if PENDING_OR_MISSING_RE.search(validation):
        return "validation is pending or missing."

    durable_records = field_value(message, "durable records")
    if PENDING_OR_MISSING_RE.search(durable_records) or durable_records.lower() in {"none", "n/a", "na"}:
        return "durable records are pending or missing."
    return None


def is_bypass_permission_mode(payload: dict[str, Any]) -> bool:
    return payload.get("permission_mode") == BYPASS_PERMISSION_MODE


def is_shell_read_only_command(command: str) -> bool:
    return classify_shell_command(command).read_only


def strip_leading_env_assignments(command: str) -> str:
    previous = command
    while True:
        current = ENV_PREFIX_RE.sub("", previous, count=1)
        if current == previous:
            return current
        previous = current


def is_mutating_shell_command(command: str) -> bool:
    return classify_shell_command(command).mutation


def is_live_tier3_shell_command(command: str) -> bool:
    return classify_shell_command(command).tier3


def classify_shell_command(command: str) -> ClassificationResult:
    normalized = strip_leading_env_assignments(command)
    reasons: list[str] = []
    if not normalized.strip():
        return ClassificationResult(category="unknown", reasons=("empty command",))

    system_codex = bool(SYSTEM_CODEX_RE.search(normalized))
    publication = bool(PUBLICATION_SHELL_RE.search(normalized))
    destructive_git = bool(DESTRUCTIVE_GIT_RE.search(normalized))
    redirection_or_tee = bool(REDIRECTION_OR_TEE_RE.search(normalized))
    tier3 = bool(LIVE_TIER3_COMMAND_RE.search(normalized))
    mutation = bool(
        MUTATING_SHELL_RE.search(normalized)
        or system_codex
        or publication
        or destructive_git
        or redirection_or_tee
    )

    if system_codex:
        reasons.append("/etc/codex path")
    if publication:
        reasons.append("publication command")
    if destructive_git:
        reasons.append("destructive git command")
    if redirection_or_tee:
        reasons.append("redirection or tee")
    if tier3:
        reasons.append("Tier 3 live-surface command")
    if mutation and not reasons:
        reasons.append("mutating shell command")

    read_only = False
    if not mutation and not tier3 and READ_ONLY_FOR_LOOP_RE.search(normalized):
        read_only = True
    elif not mutation and not tier3 and READ_ONLY_SHELL_START_RE.search(normalized):
        read_only = True

    if read_only:
        return ClassificationResult(category="read_only", reasons=("read-only shell command",), read_only=True)

    category = "unknown"
    if tier3:
        category = "tier3"
    elif publication:
        category = "publication"
    elif destructive_git:
        category = "destructive_git"
    elif system_codex:
        category = "system_codex"
    elif mutation:
        category = "mutation"

    return ClassificationResult(
        category=category,
        reasons=tuple(reasons) or ("unclassified command",),
        read_only=False,
        mutation=mutation,
        tier3=tier3,
        system_codex=system_codex,
        publication=publication,
        destructive_git=destructive_git,
        redirection_or_tee=redirection_or_tee,
    )


def classify_tool(tool_name: str, tool_input: Any) -> ClassificationResult:
    normalized = tool_name.lower()
    command = extract_command(tool_input)
    if normalized in {"bash", "shell", "functions.exec_command"}:
        return classify_shell_command(command)
    if normalized in {"apply_patch", "edit", "write"}:
        return ClassificationResult(category="mutation", reasons=("mutating tool",), mutation=True)
    if normalized.startswith("mcp__") and MUTATING_MCP_RE.search(tool_name):
        return ClassificationResult(category="mutation", reasons=("mutating MCP tool",), mutation=True)
    return ClassificationResult(category="unknown", reasons=("unclassified tool",))


def is_mutating_tool(tool_name: str, tool_input: Any) -> bool:
    return classify_tool(tool_name, tool_input).mutation


def is_live_tier3_tool(tool_name: str, tool_input: Any) -> bool:
    result = classify_tool(tool_name, tool_input)
    return bool(result.tier3 or LIVE_TIER3_TOOL_RE.search(tool_name))
