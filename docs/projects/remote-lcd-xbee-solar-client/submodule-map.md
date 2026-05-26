# Submodule Map

## Verified facts

- This repository now tracks seven private Git submodules for this project lane
  under `submodules/hardware/`. Source ID:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-PRIVATE-SUBMODULES-2026-05-26`.
- Each private submodule has a docs-only initial commit on `main` and contains
  only `README.md`, `AGENTS.md`, `docs/`, `knowledge-base/`, `research/`, a
  task record, and a Hardware QA handoff. Source ID:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-PRIVATE-SUBMODULES-2026-05-26`.
- Existing XBee coverage is for Digi `XBP9B-DPUT-001` and the current
  read-only proof boundary. Source IDs: `SRC-DIGI-XBP9B-DPUT-001`,
  `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`.

## Assumptions

- Each lane may later receive firmware, hardware, QA, or communications work
  only after source-backed intake closes the relevant unknowns.

## Private submodules

| Submodule path | Private repo | Owner lane | Acceptance boundary |
| --- | --- | --- | --- |
| `submodules/hardware/rlxsc-esp32-client-node` | `cyberpivots/rlxsc-esp32-client-node` | Hardware plus Architecture | Exact board, boot pins, recovery, power path, and framework ADR |
| `submodules/hardware/rlxsc-xbee-pro-s3b` | `cyberpivots/rlxsc-xbee-pro-s3b` | Communications plus Hardware | Read-only discovery, carrier and antenna review, no writes |
| `submodules/hardware/rlxsc-lcd-20x4-i2c` | `cyberpivots/rlxsc-lcd-20x4-i2c` | Hardware plus Firmware later | Exact module, voltage, address, pullups, and backlight evidence |
| `submodules/hardware/rlxsc-rotary-encoder` | `cyberpivots/rlxsc-rotary-encoder` | Hardware plus Firmware later | Exact part, debounce, pullups, voltage, and boot-pin review |
| `submodules/hardware/rlxsc-18650-cell` | `cyberpivots/rlxsc-18650-cell` | Hardware plus QA | Exact cell datasheet, inspection, protection status, condition, and safe storage record |
| `submodules/hardware/rlxsc-bms-protection` | `cyberpivots/rlxsc-bms-protection` | Hardware plus QA | Exact board schematic/source, thresholds, FET path, current rating, and connector labels |
| `submodules/hardware/rlxsc-solar-charger-power-path` | `cyberpivots/rlxsc-solar-charger-power-path` | Hardware plus QA | Exact panel, charger, thermistor policy, current limit, load sharing, fuse/protection, and enclosure review |

## Development order

1. Complete source-backed hardware identity intake in each private submodule.
2. Prioritize power and safety review in `rlxsc-18650-cell`,
   `rlxsc-bms-protection`, and
   `rlxsc-solar-charger-power-path`.
3. Then review board and interface risks in `rlxsc-esp32-client-node`,
   `rlxsc-lcd-20x4-i2c`, `rlxsc-rotary-encoder`, and
   `rlxsc-xbee-pro-s3b`.
4. Write parent hardware ADRs only after submodule evidence exists.
5. Keep any early behavior prototype host-only and outside hardware evidence
   submodules.

## Unknowns

- Whether the LCD and fuel-gauge paths share an I2C bus, use separate buses, or
  remain unimplemented.
- Whether the final power architecture includes a fuel gauge.
- Whether any exact selected antenna, fuse/protection part, or enclosure later
  justifies a separate private repo.

## Stop gates

Do not add firmware packages, wiring diagrams, accepted interface contracts,
XBee writes/transmit frames, battery/solar wiring, or live bench instructions
from this map. Future module work must cite source IDs or remain marked
unresolved.
