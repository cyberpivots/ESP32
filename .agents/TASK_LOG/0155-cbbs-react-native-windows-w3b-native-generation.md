# Task 0155: CBBS React Native Windows W3B Native Generation

Status: completed; W3B native generation accepted, W4 build/run remains closed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-03

Source IDs:
`SRC-REACT-NATIVE-WINDOWS-CLI-2026-06-02`,
`SRC-REACT-NATIVE-WINDOWS-CPP-APP-TEMPLATE-2026-06-03`,
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W3A-2026-06-03`,
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W3B-2026-06-03`

## Goal

Open the reviewed RNW W3B native-generation gate for `apps/cbbs-windows`
without claiming Windows build/run/runtime proof or live CBBS behavior.

## Routing Packet

- Verified facts: W3A proved package-local RNW 0.83 prerequisite readiness;
  current RNW `cpp-app` source mutates app package metadata and runs install;
  official/package-local RNW 0.83 CLI sources do not expose a no-install or
  no-package-mutation option; the W3B command must be app-scoped.
- Assumptions: package-manager effects are contained by
  `NPM_CONFIG_PACKAGE_LOCK=false`, final dependency state is pnpm-only, and
  generated RNW run scripts are dormant metadata until removed or neutralized.
- Unknowns: exact generated native diff, CLI overwrite prompts, generated
  manifest identity/publisher values, and build/runtime behavior.
- Selected tier: Tier 3.
- Owner role: React Native Windows coordinator with Agent Operations, DevEx/CI,
  Source Research, Security/Safety, and QA.
- Evidence need: same-session reviewer disposition, no-native baseline,
  app-scoped command log, generated diff inventory, manifest capability
  inspection, package/lockfile reconciliation, no package-lock proof, scaffold
  audits, and durable handoff.
- Mutation boundary: `apps/cbbs-windows/windows/**`,
  `apps/cbbs-windows/metro.config.js`,
  `apps/cbbs-windows/jest.config.windows.js`,
  `apps/cbbs-windows/NuGet.config`, `apps/cbbs-windows/package.json`,
  `pnpm-lock.yaml`, W3B audit/test updates, and W3B governance/source records.
- Validation plan: update W3-aware audits first, run fresh reviewer quorum, run
  only the app-scoped no-overwrite/no-telemetry `init-windows` command if the
  quorum has no P1/P2 blockers, remove/neutralize generated `run-windows`
  scripts, reconcile with pnpm, inspect manifest capabilities, reject package
  locks and build/signing artifacts, then run the full scaffold validation.
- Gate authority: user explicitly authorized Windows toolchain handling and
  W3B implementation. W4 build/run/deploy/signing/release and live/hardware
  surfaces remain closed.
- Trust boundary: W3B proves native generation only; repo hooks are advisory
  under bypass permissions; source records and explicit gate authority control.

## Reviewer Quorum

Fresh read-only reviewers first rejected the unrecorded W3B execution state and
approved only W3B record/audit preparation until the following corrections were
present:

- Governance, weight 5: P1 missing accepted W3B records; proceed with records
  and W3-aware audit only before a fresh quorum.
- Source Research, weight 3: P1 no supported no-install/no-package path; W3B
  must contain package-manager side effects or stop.
- DevEx/CI, weight 3: P1 generated `run-windows` script must be removed or
  neutralized before acceptance; use `NPM_CONFIG_PACKAGE_LOCK=false` and reject
  package-lock output.
- QA, weight 3: P1 command must be app-scoped with
  `pnpm --dir apps/cbbs-windows exec ...`; no root `windows/` or root
  package mutation is allowed.
- Security/Safety, weight 3: P1 no accepted W3B boundary yet; manifest
  capabilities may be recorded only as generated template facts.

Weighted disposition: 17/17 reject execution until W3B records/audit exist.
The same outputs approve W3B record/audit preparation. Visible reviewer agents
were closed after evidence capture.

After W3B records and the W3-aware audit passed, a fresh read-only reviewer
quorum approved the exact native-generation command:

- Governance, weight 5: approved the accepted ADR/task/handoff/source-index
  boundary.
- Source Research, weight 3: approved with package-local RNW 0.83 template and
  official CLI source evidence.
- DevEx/CI, weight 3: approved with generated `run-windows` script removal and
  pnpm reconciliation conditions.
- QA, weight 3: approved app-scoped no-overwrite/no-telemetry generation and
  post-generation validation requirements.
- Security/Safety, weight 3: approved native generation only, with W4,
  live/release/signing/hardware surfaces closed.

Weighted disposition: 17/17 approve for W3B native generation. No P1/P2
blockers remained. Visible reviewer agents were closed after evidence capture.

## Accepted W3B Command

Run only after W3B records/audit pass and a fresh no-P1/P2 reviewer
disposition:

```bash
NPM_CONFIG_PACKAGE_LOCK=false pnpm --dir apps/cbbs-windows exec react-native init-windows --template cpp-app --name CbbsWindows --namespace Cbbs.Windows --no-telemetry
```

Do not pass `--overwrite`. Stop if the CLI prompts for overwrite, requires
`--overwrite`, runs build/deploy, writes outside the mutation boundary, creates
tracked package-lock output, or declares capabilities beyond reviewed template
defaults.

## Stop Conditions

- Any `run-windows`, MSBuild, Visual Studio launch, deploy, package, signing,
  release, EAS, App Center, simulator/device launch, live network, BLE,
  Web Bluetooth, Web Serial, serial/RF/XBee, flash, erase, monitor, relay,
  load, mains, commit, push, PR, or deployment command.
- Any generated build output or signing/package artifact, including `bin/`,
  `obj/`, `.vs/`, `AppPackages/`, `.appx`, `.msix`, `.pfx`, `.cer`, `.snk`,
  or store-association files.
- Any `Package.appxmanifest` capability beyond `internetClient` and
  restricted `runFullTrust`.
- Any app/root `package-lock.json` in final tracked package roots.

## Generation Result

- PASS: ran exactly
  `NPM_CONFIG_PACKAGE_LOCK=false pnpm --dir apps/cbbs-windows exec react-native init-windows --template cpp-app --name CbbsWindows --namespace Cbbs.Windows --no-telemetry`.
- PASS: no `--overwrite` was passed and no overwrite prompt appeared.
- PASS: generated files were new and confined to `apps/cbbs-windows`.
- PASS: generated app-root files were `NuGet.config`,
  `jest.config.windows.js`, and `metro.config.js`.
- PASS: generated native files were under `apps/cbbs-windows/windows/**`.
- PASS: final package-root scan found no `package-lock.json`.
- PASS: generated `Package.appxmanifest` capabilities were exactly
  `internetClient` and restricted `runFullTrust`.
- PASS: no generated build output, signing material, Store association,
  `.appx`, `.msix`, `.pfx`, `.cer`, `.snk`, `bin/`, `obj/`, `.vs/`, or
  `AppPackages/` artifact was found.
- PASS: RNW-generated `windows` script was removed before acceptance; package
  scripts contain no `run-windows` or `init-windows` command.
- NOTE: RNW template `postInstall` reported internal dependency install
  failure and suggested `npm i`; this was not followed. Dependency state was
  reconciled through `pnpm install --lockfile-only` and
  `pnpm install --frozen-lockfile`.

## Validation

Pre-generation baseline passed for the W3A/no-native state:

- PASS: `pnpm install --frozen-lockfile`.
- PASS: `pnpm typecheck`.
- PASS: `pnpm --filter @cbbs/windows-spike typecheck`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_react_native_scaffold`.
- PASS: no app native folders were present.

Post-generation validation passed:

- PASS: `pnpm install --lockfile-only`.
- PASS: `pnpm install --frozen-lockfile`.
- PASS: `pnpm lint`.
- PASS: `pnpm typecheck`.
- PASS: `pnpm test` - 5 suites, 27 tests.
- PASS: `pnpm --filter @cbbs/client exec expo-doctor` - 21/21 checks.
- PASS: `pnpm --filter @cbbs/windows-spike typecheck`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_react_native_scaffold`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py` after
  narrowly allowlisting the seven RNW template package PNG assets.
- PASS: no package-lock scan, no generated build/signing artifact scan, no
  W4 package-script scan, and `git diff --check`.

## Authority Limits

W3B does not authorize RNW build/run, package identity acceptance, capability
use, signing, store packaging, App Center, EAS, release, Git publication,
live connectivity, or hardware behavior.

## Decision

Decision accepted: `cbbs_react_native_windows_w3b_native_generation`.
The app-local RNW `cpp-app` native project is generated and statically audited.
This is not RNW build/run/runtime proof. Next gate: W4 build-only planning
requires separate explicit authority, source refresh, reviewer quorum, and
closed launch/deploy/signing/live surfaces.

## Handoff

Handoff:
[../handoffs/0115-cbbs-react-native-windows-w3b-native-generation-to-qa.md](../handoffs/0115-cbbs-react-native-windows-w3b-native-generation-to-qa.md)
