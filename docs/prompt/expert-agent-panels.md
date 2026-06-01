# Expert Agent Panels

## Source basis

This guidance references `SRC-OPENAI-LATEST-MODEL`,
`SRC-OPENAI-REASONING`, `SRC-CODEX-SUBAGENTS`,
`SRC-CODEX-CONFIG-REFERENCE`, and
`SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-05-19`. The default workspace
multi-agent process also references `SRC-CODEX-HOOKS-2026-05-27`,
`SRC-CODEX-SUBAGENTS-2026-05-27`,
`SRC-CODEX-CONFIG-REFERENCE-2026-05-27`,
`SRC-OPENAI-AGENTS-SDK-2026-05-27`,
`SRC-OPENAI-AGENTS-ORCHESTRATION-2026-05-27`,
`SRC-ANTHROPIC-MULTI-AGENT-RESEARCH-2026-05-27`,
`SRC-LANGCHAIN-HANDOFFS-2026-05-27`, and
`SRC-LANGCHAIN-CONTEXT-ENGINEERING-2026-05-27`.

## Intent

Use the global `$expert-agent-panels` skill when a task needs a specialist
review loop that can inspect workspace truth, inventory skills, close knowledge
gaps, perform source-backed research, choose a bounded next action, validate
the result, and update durable records.

This workspace now uses the same role-lens discipline for every prompt.
Project-local read-only subagents are default-authorized for safe Tier 2 and
Tier 3 reviewer quorum, while mutating workers still require explicit disjoint
write scopes. Every non-trivial prompt is classified by tier, owner, evidence
need, mutation boundary, and validation plan before mutation.
Agent lifecycle cleanup is part of the panel contract: inspect completed agents
before spawning, close completed/stale agents after capturing their output,
close agents before fallback/final decisions, and record fallback only after
cleanup attempt. This is an operational parent-agent duty; hooks can remind but
cannot guarantee Codex runtime slot release.
Managed-hook profiles from `.codex/admin/` can cover supported Codex hook
events on this machine, while the project-local hooks remain advisory aids.
The default managed profile is yolo-compatible and must not override a
user-launched `codex --yolo` session; admin-strict is explicit opt-in only.

## Verified facts

- As of the source access date in `knowledge-base/source-index.md`, official
  OpenAI model guidance identifies `gpt-5.5` as the current latest model and
  describes `medium` reasoning as the balanced default for GPT-5.5.
- Official reasoning guidance lists `low`, `medium`, `high`, and `xhigh`
  reasoning effort as workload-tuning levels and reserves higher effort for
  harder, higher-value, or longer-running work.
- Official Codex subagent guidance says Codex uses built-in `default`,
  `worker`, and `explorer` agents; this workspace default-authorizes
  project-local read-only reviewers for Tier 2 and Tier 3 quorum when tools are
  available and safe.
- Official Codex configuration guidance documents project/user config,
  `skills.config`, and agent settings; the global panel skill remains usable
  without project-local agents, while this workspace now also exposes
  project-local `.codex/agents/*.toml` profiles for repeatable ESP32 panel
  roles.
- The verified local skill inventory for this pass uses plugin cache hash
  `eed16198`; older plugin cache hashes are stale for this session.
- Current Codex hooks guidance documents project-local hooks, `UserPromptSubmit`,
  `SubagentStart`, and `PreToolUse`, but also states that non-managed command
  hooks require review/trust and that `PreToolUse` interception is incomplete.
- Current Codex managed-configuration guidance documents
  `/etc/codex/requirements.toml`, managed hooks, `allow_managed_hooks_only`,
  and restrictive command prefix rules for admin-enforced requirements.
- Current OpenAI Agents SDK guidance separates handoffs from manager-style
  agents-as-tools workflows and recommends adding specialists only when the
  contract materially changes.
- Current Anthropic and LangChain guidance supports bounded delegation,
  explicit context strategy, cost awareness, and careful handoff/context
  handling rather than automatic fan-out for every prompt.

## Assumptions

- The skill is installed under `/home/cyber/.codex/skills/` so future Codex
  sessions can discover it globally.
- ESP32 workspace records capture the project-specific prompt routing and
  source evidence, but no firmware, hardware, relay, radio, or framework
  behavior changes are implied by this prompt.

## Unknowns

- Future sessions may expose additional skills, plugins, MCP servers, or
  subagent types. Run a fresh inventory before relying on the list in this
  document.
- Project-local hooks may be skipped until reviewed and trusted by the active
  Codex runtime.

## Default prompt tiers

- Tier 0: coordinator triage plus local role lens.
- Tier 1: coordinator plus relevant owner and QA lens.
- Tier 2: read-only reviewer quorum before mutation; no-P1/P2 quorum may
  accept only the named gate and mutation boundary.
- Tier 3: explicit gate authority, same-session evidence, recovery path, and
  reviewer quorum before mutation; no-P1/P2 quorum cannot waive live-gate
  prerequisites.
- Weighted veto: required roles must be present, approval weight must be at
  least 70 percent, and no P1/P2 blockers may remain. Tier 3 prerequisites
  cannot be waived by weights.
- Missing evidence is a continuation condition when safe evidence collection
  remains. Use `scripts/agent_process_decision.py` to turn weighted reviewer
  records into `continue`, `ask_user`, `blocked`, `ready_for_mutation`, or
  `handoff` without prematurely ending a gate, and record agent lifecycle
  cleanup before any fallback or final decision.

## Prompt pattern

```text
Use $expert-agent-panels to run an expert panel review and improvement loop for
this task. Read the workspace contract first, inventory available skills,
separate verified facts from assumptions and unknowns, use official or primary
sources for missing facts, spawn project-local read-only subagents by default
for safe Tier 2 and Tier 3 quorum, then implement the best bounded action and
validate it.
```

## Default multi-agentic process prompt

```text
Apply the ESP32 default-multi-agentic-process. Classify the prompt as Tier 0,
Tier 1, Tier 2, or Tier 3; state verified facts, assumptions, unknowns, owner
role, evidence need, mutation boundary, reviewer quorum, gate authority,
validation plan, and trust boundary before non-trivial mutation; use
project-local read-only subagents by default for safe Tier 2 and Tier 3 quorum;
inspect completed agents before spawning, close completed/stale agents after
reviewer output is captured, use fallback only after cleanup attempt, use
mutating workers only with explicit disjoint write scopes; end with a
decision footer naming the next gate, owner, evidence, validation, durable
records, approved mutation boundary, and authority limits.
```

## Expected output

- Workspace map and active contract.
- Skill inventory marked relevant, conditional, or irrelevant.
- Knowledge gaps with source or probe paths.
- Source-backed findings.
- Implementation or no-mutation recommendation.
- Validation evidence.
- Source-index, source-ledger, prompt-registry, and task-log updates when the
  workspace contract requires durable records.

## Development-agent-panel

Use `development-agent-panel` when a task needs automated research and
development routing across ESP32 firmware, LCD/UI, XBee/radio, CBBS, tooling,
records, safety, and release lanes. The panel reduces routine human
interruption by giving read-only specialists default evidence-gathering work,
while keeping mandatory human gates for live hardware, flashing, serial writes,
RF transmit, relay control, persistent settings, credentials, destructive
operations, external services, GitHub publication, and safety-critical
decisions.

| Role | Agent profile | Default output | Stop gate |
| --- | --- | --- | --- |
| Panel coordinator / governance architect | `development-panel-coordinator` | Routing packet, quorum summary, decision footer | Missing quorum, P1/P2 blocker, unclear authority, Tier 3 surface |
| Workspace cartographer | `governance-cartographer` | Repo map, ownership, docs/source coverage | Unsupported factual claim or scope drift |
| LCD menu and display systems | `lcd-menu-ux-reviewer` | LCD/glyph/browser host findings | Live display, serial, flash, relay, RF, or browser-live claim |
| ESP32 firmware and device development | `esp32-firmware-device-reviewer` | Firmware boundary and no-flash validation plan | Framework drift, flash, monitor, serial write, runtime proof claim |
| XBee radio and protocol development | `xbee-radio-protocol-reviewer` | AT/API/profile and simulator/live gate review | WR/AC/API transmit, RF, profile write, serial radio action |
| UI/UX interface | `ui-ux-interface-reviewer` | Operator UI intent/action findings | UI command coupled to RF, relay, flash, serial, config, or external action |
| Source-backed research | `source-research-reviewer` | Source coverage, unresolved gaps, citation needs | Unsupported hardware/protocol/toolchain/safety claim |
| Code implementation | `bounded-implementation-worker` | Scoped patch and changed paths | Missing write scope, dirty-tree conflict, live action, commit/push |
| QA, testing, and evidence review | `qa-validation-reviewer` | Validation plan and acceptance findings | Missing tests, missing task record, unsupported acceptance |
| Database / data model / knowledge base | `data-model-kb-reviewer` | Schema, KB, migration, persistence findings | Persistent write, migration, secret handling, destructive data operation |
| Tooling and resource research | `tooling-resource-reviewer` | Safe command and resource-validation plan | System install, `/etc/codex` mutation, live device action |
| Off-grid communications domain expert | `offgrid-comms-domain-reviewer` | Field workflow and cross-transport risk findings | Coupled XBee/Wi-Fi/ESP-NOW/CBBS gates or assumed range/power proof |
| Security, safety, and risk reviewer | `security-safety-risk-reviewer` | Mandatory human gates and closed-surface risks | Credentials, destructive ops, live hardware, relay/load/mains |
| DevEx / CI / release automation | `devex-ci-release-reviewer` | CI/release reproducibility and publication gate findings | GitHub publication, release, external service, secret-backed workflow |
| Hardware bench gate reviewer | `live-bench-gate-reviewer` | Same-session live-gate evidence review | Missing identity, recovery path, manifest, closed-surface proof |
| Knowledge-base and prompt-registry curator | `kb-prompt-registry-curator` | Durable-record and prompt-registry findings | Missing source coverage, missing task log, unscoped source-index update |
| Protocol / bridge ABI reviewer | `protocol-bridge-abi-reviewer` | Schema, ABI, bounds, unsafe-action separation | Firmware/serial/bridge ABI change without gate |
| Power / wiring / isolation reviewer | `power-wiring-isolation-reviewer` | Power, voltage, boot-pin, isolation, wiring risks | Physical bench, wiring, relay/load/mains, battery/solar action |

Each new panel profile is read-only by default and defines purpose, inputs,
outputs, read scope, later mutation scope if separately authorized, stop
conditions, escalation conditions, required evidence before action, validation
method, and tier boundaries. Mutating work still routes through existing worker
profiles with explicit disjoint write scopes.

## Orchestration model

1. `development-panel-coordinator` classifies the prompt and names the owner,
   evidence need, mutation boundary, reviewer quorum, validation plan, and
   trust boundary.
2. Read-only specialists gather only the evidence needed for the selected
   boundary. The coordinator avoids broad fan-out when one local lookup is
   enough.
3. The quorum is reduced with the weighted-veto rule. Missing automatable
   evidence routes to continued evidence gathering; one irreducible physical or
   authority fact routes to `ask_user`; P1/P2 blockers or hard safety limits
   block the gate.
4. Approved Tier 1 or Tier 2 edits use a bounded worker or direct parent edit
   inside the named scope. Tier 3 remains closed until explicit live authority,
   same-session evidence, recovery path, and closed-surface review exist.
5. The final answer records validation, durable records, and authority limits.
