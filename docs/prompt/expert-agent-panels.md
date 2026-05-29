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
  `skills.config`, and agent settings; this workspace does not need a
  project-scoped `.codex/agents/*.toml` file for the v1 panel skill.
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
use mutating workers only with explicit disjoint write scopes; end with a
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
