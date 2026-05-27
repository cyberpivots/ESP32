# Prompt Registry

| Prompt | Intent | Output | Risk |
| --- | --- | --- | --- |
| research-source-backed | Fill a knowledge gap using verified sources only. | Source ledger and updated profile. | Medium |
| firmware-implementation | Implement approved firmware behavior after ADR. | Code, tests, validation note. | High |
| hardware-bench-plan | Plan wiring, power, flash, and recovery for a device. | Bench checklist and risk log. | High |
| review-evidence-gate | Review source coverage and assumptions. | Findings and required fixes. | Medium |
| expert-agent-panel-loop | Run a specialist review loop with skill inventory, source-backed gap closure, bounded action selection, validation, and durable record updates. | Panel synthesis, implementation or no-mutation decision, validation evidence, and knowledge-record updates. | Medium |
| default-multi-agentic-process | Classify every ESP32 workspace prompt by tier, owner role, evidence need, mutation boundary, reviewer quorum, gate authority, and validation plan before non-trivial mutation. | Verified facts, assumptions, unknowns, selected tier, owner role, evidence need, mutation boundary, validation plan, validation evidence, continuation decision, and durable records when required. | Medium |
| continuation-decision-footer | Convert reviewer quorum findings into the next development decision without expanding authority beyond the named gate. | Decision, next gate or slice, owner role, evidence need, approved mutation boundary, validation command, required durable records, and authority limits. | Medium |
