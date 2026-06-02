# PF0530V PCNT Source Build To Hardware QA

Status: source/build prepared; live proof not performed

Date: 2026-06-02

## Context

PF0530U remains the last written/verify-flashed COM6 image, but it did not
capture physical encoder events in its post-flash monitors. PF0530V is a
different source approach: use ESP-IDF PCNT quadrature counting for A/B rotation
and keep the pushbutton on the existing poll/debounce path.

## Verified Facts

- PF0530V firmware identity/source metadata:
  `PF0530V`,
  `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530V-PCNT-SOURCE-BUILD-2026-06-02`.
- GPIO13 `CLK`, GPIO14 `DT`, and GPIO32 `SW` remain input-only with pullups.
- LCD GPIO21/GPIO22 remains display-only and `FR_DIAG_XBEE_BRIDGE_CLOSED 1`
  remains set.
- PF0530V adds `esp_driver_pcnt`, initializes a PCNT unit with GPIO13/GPIO14
  cross-level quadrature channels, uses four counts per emitted menu step, caps
  a poll at four emitted steps, and reports PCNT telemetry in readiness and
  heartbeat lines.
- The switch path remains software debounce/polling with 30 ms debounce, 40 ms
  guard, and 650 ms long press.

## Future Live Acceptance Evidence

Under a separate Tier 3 gate, look for `PF0530V`, `ENC_PCNT_READY result=ok`,
`BBS_INPUT_READY cal=pcnt-v1 decoder=pcnt`, `ENC_PCNT_HB`, `BBS_MENU_STEP` in
both directions, short and long `BBS_MENU_SELECT`, visible LCD/menu response,
no runaway/double-step pattern beyond tolerance, no serial byte writes, cleanup
proof, and zero crash/unsafe markers.

## Source Validation

- Focused unit/audit bundle: PASS, 60 tests.
- LCD generated menu freshness check: PASS.
- Firmware and agent-process scaffold audits: PASS.
- Source/docs/data audits and scaffold verification: PASS.
- ESP-IDF v6.0.1 no-flash build to `/tmp/esp32-pf0530v-pcnt-build`: PASS.
- Final `git diff --check`: PASS.

## Stop Gates

Do not flash, monitor, send serial commands, write XBee/RF settings, perform
relay/load/mains work, mutate wiring, perform DMM/current measurement, erase,
persist config, release, commit, or push without a separate explicit gate.
