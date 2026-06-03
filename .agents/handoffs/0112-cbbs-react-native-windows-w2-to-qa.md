# Handoff 0112: CBBS React Native Windows W2 To QA

Date: 2026-06-02

From: Agent Operations / Architect

To: QA, DevEx/CI, Source Research, Protocol/State, Security/Safety

## Summary

Task 0151 opens the W2 package-only RNW dependency lane for
`apps/cbbs-windows`. The lane selects RNW/RN dependencies only for the Windows
package and adds audit/test coverage for dependency, import, lockfile, and
closed-surface isolation. It does not create a native Windows project or prove
Windows runtime behavior.

## Continue With

- Review that `react-native-windows` is scoped to `apps/cbbs-windows` and
  remains `0.83.x`.
- Review that the Expo lane stays on `apps/cbbs-client` React Native `0.85.3`
  and no RNW dependency or import leaks into root/shared/client packages.
- Review that `apps/cbbs-windows` does not import `@cbbs/ui`, Expo,
  Expo Router, React Native Web, live transports, or native build/run helpers.
- Review no-native-folder and script/config blockers before any W3 discussion.
- Treat W2 validation as package/source proof only, not RNW build/run proof.

## Boundaries

No RNW CLI execution, `init-windows`, `run-windows`, native `windows/` folder,
Visual Studio/MSBuild, Windows Package.appxmanifest, package identity,
capability declaration, signing, installer/store packaging, EAS, App Center,
simulator/device launch, live network, BLE, Web Bluetooth, Web Serial,
local-network discovery, SoftAP, serial write, RF/XBee action, firmware ABI
change, bridge ABI change, serial ABI change, Gate F service-code change,
flash, erase, monitor, relay, load, mains, release, commit, push, PR, or deploy
is authorized by this handoff.

## Evidence

- ADR:
  [../DECISIONS/ADR-0010-cbbs-react-native-client-platform.md](../DECISIONS/ADR-0010-cbbs-react-native-client-platform.md)
- Task record:
  [../TASK_LOG/0151-cbbs-react-native-windows-w2-dependency-lane.md](../TASK_LOG/0151-cbbs-react-native-windows-w2-dependency-lane.md)
- Source ledger:
  [../../knowledge-base/source-ledger/2026-06-02-cbbs-react-native-windows-w2.md](../../knowledge-base/source-ledger/2026-06-02-cbbs-react-native-windows-w2.md)
- Project docs:
  [../../docs/projects/cbbs-react-native/README.md](../../docs/projects/cbbs-react-native/README.md)
- Source ID:
  `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W2-2026-06-02`
