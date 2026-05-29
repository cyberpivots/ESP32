#!/usr/bin/env python3
"""Evaluate ESP32 weighted reviewer votes and continuation decisions.

This helper is intentionally repo-local and side-effect free. It reads a JSON
packet, computes the weighted quorum result, and emits the next process action.
It does not install hooks, mutate devices, or enforce machine-wide policy.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DECISIONS = {"continue", "ready_for_mutation", "ask_user", "blocked", "handoff"}
VALID_VOTES = {"approve", "approve_with_conditions", "reject", "abstain"}
APPROVAL_VOTES = {"approve", "approve_with_conditions"}
VALID_WEIGHTS = {1, 2, 3, 5}
ROLE_WEIGHTS = {
    "coordinator": 5,
    "architecture-risk": 5,
    "architecture risk": 5,
    "agent operations": 3,
    "communications": 3,
    "evidence": 3,
    "evidence auditor": 3,
    "hardware": 3,
    "live-bench": 3,
    "live bench": 3,
    "qa": 3,
    "qa validation": 3,
    "tooling": 3,
    "kb curator": 2,
    "prompt-token triage": 2,
    "source-skill curator": 2,
    "helper": 1,
    "low-risk helper": 1,
}
TIER3_REQUIRED = {
    "explicitLiveGateAuthority": "explicit live-gate authority",
    "sameSessionEvidence": "same-session evidence",
    "recoveryPath": "recovery path",
    "reviewerQuorum": "reviewer quorum",
    "closedSurfaceReview": "closed-surface review",
}


def _normalize(value: Any) -> str:
    return str(value or "").strip().lower()


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _meaningful_findings(value: Any) -> list[str]:
    findings: list[str] = []
    for item in _as_list(value):
        text = str(item).strip()
        if not text:
            continue
        if _normalize(text) in {"none", "no", "n/a", "na", "no p1/p2 blockers"}:
            continue
        findings.append(text)
    return findings


def _vote_role(vote: dict[str, Any]) -> str:
    return _normalize(vote.get("role"))


def _resolve_weight(vote: dict[str, Any]) -> tuple[int | None, str | None]:
    raw_weight = vote.get("weight")
    if raw_weight is not None:
        try:
            weight = int(raw_weight)
        except (TypeError, ValueError):
            return None, f"invalid weight for role {vote.get('role')!r}"
        if weight not in VALID_WEIGHTS:
            return None, f"unsupported weight {weight} for role {vote.get('role')!r}"
        return weight, None

    role_class = _normalize(vote.get("roleClass"))
    role = _vote_role(vote)
    for key in (role_class, role):
        if key in ROLE_WEIGHTS:
            return ROLE_WEIGHTS[key], None
    return None, f"unknown weight for role {vote.get('role')!r}"


def _item_description(item: Any) -> str:
    if isinstance(item, dict):
        return str(item.get("description") or item.get("name") or item)
    return str(item)


def _evaluate_next_decision(
    approved: bool,
    errors: list[str],
    blockers: list[str],
    missing_roles: list[str],
    missing_tier3: list[str],
    evidence_gaps: list[Any],
    work_remaining: list[Any],
) -> str:
    action_items = [
        item for item in [*evidence_gaps, *work_remaining] if isinstance(item, dict)
    ]
    hard_items = [
        _item_description(item)
        for item in action_items
        if bool(item.get("hardBlocker"))
    ]
    human_items = [
        _item_description(item)
        for item in action_items
        if bool(item.get("requiresHuman")) and not bool(item.get("automatable"))
    ]
    automatable_items = [
        _item_description(item)
        for item in action_items
        if bool(item.get("automatable")) and not bool(item.get("hardBlocker"))
    ]

    if blockers or hard_items:
        return "blocked"
    fatal_errors = [
        error for error in errors
        if not error.startswith("missing required roles:")
        and not error.startswith("missing Tier 3 prerequisites:")
    ]
    if fatal_errors:
        return "blocked"
    if human_items and not automatable_items:
        return "ask_user"
    if automatable_items or missing_roles:
        return "continue"
    if missing_tier3:
        return "ask_user" if any("evidence" in item for item in missing_tier3) else "blocked"
    if errors:
        return "blocked"
    if approved:
        return "ready_for_mutation"
    return "blocked"


def evaluate_packet(packet: dict[str, Any]) -> dict[str, Any]:
    votes = packet.get("votes")
    required_roles = {_normalize(role) for role in _as_list(packet.get("requiredRoles")) if _normalize(role)}
    tier = _normalize(packet.get("tier"))
    threshold = float(packet.get("approvalThreshold", 0.70))
    errors: list[str] = []
    blockers: list[str] = []
    approval_weight = 0
    total_weight = 0
    present_roles: set[str] = set()
    normalized_votes: list[dict[str, Any]] = []

    if not isinstance(votes, list) or not votes:
        errors.append("votes must be a non-empty list")
        votes = []

    for index, raw_vote in enumerate(votes):
        if not isinstance(raw_vote, dict):
            errors.append(f"vote {index} must be an object")
            continue
        role = _vote_role(raw_vote)
        if not role:
            errors.append(f"vote {index} missing role")
            continue
        weight, weight_error = _resolve_weight(raw_vote)
        if weight_error:
            errors.append(weight_error)
            continue
        assert weight is not None
        vote_value = _normalize(raw_vote.get("vote"))
        if vote_value not in VALID_VOTES:
            errors.append(f"invalid vote {raw_vote.get('vote')!r} for role {raw_vote.get('role')!r}")
            continue
        p1 = _meaningful_findings(raw_vote.get("p1Findings") or raw_vote.get("p1"))
        p2 = _meaningful_findings(raw_vote.get("p2Findings") or raw_vote.get("p2"))
        if p1:
            blockers.extend(f"{role} P1: {item}" for item in p1)
        if p2:
            blockers.extend(f"{role} P2: {item}" for item in p2)
        if vote_value == "reject":
            blockers.append(f"{role} rejected the gate")
        present_roles.add(role)
        total_weight += weight
        if vote_value in APPROVAL_VOTES:
            approval_weight += weight
        normalized_votes.append({
            "role": role,
            "weight": weight,
            "vote": vote_value,
            "p1Findings": p1,
            "p2Findings": p2,
            "conditions": _as_list(raw_vote.get("conditions")),
            "confidence": raw_vote.get("confidence"),
        })

    missing_roles = sorted(required_roles - present_roles)
    if missing_roles:
        errors.append("missing required roles: " + ", ".join(missing_roles))

    approval_ratio = approval_weight / total_weight if total_weight else 0.0
    if total_weight and approval_ratio < threshold:
        errors.append(
            f"weighted approval {approval_ratio:.2f} below threshold {threshold:.2f}"
        )

    missing_tier3: list[str] = []
    if "3" in tier:
        prerequisites = packet.get("tier3Prerequisites")
        if not isinstance(prerequisites, dict):
            prerequisites = {}
        for key, label in TIER3_REQUIRED.items():
            if prerequisites.get(key) is not True:
                missing_tier3.append(label)
        if missing_tier3:
            errors.append("missing Tier 3 prerequisites: " + ", ".join(missing_tier3))

    evidence_gaps = _as_list(packet.get("evidenceGaps"))
    work_remaining = _as_list(packet.get("workRemaining"))
    approved = not errors and not blockers
    decision = _evaluate_next_decision(
        approved,
        errors,
        blockers,
        missing_roles,
        missing_tier3,
        evidence_gaps,
        work_remaining,
    )

    return {
        "ok": True,
        "decision": decision,
        "gatePasses": approved,
        "approvalWeight": approval_weight,
        "totalWeight": total_weight,
        "approvalRatio": round(approval_ratio, 4),
        "threshold": threshold,
        "requiredRoles": sorted(required_roles),
        "presentRoles": sorted(present_roles),
        "missingRoles": missing_roles,
        "missingTier3Prerequisites": missing_tier3,
        "errors": errors,
        "blockers": blockers,
        "votes": normalized_votes,
        "nextActions": [
            _item_description(item)
            for item in [*evidence_gaps, *work_remaining]
            if _item_description(item).strip()
        ],
    }


def template_packet() -> dict[str, Any]:
    return {
        "gate": "example-tier2-governance-change",
        "tier": "Tier 2",
        "approvalThreshold": 0.70,
        "requiredRoles": ["coordinator", "qa"],
        "tier3Prerequisites": {
            "explicitLiveGateAuthority": False,
            "sameSessionEvidence": False,
            "recoveryPath": False,
            "reviewerQuorum": True,
            "closedSurfaceReview": False,
        },
        "votes": [
            {
                "role": "coordinator",
                "vote": "approve",
                "evidenceReviewed": ["AGENTS.md", ".agents/GOVERNANCE.md"],
                "p1Findings": [],
                "p2Findings": [],
                "conditions": ["stay inside the named mutation boundary"],
                "confidence": "high",
            },
            {
                "role": "qa",
                "vote": "approve_with_conditions",
                "evidenceReviewed": ["tests/scaffold_audits"],
                "p1Findings": [],
                "p2Findings": [],
                "conditions": ["run focused and scaffold validation"],
                "confidence": "medium",
            },
        ],
        "evidenceGaps": [
            {
                "description": "Run focused unit tests",
                "automatable": True,
                "requiresHuman": False,
                "hardBlocker": False,
            }
        ],
        "workRemaining": [],
    }


def _load_packet(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise SystemExit(f"failed to read packet: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON packet: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("packet must be a JSON object")
    return data


def command_template(args: argparse.Namespace) -> int:
    print(json.dumps(template_packet(), indent=2, sort_keys=True))
    return 0


def command_evaluate(args: argparse.Namespace) -> int:
    record = evaluate_packet(_load_packet(args.packet))
    print(json.dumps(record, indent=2 if args.json else None, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    template = subparsers.add_parser("template", help="emit an example decision packet")
    template.add_argument("--json", action="store_true", help="accepted for consistency")
    template.set_defaults(func=command_template)

    evaluate = subparsers.add_parser("evaluate", help="evaluate a decision packet")
    evaluate.add_argument("--packet", required=True, type=Path)
    evaluate.add_argument("--json", action="store_true")
    evaluate.set_defaults(func=command_evaluate)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
