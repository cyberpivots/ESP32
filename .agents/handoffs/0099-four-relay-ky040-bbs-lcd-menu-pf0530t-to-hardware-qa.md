# PF0530T Responsive Recovery To Hardware QA

Status: PF0530T source/build passed; live proof in progress

Date: 2026-06-02

## Context

PF0530S recovered raw GPIO liveness and produced menu/select events, but it was
not left in a stable responsive condition. PF0530T is a responsiveness image:
polling-first decoder, no ISR queue in the input path, no per-edge raw serial
spam, and detent-gated menu steps.

## Verified Facts

- PF0530T firmware identity/source metadata:
  `PF0530T`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530T-RESPONSIVE-2026-06-02`.
- PF0530T keeps GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` input-only with
  pullups.
- PF0530T keeps LCD GPIO21/GPIO22 display-only and keeps
  `FR_DIAG_XBEE_BRIDGE_CLOSED 1`.
- PF0530T uses 2 ms polling, one A/B stable sample, 1 ms A/B candidate hold,
  0 ms quiet time, two transitions per detent step, and 25 ms step lockout.
- PF0530T disables interrupt telemetry and raw edge logging in the decoder path
  and reports `cal=responsive-v6`.

## Unknowns

- Physical one-detent feel remains to be proven on the live LCD.
- Fast scroll behavior remains to be proven on the live LCD.

## Suggested Interaction Cues

- idle baseline,
- 10 slow clockwise detents,
- 10 slow counterclockwise detents,
- 20 medium clockwise detents,
- five single-detent pause checks,
- five short presses,
- one long press,
- final idle.

## Acceptance Evidence

Look for `PF0530T`, `BBS_INPUT_READY cal=responsive-v6`, `BBS_MENU_STEP` in both
directions, short and long `BBS_MENU_SELECT`, visible LCD/menu response, no
runaway/double-step pattern beyond tolerance, no serial byte writes, cleanup
proof, and zero crash/unsafe markers.

## Stop Gates

Do not perform another flash, serial writes, XBee/RF writes,
relay/load/mains work, wiring mutation, DMM/current measurement, erase,
persistent config, release, commit, or push without a separate explicit gate.
