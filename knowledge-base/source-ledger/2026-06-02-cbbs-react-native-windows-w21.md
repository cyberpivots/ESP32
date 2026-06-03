# CBBS React Native Windows W2.1 Local Shell Ledger

Date: 2026-06-02

Source ID:
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W21-2026-06-02`

## Scope

Tier 2 W2.1 package-only Windows app source/testability work for
`apps/cbbs-windows`. This record continues W2 only. It does not open native
Windows project generation, RNW CLI execution, Windows build/run, live
transport, hardware, publication, or release authority.

## Source Coverage

- W2 package-only authority remains sourced by
  `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W2-2026-06-02`.
- Exact W2 dependency metadata remains sourced by
  `SRC-NPM-RNW-DEPENDENCY-METADATA-2026-06-02`.
- RNW native/toolchain prerequisites remain sourced by
  `SRC-REACT-NATIVE-WINDOWS-DEPENDENCIES-2026-06-02`,
  `SRC-REACT-NATIVE-WINDOWS-GETTING-STARTED-2026-06-02`, and
  `SRC-REACT-NATIVE-WINDOWS-CLI-2026-06-02`; those gates remain closed.

## Verified Facts

- `apps/cbbs-windows/src/index.tsx` now exports a
  `WindowsClientSysopShell` built only from React Native primitives and shared
  protocol constants.
- Windows local intents are created through `createWindowsLocalIntent`, which
  delegates to `@cbbs/protocol` `localIntent` and preserves
  `LOCAL_ONLY_REASON`.
- Windows closed-surface controls derive from `CLOSED_SURFACE_IDS` and render
  disabled accessibility state.
- Windows tests now render Client/Sysop local shells, validate emitted local
  intents, assert closed-surface disabled state, and preserve transcript-first
  evidence wording.
- `apps/cbbs-windows` still does not import `@cbbs/ui`, Expo, Expo Router, or
  React Native Web.

## Assumptions

- W2.1 package validation on Linux/WSL is valid host-side source/test proof but
  cannot prove Windows native runtime behavior.
- The Windows app remains a single role-aware Client/Sysop source surface until
  a later packaging/signing decision changes that shape.

## Unknowns

- Windows host/toolchain state, Visual Studio workloads, Windows SDK, .NET SDK,
  Developer Mode, package identity, capability declarations, signing, runtime
  screenshots, and native build/run proof remain unresolved.
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
ignored build scripts for `msgpackr-extract` and `unrs-resolver`. This is W2.1
DevEx evidence only and does not prove or authorize native Windows generation,
Windows build/run, signing, release, or live behavior.

## Decision

Decision accepted: W2 package-only Windows source/test work now includes a
local Client/Sysop shell. W3-W5/native/live/release gates remain closed.
