# Handoff 0118: CBBS RNW Product Split Hardware Tools Bridge Contract To QA

From: React Native Windows/UI coordinator

To: QA, Protocol/Bridge, React Native Windows, Safety/Security

## Summary

Task 0159 splits the Windows product source into `CBBS Client`, `CBBS Sysop`,
and `CBBS Hardware Tools`, removes the old visible developer cockpit text, and
adds an inert `cbbs_host_command_bridge.v1` contract.

The bridge contract is non-executing. It must not be treated as native module
authority, shell authority, serial/radio authority, firmware update authority,
or release authority.

## Continue With

- Review final validation results in task log 0159.
- Keep `apps/cbbs-windows` as a compatibility source entry until native product
  app generation is separately planned.
- Open a new Tier 3 gate before any executable `HostCommandBridge` work.

## Closed Surfaces

No serial writes, radio writes, firmware flash, erase, monitor, relay/load/
mains, wiring, native build/run/deploy, signing, Store/App Installer, release,
or live hardware work is authorized by this handoff.
