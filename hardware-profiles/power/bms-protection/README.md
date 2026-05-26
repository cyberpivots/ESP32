# BMS And Protection Profile

## Status

Planning stub for the `remote-lcd-xbee-solar-client` lane. Exact BMS/protection
board is unresolved.

## Verified facts

- TI documents BQ2970 as a single-cell Li-ion/Li-poly battery protector with
  FET drive, overvoltage, undervoltage, overcurrent, and short-circuit
  protection functions. This is candidate/reference coverage only and does not
  verify the local BMS board. Source ID: `SRC-TI-BQ2970`.
- This workspace has not verified an exact BMS/protection board, IC marking,
  FET path, threshold set, current rating, connector labels, or board
  schematic. Source ID:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`.

## Assumptions

- Protection is required before any future battery-powered bench action.
- A generic board cannot be trusted without markings, source, and connector
  proof.

## Unknowns

- Board vendor, model, IC marking, FET arrangement, and schematic.
- Overcharge, overdischarge, charge-overcurrent, discharge-overcurrent, and
  short-circuit thresholds.
- Continuous and peak current rating.
- Connector labels, pack polarity, load/charger sides, and whether protection is
  already built into the selected cell.

## Risks

- Connector-label ambiguity can reverse polarity or bypass protection.
- Protection thresholds may not match the selected cell chemistry or current
  budget.
- Current rating may be lower than radio transmit plus LCD backlight and ESP32
  peak load.

## Required next evidence

- Exact board source and IC marking.
- Connector label and polarity record.
- Threshold and current-rating source.
- Measurement plan that does not bypass protection.
- Owner review before any cell, charger, or load connection.
