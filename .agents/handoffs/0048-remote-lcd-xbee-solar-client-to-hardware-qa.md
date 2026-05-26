# Handoff 0048: Remote LCD XBee Solar Client To Hardware QA

## Status

Documentation-only scaffold is ready for Hardware and QA review. No hardware
action is authorized.

## Verified facts

- New project lane:
  `docs/projects/remote-lcd-xbee-solar-client/README.md`.
- Follow-on private Git submodule implementation is tracked in
  [../TASK_LOG/0060-remote-lcd-xbee-solar-client-private-submodules.md](../TASK_LOG/0060-remote-lcd-xbee-solar-client-private-submodules.md).
- Hardware profile stubs exist for the ESP32 client node, 20x4 I2C LCD, rotary
  encoder, 18650 cell, BMS/protection, and solar charger/power path.
- Existing `XBP9B-DPUT-001` source/profile coverage is reused and the current
  XBee read-only gate remains closed to writes, transmit frames, and ESP32
  carrier wiring.
- New PCF8574/74A, PEC11R, BQ25185, BQ2970, BQ27441-G1, and UL lithium-ion
  safety sources are candidate/reference-only, not selected parts.

## Assumptions

- Hardware QA should begin with source intake and physical identity evidence,
  not wiring.
- Raw photos, local serial identifiers, and unredacted bench records should stay
  private unless a publication review classifies them otherwise.

## Unknowns

- Exact hardware identity for every requested module remains unresolved.
- No power budget, cell condition record, charger threshold record, enclosure
  review, pin map, XBee carrier review, or live proof exists for this lane.

## Hardware QA next steps

1. Collect exact vendor sources and physical markings for each requested module.
2. Record battery, BMS, charger, panel, protection, and enclosure evidence
   before any electrical action.
3. Review ESP32 boot/recovery and pin-risk constraints before assigning LCD,
   encoder, XBee, charger, or fuel-gauge signals.
4. Run only the existing XBee read-only proof path after carrier identity and
   host serial evidence exist.
5. Create a follow-on task record before any approved bench procedure.

## Stop gates

Do not connect battery, solar, charger, BMS, LCD, encoder, XBee carrier, or ESP32
GPIO from this handoff. Do not select a firmware framework or add firmware
source until a project-specific accepted ADR authorizes it.
