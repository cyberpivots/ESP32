# Handoff 0117: CBBS React Native Windows Build Launch Integrated To QA

Date: 2026-06-03

From: React Native Windows coordinator

To: QA, RNW DevEx, Communications, XBee/radio, Firmware/device

## Summary

The local Windows RNW app was built, deployed, and launched with
`react-native run-windows`. The running app process is `CbbsWindows`, and the
installed package is `CbbsWindows_1.0.0.0_x64__2g54mg31548kg`. The final
same-session process proof found PID `29964`, window title `CbbsWindows`, and
`Responding=true`.

## Verified Facts

- The Windows operations console now renders mesh discovery, XBee radio
  configuration/readback, XBee OTA link, and firmware flash evidence surfaces.
- The app displays command/evidence records inertly; UI intents still go
  through `localIntent` and do not dispatch serial, RF, relay, or flash
  commands.
- PF0530W live flash source evidence is pinned in the firmware flash panel.
- W4D/W4E signing, packaging, Store, App Installer, release, and public
  distribution remain outside this handoff.

## Validation

- `pnpm --filter @cbbs/windows-spike typecheck`
- `git diff --check`
- Live Metro bundle request saved to
  `research/bench-records/react-native-windows/live-index.bundle`
- `react-native run-windows --root . --sln windows\CbbsWindows.sln --proj windows\CbbsWindows\CbbsWindows.vcxproj --arch x64 --no-telemetry`
- Windows process/package verification for `CbbsWindows`
- Focused screenshot:
  `research/bench-records/react-native-windows/cbbs-windows-window-final.png`

## Follow-Up

- Investigate the current Jest hang separately before using root Jest as fresh
  acceptance evidence again.
- Decide whether generated native NuGet `packages.lock.json` files should be
  tracked or ignored for the RNW native project.
- Treat `scripts/scaffold_audit_react_native.py` as a pre/post-clean audit for
  this lane; it fails immediately after `run-windows` because Debug build
  outputs exist under the native project.

## Evidence

- Task record:
  [../TASK_LOG/0157-cbbs-react-native-windows-build-launch-integrated.md](../TASK_LOG/0157-cbbs-react-native-windows-build-launch-integrated.md)
- Source ledger:
  [../../knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-build-launch-integrated.md](../../knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-build-launch-integrated.md)
- Source ID:
  `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-BUILD-LAUNCH-INTEGRATED-2026-06-03`
