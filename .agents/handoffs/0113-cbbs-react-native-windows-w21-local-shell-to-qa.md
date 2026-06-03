# Handoff 0113: CBBS React Native Windows W2.1 Local Shell To QA

Date: 2026-06-02

From: Agent Operations / Architect

To: QA, DevEx/CI, UI Parity, Protocol/State, Security/Safety

## Summary

Task 0153 continues W2 package-only Windows development by adding a local
Client/Sysop shell to `apps/cbbs-windows`. The shell uses React Native
primitives and shared `@cbbs/protocol` constants, renders local-only view/action
controls, emits fixture-only intents, shows transcript-first evidence wording,
and renders all closed surfaces as disabled controls.

## Continue With

- Review that `apps/cbbs-windows` still does not import `@cbbs/ui`, Expo, Expo
  Router, React Native Web, live transports, or native build/run helpers.
- Review that local intents use `LOCAL_ONLY_REASON` through `localIntent`.
- Review that closed-surface controls derive from `CLOSED_SURFACE_IDS` and stay
  disabled.
- Treat W2.1 validation as package/source proof only, not RNW build/run proof.
- Keep W3 native generation/build proof behind a separate gate with
  same-session Windows toolchain evidence.

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

- Task record:
  [../TASK_LOG/0153-cbbs-react-native-windows-w21-local-shell.md](../TASK_LOG/0153-cbbs-react-native-windows-w21-local-shell.md)
- Source ledger:
  [../../knowledge-base/source-ledger/2026-06-02-cbbs-react-native-windows-w21.md](../../knowledge-base/source-ledger/2026-06-02-cbbs-react-native-windows-w21.md)
- Project docs:
  [../../docs/projects/cbbs-react-native/README.md](../../docs/projects/cbbs-react-native/README.md)
- Source ID:
  `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W21-2026-06-02`
