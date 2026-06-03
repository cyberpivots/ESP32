# Handoff 0111: CBBS React Native Windows Client/Sysop W0/W1 To QA

Date: 2026-06-02

From: Agent Operations / Architect

To: QA, DevEx/CI, Source Research, UI/UX, Protocol, Security/Safety

## Summary

Task 0150 amends `ADR-0010` for Windows W0/W1 host-only work and hardens the
CBBS React Native fixture lane for one role-aware Client/Sysop Windows app
model. The work remains TypeScript/source/test only: no RNW dependency, native
Windows project, Windows runner, Visual Studio build, package identity,
capabilities, signing, live transport, hardware, external service, release, or
publication authority is opened.

## Continue With

- Review the exact UI intent validator for allowed-key, metadata-key,
  `localOnlyReason`, optional-string, 512-byte, secret-like, and live-action
  rejection coverage.
- Review fixture/protocol/UI closed-surface parity.
- Review `OperatorShell` Client/Sysop role profile rendering, deterministic
  accessibility/test IDs, disabled unsafe controls, and transcript-first proof
  wording.
- Review `apps/cbbs-windows` as a TypeScript-only source model; do not treat it
  as an RNW native project.
- Keep CI using frozen-lockfile pnpm validation and lockfile-bound Expo Doctor.

## Boundaries

No `react-native-windows` dependency, RNW CLI execution, `init-windows`,
`run-windows`, native `windows/` folder, Visual Studio/MSBuild, Windows
Package.appxmanifest, package identity, capability declaration, signing,
installer/store packaging, EAS, App Center, simulator/device launch, live
network, BLE, Web Bluetooth, Web Serial, local-network discovery, SoftAP,
serial write, RF/XBee action, firmware ABI change, bridge ABI change, serial
ABI change, Gate F service-code change, flash, erase, monitor, relay, load,
mains, release, commit, push, PR, or deploy is authorized by this handoff.

## Evidence

- ADR:
  [../DECISIONS/ADR-0010-cbbs-react-native-client-platform.md](../DECISIONS/ADR-0010-cbbs-react-native-client-platform.md)
- Task record:
  [../TASK_LOG/0150-cbbs-react-native-windows-client-sysop-w0-w1.md](../TASK_LOG/0150-cbbs-react-native-windows-client-sysop-w0-w1.md)
- Source ledger:
  [../../knowledge-base/source-ledger/2026-06-02-cbbs-react-native-windows-w0-w1.md](../../knowledge-base/source-ledger/2026-06-02-cbbs-react-native-windows-w0-w1.md)
- Project docs:
  [../../docs/projects/cbbs-react-native/README.md](../../docs/projects/cbbs-react-native/README.md)
- Source ID:
  `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W0-W1-2026-06-02`
