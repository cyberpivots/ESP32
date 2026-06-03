# Task 0153: CBBS React Native Windows W2.1 Local Shell

Status: completed; native/live/release gates closed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-02

Source ID:
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W21-2026-06-02`

## Goal

Continue React Native Windows development inside the W2 package-only boundary
by replacing the minimal Windows proof component with a deterministic
Client/Sysop local shell, without opening W3 native generation or runtime
authority.

## Routing Packet

- Verified facts: W0-W2 were committed and pushed; current `main` was clean
  before W2.1 edits; W2 authorizes package-only RNW source/tests in
  `apps/cbbs-windows`; W3 native generation/build/run remains closed without
  explicit authority and same-session Windows toolchain proof.
- Assumptions: continuing development means W2 package-only source/test work,
  not W3 native project generation.
- Unknowns: Windows host/toolchain, Visual Studio workloads, Windows SDK, .NET
  SDK, Developer Mode, package identity, capabilities, signing, runtime
  screenshots, live transport, firmware/bridge ABI behavior, and hardware
  acceptance remain unresolved.
- Selected tier: Tier 2.
- Owner role: Agent Operations and Architect with React Native DevEx/CI,
  UI parity, Protocol/State, Security/Safety, and QA lenses.
- Evidence need: reviewer quorum, source/test diff, audit updates, no-native
  proof, typecheck/Jest/scaffold validation, task log, source ledger, and
  handoff.
- Mutation boundary: `apps/cbbs-windows` source/tests/README/tsconfig,
  React Native scaffold audit/tests, docs index/project/research notes, source
  index/ledger, task record, and handoff. No native folders, RNW CLI,
  Visual Studio/MSBuild, Package.appxmanifest, capabilities, signing, live
  transport, firmware/hardware, release, commit, push, PR, or deploy.
- Validation plan: focused Windows typecheck/Jest/audit first, then
  frozen-lockfile install, lint, root typecheck, full Jest, Expo Doctor,
  Windows typecheck, React Native scaffold audit, audit unit tests, records
  audit, agent-process audit, scaffold verify, no-native-folder scan, and
  `git diff --check`.
- Gate authority: Tier 2 W2.1 package-only source/test mutation only. No Tier 3
  authority is opened.
- Trust boundary: W2.1 proves local source/test behavior only; it does not
  prove RNW native build/run, Windows UI runtime, CBBS live behavior, or
  hardware behavior.

## Reviewer Quorum

- DevEx/CI reviewer, weight 3: approved W2.1 package-only testability slice;
  recommended deterministic Client/Sysop shell source, tests, and audit guards.
- UI parity reviewer, weight 3: approved package-only Windows Client/Sysop
  surface with RN primitives, local intent buttons, disabled closed surfaces,
  and transcript-first evidence wording.
- Protocol/state reviewer, weight 3: approved W2 continuation and identified a
  drift gap from duplicated protocol constants; recommended deriving local
  marker, closed surfaces, role/view/action typing, and local intents from
  `@cbbs/protocol`.

Weighted disposition: 9/9 approval for W2.1 package-only source/test mutation
with no P1/P2 blockers. All reviewer outputs were captured and visible agents
were closed before mutation.

## Implementation Summary

- Replaced the one-line Windows proof component with
  `WindowsClientSysopShell`, a deterministic package-only Client/Sysop shell
  built from React Native primitives.
- Derived local-only marker, closed surfaces, local intent construction, and
  role/view/action typing from `@cbbs/protocol`.
- Added local fixture rows, Client/Sysop view tabs, local action controls,
  transcript-first evidence wording, and disabled closed-surface controls with
  stable test IDs.
- Updated Windows tests to render Client/Sysop shells, validate emitted local
  intents, assert closed-surface disabled state, and preserve no-runtime-proof
  wording.
- Updated the Windows tsconfig for standalone package typechecking against the
  shared protocol source.
- Added W2.1 source ledger, task record, handoff, docs index links, project
  docs, research notes, source-index row, and React Native audit markers.

## Validation

- PASS: `pnpm install --frozen-lockfile`.
- PASS: `pnpm lint`.
- PASS: `pnpm typecheck`.
- PASS: `pnpm test` (`5` suites, `27` tests).
- PASS: `pnpm --filter @cbbs/client exec expo-doctor` (`21/21` checks).
- PASS: `pnpm --filter @cbbs/windows-spike typecheck`.
- PASS: `pnpm exec jest apps/cbbs-windows --runInBand` (`1` suite, `7`
  tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_react_native_scaffold`
  (`5` tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `find apps packages -maxdepth 3 -type d \( -name android -o -name ios -o -name windows -o -name macos \) -print`
  returned no native app directories.
- PASS: `git diff --check`.

Observed package-manager warning: `pnpm install --frozen-lockfile` reported
ignored build scripts for `msgpackr-extract` and `unrs-resolver`. This warning
does not open or prove native Windows generation, build/run, signing, release,
or live behavior.

## Authority Limits

No RNW CLI execution, `init-windows`, `run-windows`, native `windows/` folder,
Visual Studio/MSBuild, Windows Package.appxmanifest, package identity,
capability declaration, signing, installer/store packaging, EAS, App Center,
simulator/device launch, live network, BLE, Web Bluetooth, Web Serial,
local-network discovery, SoftAP, serial write, RF/XBee action, firmware ABI
change, bridge ABI change, serial ABI change, Gate F service-code change,
flash, erase, monitor, relay, load, mains, release, commit, push, PR, or deploy
is authorized by this task.

## Handoff

Handoff:
[../handoffs/0113-cbbs-react-native-windows-w21-local-shell-to-qa.md](../handoffs/0113-cbbs-react-native-windows-w21-local-shell-to-qa.md)

## Decision Footer

Decision accepted: `cbbs_react_native_windows_w21_local_shell`.
Next gate: W3 native Windows project generation only after same-session Windows
toolchain proof and explicit gate authority. Owner: Agent Operations and
Architect with QA/DevEx/UI/Protocol/Security. Evidence: reviewer quorum,
source ledger, Windows source/tests, package-boundary audits, no-native proof,
and scaffold validation.
