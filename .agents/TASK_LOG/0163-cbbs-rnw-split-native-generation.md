# Task 0163: CBBS RNW Split Native Generation

Status: completed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-04

Source IDs:
`SRC-LOCAL-CBBS-RNW-SPLIT-NATIVE-GENERATION-2026-06-04`

## Routing

- Verified facts: the branch was clean and aligned with `origin/main` after
  commit `b8535ed`. Split source packages exist for Client, Sysop, and
  Hardware Tools. Only the compatibility app has a native Windows project
  before this task.
- Assumptions: the user request authorizes implementation of the approved plan,
  but reviewer quorum narrows execution to records plus split-native source
  generation before any runtime/live work.
- Unknowns: split runtime behavior, final package identities, accepted
  capabilities, icons, signing path, Store/App Installer path, native
  HostCommandBridge implementation, bridge live adapter, XBee current physical
  state, and release path remain unresolved.
- Selected tier: Tier 3 request with only the approved Tier 3-prep/source
  generation boundary executed.
- Owner role: React Native Windows DevEx with Agent Operations, QA,
  protocol/bridge, live-bench, XBee/radio, and KB/source-record lenses.
- Evidence need: reviewer quorum results, task/handoff/source records, ADR/docs
  gate updates, scaffold audit coverage for split native surfaces, generated
  manifest capability inspection, package-lock/script rejection, and full
  validation output.
- Mutation boundary: `.agents/DECISIONS/ADR-0010-cbbs-react-native-client-platform.md`,
  `docs/projects/cbbs-react-native/README.md`, `apps/cbbs-windows/README.md`,
  `scripts/scaffold_audit_react_native.py`, durable records/indexes, the three
  app-local `windows/` native source trees, app package metadata, and
  `pnpm-lock.yaml` reconciliation.
- Reviewer quorum: coordinator, RNW DevEx/CI, protocol/bridge, XBee/radio,
  live-bench, and QA reviewers were spawned, waited, captured, and closed.
  KB/source-record retry was spawned after lifecycle cleanup, timed out twice,
  then closed as stale; the local KB lens was used as fallback.
- Gate authority: reviewer quorum approved records plus split-native source
  generation only. It did not approve runtime launch, live bridge dispatch, or
  XBee writes.
- Validation plan: run RNW generator checks, split app typechecks/tests,
  package typechecks, scaffold audits, root lint/typecheck/test where feasible,
  package-lock/output scans, manifest inspection, `verify_scaffold.py`, and
  `git diff --check`.
- Trust boundary: generated native project files are source artifacts only.
  Manifest identities/capabilities are debug template facts only.

## Approved Commands

Generation-only commands:

```bash
NPM_CONFIG_PACKAGE_LOCK=false pnpm --dir apps/cbbs-client-windows exec react-native init-windows --template cpp-app --name CbbsClientWindows --namespace Cbbs.Client.Windows --no-telemetry
NPM_CONFIG_PACKAGE_LOCK=false pnpm --dir apps/cbbs-sysop-windows exec react-native init-windows --template cpp-app --name CbbsSysopWindows --namespace Cbbs.Sysop.Windows --no-telemetry
NPM_CONFIG_PACKAGE_LOCK=false pnpm --dir apps/cbbs-hardware-tools-windows exec react-native init-windows --template cpp-app --name CbbsHardwareToolsWindows --namespace Cbbs.HardwareTools.Windows --no-telemetry
```

Stop if a command requires `--overwrite`, creates `package-lock.json`, adds
runtime/build/signing/release scripts, creates build/package/signing outputs,
or adds manifest capabilities outside `internetClient` and restricted
`runFullTrust`.

## Validation

- Generated `CbbsClientWindows`, `CbbsSysopWindows`, and
  `CbbsHardwareToolsWindows` with the approved `init-windows --template cpp-app
  --no-telemetry` commands. Each command printed the RNW CLI's standard
  run-suggestion text, but no build, deploy, launch, or runtime command was
  run.
- `pnpm install --lockfile-only` passed with the existing Expo peer warning.
- `pnpm install --frozen-lockfile` passed; pnpm ignored build scripts for
  `msgpackr-extract` and `unrs-resolver`.
- Removed RNW-generated `windows` package scripts before acceptance.
- Inspected generated manifests: each split app records generated identity
  `Name=<component>`, `Publisher="CN=cyber"`, `Version="1.0.0.0"` and only
  `internetClient` plus restricted `runFullTrust` capabilities.
- Artifact scan found no `package-lock.json`, `.appx`, `.msix`, signing files,
  Store association files, Debug/Release/AppPackages/bin/obj outputs, or
  binlogs outside existing dependency trees.
- Package validation passed:
  `pnpm --filter @cbbs/product typecheck`,
  `pnpm --filter @cbbs/product-ui typecheck`,
  `pnpm --filter @cbbs/client-windows typecheck`,
  `pnpm --filter @cbbs/sysop-windows typecheck`,
  `pnpm --filter @cbbs/hardware-tools-windows typecheck`,
  and `pnpm --filter @cbbs/windows-spike typecheck`.
- Focused Jest passed: split app `test:windows` scripts, app-local
  `jest.config.windows.js` smoke tests, protocol/product/product-ui/windows
  focused suites, and `timeout 180s pnpm test` (10 suites, 59 tests).
- RNW generator checks passed:
  `PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_win31_parity.py --check`,
  `PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_rnw_menu.py --check`,
  and RNW menu/parity unit tests (10 tests).
- Scaffold validation passed:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 155`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`,
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`,
  `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_source_image_scan`,
  and `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- Root validation passed: `pnpm typecheck`, `pnpm lint`, and
  `git diff --check`.
- No RNW `run-windows`, MSBuild, deploy, launch, live bridge dispatch,
  serial/RF/XBee write, firmware flash/erase/monitor, relay/load/mains,
  signing, release, commit, push, PR, or deploy action was performed.

## Authority Limits

No RNW `run-windows`, MSBuild, Visual Studio build, deploy, launch, Metro app
runtime proof, package identity acceptance, capability-use acceptance, signing,
package creation, Store/App Installer association, native HostCommandBridge
implementation, live bridge dispatch, serial/RF/XBee write, firmware flash,
erase, monitor, relay/load/mains work, wiring, commit, push, PR, deploy, or
release is authorized by this task.

## Decision

Decision: split-native source generation is accepted for the named source
boundary. Live/runtime/write gates remain blocked and are recorded separately in
Tasks 0164 and 0165.

## Handoff

Handoff:
[../handoffs/0122-cbbs-rnw-split-native-generation-to-qa.md](../handoffs/0122-cbbs-rnw-split-native-generation-to-qa.md)
