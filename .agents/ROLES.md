# Agent Roles

## Coordinator

Classifies every prompt by tier, owner, evidence need, mutation boundary, and
validation plan. Project-local read-only subagents are mandatory to attempt
for safe non-trivial Tier 1 mutation and Tier 2/Tier 3 reviewer quorum when
tools are available and safe, and local role lenses are used only when
subagents are unavailable, unsafe, or blocked by higher-priority tool policy
after agent lifecycle cleanup. The
coordinator inspects completed agents before spawning when lifecycle state is
visible, waits for reviewer results, closes completed/stale agents, and records
fallback only after cleanup attempt.

## Agent Operations

Maintains prompt governance, project-local Codex profiles, hook guidance, task
records, yolo-compatible and admin-strict Codex requirements templates,
managed hook policy, mandatory subagent-attempt guidance, agent lifecycle
cleanup guidance, and handoffs for multi-agent workflows.

## Architect

Maintains architecture documents, ADRs, interface boundaries, and system-level
tradeoffs.

## Firmware

Implements firmware only after framework and board decisions are accepted.
Maintains board abstractions, drivers, and protocol integration code.

## Hardware

Maintains hardware profiles, power notes, pin-risk matrices, bench constraints,
and verified source coverage.

## Communications

Maintains wired, wireless, and custom protocol contracts and test scenarios.

## QA

Maintains verification scripts, test plans, reviewer quorum records, acceptance
gates, hook-trust follow-up, lifecycle cleanup evidence, continuation-decision
evidence, and reproducible evidence artifacts.

## Tooling

Maintains managed-profile installer/validator behavior, stable permissions,
backup and rollback checks, installed hash records, operator-sovereignty
audits, agent scheduler and lifecycle-cleanup fixtures, and direct managed-hook
fixture validation.

## Release

Maintains changelog, release notes, GitHub workflow readiness, and packaging
criteria.
