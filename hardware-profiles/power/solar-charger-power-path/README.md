# Solar Charger And Power Path Profile

## Status

Planning stub for the `remote-lcd-xbee-solar-client` lane. Exact solar panel,
charger module, and power path are unresolved.

## Verified facts

- TI documents BQ25185 as a one-cell, 1 A standalone linear battery charger with
  power path and solar input support, including input current limiting and
  battery-tracking VINDPM features. This is candidate/reference coverage only
  and does not select a charger module. Source ID: `SRC-TI-BQ25185`.
- TI documents BQ27441-G1 as a system-side single-cell Li-ion battery fuel
  gauge with I2C communication. This is candidate/reference coverage only and
  does not select a gauge. Source ID: `SRC-TI-BQ27441-G1`.
- This workspace has not verified an exact panel, charger module, charger IC,
  load-sharing behavior, thermistor policy, input range, charge voltage, or
  current limit. Source ID:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`.

## Assumptions

- Solar and battery charging remain blocked until exact hardware is identified.
- Runtime power reporting is optional until a fuel gauge or measurement method
  is selected by a future ADR or owner-reviewed design record.

## Unknowns

- Solar panel voltage/current/power ratings, connector, blocking protection,
  and environmental rating.
- Charger module model, IC, charge voltage, charge current, input current limit,
  thermistor requirements, status pins, and load-sharing behavior.
- Whether the charger SYS output can supply ESP32, XBee transmit current, LCD
  backlight current, and any future peripherals.
- Whether an enclosure creates heat or moisture conditions outside component
  limits.

## Risks

- Solar panel open-circuit voltage can exceed charger input limits.
- Charger modules may not safely support simultaneous load and battery charging
  as assumed.
- Missing thermistor handling can disable charging or create an unsafe charge
  condition.
- Inadequate power-path capacity can trigger ESP32 brownouts during radio
  transmit or LCD backlight use.

## Required next evidence

- Exact panel datasheet or vendor source.
- Exact charger module source and IC marking.
- Charge voltage/current limit record tied to exact cell source.
- Load-sharing/power-path proof before connecting ESP32 or XBee.
- Thermistor, fuse/protection, enclosure, and cable-entry review.
