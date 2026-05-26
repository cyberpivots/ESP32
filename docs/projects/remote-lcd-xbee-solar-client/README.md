# Remote LCD XBee Solar Client

## Goal

Scaffold a documentation-only project lane for a remote ESP32 client node with
local LCD status, rotary input, Digi XBee telemetry, and a future
solar-recharged single-cell power path.

This lane is framework-neutral. It does not add firmware source, framework
project files, XBee write procedures, battery charging procedures, solar wiring
instructions, or ESP32 pin assignments.

## Package map

- [Separate hardware development stream](development-stream.md)
- [Submodule map](submodule-map.md)
- [Architecture](architecture.md)
- [Hardware intake](hardware-intake.md)
- [Power and safety](power-and-safety.md)
- [Pin risk matrix](pin-risk-matrix.md)
- [Bench bring-up runbook](bench-bring-up-runbook.md)
- [XBee boundary](xbee-boundary.md)
- [Private ESP32 client node submodule](../../../submodules/hardware/rlxsc-esp32-client-node/README.md)
- [Private XBee-PRO S3B submodule](../../../submodules/hardware/rlxsc-xbee-pro-s3b/README.md)
- [Private 20x4 I2C LCD submodule](../../../submodules/hardware/rlxsc-lcd-20x4-i2c/README.md)
- [Private rotary encoder submodule](../../../submodules/hardware/rlxsc-rotary-encoder/README.md)
- [Private 18650 cell submodule](../../../submodules/hardware/rlxsc-18650-cell/README.md)
- [Private BMS/protection submodule](../../../submodules/hardware/rlxsc-bms-protection/README.md)
- [Private solar charger/power-path submodule](../../../submodules/hardware/rlxsc-solar-charger-power-path/README.md)
- [20x4 I2C LCD profile](../../../hardware-profiles/displays/20x4-i2c-lcd/README.md)
- [Rotary encoder profile](../../../hardware-profiles/inputs/rotary-encoder/README.md)
- [Remote ESP32 client node profile](../../../hardware-profiles/esp32/remote-lcd-xbee-client-node/README.md)
- [18650 cell profile](../../../hardware-profiles/power/18650-cell/README.md)
- [BMS/protection profile](../../../hardware-profiles/power/bms-protection/README.md)
- [Solar charger/power-path profile](../../../hardware-profiles/power/solar-charger-power-path/README.md)
- [Existing XBee profile](../../../hardware-profiles/xbee/xbp9b-dput-001/README.md)
- [Source ledger](../../../knowledge-base/source-ledger/2026-05-26-remote-lcd-xbee-solar-client.md)
- [Separate hardware stream source ledger](../../../knowledge-base/source-ledger/2026-05-26-remote-lcd-xbee-solar-client-separate-hardware-stream.md)

## Verified facts

- The current workspace remains framework-neutral outside project-specific
  accepted ADRs. This project lane has no accepted framework ADR and adds no
  framework-specific files. Source ID:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`.
- Seven private hardware Git submodules now exist under `submodules/hardware/`,
  each seeded with docs-only content on `main`. Source ID:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-PRIVATE-SUBMODULES-2026-05-26`.
- This lane is now recorded as a separate hardware-device development stream
  from ESP-NOW BBS, Win31/DOS-C, Gate F runtime, Gate G export, Gate H proof,
  mesh, BLE, network, relay, TFT, MicroSD, load, and mains work. Source ID:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SEPARATE-HARDWARE-STREAM-2026-05-26`.
- Digi identifies `XBP9B-DPUT-001` as an XBee-PRO 900HP S3B
  Point2Multipoint, 900 MHz, 250 mW, U.FL, 10 kbps model. Source ID:
  `SRC-DIGI-XBP9B-DPUT-001`.
- The existing XBee bench boundary is read-only discovery only: no setting
  writes, no API transmit frames, and no ESP32 DIN/DOUT carrier wiring. Source
  IDs: `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`,
  `SRC-DIGI-XBEE-900HP-USER-GUIDE`.
- NXP documents PCF8574/74A as an 8-bit I2C-bus I/O expander with interrupt;
  this is candidate/reference coverage only and does not verify the exact LCD
  backpack. Source ID: `SRC-NXP-PCF8574-74A`.
- Bourns documents PEC11R as a contacting incremental encoder family; this is
  candidate/reference coverage only and does not verify the exact encoder.
  Source ID: `SRC-BOURNS-PEC11R`.
- TI documents BQ25185 as a one-cell linear charger with power path and solar
  input support; this is candidate/reference coverage only and does not select
  a charger module. Source ID: `SRC-TI-BQ25185`.
- TI documents BQ2970 as a single-cell Li-ion/Li-poly battery protector; this
  is candidate/reference coverage only and does not verify the local BMS board.
  Source ID: `SRC-TI-BQ2970`.
- TI documents BQ27441-G1 as a system-side single-cell Li-ion battery fuel
  gauge with I2C communication; this is candidate/reference coverage only and
  does not select a gauge. Source ID: `SRC-TI-BQ27441-G1`.
- UL lithium-ion battery safety guidance is retained as broad hazard context;
  it is not a project-specific 18650 charging, wiring, or enclosure procedure.
  Source ID: `SRC-UL-LIION-SAFETY`.

## Assumptions

- The private Git submodules are evidence and ownership lanes; they do not
  authorize firmware, wiring, charging, radio writes, or bench action.
- This is a distinct project lane, not an extension of
  `four-relay-xbee-wifi`.
- Future user-facing behavior may include display status lines, rotary encoder
  intents, radio telemetry boundaries, and power-state reporting, but those are
  documentation-only sketches until an accepted ADR defines implementation
  contracts.

## Unknowns

- Exact ESP32 board, module, carrier, regulator, USB-UART bridge, power input,
  and boot/recovery method.
- Exact 20x4 LCD module, LCD controller, I2C backpack, I2C address, pullups,
  voltage, backlight current, and mechanical mounting.
- Exact rotary encoder part, switch option, detent count, pulse count, debounce
  needs, voltage domain, and mounting.
- Exact 18650 cell manufacturer, model, chemistry, capacity, discharge rating,
  charge limit, protection status, age, and condition.
- Exact BMS/protection board, FET topology, protection thresholds, continuous
  current rating, and connection labels.
- Exact solar panel, charger module, power-path behavior, thermistor policy,
  input current limit, enclosure, fuse/protection parts, and outdoor exposure
  constraints.
- Exact XBee carrier, antenna, regulatory deployment context, current settings,
  UART voltage, DIN/DOUT routing, address plan, and key provisioning process.

## Hard gates

No firmware implementation, framework selection, XBee setting write, API
transmit frame, ESP32-to-XBee wiring, battery charging, solar connection,
battery pack assembly, or power-path wiring is authorized by this scaffold.

Stop before any bench action until power, voltage, boot-pin, isolation, battery
safety, XBee carrier, antenna, enclosure, protection, recovery, and evidence
record requirements are satisfied.
