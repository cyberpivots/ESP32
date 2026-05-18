# Power And Safety Gates

## Verified facts

- The current photo archive shows an ESP-WROOM-32-family development board on a
  black ESP32 I/O expansion shield with visible `DC6.5-16V`, `USB5V`, `5V`, and
  `3.3V` markings. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Espressif's ESP32-WROOM-32 datasheet gives module-level supply and electrical
  context for ESP32-WROOM-32, but not the photographed dev-board regulator or
  expansion-shield power path. Source ID: `SRC-ESP32-WROOM-32-DATASHEET`.
- Espressif's ESP32 hardware design guidelines provide ESP32 review points for
  3.3 V supply/current, reset timing, UART, strapping pins, and GPIO. Source
  ID: `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.
- A third-party NodeMCU ESP32 expansion-board page is a non-authoritative
  identity candidate for a similar shield class with DC 6.5-16 V, USB 5 V, and
  5 V/3.3 V jumper text; it does not verify the photographed shield. Source ID:
  `SRC-ESP32-IO-SHIELD-CANDIDATE`.
- The relay module photos show a blue `4 Relay Module` populated with Songle
  `SRD-05VDC-SL-C` relay cans and a visible `JD-VCC`/`VCC` area. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- The Songle relay datasheet mirror provides component-level context for
  `SRD-05VDC-SL-C`; it does not verify the photographed module's input trigger
  circuit, jumper behavior, or isolation boundary. Source ID:
  `SRC-SONGLE-SRD-05VDC-SL-C`.
- Digi's 900HP product material lists UART (3V) and SPI data interfaces. Source
  ID: `SRC-DIGI-XBEE-PRO-900HP`.
- The photo archive shows a Waveshare `XBee USB Adapter`; Waveshare documents
  the adapter as a UART communication board with XBee and USB interfaces.
  Source IDs: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
  `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- NIOSH, OSHA, and NEMA sources support a mains-readiness checklist around
  qualified-person review, de-energization, GFCI/grounding context, protective
  devices, and enclosure selection; they do not authorize DIY mains wiring.
  Source IDs: `SRC-NIOSH-ELECTRICAL-SAFETY`, `SRC-OSHA-DEENERGIZED-WORK`,
  `SRC-OSHA-GFCI`, `SRC-OSHA-AEGCP`, `SRC-OSHA-GROUNDING-OVERCURRENT`,
  `SRC-NEMA-ENCLOSURES`.

## Assumptions

- Bench development uses low-voltage test loads or disconnected relay outputs
  until load safety is reviewed.
- Relay GPIO outputs are configured to the inactive state before relay driver
  enablement.
- The application treats ambiguous relay polarity as a configuration error and
  refuses relay changes until the polarity is verified.
- The Waveshare adapter is a PC-side XBee configuration/debug dock until proven
  safe for any ESP32-mounted role.
- Relay contacts remain disconnected or attached only to a reviewed low-voltage
  dummy load until a mains/load package is separately approved.

## Hardware gates before wiring

| Gate | Required evidence | Owner |
| --- | --- | --- |
| ESP32 board identity | Photo/source/inspection record showing dev-board vendor, revision, USB-UART bridge, regulator, and module variant. | Hardware |
| Expansion shield power and routing | Jumper position, selected input source, regulator output, current limit, shield-to-board continuity, and no dual-power conflict. | Hardware |
| Relay board identity | Board manufacturer/model, schematic or product page, input voltage, trigger polarity, input current, isolation design, `JD-VCC`/`VCC` behavior, and channel/load ratings. | Hardware |
| XBee adapter identity and PC dock path | Adapter revision, PC serial port, driver path, power source, DIN/DOUT mapping, reset/sleep pins, optional CTS/RTS mapping, and level compatibility. | Hardware |
| Final ESP32-to-XBee carrier | Carrier/socket selection, 3.3 V power budget, DIN/DOUT routing, reset/sleep/associate/flow-control handling, and antenna clearance. | Hardware |
| Power tree | Bench supply limits, shared ground plan, 3.3 V/5 V budget, relay supply path, XBee transmit current budget, and isolation boundary. | Hardware |
| Load design | Load type, voltage/current, fusing, enclosure, grounding, snubber/surge needs, and legal/safety review for mains or inductive loads. | Hardware |
| Mains readiness | Qualified review, load definition, enclosure, overcurrent protection, grounding/bonding, strain relief, GFCI/de-energization, separation, labels/disconnect, and test record. | Hardware + QA |

## Firmware safety requirements

- Boot state: all relay outputs are inactive before any saved state is applied.
- Reset/watchdog recovery: all relay outputs return inactive.
- Invalid HTTP or XBee command: no relay state change; reject reason is logged
  and reported.
- Safety lock closed: relay state-changing commands are rejected; all-off
  remains available through authenticated local control.
- Missing admin credential: relay state-changing HTTP endpoints are disabled.
- Missing XBee allowlist: radio relay commands are rejected.
- Missing relay polarity config: all relay commands are rejected.

## Bench action status

| Action | Status | Reason |
| --- | --- | --- |
| Power ESP32/shield through barrel jack | Blocked | Expansion-shield jumper state, regulator behavior, and active power source are unverified. |
| Wire ESP32 GPIO to relay inputs | Blocked | Relay trigger voltage/current/polarity and shield routing are unknown. |
| Power relay board from ESP32/shield 5 V | Blocked | Relay module current and `JD-VCC`/`VCC` isolation behavior are unknown. |
| Switch mains or inductive loads | Blocked | Load safety design is unknown. |
| Prepare mains switching steps | Blocked | The approved artifact is only `mains-readiness-gate.md`; no mains wiring procedure is allowed in this phase. |
| Use Waveshare adapter for read-only XBee discovery | Allowed after PC serial/driver check | No ESP32 wiring or XBee setting writes. |
| Write XBee configuration | Blocked | Current settings backup, address plan, AES key process, and rollback are not documented. |
| Connect XBee DIN/DOUT to ESP32 UART | Blocked | Final carrier, voltage path, and DIN/DOUT routing are unknown. |
| Build static UI prototype | Allowed | No hardware mutation. |
| Write ESP-IDF firmware source | Deferred | This pass is documentation and validation only. |

## Unknowns

- Whether the relay board is active-high or active-low.
- Whether relay inputs are compatible with ESP32 3.3 V GPIO levels.
- Relay input current per channel.
- Whether the relay board input side is opto-isolated and how that isolation is
  powered or bypassed by jumper position.
- Whether relay coils share logic supply or use a separate relay supply.
- Whether the intended load requires snubber, flyback, MOV, fuse, or contactor
  design.
- Whether the Waveshare XBee adapter exposes direct 3.3 V UART, level-shifted
  UART, or selectable power/logic rails on the photographed headers.
- Whether any future load design can satisfy the mains-readiness gate in
  `mains-readiness-gate.md`.
