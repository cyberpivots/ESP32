# PF0530S Raw-Liveness Recovery To Hardware QA

Status: PF0530S raw-liveness proof accepted; decoder stability open

Date: 2026-06-01

## Context

PF0530R was written and separately verify-flashed on COM6 with readiness proof,
but the attended monitor captured zero encoder/button input event lines.
PF0530S recovered raw GPIO13/GPIO14/GPIO32 visibility and produced local menu
movement plus short/long select events. It is not yet accepted as fully stable.

## Verified Facts

- PF0530S firmware identity/source metadata:
  `PF0530S`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530S-RAW-LIVENESS-CAL-2026-06-01`.
- PF0530S keeps GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` input-only with
  pullups.
- PF0530S keeps LCD GPIO21/GPIO22 display-only and keeps
  `FR_DIAG_XBEE_BRIDGE_CLOSED 1`.
- PF0530S uses 3 ms A/B hold, 0 ms quiet time, one transition per step, and
  45 ms step lockout.
- PF0530S adds `ENC_BASE`, `ENC_GPIO_CONFIG`, GPIO config dump,
  `ENC_LEVEL_HB`, raw/ISR/queue/poll counters in `BBS_MENU_HB`, and
  `cal=raw-live-v5`.
- PF0530S COM6 write-flash and separate verify-flash passed for only the
  bootloader, partition table, and app offsets.
- Reset boot proof captured PF0530S readiness, raw-live-v5 metadata,
  baseline/config/heartbeat telemetry, and zero crash/unsafe markers.
- The attended 150 second read-only monitor captured 450 A/B raw events, 84
  switch raw events, GPIO13/GPIO14/GPIO32 ISR events, 27 clockwise steps, 21
  counterclockwise steps, 14 short selects, 4 long selects, LCD/menu response,
  no serial byte writes, and zero crash/unsafe markers.
- Cleanup checks found no lingering Linux or Windows COM6/esptool/PF0530S
  monitor process.

## Assumptions

- The PF0530S attended cue sequence was physically applied during the
  read-only monitor.
- PCNT/knob/button remain deferred until raw A/B edge visibility is proven.

## Unknowns

- Full PF0530S rotary stability remains open.
- The attended scan recorded 15 invalid transitions, 31 A/B suppressions, five
  step-lockout filters, and final heartbeat `queue_drop=57`.

## Suggested Interaction Cues

- idle baseline,
- 5 slow clockwise detents,
- 5 slow counterclockwise detents,
- 10 faster clockwise detents,
- five single-detent pause checks,
- five short presses,
- one long press,
- final idle.

## Acceptance Evidence

Accepted for this handoff: `ENC_RAW > 0`, `ENC_EV > 0`, `BBS_MENU_STEP` in
both directions, short and long `BBS_MENU_SELECT`, visible LCD/menu response,
no serial byte writes, cleanup proof, and zero crash/unsafe markers. Not yet
accepted: stable one-detent behavior or bounce/drop-free operation.

## Stop Gates

Do not perform another flash, serial writes, XBee/RF writes,
relay/load/mains work, wiring mutation, DMM/current measurement, erase,
persistent config, release, commit, or push without a separate explicit gate.
The next useful gate is bounded decoder/queue/debounce stability tuning, not a
raw input visibility investigation.
