# React Native Tooling

This directory holds host-only React Native scaffold notes for the CBBS client
lane. The current validation entry point is:

```sh
python3 scripts/scaffold_audit_react_native.py
```

The audit checks accepted ADR/source records, workspace files, exact role/view
intent markers, native-folder absence, package-manifest forbidden terms, and
closed live transport markers.

Hardware Tools RNW product menus are generated from:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_rnw_menu.py --check
```

The generator reads `tools/react-native/cbbs_rnw_menu.v1.xml` and verifies the
tracked `packages/cbbs-product/src/hardwareToolsMenu.generated.ts` output.

No native prebuild, EAS, App Center, simulator/device run, live network, BLE,
Web Serial, Web Bluetooth, serial write, flash, RF/XBee, relay, release, PR,
push, or deploy command is authorized by this directory.
