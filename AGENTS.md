# Agent Operating Contract

This workspace supports multi-agent development for ESP32-based devices,
custom firmware, communication interfaces, and verified hardware integrations.

## Non-negotiable rules

- Do not make unverified hardware, protocol, toolchain, or wiring claims.
- Keep verified facts, assumptions, and unknowns in separate sections.
- Do not select Arduino, ESP-IDF, PlatformIO, or any other framework until an
  accepted ADR changes the framework-neutral status.
- Do not add source code that depends on a specific framework during the
  scaffold phase.
- Do not copy vendor PDFs or bulky source artifacts into the repository.
  Store source links and concise verified summaries instead.
- Hardware bring-up work must identify power, voltage, boot-pin, and isolation
  risks before recommending bench actions.

## Required reading before edits

1. `.agents/GOVERNANCE.md`
2. `.agents/OWNERSHIP.md`
3. `.agents/ROLES.md`
4. `docs/index.md`
5. `knowledge-base/source-index.md`

## Evidence rule

Any factual change under `hardware-profiles/`, `comm-protocols/`, `firmware/`,
or `docs/architecture/` must cite a source listed in
`knowledge-base/source-index.md`, or mark the item as an unresolved gap.

## Handoff rule

Each non-trivial task must leave a task record in `.agents/TASK_LOG/` and, when
another role needs to continue the work, a handoff in `.agents/handoffs/`.

