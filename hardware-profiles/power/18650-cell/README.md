# 18650 Cell Profile

## Status

Planning stub for the `remote-lcd-xbee-solar-client` lane. Exact 18650 cell is
unresolved.

## Verified facts

- This workspace has not verified an exact 18650 cell manufacturer, model,
  chemistry, capacity, discharge rating, charge limit, protection status, age,
  or condition. Source ID:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`.
- UL lithium-ion battery safety guidance is retained as broad hazard context;
  it is not a project-specific 18650 charging, wiring, storage, or enclosure
  procedure. Source ID: `SRC-UL-LIION-SAFETY`.

## Assumptions

- The cell remains disconnected and unused until exact source and inspection
  records exist.
- Any future cell use must include protection, charging, storage, transport,
  enclosure, and thermal review.

## Unknowns

- Cell manufacturer, model, chemistry, capacity, charge voltage, maximum charge
  current, continuous discharge rating, and operating temperature range.
- Whether the cell is protected or unprotected.
- Cell age, previous use, damage, swelling, corrosion, or measured condition.
- Required holder, strain relief, fuse/protection, and enclosure.

## Risks

- Mismatched charging voltage or chemistry can damage the cell.
- Unknown cell condition can create heat, leakage, venting, or fire risk.
- Unprotected cells can expose the project to short-circuit and overdischarge
  hazards.
- Outdoor or enclosed deployment can increase temperature and condensation risk.

## Required next evidence

- Exact cell datasheet or vendor source.
- Physical inspection and condition record.
- Protection status and holder/enclosure review.
- Charge limit and discharge-current budget tied to the selected charger,
  protection board, ESP32, XBee, LCD, and any backlight load.
