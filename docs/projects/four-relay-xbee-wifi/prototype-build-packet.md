# Prototype Build Packet

## Purpose

This packet is the public starting point for the ESP32 four-relay workbench
prototype. It gathers the currently verified review path, source links,
conceptual diagrams, bench evidence requirements, unresolved gaps, and stop
conditions in one place.

This is not a final wiring diagram, relay terminal map, mains/load procedure,
XBee write procedure, or live firmware/hardware proof.

## Verified facts

- The public GitHub Pages package is a curated static artifact built from an
  explicit allowlist, with named WebP backplates and source-backed Markdown.
  Source IDs: `SRC-GITHUB-PAGES-CUSTOM-WORKFLOWS`,
  `SRC-LOCAL-PROTOTYPE-PACKET-2026-05-21`.
- The current four-relay target is documented from photo evidence as an
  ESP-WROOM-32-family board and expansion shield, a four-channel relay module
  with Songle `SRD-05VDC-SL-C` relay cans, Digi `XBP9B-DPUT-001 RevF`, and a
  Waveshare XBee USB Adapter. Source IDs:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
  `SRC-SONGLE-SRD-05VDC-SL-C`, `SRC-DIGI-XBP9B-DPUT-001`,
  `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- Espressif GPIO and schematic-checklist sources are the public review sources
  for GPIO, strapping-pin, flash-pin, UART, reset, and 3.3 V power-entry
  concerns. Source IDs: `SRC-ESP-IDF-GPIO`,
  `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.
- Digi identifies `XBP9B-DPUT-001` as an XBee-PRO 900HP S3B Point2Multipoint
  900 MHz, 250 mW, U.FL, 10 kbps model. Source ID:
  `SRC-DIGI-XBP9B-DPUT-001`.
- The XBee bench lane is read-only: passive discovery first, then explicitly
  confirmed fixed AT reads only. Source IDs:
  `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`,
  `SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`,
  `SRC-DIGI-XBEE-900HP-NP`, `SRC-DIGI-XBEE-900HP-USER-GUIDE`.
- CD74HC4067 remains an input-only mux planning path. TCA9555 and MCP23017
  remain latched-output expander planning paths. Relay-driver candidates stay
  candidate-only until relay-module input behavior is measured. Source IDs:
  `SRC-TI-CD74HC4067`, `SRC-TI-TCA9555`,
  `SRC-ESPRESSIF-MCP23017-COMPONENT`, `SRC-TI-TPIC6B595`,
  `SRC-TI-ULN2003A`.
- NIOSH, OSHA, and NEMA sources support a hard mains/load qualified-review
  gate. They do not authorize a public DIY mains wiring procedure. Source IDs:
  `SRC-NIOSH-ELECTRICAL-SAFETY`, `SRC-OSHA-DEENERGIZED-WORK`,
  `SRC-OSHA-GFCI`, `SRC-OSHA-AEGCP`,
  `SRC-OSHA-GROUNDING-OVERCURRENT`, `SRC-OSHA-1910-305`,
  `SRC-NEMA-ENCLOSURES`, `SRC-NEMA-250-ENCLOSURES`.

## Assumptions

- This packet is documentation and public artifact work only.
- Relay contacts remain disconnected or attached only to a reviewed
  low-voltage dummy load during any future prototype proof.
- XBee discovery uses the Waveshare adapter as a PC dock until a separate
  carrier review closes.
- MicroSD, TFT, expander, mux, and relay-driver branches are review branches,
  not approved wiring branches.
- Public diagrams are educational review surfaces. Factual labels, pin names,
  warnings, and gates stay in HTML or Markdown, not in raster artwork.

## Unknowns

- Exact ESP32 board vendor/revision, expansion-shield schematic, regulator,
  jumper state, USB-UART bridge, and shield-to-board GPIO continuity.
- Exact relay module manufacturer/model, trigger polarity, input current,
  3.3 V behavior, `JD-VCC`/`VCC` behavior, and isolation design.
- Exact MicroSD reader, 3.3 V path, pull-ups, card-detect/write-protect
  behavior, card policy, log rotation, and fallback behavior.
- Exact Open-Smart R61509V display identity, pinout, power/backlight, touch
  interface, driver path, and shared pin-budget impact.
- Exact MCP23017 or TCA9555 expander board, I2C address, pullups, inactive
  defaults, output latch behavior, and readback policy.
- Exact CD74HC4067 breakout, select/enable wiring, ADC1 input, voltage
  protection, source impedance, and input-only scan cadence.
- XBee adapter header voltage, DIN/DOUT direction naming, current settings, and
  whether any final ESP32-mounted carrier is selected.
- Final load type, enclosure, overcurrent protection, grounding/bonding,
  strain relief, GFCI/de-energization process, and qualified review outcome.

## Public packet map

| Public surface | Use |
| --- | --- |
| `prototype.html` | Start here for the public packet, evidence map, review sequence, and stop conditions. |
| `blueprints.html` | Visual schematic/review page with conceptual system and safety diagrams. |
| `quality.html` | Artifact, manifest, smoke, host-test, and non-coverage summary. |
| `prototype-blueprint.md` | Source-backed text explanation of the conceptual schematic. |
| `build-guide.md` | Low-voltage review order and checklist wording. |
| `pin-plan.md` | Provisional signal map and pin-pressure gates. |
| `power-and-safety.md` | Power, relay, XBee, expansion, and mains/load stop gates. |
| `hardware-circuit-improvement-research.md` | Research lanes, candidate-only parts, evidence needs, and blockers. |
| `xbee-public-boundary.md` | Public-safe XBee read-only boundary summary. |
| `xbee-read-only-bench-proof.md` | Detailed read-only bench proof plan without setting writes. |

## Provisional signal map

| Function | Provisional signal | Current status |
| --- | --- | --- |
| Output A | `GPIO25` candidate | Blocked until shield continuity and relay input behavior are verified. |
| Output B | `GPIO26` candidate | Blocked until shield continuity and relay input behavior are verified. |
| Output C | `GPIO27` candidate | Blocked until shield continuity and relay input behavior are verified. |
| Output D | `GPIO33` candidate | Blocked until shield continuity and relay input behavior are verified. |
| Relay expander | I2C unassigned | LED or logic-analyzer proof first; no relay input connection. |
| CD74HC4067 mux | ADC1/select pins unassigned | Input-only review branch; no relay output holding. |
| MicroSD | `GPIO18/19/23/32` investigation set | Reader identity, 3.3 V path, pull-ups, and boot risks unresolved. |
| TFT branch | Unassigned | Exact module, bus width, touch, power, and pin pressure unresolved. |
| XBee UART | Unassigned | Final carrier, voltage path, DIN/DOUT direction, and current budget unresolved. |

## Bench review sequence

1. Documentation preflight:
   verify this packet, source index, public artifact policy, known gaps, and
   task record are current.
2. Board/shield power review:
   record one selected power source, jumper position, rail resistance, current
   limit, regulator behavior, boot-pin risks, and shield continuity.
3. Relay verification path:
   keep contacts disconnected, identify module source or markings, measure
   input polarity/current/3.3 V behavior, and record isolation observations.
4. XBee read-only path:
   use PC-side passive discovery first; run fixed AT read queries only with
   the explicit confirmation flag and redaction policy.
5. MicroSD/TFT/expander/mux branches:
   keep each branch in dry proof until exact module identity, voltage, pullups,
   address pins, defaults, conflicts, and input/output boundaries are recorded.
6. Static UI review:
   use the Pages packet and admin HMI demo as review surfaces only.
7. Qualified load review:
   create a separate review package before any load or mains design is added.

## Bench evidence checklist

- Source IDs exist for every new factual hardware, protocol, safety, or public
  artifact claim.
- Board/shield inspection record captures single power source, jumper state,
  rail resistance, 3.3 V/5 V behavior, and candidate GPIO continuity.
- Relay module record captures trigger polarity, input current, 3.3 V
  compatibility, `JD-VCC`/`VCC` behavior, isolation observations, and contact
  disconnection state.
- XBee record captures host serial candidate, adapter inspection, measured
  header voltage, redaction choice, and whether Tier B reads were used.
- MicroSD record captures exact reader, 3.3 V path, pullups, card policy,
  boot/flashing interaction, low-space behavior, and log rotation.
- TFT record captures exact module, pinout, power/backlight, touch interface,
  driver path, and pin-conflict table.
- Expander/mux record captures exact board/breakout, pullups, address/enable
  state, inactive defaults, and LED/logic-analyzer or input-only proof.
- Public bundle audit shows no private uploads, raw photo filenames, local
  device identifiers, unredacted radio identifiers, AES key values, private
  bench notes, vendor PDFs, bulky binaries, or `.agents/` records.

## Stop conditions

- Stop if any step requires relay-contact energization, relay terminal/load
  mapping, mains wiring, or a final wiring diagram.
- Stop if power source, shield jumper, regulator behavior, or rail state is
  ambiguous.
- Stop if a relay input measurement exceeds the source-backed ESP32 voltage or
  current gate.
- Stop if CD74HC4067 is proposed for relay output state holding.
- Stop if expander outputs are connected to relay inputs before relay input
  evidence and driver-stage review close.
- Stop if TFT wiring consumes boot, flash, UART0, relay, XBee, or MicroSD pins
  before the conflict review is recorded.
- Stop if XBee discovery requires setting writes, API transmit frames, relay
  commands, firmware updates, or ESP32 DIN/DOUT carrier wiring.
- Stop if a public artifact exposes private evidence breadcrumbs or treats a
  browser label as a hardware fact.
