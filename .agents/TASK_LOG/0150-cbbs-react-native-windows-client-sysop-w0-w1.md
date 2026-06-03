# Task 0150: CBBS React Native Windows Client/Sysop W0/W1

Status: implemented and validated; native/live/release gates closed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-02

Source ID:
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W0-W1-2026-06-02`

## Goal

Implement the W0/W1 portion of the CBBS React Native Windows Client/Sysop
plan: source-backed governance amendment, host-only protocol/UI hardening,
Windows TypeScript-only source model, audit/test coverage, and CI validation.

## Routing Packet

- Verified facts: `ADR-0010` was accepted for CBBS client/operator apps, but
  it originally kept the Windows lane docs/stub-only; `apps/cbbs-windows`
  had no native `windows/` folder; existing source rows covered RN, Expo,
  RNW support, and App Center; no live/native/release authority was present.
- Assumptions: the supplied continuation plan is the user intent; W0/W1 means
  records/source/tests/audits/CI only; Windows Client/Sysop starts as one
  role-aware app model, not separate binaries/package identities.
- Unknowns: local Windows host/toolchain, Visual Studio workloads, Windows
  SDK/.NET SDK, Developer Mode, RNW runner, package identity, capabilities,
  signing, Store packaging, live transport, and CBBS runtime proof remain
  unresolved.
- Selected tier: Tier 2.
- Owner role: Agent Operations and Architect with Source Research, DevEx/CI,
  UI/UX, Protocol/State, Security/Safety, and QA reviewers.
- Evidence need: read-only reviewer quorum, accepted ADR amendment, official
  RNW/Windows source rows, source ledger, protocol/UI/Windows tests,
  scaffold audit updates, CI pnpm validation, task log, and QA handoff.
- Mutation boundary: `ADR-0010`, `knowledge-base/source-index.md`, new source
  ledger, this task record, QA handoff, `docs/index.md`, CBBS React Native
  project/research/docs, TypeScript-only `apps/cbbs-windows`, host-only
  `packages/cbbs-*`, React Native tests/audits, root TS/Jest/lint config, and
  scaffold CI. No firmware, hardware, native folders, RNW dependencies, live
  transport, external services, signing, release, commit, push, PR, or deploy.
- Validation plan: React Native scaffold audit, durable-record audit,
  agent-process audit, focused scaffold unittests, full scaffold verification,
  frozen-lockfile pnpm install, lint, typecheck, Jest, Windows spike typecheck,
  Expo Doctor, and `git diff --check`.
- Gate authority: Tier 2 W0/W1 host-only mutation only. No Tier 3 authority is
  opened.
- Trust boundary: all UI intents are local fixture intents and do not prove or
  operate CBBS, firmware, bridge, serial, RF, BLE, network, or hardware.

## Reviewer Quorum

- Governance cartographer, weight 5: initially rejected W1 mutation until
  `ADR-0010` was amended; required new task/handoff/source ledger and audit
  policy updates.
- Source research reviewer, weight 3: approved W0/W1 host-only boundary with
  future source refresh required before native, Windows runner, EAS/App
  Center, live connectivity, signing, release, or device/simulator gates.
- UI parity reviewer, weight 3: rejected current W1 until role/view render
  parity, local intent controls, closed-surface labels, accessibility IDs, and
  evidence wording were fixed.
- Protocol/state reviewer, weight 3: rejected current W1 until exact allowed
  keys, mandatory local-only marker, metadata-key rejection, optional-string
  checks, and protocol/fixture closed-surface parity were fixed.
- Security/safety reviewer, weight 3: approved W0/W1 host-only boundary with
  native, external-service, credential, live-connectivity, firmware/hardware,
  release, and publication surfaces closed.
- QA reviewer, weight 3: approved W0-first sequencing and rejected W1 before
  the ADR amendment; required new durable record, handoff, audit policy, and
  explicit Windows Client/Sysop tests.
- DevEx/CI reviewer, weight 3: conditional pass for W0/W1 host-only and
  blocked a CI-ready claim until pnpm frozen-lockfile validation was added to
  CI.

Weighted disposition after fixes planned in this task: 25/25 approve for the
named W0/W1 host-only gate if no P1/P2 blockers remain after validation. Six
read-only reviewers were spawned initially; the seventh QA spawn was retried
after one reviewer was closed. All reviewer outputs were captured and all
visible agents were closed before mutation.

## Implementation Summary

- Amended `ADR-0010` to authorize Windows W0/W1 host-only records/source/tests
  while keeping W2-W5, RNW dependency/native/toolchain/live/release gates
  closed.
- Added official RNW dependency, RNW getting-started, RNW CLI, and Windows app
  capability source rows.
- Added this source ledger and local source-index row.
- Hardened UI intent validation with exact top-level keys, mandatory
  `fixture-only-ui-intent`, metadata-key rejection, optional-string validation,
  recursive secret/live-action rejection, and 512-byte payload bounds.
- Pinned closed-surface parity between protocol constants, fixtures, UI labels,
  tests, and audits.
- Added Client/Sysop role profiles and testable UI local-action controls,
  disabled unsafe controls, accessibility/test IDs, and transcript-first proof
  details.
- Expanded `apps/cbbs-windows` from stub-only to a TypeScript-only host source
  model for one Client/Sysop app.
- Added protocol, fixture, UI, Windows spike, audit, and CI coverage.
- Added pnpm frozen-lockfile React Native validation to scaffold CI.

## Validation

- PASS: `pnpm install --frozen-lockfile`.
  - Note: pnpm reported ignored dependency build scripts for
    `msgpackr-extract` and `unrs-resolver`; no native project, RNW CLI, EAS,
    App Center, device, or live command was run.
- PASS: `pnpm lint`.
- PASS: `pnpm typecheck`.
- PASS: `pnpm test` (5 suites, 22 tests).
- PASS: `pnpm --filter @cbbs/windows-spike typecheck`.
- PASS: `pnpm --filter @cbbs/client exec expo-doctor` (21/21 checks).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_react_native_scaffold tests.scaffold_audits.test_agent_process_classifiers tests.scaffold_audits.test_agent_process_decision`
  (18 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `git diff --check`.

## Authority Limits

No `react-native-windows` dependency, RNW CLI execution, `init-windows`,
`run-windows`, native `windows/` folder, Visual Studio/MSBuild, Windows
Package.appxmanifest, package identity, capability declaration, signing,
installer/store packaging, EAS, App Center, simulator/device launch, live
network, BLE, Web Bluetooth, Web Serial, local-network discovery, SoftAP,
serial write, RF/XBee action, firmware ABI change, bridge ABI change, serial
ABI change, Gate F service-code change, flash, erase, monitor, relay, load,
mains, release, commit, push, PR, or deploy is authorized by this task.

## Handoff

Handoff:
[../handoffs/0111-cbbs-react-native-windows-client-sysop-w0-w1-to-qa.md](../handoffs/0111-cbbs-react-native-windows-client-sysop-w0-w1-to-qa.md)

## Decision Footer

Decision: `cbbs_react_native_windows_w0_w1_host_only_validated`.
Next gate: W2 RNW dependency-lane planning or W1 QA review only after this
host-only validation remains green. Owner: Agent Operations and Architect with
QA/DevEx/Source/UI/Protocol/Security. Evidence: reviewer quorum, ADR
amendment, source rows, source ledger, host-only code/tests, scaffold audit,
CI validation, and closed-surface checks.
