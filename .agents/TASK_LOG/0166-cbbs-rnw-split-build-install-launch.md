# Task 0166: CBBS RNW Split Build Install Launch

Status: completed for local review; cleanup deferred by review need

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-04

Source IDs:
`SRC-LOCAL-CBBS-RNW-SPLIT-BUILD-INSTALL-LAUNCH-2026-06-04`

## Routing

- Verified facts: Task 0163 generated split RNW native source trees for
  `CbbsClientWindows`, `CbbsSysopWindows`, and
  `CbbsHardwareToolsWindows`, but did not authorize build, deploy, install, or
  launch. The current user request explicitly authorizes local Windows 11
  build/install/launch for review and testing.
- Assumptions: "install" means local RNW debug deploy/install through
  `react-native run-windows --no-telemetry`, not signing, Store/App Installer
  packaging, release, publication, or final package identity acceptance.
- Unknowns: current Windows toolchain state, split app runtime behavior,
  package full names, final package identities, capability-use acceptance,
  signing path, Store/App Installer path, installed debug package retention,
  and post-launch generated-output cleanup remain unresolved until proof is
  captured.
- Selected tier: Tier 3 local RNW runtime gate.
- Owner role: React Native Windows DevEx/runtime with QA, live-bench,
  protocol/bridge, safety/security, and KB/source-record lenses.
- Evidence need: reviewer quorum outputs, same-session Windows host/toolchain
  inventory, dirty-tree boundary, static no-dispatch scan, package-script and
  manifest inspection, command transcripts, process/window/package proof,
  screenshots after loaded UI, screenshot hashes/dimensions, generated-output
  inventory, and explicit closed-surface proof.
- Mutation boundary: local Debug build outputs, local Windows debug package
  deploy/install/start state, Metro/Node/MSBuild processes started by
  `run-windows`, local evidence artifacts, and this task/source/handoff record.
- Reviewer quorum: coordinator, RNW DevEx/CI, live-bench, protocol/bridge,
  safety/security, and QA reviewers were spawned, waited, captured, and closed.
  Coordinator and DevEx approved the bounded local debug runtime gate with
  conditions. QA, live-bench, protocol, and safety reviewers required
  same-session evidence, no-dispatch proof, and closed live/hardware surfaces
  before acceptance.
- Gate authority: the user explicitly authorized build/install/launch of the
  RNW applications on this Windows 11 PC for review and testing. This opens
  only the bounded local debug runtime gate below.
- Validation plan: run preflight typecheck/test/audit commands, static
  no-dispatch scans, Windows host inventory, then run each split app one at a
  time with `--no-telemetry` and capture transcript/process/package/screenshot
  evidence.
- Trust boundary: successful local debug launch proves only local RNW runtime
  review readiness. It does not accept final package identity, capability use,
  signing, Store/App Installer distribution, release, live bridge dispatch, or
  any hardware action.

## Approved Commands

Preflight:

```bash
pnpm --filter @cbbs/client-windows typecheck
pnpm --filter @cbbs/client-windows test:windows
pnpm --filter @cbbs/sysop-windows typecheck
pnpm --filter @cbbs/sysop-windows test:windows
pnpm --filter @cbbs/hardware-tools-windows typecheck
pnpm --filter @cbbs/hardware-tools-windows test:windows
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py
```

Runtime proof, one app at a time:

```bash
pnpm --dir apps/cbbs-client-windows exec react-native run-windows --root . --sln windows\\CbbsClientWindows.sln --proj windows\\CbbsClientWindows\\CbbsClientWindows.vcxproj --arch x64 --no-telemetry
pnpm --dir apps/cbbs-sysop-windows exec react-native run-windows --root . --sln windows\\CbbsSysopWindows.sln --proj windows\\CbbsSysopWindows\\CbbsSysopWindows.vcxproj --arch x64 --no-telemetry
pnpm --dir apps/cbbs-hardware-tools-windows exec react-native run-windows --root . --sln windows\\CbbsHardwareToolsWindows.sln --proj windows\\CbbsHardwareToolsWindows\\CbbsHardwareToolsWindows.vcxproj --arch x64 --no-telemetry
```

## Closed Surfaces

Still closed: native HostCommandBridge implementation or dispatch, shell or
DOS-C execution, serial port open/write, RF/XBee writes or transmit,
firmware flash/erase/monitor, relay/load/mains work, wiring, BLE/Web
Serial/Web Bluetooth, SoftAP or local-network discovery, signing certificates,
Store/App Installer association, package creation for distribution, EAS, App
Center, credentials/key material, commit, push, PR, deploy, and release.

## Recovery Path

If review/testing must be cleaned up, stop local split app processes, stop
Metro/Node/MSBuild trees started by this gate, and remove only the local debug
packages for `CbbsClientWindows`, `CbbsSysopWindows`, and
`CbbsHardwareToolsWindows` if package retention is not desired. Do not remove
source files or generated native source trees without a separate mutation gate.

## Validation

- Same-session Windows host/toolchain inventory captured: Windows 11 Pro
  `10.0.26200`, Node `v24.12.0`, pnpm `10.15.0`, Yarn `1.22.22`, .NET SDK
  `8.0.421` plus newer SDKs, and Visual Studio 2022 `17.14.37301.10`.
- Preflight passed before runtime launch:
  `pnpm --filter @cbbs/client-windows typecheck`,
  `pnpm --filter @cbbs/sysop-windows typecheck`,
  `pnpm --filter @cbbs/hardware-tools-windows typecheck`,
  all three split app `test:windows` suites, and
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`.
- Static no-dispatch scan found only expected inert bridge contract, closed
  surface vocabulary, and tests. Package-script scan found no app-local
  `run-windows`, MSBuild, deploy, install, signing, release, Store/App
  Installer, App Center, EAS, serial, XBee, flash, relay, push, or PR scripts.
- Manifest scan confirmed generated debug identity facts only:
  `Publisher="CN=cyber"`, `Version="1.0.0.0"`, `internetClient`, and restricted
  `runFullTrust`.
- First Client launch built/deployed/started but produced a loading-only
  screenshot. Metro returned HTTP 500 because the split app Metro configs lacked
  the monorepo resolver settings used by the working compatibility app.
- Added app-local split Metro resolver configs and
  `metro-shims/reactDevToolsSettingsManager.windows.js` for Client, Sysop, and
  Hardware Tools. Post-fix split app `test:windows` suites passed.
- Post-fix Client proof passed:
  `client-screenshot-final.png`, 2560x1600, SHA-256
  `F553980CA92AEF5FAA8C33E81A1CB5D72B6933F6903DF9DEA83CB3E585E1CAC4`,
  visible `CBBS Client`, no redbox, no loading-only state.
- Sysop first proof was rejected because stale Client Metro served a Client
  bundle and produced a redbox. After stopping the stale Metro server and
  restarting Sysop with its own server, Sysop proof passed:
  `sysop-screenshot-final.png`, 2560x1600, SHA-256
  `8DBF5CDF5854317D84E875065D51B860AC117116D8BDE9E91025E2598F722003`,
  visible `CBBS Sysop`, no redbox, no loading-only state.
- Hardware Tools proof passed:
  `hardware-tools-screenshot.png`, 2560x1600, SHA-256
  `88295B3D29F34FB0C86C1DD64898F7FAF44D04A261737B2436A48C4CC4B5A9F4`,
  visible `CBBS Hardware Tools`, no redbox, no loading-only state.
- Installed local debug package facts captured:
  `CbbsClientWindows_1.0.0.0_x64__2g54mg31548kg`,
  `CbbsSysopWindows_1.0.0.0_x64__2g54mg31548kg`, and
  `CbbsHardwareToolsWindows_1.0.0.0_x64__2g54mg31548kg`. These remain local
  debug facts only, not accepted package identities.
- Final process proof captured all three app processes responding:
  `CbbsClientWindows`, `CbbsSysopWindows`, and
  `CbbsHardwareToolsWindows`.
- Metro/Node/cmd worker cleanup proof captured: final Metro status is closed
  and no Metro worker targets remained. The three app windows were intentionally
  left running for user review/testing.
- Generated output inventory after runtime contains 5,983 Debug/obj/bin entries
  across the split native app roots. This is expected runtime output and is not
  source acceptance. Post-run `scripts/scaffold_audit_react_native.py` is
  expected to fail until those generated outputs are cleaned.
- `git diff --check` passed after the source and record updates.
- Evidence artifacts are local and ignored under
  `research/bench-records/react-native-windows/cbbs-rnw-split-runtime-20260604T052309Z/`.

## Retained Local State

The following state is intentionally retained for user review/testing:

- Three open app windows: `CbbsClientWindows`, `CbbsSysopWindows`, and
  `CbbsHardwareToolsWindows`.
- Three local debug packages installed from app-local Debug layouts.
- Generated Debug/obj/bin output under the three split `windows/` roots.

Metro/Node/cmd worker processes started by the launch gate were stopped.

## Decision

Decision: local Windows 11 debug build/deploy/install/launch is accepted for
user review/testing for `CbbsClientWindows`, `CbbsSysopWindows`, and
`CbbsHardwareToolsWindows`. This acceptance is limited to local debug runtime
proof. Generated Debug output, local debug packages, and the three open app
windows are retained intentionally until review/testing is complete.

## Handoff

Handoff:
[../handoffs/0125-cbbs-rnw-split-build-install-launch-to-qa.md](../handoffs/0125-cbbs-rnw-split-build-install-launch-to-qa.md)
