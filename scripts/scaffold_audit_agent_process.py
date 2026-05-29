#!/usr/bin/env python3
"""Audit the repo-local multi-agent operating process."""

from __future__ import annotations

import json
import subprocess
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
    "SRC-CODEX-ADMIN-REQUIREMENTS-2026-05-28",
    "SRC-CODEX-HOOKS-MANAGED-2026-05-28",
    "SRC-OPENAI-LLM-ACCURACY-2026-05-28",
    "SRC-LOCAL-MULTI-AGENTIC-DEFAULT-PROCESS-2026-05-27",
    "SRC-LOCAL-MULTI-AGENTIC-CONTINUATION-DECISION-2026-05-27",
    "SRC-LOCAL-ADMIN-STRICT-CODEX-ENFORCEMENT-2026-05-28",
    "SRC-LOCAL-AGENT-INSTRUCTION-YOLO-ENFORCEMENT-2026-05-28",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _require_markers(text: str, markers: list[str], label: str) -> list[str]:
    return [f"{label} missing marker: {marker}" for marker in markers if marker not in text]


def _run_hook(
    root: Path,
    script: str,
    stdin_text: str,
    event_name: str,
    markers: list[str],
) -> list[str]:
    path = root / ".codex" / "hooks" / script
    result = subprocess.run(
        [sys.executable, str(path)],
        input=stdin_text,
        text=True,
        capture_output=True,
        check=False,
    )
    failures: list[str] = []
    label = f".codex/hooks/{script}"
    if result.returncode != 0:
        failures.append(f"{label} exited {result.returncode}: {result.stderr.strip()}")
        return failures
    if not result.stdout.strip():
        failures.append(f"{label} did not emit hookSpecificOutput")
        return failures
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        failures.append(f"{label} emitted invalid JSON: {exc}")
        return failures
    hook_output = output.get("hookSpecificOutput")
    if not isinstance(hook_output, dict):
        failures.append(f"{label} missing hookSpecificOutput object")
        return failures
    if hook_output.get("hookEventName") != event_name:
        failures.append(f"{label} hookEventName must be {event_name}")
    context = hook_output.get("additionalContext")
    if not isinstance(context, str) or not context.strip():
        failures.append(f"{label} missing additionalContext")
        return failures
    failures.extend(_require_markers(context, markers, label))
    return failures


def _run_admin_hook(
    root: Path,
    payload: dict[str, object] | str,
    markers: list[str],
) -> list[str]:
    path = root / ".codex" / "admin" / "hooks" / "esp32_admin_policy.py"
    stdin_text = payload if isinstance(payload, str) else json.dumps(payload)
    result = subprocess.run(
        [sys.executable, str(path)],
        input=stdin_text,
        text=True,
        capture_output=True,
        check=False,
    )
    failures: list[str] = []
    label = ".codex/admin/hooks/esp32_admin_policy.py"
    if result.returncode != 0:
        failures.append(f"{label} exited {result.returncode}: {result.stderr.strip()}")
        return failures
    if not markers and result.stdout.strip():
        failures.append(f"{label} should not emit output for this fixture: {result.stdout.strip()}")
        return failures
    failures.extend(_require_markers(result.stdout + result.stderr, markers, label))
    return failures


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
        "evidence need",
        "mutation boundary",
        "validation plan",
        "default-authorized",
        "no-P1/P2",
        "## Agent Instruction Enforcement Boundary",
        ".codex/agents/*.toml",
        "operator sovereignty",
        "permission_mode = \"bypassPermissions\"",
    ], "AGENTS.md"))

    governance_text = _read(root / ".agents/GOVERNANCE.md")
    failures.extend(_require_markers(governance_text, [
        "## Multi-agent operating policy",
        "yolo-compatible",
        "Weighted veto",
        "reviewer quorum",
        "default-authorized",
        "no-P1/P2",
        "Agent-process gate",
        "project-local Codex hooks remain trust-gated runtime aids",
        "Agent instruction files are the default enforcement surface",
        "/etc/codex/requirements.toml",
    ], "governance"))

    ownership_text = _read(root / ".agents/OWNERSHIP.md")
    failures.extend(_require_markers(ownership_text, [
        ".codex/",
        "knowledge-base/prompt-registry.md",
        "scripts/scaffold_audit_agent_process.py",
        "Hook trust follow-up owner",
        "Managed-profile opt-in owner",
        "AGENTS.md",
        ".codex/agents/*.toml",
    ], "ownership"))

    roles_text = _read(root / ".agents/ROLES.md")
    failures.extend(_require_markers(roles_text, [
        "## Coordinator",
        "## Agent Operations",
        "reviewer quorum",
        "default-authorized",
    ], "roles"))

    docs_text = "\n".join(_read(root / rel) for rel in [
        "docs/agent-coordination.md",
        "docs/prompt/admin-strict-codex-enforcement.md",
        "docs/prompt/prompt-triage.md",
        "docs/prompt/expert-agent-panels.md",
        "docs/prompt/preengineered-prompts.md",
        "knowledge-base/prompt-registry.md",
    ])
    failures.extend(_require_markers(docs_text, [
        "yolo-compatible",
        "bypassPermissions",
        "Agent instruction files",
        ".codex/agents/*.toml",
        "Weighted veto",
        "default-multi-agentic-process",
        "reviewer quorum",
        "UserPromptSubmit",
        "SubagentStart",
        "PreToolUse",
        "evidence need",
        "decision footer",
        "ready_for_mutation",
        "default-authorized",
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
        failures.extend(_require_markers(text, [
            "AGENTS.md as the canonical contract",
            "operator sovereignty",
            "/etc/codex/requirements.toml",
            "codex --yolo",
            "permission_mode=bypassPermissions",
            "governance is advisory",
            "admin-strict profile by name",
        ], profile))
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

    admin_requirements = root / ".codex" / "admin" / "requirements.toml"
    yolo_requirements = root / ".codex" / "admin" / "profiles" / "yolo-compatible" / "requirements.toml"
    strict_requirements = root / ".codex" / "admin" / "profiles" / "admin-strict" / "requirements.toml"
    admin_hook = root / ".codex" / "admin" / "hooks" / "esp32_admin_policy.py"
    admin_installer = root / ".codex" / "admin" / "install_admin_policy.py"
    admin_readme = root / ".codex" / "admin" / "README.md"
    for path in [admin_requirements, yolo_requirements, strict_requirements, admin_hook, admin_installer, admin_readme]:
        if not path.exists():
            failures.append(f"missing admin policy artifact: {path.relative_to(root)}")

    def _audit_yolo_requirements(path: Path) -> None:
        raw_text = _read(path)
        for marker in ["allowed_sandbox_modes", "allowed_approval_policies", "rules.prefix_rules"]:
            if marker in raw_text:
                failures.append(f"{path.relative_to(root)} must not contain {marker}; yolo must remain full access")
        try:
            requirements = tomllib.loads(raw_text)
        except tomllib.TOMLDecodeError as exc:
            failures.append(f"{path.relative_to(root)} invalid TOML: {exc}")
            return
        if requirements.get("allow_managed_hooks_only") is not True:
            failures.append(f"{path.relative_to(root)} must set allow_managed_hooks_only = true")
        if requirements.get("features", {}).get("hooks") is not True:
            failures.append(f"{path.relative_to(root)} must set [features].hooks = true")
        if requirements.get("hooks", {}).get("managed_dir") != "/etc/codex/hooks":
            failures.append(f"{path.relative_to(root)} hooks.managed_dir must be /etc/codex/hooks")
        for key in ["allowed_sandbox_modes", "allowed_approval_policies"]:
            if key in requirements:
                failures.append(f"{path.relative_to(root)} must not set {key}; yolo must remain full access")
        rules = requirements.get("rules")
        if isinstance(rules, dict) and "prefix_rules" in rules:
            failures.append(f"{path.relative_to(root)} must not set rules.prefix_rules")

    for path in [admin_requirements, yolo_requirements]:
        if path.exists():
            _audit_yolo_requirements(path)
    if strict_requirements.exists():
        try:
            requirements = tomllib.loads(_read(strict_requirements))
        except tomllib.TOMLDecodeError as exc:
            failures.append(f".codex/admin/profiles/admin-strict/requirements.toml invalid TOML: {exc}")
            requirements = {}
        if "danger-full-access" in requirements.get("allowed_sandbox_modes", []):
            failures.append("admin-strict profile must block danger-full-access by omission")
        if "never" in requirements.get("allowed_approval_policies", []):
            failures.append("admin-strict profile must block approval_policy never by omission")
        strict_text = _read(strict_requirements)
        failures.extend(_require_markers(strict_text, [
            "Explicit opt-in only",
            "blocks `codex --yolo`",
        ], "admin-strict requirements"))
    for path in [admin_hook, admin_installer, admin_readme]:
        if path.exists():
            failures.extend(_require_markers(_read(path), [
                "yolo",
                "Tier 3",
            ], str(path.relative_to(root))))

    failures.extend(_run_admin_hook(
        root,
        "{",
        ["hookSpecificOutput", "Hook input shape was unknown"],
    ))
    failures.extend(_run_admin_hook(
        root,
        {
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "touch should-deny"},
            "prompt": "",
        },
        ["permissionDecision", "deny", "missing routing packet fields"],
    ))
    failures.extend(_run_admin_hook(
        root,
        {
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": "idf.py flash"},
            "prompt": (
                "Verified facts: none. Assumptions: none. Unknowns: none. "
                "Selected tier: Tier 2. Owner role: QA. Evidence need: local. "
                "Mutation boundary: docs. Validation plan: tests."
            ),
        },
        ["permissionDecision", "deny", "Tier 3 command denied"],
    ))
    failures.extend(_run_admin_hook(
        root,
        {
            "hook_event_name": "SubagentStop",
            "last_assistant_message": "Looks fine.",
        },
        ["block", "reviewer output missing"],
    ))
    failures.extend(_run_admin_hook(
        root,
        {
            "hook_event_name": "Stop",
            "last_assistant_message": "Implemented the admin policy.",
        },
        ["block", "decision footer"],
    ))
    failures.extend(_run_admin_hook(
        root,
        {
            "hook_event_name": "PreToolUse",
            "permission_mode": "bypassPermissions",
            "tool_name": "Bash",
            "tool_input": {"command": "git reset --hard HEAD"},
            "prompt": "",
        },
        [],
    ))

    failures.extend(_run_hook(
        root,
        "user_prompt_submit_agent_process.py",
        json.dumps({"hook_event_name": "UserPromptSubmit"}),
        "UserPromptSubmit",
        ["evidence need", "default-authorized", "decision footer", "advisory aids"],
    ))
    failures.extend(_run_hook(
        root,
        "subagent_start_agent_process.py",
        json.dumps({"agent_type": "qa-validation-reviewer", "permission_mode": "read-only"}),
        "SubagentStart",
        ["default-authorized", "explicit disjoint write scope", "advisory aids"],
    ))
    failures.extend(_run_hook(
        root,
        "pre_tool_use_agent_process.py",
        json.dumps({
            "tool_name": "functions.exec_command",
            "tool_input": {"cmd": "touch scaffold-audit-should-warn"},
            "prompt": "Tier 2 validation plan mutation boundary",
        }),
        "PreToolUse",
        ["verified facts", "assumptions", "unknowns", "owner role", "evidence need", "advisory aids"],
    ))
    for script, event_name in [
        ("user_prompt_submit_agent_process.py", "UserPromptSubmit"),
        ("subagent_start_agent_process.py", "SubagentStart"),
        ("pre_tool_use_agent_process.py", "PreToolUse"),
    ]:
        failures.extend(_run_hook(
            root,
            script,
            "[]",
            event_name,
            ["Hook input shape was unknown"],
        ))

    docs_index = _read(root / "docs/index.md")
    for link in [
        "../.agents/TASK_LOG/0074-multi-agentic-default-process.md",
        "../.agents/handoffs/0063-multi-agentic-default-process-to-qa.md",
        "../knowledge-base/source-ledger/2026-05-27-multi-agentic-default-process.md",
        "../.agents/TASK_LOG/0077-multi-agentic-continuation-decision.md",
        "../.agents/handoffs/0066-multi-agentic-continuation-decision-to-qa.md",
        "../knowledge-base/source-ledger/2026-05-27-multi-agentic-continuation-decision.md",
        "../.agents/TASK_LOG/0084-admin-strict-codex-enforcement.md",
        "../.agents/handoffs/0073-admin-strict-codex-enforcement-to-qa.md",
        "../knowledge-base/source-ledger/2026-05-28-admin-strict-codex-enforcement.md",
        "../.agents/TASK_LOG/0085-agent-instruction-yolo-enforcement.md",
        "../.agents/handoffs/0074-agent-instruction-yolo-enforcement-to-qa.md",
        "../knowledge-base/source-ledger/2026-05-28-agent-instruction-yolo-enforcement.md",
        "prompt/admin-strict-codex-enforcement.md",
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
        ".agents/TASK_LOG/0077-multi-agentic-continuation-decision.md",
        ".agents/handoffs/0066-multi-agentic-continuation-decision-to-qa.md",
        "knowledge-base/source-ledger/2026-05-27-multi-agentic-continuation-decision.md",
        ".agents/TASK_LOG/0084-admin-strict-codex-enforcement.md",
        ".agents/handoffs/0073-admin-strict-codex-enforcement-to-qa.md",
        "knowledge-base/source-ledger/2026-05-28-admin-strict-codex-enforcement.md",
        ".agents/TASK_LOG/0085-agent-instruction-yolo-enforcement.md",
        ".agents/handoffs/0074-agent-instruction-yolo-enforcement-to-qa.md",
        "knowledge-base/source-ledger/2026-05-28-agent-instruction-yolo-enforcement.md",
    ]:
        path = root / rel
        if not path.exists():
            failures.append(f"missing record: {rel}")

    tests_readme = _read(root / "tests/README.md")
    failures.extend(_require_markers(tests_readme, [
        "python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'",
        "python3 scripts/scaffold_audit_agent_process.py",
    ], "tests README"))

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
