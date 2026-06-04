# Handoff 0119: CBBS Hardware Tools RNW Productization To QA

From: React Native Windows/UI coordinator

To: QA, Protocol/Bridge, React Native Windows, XBee/radio, Safety/Security

## Summary

Task 0160 productizes the `CBBS Hardware Tools` RNW surface with a generated
`cbbs_rnw_menu.v1` XML source, page-scoped Hardware Tools menu data, and a
desktop utility shell with menu/dropdowns, page list, workspace, evidence rail,
gate phrase field, and transcript strip.

The accepted runtime proof is the existing `CbbsWindows` compatibility entry
only:
`research/bench-records/react-native-windows/cbbs-rnw-hardware-tools-productized-menu-after-wait-20260603.png`
with SHA-256
`C4050B275954634EC4D7BD601963894FD5811597EBFC66DF94473FF11A871D4A`.

## Continue With

- Review final validation results in task log 0160 and the matching source
  ledger.
- Keep `tools/react-native/cbbs_rnw_menu.v1.xml` and
  `packages/cbbs-product/src/hardwareToolsMenu.generated.ts` in sync through
  `PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_rnw_menu.py --check`.
- Keep `apps/cbbs-windows` as the compatibility runtime entry until separate
  native product app generation is explicitly gated.
- Open a new Tier 3 gate before any executable HostCommandBridge, radio,
  firmware update, relay/load/mains, or live hardware work.

## Closed Surfaces

No serial writes, radio writes, XBee setting changes, firmware flash, erase,
monitor, relay/load/mains, wiring, native split-product build/deploy,
package/signing/release, commit, push, PR, or live hardware work is authorized
by this handoff.
