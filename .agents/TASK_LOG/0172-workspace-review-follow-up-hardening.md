# Task 0172: Workspace Review Follow-Up Hardening

Status: completed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-05

Source IDs:
`SRC-LOCAL-WORKSPACE-REVIEW-FOLLOW-UP-HARDENING-2026-06-05`,
`SRC-GITHUB-UPLOAD-PAGES-ARTIFACT-HIDDEN-FILES-2026-06-05`,
`SRC-LOCAL-CBBS-HOST-COMMAND-BRIDGE-LIVE-GATE-BLOCKED-2026-06-04`,
`SRC-LOCAL-CBBS-XBEE-KNOWN-PROFILE-WRITE-GATE-BLOCKED-2026-06-04`,
`SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-06-05`

## Routing

- Verified facts: Task 0169, Task 0170, and Task 0171 existed before this
  follow-up. Task 0172 did not exist. Task 0171 closes the stale
  skill-inventory and RNW generated-output scaffold blockers recorded in Task
  0170, and current scaffold audits pass; Task 0171 does not close the whole
  Task 0170 backlog. `tests/live_bench` reproduced two path-case expectation
  failures on this checkout. GitHub `actions/upload-pages-artifact` documents
  `include-hidden-files` defaulting to `false`.
- Assumptions: this implementation slice is limited to records, review
  tooling, host-only CI/test hardening, Pages artifact semantics, protocol
  safety tests, and generated-evidence audit checks.
- Unknowns: final native HostCommandBridge ABI, live adapter behavior, XBee
  write evidence, final package identities, capability-use acceptance, signing,
  release packaging, hardware power/voltage/boot-pin/isolation facts, and any
  future dependency update path remain unresolved.
- Selected tier: Tier 2 host-only governance, protocol, CI/tooling, evidence,
  and docs hardening.
- Owner role: Agent Operations with QA, Tooling/Release, Protocol/Bridge ABI,
  Evidence Records, RNW, Firmware/Device, and Hardware/Power reviewer lenses.
- Evidence need: required governance docs, current repo state, primary GitHub
  Pages upload source, read-only reviewer quorum, focused host-only tests,
  scaffold audits, publication hygiene check, and this durable record.
- Mutation boundary: `.github/workflows/`, `tests/`, `scripts/`,
  `packages/cbbs-protocol/`, `tools/simulators/custom_wireless_protocol/`,
  `comm-protocols/custom/README.md`,
  `docs/projects/espnow-bbs/bridge-abi-draft.md`, `docs/index.md`,
  `knowledge-base/source-index.md`,
  `knowledge-base/source-ledger/2026-06-05-workspace-review-follow-up-hardening.md`,
  `research/2026-06-05-workspace-review-follow-up.md`,
  `research/workspace-review-command-matrix.md`, this task record, and a
  narrow status note in Task 0170.
- Reviewer quorum: six project-local read-only reviewers were spawned, waited,
  captured, and closed by the parent. Weighted result was 23/23 approval for
  this named host-only boundary, threshold 70 percent, with no P1/P2 blockers
  remaining inside scope.
- Gate authority: Tier 2 host-only mutation only.
- Validation plan: run focused protocol, simulator, live-bench, RNW audit,
  scaffold audit, publication hygiene, Pages build/audit/smoke, and whitespace
  checks after mutation.
- Trust boundary: repo-local source, generated local Pages output, local
  host-only tests, and official GitHub action documentation. Hooks and scheduler
  warnings are advisory under `bypassPermissions`.

## Reviewer Quorum

| Role | Weight | Vote | Conditions |
| --- | ---: | --- | --- |
| Governance cartographer | 5 | approve | Create Task 0172; add discoverability for Tasks 0169-0171; avoid false source-ledger claims. |
| DevEx, CI, and release | 3 | approve | Add host-only suite CI coverage, Pages hidden-file preservation, and live-bench path-case fix. |
| Protocol bridge ABI | 3 | approve | Reject neutral-field secret-like bridge values and unknown simulator bridge keys. |
| QA validation | 3 | approve | Add current host-only command documentation. |
| Evidence records | 3 | approve | Source-record boundary must say Task 0171 closes specific Task 0170 scaffold blockers only. |
| Power, wiring, and isolation | 3 | approve host-only | Keep bench, wiring, relay/load/mains, battery/solar, XBee writes, flash, monitor, and live bridge closed. |

## Changes

- Added docs-index discoverability for Tasks 0169, 0170, 0171, and 0172.
- Added this task record, a source ledger, a review report, and a command matrix.
- Added host-only Python suite coverage to scaffold and Pages workflows.
- Set Pages artifact upload `include-hidden-files: true` and audited `.nojekyll`
  as a required hidden public artifact.
- Fixed live-bench path-case expectations by deriving expected Windows paths
  from the active checkout.
- Hardened HostCommandBridge validation against secret-like values in neutral
  fields while preserving unavailable-only behavior.
- Hardened simulator bridge request validation with per-type key allowlists and
  stable error reason `field_unknown`.
- Added RNW generated-evidence checks for size, SHA-256, source-record linkage,
  and classification as tracked generated RNW evidence, not a publication
  artifact, and local review evidence.
- Recorded that Task 0171 closes the two stale Task 0170 scaffold blockers while
  Task 0170's remaining backlog items stay open.

## Tracked Generated Evidence

These files are tracked generated RNW evidence, not a publication artifact, and
local review evidence only:

- `research/bench-records/react-native-windows/cbbs-windows-index.bundle`,
  5133785 bytes,
  `07c301fedfa809e20f8b3b95a891f6090ea2a39d3be2389f18697e0001bbb9a0`.
- `research/bench-records/react-native-windows/cbbs-windows-index.map`,
  10328346 bytes,
  `f64c8a6f20763a6bcd55c7684f8600717fe7462e63b011b22401eaab999100bb`.
- `research/bench-records/react-native-windows/live-index.bundle`,
  5133923 bytes,
  `fdd80512d04989c0a8f83fc4bd16181a5bcae38acffe0da5d5a944eb72633bc9`.

## Authority Limits

Still closed: live bench, flashing, monitor, serial port open/write,
RF/XBee/radio writes or transmit, native HostCommandBridge implementation or
dispatch, shell or DOS-C execution, relay/load/mains work, wiring, battery or
solar work, BLE/Web Serial/Web Bluetooth, SoftAP or local-network discovery,
signing certificates, Store/App Installer association, package creation for
distribution, EAS, App Center, credentials/key material, dependency updates,
commit, push, PR, deploy, release, `/etc/codex/requirements.toml`, and
`admin-strict` installation.

## Validation

Passed:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/custom_wireless_protocol -p 'test_*.py'`
  - 33 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'`
  - 34 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/rnw_menu -p 'test_*.py'`
  - 10 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/esp32_gateway_tcp -p 'test_*.py'`
  - 9 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/live_bench -p 'test_*.py'`
  - 43 tests passed. This is unit-test coverage only, not live-bench
    authority or live-device evidence.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
  - 116 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_scaffold_audit_reporting tests.scaffold_audits.test_react_native_scaffold`
  - 15 tests passed.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_pages.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 172`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/git_publication_hygiene.py check --json`
  - Returned `dirty: true` for this bounded edit set, with branch `main`
    matching `origin/main` at 0 ahead and 0 behind.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_github_pages.py`
  - Built `build/github-pages` with 64 public files.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/audit_public_manifest.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/smoke_github_pages.py`
- `pnpm test -- packages/cbbs-protocol/__tests__/contract.test.ts`
  - 24 tests passed.
- `pnpm --filter @cbbs/protocol typecheck`
- `git diff --check`
- `git status --short --branch --untracked-files=all`
  - Branch `main` remained aligned with `origin/main`; dirty entries were this
    bounded edit set.

## Handoff

No handoff is required for the completed host-only hardening slice. Future
dependency updates, live hardware work, RNW release/runtime work, XBee writes,
HostCommandBridge live dispatch, publication, commit, push, PR, or release need
separate gates.

## Decision

Decision: accept only the bounded Tier 2 host-only hardening slice. All live,
hardware, release, publication, and system-policy surfaces remain closed.
