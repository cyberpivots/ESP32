# Agent Roles

## Coordinator

Classifies every prompt by tier, owner, evidence need, mutation boundary, and
validation plan. Project-local read-only subagents are default-authorized for
safe Tier 2 and Tier 3 reviewer quorum, and local role lenses are used when
subagents are unavailable or unsafe.

## Agent Operations

Maintains prompt governance, project-local Codex profiles, hook guidance, task
records, yolo-compatible and admin-strict Codex requirements templates,
managed hook policy, and handoffs for multi-agent workflows.

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
gates, hook-trust follow-up, continuation-decision evidence, and reproducible
evidence artifacts.

## Tooling

Maintains managed-profile installer/validator behavior, stable permissions,
backup and rollback checks, installed hash records, operator-sovereignty
audits, and direct managed-hook fixture validation.

## Release

Maintains changelog, release notes, GitHub workflow readiness, and packaging
criteria.
