# Handoff 0116: CBBS React Native Windows W4 Pre-Release To QA/Release

Date: 2026-06-03

From: React Native Windows coordinator

To: QA, Release, DevEx/CI, Source Research, Security/Safety

## Summary

W4A is accepted as pre-release source/record refresh only. It registers the
`CbbsWindows` JS component, corrects W3B-aware status fields, records app-local
RNW project metadata, adds source coverage for signing/distribution planning,
and keeps W4B-W4E closed.

## Verified Facts

- W3B generated the native project and did not prove build/run/runtime.
- W4A registers `CbbsWindows` with `AppRegistry`.
- W4A does not accept generated manifest identity as signing/release identity.
- W4A does not accept `internetClient` or restricted `runFullTrust` for
  capability use.
- No package scripts expose RNW build/run, MSBuild, MakeAppx, SignTool,
  signing, deploy, Store upload, EAS, App Center, or release commands.

## Continue With

Open W4B only after separate explicit authority, fresh same-session Windows
host evidence, a build-output policy, no-P1/P2 reviewer quorum, exact command
boundary, post-command artifact scan, and green current-host audits.

## Boundaries

No RNW `run-windows`, Visual Studio/MSBuild build, deploy, launch, package
creation, signing, certificate/PFX handling, Store association, App Installer
publishing, live transport, release, commit, push, PR, or deploy is authorized
by this handoff.

## Validation

Use the task record validation list for current-host W4A checks. Future W4B
evidence must not be confused with package, signing, deploy, runtime, Store,
or live CBBS proof.

## Evidence

- Task record:
  [../TASK_LOG/0156-cbbs-react-native-windows-w4-pre-release.md](../TASK_LOG/0156-cbbs-react-native-windows-w4-pre-release.md)
- Source ledger:
  [../../knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-w4-pre-release.md](../../knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-w4-pre-release.md)
- Source ID:
  `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W4-PRE-RELEASE-2026-06-03`
