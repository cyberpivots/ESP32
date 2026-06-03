# Task 0151: CBBS React Native Windows W2 Dependency Lane

Status: completed; native/live/release gates closed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-02

Source ID:
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W2-2026-06-02`

## Goal

Continue the RNW development plan by opening and implementing W2 package-only
dependency selection for `apps/cbbs-windows`, while keeping RNW native
generation, Windows build/run, live transport, hardware, and release gates
closed.

## Routing Packet

- Verified facts: W0/W1 was implemented and validated in Task 0150; `ADR-0010`
  required a separate W2 gate before RNW dependency work; current
  `apps/cbbs-windows` had no RNW dependency or native `windows/` folder; npm
  metadata showed `react-native-windows@0.83.0` peers on
  `react-native ^0.83.0` and `react ^19.2.0`, React Native `0.83.9` was the
  current `0.83.x` patch observed, and React `19.2.3` exists.
- Assumptions: W2 means package/dependency/source/test isolation only; Windows
  native generation/build/run belongs to W3/W4; package validation on Linux/WSL
  cannot prove Windows runtime behavior.
- Unknowns: local Windows host/toolchain, Visual Studio workloads, Windows SDK,
  .NET SDK, Developer Mode, package identity, capabilities, signing, runtime
  screenshot proof, live transport, firmware/bridge ABI behavior, and hardware
  acceptance remain unresolved.
- Selected tier: Tier 2.
- Owner role: Agent Operations and Architect with Source Research, DevEx/CI,
  Protocol/State, Security/Safety, and QA reviewers.
- Evidence need: W2 reviewer quorum, accepted ADR amendment, npm/source rows,
  source ledger, package manifests, lockfile importer proof, import-boundary
  tests, scaffold audit updates, no-native-folder proof, validation commands,
  task log, and QA handoff.
- Mutation boundary: `ADR-0010`, source index/ledger, this task record,
  handoff, docs index/project/research docs, `apps/cbbs-windows/package.json`,
  `apps/cbbs-windows` source/tests, `pnpm-lock.yaml`, React Native audit/tests,
  CI validation if needed. No root/shared Expo dependency changes, no
  `apps/cbbs-client` dependency changes, no native folders, RNW CLI, build/run,
  capabilities, signing, live transport, firmware/hardware, release, commit,
  push, PR, or deploy.
- Validation plan: frozen-lockfile pnpm install, lint, typecheck, Jest,
  Windows spike typecheck, Expo Doctor, React Native scaffold audit, records
  audit, agent-process audit, full scaffold verify, no-native-folder scan,
  scoped RNW dependency/lockfile/import audit, and `git diff --check`.
- Gate authority: Tier 2 W2 package-only dependency/source/test mutation only.
  No Tier 3 authority is opened.
- Trust boundary: W2 proves package graph/source isolation only; it does not
  prove RNW native build/run, Windows UI runtime, CBBS live behavior, or
  hardware behavior.

## Reviewer Quorum

- Governance cartographer, weight 5: rejected W2 mutation until a separate W2
  gate, new records, source ledger, and docs links were added.
- Source research reviewer, weight 3: conditionally approved package-only W2
  if exact npm/package metadata and isolation boundary are recorded.
- DevEx/CI reviewer, weight 3: rejected current W2 until audit changes from a
  blanket RNW ban to a scoped allowlist, with lockfile importer checks and no
  root/shared RNW changes.
- Protocol/state reviewer, weight 3: conditionally passed W0/W1 and required
  W2 guards against `@cbbs/ui` imports plus Windows closed-surface parity.
- Security/safety reviewer, weight 3: rejected mutation until W2 gate opens and
  required script/native/config blockers, exact scoped RNW allowlist, and no
  live/native/release surfaces.
- QA reviewer, weight 3: rejected W2 mutation until W2 records, source proof,
  no-native proof, dependency isolation proof, and validation checklist exist.

Weighted disposition after this W2 gate and planned fixes: 20/20 conditional
approval for package-only W2 if no P1/P2 blockers remain after validation. All
reviewer outputs were captured and all visible agents were closed before
mutation.

## Implementation Summary

- Added the accepted W2 amendment to `ADR-0010`, with source IDs for npm
  dependency metadata and the local W2 package-only implementation.
- Scoped RNW dependencies to `apps/cbbs-windows/package.json` only:
  `react-native-windows` `0.83.0`, `react-native` `0.83.9`, and React
  `19.2.3`.
- Updated `pnpm-lock.yaml` and added scaffold audit coverage for the Windows
  lockfile importer, exact dependency pins, RNW isolation from all other
  importers, no native folders/configs, and native/build/run/signing script
  blockers.
- Added a local Windows RN primitive proof component and tests that keep the
  lane package-only, role-aware, local-only, and in parity with protocol
  closed surfaces.
- Added a guard against Windows source consumption of `@cbbs/ui`, Expo, Expo
  Router, and React Native Web.
- Updated the W2 source ledger, docs index, project notes, research notes, and
  QA handoff.

## Validation

- PASS: `pnpm install --frozen-lockfile`.
- PASS: `pnpm lint`.
- PASS: `pnpm typecheck`.
- PASS: `pnpm test` (`5` suites, `24` tests).
- PASS: `pnpm --filter @cbbs/client exec expo-doctor` (`21/21` checks).
- PASS: `pnpm --filter @cbbs/windows-spike typecheck`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_react_native_scaffold`
  (`5` tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `find apps packages -maxdepth 3 -type d \( -name android -o -name ios -o -name windows -o -name macos \) -print`
  returned no native app directories.
- PASS: `git diff --check`.

Observed package-manager warnings: the initial dependency install reported
deprecated transitive packages and an Expo lane peer warning for
`react-native-worklets`; the frozen install reported ignored build scripts for
`msgpackr-extract` and `unrs-resolver`. These warnings did not open any native
generation/build/run authority and were not validation failures.

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
[../handoffs/0112-cbbs-react-native-windows-w2-to-qa.md](../handoffs/0112-cbbs-react-native-windows-w2-to-qa.md)

## Decision Footer

Decision accepted: `cbbs_react_native_windows_w2_dependency_lane`.
Next gate: W3 native Windows project generation only after same-session Windows
toolchain proof and explicit gate authority. Owner: Agent Operations and
Architect with QA/DevEx/Source/Protocol/Security. Evidence: reviewer quorum,
ADR amendment, source rows, source ledger, package/lockfile audits, host-only
tests, no-native proof, and scaffold validation.
