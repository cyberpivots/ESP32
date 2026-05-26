# Power And Safety

## Verified facts

- BQ25185 is documented by TI as a one-cell linear charger with power path and
  solar input support. This is candidate/reference coverage only; no charger
  module is selected. Source ID: `SRC-TI-BQ25185`.
- BQ2970 is documented by TI as a single-cell Li-ion/Li-poly battery protector.
  This is candidate/reference coverage only; no BMS/protection board is
  verified. Source ID: `SRC-TI-BQ2970`.
- BQ27441-G1 is documented by TI as a system-side single-cell Li-ion battery
  fuel gauge with I2C communication. This is candidate/reference coverage only;
  no fuel gauge is selected. Source ID: `SRC-TI-BQ27441-G1`.
- UL lithium-ion battery safety guidance is retained as broad hazard context
  and does not authorize a project charging or wiring procedure. Source ID:
  `SRC-UL-LIION-SAFETY`.
- Espressif hardware guidelines require ESP32 power, reset, UART, strapping pin,
  and GPIO review before hardware integration claims. Source ID:
  `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.

## Assumptions

- The power system is treated as unsafe to energize until the exact cell,
  protection board, charger, panel, fuse/protection, and enclosure are known.
- A future bench record must start with a current-limited, reversible, observed
  setup and a written recovery path.
- Battery and solar work needs owner review before any physical connection.

## Risks

| Risk | Why it matters | Current status |
| --- | --- | --- |
| Cell charge limit mismatch | Incorrect charge voltage or chemistry can damage a lithium cell | Unresolved |
| Missing or unsuitable protection | Overcurrent, short, overcharge, and overdischarge behavior is unknown | Unresolved |
| Solar panel input mismatch | Panel open-circuit voltage/current can exceed charger/module limits | Unresolved |
| Load sharing ambiguity | Some charger boards cannot safely power load and charge battery as assumed | Unresolved |
| Thermistor omission | Charger behavior may require battery temperature sensing or a valid substitute policy | Unresolved |
| ESP32 brownout or reset instability | Radio transmit and LCD backlight loads can stress the rail | Unresolved |
| Boot-pin conflict | Pullups, encoder switches, LCD backpacks, or radio pins can affect boot | Unresolved |
| Enclosure heat and moisture | Outdoor battery systems need thermal, ingress, and strain-relief review | Unresolved |

## Required next evidence

- Exact battery cell datasheet and physical inspection.
- Exact BMS/protection board source and connector-label proof.
- Exact charger/power-path module source, IC marking, and module schematic if
  available.
- Exact solar panel source with open-circuit voltage, short-circuit current, and
  rated operating conditions.
- Fuse/protection candidate record tied to measured current budget.
- Enclosure and cable-entry review for battery retention, moisture, venting,
  strain relief, and service access.
- ESP32 rail budget including XBee transmit current, LCD backlight current,
  charger SYS behavior, and brownout recovery.

## Stop gates

Do not connect a battery, charger, panel, BMS, ESP32 rail, or XBee power path
from this document. Do not write a charging procedure until the exact hardware
and owner-reviewed safety record exist.
