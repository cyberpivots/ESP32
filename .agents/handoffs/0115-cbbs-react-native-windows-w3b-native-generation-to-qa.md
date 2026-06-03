# Handoff 0115: CBBS React Native Windows W3B Native Generation To QA

Date: 2026-06-03

From: React Native Windows coordinator

To: QA, DevEx/CI, Source Research, Security/Safety

## Summary

W3B generated the app-local RNW `cpp-app` native project for
`apps/cbbs-windows` only. The gate is not build/run/runtime proof. The command
was app-scoped, package-lock disabled, no-overwrite, and no-telemetry.

## Verified Facts

- W3A proved RNW 0.83 package-local prerequisites but did not generate native
  files.
- RNW 0.83 `cpp-app` source mutates `apps/cbbs-windows/package.json`, adds
  `@rnx-kit/jest-preset`, injects a `run-windows` script, and runs install.
- RNW 0.83 exposes no supported no-install/no-package-mutation
  `init-windows` option.
- The generated `windows`/`run-windows` script was removed before W3B
  acceptance.
- Final dependency state was reconciled through pnpm; app/root
  `package-lock.json` output was not present.
- Generated manifest capabilities are exactly `internetClient` and restricted
  `runFullTrust`.

## Continue With

Review W3B as native-generation proof only. Continue with W4 build-only
planning only after separate explicit authority, source refresh, no-P1/P2
quorum, and command logs that avoid launch/deploy/signing.

## Boundaries

Final tracked mutation boundary:
`apps/cbbs-windows/windows/**`, generated app-root RNW config files,
`apps/cbbs-windows/package.json`, `pnpm-lock.yaml`, W3B audit/test files,
path-image allowlist updates for the generated package PNGs, and W3B
governance/source records.

No root native folder, app/root `package-lock.json`, build outputs, signing
material, Store association, EAS/App Center config, live transport, release,
commit, push, PR, deploy, RNW build/run, serial/RF/BLE/network, or hardware
authority is opened by this handoff.

## Validation

- PASS: W3B native generation command completed without overwrite prompt.
- PASS: generated manifest capability inspection.
- PASS: pnpm lockfile reconciliation and frozen install.
- PASS: lint, typecheck, Jest, Expo Doctor, Windows typecheck, React Native
  scaffold audit/tests, durable-record audit, agent-process audit, skill audit,
  full scaffold verification, no-package-lock scan, no W4 package-script scan,
  no build/signing artifact scan, and `git diff --check`.

## Evidence

- Task record:
  [../TASK_LOG/0155-cbbs-react-native-windows-w3b-native-generation.md](../TASK_LOG/0155-cbbs-react-native-windows-w3b-native-generation.md)
- Source ledger:
  [../../knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-w3b.md](../../knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-w3b.md)
- Source IDs:
  `SRC-REACT-NATIVE-WINDOWS-CPP-APP-TEMPLATE-2026-06-03`,
  `SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W3B-2026-06-03`
