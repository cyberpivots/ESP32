# Prompt Triage

## Goal

Route work requests to the smallest reliable agent/profile that can complete the
task while preserving evidence and validation requirements.

## Triage dimensions

- task type: research, architecture, firmware, hardware, QA, GitHub, release,
- risk level: low, medium, high,
- evidence need: none, local, web, physical bench,
- mutation scope: read-only, docs, code, hardware,
- required owner role.

## Routing rule

If a task touches live hardware, firmware flashing, power wiring, relays, or
radio configuration, route to high-rigor review and require a task-specific
bench plan.

