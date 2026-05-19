# Source Ledger - 2026-05-19 Four Relay Hardware Circuit Improvement

## Scope

Source-backed research package for improving the `four-relay-xbee-wifi`
hardware and circuit design without approving relay/load wiring, mains wiring,
XBee setting writes, ESP32 carrier wiring, final pin maps, final schematics, or
firmware source.

## Verified facts

- The active target remains the photographed ESP-WROOM-32-family development
  board, ESP32 I/O expansion shield, four-channel relay module with Songle
  `SRD-05VDC-SL-C` relay cans, Digi `XBP9B-DPUT-001 RevF`, and Waveshare XBee
  USB Adapter. Source IDs: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
  `SRC-SONGLE-SRD-05VDC-SL-C`, `SRC-DIGI-XBP9B-DPUT-001`,
  `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- Espressif sources remain the authority for ESP32 module, GPIO, UART,
  strapping, SD-card pull-up, hardware-design, and brownout review. Source IDs:
  `SRC-ESP32-WROOM-32-DATASHEET`,
  `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`, `SRC-ESP-IDF-GPIO`,
  `SRC-ESP-IDF-UART`, `SRC-ESP-IDF-SD-PULLUP`,
  `SRC-ESP-IDF-FATAL-BROWNOUT`.
- ESP-IDF storage and HTTP sources, plus SD Association card-preparation
  sources, support the future MicroSD asset/log branch but do not close exact
  reader, card, wiring, or firmware evidence. Source IDs:
  `SRC-ESP-IDF-FATFS`, `SRC-ESP-IDF-SDSPI`, `SRC-ESP-IDF-SDMMC`,
  `SRC-ESP-IDF-SDSPI-EXAMPLE`, `SRC-ESP-IDF-HTTP-SERVER`,
  `SRC-ESP-IDF-RESTFUL-SERVER-EXAMPLE`, `SRC-SD-ASSOCIATION-FORMATTER`,
  `SRC-SD-ASSOCIATION-CAPACITY`.
- The XBee path remains read-only discovery only until separate review
  authorizes any write, transmit, relay command, or ESP32 carrier wiring.
  Source IDs: `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`,
  `SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`,
  `SRC-DIGI-XBEE-900HP-NP`, `SRC-DIGI-XBEE-900HP-USER-GUIDE`.
- CD74HC4067 remains input-only; TCA9555/MCP23017 remain latched expansion
  candidates; TPIC6B595/ULN2003A remain driver-stage candidates until relay
  input evidence closes. Source IDs: `SRC-TI-CD74HC4067`,
  `SRC-TI-TCA9555`, `SRC-ESPRESSIF-MCP23017-COMPONENT`,
  `SRC-TI-TPIC6B595`, `SRC-TI-ULN2003A`.
- LM66100, Littelfuse 16R PolySwitch PPTCs, and Littelfuse SLVU2.8 TVS arrays
  are candidate protection sources only. They do not select a project
  protection circuit. Source IDs: `SRC-TI-LM66100`,
  `SRC-LITTELFUSE-16R-PPTC`, `SRC-LITTELFUSE-SLVU2-8-TVS`.
- Fluke 87V, Keysight E36200-series supplies, and Saleae Logic 8 are candidate
  bench instrument examples only. Source IDs: `SRC-FLUKE-87V`,
  `SRC-KEYSIGHT-E36200`, `SRC-SALEAE-LOGIC-8`.
- NIOSH, OSHA, and NEMA sources keep load/enclosure work at a qualified-review
  gate. Source IDs: `SRC-NIOSH-ELECTRICAL-SAFETY`,
  `SRC-OSHA-DEENERGIZED-WORK`, `SRC-OSHA-GFCI`, `SRC-OSHA-AEGCP`,
  `SRC-OSHA-GROUNDING-OVERCURRENT`, `SRC-OSHA-1910-305`,
  `SRC-NEMA-ENCLOSURES`, `SRC-NEMA-250-ENCLOSURES`.

## Assumptions

- Deliverable mode is a repo documentation package.
- Component candidates remain requirements-level until exact board/module
  evidence and measured rail/load data exist.
- The existing project-scoped ADR-0002 framework target is not changed by this
  research package.
- The public bundle may include the research doc and source ledger because they
  contain source links and gate language, not private bench records or raw
  uploads.

## Unresolved gaps

- Exact ESP32 board/shield identity, regulator, jumper state, current budget,
  and continuity matrix.
- Exact relay module source and measured input behavior.
- Exact protection components and ratings for the selected input rail and
  low-voltage signal lines.
- Exact MicroSD reader/card, filesystem, low-space, and log-retention policy.
- Exact TFT, mux, expander, and driver-stage boards.
- Exact XBee carrier, antenna clearance, and read-only settings record.
- Exact bench instruments and dummy-load ratings.
- Qualified load and enclosure review package.

## Source-index additions

- Added `SRC-ESP-IDF-FATAL-BROWNOUT` for brownout detector context.
- Added `SRC-SD-ASSOCIATION-FORMATTER` and `SRC-SD-ASSOCIATION-CAPACITY` for
  SD card preparation and capacity-class context.
- Added `SRC-TI-LM66100`, `SRC-LITTELFUSE-16R-PPTC`, and
  `SRC-LITTELFUSE-SLVU2-8-TVS` as candidate protection sources.
- Added `SRC-TI-ULN2003A` as a candidate relay-driver source.
- Added `SRC-FLUKE-87V`, `SRC-KEYSIGHT-E36200`, and `SRC-SALEAE-LOGIC-8` as
  candidate instrument sources.
- Added `SRC-OSHA-1910-305` and `SRC-NEMA-250-ENCLOSURES` for strain-relief,
  cable-entry, disconnect, and enclosure-readiness context.

## Blocked actions

- No relay/load wiring.
- No mains wiring design or procedure.
- No XBee setting writes, `WR`, `AC`, firmware update, reset, API transmit
  frame, or relay command.
- No ESP32 DIN/DOUT carrier wiring.
- No final wiring diagram, final schematic, PCB design, or firmware source.
- No vendor PDFs, raw photos, private bench notes, or bench records in public
  Pages artifacts.
