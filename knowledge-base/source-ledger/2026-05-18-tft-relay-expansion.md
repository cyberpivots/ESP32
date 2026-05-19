# Source Ledger - 2026-05-18 TFT Relay Expansion

## Scope

Source-backed revision for adding a parallel R61509V TFT planning branch while
freeing ESP32 GPIO pressure by moving relay outputs away from direct GPIO and
away from analog multiplexers.

## Verified Facts

- TI identifies CD74HC4067 as a 16:1, one-channel analog
  multiplexer/demultiplexer. Source ID: `SRC-TI-CD74HC4067`.
- TI identifies TCA9555 as a 16-bit I2C/SMBus I/O expander with configuration
  and output registers. Source ID: `SRC-TI-TCA9555`.
- Espressif publishes an ESP-IDF component registry entry for an MCP23017 I/O
  expander driver. Source ID: `SRC-ESPRESSIF-MCP23017-COMPONENT`.
- TI identifies TPIC6B595 as an 8-bit power shift register with a storage
  register and open-drain DMOS outputs, with relay and solenoid application
  context. Source ID: `SRC-TI-TPIC6B595`.
- External R61509V TFT references show parallel display interfaces can consume a
  large GPIO set. Source IDs: `SRC-NOPNOP2002-ESP-IDF-PARALLEL-TFT`,
  `SRC-LCDWIKI-R61509V-MRB2802`.

## Assumptions

- The user-requested Open-Smart R61509V TFT remains the display planning target,
  but exact module identity, pinout, power, touch behavior, and driver path are
  not verified by this ledger.
- GPIO pressure from a future parallel TFT makes direct relay GPIO assignment a
  poor first architecture unless later bench evidence proves it is simpler and
  safe.
- Relay output expansion should prefer a latched I/O expander path over a mux
  path because relay states must remain independently held between writes.

## Unresolved Gaps

- Exact Open-Smart R61509V module model, revision, pinout, touch interface,
  backlight behavior, current draw, and whether it matches any cited reference.
- Final TFT data/control pin allocation on the photographed ESP32 board and
  expansion shield.
- Final I2C expander choice, board/module source, address pins, pullups, power
  rail, reset/default state, and readback behavior.
- Relay driver-stage choice after trigger polarity, input current, logic voltage,
  and isolation behavior are verified on the exact relay module.
- Whether any TFT, mux, expander, MicroSD, XBee, or relay signals collide with
  ESP32 strapping, flash, UART0, ADC1/ADC2, Wi-Fi, or shield-routing limits.
