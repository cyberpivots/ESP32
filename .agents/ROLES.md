# Agent Roles

## Coordinator

Classifies every prompt by tier, owner, evidence need, mutation boundary, and
validation plan. Runs local role lenses when subagents are unavailable or unsafe.

## Agent Operations

Maintains prompt governance, project-local Codex profiles, hook guidance, task
records, and handoffs for multi-agent workflows.

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
gates, hook-trust follow-up, and reproducible evidence artifacts.

## Release

Maintains changelog, release notes, GitHub workflow readiness, and packaging
criteria.
