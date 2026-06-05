# Task 0170: Whole Workspace Tools Research Backlog

Status: completed research loop; mutation backlog produced; scaffold-clean
claims deferred

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-05

Source IDs:
`SRC-LOCAL-DEVELOPMENT-AGENT-PANEL-2026-05-31`,
`SRC-LOCAL-MULTI-AGENTIC-CONTINUOUS-ENFORCEMENT-2026-05-29`,
`SRC-LOCAL-SUBAGENT-LIFECYCLE-CLEANUP-2026-06-01`,
`SRC-LOCAL-AGENT-INSTRUCTION-SKILL-HOOK-CI-HARDENING-2026-06-02`,
`SRC-LOCAL-CBBS-RNW-SPLIT-BUILD-INSTALL-LAUNCH-2026-06-04`,
`SRC-LOCAL-CBBS-HOST-COMMAND-BRIDGE-LIVE-GATE-BLOCKED-2026-06-04`,
`SRC-LOCAL-CBBS-XBEE-KNOWN-PROFILE-WRITE-GATE-BLOCKED-2026-06-04`,
`SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-DEBUG-METRO-INCIDENT-2026-06-04`

## Routing

- Verified facts: the user requested implementation of a planned 50-iteration
  whole-workspace tools research/analysis loop. `research/development-status-ledger.md`
  is the canonical planning-status ledger. `research/known-gaps.md` lists open
  high-priority hardware, RNW, XBee, and release gaps. The current worktree
  already contains RNW/product/docs/source-index changes and untracked Task
  0168/0169 records; those changes are outside this task.
- Assumptions: implementing the plan means running source-backed analysis and
  adding one durable backlog task record. It does not mean implementing backlog
  items, cleaning generated files, updating source indexes, updating docs index,
  or opening any live or release surface.
- Unknowns: whether Task 0169 should later gain docs-index/source-ledger/source-index
  linkage, whether retained RNW debug packages/windows/Metro state should be
  cleaned, and whether future hardware identity facts can be resolved without
  same-session physical inspection.
- Selected tier: Tier 2 whole-workspace tooling, evidence, QA, and governance
  research.
- Owner role: Agent Operations and Tooling with QA, Evidence Records,
  Security/Safety, RNW, XBee/radio, and hardware lenses.
- Evidence need: required governance docs, docs/source indexes, status/gap
  ledgers, recent task/source records, script/test inventory, read-only reviewer
  quorum, read-only audit commands, current scaffold-failure disposition, and
  this durable record.
- Mutation boundary: this task record only:
  `.agents/TASK_LOG/0170-whole-workspace-tools-research-backlog.md`. No source
  code, docs index, source index, source ledger, handoff, hook, generated-output
  cleanup, package, release, hardware, or external-service mutation is included.
- Reviewer quorum: read-only subagents were spawned, waited, their outputs were
  captured, and all spawned reviewers were closed. Coordinator, Tooling,
  Evidence, QA, and Security/Safety reviewers found no P1/P2 blocker to the
  one-record backlog mutation when scoped honestly. Reviewer conditions were:
  preserve dirty-tree boundaries, use a non-conflicting Task 0170 path, do not
  claim scaffold-clean, record stale skill inventory and RNW output blockers,
  and keep Tier 3 surfaces closed.
- Gate authority: records-only Tier 2 analysis. No Tier 3, runtime, release,
  cleanup, publication, or system-policy authority is opened.
- Trust boundary: repo-local analysis and advisory governance only; hooks remain
  advisory under bypassPermissions.

## Iteration Records

Each iteration records one source-backed improvement candidate. Priority is the
current backlog priority, not an implementation approval.

| Iteration | Lane | Priority | Backlog candidate | Evidence basis | Next validation |
| --- | --- | --- | --- | --- | --- |
| 01 | Governance | P1 | Add a lightweight task-log ID collision preflight before creating new records. | `.agents/TASK_LOG/`, `scripts/scaffold_audit_records.py`, reviewer quorum | New unit test plus `scripts/scaffold_audit_records.py` |
| 02 | Governance | P1 | Add a report-only task-log template/check for planning backlogs. | `scripts/scaffold_audit_records.py`, Task 0144 pattern | Focused durable-record audit fixture |
| 03 | Governance | P2 | Record parent lifecycle cleanup expectations in an auditable checklist field. | `.agents/GOVERNANCE.md`, `SRC-LOCAL-SUBAGENT-LIFECYCLE-CLEANUP-2026-06-01` | Agent-process audit update |
| 04 | Governance | P2 | Add a same-session reviewer-quorum summary format with weights and stale-context notes. | `docs/prompt/prompt-triage.md`, reviewer outputs | `scripts/scaffold_audit_agent_process.py` |
| 05 | Governance | P2 | Add explicit "plan implemented as analysis only" wording to backlog record guidance. | `AGENTS.md`, `scripts/scaffold_audit_records.py` | Record-audit fixture |
| 06 | Docs/Records | P1 | Decide Task 0169 discoverability: docs-index link only, or source-ledger/source-index follow-up. | Task 0169, `docs/index.md`, evidence auditor output | `scripts/scaffold_audit_records.py`; docs/source audits if touched |
| 07 | Docs/Records | P2 | Normalize older task/source cross-reference style where records are archival. | `docs/index.md`, source-ledger inventory | `scripts/scaffold_audit_docs.py` |
| 08 | Docs/Records | P2 | Add known-gap entries for stale skill inventory and RNW retained outputs if not fixed immediately. | `research/known-gaps.md`, audit results | Source/record audit |
| 09 | Docs/Records | P2 | Add a source-index unresolved-gap convention for task-log-only Tier 2 reports. | `knowledge-base/source-index.md`, Task 0169 | Source audit after separate mutation |
| 10 | Docs/Records | P3 | Add a short "current scaffold blockers" status table to the planning ledger. | `research/development-status-ledger.md`, current audits | Docs/source audit |
| 11 | RNW/CBBS | P0 | Create a bounded RNW cleanup gate for retained ignored `obj`, `bin`, `x64/Debug`, and AppX/AppPackages outputs. | Task 0166, Task 0169, `scaffold_audit_react_native.py` failure | Stop app/Metro if needed, cleanup gate, rerun RNW audit |
| 12 | RNW/CBBS | P0 | Refresh plugin/skill inventory paths from cache hash `2b564709` to current `9c1190e4`. | `scripts/scaffold_audit_skills.py` failure | `scripts/scaffold_audit_skills.py` |
| 13 | RNW/CBBS | P1 | Add an RNW audit failure summarizer that groups thousands of generated-output rows by root directory. | `scripts/scaffold_audit_react_native.py` 6030-line failure | Focused Python test and RNW audit |
| 14 | RNW/CBBS | P1 | Add a debug-review checklist that proves app-local Metro before Start menu/AppFolder review. | Task 0168, CBBS React Native README | Focused RNW docs/test audit |
| 15 | RNW/CBBS | P2 | Add package identity/capability acceptance backlog rows for split apps without treating debug identity as final. | Task 0166, CBBS React Native README | RNW source/record review |
| 16 | DOS-C/Win31 | P1 | Keep Gate H accepted proof separate from any new simulator/UI claims. | `research/development-status-ledger.md` | Task/source review before mutation |
| 17 | DOS-C/Win31 | P2 | Add a Win31 proof artifact index that distinguishes transcript, screenshot, OCR, and cleanup proof. | docs index, Gate H records | Docs/source audit |
| 18 | DOS-C/Win31 | P2 | Add an explicit SLIRP proof backlog item for Windows 3.1 operator console to simulator at `10.0.2.2:31331`. | `research/known-gaps.md` | Host-only proof gate |
| 19 | DOS-C/Win31 | P3 | Normalize visual-proof acceptance wording for no-redbox/no-loading RNW versus Win31 screenshot/CV proof. | Task 0166/0168, Win31 vision records | QA review |
| 20 | DOS-C/Win31 | P3 | Add cleanup-state checklist wording for retained local review windows versus accepted cleanup proof. | Task 0166/0168 | QA/source record review |
| 21 | Firmware/Protocol | P1 | Keep Gate F runtime implementation separate from accepted ABI/runtime requirements/prototype. | `research/development-status-ledger.md`, ADR-0006/0007/0008 | Firmware source audit |
| 22 | Firmware/Protocol | P1 | Add host-only firmware ABI regression matrix before any runtime firmware mutation. | Gate F records, protocol tests | Host-only tests |
| 23 | Firmware/Protocol | P2 | Add command-safety classification for scripts that can flash, monitor, or prepare live gates. | `scripts/espnow_bbs_live_gate.py`, `scripts/live_bench_preflight.py` | Tooling audit/test |
| 24 | Firmware/Protocol | P2 | Add no-live-surface smoke tests around offline portions of `live_bench_preflight.py`. | Security/tooling reviewer output | Python unit tests |
| 25 | Firmware/Protocol | P3 | Add exact protocol-contract status notes for simulator-only versus live serial ABI paths. | `docs/architecture/protocol-contract.md` | Docs/source audit |
| 26 | LCD/Input | P1 | Preserve PF0530L accepted electrical/glyph proof while keeping broader hardware acceptance closed. | `research/development-status-ledger.md` | Known-gap/source review |
| 27 | LCD/Input | P1 | Add current PF0530V/W status reconciliation so PCNT/source/build/live/user acceptance are easy to follow. | recent source ledgers/task inventory | Record audit |
| 28 | LCD/Input | P2 | Add host simulator tests for future menu XML/render viewport regressions before flash gates. | `tools/simulators/lcd_bbs_menu`, tests inventory | `tests/lcd_bbs_menu` |
| 29 | LCD/Input | P2 | Add a compact LCD proof taxonomy: serial proof, user visual proof, DMM proof, and physical interaction proof. | LCD task/source records | Docs/source audit |
| 30 | LCD/Input | P3 | Add source-backed constraints for any future encoder direction-label expectation changes. | `research/known-gaps.md` | Hardware/QA review |
| 31 | XBee/Radio | P0 | Keep known-profile writes blocked until same-session port identity, readback backup, voltage/isolation/antenna evidence, key handling, rollback, redaction, and cleanup exist. | Task 0165 | Tier 3 gate packet |
| 32 | XBee/Radio | P1 | Run only the explicitly read-only no-serial XBee inventory path in future analysis gates. | Tooling reviewer, `xbee_radio_study.py` | Inventory JSON, no serial flags |
| 33 | XBee/Radio | P1 | Add tests proving `xbee_radio_study.py inventory --json` does not open serial ports or send writes. | Tooling reviewer output | Python tests |
| 34 | XBee/Radio | P2 | Add optional-output guard tests for `xbee_read_only_probe.py` so artifacts stay under approved bench-record paths. | `scripts/xbee_read_only_probe.py` | Python tests |
| 35 | XBee/Radio | P2 | Clarify that XBee `at-query` style read commands still open serial and need explicit authority. | Security reviewer output | Docs/tooling audit |
| 36 | Hardware/Safety | P0 | Build source-backed power-entry/protection requirements for `four-relay-xbee-wifi` before bench action. | `research/known-gaps.md`, `docs/risk-and-safety.md` | Source-index-backed docs update |
| 37 | Hardware/Safety | P0 | Identify exact four-channel relay module manufacturer, polarity, voltage, current, isolation, and ratings before relay GPIO decisions. | `research/known-gaps.md` | Hardware source package |
| 38 | Hardware/Safety | P1 | Verify exact ESP32 board, USB-UART bridge, regulator, shield schematic, jumpers, and continuity for `four-relay-xbee-wifi`. | `research/known-gaps.md` | Bench record/source review |
| 39 | Hardware/Safety | P1 | Define relay driver stage only after module trigger/current/isolation evidence is accepted. | `research/known-gaps.md`, risk policy | Hardware review |
| 40 | Hardware/Safety | P2 | Add a bench instrument/fixture readiness checklist tied to `research/bench-records/TEMPLATE.md`. | `research/known-gaps.md` | QA/hardware audit |
| 41 | Validation/CI | P0 | Do not claim `verify_scaffold.py` clean until RNW generated outputs and stale skill inventory are fixed. | local audit results | `scripts/verify_scaffold.py` |
| 42 | Validation/CI | P1 | Improve `verify_scaffold.py` failure reporting so it names the failing audit groups before long detail output. | QA/tooling reviewer output | Focused test plus verify run |
| 43 | Validation/CI | P1 | Add a whole-workspace audit matrix command or doc that classifies each audit as read-only, repo-mutating, temp/state, live, or publication. | scripts inventory | Tooling tests |
| 44 | Validation/CI | P2 | Add a host-only research-backlog validation profile that excludes page generation and Tier 3 probes. | reviewer outputs | New audit/test gate |
| 45 | Validation/CI | P2 | Add dirty-tree boundary audit before future broad mutation so untracked task/source records are preserved. | publication hygiene output | `git_publication_hygiene.py` test |
| 46 | Release/Security | P0 | Keep commit, push, PR, release, package signing, Store/App Installer, and publication closed without exact user authority. | `scripts/git_publication_hygiene.py`, Task 0166 | Publication hygiene JSON |
| 47 | Release/Security | P1 | Add public-manifest redaction backlog for COM ports, MAC-like identifiers, local paths, hashes, private uploads, and bench records. | security reviewer output | `scripts/audit_public_manifest.py` |
| 48 | Release/Security | P1 | Keep `/etc/codex/requirements.toml` and `admin-strict` install closed unless explicitly requested by name. | `.agents/GOVERNANCE.md`, `.codex/admin/README.md` | Admin policy tests |
| 49 | Release/Security | P2 | Add a no-secret scan requirement to any future bridge, XBee, package, or publication evidence packet. | Task 0164/0165/0169 | Protocol/tooling tests |
| 50 | Release/Security | P2 | Add final acceptance wording that separates backlog completion from implementation, cleanup, and full scaffold acceptance. | this task, QA reviewer output | Durable-record audit |

## Ranked Mutation Backlog

P0:

- RNW scaffold-clean cleanup gate: stop retained app/Metro state as needed,
  remove only ignored generated RNW native build/package outputs under the
  split Windows `windows/` roots, then rerun
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`.
- Skill/plugin inventory refresh: update stale GitHub/Canva plugin cache paths
  from `2b564709` to current `9c1190e4`, with same-session inventory evidence,
  then rerun `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`.
- Do not claim full `scripts/verify_scaffold.py` success until both RNW and
  skill blockers are resolved.
- Keep HostCommandBridge live dispatch, XBee writes, relay/load/mains, flashing,
  signing, release, publication, and `/etc/codex` install closed without
  separate explicit gates.

P1:

- Add task-log collision preflight, report-only durable-record template checks,
  and dirty-tree boundary checks before broad future mutation.
- Improve RNW audit output summarization and RNW debug-review proof checklist.
- Add command-safety classifications for scripts that are read-only, repo
  mutating, temp/state mutating, serial-opening, flash-capable, or publication
  capable.
- Add XBee inventory no-serial/no-write tests and redaction/output guard tests.
- Build source-backed hardware identity, power, relay, and isolation evidence
  packages before any new bench action.

P2/P3:

- Normalize Task 0169 discoverability and decide whether its explicit
  task-log-only boundary should stand or receive a future source/index record.
- Add status tables for current scaffold blockers and recent PF0530V/W LCD
  evidence lineage.
- Add public-manifest redaction coverage and no-secret scan requirements for
  future bridge/radio/release evidence packets.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`
  passed before this task record was added.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 170`
  passed after this task record was added.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/git_publication_hygiene.py check --json`
  passed and reported the current dirty tree; publication remains closed.
- FAIL, backlog item: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`
  found stale plugin cache paths in `research/skills/available-skills.md`.
- FAIL, backlog item: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`
  found retained RNW native build/package output directories and files under
  split Windows native trees. The failure output is very large and should be
  summarized by a future tooling improvement.
- NOT CLAIMED: full `scripts/verify_scaffold.py` cleanliness, because the RNW
  and skill blockers above are current.

## Authority Limits

Still closed: source-code mutation, docs-index/source-index/source-ledger
mutation, generated-output cleanup, native HostCommandBridge implementation or
dispatch, shell or DOS-C execution, serial port open/write, RF/XBee/radio writes
or transmit, firmware flash/erase/monitor, relay/load/mains work, wiring,
BLE/Web Serial/Web Bluetooth, SoftAP or local-network discovery, signing
certificates, Store/App Installer association, package creation for
distribution, EAS, App Center, credentials/key material, runtime proof, commit,
push, PR, deploy, release, `/etc/codex/requirements.toml`, and `admin-strict`
installation.

## Handoff

No handoff is required for this report-only backlog. Future backlog items need
their own routing packets, reviewer quorum, mutation boundary, and validation.

## Decision

Decision: complete for the 50-iteration whole-workspace tools research/analysis
loop and backlog report. This task accepts only the backlog analysis and this
task-log record. It does not accept implementation of any backlog item, full
scaffold cleanliness, cleanup, live hardware, serial/RF action, release, or
publication.

## Decision Footer

Decision: complete. Next gate: pick one P0 backlog item and run a separate Tier
2 or Tier 3 routing packet for that exact mutation. Owner role: depends on the
selected item; current highest-value owners are Tooling/QA for skill inventory
or RNW cleanup, and Hardware/Safety for power/relay identity. Evidence need:
source-backed local records, current dirty-tree boundary, reviewer quorum, and
focused validation. Approved mutation boundary for this task: this task-log
record only. Validation command: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 170`
plus `git diff --check`. Required durable record: this task log. Authority
limits: no Tier 3, cleanup, source/index/doc mutation, release, publication, or
system-policy mutation.
