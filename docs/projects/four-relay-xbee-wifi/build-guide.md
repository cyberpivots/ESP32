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

## Parts layout

| Area | Current role | Evidence boundary |
| --- | --- | --- |
| ESP32 board plus expansion shield | Low-voltage controller target | Visible photo evidence and Espressif module/GPIO sources; exact carrier board still unresolved. |
| Four-channel relay module | Relay-input verification target | Relay contacts stay disconnected; module input behavior remains unresolved. |
| XBee-PRO 900HP radio | Read-only discovery target | Digi model identity is source-backed; ESP32 carrier wiring is unresolved. |
| Waveshare XBee USB Adapter | PC-side radio dock | Source-backed as a USB/XBee UART adapter; not approved as final ESP32 carrier. |
| Browser/admin HMI | Static review surface | Local UI only until firmware and hardware gates are accepted. |

## Provisional signal map

| UI label | Provisional signal | Gate |
| --- | --- | --- |
| Output A | GPIO25 | Shield routing plus relay trigger voltage/current/polarity and isolation verification. |
| Output B | GPIO26 | Shield routing plus relay trigger voltage/current/polarity and isolation verification. |
| Output C | GPIO27 | Shield routing plus relay trigger voltage/current/polarity and isolation verification. |
| Output D | GPIO33 | Shield routing plus relay trigger voltage/current/polarity and isolation verification. |

The public site lets a reviewer rename the labels in browser storage. Those
labels are not hardware facts and must not be used as wiring evidence.

## Low-voltage construction order

1. Board and shield inspection:
   Record the selected single power source, jumper state, visible labels, rail
   resistance checks, and shield continuity for `GPIO25`, `GPIO26`, `GPIO27`,
   and `GPIO33`. Stop on shorts, dual-power ambiguity, unstable rails, heat, or
   unexpected boot behavior.
2. Relay module inspection with contacts disconnected:
   Record input labels, jumper state, visible isolation components, and
   continuity observations. Do not connect any load while identifying trigger
   polarity, input current, 3.3 V behavior, and `JD-VCC`/`VCC` behavior.
3. XBee read-only discovery:
   Use the Waveshare adapter as a PC dock only. Record serial identity and
   read-only radio identity before any setting write is considered.
4. Static UI review:
   Review the GitHub Pages site and admin HMI demo for labels, safety locks,
   storage panels, XBee status, and log display. This does not approve relay
   switching or hardware mutation.
5. Qualified load review:
   Prepare only a review package for load or mains work. Do not add a
   relay-terminal wiring procedure to this public guide.

## Verification checklist

- Source index contains every source ID cited by this guide.
- Build artifact includes this guide and the generated manifest records it.
- Public links resolve for the build guide, pin plan, power gates, mains gate,
  source index, and admin HMI demo.
- Relay labels render from checked-in defaults, can be changed in browser
  storage, persist across reload, and reset to defaults.
- Admin HMI static mode makes no `/api/` requests on GitHub Pages.
- No vendor PDFs, raw photo archives, generated screenshots, bulky binaries,
  private bench notes, or `.agents/` records are published in the Pages
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
