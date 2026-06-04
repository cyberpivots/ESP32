# Handoff 0125: CBBS RNW Split Build Install Launch To QA

From: RNW split local runtime coordinator

To: QA, RNW DevEx, protocol/bridge, safety/security, KB records

Task:
[../TASK_LOG/0166-cbbs-rnw-split-build-install-launch.md](../TASK_LOG/0166-cbbs-rnw-split-build-install-launch.md)

## Summary

Task 0166 opens a local Windows 11 debug build/deploy/install/launch gate for
the three split RNW product apps:

- `CbbsClientWindows`
- `CbbsSysopWindows`
- `CbbsHardwareToolsWindows`

The gate is for user review and testing only. It does not accept final package
identity, capability use, signing, Store/App Installer distribution, release,
native HostCommandBridge dispatch, serial/RF/XBee, firmware, relay/load/mains,
or any hardware action.

## QA Focus

- Confirm every `run-windows` command includes `--no-telemetry` and uses the
  app-local split solution/project path.
- Confirm screenshots show loaded UI, not a redbox or loading-only state.
- Confirm process/window/package proof is tied to the same app/session as each
  screenshot.
- Confirm static scans and runtime evidence show no HostCommandBridge dispatch,
  shell execution, serial/RF/XBee action, flash/erase/monitor, relay/load/mains,
  signing, Store/App Installer packaging, release, commit, push, PR, or deploy.
- Confirm generated Debug/AppPackages/bin/obj outputs and debug package
  retention are recorded before any later scaffold-clean acceptance claim.

## Validation Evidence

Review Task 0166 and its source ledger after the run for the final command
list, evidence paths, runtime disposition, and cleanup/retention statement.

## Closed Surfaces

No live bridge dispatch, serial/RF/XBee write, firmware flash/erase/monitor,
relay/load/mains work, wiring, signing, package creation for distribution,
Store/App Installer release, commit, push, PR, deploy, or release is authorized
by this handoff.
