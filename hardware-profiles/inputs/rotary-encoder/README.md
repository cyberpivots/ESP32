# Rotary Encoder Profile

## Status

Planning stub for the `remote-lcd-xbee-solar-client` lane. Exact encoder part
is unresolved.

## Verified facts

- Bourns documents PEC11R as a contacting incremental encoder family with
  detent and switch options, PC pins, 12/18/24 PPR options, and 1 mA at 5 VDC
  circuit compatibility. This is candidate/reference coverage only and does not
  verify the exact encoder. Source ID: `SRC-BOURNS-PEC11R`.
- This workspace has not verified the exact encoder part, detent count, switch
  option, pullup/debounce circuit, voltage domain, or mounting. Source ID:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`.

## Assumptions

- Encoder rotation and switch input are future UI intents only.
- Encoder input must not directly trigger radio transmission, charging actions,
  or safety-critical state changes.

## Unknowns

- Exact encoder vendor, part number, pulses per revolution, detents, switch
  option, shaft/bushing style, and mounting.
- Required pullups, debounce method, shielding/noise handling, and ESD needs.
- Whether any encoder signal could be assigned to an ESP32 boot-sensitive pin.

## Risks

- Mechanical bounce can create multiple intents if firmware later omits debounce.
- Pullup voltage can exceed ESP32 input limits if tied to a 5 V rail.
- Switch or encoder defaults can interfere with boot if assigned to strapping
  pins.

## Required next evidence

- Exact encoder datasheet or vendor page.
- Physical inspection of markings and pinout.
- Debounce and pullup plan tied to selected ESP32 pins.
- Boot-pin review before wiring.
