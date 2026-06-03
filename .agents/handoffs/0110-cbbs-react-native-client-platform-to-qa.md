# Handoff 0110: CBBS React Native Client Platform To QA

Date: 2026-06-02

From: Agent Operations / Architect

To: QA, DevEx/CI, Source Research, UI/UX, Protocol, Security/Safety

## Summary

Task 0149 accepts `ADR-0010` and creates the initial host-only CBBS React
Native client/operator scaffold. The approved lane uses Expo SDK 56 and React
Native 0.85 for Android/iOS/browser fixture work, with a separate RNW
docs/stub-only Windows spike. The scaffold keeps native folders, EAS, App
Center, live connectivity, firmware, hardware, release, and publication
surfaces closed.

## Continue With

- Review `scripts/scaffold_audit_react_native.py` and the package tests for
  role/view/intent parity, no-secret recursion, oversize rejection, unsafe
  intent rejection, and no native folders.
- Treat `compose_draft`, `queue_file_request`, and `ack_local` as local
  fixture/draft intents only.
- Keep browser export proof as the next host-only gate if requested.
- Keep Android/iOS simulator/device work, native builds, RNW native builds,
  EAS, App Center, live local-network/BLE/serial work, release, and publication
  as separate gates.

## Boundaries

No native prebuild, native folders, native builds, simulator/device runs, Expo
Go proof, EAS cloud/local builds, EAS Submit, EAS Update, EAS Hosting, App
Center SDKs or automation, signing credentials, store upload, GitHub
publication, release, BLE pairing, Web Bluetooth, Web Serial, local-network
discovery, SoftAP probing, live bridge traffic, serial writes, firmware ABI
changes, bridge ABI changes, Gate F service-code changes, flash, erase,
monitor, RF/XBee action, router/admin mutation, relay, MicroSD, TFT, wiring,
load, mains, commit, push, PR, or deploy is authorized by this handoff.

## Evidence

- ADR:
  [../DECISIONS/ADR-0010-cbbs-react-native-client-platform.md](../DECISIONS/ADR-0010-cbbs-react-native-client-platform.md)
- Task record:
  [../TASK_LOG/0149-cbbs-react-native-client-platform.md](../TASK_LOG/0149-cbbs-react-native-client-platform.md)
- Source ledger:
  [../../knowledge-base/source-ledger/2026-06-02-cbbs-react-native-client-platform.md](../../knowledge-base/source-ledger/2026-06-02-cbbs-react-native-client-platform.md)
- Project docs:
  [../../docs/projects/cbbs-react-native/README.md](../../docs/projects/cbbs-react-native/README.md)
- Source ID:
  `SRC-LOCAL-CBBS-REACT-NATIVE-CLIENT-PLATFORM-2026-06-02`
