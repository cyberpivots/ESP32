# CBBS RNW Split Native Generation Ledger

Date: 2026-06-04

Source ID:
`SRC-LOCAL-CBBS-RNW-SPLIT-NATIVE-GENERATION-2026-06-04`

## Scope

Tier 3-prep source generation for split React Native Windows native project
trees under the Client, Sysop, and Hardware Tools app packages.

This record does not prove native runtime behavior and does not authorize
bridge dispatch, hardware actions, signing, release, or publication.

## Verified Facts

- The three split app packages already registered the component names
  `CbbsClientWindows`, `CbbsSysopWindows`, and `CbbsHardwareToolsWindows`.
- Before this task, only `apps/cbbs-windows/windows` had a generated native
  RNW project.
- The reviewer quorum approved only records plus split-native source
  generation. Runtime launch, live bridge dispatch, and XBee writes were
  rejected by the same quorum.

## Assumptions

- RNW `cpp-app` generation for split app packages follows the same app-local
  boundary as the accepted compatibility W3B generation, with package-lock
  suppression and package metadata reconciliation.
- Generated manifest identity and capability values are template/debug facts
  only and are not package identity or capability-use acceptance.

## Unknowns

- Native runtime behavior for all three split apps.
- Final package identities, icons, accepted capabilities, signing,
  Store/App Installer packaging, App Center/EAS exclusion beyond static audit,
  and release path.
- Native HostCommandBridge ABI/implementation and live adapter behavior.

## Reviewer Quorum

- Coordinator, weight 5: approved only records plus split-native source
  generation.
- RNW DevEx/CI, weight 3: required an ADR/gate amendment and split-native
  audit coverage before generation.
- QA, weight 3: approved source/records and generation-only after gate records;
  blocked runtime/live work.
- Protocol/bridge, weight 3: blocked live dispatch and kept v1 unavailable.
- XBee/radio, weight 3: blocked radio writes without same-session evidence.
- Live-bench, weight 5: blocked all live/runtime/write surfaces.

Weighted result for records plus split-native source generation: 25/25 approve,
no P1/P2 blockers. Weighted result for live/runtime/write: 0/25 approve.

## Authority Limits

No RNW `run-windows`, MSBuild, deploy, launch, package identity acceptance,
capability-use acceptance, signing, package creation, Store/App Installer
association, native HostCommandBridge implementation, live bridge dispatch,
serial/RF/XBee write, firmware flash, erase, monitor, relay/load/mains work,
wiring, commit, push, PR, deploy, or release is authorized.

## Validation

- Generated `apps/cbbs-client-windows/windows`,
  `apps/cbbs-sysop-windows/windows`, and
  `apps/cbbs-hardware-tools-windows/windows` with app-scoped
  `init-windows --template cpp-app --no-telemetry` commands.
- Removed generated `windows` package scripts before acceptance.
- Reconciled package metadata and `pnpm-lock.yaml` with pnpm.
- Inspected generated manifests: identities are
  `CbbsClientWindows`, `CbbsSysopWindows`, and `CbbsHardwareToolsWindows`,
  each with `Publisher="CN=cyber"` and `Version="1.0.0.0"` as debug template
  facts only. Capabilities are only `internetClient` and restricted
  `runFullTrust`.
- No package-lock, Store association, package/signing artifact, Debug/Release/
  AppPackages/bin/obj output, or binlog was accepted.
- Passed: frozen pnpm install, package typechecks, split app tests, app-local
  Jest config smoke tests, focused protocol/product/product-ui/windows tests,
  RNW generator checks, RNW menu/parity unit tests, root typecheck/lint/full
  Jest, scaffold audits, source-image allowlist regression, `verify_scaffold.py`,
  and `git diff --check`.
- Not run: RNW `run-windows`, MSBuild, deploy, launch, Metro runtime proof,
  live bridge dispatch, serial/RF/XBee writes, flash, monitor, relay/load/mains,
  signing, release, commit, push, PR, or deploy.

Final disposition: accepted only as split-native source generation. Runtime
proof remains closed.
