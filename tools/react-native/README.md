# React Native Tooling

This directory holds host-only React Native scaffold notes for the CBBS client
lane. The current validation entry point is:

```sh
python3 scripts/scaffold_audit_react_native.py
```

The audit checks accepted ADR/source records, workspace files, exact role/view
intent markers, native-folder absence, package-manifest forbidden terms, and
closed live transport markers.

No native prebuild, EAS, App Center, simulator/device run, live network, BLE,
Web Serial, Web Bluetooth, serial write, flash, RF/XBee, relay, release, PR,
push, or deploy command is authorized by this directory.
