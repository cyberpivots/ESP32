# Handoff 0122: CBBS RNW Split Native Generation To QA

From: RNW split-native generation coordinator

To: QA, RNW DevEx, protocol/bridge, safety/security, KB records

Task:
[../TASK_LOG/0163-cbbs-rnw-split-native-generation.md](../TASK_LOG/0163-cbbs-rnw-split-native-generation.md)

## Summary

Task 0163 opens only split-native source generation for the three product app
packages. It does not open runtime launch, bridge dispatch, serial/RF/XBee
writes, signing, release, or publication.

## QA Focus

- Confirm the three split app native directories exist only as generated source
  trees.
- Confirm package scripts do not expose `run-windows`, build, signing, Store,
  EAS, App Center, deploy, or release commands.
- Confirm no `package-lock.json`, Debug/AppPackages/bin/obj output,
  package/signing artifact, or Store association file is accepted.
- Confirm generated manifests contain only the reviewed template capabilities
  `internetClient` and restricted `runFullTrust`.
- Confirm generated manifest identities are recorded as local debug facts only.

## Validation Evidence

Review Task 0163 and its source ledger after generation for the final command
list and validation summary.

## Closed Surfaces

No RNW `run-windows`, native build/deploy/launch, native bridge execution,
serial/RF/XBee write, firmware flash/erase/monitor, relay/load/mains work,
wiring, signing, package creation, Store/App Installer release, commit, push,
PR, deploy, or release is authorized by this handoff.
