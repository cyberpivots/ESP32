---
name: react-native-client-development
description: Use for CBBS React Native client/operator app work in this ESP32 workspace, including ADR/source checks, host-only Expo fixtures, pnpm validation, native-folder absence, and closed live connectivity/release gates.
---

# React Native Client Development

1. Re-read `AGENTS.md`, `ADR-0010`, `docs/projects/cbbs-react-native/README.md`,
   and `knowledge-base/source-ledger/2026-06-02-cbbs-react-native-client-platform.md`.
2. Keep verified facts, assumptions, and unknowns separate in records.
3. Confirm source IDs before changing React Native, Expo, RNW, App Center,
   Android/iOS permission, or EAS claims.
4. Keep Phase 1/2 host-only: fixtures only, no native `android/`, `ios/`, or
   `windows/` folders, no `expo prebuild`, no EAS, no App Center, no signing,
   no simulator/device run, and no live connectivity.
5. Treat UI intents as local-only. Do not map `compose_draft`,
   `queue_file_request`, `ack_local`, or `refresh` to transport side effects.
6. Run `python3 scripts/scaffold_audit_react_native.py` after scaffold changes.

Closed surfaces: BLE pairing, Web Bluetooth, Web Serial, LAN/SoftAP discovery,
serial writes, RF/XBee, flash, erase, monitor, relay, MicroSD, TFT, wiring,
load, mains, release, deploy, push, PR, and external-service automation.
