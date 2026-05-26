# Architecture

## Verified facts

- This scaffold defines documentation-only future boundaries and does not add
  runtime APIs, wire formats, firmware source, or framework files. Source ID:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`.
- Private hardware submodules now exist for ESP32 client node, XBee-PRO S3B,
  20x4 I2C LCD, rotary encoder, 18650 cell, BMS/protection, and solar
  charger/power path. Source ID:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-PRIVATE-SUBMODULES-2026-05-26`.
- Espressif source coverage exists for ESP32 GPIO and UART review, but the exact
  client board is unresolved. Source IDs: `SRC-ESP-IDF-GPIO`,
  `SRC-ESP-IDF-UART`, `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.
- Digi source coverage exists for the `XBP9B-DPUT-001` radio and XBee-PRO 900HP
  API documentation. Source IDs: `SRC-DIGI-XBP9B-DPUT-001`,
  `SRC-DIGI-XBEE-900HP-USER-GUIDE`.
- Candidate/reference source coverage exists for a PCF8574/74A I2C I/O
  expander class, PEC11R encoder family, BQ25185 charger/power-path IC,
  BQ2970 battery protector, and BQ27441-G1 fuel gauge. Source IDs:
  `SRC-NXP-PCF8574-74A`, `SRC-BOURNS-PEC11R`, `SRC-TI-BQ25185`,
  `SRC-TI-BQ2970`, `SRC-TI-BQ27441-G1`.

## Assumptions

- The client node is a field-visible status and input endpoint, not a relay or
  load controller in this scaffold.
- A future local UI could show link, power, and node state on the LCD while the
  encoder emits local navigation or acknowledgement intents.
- XBee telemetry and command behavior remain closed until a communications ADR
  and bench evidence define source allowlists, payload boundaries, security,
  retry behavior, and rollback.
- Power-state reporting may later include battery voltage, charge state,
  charger status, or fuel-gauge estimates, but no specific sensor or data model
  is selected.

## Documentation-only component boundary

| Component | Future responsibility | Current status |
| --- | --- | --- |
| Client state model | Hold displayable node status, link status, and power status | Not implemented; no accepted data schema |
| LCD view | Render a small set of status lines | Not implemented; exact LCD module unresolved |
| Rotary input | Emit local UI intents such as navigate, select, or acknowledge | Not implemented; exact encoder unresolved |
| XBee transport | Carry telemetry or future commands after read-only gate closes | Blocked; no writes, transmit frames, or ESP32 wiring |
| Power supervisor | Report safe power state and reject unsafe runtime assumptions | Not implemented; exact cell, BMS, charger, and panel unresolved |
| Recovery path | Preserve flash/recovery access and power-off rollback | Not defined; exact board unresolved |

## Future interface sketches

These names are placeholders for planning only. They are not firmware APIs,
serial protocols, or public runtime contracts.

| Sketch | Direction | Gate before acceptance |
| --- | --- | --- |
| Display status lines | State model to LCD | Exact LCD, voltage, I2C address, pullups, and UI requirements |
| Encoder intents | Encoder to state model | Exact encoder, debounce evidence, pullups, and boot-pin review |
| XBee telemetry boundary | State model to radio | Read-only proof, carrier review, address/security plan, and protocol ADR |
| Power-state reporting | Power path to state model | Exact cell, charger, protection, measurement source, and safety review |

## Unknowns

- Final board, firmware framework, scheduling model, memory budget, and power
  budget.
- Final display content, update rate, error states, and local input behavior.
- Whether XBee is telemetry-only or includes future command intake.
- Whether power telemetry comes from raw ADC measurement, charger status pins,
  a fuel gauge, or no runtime measurement at all.

## Stop gates

Do not treat this architecture as an accepted runtime contract. A future ADR is
required before adding framework-specific files, firmware source, wire formats,
XBee commands, battery/solar bench steps, or pin assignments.
