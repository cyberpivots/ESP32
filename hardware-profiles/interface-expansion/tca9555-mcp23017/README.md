# TCA9555 / MCP23017 GPIO Expander Profile

## Status

Planning-only relay-output-expansion profile. The relay module is still blocked
until trigger polarity, input current, voltage compatibility, and isolation
behavior are verified.

## Verified Facts

- TI identifies TCA9555 as a 16-bit I2C/SMBus I/O expander with configuration
  registers, output registers, address pins, and latched outputs. Source ID:
  `SRC-TI-TCA9555`.
- Espressif publishes an ESP-IDF component registry entry for an MCP23017 I/O
  expander driver and describes the MCP23017 as the I2C member of a 16-bit I/O
  expander family. Source ID: `SRC-ESPRESSIF-MCP23017-COMPONENT`.

## Assumptions

- A future v1 relay expansion path should use ESP32 I2C to a latched GPIO
  expander, then a verified relay driver stage, before relay-module inputs.
- Expander outputs are command-state mirrors only; all relay changes still come
  from `relay_manager` after `safety_supervisor` approval.

## Required Verification Checklist

| Item | Required evidence before relay use |
| --- | --- |
| Exact expander board | Manufacturer, schematic, pullups, address pins, reset/default behavior, and power rail. |
| I2C bus | Selected ESP32 pins, pullup voltage, scan result, address conflict review, and bus recovery behavior. |
| Output defaults | Measured inactive state before firmware accepts relay commands. |
| Output latch behavior | LED or logic-analyzer proof that unrelated TFT/mux scans do not change relay states. |
| Driver stage | Selected only after exact relay-module trigger polarity, input current, voltage, and isolation are verified. |

## Unknowns

- Final expander selection, address, I2C pins, pullup source, board reset state,
  output current limits, readback policy, and fault handling.
- Whether the eventual relay module input can be driven through an expander plus
  driver without defeating isolation or creating boot glitches.
