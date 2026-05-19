# Firmware Interfaces

This folder holds framework-neutral interface contracts. Do not add
framework-specific implementation until ADR-0001 is accepted.

Planned interfaces:

- board identity,
- flash/recovery,
- GPIO,
- relay control,
- relay expander health,
- mux scan inputs,
- TFT UI intents,
- radio transport,
- web/HTML control surfaces,
- diagnostics.

Source IDs for the current `four-relay-xbee-wifi` expansion interface planning:
`SRC-TI-TCA9555`, `SRC-ESPRESSIF-MCP23017-COMPONENT`,
`SRC-TI-CD74HC4067`, `SRC-NOPNOP2002-ESP-IDF-PARALLEL-TFT`.

Unknowns remain the exact expander board, mux breakout, TFT module, driver
stage, and final firmware implementation shape.
