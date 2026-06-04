# CBBS RNW Source/UI Mutation Ledger

Date: 2026-06-03

Source ID:
`SRC-LOCAL-CBBS-RNW-SOURCE-UI-MUTATION-2026-06-03`

## Scope

Tier 2 cross-repo source, UI, protocol, test, audit, and durable-record
alignment for ESP32 RNW CBBS product surfaces against the current local DOS-C
Win31 OPCON source tree.

This record uses local DOS-C source evidence from `/mnt/h/dos-c` at
`main...origin/main [ahead 1]`. It does not claim that the ahead local DOS-C
facts have been published to `origin/main`.

## Verified Facts

- DOS-C `knowledge-base/og-communication-retro31-branding-2026-05-28.md`
  records `OG Communication Retro3.1` as the versioned platform/app framing,
  `CBBS` as the BBS module, and `OPCON.EXE` as a stable internal binary name.
- DOS-C `software/win31-operator/README.md` records the current Win31 UI
  categories and operator request names.
- DOS-C `software/win31-operator/src/operator.rc` records Session, Views,
  Messages, Files, Devices, Style, and Help menu labels.
- DOS-C `software/win31-operator/src/operator.c` records the current category
  button labels and non-live initial status/counter wording.
- DOS-C `software/win31-operator/include/operator_protocol.h` and
  `software/win31-operator/src/operator_protocol.c` record the current
  20-request operator protocol table and compact JSON request formatting.
- ESP32 `tools/react-native/cbbs_rnw_menu.v1.xml` and
  `tools/react-native/generate_rnw_menu.py` already define the generated
  Hardware Tools product menu and fail-closed copy/bridge validators.

## Assumptions

- RNW alignment means source-backed product vocabulary, category order,
  role-boundary metadata, local-only UI intent semantics, audit-only protocol
  constants, tests, docs, and records.
- Unknown or conflicting DOS-C facts should render as unresolved gaps or
  evidence-only metadata, not product copy.
- Existing RNW generated bundle/map artifacts in the dirty tree are not
  publication sources for this task.

## Unknowns

- Whether the DOS-C ahead commit has been published.
- Whether split native RNW Client/Sysop/Hardware Tools runtimes will later be
  generated, signed, packaged, or run.
- Whether any executable HostCommandBridge, live serial/radio transport, or
  Win31/RNW runtime parity proof will be accepted later.

## Authority Limits

This record does not authorize live DOSBox-X operation, RNW runtime proof,
native bridge execution, serial writes, radio writes, XBee setting changes,
firmware flash, erase, monitor, relay/load/mains work, wiring, package
signing, Store/App Installer release, commit, push, PR, deploy, or cleanup
acceptance.

## Validation

- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_win31_parity.py --check`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 tools/react-native/generate_rnw_menu.py --check`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.rnw_menu.test_rnw_menu tests.rnw_menu.test_win31_parity`
- PASS: `pnpm --filter @cbbs/product typecheck`
- PASS: `pnpm --filter @cbbs/product-ui typecheck`
- PASS: focused Jest for protocol, product, product-ui, Windows compatibility,
  and shared fixture UI tests.
- PASS: `pnpm typecheck`
- PASS: `pnpm lint`
- PASS: `pnpm test` (10 suites, 52 tests)
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_react_native_scaffold`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 156`
- PASS: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- PASS: `/mnt/h/dos-c` Win31 operator, ESP-NOW bridge, vision-gate, scaffold,
  and diff checks.
- PASS: `git diff --check` in both repositories.

Final acceptance is recorded in task log 0161.
