# Instruction Surface Map

This map identifies where ESP32 workspace operating rules live and what each
surface can and cannot enforce.

## Contract IDs

| ID | Meaning | Canonical surface |
| --- | --- | --- |
| `ESP32-GOV-v1` | Tiered coordinator triage, owner routing, evidence boundary, and validation packet. | `AGENTS.md`, `.agents/GOVERNANCE.md`, `docs/agent-coordination.md` |
| `SOV-v1` | Operator sovereignty for `codex --yolo`, `danger-full-access`, `approval_policy=never`, and `permission_mode=bypassPermissions`. | `AGENTS.md`, `.agents/GOVERNANCE.md`, `.codex/admin/README.md` |
| `LIFECYCLE-v1` | Tier 2/Tier 3 reviewer lifecycle cleanup: collect output, use `wait_agent`, close reviewers, and record fallback. | `AGENTS.md`, `docs/agent-coordination.md` |
| `TIER3-CLOSED-v1` | Live bench, flash, serial-write, RF/XBee write, relay/load/mains, release, and other closed surfaces require explicit gate authority. | `AGENTS.md`, `docs/risk-and-safety.md` |

## Surfaces

| Surface | Role | Enforcement status |
| --- | --- | --- |
| `AGENTS.md` | Canonical workspace operating contract loaded by Codex instruction discovery. | Authoritative project instruction surface. |
| `.agents/GOVERNANCE.md`, `.agents/OWNERSHIP.md`, `.agents/ROLES.md` | Policy, owner map, and role responsibilities required before edits. | Authoritative repo governance records. |
| `.codex/agents/*.toml` | Project-local custom reviewer and worker profiles that inherit the canonical contract, including standing user authorization for read-only subagent use. | Instruction surface for spawned agents; read-only or scoped-write by profile. |
| `.codex/hooks.json` and `.codex/hooks/*.py` | Advisory reminders for prompt routing, standing subagent authorization, pre-tool mutation triage, subagent boundaries, and lifecycle cleanup. | Trust-gated project hooks; advisory, especially under `bypassPermissions`. |
| `.codex/admin/requirements.toml` and `.codex/admin/profiles/yolo-compatible/requirements.toml` | Repo source templates for yolo-compatible managed hooks. | Not installed by default; must not constrain yolo permissions. |
| `.codex/admin/profiles/admin-strict/requirements.toml` | Optional strict managed profile that may block yolo semantics. | Explicit opt-in only after the user asks for `admin-strict` by name. |
| `.codex/admin/hooks/esp32_admin_policy.py` plus `scripts/agent_process_classifiers.py` and `scripts/agent_process_contracts.py` | Source files for the managed hook and its stdlib-only support modules. | Installed together only by explicit installer action; temp `--target-dir` validation is host-only and does not touch `/etc/codex`. |
| `.codex/skills/*/SKILL.md` | Repo-local reusable workflows for ESP32 live gates, LCD menu work, Win31 vision review, and XBee radio integration. | Skill routing surface; audited for frontmatter/config path consistency. |
| `docs/prompt/*.md` and `knowledge-base/prompt-registry.md` | Prompt process records and reusable prompt guidance. | Advisory documentation and source-backed prompt registry. |
| `scripts/scaffold_audit_*.py` and `scripts/verify_scaffold.py` | Static checks for path, source, docs, firmware, Pages, agent-process, skill, and durable-record contracts. | Validation surface; host-only and repo-local. |
| `.agents/TASK_LOG/*.md` | Durable task records with triage, scope, validation, authority limits, and decision footers. | Required for non-trivial work. |
| `.agents/handoffs/*.md` | Continuation records when another owner needs to review or continue work. | Required when next ownership is not closed in the same task. |
| `knowledge-base/source-index.md` and `knowledge-base/source-ledger/*.md` | Source IDs and concise verified ledgers for factual changes. | Source-backed evidence surface; unresolved gaps must stay explicit. |
| `.github/workflows/scaffold-ci.yml` | Non-deploy PR/manual validation for scaffold audits and host tests. | CI validation only; no publish authority. |
| `.github/workflows/pages.yml` | Main/manual Pages build and deployment for the curated public artifact. | Deploys only the curated artifact after validation; no PR deployment. |

## Publication Boundary

No commit, push, PR creation, branch deletion, rebase/reset, release, Pages
setting change, or external publication is authorized by these surfaces alone.
Use `scripts/git_publication_hygiene.py check --json` for a read-only report,
then require explicit user authority and dirty-tree proof before any GitHub or
history mutation.
