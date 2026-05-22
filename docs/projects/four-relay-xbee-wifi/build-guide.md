# Four Relay Build Guide

## Verified facts

- The project target is the photographed ESP-WROOM-32-family development board
  on an ESP32 I/O expansion shield, a blue four-channel relay module with
  Songle `SRD-05VDC-SL-C` relay cans, a Digi `XBP9B-DPUT-001 RevF` radio, and
  a Waveshare XBee USB Adapter. Source IDs:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
  `SRC-SONGLE-SRD-05VDC-SL-C`, `SRC-DIGI-XBP9B-DPUT-001`,
  `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- The photographed expansion shield exposes visible labels for `GPIO25`,
  `GPIO26`, `GPIO27`, and `GPIO33`; these are provisional relay-output
  candidates only. Source ID: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Espressif ESP32 GPIO and hardware-design sources are the review sources for
  GPIO, strapping-pin, flash-pin, UART, reset, and 3.3 V supply constraints.
  Source IDs: `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-UART`,
  `SRC-ESP32-WROOM-32-DATASHEET`,
  `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.
- The relay can datasheet source gives component-level context only; it does
  not verify the photographed relay module input circuit, trigger polarity,
  input current, jumper behavior, or isolation boundary. Source ID:
  `SRC-SONGLE-SRD-05VDC-SL-C`.
- NIOSH, OSHA, and NEMA sources support the qualified-review gate for
  hazardous-voltage work; they do not authorize a DIY mains wiring procedure.
  Source IDs: `SRC-NIOSH-ELECTRICAL-SAFETY`,
  `SRC-OSHA-DEENERGIZED-WORK`, `SRC-OSHA-GFCI`, `SRC-OSHA-AEGCP`,
  `SRC-OSHA-GROUNDING-OVERCURRENT`, `SRC-NEMA-ENCLOSURES`.
- CD74HC4067 is an analog mux/demux planning source for slow input routing, not
  relay state holding. Source ID: `SRC-TI-CD74HC4067`.
- TCA9555 and MCP23017 are planning sources for a latched relay-expander branch.
  Source IDs: `SRC-TI-TCA9555`, `SRC-ESPRESSIF-MCP23017-COMPONENT`.
- TPIC6B595 is a relay-driver reference only until the exact relay module input
  behavior is verified. Source ID: `SRC-TI-TPIC6B595`.

## Assumptions

- Relay labels such as `Output A` through `Output D` are UI aliases only and do
  not prove wiring, load identity, or channel function.
- The public build path is limited to documentation, static UI review,
  low-voltage inspection, and relay-input verification with relay contacts
  disconnected.
- XBee work starts with read-only PC-side discovery through the Waveshare USB
  adapter.
- Any final load wiring requires a separate source-backed design package and
  qualified review.
- The Open-Smart R61509V TFT remains a planning target, so relay GPIO relief
  should prefer the expander branch over direct GPIO.

## Unknowns

- Exact ESP32 board vendor, shield revision, regulator capacity, jumper state,
  active power source, and shield-to-board routing.
- Exact relay module manufacturer, input trigger polarity, input current,
  3.3 V compatibility, `JD-VCC`/`VCC` behavior, and isolation design.
- Final XBee carrier, ESP32 DIN/DOUT routing, flow-control needs, reset/sleep
  handling, and power budget.
- Load type, load voltage/current, enclosure, overcurrent protection,
  grounding/bonding, strain relief, GFCI/de-energization process, and qualified
  review outcome.
- Exact TFT module, expander board, mux breakout, I2C bus, ADC pins, and
  driver-stage choice.

## Parts layout

Start public review from [Prototype Build Packet](prototype-build-packet.md).
This build guide is the low-voltage review order inside that packet, not a
final construction or load-wiring procedure.

| Area | Current role | Evidence boundary |
| --- | --- | --- |
| ESP32 board plus expansion shield | Low-voltage controller target | Visible photo evidence and Espressif module/GPIO sources; exact carrier board still unresolved. |
| Four-channel relay module | Relay-input verification target | Relay contacts stay disconnected; module input behavior remains unresolved. |
| XBee-PRO 900HP radio | Read-only discovery target | Digi model identity is source-backed; ESP32 carrier wiring is unresolved. |
| Waveshare XBee USB Adapter | PC-side radio dock | Source-backed as a USB/XBee UART adapter; not approved as final ESP32 carrier. |
| Browser/admin HMI | Static review surface | Local UI only until firmware and hardware gates are accepted. |
| Open-Smart R61509V TFT | Future local display/touch surface | Exact module and pin plan are unverified; relay changes remain UI intents only. |
| CD74HC4067 mux | Slow input expansion candidate | Input-only; rejected for direct relay state holding. |
| MCP23017/TCA9555 expander | Relay output state mirror candidate | LED/logic-analyzer proof first; relay inputs remain blocked. |

## Provisional signal map

| UI label | Provisional signal | Gate |
| --- | --- | --- |
| Output A | GPIO25 | Shield routing plus relay trigger voltage/current/polarity and isolation verification. |
| Output B | GPIO26 | Shield routing plus relay trigger voltage/current/polarity and isolation verification. |
| Output C | GPIO27 | Shield routing plus relay trigger voltage/current/polarity and isolation verification. |
| Output D | GPIO33 | Shield routing plus relay trigger voltage/current/polarity and isolation verification. |
| Relay expander | I2C unassigned | Exact expander board, pullups, address pins, inactive defaults, latch behavior, and driver-stage evidence. |
| Mux scan | ADC1 and select pins unassigned | Input-only proof for touch/buttons/sensors; no relay outputs. |
| TFT bus | Unassigned | Exact Open-Smart module, bus width, control pins, power/backlight, and conflict review. |

The public site lets a reviewer rename the labels in browser storage. Those
labels are not hardware facts and must not be used as wiring evidence.

## Low-voltage construction order

1. Visual blueprint review:
   Open the public `blueprints.html` page or
   `prototype-blueprint.md` text version first. Treat the system overview and
   safety proof ladder as conceptual review maps only; they are not wiring
   instructions.
2. Board and shield inspection:
   Record the selected single power source, jumper state, visible labels, rail
   resistance checks, and shield continuity for `GPIO25`, `GPIO26`, `GPIO27`,
   and `GPIO33`. Stop on shorts, dual-power ambiguity, unstable rails, heat, or
   unexpected boot behavior.
3. Relay module inspection with contacts disconnected:
   Record input labels, jumper state, visible isolation components, and
   continuity observations. Do not connect any load while identifying trigger
   polarity, input current, 3.3 V behavior, and `JD-VCC`/`VCC` behavior.
4. XBee read-only discovery:
   Use the Waveshare adapter as a PC dock only. Record serial identity and
   read-only radio identity before any setting write is considered.
5. Expansion dry proof:
   Verify CD74HC4067 only with ADC1 test voltages, and verify the selected
   MCP23017/TCA9555 expander only on LEDs or a logic analyzer. Do not connect
   relay-module inputs or coils.
6. Static UI review:
   Review the GitHub Pages site and admin HMI demo for labels, safety locks,
   storage panels, XBee status, and log display. This does not approve relay
   switching or hardware mutation.
7. Qualified load review:
   Prepare only a review package for load or mains work. Do not add a
   relay-terminal wiring procedure to this public guide.

## Verification checklist

- Prototype packet page and Markdown link to the visual blueprint, quality
  evidence, public-safe XBee boundary, source index, known gaps, and stop
  conditions.
- Source index contains every source ID cited by this guide.
- Build artifact includes this guide and the generated manifest records it.
- Public links resolve for the visual blueprint page, build guide, pin plan,
  power gates, mains gate, source index, and admin HMI demo.
- Public blueprint panels say relay/load wiring, mains wiring, TFT wiring, and
  expander-to-relay wiring remain blocked until the documented gates close.
- Relay labels render from checked-in defaults, can be changed in browser
  storage, persist across reload, and reset to defaults.
- Admin HMI state rendering includes `relayExpander.present`,
  `relayExpander.ready`, `relayExpander.lastWrite`, and `mux.ready`.
- Admin HMI static mode makes no `/api/` requests on GitHub Pages.
- No vendor PDFs, raw photo archives, generated screenshots, bulky binaries,
  private bench records, or `.agents/` records are published in the Pages
  artifact.

## Stop conditions

- Stop if any step requires mains wiring, relay-contact energization, or
  line/load terminal mapping.
- Stop if a relay input measurement suggests the ESP32 GPIO current or voltage
  gate is not satisfied.
- Stop if power-source selection, jumper position, or board/shield routing is
  ambiguous.
- Stop if an XBee tool requires setting writes before read-only identity is
  captured.
- Stop if a label change is treated as evidence that a relay output has been
  wired or qualified.
- Stop if CD74HC4067 is proposed as direct relay output state holding.
- Stop if expander outputs are connected to relay-module inputs before the
  relay input and driver-stage evidence exists.
