# Handoff 0120: CBBS RNW Source/UI Mutation To QA

From: React Native Windows/UI coordinator

To: QA, Protocol/Bridge, DOS-C Win31 operator, evidence records

Task:
[../TASK_LOG/0161-cbbs-rnw-source-ui-mutation.md](../TASK_LOG/0161-cbbs-rnw-source-ui-mutation.md)

## Summary

Task 0161 aligns the ESP32 RNW CBBS product surfaces with the current local
DOS-C Win31 OPCON source vocabulary and protocol table. The expected result is
source-backed UI/product/protocol parity, not live transport equivalence.

The local DOS-C checkout used for source evidence is
`/mnt/h/dos-c` at `main...origin/main [ahead 1]`. Do not claim those facts are
published on `origin/main` unless publication is separately verified.

## QA Focus

- Confirm `tools/react-native/cbbs_rnw_win31_parity.v1` source and
  `generate_win31_parity.py --check` stay in sync with tracked generated
  product parity data.
- Confirm RNW Sysop page order is exactly Status, Messages, Files, Devices,
  Help, Peers, Link, Updates, Setup, Diagnostics, and Locks.
- Confirm visible RNW framing uses `OG Communication Retro3.1`, keeps `CBBS`
  as the BBS module name, and keeps `OPCON.EXE` and DOS-C wire names as
  evidence/internal references only.
- Confirm every client role parity category is represented, evidence-only, or
  `notRenderedRoleBoundary` with a source-backed reason.
- Confirm Hardware Tools remains generated from `cbbs_rnw_menu.v1` and keeps
  bridge/raw-term validators fail-closed.
- Confirm `tier3Closed` and `bridgePreviewUnavailable` actions remain disabled
  even when state is `ready` or `complete`.
- Confirm audit-only DOS-C request-name constants do not become UI intents,
  HostCommandBridge action IDs, or dispatched DOS-C `type` frames.

## Validation Evidence

- PASS: Win31 parity generator `--check`, Hardware Tools generator `--check`,
  and RNW generator unit tests.
- PASS: product/product-ui/protocol focused Jest and typecheck coverage.
- PASS: root `pnpm typecheck`, `pnpm lint`, and `pnpm test` (10 suites,
  52 tests).
- PASS: React Native scaffold audit, durable-record audit, ESP32 scaffold
  verification, and `git diff --check`.
- PASS: paired DOS-C Win31 operator, ESP-NOW bridge, vision-gate, scaffold,
  and diff checks.

Review the dirty-tree boundary before publication: ESP32 still contains the
broader pre-existing RNW dirty tree and generated bundle/map artifacts that
are not source for this handoff.

## Closed Surfaces

No live DOSBox-X proof, RNW runtime proof, serial writes, RF/XBee writes,
firmware flash, erase, monitor, relay/load/mains work, wiring, native bridge
execution, package/signing/release, commit, push, PR, deploy, or cleanup claim
is authorized by this handoff.
