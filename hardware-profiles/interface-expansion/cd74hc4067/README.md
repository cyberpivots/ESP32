# CD74HC4067 Analog Multiplexer Profile

## Status

Planning-only input-expansion profile. This device is not approved as a direct
relay output surface for `four-relay-xbee-wifi`.

## Verified Facts

- TI identifies CD74HC4067 as a 16:1, one-channel analog
  multiplexer/demultiplexer. Source ID: `SRC-TI-CD74HC4067`.
- TI lists analog switching behavior, break-before-make behavior, and an enable
  control that disables all switches when asserted. Source ID:
  `SRC-TI-CD74HC4067`.

## Assumptions

- The mux can be useful for slow, non-safety-critical input routing such as
  resistive touch, buttons, potentiometers, or sensor reads after voltage and ADC
  limits are verified.
- The mux is rejected for independent relay state holding because it selects an
  analog path rather than storing multiple output states.

## Allowed First Proof

- ADC1 test voltages only.
- One selected input at a time.
- No relay module inputs, relay coils, TFT parallel data bus reduction, or
  safety-critical output selection.

## Unknowns

- Exact breakout/module, power rail, enable polarity at the board level, address
  line wiring, on-resistance impact on the selected input, and ADC protection
  network.
- Whether the selected ESP32 ADC pins remain usable with Wi-Fi, TFT, MicroSD,
  XBee, and shield routing.
