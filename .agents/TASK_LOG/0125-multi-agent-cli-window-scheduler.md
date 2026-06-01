# Multi-Agent CLI Window Scheduler

Status: Tier 2 host-only scheduler implementation validated

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-01

## Routing

- Selected tier: Tier 2 because this changes repo-local tooling, advisory
  hooks, tests, prompt docs, source records, and task records.
- Owner role: Agent Operations with Tooling and QA.
- Evidence need: required governance docs, official Codex hook/config sources,
  read-only reviewer quorum, focused scheduler tests, self-test, doctor,
  scaffold audit, verify scaffold, and `git diff --check`.
- Mutation boundary: `scripts/agent_scheduler.py`,
  `tests/scaffold_audits/test_agent_scheduler.py`,
  `.codex/hooks/pre_tool_use_agent_process.py`, focused hook tests, prompt
  docs, docs index, prompt registry, source index, source ledger, and this task
  log.
- Gate authority: host-only advisory scheduler infrastructure only.

## Verified Facts

- Official Codex docs describe project `.codex/config.toml`/`hooks.json`
  loading and `PreToolUse` as a guardrail rather than a complete enforcement
  boundary.
- Workspace governance requires `permission_mode=bypassPermissions` to remain
  advisory and non-blocking.
- Runtime scheduler state belongs outside the repository under the user state
  directory.
- The current dirty tree already contains unrelated firmware, LCD, simulator,
  source, and docs changes, so this task does not touch those unrelated
  surfaces.
- Task ordinal `0124` is already occupied in the current tree by the PF0530N
  scrolling/XML task record, so this scheduler task uses the next available
  local ordinal, `0125`.

## Assumptions

- The scheduler coordinates same-user local/WSL Codex windows only.
- Scheduler claims are advisory coordination signals, not an enforcement layer
  for operator permissions.
- Cross-machine locking, networked coordination, and release governance are out
  of scope for this v1.

## Unknowns

- Whether future Codex hook schemas will change enough to require hook fixture
  updates.
- Whether additional UI around queue promotion is needed after real multi-window
  use.

## Reviewer Quorum

- Governance/Agent Operations, weight 5: approved; no P1/P2 blockers for the
  host-only advisory boundary.
- Tooling, weight 3: approved; required socket-unavailable, stale lease, SQLite,
  malformed/fallback, and timeout-oriented coverage.
- Security/Safety, weight 3: approved; required state outside repo and no closed
  Tier 3/live/credential/external/destructive authority.
- QA, weight 3: rejected final acceptance until scheduler tests, doctor,
  daemon-unavailable fallback, dirty-baseline, and reservation-concurrency
  coverage existed. This task adds that validation surface.

Weighted disposition before mutation: 11/14 approve with one QA P2 that is the
named implementation/validation surface. The P2 is accepted as an in-scope
condition to close before final acceptance, not as authority to expand scope.

## Implementation

- Added `scripts/agent_scheduler.py` with:
  - JSON-over-Unix-socket daemon commands.
  - SQLite-backed `multi_window_coordination.v1` state.
  - Window open, heartbeat, close, queue, and max-active-window handling.
  - Claim acquire, renew, release, finalize, write/write conflict detection,
    stale-evidence warnings, dirty-baseline overlap warnings, lease expiry, and
    stale-reap events.
  - Task-log and handoff ordinal reservation/finalization.
  - `preflight`, `pretool-check`, `doctor`, and `self-test`.
- Updated `.codex/hooks/pre_tool_use_agent_process.py` to call
  `pretool-check` with a short timeout and append advisory context only.
- Added focused scheduler tests and updated the hook test for complete-triage
  scheduler advisory output.
- Added prompt docs, prompt registry, source index, source ledger, and docs
  index links.

## Validation Plan

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_agent_scheduler`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_scheduler.py self-test`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_scheduler.py doctor --repo /mnt/h/ESP32`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `git diff --check`

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_agent_scheduler` (9 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_scheduler.py self-test`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_scheduler.py doctor --repo /mnt/h/ESP32`
- PASS: temporary-state daemon lifecycle check with `daemon ensure`, `daemon status`, and `daemon stop`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_agent_process_hooks` (8 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'` (64 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `git diff --check`

## Closed Surfaces

No `/etc/codex` mutation, admin-strict install, hard yolo block, live hardware,
COM/serial access, flash, monitor, RF/XBee writes, relay/load/mains, wiring,
credentials, external service calls, destructive git, GitHub publication,
release, commit, or push is opened by this task.

## Decision Footer

Decision: `handoff` with the Tier 2 host-only scheduler validation complete.
Next gate: optional same-session daemon trial with multiple real Codex windows,
or normal use through advisory claims. Owner: Agent Operations with Tooling and
QA. Evidence: local host-only tests, scheduler self-test, doctor, scaffold
audit, source/task records. Approved mutation boundary: the Tier 2 scheduler,
hook, tests, docs, and records listed above. Authority limits remain closed for
Tier 3/live/device/system/release actions.

## Real Daemon Trial - 2026-06-01

Tier 2 reviewer quorum before mutation:

- Coordinator/Agent Operations, weight 5: approved the default-state host-only
  daemon trial with append-only task-log evidence.
- Tooling, weight 3: approved host-only daemon harness conditions; noted
  isolated `/tmp` state would reduce contamination risk, but the user-approved
  gate here intentionally used the default user state.
- QA, weight 3: approved only if cleanup proof includes daemon status with
  zero active trial windows and claims before stop.
- Security/Safety, weight 3: approved the closed-surface boundary and required
  `permission_mode=bypassPermissions` to remain advisory-only.

Weighted disposition: 14/14 approve, no P1/P2 blockers after the cleanup-proof
condition is recorded. Reviewer lifecycle cleanup was completed by waiting for
and closing all four spawned read-only reviewers.

Trial command:

- `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/esp32_scheduler_real_daemon_trial.py`
- Evidence JSON: `/tmp/real-daemon-trial-1780306747-1403689.json`
- Trial prefix: `real-daemon-trial-1780306747-1403689`
- Runtime state path:
  `/home/cyber/.local/state/codex/esp32-scheduler/ESP32-614a4f5ef2de`

Observed passes before the stop gate:

- `preflight` returned `ok: true`, repo ID `ESP32-614a4f5ef2de`, default state
  path outside the repo, and authority limits including advisory-only, no
  `/etc/codex` mutation, no live hardware, no credentials, no external
  services, and no commit/push/release.
- `daemon ensure` started the real daemon; initial `daemon status` reported
  `running: true`, `activeWindowCount: 0`, and dirty-baseline capture with 81
  dirty paths.
- Five logical windows opened active.
- A sixth default `window open` returned exit code 1 with
  `reason: max-active-windows`, `activeWindowCount: 5`, and
  `maxActiveWindows: 5`.
- A sixth `--on-full queue` window opened with `status: queued`.
- Five disjoint write claims on trial-only nonexistent path globs were acquired.
- An overlapping write claim was rejected with
  `reason: overlapping-write-claim`.
- A review claim reported `stale-evidence-warning`.
- A claim against `.agents/TASK_LOG/0125-multi-agent-cli-window-scheduler.md`
  reported `dirty-baseline-overlap`.

Stop-gate failure:

- The zero-second lease claim command returned `ok: true`, but the claim
  `claim-b84775358d8d` received `leaseExpiresAt: 2026-06-01T09:54:16Z`
  instead of expiring immediately.
- The following `daemon status` reported `reaped: []`; the zero-lease claim was
  still `status: active`, so the required `stale-reap` event was not observed.
- The trial stopped at this failure. No scheduler source code was edited in
  this gate.

Cleanup proof:

- The harness released every trial claim and closed every trial window in its
  `finally` block; all release and close commands returned exit code 0.
- Pre-stop cleanup status reported `activeWindowCount: 0`,
  `activeTrialWindowsBeforeStop: 0`, and `activeTrialClaimsBeforeStop: 0`.
- Post-stop daemon status reported `running: false` for
  `/mnt/h/ESP32` with repo ID `ESP32-614a4f5ef2de`.

Post-trial validation:

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_scheduler.py doctor --repo /mnt/h/ESP32`
  returned `ok: true`; `stateDirOutsideRepo`, `stateDirExistsOrCreatable`, and
  `sqliteOpen` were true; `daemonResponding` was false because cleanup stopped
  the daemon.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
  returned `PASS: ESP32 agent-process audit succeeded`.
- PASS: `git diff --check`.
- `git status --short` still reported the broad preexisting dirty tree; this
  gate intentionally changed only this task-log record under the approved repo
  mutation boundary. During the run, unrelated untracked task/source/handoff
  files such as `0127`/`0093` were visible and were not touched by this gate.
- Final `daemon status` reported `running: false` at the default state path.

Separate follow-up fix plan:

- Keep the scheduler code closed in this trial gate.
- Next Tooling/QA gate should inspect the daemon request path for
  `claim_acquire` lease handling, because the daemon dispatch appears to treat
  `lease_seconds=0` as missing/default while direct `SchedulerCore` unit
  coverage expects zero-second leases to expire.
- Add a focused daemon/CLI regression for `--lease-seconds 0`, then rerun the
  real default-state daemon trial and record promotion plus
  `pretool-check permission_mode=bypassPermissions` evidence after the stale
  reap assertion passes.

## Zero-Lease Fix And Real Daemon Rerun - 2026-06-01

Classification: Tier 2 host-only Tooling/QA follow-up. No hardware,
serial/RF/flash, relay/load/mains, credentials, `/etc/codex`, external
services, destructive git, commit, push, or release authority was opened.

Routing packet:

- Verified facts: `SchedulerCore.acquire_claim()` and `renew_claim()` already
  preserve explicit zero leases through `max(0, int(lease_seconds))`; daemon
  dispatch was replacing explicit `0` with `CLAIM_LEASE_SECONDS` through
  `request.get("lease_seconds") or CLAIM_LEASE_SECONDS`; this task log already
  recorded the real-daemon zero-lease failure above.
- Assumptions: explicit `lease_seconds=0` means immediate expiry/reap; absent,
  `None`, and blank lease fields should keep the default lease; nonblank
  invalid values should still flow to the daemon JSON error path.
- Unknowns: default user scheduler state could contain unrelated old records,
  so the rerun used a unique trial prefix and cleaned up only its own
  windows/claims.
- Owner role: Tooling with Agent Operations and QA.
- Evidence need: read-only reviewer quorum, focused scheduler tests,
  self-test, doctor, scaffold audit, default-state daemon trial, cleanup proof,
  `git diff --check`, and dirty-tree review.
- Mutation boundary: `scripts/agent_scheduler.py`,
  `tests/scaffold_audits/test_agent_scheduler.py`, and append-only evidence in
  this task log.

Reviewer quorum:

- Coordinator/Agent Operations, weight 5: approved the named Tier 2 boundary
  with required daemon/CLI zero-lease evidence and cleanup proof.
- Tooling, weight 3: approved with required parsing behavior: default only for
  missing, `None`, or blank; preserve `0`; keep invalid nonblank values on the
  existing error path; cover acquire and renew.
- QA, weight 3: recorded the pre-mutation daemon-dispatch bug as a P1 and
  required focused dispatch regression coverage plus a passing real default
  daemon trial.
- Security/Safety, weight 3: approved the host-only boundary and required
  `permission_mode=bypassPermissions` to remain advisory with no deny/block
  fields.

Weighted disposition: 11/14 approved mutation of the named boundary, with QA's
P1 being the in-scope defect fixed by this gate. Required roles were present,
no reviewer objected to the bounded fix, and all four read-only reviewers were
waited and closed before mutation.

Implementation:

- Added internal lease parsing in `scripts/agent_scheduler.py` so daemon
  dispatch defaults only when `lease_seconds` is absent, `None`, or blank.
- Updated `claim_acquire` and `claim_renew` dispatch to use that parser.
- Added focused regression coverage in
  `tests/scaffold_audits/test_agent_scheduler.py` for:
  - dispatch `claim_acquire` preserving `lease_seconds: 0` and producing a
    `stale-reap` on following `status`;
  - dispatch `claim_renew` preserving `lease_seconds: 0` and producing a
    `stale-reap` on following `status`;
  - missing, `None`, empty, and whitespace lease fields defaulting;
  - invalid nonblank lease values not silently defaulting.

Validation before daemon rerun:

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_agent_scheduler`
  ran 13 tests.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_scheduler.py self-test`
  returned `ok: true` with `window-limit`, `write-conflict`,
  `dirty-baseline`, `stale-reap`, and `record-reserve`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_scheduler.py doctor --repo /mnt/h/ESP32`
  returned `ok: true`; daemon was stopped before the trial, state directory was
  outside the repo, and SQLite opened.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
  returned `PASS: ESP32 agent-process audit succeeded`.
- PASS: `git diff --check`.

Real default-state daemon rerun:

- Command family: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_scheduler.py ...`
- Evidence JSON:
  `/tmp/real-daemon-trial-zero-lease-fix-1780307677-1418825.json`
- Trial prefix: `zero-lease-fix-1780307677-1418825`
- Runtime state path:
  `/home/cyber/.local/state/codex/esp32-scheduler/ESP32-614a4f5ef2de`
- Result: PASS with `failures: []`.

Observed pass evidence:

- `preflight` and `daemon ensure` returned `ok: true`; initial daemon status
  reported `running: true` and `activeWindowCount: 0`.
- Five logical trial windows opened with `status: active`.
- Sixth default `window open` returned exit code 1 with
  `reason: max-active-windows`.
- Sixth `--on-full queue` window opened with `status: queued`.
- Five disjoint trial write claims were acquired.
- Overlapping write claim was rejected with
  `reason: overlapping-write-claim`.
- Review claim returned `stale-evidence-warning`.
- Claim against `.agents/TASK_LOG/0125-multi-agent-cli-window-scheduler.md`
  returned `dirty-baseline-overlap`.
- Closing one active trial window promoted the queued trial window and daemon
  status still reported five active windows.
- Zero-second acquire claim `claim-c22d3ccab9e1` produced a following
  `stale-reap`.
- Zero-second renew claim `claim-d80de2d0f450` produced a following
  `stale-reap`.
- `pretool-check` with `permission_mode=bypassPermissions` emitted advisory
  context containing `no deny/block`, and no `permissionDecision` or hook-level
  `decision` field.

Cleanup proof:

- The harness released active trial claims and closed all six trial windows.
- Pre-stop cleanup status reported `preStopActiveTrial: [0, 0]`, meaning zero
  active trial windows and zero active trial claims.
- Post-stop daemon status reported `postStopRunning: false`.
- A superseded first rerun attempt also cleaned up and stopped the daemon; it
  failed only because the harness incorrectly required an `ok` field from
  `pretool-check`, whose documented output shape is hook context.

Post-rerun validation:

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_scheduler.py doctor --repo /mnt/h/ESP32`
  returned `ok: true` after cleanup, with `daemonResponding: false` because the
  daemon was intentionally stopped.
- PASS: final `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_agent_scheduler`
  ran 13 tests after the task-log append.
- PASS: final `PYTHONDONTWRITEBYTECODE=1 python3 scripts/agent_scheduler.py self-test`.
- PASS: final `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: final `git diff --check`.

Dirty-tree boundary:

- The broad preexisting dirty tree remains. This follow-up intentionally
  touched only `scripts/agent_scheduler.py`,
  `tests/scaffold_audits/test_agent_scheduler.py`, and this task log under the
  approved mutation boundary.

Decision Footer:

Decision: `continue` completed for the named Tier 2 zero-lease fix. Next gate:
normal scheduler use or any future scheduler change under a fresh Tooling/QA
gate. Owner: Tooling with Agent Operations and QA. Evidence: reviewer quorum,
focused tests, self-test, doctor, scaffold audit, default-state daemon rerun
JSON, cleanup proof, and stopped daemon status. Approved mutation boundary:
the three files named above. Authority limits remain closed for hardware,
serial/RF/flash, relay/load/mains, credentials, `/etc/codex`, external
services, destructive git, commit, push, and release.
