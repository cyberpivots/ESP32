# TFT And Relay Expansion

## Goal

Retain the user-requested Open-Smart R61509V TFT planning branch while revising
relay pin relief to use latched output expansion instead of a direct analog mux
relay surface.

## Verified Facts

- CD74HC4067 is a 16:1, one-channel analog multiplexer/demultiplexer. Source ID:
  `SRC-TI-CD74HC4067`.
- TCA9555 is a 16-bit I2C/SMBus I/O expander with configuration and output
  registers. Source ID: `SRC-TI-TCA9555`.
- Espressif publishes an MCP23017 ESP-IDF component registry entry for future
  firmware work. Source ID: `SRC-ESPRESSIF-MCP23017-COMPONENT`.
- TPIC6B595 is a relay-driver reference with an 8-bit storage register and
  open-drain DMOS outputs. Source ID: `SRC-TI-TPIC6B595`.
- External R61509V planning references show parallel TFT modules can require
  many data and control pins. Source IDs:
  `SRC-NOPNOP2002-ESP-IDF-PARALLEL-TFT`,
  `SRC-LCDWIKI-R61509V-MRB2802`.

## Assumptions

- The Open-Smart R61509V TFT remains the requested display target, but exact
  module identity, pinout, power, touch behavior, and firmware driver path remain
  unverified.
- Relay GPIOs should be freed where possible because TFT, MicroSD, XBee, and mux
  inputs all compete for ESP32 pins.
- Relay output state must be independently latched and recoverable through a
  health gate. An analog mux is not that surface.

## Revised Architecture

```text
ESP32
  |
  +-- Parallel TFT branch
  |     +-- R61509V display bus, control pins, backlight, and touch pending proof
  |
  +-- I2C relay expansion branch
  |     +-- MCP23017 or TCA9555 latched GPIO expander
  |           +-- relay driver stage selected after relay input proof
  |                 +-- relay module inputs, contacts still disconnected
  |
  +-- CD74HC4067 input branch
        +-- touch ADC routing, buttons, pots, or low-rate sensors only
```

## Relay Expansion Rules

- Preferred v1 relay-control architecture:
  `ESP32 I2C -> MCP23017 or TCA9555 -> verified driver stage -> relay module inputs`.
- Expander outputs mirror only approved relay states from `relay_manager`.
- Driver-stage selection is blocked until exact relay trigger polarity, input
  current, logic voltage, and isolation behavior are verified.
- Initial output proof uses LEDs or a logic analyzer, not relay-module inputs or
  relay coils.
- Direct ESP32 GPIO relay drive remains a fallback only if TFT pin pressure is
  removed and relay/shield evidence closes every direct-GPIO gate.

## Mux Rules

Allowed:

- Resistive touch or other slow ADC routing after voltage and ADC limits are
  verified.
- Buttons, potentiometers, status inputs, or low-rate sensors.

Not allowed:

- Direct relay state holding.
- TFT parallel data bus reduction.
- Safety-critical output selection.
- Mux-plus-latch relay output design for v1.

## Firmware Model Update

Add these future tasks beneath the existing relay and UI model:

| Task | Responsibility | Inputs | Outputs |
| --- | --- | --- | --- |
| `relay_expander` | Initialize expander pins inactive, mirror approved relay states to the latched expander, read back health when supported, and fault the hardware gate on write/readback failure. | Approved relay state snapshot, expander config, I2C health. | Expander writes, readback status, `relayExpander` state fields, hardware-gate fault. |
| `mux_scan` | Scan CD74HC4067 input channels at low rate and publish filtered input events. | Mux address pins, ADC result, debounce/filter config. | `mux.ready`, input observations, UI-intent events only. |

State snapshots add:

```json
{
  "relayExpander": {
    "present": false,
    "ready": false,
    "lastWrite": "none"
  },
  "mux": {
    "ready": false
  }
}
```

TFT touch buttons and mux-derived inputs are UI intents only. Any all-off or
relay change still uses the same relay-manager command path and
`safety_supervisor` gate as HTTP and XBee commands.

## Safety Behavior

- On boot, expander pins initialize inactive before relay commands are accepted.
- If expander init, write, or required readback fails, `hardwareGateClosed` is
  false and relay commands return `hardware_gate_open`.
- TFT, mux, storage, and XBee scans must not change expander outputs.
- All relay contacts remain disconnected or limited to a reviewed low-voltage
  dummy load until relay-module and load gates close.

## Proof Sequence

1. Verify CD74HC4067 with ADC1 test voltages only.
2. Verify MCP23017 or TCA9555 I2C detection, address pins, pullups, and inactive
   output defaults.
3. Verify expander latch behavior on LEDs or a logic analyzer.
4. Run unrelated TFT and mux scans while confirming relay-expander output state
   does not glitch.
5. Only after relay-module polarity/current/voltage/isolation evidence exists,
   test one relay channel through the selected driver stage.

## Unknowns

- Exact Open-Smart R61509V module identity, pinout, power, backlight, touch
  hardware, and driver compatibility.
- Final TFT pin allocation and whether it conflicts with relay, MicroSD, XBee,
  boot, flash, UART0, ADC, or shield-routing constraints.
- Final GPIO expander part, board, I2C address, pullups, reset/default behavior,
  output current, readback policy, and driver-stage interface.
- Exact relay module trigger polarity, input current, 3.3 V compatibility,
  `JD-VCC`/`VCC` behavior, and isolation boundary.
