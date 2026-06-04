# Task 0156: CBBS React Native Windows W4 Pre-Release

Status: completed; W4A source/record refresh accepted, W4B-W4E closed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-03

Source IDs:
`SRC-REACT-NATIVE-WINDOWS-RUN-WINDOWS-2026-06-03`,
`SRC-REACT-NATIVE-WINDOWS-STORE-PUBLISHING-2026-06-03`,
`SRC-MICROSOFT-MSIX-SIGNING-2026-06-03`,
`SRC-MICROSOFT-WINDOWS-CODE-SIGNING-OPTIONS-2026-06-03`,
`SRC-MICROSOFT-WINDOWS-SIDELOADING-2026-06-03`,
`SRC-MICROSOFT-MSIX-UNSIGNED-2026-06-03`,
`SRC-MICROSOFT-MSIX-APP-INSTALLER-2026-06-03`,
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W4-PRE-RELEASE-2026-06-03`

## Goal

Implement the W4 RNW pre-release plan as a source/record and app-local
readiness refresh only, while keeping build/run/package/signing/release/live
surfaces closed.

## Routing Packet

- Verified facts: W3B generated the app-local RNW native project only; W4
  build/run/deploy/signing/release remained closed; the generated native shell
  uses component name `CbbsWindows`; the generated manifest identity and
  capabilities are template facts only.
- Assumptions: pre-release means controlled planning and later local/internal
  validation, not public distribution or Store release.
- Unknowns: RNW build behavior, runtime behavior, build output layout,
  accepted package identity, signing certificate, trust model, update policy,
  and live transport.
- Selected tier: Tier 2.
- Owner role: React Native Windows coordinator with Release, QA, Source
  Research, Security/Safety, and Agent Operations.
- Evidence need: official source refresh for RNW run/build and Microsoft
  signing/distribution choices, reviewer quorum, source/test metadata
  correction, no package/signing artifacts, durable record set, and scaffold
  audits.
- Mutation boundary: `apps/cbbs-windows/src/index.tsx`,
  `apps/cbbs-windows/__tests__/windowsHostOnly.test.tsx`,
  `apps/cbbs-windows/jest.config.windows.js`,
  `apps/cbbs-windows/README.md`, ADR/docs/research notes,
  `scripts/scaffold_audit_react_native.py`, focused scaffold tests,
  `knowledge-base/source-index.md`, this task record, the matching source
  ledger, and the matching handoff.
- Validation plan: run lint, typecheck, Jest, Expo Doctor, Windows typecheck,
  React Native scaffold audit/tests, durable-record audit, agent-process audit,
  skill audit, full scaffold verification, no package/signing artifact scan,
  and `git diff --check`.
- Gate authority: W4A source/record refresh only. W4B build-only proof, W4C
  deploy/run, W4D packaging, W4E Store/production release, and all live/hardware
  surfaces remain closed.
- Trust boundary: repo-local static/source proof only; no Windows-host build,
  deploy, package, signing, install, or live transport evidence is claimed.

## Reviewer Quorum

- Coordinator/Release, weight 5: approved records plus inert metadata only,
  no release-readiness or signing/package identity claims.
- RNW DevEx/CI, weight 3: P1 found missing `AppRegistry` registration; approved
  fixing registration, stale status/test wording, audit coverage, and package
  identity/capability record clarification.
- Source Research, weight 3: rejected unsupported signing/distribution claims
  until official Microsoft source IDs were added; approved bounded records and
  metadata after source refresh.
- Security/Safety, weight 3: no P1 secret/signing/live-transport issue;
  required stale native-status correction and continued closure of signing,
  PFX/private keys, Store association, App Installer, live transport, and
  hardware surfaces.
- QA/Evidence, weight 3: rejected W4 execution; approved W4 records/audit
  preparation, source refresh, and stop-gate cleanup.

Weighted disposition: 17/17 approve W4A records/source/app-local metadata
mutation after conditions are met. No W4B/W4C/W4D/W4E execution authority is
granted. Reviewer agents were closed after evidence capture. Scheduler
advisory reported unavailable; `multi_agent_v1` reviewer tools were available
and used.

## Implemented Changes

- Registered `CbbsWindows` with `AppRegistry`.
- Corrected stale Windows status fields to reflect W3B native project
  generation while preserving no build/run/runtime proof.
- Added app-local RNW project metadata for generated solution/manifest paths,
  generated identity, generated capabilities, and non-accepted signing/Store
  state.
- Split W4 status into W4A-W4E subgates.
- Added official source IDs for RNW `run-windows`, RNW Store publishing,
  Microsoft MSIX signing, Windows code-signing options, sideloading,
  unsigned MSIX, and App Installer planning.
- Updated ADR, docs, research notes, source ledger, task log, handoff, and
  scaffold audits/tests.
- Configured the package-local Windows Jest transform to use the React Native
  Babel preset so RNW Jest setup Flow annotations parse in current-host tests.

## Validation

W4A validation passed:

- PASS: `pnpm install --frozen-lockfile`.
- PASS: `pnpm lint`.
- PASS: `pnpm typecheck`.
- PASS: `pnpm test` - 5 suites, 28 tests.
- PASS: `pnpm --filter @cbbs/client exec expo-doctor` - 21/21 checks.
- PASS: `pnpm --filter @cbbs/windows-spike typecheck`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_react_native_scaffold`
  - 8 tests.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: no package-lock/package/signing artifact scan.
- PASS: package-script scan found no build/run/signing/deploy/release
  commands.
- PASS: `git diff --check`.

Note: package-local `pnpm --filter @cbbs/windows-spike test:windows` remains
outside the accepted W4A validation path. It initially failed parsing RNW Jest
setup before the transform fix, then the direct RNW preset command hung without
test output and was terminated. Root `pnpm test` remains the accepted host Jest
evidence and passed the Windows test suite.

No Windows build/run, deploy, packaging, signing, install, Store association,
App Installer publishing, or live transport command is part of W4A.

## Authority Limits

No RNW `run-windows`, Visual Studio/MSBuild build, deploy, launch, package
creation, signing, certificate/PFX handling, package identity acceptance,
capability use, Store association, Store upload, App Installer publishing,
App Center, EAS, simulator/device launch, live network, BLE, Web Bluetooth,
Web Serial, local-network discovery, SoftAP, serial/RF/XBee action,
firmware/bridge/serial ABI change, flash, erase, monitor, relay, load, mains,
release, commit, push, PR, or deploy is authorized by this task.

## Decision

Decision accepted: `cbbs_react_native_windows_w4a_pre_release_source_record_refresh`.
W4A is complete as a source/record and app-local metadata refresh. W4B-W4E
remain future gates requiring separate authority.

## Handoff

Handoff:
[../handoffs/0116-cbbs-react-native-windows-w4-pre-release-to-qa-release.md](../handoffs/0116-cbbs-react-native-windows-w4-pre-release-to-qa-release.md)
