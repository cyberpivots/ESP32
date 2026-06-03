# CBBS React Native Windows W2 Dependency Lane Ledger

Date: 2026-06-02

Source ID:
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W2-2026-06-02`

## Scope

Tier 2 package-only RNW dependency-lane work for `apps/cbbs-windows`. This
record opens W2 only after the W2 read-only reviewer quorum. It does not open
native Windows generation, RNW CLI, Windows toolchain, live transport, external
service, hardware, or release authority.

## Source Coverage

- RNW `0.83` support remains sourced by
  `SRC-REACT-NATIVE-WINDOWS-SUPPORT-2026-06-02`.
- RNW dependency and Windows host prerequisites remain sourced by
  `SRC-REACT-NATIVE-WINDOWS-DEPENDENCIES-2026-06-02` and
  `SRC-REACT-NATIVE-WINDOWS-GETTING-STARTED-2026-06-02`.
- RNW CLI/native command planning remains sourced by
  `SRC-REACT-NATIVE-WINDOWS-CLI-2026-06-02` and stays closed.
- Exact npm package metadata for W2 is sourced by
  `SRC-NPM-RNW-DEPENDENCY-METADATA-2026-06-02`.

## Verified Facts

- `ADR-0010` now has a W2 package-only amendment.
- `react-native-windows@0.83.0` peers on `react-native ^0.83.0`,
  `react ^19.2.0`, and `@types/react ^19.1.1`.
- React Native `0.83.9` is the current `0.83.x` patch observed from npm
  metadata in this session.
- React `19.2.3` exists and satisfies the RNW peer range.
- The Expo lane remains `apps/cbbs-client` with React Native `0.85.3`; W2 does
  not alter it.
- W2 package isolation is proven by manifests, lockfile importer checks, audit
  rules, and import-boundary tests, not by physical `node_modules` separation.

## Assumptions

- W2 dependency validation on Linux/WSL is useful for package graph and
  TypeScript boundaries but cannot prove RNW native build/run behavior.
- `apps/cbbs-windows` remains local source/test code until W3 native generation
  is explicitly opened.
- `@cbbs/ui` remains Expo/RN `0.85.3` oriented and is not consumed by the W2
  Windows lane.

## Unknowns

- Local Windows 10/11 host identity and RNW toolchain status are unverified.
- Visual Studio 2022 workloads/components, Windows SDK, .NET SDK, Developer
  Mode, Node version on Windows, long-path configuration, and runner behavior
  are unproven.
- Windows package identity, capabilities, signing, Store packaging, and runtime
  screenshot proof remain unresolved.
- Live CBBS transport, serial/RF/BLE/local-network behavior, firmware/bridge
  ABI behavior, and hardware acceptance remain separate proof lanes.

## Authority Limits

No RNW CLI execution, `init-windows`, `run-windows`, native `windows/` folder,
Visual Studio/MSBuild, Windows Package.appxmanifest, package identity,
capability declaration, signing, installer/store packaging, EAS, App Center,
simulator/device launch, live network, BLE, Web Bluetooth, Web Serial,
local-network discovery, SoftAP, serial write, RF/XBee action, firmware ABI
change, bridge ABI change, serial ABI change, Gate F service-code change,
flash, erase, monitor, relay, load, mains, release, commit, push, PR, or deploy
is authorized by this record.

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
`msgpackr-extract` and `unrs-resolver`. These warnings are recorded as W2
DevEx evidence and do not prove or authorize native Windows generation,
Windows build/run, signing, release, or live behavior.

## Decision

Decision accepted: W2 package-only RNW dependency-lane selection for
`apps/cbbs-windows` is complete. W3-W5/native/live/release gates remain
closed.
