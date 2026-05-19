# Open-Smart R61509V TFT Planning Profile

## Status

User-requested display planning target. Exact module identity and bench evidence
are not yet verified in this workspace.

## Verified Facts

- External ESP-IDF TFT notes include an OPEN-SMART R61509V 16-pin parallel
  target and warn that exact display selection matters. Source ID:
  `SRC-NOPNOP2002-ESP-IDF-PARALLEL-TFT`.
- A candidate R61509V module reference documents 8-bit/16-bit parallel interface
  options and many data/control pins. Source ID: `SRC-LCDWIKI-R61509V-MRB2802`.

## Assumptions

- Adding the requested TFT will increase GPIO pressure enough that relay outputs
  should move to a latched expander branch rather than occupying the current
  direct-GPIO candidates.
- TFT touch inputs, if present on the exact module, are UI-intent sources only;
  they must not directly change relay state.

## Required Verification Checklist

| Item | Required evidence before wiring |
| --- | --- |
| Exact display module | Photo/inspection and source record for manufacturer, model, revision, driver IC, touch interface, backlight, and pinout. |
| Power path | Required voltage rails, current draw, backlight control, and regulator behavior. |
| Data/control bus | 8-bit versus 16-bit mode, control pins, reset/read/write behavior, and ESP32 pin conflicts. |
| Touch path | Resistive/capacitive type, signal voltage, ADC/SPI needs, interrupt behavior, and debounce/noise handling. |
| Firmware driver | Project-approved framework integration after implementation gate; no firmware dependency is added by this profile. |

## Unknowns

- Whether the user's Open-Smart R61509V module matches either cited external
  reference.
- Final TFT GPIO allocation, touch routing, backlight driver needs, and whether
  display bus activity creates relay, XBee, MicroSD, or boot-pin conflicts.
