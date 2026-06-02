# PF0530U Responsive V7 To Hardware QA

Status: PF0530U written and verify-flashed on COM6; post-flash actuation proof pending

Date: 2026-06-02

## Context

PF0530T proved the raw GPIO path and switch path are live, but rotation was too
conservative for the requested responsive LCD menu. PF0530U keeps the polling
decoder and detent gate, then lowers the detent-return threshold to one
transition per emitted step.

## Verified Facts

- PF0530U firmware identity/source metadata:
  `PF0530U`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530U-RESPONSIVE-V7-2026-06-02`.
- GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` remain input-only with pullups.
- LCD GPIO21/GPIO22 remains display-only and `FR_DIAG_XBEE_BRIDGE_CLOSED 1`
  remains set.
- PF0530U uses 2 ms polling, one A/B stable sample, 1 ms A/B candidate hold,
  0 ms quiet time, one transition per detent-gated step, and 25 ms step
  lockout.
- PF0530U disables interrupt telemetry and raw edge logging in the decoder path
  and reports `cal=responsive-v7`.

## Acceptance Evidence

Look for `PF0530U`, `BBS_INPUT_READY cal=responsive-v7`, `BBS_MENU_STEP` in both
directions, short and long `BBS_MENU_SELECT`, visible LCD/menu response, no
runaway/double-step pattern beyond tolerance, no serial byte writes, cleanup
proof, and zero crash/unsafe markers.

Current live note: PF0530U reset/readiness proof passed, but two post-flash
read-only monitor windows captured no physical input events. The next useful
action is a read-only monitor while the operator actively turns and presses the
encoder; do not reflash before collecting that actuation proof unless a new
gate explicitly authorizes it.

## Stop Gates

Do not perform another flash, serial writes, XBee/RF writes,
relay/load/mains work, wiring mutation, DMM/current measurement, erase,
persistent config, release, commit, or push without a separate explicit gate.
