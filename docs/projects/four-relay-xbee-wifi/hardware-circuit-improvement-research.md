# Hardware And Circuit Design Improvement Research

## Verified facts

- The current `four-relay-xbee-wifi` target is the photographed
  ESP-WROOM-32-family development board on a black ESP32 I/O expansion shield,
  a blue four-channel relay module with Songle `SRD-05VDC-SL-C` relay cans, a
  Digi `XBP9B-DPUT-001 RevF` radio, and a Waveshare XBee USB Adapter. Source
  IDs: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
  `SRC-SONGLE-SRD-05VDC-SL-C`, `SRC-DIGI-XBP9B-DPUT-001`,
  `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- The expansion shield photo shows `DC6.5-16V`, `USB5V`, `5V`, and `3.3V`
  markings, but the shield schematic, regulator, jumper behavior, dual-power
  behavior, and safe power budget are not verified. Source IDs:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
  `SRC-ESP32-IO-SHIELD-CANDIDATE`.
- Espressif sources are the current authority for ESP32-WROOM-32 module supply,
  GPIO, UART, flash/strapping-pin, SD-card pull-up, and hardware-design review
  constraints. Source IDs: `SRC-ESP32-WROOM-32-DATASHEET`,
  `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`, `SRC-ESP-IDF-GPIO`,
  `SRC-ESP-IDF-UART`, `SRC-ESP-IDF-SD-PULLUP`.
- ESP-IDF documentation states that ESP32 has a built-in brownout detector that
  can reset the system when supply voltage drops below a safe level. Source ID:
  `SRC-ESP-IDF-FATAL-BROWNOUT`.
- ESP-IDF storage and web-serving sources support a future `/sdcard/www` asset
  branch and `/sdcard/logs` event-log branch, but they do not identify the
  exact reader module, card, wiring, or firmware implementation. Source IDs:
  `SRC-ESP-IDF-FATFS`, `SRC-ESP-IDF-SDSPI`, `SRC-ESP-IDF-SDMMC`,
  `SRC-ESP-IDF-SD-PULLUP`, `SRC-ESP-IDF-SDSPI-EXAMPLE`,
  `SRC-ESP-IDF-HTTP-SERVER`, `SRC-ESP-IDF-RESTFUL-SERVER-EXAMPLE`,
  `SRC-SD-ASSOCIATION-FORMATTER`, `SRC-SD-ASSOCIATION-CAPACITY`.
- Digi identifies `XBP9B-DPUT-001` as an XBee-PRO 900HP S3B Point2Multipoint
  900 MHz, 250 mW, U.FL, 10 kbps module, and Digi material lists UART (3V) and
  SPI interfaces for the 900HP family. Source IDs:
  `SRC-DIGI-XBP9B-DPUT-001`, `SRC-DIGI-XBEE-PRO-900HP`.
- The existing XBee path is read-only only: Tier A passive discovery and
  explicitly gated Tier B AT reads for `VR`, `HV`, `SH`, `SL`, `AP`, `AO`,
  `BD`, and `NP`; XBee writes, API transmit frames, relay commands, and ESP32
  carrier wiring are blocked. Source IDs:
  `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`,
  `SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`,
  `SRC-DIGI-XBEE-900HP-NP`, `SRC-DIGI-XBEE-900HP-USER-GUIDE`.
- The Songle relay source supports only relay-component context. It does not
  prove the photographed relay module trigger polarity, input current, 3.3 V
  input behavior, `JD-VCC`/`VCC` jumper behavior, isolation design, or safe load
  wiring. Source ID: `SRC-SONGLE-SRD-05VDC-SL-C`.
- CD74HC4067 is source-backed as a 16:1 analog mux/demux for slow input routing
  only. TCA9555 and MCP23017 are source-backed 16-bit I/O expander paths.
  TPIC6B595 and ULN2003A are source-backed relay-driver candidates, not
  selected project drivers. Source IDs: `SRC-TI-CD74HC4067`,
  `SRC-TI-TCA9555`, `SRC-ESPRESSIF-MCP23017-COMPONENT`,
  `SRC-TI-TPIC6B595`, `SRC-TI-ULN2003A`.
- External R61509V references show parallel TFT pin pressure, but they do not
  verify the user's exact Open-Smart module, pinout, power, touch interface, or
  driver path. Source IDs: `SRC-NOPNOP2002-ESP-IDF-PARALLEL-TFT`,
  `SRC-LCDWIKI-R61509V-MRB2802`.
- LM66100, Littelfuse 16R PolySwitch PPTCs, and Littelfuse SLVU2.8 TVS arrays
  are source-backed protection candidates only. Their ratings do not close the
  project power-entry design because rail voltage, current, placement, and
  surge requirements are not measured. Source IDs: `SRC-TI-LM66100`,
  `SRC-LITTELFUSE-16R-PPTC`, `SRC-LITTELFUSE-SLVU2-8-TVS`.
- Fluke 87V, Keysight E36200-series supplies, and Saleae Logic 8 are
  source-backed examples of bench instrument classes useful for measurement and
  proof. They are candidate examples only, not required purchases. Source IDs:
  `SRC-FLUKE-87V`, `SRC-KEYSIGHT-E36200`, `SRC-SALEAE-LOGIC-8`.
- NIOSH, OSHA, and NEMA sources support a qualified-review gate for load,
  strain-relief, cable-entry, disconnect, and enclosure readiness. They do not
  authorize DIY mains wiring instructions. Source IDs:
  `SRC-NIOSH-ELECTRICAL-SAFETY`, `SRC-OSHA-DEENERGIZED-WORK`,
  `SRC-OSHA-GFCI`, `SRC-OSHA-AEGCP`,
  `SRC-OSHA-GROUNDING-OVERCURRENT`, `SRC-OSHA-1910-305`,
  `SRC-NEMA-ENCLOSURES`, `SRC-NEMA-250-ENCLOSURES`.

## Current blockers

The public [Prototype Build Packet](prototype-build-packet.md) is now the
navigation surface for these blockers. This research document remains the
source-backed hardware/circuit evidence package; no blocker below was closed
by the public-site packet work.

- Board/shield identity is not closed: vendor, revision, schematic, regulator,
  USB-UART bridge, jumper position, single-source power path, and GPIO
  continuity remain unresolved.
- Relay module identity is not closed: board manufacturer/model, trigger
  polarity, input current, 3.3 V compatibility, `JD-VCC`/`VCC` behavior,
  isolation design, coil current, and load rating remain unresolved.
- Load design is not closed: load type, voltage/current, fusing, snubber or
  surge handling, enclosure, separation, grounding/bonding, strain relief,
  labeling, disconnect, and qualified review remain unresolved.
- XBee carrier design is not closed: the Waveshare adapter remains a PC dock
  candidate only, and final ESP32 DIN/DOUT routing, voltage, current budget,
  flow control, reset/sleep pins, and antenna clearance remain unresolved.
- Storage design is not closed: exact MicroSD reader, 3.3 V path, pull-ups,
  card-detect/write-protect behavior, card prep, low-space policy, and
  retention policy remain unresolved.
- TFT and expansion design is not closed: exact R61509V module, bus width,
  power/backlight, touch interface, pin conflicts, expander board, pullups,
  inactive defaults, output latch behavior, mux input protection, and driver
  stage remain unresolved.

### Assumptions

- This package is documentation and research only; it does not add firmware
  source, framework project files, relay wiring, load wiring, XBee writes, or a
  final schematic.
- Relay contacts stay disconnected or attached only to a reviewed low-voltage
  dummy load during any future prototype proof.
- The existing project-scoped ESP-IDF target from ADR-0002 remains unchanged;
  this package does not change framework scope.
- The Waveshare XBee USB Adapter remains a PC-side discovery dock until a
  separate carrier review closes.
- MicroSD remains the planned asset and log store, while NVS remains the
  planned store for safety-critical credentials, relay polarity, and XBee
  allowlists.

### Unknowns

- Whether the photographed expansion shield can safely power the ESP32 board,
  relay module, XBee, MicroSD reader, TFT branch, and expansion branch from one
  selected source.
- Whether the relay module input circuit can be driven directly from ESP32
  GPIO or requires a separate driver stage.
- Whether the final relay driver stage should be a low-side array, power shift
  register, transistor/MOSFET stage, opto-isolated stage, or remain blocked by
  relay-module evidence.
- Whether the R61509V TFT branch can coexist with MicroSD, XBee UART, relay
  expansion, mux inputs, UART0, flash pins, and boot strapping.
- Whether any final enclosure/load design can satisfy the mains-readiness gate.

### Risks

- Dual-power or regulator ambiguity can damage the ESP32 board, shield,
  reader, XBee, relay module, or PC USB port.
- Relay input misidentification can create boot-time relay actuation, stuck-on
  outputs, over-current GPIO loading, or defeated isolation.
- Treating relay-can markings as relay-module proof can produce incorrect load,
  input, and isolation claims.
- XBee setting writes before readback and rollback evidence can lose the
  current radio state.
- Adding protection parts without measured rail/current/surge requirements can
  create false confidence or brownout under load.
- Publishing raw bench notes, serial addresses, photos, or vendor PDFs would
  violate the current repository and Pages boundaries.

### Required next evidence

- Photos or exact purchase/source links for the ESP32 dev board, expansion
  shield, relay module, MicroSD reader, R61509V display, expander board, mux
  breakout, and any XBee carrier candidate.
- Power-off continuity records for shield labels and candidate pins, with the
  ESP32 unpowered and external modules disconnected.
- Power-on rail records with one selected power source, current limit, jumper
  position, regulator output, idle current, and brownout observations.
- Relay-module bench records with contacts disconnected: input polarity, input
  current, 3.3 V behavior, `JD-VCC`/`VCC` behavior, and isolation observations.
- XBee Tier A record and optional Tier B read-only record using the existing
  allowlisted probe.
- MicroSD reader/card record: exact model, pull-ups, 3.3 V behavior, card
  format, host preparation, low-space/log-rotation policy, and fallback
  behavior.
- Enclosure/load review package by a qualified person before any load wiring
  design is attempted.

## Recommended research lanes

| Lane | Verified basis | Unknowns and risks | Required next evidence | Source-index update requirements |
| --- | --- | --- | --- | --- |
| Power/protection | ESP32 module and hardware-design sources; photo labels; brownout source; protection candidate sources. | Shield regulator and dual-power behavior, rail budget, XBee transmit current, MicroSD/TFT current, relay coil current, fuse/PTC/TVS/reverse-protection ratings. | Board/shield identity, jumper state, one selected input source, current-limited rail measurements, idle and worst-case current estimates, brownout notes, protection placement requirements. | Add exact shield/regulator/protection sources only after parts are identified. Keep `SRC-TI-LM66100`, `SRC-LITTELFUSE-16R-PPTC`, and `SRC-LITTELFUSE-SLVU2-8-TVS` candidate-only until ratings close. |
| Relay/load interface | Photo ledger, Songle relay-component source, Espressif GPIO/hardware sources, TCA9555/MCP23017/TPIC6B595/ULN2003A sources. | Exact module input behavior, isolation, relay coil current, load type, driver-stage topology, boot defaults. | Exact module source or inspection record, contacts-disconnected measurements, LED or logic-analyzer driver proof, dummy-load definition, owner review. | Add exact relay module product/schematic source or mark unresolved; add selected driver source only after relay evidence closes. |
| I/O expansion/TFT | R61509V planning refs, GPIO matrix/strapping sources, TCA9555/MCP23017 and CD74HC4067 sources. | TFT pin pressure, bus width, backlight/touch current, I2C pullups, mux input protection, ADC1/ADC2 and Wi-Fi interactions, pin conflicts. | Exact TFT module source, exact expander/mux breakout source, pin-conflict matrix, I2C address proof, inactive default proof, mux input voltage/protection proof. | Add exact Open-Smart/R61509V module source and exact breakout/expander board sources; keep current references as candidates. |
| XBee/comms hardware | Digi exact model and 900HP docs, Waveshare adapter source, local read-only probe baseline. | Adapter voltage, DIN/DOUT label direction, final ESP32 carrier, reset/sleep/CTS/RTS use, antenna clearance, current budget, regulatory deployment context. | Tier A serial/inspection/voltage record, optional Tier B read-only query record, carrier candidate source, antenna/mechanical review. | Add final carrier/socket/antenna source only after selection; do not add XBee write procedure sources until a new request authorizes writes. |
| Storage/serviceability | ESP-IDF FatFS/SDSPI/SDMMC/pull-up/example sources, SD Association sources, and existing MicroSD HMI plan. | Exact reader, 3.3 V and level shifting, pullups, card detect/write protect, host prep, auto-format policy, log rotation, retention, backup/export. | Reader photo/source, card capacity/filesystem record, boot/flashing check with reader connected, low-space/log-retention decision, config backup/export plan. | Add exact reader and card source if selected; keep firmware implementation deferred. |
| Bench equipment/fixtures | Existing runbook plus DMM, bench supply, and logic analyzer candidate sources. | What instruments are already available, current-limit range, logic threshold support, harness quality, dummy-load ratings, label scheme, test-record format. | Inventory available instruments, calibration/safety status if applicable, current-limit setting records, labeled harness plan, dummy-load rating evidence, bench record template. | Add exact instrument/tool sources only for tools actually used; otherwise keep candidate examples. |
| Safety/enclosure readiness | NIOSH, OSHA, NEMA, mains-readiness gate, and current project safety docs. | Enclosure type, separation, strain relief, grounding/bonding, overcurrent protection, qualified reviewer, applicable code path, final load. | Qualified-review package before load design, enclosure source, load definition, protection/disconnect labels, test-record plan. | Add exact enclosure, strain relief, fuse/overcurrent, and qualified-review sources only after load scope is defined. |

## Additional components and instruments needed

### must buy

- If not already available, a digital multimeter suitable for voltage,
  resistance, continuity, and current checks. `SRC-FLUKE-87V` is a
  source-backed example only.
- If not already available, a current-limited low-voltage bench supply or
  equivalent current-limited power path for board/shield and module proof.
  `SRC-KEYSIGHT-E36200` is a source-backed example only.
- If not already available, an LED proof fixture or logic analyzer for expander
  output proof before any relay-module input connection. `SRC-SALEAE-LOGIC-8`
  is a source-backed example only.
- Low-voltage dummy loads for relay-contact proof after the load is defined;
  exact resistor/load values and power ratings are pending source-index entry.
- Labeled low-voltage breakout harnesses, Dupont leads, terminal blocks, and
  insulation/strain-relief materials for bench organization; exact parts are
  pending source-index entry.

### must identify

- Exact ESP32 development board vendor/revision, USB-UART bridge, regulator,
  boot/reset circuit, and expansion-shield schematic or source.
- Exact four-channel relay module manufacturer/model, schematic/product page,
  input stage, `JD-VCC`/`VCC` behavior, and isolation boundary.
- Exact MicroSD reader, R61509V TFT module, MCP23017/TCA9555 expander board,
  CD74HC4067 breakout, and any final XBee carrier/socket board.
- Intended load class for qualified review: low-voltage DC, low-voltage AC,
  mains AC, inductive, capacitive, motor, heater, lighting, or unknown.

### must measure

- Board/shield rail resistance before power, selected power-source voltage,
  3.3 V and 5 V rail behavior, idle current, and brownout/reset observations.
- Shield continuity from visible labels to actual ESP32 pins for relay,
  MicroSD, I2C, mux, TFT, and UART candidates.
- Relay input polarity, per-channel input current, 3.3 V behavior, coil supply
  current, and `JD-VCC`/`VCC` behavior with contacts disconnected.
- Waveshare adapter header voltage and serial-path behavior while disconnected
  from ESP32 GPIO.
- MicroSD reader/card current, pull-up presence or source evidence, and boot
  behavior with the reader connected but relay and XBee carrier paths still
  disconnected.

### candidate only

- `LM66100` for low-voltage ideal-diode/reverse-polarity investigation only;
  it is not a candidate for the shield `DC6.5-16V` input because that input is
  outside the source-backed LM66100 operating range. Source ID:
  `SRC-TI-LM66100`.
- Littelfuse `16R` PolySwitch resettable PPTC family for low-voltage
  overcurrent investigation after rail current is measured. Source ID:
  `SRC-LITTELFUSE-16R-PPTC`.
- Littelfuse `SLVU2.8` TVS array for low-voltage line/transient protection
  investigation only; exact working voltage and capacitance must match the
  protected line. Source ID: `SRC-LITTELFUSE-SLVU2-8-TVS`.
- `TCA9555` or `MCP23017` for relay-state expansion after I2C, pullup, default
  state, and latch proof. Source IDs: `SRC-TI-TCA9555`,
  `SRC-ESPRESSIF-MCP23017-COMPONENT`.
- `TPIC6B595` or `ULN2003A` as driver-stage references after relay input
  behavior is known. Source IDs: `SRC-TI-TPIC6B595`, `SRC-TI-ULN2003A`.
- Fluke 87V, Keysight E36200-series supply, and Saleae Logic 8 as example
  instrument classes. Source IDs: `SRC-FLUKE-87V`, `SRC-KEYSIGHT-E36200`,
  `SRC-SALEAE-LOGIC-8`.

### blocked

- Relay/load wiring, mains wiring design, and any public wiring procedure for
  relay contacts.
- XBee configuration writes, `WR`, `AC`, API transmit frames, relay commands,
  firmware updates, factory reset, and unredacted public radio identifiers.
- ESP32 DIN/DOUT carrier wiring before final carrier voltage, direction,
  current, reset/sleep, flow-control, and antenna evidence exists.
- Final wiring diagrams, PCB schematics, pin maps, or firmware source that
  imply closed hardware gates.

## Circuit design improvement candidates

- Power entry/protection: require a single selected input source, measured
  current budget, reset/brownout observation, fuse or PPTC selection, TVS or ESD
  placement decision, reverse-protection decision, test points, and a no
  dual-power rule before any final power diagram. Candidate sources:
  `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`, `SRC-ESP-IDF-FATAL-BROWNOUT`,
  `SRC-TI-LM66100`, `SRC-LITTELFUSE-16R-PPTC`,
  `SRC-LITTELFUSE-SLVU2-8-TVS`.
- Relay driver stage: require measured relay input polarity/current/logic
  behavior and isolation behavior before selecting direct GPIO, expander plus
  driver, low-side driver, power shift register, discrete transistor, or an
  isolated stage. Candidate sources: `SRC-SONGLE-SRD-05VDC-SL-C`,
  `SRC-TI-TPIC6B595`, `SRC-TI-ULN2003A`.
- I2C expander branch: require exact expander board source, address pins,
  pullup voltage, boot default state, output latch proof, readback/fault
  behavior, and no relay connection during first proof. Candidate sources:
  `SRC-TI-TCA9555`, `SRC-ESPRESSIF-MCP23017-COMPONENT`.
- Input mux protection: keep CD74HC4067 input-only; require exact breakout,
  enable/default behavior, ADC1 route, source impedance, input clamp or series
  protection decision, and proof that mux scans cannot change relay state.
  Source ID: `SRC-TI-CD74HC4067`.
- XBee carrier: require a final carrier/socket source, 3.3 V current budget,
  DIN/DOUT direction proof, optional CTS/RTS/reset/sleep decisions, antenna
  clearance, and read-only settings backup before any write procedure. Source
  IDs: `SRC-DIGI-XBP9B-DPUT-001`, `SRC-DIGI-XBEE-PRO-900HP`,
  `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- MicroSD protection/serviceability: require exact reader/card source,
  3.3 V-only behavior or level-shifter evidence, pull-up evidence, removable
  card policy, host-prepared filesystem, log-rotation and low-space policy,
  and config export/backup plan. Source IDs: `SRC-ESP-IDF-FATFS`,
  `SRC-ESP-IDF-SDSPI`, `SRC-ESP-IDF-SD-PULLUP`,
  `SRC-SD-ASSOCIATION-FORMATTER`, `SRC-SD-ASSOCIATION-CAPACITY`.
- Enclosure/test fixture: require low-voltage-only bench fixture labels,
  separation from relay contacts, strain relief, disconnect labels, qualified
  load review, and test records before any final enclosure or load design.
  Source IDs: `SRC-NIOSH-ELECTRICAL-SAFETY`,
  `SRC-OSHA-DEENERGIZED-WORK`, `SRC-OSHA-GFCI`, `SRC-OSHA-AEGCP`,
  `SRC-OSHA-GROUNDING-OVERCURRENT`, `SRC-OSHA-1910-305`,
  `SRC-NEMA-ENCLOSURES`, `SRC-NEMA-250-ENCLOSURES`.

## Bench validation sequence

1. Documentation preflight: confirm this package, the source ledger,
   `research/known-gaps.md`, the task log, and the handoff are present. Confirm
   every cited `SRC-*` exists in `knowledge-base/source-index.md`.
2. Equipment inventory: record available DMM, current-limited supply, logic
   analyzer or LED fixture, USB serial tooling, dummy loads, labels, and bench
   record template. Do not substitute unsourced wiring claims for missing
   instruments.
3. Power-off board/shield inspection: disconnect relay module, XBee carrier,
   MicroSD reader, TFT, and expander hardware. Record photos, jumper state,
   rail resistance, and shield label continuity.
4. Current-limited board/shield power proof: power from one selected source
   only. Record current limit, 3.3 V/5 V rails, idle current, boot state, heat,
   and brownout messages. Stop on dual-power ambiguity, unstable rails, heat,
   or unexpected boot mode.
5. Relay module proof, contacts disconnected: identify supply pins, jumper
   state, input polarity, per-input current, 3.3 V behavior, coil current, and
   isolation observations. Stop on unclear supply, unexpected actuation,
   over-current input behavior, heat, or any load/mains connection.
6. Expansion dry proof: prove MCP23017/TCA9555 outputs on LEDs or logic
   analyzer only; prove CD74HC4067 only on reviewed low-voltage inputs. Confirm
   unrelated mux/TFT/storage/XBee activity cannot glitch relay-state outputs.
7. XBee read-only proof: run Tier A first, then Tier B only with
   `--confirm-sends-read-commands`. Keep addresses redacted unless the record
   is local-only. Stop before any setting write or ESP32 carrier wiring.
8. MicroSD serviceability proof: identify the reader/card, confirm pull-ups and
   3.3 V behavior, test boot/flashing impact, and record host-prepared
   filesystem, low-space, log-rotation, and fallback policies. Do not
   auto-format normal runtime media.
9. Enclosure/load review gate: collect load definition and qualified review
   evidence before any load wiring design. No mains wiring procedure is part of
   this sequence.

## Required documentation updates

- Add exact source-index entries for any newly identified board, shield, relay
  module, MicroSD reader, TFT, expander, mux, XBee carrier, enclosure,
  protection part, or bench instrument actually used.
- Update the relevant hardware profile only after exact evidence exists:
  ESP32 board/shield, relay module, XBee carrier, MicroSD reader, display, mux,
  expander, and any protection/fixture profiles.
- Update `power-and-safety.md`, `pin-plan.md`, `bench-bring-up-runbook.md`,
  and `tft-relay-expansion.md` only when the evidence closes a current blocker.
- Store local bench records under a deliberate `research/bench-records/`
  subtree and keep private notes, raw photos, unredacted radio addresses, and
  bulky artifacts out of the public Pages artifact.
- Keep `research/known-gaps.md` open for every item not closed by a source,
  inspection record, ADR, or test artifact.
- Create a new task and handoff whenever the next role must continue hardware,
  communications, QA, or safety review work.

## Open questions for the user

- Which bench instruments are already available: DMM, current-limited supply,
  logic analyzer, USB serial tools, dummy loads, and labeled harness materials?
- Can you provide exact purchase links, underside photos, or model markings for
  the ESP32 shield, relay module, MicroSD reader, R61509V TFT, expander board,
  mux breakout, and any XBee carrier candidate?
- What load class is eventually intended? A general class is enough for gating;
  this package still does not produce mains wiring steps.
- Should the first relay proof use disconnected contacts only, or a specific
  low-voltage dummy load after its ratings are sourced?
- Should the project buy a known-good XBee carrier board instead of trying to
  repurpose the Waveshare PC adapter?
- What MicroSD card capacity and retention target should the logging plan use?
