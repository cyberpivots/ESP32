# Four Relay KY-040 BBS LCD Menu PF0530V User Acceptance Ledger

Source ID:
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-USER-ACCEPTANCE-2026-06-02`

Date: 2026-06-02

## Scope

Records the operator/user confirmation that the already written,
verify-flashed, and readiness-proven PF0530V image provides usable rotary
encoder control of the real LCD menu. This is a records-only acceptance source;
it does not add new live monitor data.

## Verified Facts

- PF0530V COM6 flash, separate verify-flash, reset/read-only readiness, idle
  heartbeat, scan, and cleanup evidence are recorded under
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-LIVE-2026-06-02`.
- The user later stated:
  `ENCODER FUNCTIONALITY CONFIRMED AND APPROVED BY USER`.
- The statement closes the user/operator acceptance item for PF0530V real LCD
  menu navigation/operation.

## Assumptions

- The confirmation refers to the currently flashed PF0530V image.
- Operator acceptance covers practical rotary encoder movement and button/menu
  operation from the user's observation.

## Unknowns

- No post-confirmation read-only transcript counts were captured for
  `BBS_MENU_STEP`, `BBS_MENU_SELECT`, PCNT direction/counts per detent, or
  quantified runaway tolerance.
- Exact direction labels, counts-per-detent behavior, and short/long select
  counts remain telemetry characterization topics only.

## Closed Surfaces

No erase-all, reflash, monitor, serial command writes, XBee/RF writes or tests,
ESP-NOW runtime expansion, relay GPIO writes, relay-expander writes, MicroSD/TFT
action, wiring mutation, DMM/current measurement, relay/load/mains work,
persistent config, external services, GitHub publication, release, commit, or
push is proven or authorized by this record.
