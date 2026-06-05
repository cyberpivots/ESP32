# Source Ledger - 2026-06-05 XBee Hub-Spoke Host Plan

## Scope

Tier 2 host-only implementation of an XBee hub-spoke planning matrix, simulator,
offline CLI command, source correction, and review-only Hardware Tools evidence.
No live serial, RF, XBee write, firmware, bridge dispatch, wiring, relay/load,
mains, release, commit, push, PR, or deploy authority was granted or used.

## Source IDs

- `SRC-DIGI-XBP9B-DPUT-001`
- `SRC-DIGI-XBEE-900HP-AP`
- `SRC-DIGI-XBEE-900HP-AO`
- `SRC-DIGI-XBEE-900HP-NP`
- `SRC-DIGI-XBEE-900HP-DELIVERY`
- `SRC-DIGI-XBEE-900HP-TO-2026-06-05`
- `SRC-DIGI-XBEE-900HP-USER-GUIDE-REFRESH-2026-06-05`
- `SRC-DIGI-XCTU-SUPPORT-2026-06-05`
- `SRC-DIGI-XBEE-STUDIO-SUPPORT-2026-06-05`
- `SRC-LOCAL-XBEE-RADIO-STUDY-2026-05-29`
- `SRC-LOCAL-XBEE-HUB-SPOKE-HOST-PLAN-2026-06-05`

## Verified facts

- `XBP9B-DPUT-001` remains the source-indexed exact part for this repo lane.
- Implementation-facing 900HP transmit-status records now use Extended
  Transmit Status `0x8B` for `0x10` requests; older `0x89` wording was corrected
  in the protocol records and legacy design ledger.
- `TO` source coverage was added for the 10k product default and DigiMesh stop
  condition.
- `scripts/xbee_radio_study.py hub-spoke-plan` emits deterministic host-only
  JSON and delegates no serial, subprocess, RF, firmware, or hardware action.
- `tools/simulators/xbee_hub_spoke/` models one hub, at least 10 redacted
  spokes, 12 use cases, synthetic `0x90` receive metadata, synthetic `0x8B`
  transmit-status metadata, and `NP` payload-budget checks.

## Assumptions

- Hub-spoke means point-to-multipoint planning for the current 10k part unless
  a later source and readback prove a different variant.
- Saved Hardware Tools radio analysis may include hub matrix evidence but stays
  review-only with closed `serial_write` and `rf_xbee_write` surfaces.

## Unknowns

- Current radio firmware, settings, address plan, key state, exact port
  identity, antenna/regulatory state, carrier wiring, voltage, and live payload
  limit remain unverified.
- Remote solar-client power behavior, battery/charger selection, and field
  range remain unresolved.

## Validation

Validation completed on 2026-06-05:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_radio_study.py hub-spoke-plan --json
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/xbee_hub_spoke -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.scaffold_audits.test_xbee_radio_study
PYTHONDONTWRITEBYTECODE=1 python3 scripts/xbee_read_only_probe.py self-test --json
PYTHONDONTWRITEBYTECODE=1 python3 tests/four_relay_safe_core/run_host_tests.py
pnpm test -- packages/cbbs-product/__tests__/product.test.ts packages/cbbs-product-ui/__tests__/ProductWindowsShell.test.tsx
pnpm --filter @cbbs/hardware-tools-windows test:windows
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id 176
PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'
git diff --check
```

All listed commands passed. `git diff --check` emitted only the existing CRLF
normalization warning for the dirty RNW C++ file.

## Decision

Decision: accept the staged Tier 2 host-only implementation boundary after the
source reviewer cleared the `0x8B` correction prerequisite. All live XBee,
serial, RF, firmware, bridge-dispatch, wiring, relay/load/mains, and release
surfaces remain closed.
