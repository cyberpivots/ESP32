# Task 0149: CBBS React Native Client Platform

Status: implemented and validated; live/native/release gates closed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-02

Source ID:
`SRC-LOCAL-CBBS-REACT-NATIVE-CLIENT-PLATFORM-2026-06-02`

## Goal

Create the accepted CBBS React Native client/operator app lane and initial
host-only scaffold from the supplied plan, while preserving firmware neutrality,
closed hardware/live surfaces, and source-backed governance records.

## Routing Packet

- Verified facts: the repo had no existing root Node/pnpm/Expo scaffold before
  this task; framework-dependent client files required an accepted client-app
  ADR; current official source checks support React Native `0.85`, Expo SDK 56,
  React `19.2.3`, React Native Web `0.21.0`, minimum Node `22.13.x`, and RNW
  `0.83` active support.
- Assumptions: the previous agent plan is the user intent; `ADR-0010` may
  accept a client/operator app framework without changing firmware framework
  selections; initial app work is host-only and simulated.
- Unknowns: live transport, BLE UUIDs, local-network mode, credentials, native
  distribution, update policy, Windows runner/toolchain, and any device or
  simulator proof remain unresolved.
- Selected tier: Tier 2.
- Owner role: Agent Operations and Architect with Source Research, UI/UX,
  Protocol, DevEx/CI, Security/Safety, and QA lenses.
- Evidence need: read-only reviewer quorum, accepted ADR, source-index rows,
  source ledger, project docs, task/handoff records, package tests, scaffold
  audits, no-secret checks, and native-folder absence checks.
- Mutation boundary: `ADR-0010`, source records, docs/project/research notes,
  task/handoff records, host-only `apps/` and `packages/`, `tools/react-native/`,
  React Native audit/test scripts, project-local React Native skill, reviewer
  profiles, advisory hook classifiers, and package metadata. No native folders,
  EAS/App Center config, live connectivity, firmware, hardware, release,
  commit, push, PR, or deploy mutation.
- Validation plan: `scripts/scaffold_audit_react_native.py`, existing scaffold
  audits, focused Python tests, `pnpm install --frozen-lockfile`, `pnpm lint`,
  `pnpm typecheck`, `pnpm test`, lockfile-bound Expo Doctor when local
  toolchain permits, `git_publication_hygiene.py check --json`, and
  `git diff --check`.
- Gate authority: Tier 2 source/tooling/host-only scaffold only. No Tier 3
  authority is opened.
- Trust boundary: UI intents are local fixture intents and are not hardware,
  transport, or external-service authority.

## Reviewer Quorum

- Governance reviewer, weight 5: conditional approval for ADR/source-record
  mutation first; rejected framework-dependent scaffold before accepted ADR.
- Source research reviewer, weight 3: approved with current primary source rows
  and precise App Center retirement wording.
- UI/UX reviewer, weight 3: approved with exact role/view/intent tests and
  transcript-first evidence wording.
- Protocol/state reviewer, weight 3: approved fixture-only protocol package and
  no ABI/transport side effects.
- DevEx/CI reviewer, weight 3: approved with lockfile-bound validation,
  native-folder absence audit, and no EAS config.
- Security/safety reviewer, weight 3: approved with no secrets, no native
  folders, no external services, no live connectivity, and disabled unsafe
  authority.

Weighted disposition: 17/17 approve for the named Phase 0 plus Phase 1/2
host-only boundary after applying the governance ADR-first condition. No P1/P2
blockers remain for this boundary. Six project-local read-only subagents were
spawned, reviewer outputs were captured, and all completed agents were closed.
A seventh QA reviewer spawn attempt was blocked by the runtime agent-thread
limit; QA validation was covered locally and by the DevEx/Security reviewer
conditions.

## Implementation Summary

- Accepted `ADR-0010` for the CBBS client/operator app lane only.
- Added source-index rows and a local source ledger for React Native, Expo SDK
  56, Expo Router/Web/New Architecture/EAS, React Native Web, React Native for
  Windows, Android/iOS permission planning, and App Center retirement context.
- Added project documentation and research notes for the CBBS React Native
  lane.
- Added a `pnpm` workspace with pinned Node `>=22.13.0` and Expo Doctor,
  TypeScript, ESLint, Jest, React Native Testing Library, and scaffold audit
  scripts.
- Added `apps/cbbs-client/` as an Expo Router Android/iOS/browser fixture app.
- Added `apps/cbbs-windows/` as a docs/stub-only RNW spike with no generated
  native Windows project.
- Added `packages/cbbs-protocol`, `cbbs-fixtures`, `cbbs-state`, `cbbs-ui`,
  `cbbs-theme`, and `cbbs-evidence`.
- Added exact role/view/intent contract tests, no-secret recursion tests,
  unsafe-action negative tests, oversized-payload tests, local-state reducer
  tests, and a React Native Testing Library render test.
- Added `scripts/scaffold_audit_react_native.py` and included it in
  `scripts/verify_scaffold.py`.
- Added a project-local `react-native-client-development` skill and five
  read-only React Native reviewer agent profiles.
- Updated advisory hook command classification for package installs,
  `create-expo-app`, Expo prebuild/export/run, EAS/App Center/store actions,
  native build commands, and device/simulator access.
- Added JS/Expo generated-output ignores for `node_modules/`, `.expo/`,
  `coverage/`, and `*.tsbuildinfo`.

## Validation

- PASS: `pnpm install`.
- PASS: `pnpm install --frozen-lockfile`.
  - Note: pnpm reported ignored dependency build scripts for
    `msgpackr-extract` and `unrs-resolver`; no native project, EAS, App
    Center, or device command was run.
- PASS: `pnpm lint`.
- PASS: `pnpm typecheck`.
- PASS: `pnpm test` (3 suites, 10 tests).
- PASS: `pnpm doctor:expo` (21/21 Expo Doctor checks).
- PASS: `pnpm --filter @cbbs/client export:web`.
- PASS: temporary static smoke check using `python3 -m http.server 4173
  --directory apps/cbbs-client/dist` plus `curl -fsS` to
  `http://127.0.0.1:4173/`; the server was stopped in the same command.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_react_native_scaffold tests.scaffold_audits.test_agent_process_classifiers`
  (11 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/git_publication_hygiene.py check --json`
  (command passed; dirty tree reflects this task; branch `main` is aligned
  with `origin/main`; no open PRs reported).
- PASS: `git diff --check`.

## Authority Limits

No native prebuild, native folders, native builds, simulator/device runs, Expo
Go proof, EAS cloud/local builds, EAS Submit, EAS Update, EAS Hosting, App
Center SDKs or automation, signing credentials, store upload, GitHub
publication, release, BLE pairing, Web Bluetooth, Web Serial, local-network
discovery, SoftAP probing, live bridge traffic, serial writes, firmware ABI
changes, bridge ABI changes, Gate F service-code changes, flash, erase,
monitor, RF/XBee action, router/admin mutation, relay, MicroSD, TFT, wiring,
load, mains, commit, push, PR, or deploy is authorized by this task.

## Handoff

Handoff:
[../handoffs/0110-cbbs-react-native-client-platform-to-qa.md](../handoffs/0110-cbbs-react-native-client-platform-to-qa.md)

## Decision Footer

Decision: `cbbs_react_native_client_platform_host_scaffold_validated`.
Next gate: optional QA review of the host-only browser export proof, or
separate future gate for native/device/live/release work. Owner: Agent
Operations and Architect with QA/DevEx/Source/UI/Protocol/Security. Evidence:
accepted ADR, source records, host-only scaffold, package validation, web
export/static smoke proof, scaffold audits, and publication hygiene check.
