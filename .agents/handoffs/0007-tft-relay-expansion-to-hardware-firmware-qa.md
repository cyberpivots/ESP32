# Handoff 0007 - TFT Relay Expansion To Hardware Firmware QA

## From

Architect, QA

## To

Hardware, Firmware, QA

## Summary

The `four-relay-xbee-wifi` package now carries the revised TFT and relay
expansion plan:

- Open-Smart R61509V is retained only as a planning target until exact module
  evidence exists.
- CD74HC4067 is input-only for touch/buttons/pots/sensors and is rejected as a
  relay-output state holder.
- Relay pin relief moves to a latched GPIO expander branch using MCP23017 or
  TCA9555, followed by a driver stage selected only after relay input evidence.
- Static and telemetry state contracts now include `relayExpander.present`,
  `relayExpander.ready`, `relayExpander.lastWrite`, and `mux.ready`.

## Required Next Checks

- Hardware must verify the exact TFT module, power/backlight, data/control pins,
  touch interface, and ESP32 pin conflicts.
- Hardware must verify the exact CD74HC4067 breakout, voltage limits,
  address/enable pins, ADC1 path, source impedance, and protection network.
- Hardware must verify the exact MCP23017/TCA9555 board, I2C address pins,
  pullups, reset/default behavior, inactive outputs, and output latch behavior.
- Hardware must close relay trigger polarity, input current, 3.3 V compatibility,
  `JD-VCC`/`VCC` behavior, and isolation before any expander/driver output is
  connected to relay-module inputs.
- Firmware must keep TFT touch, mux inputs, HTTP, and XBee commands routed
  through `relay_manager` and `safety_supervisor`.
- QA must validate expander failure returns `hardware_gate_open` and keeps
  `hardwareGateClosed=false`.

## Blockers

- Exact Open-Smart R61509V module source and bench identity are unresolved.
- Exact CD74HC4067 breakout and ADC protection are unresolved.
- Exact relay expander board and driver stage are unresolved.
- Exact relay-module electrical behavior is unresolved.
- No TFT wiring, relay-expander-to-relay wiring, relay switching, XBee writes,
  firmware flashing, or mains/load wiring is approved by this handoff.

## Evidence

- Source IDs are recorded in `knowledge-base/source-index.md`.
- The source-backed revision ledger is
  `knowledge-base/source-ledger/2026-05-18-tft-relay-expansion.md`.
- The main project contract is
  `docs/projects/four-relay-xbee-wifi/tft-relay-expansion.md`.
- Validation results are recorded in
  `.agents/TASK_LOG/0010-tft-relay-expansion.md`.
