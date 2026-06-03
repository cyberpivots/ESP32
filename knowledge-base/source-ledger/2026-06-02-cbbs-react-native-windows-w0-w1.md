# CBBS React Native Windows W0/W1 Ledger

Date: 2026-06-02

Source ID:
`SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W0-W1-2026-06-02`

## Scope

Tier 2 governance, source-record, host-only protocol/UI, tooling, and CI
hardening for the CBBS React Native Windows Client/Sysop planning lane. This
record amends `ADR-0010` for Windows W0/W1 only and does not open RNW
dependency, native Windows, live transport, hardware, external service, or
release authority.

## Source Coverage

- RNW `0.83` support remains sourced by
  `SRC-REACT-NATIVE-WINDOWS-SUPPORT-2026-06-02`.
- RNW Windows development prerequisites and OS compatibility are sourced by
  `SRC-REACT-NATIVE-WINDOWS-DEPENDENCIES-2026-06-02`.
- RNW getting-started dependency/native-init/run/build/package context is
  sourced by `SRC-REACT-NATIVE-WINDOWS-GETTING-STARTED-2026-06-02`.
- RNW CLI `init-windows`, `run-windows`, `cpp-app`, `--overwrite`, and
  `--no-telemetry` planning is sourced by
  `SRC-REACT-NATIVE-WINDOWS-CLI-2026-06-02`.
- Windows capability/package-manifest planning is sourced by
  `SRC-WINDOWS-APP-CAPABILITIES-2026-06-02`.
- Existing Expo/RN/App Center/platform-permission source coverage remains in
  `SRC-LOCAL-CBBS-REACT-NATIVE-CLIENT-PLATFORM-2026-06-02`.

## Verified Facts

- `ADR-0010` is accepted for CBBS client/operator app work only.
- The Windows W0/W1 amendment permits only host-only records, TypeScript source
  models, fixtures, UI render tests, protocol tests, audit policy, and CI
  validation.
- `apps/cbbs-windows` remains TypeScript-only with no generated `windows/`
  native project.
- W1 protocol validation requires exact top-level UI-intent keys, mandatory
  `localOnlyReason === "fixture-only-ui-intent"`, forbidden metadata-key
  rejection, optional-string validation, and a 512-byte payload bound.
- Fixture closed surfaces are generated from protocol constants and rendered
  as disabled UI controls.
- The Windows Client/Sysop product model remains one role-aware app, not
  separate binaries or package identities.
- CI now includes frozen-lockfile pnpm validation for the React Native
  workspace.

## Assumptions

- W0/W1 proof is package/source validation only.
- Windows native runner/toolchain proof must happen on a Windows host in a
  later gate.
- RNW dependency selection remains separate from the Expo React Native `0.85`
  lane and must not be inferred from this host-only source model.

## Unknowns

- Local Windows 10/11 host identity and RNW toolchain status are unverified.
- Visual Studio 2022 workloads/components, Windows SDK, .NET SDK, Developer
  Mode, Node version, and long-path configuration are unproven locally.
- Windows package identity, capabilities, signing, Store packaging, and
  runtime screenshot proof remain unresolved.
- Live CBBS transport, serial/RF/BLE/local-network behavior, firmware/bridge
  ABI behavior, and hardware acceptance remain separate proof lanes.

## Authority Limits

No `react-native-windows` dependency, RNW CLI execution, `init-windows`,
`run-windows`, native `windows/` folder, Visual Studio/MSBuild, Windows
Package.appxmanifest, package identity, capability declaration, signing,
installer/store packaging, EAS, App Center, simulator/device launch, live
network, BLE, Web Bluetooth, Web Serial, local-network discovery, SoftAP,
serial write, RF/XBee action, firmware ABI change, bridge ABI change, serial
ABI change, Gate F service-code change, flash, erase, monitor, relay, load,
mains, release, commit, push, PR, or deploy is authorized by this record.

## Validation

- PASS: `pnpm install --frozen-lockfile`.
  - Note: pnpm reported ignored dependency build scripts for
    `msgpackr-extract` and `unrs-resolver`; no native project, RNW CLI, EAS,
    App Center, device, or live command was run.
- PASS: `pnpm lint`.
- PASS: `pnpm typecheck`.
- PASS: `pnpm test` (5 suites, 22 tests).
- PASS: `pnpm --filter @cbbs/windows-spike typecheck`.
- PASS: `pnpm --filter @cbbs/client exec expo-doctor` (21/21 checks).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`.
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_react_native_scaffold tests.scaffold_audits.test_agent_process_classifiers tests.scaffold_audits.test_agent_process_decision`
  (18 tests).
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`.
- PASS: `git diff --check`.

## Decision

Decision: accept W0/W1 host-only Windows Client/Sysop
records/source/tests/audits/CI only; keep W2-W5, native, live,
external-service, hardware, and release gates closed.
