---
name: react-native-client-development
description: Use for CBBS React Native client/operator app work in this ESP32 workspace, including ADR/source checks, host-only Expo fixtures, pnpm validation, native-folder absence, and closed live connectivity/release gates.
---

# React Native Client Development

1. Re-read `AGENTS.md`, `ADR-0010`, `docs/projects/cbbs-react-native/README.md`,
   and `knowledge-base/source-ledger/2026-06-02-cbbs-react-native-client-platform.md`.
   Before CBBS RNW view, action, or protocol changes, also check the current
   local DOS-C Win31 sources: `/mnt/h/dos-c/software/win31-operator/README.md`,
   `/mnt/h/dos-c/software/win31-operator/include/operator_protocol.h`,
   `/mnt/h/dos-c/software/win31-operator/src/operator_protocol.c`, and the
   DOS-C Win31 dashboard vision-gate source.
2. Keep verified facts, assumptions, and unknowns separate in records.
3. Confirm source IDs before changing React Native, Expo, RNW, App Center,
   Android/iOS permission, or EAS claims.
4. Keep Phase 1/2 host-only: fixtures only, no native `android/`, `ios/`, or
   `windows/` folders, no `expo prebuild`, no EAS, no App Center, no signing,
   no simulator/device run, and no live connectivity.
5. Treat UI intents as local-only. Do not map `compose_draft`,
   `queue_file_request`, `ack_local`, or `refresh` to transport side effects.
6. For RNW Debug apps, do not treat Start menu or `shell:AppsFolder` launch as
   review acceptance unless the matching app-local Metro server is already
   proven live and a fresh screenshot shows loaded UI with no redbox and no
   loading-only state. Preferred debug relaunch is the app-local
   `pnpm --dir <split-app> exec react-native run-windows ... --no-telemetry`
   command. If `run-windows` is blocked by toolchain discovery after the debug
   package is already installed, start the matching app-local Metro server first
   and then launch the installed app registration.
7. Run only one split RNW app/Metro pairing at a time. Stop stale Metro/Node
   workers before switching Client, Sysop, and Hardware Tools; stale Metro has
   already produced wrong-bundle redbox evidence.
8. Run `python3 scripts/scaffold_audit_react_native.py` after scaffold changes.

Closed surfaces: BLE pairing, Web Bluetooth, Web Serial, LAN/SoftAP discovery,
serial writes, RF/XBee, flash, erase, monitor, relay, MicroSD, TFT, wiring,
load, mains, release, deploy, push, PR, and external-service automation.
