# CBBS React Native Windows W3B Native Generation Ledger

Date: 2026-06-03

Source IDs:
`SRC-REACT-NATIVE-WINDOWS-CLI-2026-06-02`,
`SRC-REACT-NATIVE-WINDOWS-CPP-APP-TEMPLATE-2026-06-03`,
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W3A-2026-06-03`,
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W3B-2026-06-03`

## Scope

Tier 3 native-generation gate for `apps/cbbs-windows`. This ledger records
the W3B source, audit boundary, and generated native project result; it does
not prove RNW build/run/runtime, package identity acceptance, signing, release,
live connectivity, or hardware behavior.

## Source Coverage

- Official RNW CLI documentation lists `init-windows` flags including
  `--template`, `--name`, `--namespace`, `--overwrite`, `--no-telemetry`, and
  `--list`, but no no-install or no-package-mutation option.
- Package-local RNW 0.83 CLI source matches that option surface.
- Package-local RNW 0.83 `cpp-app` template source updates package metadata,
  adds Windows scripts and `@rnx-kit/jest-preset`, and runs install.
- Package-local RNW 0.83 install helper chooses Yarn only when app-local
  `yarn.lock` exists; otherwise it runs `npm i`.
- Package-local RNW 0.83 manifest template declares `internetClient` and
  restricted `runFullTrust`.

## Verified Facts

- A W3B command that promises only `apps/cbbs-windows/windows/**` mutations is
  not source-backed.
- The accepted W3B command must be app-scoped with
  `pnpm --dir apps/cbbs-windows exec ...`.
- `NPM_CONFIG_PACKAGE_LOCK=false` is required to contain RNW template internal
  npm install package-lock side effects.
- Final tracked state must not include app/root `package-lock.json`.
- Generated `run-windows` scripts are not accepted because W4 build/run/deploy
  remains closed.
- Generated manifest capabilities may be recorded as template facts only.

## Generated Result

- The W3B command ran exactly as recorded, with
  `NPM_CONFIG_PACKAGE_LOCK=false`, app-scoped `pnpm --dir apps/cbbs-windows`,
  `--no-telemetry`, and no `--overwrite`.
- RNW generated `apps/cbbs-windows/windows/**`, `NuGet.config`,
  `jest.config.windows.js`, and `metro.config.js`.
- RNW updated `apps/cbbs-windows/package.json` with
  `@rnx-kit/jest-preset` and `react-native-windows.init-windows` metadata.
- The generated `windows` package script was removed before acceptance.
- The generated manifest identity is `Name="CbbsWindows"`,
  `Publisher="CN=cyber"`, `Version="1.0.0.0"`. This is recorded as generated
  template output, not package identity acceptance for signing or release.
- Generated capabilities are exactly `internetClient` and restricted
  `runFullTrust`.
- No app/root `package-lock.json`, generated build output, signing material,
  Store association file, `.appx`, `.msix`, `.pfx`, `.cer`, `.snk`, `bin/`,
  `obj/`, `.vs/`, or `AppPackages/` artifact was found.

## Assumptions

- The package-local RNW 0.83 source remains authoritative for the installed
  dependency lane during this same-session W3B gate.
- WSL/Linux validation can prove repository state and static checks, but not
  native Windows build/run/runtime.

## Unknowns

- Exact generated file inventory before the RNW command is run.
- Whether the RNW CLI prompts for overwrite in this monorepo app.
- Generated manifest package identity and publisher values.
- Native Windows build/run/runtime behavior.

## Validation

W3B audit requirements:

- Allow `apps/cbbs-windows/windows/**` only with W3B records present.
- Inspect generated native files for build outputs, signing/package artifacts,
  store association files, and unexpected capabilities.
- Fail package scripts containing `run-windows`, `init-windows`, MSBuild,
  signing, release, EAS, App Center, or deploy commands.
- Fail app/root `package-lock.json`.
- Keep RNW dependencies scoped to `apps/cbbs-windows`.

Validation passed with pnpm lockfile reconciliation, frozen install, lint,
typecheck, Jest, Expo Doctor, Windows typecheck, React Native scaffold audit,
targeted scaffold unit tests, durable-record audit, agent-process audit, skill
audit, full scaffold verification, no-package-lock scan, no W4 package-script
scan, no build/signing artifact scan, and `git diff --check`.

## Authority Limits

No RNW `run-windows`, Visual Studio/MSBuild build, deploy, package identity
acceptance, capability use, signing, store packaging, EAS, App Center,
simulator/device launch, live network, BLE, Web Bluetooth, Web Serial,
local-network discovery, SoftAP, serial/RF/XBee action, firmware/bridge/serial
ABI change, flash, erase, monitor, relay, load, mains, release, commit, push,
PR, or deploy is authorized by this record.
