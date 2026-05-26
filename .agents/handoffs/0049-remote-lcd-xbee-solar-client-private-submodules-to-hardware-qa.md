# Handoff 0049: Remote LCD XBee Solar Client Private Submodules To Hardware QA

## Status

Seven private docs-only hardware submodules are created, seeded, and added to
the parent ESP32 repo. No hardware action is authorized.

## Verified facts

- Private GitHub repos exist on `main` for ESP32 client node, XBee-PRO S3B,
  20x4 I2C LCD, rotary encoder, 18650 cell, BMS/protection, and solar
  charger/power path.
- `.gitmodules` uses HTTPS URLs under `https://github.com/cyberpivots/`.
- Each submodule contains only docs, a source index, known gaps, a task record,
  and a Hardware QA handoff.
- Antenna review remains inside the XBee repo. Fuse/protection and enclosure
  review remain inside the solar charger/power-path repo.

## Assumptions

- Hardware QA should begin with exact part identity and source intake, not
  wiring.
- Raw photos, local serial identifiers, and unredacted bench records should stay
  private unless a publication review classifies them otherwise.

## Unknowns

- Exact hardware identity for every requested module remains unresolved.
- No power budget, cell condition record, charger threshold record, enclosure
  review, pin map, XBee carrier review, antenna review, or live proof exists for
  this lane.

## Hardware QA next steps

1. Review each private submodule `docs/hardware-intake.md` and
   `research/known-gaps.md`.
2. Collect exact vendor sources and physical markings for each requested module.
3. Record battery, BMS, charger, panel, protection, antenna, and enclosure
   evidence before any electrical action.
4. Review ESP32 boot/recovery and pin-risk constraints before assigning LCD,
   encoder, XBee, charger, or fuel-gauge signals.
5. Create a follow-on task record before any approved bench procedure.

## Stop gates

Do not connect battery, solar, charger, BMS, LCD, encoder, XBee carrier, antenna
hardware, fuse/protection hardware, enclosure hardware, or ESP32 GPIO from this
handoff. Do not select a firmware framework or add firmware source until a
project-specific accepted ADR authorizes it.
