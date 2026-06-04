# Task 0161: CBBS RNW Source/UI Mutation

Status: completed

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-03

Source IDs:
`SRC-LOCAL-CBBS-RNW-SOURCE-UI-MUTATION-2026-06-03`

## Routing

- Verified facts: the ESP32 checkout is `/mnt/h/esp32` on branch `main`
  tracking `origin/main` with a pre-existing dirty RNW tree. The current local
  DOS-C checkout is `/mnt/h/dos-c` on `main...origin/main [ahead 1]`; source
  facts in this task are local checkout facts and are not claimed to be present
  on `origin/main`. DOS-C `software/win31-operator/README.md` names the Win31
  surface `OG Communication Retro3.1`, keeps `CBBS` as the BBS module, lists
  the current UI scope, and lists the 20 compact operator request names.
  DOS-C source files `operator.rc`, `operator.c`, `operator_protocol.h`, and
  `operator_protocol.c` contain the current menu/view/status/request evidence.
- Assumptions: the accepted plan authorizes Tier 2 source, UI, protocol-test,
  audit, docs, and durable-record alignment only. Product copy may mirror
  source-backed Win31 vocabulary and role boundaries, but must not imply live
  transport, bridge execution, hardware behavior, or publication.
- Unknowns: current `origin/main` publication state for the DOS-C ahead commit,
  final split native RNW product runtimes, native HostCommandBridge ABI,
  signing/package identity, live RNW runtime proof, live DOSBox-X proof, serial
  or radio transport behavior, and release path remain unresolved.
- Selected tier: Tier 2 cross-repo source/UI/protocol/governance alignment.
- Owner role: React Native Windows/UI parity owner with Protocol/Bridge,
  DOS-C Win31 operator, evidence-record, and QA lenses.
- Evidence need: local DOS-C source citations, deterministic parity
  generator/check output, tracked generated parity data, product/product-ui
  tests, protocol no-dispatch tests, DOS-C host tests, scaffold audits, record
  audits, and dirty-tree/artifact boundary checks.
- Mutation boundary: ESP32 RNW parity source/generator/tests, generated
  `@cbbs/product` parity data, `@cbbs/product`, `@cbbs/product-ui`,
  `@cbbs/protocol`, `apps/cbbs-windows` compatibility default/tests/docs,
  React Native scaffold audit/tests, task/handoff/source-ledger/index records,
  and focused DOS-C docs/tests/records. Generated Metro/RNW bundle or source
  map artifacts remain out of publication scope.
- Gate authority: user accepted implementation of the RNW to DOS-C Win31
  alignment plan. No Tier 3 live DOSBox-X, RNW runtime proof, serial/RF/XBee
  writes, firmware flash, erase, monitor, relay/load/mains work, package
  signing, release, commit, push, PR, or cleanup claim is authorized.
- Validation plan: run the RNW Win31 parity generator in check mode, the
  existing Hardware Tools generator in check mode, RNW menu/parity unit tests,
  focused product/product-ui/protocol tests, package/root typecheck/lint/test
  where practical, React Native and durable-record scaffold audits, DOS-C
  Win31 operator and bridge host tests, DOS-C scaffold verification, and
  `git diff --check` in both repositories.
- Trust boundary: source/test/audit evidence only. Runtime screenshots are not
  required for this Tier 2 pass and are not accepted as live-transport proof.

## Reviewer Quorum

- Coordinator, weight 5: classified the work as Tier 2, kept Tier 3 and
  publication surfaces closed, and accepted mutation only after records-first
  gate creation.
- React Native UI parity reviewer, weight 3: found P1/P2 blockers in the
  prior RNW surface and required a machine-readable Win31 parity baseline,
  visible `OG Communication Retro3.1` framing, exact Sysop page order, and a
  Sysop default for the compatibility app.
- Protocol/Bridge reviewer, weight 3: required audit-only DOS-C request-name
  constants, no DOS-C `type` frames in UI intents or HostCommandBridge, an
  unavailable-by-default HostCommandBridge result, and disabled closed-gate
  actions even when action state reads ready or complete.
- Evidence auditor, weight 3: blocked source/UI mutation until paired ESP32
  and DOS-C durable records, source-index entries, and handoffs existed.
- QA reviewer, weight 3: required focused generator/product/protocol/DOS-C
  tests plus dirty-tree and generated-artifact boundary reporting before
  acceptance.

Weighted result: records-first mutation is accepted. Product/source mutation
remains conditional on this task record, the paired handoff, and source ledger
being present before source/UI edits.

## Planned Changes

- Add a source-backed `cbbs_rnw_win31_parity.v1` contract plus stdlib Python
  generator/check that emits tracked `@cbbs/product` parity data and fails
  closed on missing DOS-C source references, duplicate IDs, unsafe visible
  copy, raw live-action wording, unknown DOS-C request names, and stale
  generated TypeScript.
- Align RNW visible branding to `OG Communication Retro3.1` while keeping
  `CBBS` as the BBS module name and preserving stable app IDs/component names.
- Make RNW `sysop` match the DOS-C Win31 OPCON category order: Status,
  Messages, Files, Devices, Help, Peers, Link, Updates, Setup, Diagnostics,
  and Locks.
- Keep RNW `client` role-adapted with each Win31 parity category represented,
  marked evidence-only, or marked `notRenderedRoleBoundary` with a
  source-backed reason.
- Keep Hardware Tools' generated `cbbs_rnw_menu.v1` pages and map them into
  Devices/Diagnostics/Locks-adjacent support surfaces without loosening bridge
  or raw-term validators.
- Change the `apps/cbbs-windows` compatibility default from Hardware Tools to
  the Sysop parity surface.
- Harden product/UI/protocol enablement so closed Tier 3 and unavailable bridge
  preview controls do not become clickable from `ready` or `complete` state.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_win31_parity.py --check`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_rnw_menu.py --check`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.rnw_menu.test_rnw_menu tests.rnw_menu.test_win31_parity`
- PASS: `pnpm --filter @cbbs/product typecheck`
- PASS: `pnpm --filter @cbbs/product-ui typecheck`
- PASS: focused Jest for `packages/cbbs-protocol/__tests__/contract.test.ts`
- PASS: focused Jest for `packages/cbbs-product/__tests__/product.test.ts`
- PASS: focused Jest for `packages/cbbs-product-ui/__tests__/ProductWindowsShell.test.tsx`
- PASS: focused Jest for `apps/cbbs-windows/__tests__/windowsHostOnly.test.tsx`
- PASS: focused Jest for `packages/cbbs-ui/__tests__/OperatorShell.test.tsx`
- PASS: `pnpm typecheck`
- PASS: `pnpm lint`
- PASS: `pnpm test` (10 suites, 52 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_react_native_scaffold`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 156`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `/mnt/h/dos-c`: `bash tests/win31_operator/run_host_tests.sh`
- PASS: `/mnt/h/dos-c`: `bash tests/espnow_bbs_bridge/run_tests.sh`
- PASS: `/mnt/h/dos-c`: `python3 -m unittest tests.test_win31_dashboard_vision_gate`
- PASS: `/mnt/h/dos-c`: `bash scripts/verify_scaffold.sh`
- PASS: `git diff --check` in `/mnt/h/esp32`
- PASS: `git diff --check` in `/mnt/h/dos-c`

Dirty-tree boundary retained: `/mnt/h/esp32` still contains the broader
pre-existing RNW dirty tree, including generated bundle/map artifacts under
`research/bench-records/react-native-windows/`; those artifacts were not
treated as source or publication material. `/mnt/h/dos-c` remains
`main...origin/main [ahead 1]`.

## Authority Limits

This task does not authorize live DOSBox-X operation, RNW runtime proof,
serial writes, radio writes, XBee setting changes, firmware flash, erase,
monitor, relay/load/mains work, wiring, package signing, Store/App Installer
distribution, release, commit, push, PR, deploy, or cleanup acceptance.

## Decision

Accepted as Tier 2 source/UI/protocol/test alignment. RNW now has a
source-backed Win31 parity contract, exact Sysop category order, role-adapted
Client coverage metadata, Sysop compatibility default, audit-only DOS-C
request constants, fail-closed unavailable bridge results, and mode-aware
closed-gate UI enablement. This does not claim live transport or runtime
parity.

## Handoff

Handoff:
[../handoffs/0120-cbbs-rnw-source-ui-mutation-to-qa.md](../handoffs/0120-cbbs-rnw-source-ui-mutation-to-qa.md)
