# Four Relay KY-040 BBS LCD Menu PF0530V User Acceptance

Status: PF0530V encoder functionality user-confirmed and accepted; transcript-count characterization open

Contract: [../../AGENTS.md](../../AGENTS.md)

Date: 2026-06-02

## Routing

- Selected tier: Tier 2 because this update mutates durable evidence/status
  records after a user confirmation. No live bench, flash, monitor, serial
  write, firmware source change, or hardware action is included.
- Owner role: Evidence Records with Firmware, QA, LCD UX, and coordinator
  lenses.
- Evidence need: exact user confirmation phrase, PF0530V flash/readiness source
  linkage, reviewer quorum result, durable task/source/status updates, stale
  wording scan, scaffold audits, and `git diff --check`.
- Mutation boundary: PF0530V docs and records only. No firmware behavior change,
  COM6 access, erase, reflash, monitor, serial command writes, XBee/RF writes or
  tests, relay GPIO writes, relay-expander writes, ESP-NOW runtime expansion,
  wiring changes, DMM/current/load/mains, persistent config, external services,
  release, commit, or push.
- Reviewer disposition: Tier 2 project-local read-only quorum approved the
  records-only boundary at 14/14 weight, 100 percent, with no P1/P2 blockers.
  Conditions: preserve the exact user confirmation, classify it as
  user/operator acceptance evidence, and do not claim transcript-captured
  step/select/PCNT counts.

## Verified Facts

- PF0530V was already written and separately verify-flashed on COM6 under
  source ID
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-LIVE-2026-06-02`.
- The PF0530V live gate proved COM6 identity, rollback backup, staged artifact
  hashes, write-flash, separate verify-flash, reset/read-only readiness, idle
  read-only heartbeats, transcript scan, cleanup proof, and zero crash/unsafe
  markers.
- After that PF0530V gate, the user stated:
  `ENCODER FUNCTIONALITY CONFIRMED AND APPROVED BY USER`.
- This records user-confirmed real LCD menu encoder functionality acceptance for
  the flashed PF0530V image.

## Assumptions

- The user confirmation refers to the currently flashed PF0530V image.
- The user confirmation is sufficient to close the operator-use acceptance item
  for PF0530V encoder/LCD menu functionality.

## Unknowns

- No post-confirmation serial transcript counts are claimed for
  `BBS_MENU_STEP`, `BBS_MENU_SELECT`, PCNT direction/counts per detent, or
  quantified runaway tolerance.
- Exact direction labels, short/long select counts, and counts-per-detent
  calibration remain uncaptured unless a later read-only monitor is requested.

## Decision Footer

Decision: `pf0530v_user_confirmed_functional_telemetry_characterization_open`.
Next gate: use PF0530V as the accepted functional LCD menu encoder image; only
run a separate read-only monitor if transcript-count characterization is later
needed. Owner: Evidence Records with Hardware QA and LCD UX. Evidence: user
confirmation, PF0530V live source ledger, reviewer quorum, updated records, and
static validation. Authority limits: no erase, serial command writes, XBee/RF,
relay/load/mains, wiring, DMM/current, persistent config, external services,
release, commit, or push.
