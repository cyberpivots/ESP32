#!/usr/bin/env python3
"""Audit the repo-local multi-agent operating process."""

from __future__ import annotations

import json
import sys
import tomllib
from pathlib import Path

from scaffold_audit_data import ROOT


REQUIRED_AGENT_PROFILES = [
    "governance-cartographer",
    "evidence-record-auditor",
    "live-bench-gate-reviewer",
    "win31-dashboard-vision-gate",
    "ui-code-protocol-analyst",
    "source-skill-curator",
    "prompt-token-triage",
    "qa-validation-reviewer",
    "governance-doc-worker",
    "kb-record-worker",
    "bounded-implementation-worker",
]
REQUIRED_SOURCE_IDS = [
    "SRC-CODEX-HOOKS-2026-05-27",
    "SRC-CODEX-SUBAGENTS-2026-05-27",
    "SRC-CODEX-CONFIG-REFERENCE-2026-05-27",
    "SRC-OPENAI-AGENTS-SDK-2026-05-27",
    "SRC-OPENAI-AGENTS-ORCHESTRATION-2026-05-27",
    "SRC-ANTHROPIC-MULTI-AGENT-RESEARCH-2026-05-27",
    "SRC-LANGCHAIN-HANDOFFS-2026-05-27",
    "SRC-LANGCHAIN-CONTEXT-ENGINEERING-2026-05-27",
    "SRC-LOCAL-MULTI-AGENTIC-DEFAULT-PROCESS-2026-05-27",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _require_markers(text: str, markers: list[str], label: str) -> list[str]:
    return [f"{label} missing marker: {marker}" for marker in markers if marker not in text]


def audit_agent_process(root: Path = ROOT) -> list[str]:
    failures: list[str] = []

    agents_text = _read(root / "AGENTS.md")
    failures.extend(_require_markers(agents_text, [
        "## Multi-Agent Process For Every Prompt",
        "Tier 0",
        "Tier 1",
        "Tier 2",
        "Tier 3",
        "selected tier",
        "owner role",
        "mutation boundary",
        "validation plan",
    ], "AGENTS.md"))

    governance_text = _read(root / ".agents/GOVERNANCE.md")
    failures.extend(_require_markers(governance_text, [
        "## Multi-agent operating policy",
        "reviewer quorum",
        "Agent-process gate",
        "project-local Codex hooks remain trust-gated runtime aids",
    ], "governance"))

    ownership_text = _read(root / ".agents/OWNERSHIP.md")
    failures.extend(_require_markers(ownership_text, [
        ".codex/",
        "knowledge-base/prompt-registry.md",
        "scripts/scaffold_audit_agent_process.py",
        "Hook trust follow-up owner",
    ], "ownership"))

    roles_text = _read(root / ".agents/ROLES.md")
    failures.extend(_require_markers(roles_text, [
        "## Coordinator",
        "## Agent Operations",
        "reviewer quorum",
    ], "roles"))

    docs_text = "\n".join(_read(root / rel) for rel in [
        "docs/agent-coordination.md",
        "docs/prompt/prompt-triage.md",
        "docs/prompt/expert-agent-panels.md",
        "docs/prompt/preengineered-prompts.md",
        "knowledge-base/prompt-registry.md",
    ])
    failures.extend(_require_markers(docs_text, [
        "default-multi-agentic-process",
        "reviewer quorum",
        "UserPromptSubmit",
        "SubagentStart",
        "PreToolUse",
        "bounded-implementation-worker",
    ], "agent process docs"))

    config_path = root / ".codex/config.toml"
    config = tomllib.loads(_read(config_path))
    agents = config.get("agents", {})
    if agents.get("max_threads") != 6:
        failures.append(".codex/config.toml agents.max_threads must be 6")
    if agents.get("max_depth") != 1:
        failures.append(".codex/config.toml agents.max_depth must be 1")
    for profile in REQUIRED_AGENT_PROFILES:
        entry = agents.get(profile)
        if not isinstance(entry, dict):
            failures.append(f".codex/config.toml missing agent profile: {profile}")
            continue
        expected = f"agents/{profile}.toml"
        if entry.get("config_file") != expected:
            failures.append(f"{profile} config_file must be {expected}")

    for profile in REQUIRED_AGENT_PROFILES:
        path = root / ".codex/agents" / f"{profile}.toml"
        if not path.exists():
            failures.append(f"missing agent file: {path.relative_to(root)}")
            continue
        data = tomllib.loads(_read(path))
        for key in ["name", "description", "developer_instructions"]:
            if key not in data:
                failures.append(f"{path.relative_to(root)} missing {key}")
        if data.get("name") != profile:
            failures.append(f"{path.relative_to(root)} name must be {profile}")
        text = _read(path)
        if "worker" in profile:
            failures.extend(_require_markers(text, [
                "explicit write scope",
                "Preserve dirty work",
                "Do not select",
                "Do not run live hardware",
                "Do not commit or push",
            ], profile))

    hooks_config = json.loads(_read(root / ".codex/hooks.json"))
    hooks = hooks_config.get("hooks", {})
    for event in ["UserPromptSubmit", "SubagentStart", "PreToolUse"]:
        groups = hooks.get(event)
        if not isinstance(groups, list) or not groups:
            failures.append(f".codex/hooks.json missing event: {event}")
            continue
        command_text = json.dumps(groups)
        if ".codex/hooks/" not in command_text or "python3" not in command_text:
            failures.append(f"{event} hook does not call repo-local python script")
    for script in [
        "user_prompt_submit_agent_process.py",
        "subagent_start_agent_process.py",
        "pre_tool_use_agent_process.py",
    ]:
        path = root / ".codex/hooks" / script
        if not path.exists():
            failures.append(f"missing hook script: .codex/hooks/{script}")
        elif "hookSpecificOutput" not in _read(path):
            failures.append(f".codex/hooks/{script} missing hookSpecificOutput")

    docs_index = _read(root / "docs/index.md")
    for link in [
        "../.agents/TASK_LOG/0074-multi-agentic-default-process.md",
        "../.agents/handoffs/0063-multi-agentic-default-process-to-qa.md",
        "../knowledge-base/source-ledger/2026-05-27-multi-agentic-default-process.md",
    ]:
        if link not in docs_index:
            failures.append(f"docs index missing multi-agent link: {link}")

    source_index = _read(root / "knowledge-base/source-index.md")
    for source_id in REQUIRED_SOURCE_IDS:
        if source_id not in source_index:
            failures.append(f"source index missing {source_id}")

    for rel in [
        ".agents/TASK_LOG/0074-multi-agentic-default-process.md",
        ".agents/handoffs/0063-multi-agentic-default-process-to-qa.md",
        "knowledge-base/source-ledger/2026-05-27-multi-agentic-default-process.md",
    ]:
        path = root / rel
        if not path.exists():
            failures.append(f"missing record: {rel}")

    return failures


def main() -> int:
    failures = audit_agent_process()
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("PASS: ESP32 agent-process audit succeeded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
