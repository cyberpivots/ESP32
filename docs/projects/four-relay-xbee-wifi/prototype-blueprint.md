# Prototype Blueprint

## What this does in plain English

This blueprint explains the ESP32 four-relay workbench as a review map. The
ESP32 is the planned low-voltage controller, the browser HMI is the public
review surface, MicroSD is the planned asset/log storage branch, XBee discovery
starts read-only, and the relay side stays behind safety gates.

The visual GitHub Pages blueprint uses generated label-free backplates with
HTML labels so the public page can stay readable without turning the image into
unverified wiring evidence.

For the complete public review path, start with
[Prototype Build Packet](prototype-build-packet.md). It links the visual
schematics to the low-voltage review sequence, pin-pressure map, XBee
read-only boundary, MicroSD/TFT/expander/mux branches, evidence checklist, and
stop conditions.

## What each box means

| Box | Plain meaning | Evidence boundary |
| --- | --- | --- |
| ESP32 controller | The low-voltage board being reviewed as the center of the prototype. | Source-backed at module/GPIO level; carrier/shield routing is still unresolved. |
| Browser HMI | A static control-surface preview for labels, locks, and status display. | It is a review interface, not live hardware control. |
| XBee 900HP | The Digi radio identified by the project source set. | Read-only discovery comes before any setting writes or ESP32 carrier wiring. |
| MicroSD | Planned storage for assets and logs. | Bus and pin choices remain part of the low-voltage review. |
| TFT branch | Planned local display/touch surface. | Exact module identity, power, pinout, and firmware path are unresolved. |
| Mux branch | Candidate input expansion path. | Input-only; rejected for relay output state holding. |
| Relay expander | Candidate latched output branch for relay-state relief. | Must be proven on LEDs or a logic analyzer before relay inputs. |
| Relay module | The four-channel relay board seen in the photo set. | Relay input behavior and load-side safety remain unresolved. |
| Load side | The switched electrical side of a relay. | Not documented as a public wiring procedure. |

## What is blocked and why

- Relay/load wiring is blocked because the exact relay-module trigger polarity,
  input current, 3.3 V behavior, jumper behavior, and isolation boundary remain
  unresolved.
- Mains wiring is blocked because hazardous-voltage work requires qualified
  review, enclosure, overcurrent, grounding/bonding, strain relief, and
  de-energization evidence.
- TFT wiring is blocked because the exact display module, power, bus width,
  control pins, backlight, touch interface, and pin-conflict review are not
  closed.
- Expander-to-relay wiring is blocked because the expander output behavior,
  inactive defaults, pullups/addressing, and driver-stage fit must be proven
  before any relay input connection.

Relay/load wiring, mains wiring, TFT wiring, and expander-to-relay wiring
remain blocked until the documented gates close.

## Conceptual schematic, not a wiring diagram

The visual blueprint and the text block diagram do not specify exact wires,
wire colors, pin numbers, terminal order, current ratings, enclosure choices, or
bench authorization. Treat them as a checklist for what must be verified next.

## Short glossary

| Term | Meaning |
| --- | --- |
| GPIO | General-purpose ESP32 signal pin; a visible label is not proof of safe relay drive. |
| Relay | Electrically controlled switch; this project has not approved load terminals or relay contacts. |
| Mux | Multiplexer; a selector for input scanning, not relay output holding. |
| Expander | I/O expander; a chip that can add low-voltage outputs after LED or logic-analyzer proof. |
| XBee | Digi radio module; current work starts with read-only identification through a PC adapter. |
| TFT | Planned local display; exact module and wiring remain unresolved. |
| MicroSD | Storage media for static assets and logs; bus and pin choices remain gated. |
| Hardware gate | A documented stop point that must close before the next bench action is allowed. |

## Verified facts

- The photographed bench target is an ESP-WROOM-32-family development board on
  an ESP32 I/O expansion shield, a four-channel relay module with Songle
  `SRD-05VDC-SL-C` relay cans, Digi `XBP9B-DPUT-001 RevF`, and a Waveshare
  XBee USB Adapter. Source IDs:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
  `SRC-SONGLE-SRD-05VDC-SL-C`, `SRC-DIGI-XBP9B-DPUT-001`,
  `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- Espressif's ESP32-WROOM-32 datasheet and ESP32 hardware design guidelines are
  the source-backed references for ESP32 module power, GPIO, UART, reset, and
  strapping-pin review. Source IDs: `SRC-ESP32-WROOM-32-DATASHEET`,
  `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.
- The photographed shield labels include `GPIO25`, `GPIO26`, `GPIO27`, and
  `GPIO33`; those remain provisional relay-output candidates only. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- The Waveshare XBee USB Adapter is source-backed as a PC-side UART/XBee
  communication board; it is not verified as an ESP32-mounted carrier. Source
  ID: `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- Safety references support a hard mains-readiness gate, not a mains wiring
  procedure. Source IDs: `SRC-NIOSH-ELECTRICAL-SAFETY`,
  `SRC-OSHA-DEENERGIZED-WORK`, `SRC-OSHA-GFCI`, `SRC-OSHA-AEGCP`,
  `SRC-OSHA-GROUNDING-OVERCURRENT`, `SRC-NEMA-ENCLOSURES`.
- CD74HC4067, TCA9555, MCP23017, and TPIC6B595 sources support the revised
  expansion plan: mux for slow inputs, latched GPIO expander for relay-state
  mirroring, and driver-stage selection only after relay evidence exists. Source
  IDs: `SRC-TI-CD74HC4067`, `SRC-TI-TCA9555`,
  `SRC-ESPRESSIF-MCP23017-COMPONENT`, `SRC-TI-TPIC6B595`.
- External R61509V references provide only planning context for the requested
  parallel TFT branch. Source IDs: `SRC-NOPNOP2002-ESP-IDF-PARALLEL-TFT`,
  `SRC-LCDWIKI-R61509V-MRB2802`.

## Assumptions

- This blueprint is documentation for staged bench verification only.
- Relay contacts stay disconnected or attached only to a reviewed low-voltage
  dummy load during prototype work.
- XBee work uses the Waveshare adapter as a PC dock for read-only discovery.
- New framework selection, hardware-facing firmware enablement, XBee setting
  writes, relay switching, and mains wiring stay out of scope for this
  documentation pass.
- TFT wiring, expander-to-relay wiring, and relay driver-stage wiring stay out
  of scope until exact module and bench evidence exist.

## Unknowns

- ESP32 board and shield identity, regulator capability, jumper state, and GPIO
  routing.
- Relay input polarity, input current, 3.3 V compatibility, coil/logic supply
  split, and isolation behavior.
- XBee adapter UART voltage, DIN/DOUT direction naming, serial-port path, and
  current budget.
- Open-Smart R61509V module identity, pinout, power, backlight, touch interface,
  and display-driver path.
- Relay expander board, I2C address/pullups, inactive defaults, output latch
  behavior, and driver-stage fit.
- CD74HC4067 breakout, address/enable wiring, ADC protection, scan cadence, and
  verified input-only role.
- Final load type, enclosure, overcurrent protection, grounding, strain relief,
  GFCI/de-energization process, and qualified review outcome.

## Prototype block diagram

```text
PC USB
  |
  +-- ESP32 dev board + expansion shield
  |      |
  |      +-- R61509V TFT planning branch, wiring blocked
  |      |
  |      +-- I2C relay expander planning branch
  |      |      |
  |      |      +-- LEDs or logic analyzer first proof
  |      |      |
  |      |      +-- relay driver stage only after relay input proof
  |      |
  |      +-- CD74HC4067 slow-input mux planning branch
  |      |
  |      +-- GPIO25/GPIO26/GPIO27/GPIO33 legacy direct candidates
  |             |
  |             +-- relay input header only after 3.3 V/current gate
  |                    |
  |                    +-- relay contacts disconnected or low-voltage dummy load
  |
  +-- Waveshare XBee USB Adapter
         |
         +-- Digi XBP9B-DPUT-001 read-only discovery

Mains wiring: hard blocked by mains-readiness gate.
```

## Stage 0 - Documentation preflight

Do not continue unless:

- [Prototype Build Packet](prototype-build-packet.md) is current and linked
  from the public Pages artifact.
- The active hardware is confirmed as the photographed target set or the docs
  are updated for a different target.
- `knowledge-base/source-index.md` contains all source IDs cited by this
  blueprint.
- The task record and handoff for this bench package are present.

Stop if:

- A required source ID is missing.
- The target hardware changes without a new photo/inspection record.

## Stage 1 - ESP32 board and shield verification

Goal: prove the shield can be inspected and powered safely before connecting
external modules.

Do not continue unless:

- Only one power source is selected for the board/shield inspection.
- Shield jumper position, active power input, regulator output, and current
  limit are recorded.
- Power-off continuity verifies each candidate shield label to the expected
  board pin.
- Boot-pin and flash-pin risks are reviewed against Espressif sources.

Stop if:

- Any power rail is shorted, ambiguous, or outside the expected board-source
  range.
- The shield appears to route a candidate GPIO to the wrong pin.
- The board enters an unexpected boot mode or the boot/reset circuit is not
  understood.

## Stage 2 - Relay-module verification

Goal: decide whether direct ESP32 GPIO drive is allowed, blocked, or superseded
by the relay-expander branch.

Do not continue unless:

- Relay outputs are disconnected or attached only to a reviewed low-voltage
  dummy load.
- Relay input polarity is identified by source or measurement.
- Relay input current is measured or source-backed for the exact module.
- 3.3 V drive behavior is tested without exceeding a source-backed ESP32 GPIO
  current limit.
- `JD-VCC`/`VCC` coil/logic behavior and isolation boundary are recorded.

Pass result:

- Direct GPIO drive remains a candidate only if the measured relay input
  behavior passes the 3.3 V/current gate and owner review records the result.

Fail result:

- Relay wiring stays blocked and the next design must add a future driver-stage
  design.

Expansion result:

- If TFT pin pressure remains active, route relay control through a latched
  expander plus verified driver stage even if direct GPIO remains electrically
  possible.

Stop if:

- The module actuates unpredictably, exceeds the current gate, requires 5 V
  logic, has unclear isolation behavior, or has any load connected.

## Stage 3 - XBee read-only discovery

Goal: identify the radio from a PC dock without changing settings.

Do not continue unless:

- The Waveshare adapter is connected only to the PC for this pass.
- Host serial-port identity, driver state, and adapter power source are
  recorded.
- The dedicated [XBee read-only bench proof](xbee-read-only-bench-proof.md) is
  followed before any configuration write is considered.
- Tier A passive discovery is complete before Tier B read-query discovery is
  attempted.

Tier A passive discovery:

- Enumerate host serial candidates with
  `python3 scripts/xbee_read_only_probe.py list --json`.
- Inspect adapter markings, socket orientation, antenna connection, header
  labels, and the active host connection.
- Measure exposed adapter/header voltage with a multimeter while the adapter is
  not connected to ESP32 GPIO.
- Optionally observe incoming bytes with `passive`; the passive command must
  open and read only, with no serial writes.

Tier B read-query discovery:

- Run only with `--confirm-sends-read-commands`.
- Send the command-mode guard sequence, then allow only fixed non-persistent AT
  reads: `VR`, `HV`, `SH`, `SL`, `AP`, `AO`, `BD`, and `NP`.
- Redact `SH` and `SL` by default unless the evidence is kept local-only.
- Block AT parameter writes, `WR`, `AC`, firmware updates, API transmit frames,
  relay commands, ESP32 DIN/DOUT wiring, and adapter/radio setting changes.

Stop if:

- The adapter voltage path is unclear.
- Any tool requires writing settings to identify the radio.
- Tier B is attempted without the explicit confirmation flag.
- The adapter is proposed as an ESP32 carrier without a separate carrier review.

## Stage 3A - TFT and expansion dry proof

Goal: prove input and output expansion behavior without relay-module inputs,
relay coils, or TFT wiring.

Do not continue unless:

- CD74HC4067 is connected only to ADC1 test voltages or other reviewed
  low-voltage inputs.
- MCP23017 or TCA9555 is powered from a verified logic rail with documented I2C
  pullups and address pins.
- Expander outputs drive LEDs or a logic analyzer only.
- TFT work is still documentation and pin-conflict review unless exact module
  power and pinout evidence exists.

Stop if:

- Any mux channel is proposed as a relay output.
- Any expander output is connected to a relay module before trigger
  polarity/current/voltage/isolation evidence exists.
- TFT bus wiring would use boot, flash, UART0, relay, XBee, or MicroSD pins
  before the conflict review is complete.

## Mains-readiness gate

Mains switching is not part of this prototype. See
[Mains readiness gate](mains-readiness-gate.md).

Do not continue unless:

- A qualified person reviews the load, enclosure, overcurrent protection,
  grounding/bonding, strain relief, GFCI/de-energization process, and applicable
  code/source evidence.
- The reviewed design is captured in a new source-backed task and handoff.
