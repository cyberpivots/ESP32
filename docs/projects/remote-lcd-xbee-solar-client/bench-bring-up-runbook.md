# Bench Bring-Up Runbook

## Status

This is a non-executable bring-up outline. It records the evidence sequence
that a future owner should satisfy before any battery, solar, XBee, LCD,
encoder, or ESP32 wiring action.

## Verified facts

- This scaffold authorizes documentation only and no bench mutation. Source ID:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`.
- The private hardware submodules are docs-only evidence lanes and do not
  authorize bench mutation. Source ID:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-PRIVATE-SUBMODULES-2026-05-26`.
- The current XBee path remains read-only discovery only, with no setting
  writes, no API transmit frames, and no ESP32 DIN/DOUT wiring. Source IDs:
  `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`,
  `SRC-DIGI-XBEE-900HP-USER-GUIDE`.
- Battery, protection, charger, and fuel-gauge sources are candidate/reference
  only and do not verify local modules. Source IDs: `SRC-TI-BQ25185`,
  `SRC-TI-BQ2970`, `SRC-TI-BQ27441-G1`, `SRC-UL-LIION-SAFETY`.

## Assumptions

- Future bring-up should be broken into separate inspection, source review,
  power-path review, and low-voltage proof records.
- Each stage should stop on identity mismatch, unreadable markings, missing
  source, unexpected voltage, unexpected continuity, heat, smell, swelling,
  corrosion, damaged wiring, or unplanned current draw.

## Stage 0 - Source and identity packet

Required before bench action:

- Exact part sources for ESP32 board, XBee carrier, LCD, encoder, cell, BMS,
  charger, panel, protection, and enclosure.
- Photos or physical-inspection notes for markings and connector labels.
- A recovery plan for ESP32 boot/flash access.
- A private evidence location for raw local captures if needed.

Stop condition: any exact part remains unidentified.

## Stage 1 - Unpowered hardware inspection

Required evidence:

- Board and module markings.
- Connector labels and polarity markings.
- Visible damage, corrosion, swelling, or missing insulation.
- Jumper positions and switch positions.
- Antenna and enclosure constraints.

Stop condition: any battery, charger, panel, or connector label is ambiguous.

## Stage 2 - Power-path review

Required evidence before energizing:

- Cell chemistry and charge voltage.
- Protection-board thresholds and current rating.
- Charger input range, charge current, thermistor policy, and load-sharing
  behavior.
- Solar panel open-circuit voltage and short-circuit current.
- Current-limited supply plan, measurement points, and rollback path.

Stop condition: no source-backed current limit, charge limit, or protection
threshold exists.

## Stage 3 - Peripheral low-voltage proof

Required evidence before wiring to ESP32:

- LCD logic voltage, pullup voltage, I2C address, and backlight current.
- Encoder pullup/debounce plan and boot-pin review.
- XBee carrier logic voltage, DIN/DOUT naming, and read-only proof result.
- ESP32 selected pins and boot/recovery proof.

Stop condition: any peripheral could drive an ESP32 pin outside the verified
voltage domain or interfere with boot/recovery.

## Stage 4 - Owner review

Required owner review:

- Hardware owner reviews power, cell, protection, charger, and enclosure.
- Communications owner reviews XBee read-only evidence and future carrier
  boundary.
- Firmware owner reviews framework ADR status before implementation.
- QA owner reviews evidence packet completeness and stop-condition handling.

## Unknowns

- No current physical evidence packet exists for this project lane.
- No power budget, charger module, battery condition, or pin map has been
  verified.
- No live XBee read-only proof has been run for this lane.

## Stop gates

Do not execute this runbook as a procedure. It is a checklist for the evidence
that a future approved procedure must contain.
