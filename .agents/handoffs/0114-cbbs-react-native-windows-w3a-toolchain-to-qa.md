# Handoff 0114: CBBS React Native Windows W3A Toolchain To QA

Date: 2026-06-03

From: Agent Operations / Tooling

To: QA, React Native DevEx/CI, Source Research, Security/Safety

## Summary

Task 0154 completed the Windows host/toolchain preflight for the CBBS React
Native Windows lane. The RNW 0.83 package-local dependency script now passes
all mandatory checks after installing Yarn through the package-local script,
adding Yarn's MSI bin directory to the Windows user PATH, and enabling the
repo-pinned Corepack pnpm shim.

## Verified Facts

- Package-local script:
  `node_modules/react-native-windows/Scripts/rnw-dependencies.ps1`.
- Package-local script SHA-256:
  `3579E330746598B44B858DD6DFA919CC11FCA944D3539C42ECA5BA5B8BBF6067`.
- The floating public `aka.ms` dependency script had drifted to VS 2026/.NET
  10 checks and was not used for install/config.
- Post-remediation package-local check passed Windows version, Developer Mode,
  long paths, Visual Studio 2022 components, Node `v24.12.0`, Yarn `1.22.22`,
  and .NET SDK `8.0.421`.
- Windows `pnpm` resolves through Corepack to `10.15.0`.
- No app native Windows project was generated.
- Package-local RNW 0.83 `cpp-app` `postInstall` is not confined to
  `windows/`: it updates `package.json` and runs an install.

## Continue With

- Review W3A as toolchain proof only, not RNW native generation/build proof.
- Before W3 native generation, require an accepted W3 amendment or task record
  that opens only `apps/cbbs-windows/windows`, updates the audit boundary, and
  states the exact `init-windows --no-telemetry` no-overwrite command; if the
  default CLI path remains necessary, expand the reviewed boundary to include
  package/lockfile effects.
- Stop if the CLI requires `--overwrite`, if generated files leave the named
  boundary, or if a generated manifest requests capabilities beyond inert
  template defaults.

## Boundaries

No RNW CLI `init-windows`, `run-windows`, MSBuild build, Visual Studio launch,
deploy, package, signing, release, EAS, App Center, live network, BLE,
Web Bluetooth, Web Serial, serial/RF/XBee, firmware/bridge/serial ABI change,
flash, erase, monitor, relay, load, mains, commit, push, PR, or deployment is
authorized by this handoff.

## Evidence

- Task record:
  [../TASK_LOG/0154-cbbs-react-native-windows-w3a-toolchain-preflight.md](../TASK_LOG/0154-cbbs-react-native-windows-w3a-toolchain-preflight.md)
- Source ledger:
  [../../knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-w3a.md](../../knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-w3a.md)
- Source IDs:
  `SRC-REACT-NATIVE-WINDOWS-PACKAGE-DEPS-2026-06-03`,
  `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W3A-2026-06-03`
