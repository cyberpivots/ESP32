#!/usr/bin/env python3
"""Audit the repo-local multi-agent operating process."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
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
DEVELOPMENT_PANEL_AGENT_PROFILES = [
    "development-panel-coordinator",
    "esp32-firmware-device-reviewer",
    "xbee-radio-protocol-reviewer",
    "ui-ux-interface-reviewer",
    "source-research-reviewer",
    "data-model-kb-reviewer",
    "tooling-resource-reviewer",
    "offgrid-comms-domain-reviewer",
    "security-safety-risk-reviewer",
    "devex-ci-release-reviewer",
    "kb-prompt-registry-curator",
    "protocol-bridge-abi-reviewer",
    "power-wiring-isolation-reviewer",
]
REQUIRED_AGENT_PROFILES.extend(DEVELOPMENT_PANEL_AGENT_PROFILES)
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
    "SRC-CODEX-SKILLS-2026-06-02",
    "SRC-CODEX-AGENTS-MD-2026-06-02",
    "SRC-CODEX-HOOKS-2026-06-02",
    "SRC-CODEX-MANAGED-CONFIG-2026-06-02",
    "SRC-CODEX-SUBAGENTS-2026-06-02",
    "SRC-OPENAI-LLM-ACCURACY-2026-05-28",
    "SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-06-02",
    "SRC-LOCAL-MULTI-AGENTIC-DEFAULT-PROCESS-2026-05-27",
    "SRC-LOCAL-MULTI-AGENTIC-CONTINUATION-DECISION-2026-05-27",
    "SRC-LOCAL-ADMIN-STRICT-CODEX-ENFORCEMENT-2026-05-28",
    "SRC-LOCAL-AGENT-INSTRUCTION-YOLO-ENFORCEMENT-2026-05-28",
    "SRC-LOCAL-MULTI-AGENTIC-CONTINUOUS-ENFORCEMENT-2026-05-29",
    "SRC-LOCAL-DEVELOPMENT-AGENT-PANEL-2026-05-31",
    "SRC-LOCAL-COMPREHENSIVE-BENCH-DEVELOPMENT-PROCESS-2026-05-31",
    "SRC-LOCAL-MULTI-WINDOW-CODEX-SCHEDULER-2026-06-01",
    "SRC-LOCAL-SUBAGENT-LIFECYCLE-CLEANUP-2026-06-01",
    "SRC-LOCAL-ALWAYS-ON-SUBAGENT-PROCESS-ENFORCEMENT-2026-06-02",
    "SRC-LOCAL-AGENT-INSTRUCTION-SKILL-HOOK-CI-HARDENING-2026-06-02",
    "SRC-LOCAL-AGENT-PROCESS-HARDENING-PRODUCTION-REFACTOR-2026-06-02",
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


def _run_admin_installer_dry_run(root: Path, profile: str) -> list[str]:
    path = root / ".codex" / "admin" / "install_admin_policy.py"
    label = f".codex/admin/install_admin_policy.py --dry-run --profile {profile}"
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "codex"
        result = subprocess.run(
            [sys.executable, str(path), "--dry-run", "--profile", profile, "--target-dir", str(target)],
            text=True,
            capture_output=True,
            check=False,
        )
    if result.returncode != 0:
        return [f"{label} exited {result.returncode}: {result.stdout}{result.stderr}"]
    return _require_markers(result.stdout, [
        f"profile: {profile}",
        "target-dir:",
        "source files",
        "target files",
        "requirements diff",
        "hook diff",
        "support:agent_process_classifiers.py diff",
        "support:agent_process_contracts.py diff",
        "planned backups",
        "sha256=",
        "mode=",
        "owner=",
    ], label)


def _run_admin_installer_temp_smoke(root: Path) -> list[str]:
    path = root / ".codex" / "admin" / "install_admin_policy.py"
    failures: list[str] = []
    label = ".codex/admin/install_admin_policy.py temp --target-dir smoke"
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "codex"
        install_result = subprocess.run(
            [sys.executable, str(path), "--install", "--profile", "yolo-compatible", "--target-dir", str(target)],
            text=True,
            capture_output=True,
            check=False,
        )
        if install_result.returncode != 0:
            return [f"{label} install exited {install_result.returncode}: {install_result.stdout}{install_result.stderr}"]
        failures.extend(_require_markers(install_result.stdout, [
            "installed profile: yolo-compatible",
            "agent_process_classifiers.py",
            "agent_process_contracts.py",
            "sha256=",
            "mode=",
            "owner=",
            "backups:",
        ], label))

        hook = target / "hooks" / "esp32_admin_policy.py"
        support_files = [
            target / "hooks" / "agent_process_classifiers.py",
            target / "hooks" / "agent_process_contracts.py",
        ]
        for support in [hook, *support_files]:
            if not support.exists():
                failures.append(f"{label} missing installed file: {support}")
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        hook_fixtures: list[dict[str, object] | str] = [
            "{",
            {"hook_event_name": "UserPromptSubmit", "permission_mode": "bypassPermissions"},
        ]
        for fixture in hook_fixtures:
            stdin_text = fixture if isinstance(fixture, str) else json.dumps(fixture)
            hook_result = subprocess.run(
                [sys.executable, str(hook)],
                input=stdin_text,
                text=True,
                capture_output=True,
                check=False,
                cwd=tmp,
                env=env,
            )
            if hook_result.returncode != 0:
                failures.append(f"{label} installed hook exited {hook_result.returncode}: {hook_result.stderr.strip()}")
                continue
            if "ModuleNotFoundError" in hook_result.stderr:
                failures.append(f"{label} installed hook imported from repo or missed support module: {hook_result.stderr.strip()}")
            failures.extend(_require_markers(hook_result.stdout, ["hookSpecificOutput"], label))

        validate_result = subprocess.run(
            [sys.executable, str(path), "--validate", "--profile", "yolo-compatible", "--target-dir", str(target)],
            text=True,
            capture_output=True,
            check=False,
        )
        if validate_result.returncode != 0:
            failures.append(f"{label} validate exited {validate_result.returncode}: {validate_result.stdout}{validate_result.stderr}")
        else:
            failures.extend(_require_markers(validate_result.stdout, [
                "validated profile: yolo-compatible",
                "agent_process_classifiers.py",
                "agent_process_contracts.py",
            ], label))

        remove_result = subprocess.run(
            [sys.executable, str(path), "--remove-system-requirements", "--target-dir", str(target)],
            text=True,
            capture_output=True,
            check=False,
        )
        if remove_result.returncode != 0:
            failures.append(f"{label} remove exited {remove_result.returncode}: {remove_result.stdout}{remove_result.stderr}")
        else:
            failures.extend(_require_markers(remove_result.stdout, [
                "removed target requirements",
                "remaining managed hook files",
                "agent_process_classifiers.py",
                "agent_process_contracts.py",
            ], label))
        if (target / "requirements.toml").exists():
            failures.append(f"{label} remove left temp requirements.toml in place")
    return failures


def _run_decision_helper(root: Path) -> list[str]:
    path = root / "scripts" / "agent_process_decision.py"
    failures: list[str] = []
    label = "scripts/agent_process_decision.py"
    result = subprocess.run(
        [sys.executable, str(path), "template", "--json"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return [f"{label} template exited {result.returncode}: {result.stderr.strip()}"]
    try:
        packet = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        return [f"{label} template emitted invalid JSON: {exc}"]
    packet["evidenceGaps"] = []
    packet["workRemaining"] = []
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as handle:
        json.dump(packet, handle)
        packet_path = Path(handle.name)
    try:
        evaluated = subprocess.run(
            [sys.executable, str(path), "evaluate", "--packet", str(packet_path), "--json"],
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        packet_path.unlink(missing_ok=True)
    if evaluated.returncode != 0:
        failures.append(f"{label} evaluate exited {evaluated.returncode}: {evaluated.stdout}{evaluated.stderr}")
        return failures
    failures.extend(_require_markers(evaluated.stdout, [
        '"decision": "ready_for_mutation"',
        '"gatePasses": true',
        '"approvalRatio"',
    ], label))
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
        "mandatory to attempt",
        "no-P1/P2",
        "Agent lifecycle cleanup",
        "inspect completed agents before spawning",
        "close completed/stale agents",
        "close agents before fallback/final",
        "fallback is valid only after a cleanup attempt",
        "Standing user authorization",
        "requested and allowed for every prompt",
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
        "mandatory to attempt",
        "no-P1/P2",
        "Agent-process gate",
        "project-local Codex hooks remain trust-gated runtime aids",
        "Agent instruction files are the default enforcement surface",
        "/etc/codex/requirements.toml",
        "Agent lifecycle cleanup",
        "wait_agent",
        "close_agent",
        "guarantee runtime slot release",
        "Standing user authorization",
        "requested and allowed for every prompt",
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
        "mandatory to attempt",
        "agent lifecycle cleanup",
        "fallback only after cleanup attempt",
        "Standing user authorization",
        "requested and allowed for every prompt",
    ], "roles"))

    docs_text = "\n".join(_read(root / rel) for rel in [
        "docs/agent-coordination.md",
        "docs/prompt/admin-strict-codex-enforcement.md",
        "docs/prompt/prompt-triage.md",
        "docs/prompt/expert-agent-panels.md",
        "docs/prompt/preengineered-prompts.md",
        "docs/prompt/multi-window-codex-scheduler.md",
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
        "Missing evidence",
        "agent_process_decision.py",
        "ready_for_mutation",
        "mandatory subagent attempt",
        "agent lifecycle cleanup",
        "inspect completed agents before spawning",
        "close completed/stale agents",
        "close agents before fallback/final",
        "fallback only after cleanup attempt",
        "bypassPermissions advisory only",
        "bounded-implementation-worker",
        "development-agent-panel",
        "bench_state_packet.v1",
        "comprehensive-bench-development-process",
        "development-panel-coordinator",
        "security-safety-risk-reviewer",
        "xbee-radio-protocol-reviewer",
        "multi-window-codex-scheduler",
        "agent_scheduler.py",
        "scheduler-unavailable",
        "multi_window_coordination.v1",
        "Standing user authorization",
        "requested and allowed for every prompt",
    ], "agent process docs"))

    decision_helper = root / "scripts" / "agent_process_decision.py"
    if not decision_helper.exists():
        failures.append("missing script: scripts/agent_process_decision.py")
    else:
        helper_text = _read(decision_helper)
        failures.extend(_require_markers(helper_text, [
            "weighted",
            "approvalThreshold",
            "P1",
            "P2",
            "same-session evidence",
            "continue",
            "ask_user",
            "ready_for_mutation",
        ], "scripts/agent_process_decision.py"))
        failures.extend(_run_decision_helper(root))

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
            "Contract IDs: ESP32-GOV-v1 SOV-v1 LIFECYCLE-v1 TIER3-CLOSED-v1",
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
        if profile in DEVELOPMENT_PANEL_AGENT_PROFILES:
            if data.get("sandbox_mode") != "read-only":
                failures.append(f"{path.relative_to(root)} must be read-only")
            failures.extend(_require_markers(text, [
                "Purpose:",
                "Inputs:",
                "Outputs:",
                "Read scope:",
                "Later mutation scope if separately authorized:",
                "Stop conditions:",
                "Escalation conditions:",
                "Required evidence before action:",
                "Validation method:",
                "Tier boundaries:",
            ], profile))

    hooks_config = json.loads(_read(root / ".codex/hooks.json"))
    hooks = hooks_config.get("hooks", {})
    for event in ["UserPromptSubmit", "SubagentStart", "SubagentStop", "PreToolUse"]:
        groups = hooks.get(event)
        if not isinstance(groups, list) or not groups:
            failures.append(f".codex/hooks.json missing event: {event}")
            continue
        command_text = json.dumps(groups)
        if ".codex/hooks/" not in command_text or "python3" not in command_text:
            failures.append(f"{event} hook does not call repo-local python script")
    pretool_text = json.dumps(hooks.get("PreToolUse", []))
    if "functions\\\\.exec_command" not in pretool_text:
        failures.append(".codex/hooks.json PreToolUse matcher must include functions.exec_command")
    for script in [
        "user_prompt_submit_agent_process.py",
        "subagent_start_agent_process.py",
        "subagent_stop_agent_process.py",
        "pre_tool_use_agent_process.py",
    ]:
        path = root / ".codex/hooks" / script
        if not path.exists():
            failures.append(f"missing hook script: .codex/hooks/{script}")
        elif "hookSpecificOutput" not in _read(path):
            failures.append(f".codex/hooks/{script} missing hookSpecificOutput")

    scheduler_path = root / "scripts" / "agent_scheduler.py"
    if not scheduler_path.exists():
        failures.append("missing script: scripts/agent_scheduler.py")
    else:
        failures.extend(_require_markers(_read(scheduler_path), [
            "multi_window_coordination.v1",
            "daemon",
            "pretool-check",
            "scheduler-unavailable",
            "permission_mode=bypassPermissions",
            "record-reserve",
            "stale-reap",
        ], "scripts/agent_scheduler.py"))
    scheduler_tests = root / "tests" / "scaffold_audits" / "test_agent_scheduler.py"
    if not scheduler_tests.exists():
        failures.append("missing scheduler tests: tests/scaffold_audits/test_agent_scheduler.py")
    else:
        failures.extend(_require_markers(_read(scheduler_tests), [
            "test_five_windows_can_hold_disjoint_write_claims",
            "test_sixth_window_is_deterministically_rejected_or_queued",
            "test_overlapping_write_claim_is_rejected",
            "test_read_claim_warns_when_active_write_exists",
            "test_stale_lease_expiry_records_reap_event",
            "test_dirty_baseline_overlap_emits_warning_and_ack_field",
            "test_concurrent_task_log_and_handoff_reservations_are_unique",
            "test_bypass_permissions_hook_path_is_advisory_only",
            "test_pretool_check_daemon_unavailable_fallback_is_advisory",
        ], "tests/scaffold_audits/test_agent_scheduler.py"))

    classifier_path = root / "scripts" / "agent_process_classifiers.py"
    contracts_path = root / "scripts" / "agent_process_contracts.py"
    classifier_tests = root / "tests" / "scaffold_audits" / "test_agent_process_classifiers.py"
    if not classifier_path.exists():
        failures.append("missing script: scripts/agent_process_classifiers.py")
    else:
        failures.extend(_require_markers(_read(classifier_path), [
            "stdlib-only",
            "ClassificationResult",
            "classify_shell_command",
            "classify_tool",
            "is_mutating_tool",
            "is_live_tier3_tool",
            "is_shell_read_only_command",
            "ROUTING_PATTERNS",
            "TIER3_AUTH_PATTERNS",
            "MUTATION_CLAIM_RE",
            "footer_semantic_failure",
            "publication",
            "destructive_git",
            "redirection_or_tee",
        ], "scripts/agent_process_classifiers.py"))
    if not contracts_path.exists():
        failures.append("missing script: scripts/agent_process_contracts.py")
    else:
        failures.extend(_require_markers(_read(contracts_path), [
            "stdlib-only",
            "CONTRACT_IDS",
            "ROUTING_PACKET",
            "PROCESS_CHECKLIST",
            "SUBAGENT_BOUNDARY",
            "BYPASS_ADVISORY",
            "LIFECYCLE_MARKERS",
            "SUBAGENT_STANDING_AUTHORIZATION",
            "pretool_missing_triage_message",
        ], "scripts/agent_process_contracts.py"))
    if not classifier_tests.exists():
        failures.append("missing classifier tests: tests/scaffold_audits/test_agent_process_classifiers.py")
    else:
        failures.extend(_require_markers(_read(classifier_tests), [
            "test_read_only_shell_chains_are_not_mutating",
            "pwd && rg --files",
            "nl -ba AGENTS.md | sed",
            "git status --short",
            "test_mutating_shell_commands_are_detected",
            "test_live_tier3_commands_are_detected",
            "test_structured_classification_flags_risk_categories",
            "test_structured_classification_preserves_wrapper_compatibility",
            "test_validation_performed_is_not_a_mutation_claim",
        ], "tests/scaffold_audits/test_agent_process_classifiers.py"))
    for rel in [
        ".codex/hooks/user_prompt_submit_agent_process.py",
        ".codex/hooks/subagent_start_agent_process.py",
        ".codex/hooks/subagent_stop_agent_process.py",
        ".codex/hooks/pre_tool_use_agent_process.py",
        ".codex/admin/hooks/esp32_admin_policy.py",
    ]:
        hook_text = _read(root / rel)
        if rel.endswith("pre_tool_use_agent_process.py") or rel.endswith("esp32_admin_policy.py"):
            if "from agent_process_classifiers import" not in hook_text:
                failures.append(f"{rel} must import scripts/agent_process_classifiers.py")
        if "from agent_process_contracts import" not in hook_text:
            failures.append(f"{rel} must import scripts/agent_process_contracts.py")
        for duplicate_marker in ["MUTATING_SHELL_RE =", "READ_ONLY_SHELL_RE =", "LIVE_TIER3_COMMAND_RE ="]:
            if duplicate_marker in hook_text:
                failures.append(f"{rel} duplicates shared classifier marker: {duplicate_marker}")

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
    if admin_installer.exists():
        failures.extend(_require_markers(_read(admin_installer), [
            "--target-dir",
            "SUPPORT_SOURCES",
            "agent_process_classifiers.py",
            "agent_process_contracts.py",
            "target-dir:",
            "support:",
        ], ".codex/admin/install_admin_policy.py"))
    if admin_hook.exists():
        failures.extend(_require_markers(_read(admin_hook), [
            "HOOK_DIR",
            "ROOT / \"scripts\"",
            "agent_process_contracts",
        ], ".codex/admin/hooks/esp32_admin_policy.py"))

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
    failures.extend(_run_admin_installer_dry_run(root, "yolo-compatible"))
    failures.extend(_run_admin_installer_dry_run(root, "admin-strict"))
    failures.extend(_run_admin_installer_temp_smoke(root))

    failures.extend(_run_hook(
        root,
        "user_prompt_submit_agent_process.py",
        json.dumps({"hook_event_name": "UserPromptSubmit"}),
        "UserPromptSubmit",
        [
            "ESP32-GOV-v1",
            "SOV-v1",
            "LIFECYCLE-v1",
            "TIER3-CLOSED-v1",
            "standing user authorization",
            "Safe non-trivial Tier 1",
            "evidence need",
            "weighted no-P1/P2 quorum",
            "decision footer",
            "source records",
        ],
    ))
    failures.extend(_run_hook(
        root,
        "subagent_start_agent_process.py",
        json.dumps({"agent_type": "qa-validation-reviewer", "permission_mode": "read-only"}),
        "SubagentStart",
        [
            "standing user authorization",
            "explicit disjoint write scope",
            "role, weight, evidence",
            "wait_agent/close_agent",
            "bypassPermissions",
        ],
    ))
    failures.extend(_run_hook(
        root,
        "subagent_stop_agent_process.py",
        json.dumps({"hook_event_name": "SubagentStop"}),
        "SubagentStop",
        [
            "ESP32-GOV-v1",
            "inspect visible completed agents before replacements",
            "close completed/stale agents with close_agent",
            "close agents before fallback/final",
            "fallback is valid only after cleanup attempt",
            "bypassPermissions advisory only",
        ],
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
        ["verified facts", "assumptions", "unknowns", "owner role", "evidence need", "reviewer disposition", "Hooks are advisory"],
    ))
    for script, event_name in [
        ("user_prompt_submit_agent_process.py", "UserPromptSubmit"),
        ("subagent_start_agent_process.py", "SubagentStart"),
        ("subagent_stop_agent_process.py", "SubagentStop"),
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
        "../.agents/TASK_LOG/0089-multi-agentic-continuous-enforcement.md",
        "../.agents/handoffs/0078-multi-agentic-continuous-enforcement-to-qa.md",
        "../knowledge-base/source-ledger/2026-05-29-multi-agentic-continuous-enforcement.md",
        "../.agents/TASK_LOG/0126-subagent-lifecycle-cleanup.md",
        "../.agents/handoffs/0092-subagent-lifecycle-cleanup-to-qa-tooling.md",
        "../knowledge-base/source-ledger/2026-06-01-subagent-lifecycle-cleanup.md",
        "../.agents/TASK_LOG/0137-always-on-subagent-process-enforcement.md",
        "../.agents/handoffs/0101-always-on-subagent-process-enforcement-to-qa-tooling.md",
        "../knowledge-base/source-ledger/2026-06-02-always-on-subagent-process-enforcement.md",
        "../.agents/TASK_LOG/0144-agent-instruction-skill-hook-ci-hardening.md",
        "../.agents/handoffs/0105-agent-instruction-skill-hook-ci-hardening-to-qa-tooling.md",
        "../knowledge-base/source-ledger/2026-06-02-agent-instruction-skill-hook-ci-hardening.md",
        "../.agents/TASK_LOG/0145-agent-process-hardening-production-refactor.md",
        "../.agents/handoffs/0106-agent-process-hardening-production-refactor-to-qa-tooling.md",
        "../knowledge-base/source-ledger/2026-06-02-agent-process-hardening-production-refactor.md",
        "prompt/admin-strict-codex-enforcement.md",
        "prompt/comprehensive-bench-development-process.md",
        "../.agents/TASK_LOG/0120-comprehensive-bench-development-process.md",
        "../knowledge-base/source-ledger/2026-05-31-comprehensive-bench-development-process.md",
        "prompt/multi-window-codex-scheduler.md",
        "../.agents/TASK_LOG/0125-multi-agent-cli-window-scheduler.md",
        "../knowledge-base/source-ledger/2026-06-01-multi-window-codex-scheduler.md",
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
        ".agents/TASK_LOG/0089-multi-agentic-continuous-enforcement.md",
        ".agents/handoffs/0078-multi-agentic-continuous-enforcement-to-qa.md",
        "knowledge-base/source-ledger/2026-05-29-multi-agentic-continuous-enforcement.md",
        ".agents/TASK_LOG/0126-subagent-lifecycle-cleanup.md",
        ".agents/handoffs/0092-subagent-lifecycle-cleanup-to-qa-tooling.md",
        "knowledge-base/source-ledger/2026-06-01-subagent-lifecycle-cleanup.md",
        ".agents/TASK_LOG/0137-always-on-subagent-process-enforcement.md",
        ".agents/handoffs/0101-always-on-subagent-process-enforcement-to-qa-tooling.md",
        "knowledge-base/source-ledger/2026-06-02-always-on-subagent-process-enforcement.md",
        ".agents/TASK_LOG/0144-agent-instruction-skill-hook-ci-hardening.md",
        ".agents/handoffs/0105-agent-instruction-skill-hook-ci-hardening-to-qa-tooling.md",
        "knowledge-base/source-ledger/2026-06-02-agent-instruction-skill-hook-ci-hardening.md",
        ".agents/TASK_LOG/0145-agent-process-hardening-production-refactor.md",
        ".agents/handoffs/0106-agent-process-hardening-production-refactor-to-qa-tooling.md",
        "knowledge-base/source-ledger/2026-06-02-agent-process-hardening-production-refactor.md",
        ".agents/TASK_LOG/0119-development-agent-panel.md",
        "knowledge-base/source-ledger/2026-05-31-development-agent-panel.md",
        ".agents/TASK_LOG/0120-comprehensive-bench-development-process.md",
        "docs/prompt/comprehensive-bench-development-process.md",
        "knowledge-base/source-ledger/2026-05-31-comprehensive-bench-development-process.md",
        ".agents/TASK_LOG/0125-multi-agent-cli-window-scheduler.md",
        "docs/prompt/multi-window-codex-scheduler.md",
        "knowledge-base/source-ledger/2026-06-01-multi-window-codex-scheduler.md",
    ]:
        path = root / rel
        if not path.exists():
            failures.append(f"missing record: {rel}")

    bench_process = _read(root / "docs/prompt/comprehensive-bench-development-process.md")
    failures.extend(_require_markers(bench_process, [
        "bench_state_packet.v1",
        "PF0530L",
        "COM6",
        "serial/menu physical interaction accepted on retry",
        "`ENC_RAW`",
        "`ENC_EV`",
        "`BBS_MENU_STEP`",
        "`BBS_MENU_SELECT`",
        "LCD visual/glyph readability",
        "hardware/electrical acceptance",
        "XBee",
        "relay",
        "ESP-NOW/BBS/CBBS",
        "SoftAP/browser",
        "does not authorize live hardware access",
        "flashing",
        "serial monitor",
        "RF transmit",
        "relay control",
        "GitHub publication",
    ], "comprehensive bench process"))

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
