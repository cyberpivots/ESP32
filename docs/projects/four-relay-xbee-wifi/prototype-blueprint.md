# Prototype Blueprint

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

## Assumptions

- This blueprint is documentation for staged bench verification only.
- Relay contacts stay disconnected or attached only to a reviewed low-voltage
  dummy load during prototype work.
- XBee work uses the Waveshare adapter as a PC dock for read-only discovery.
- Firmware, framework files, XBee setting writes, relay switching, and mains
  wiring stay out of scope for this documentation pass.

## Unknowns

- ESP32 board and shield identity, regulator capability, jumper state, and GPIO
  routing.
- Relay input polarity, input current, 3.3 V compatibility, coil/logic supply
  split, and isolation behavior.
- XBee adapter UART voltage, DIN/DOUT direction naming, serial-port path, and
  current budget.
- Final load type, enclosure, overcurrent protection, grounding, strain relief,
  GFCI/de-energization process, and qualified review outcome.

## Prototype block diagram

```text
PC USB
  |
  +-- ESP32 dev board + expansion shield
  |      |
  |      +-- GPIO25/GPIO26/GPIO27/GPIO33 candidates
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

Goal: decide whether direct ESP32 GPIO drive is allowed or blocked.

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

Stop if:

- The module actuates unpredictably, exceeds the current gate, requires 5 V
  logic, has unclear isolation behavior, or has any load connected.

## Stage 3 - XBee read-only discovery

Goal: identify the radio from a PC dock without changing settings.

Do not continue unless:

- The Waveshare adapter is connected only to the PC for this pass.
- Host serial-port identity, driver state, and adapter power source are
  recorded.
- Read-only radio identity is captured before any configuration write is
  considered.

Stop if:

- The adapter voltage path is unclear.
- Any tool requires writing settings to identify the radio.
- The adapter is proposed as an ESP32 carrier without a separate carrier review.

## Mains-readiness gate

Mains switching is not part of this prototype. See
[Mains readiness gate](mains-readiness-gate.md).

Do not continue unless:

- A qualified person reviews the load, enclosure, overcurrent protection,
  grounding/bonding, strain relief, GFCI/de-energization process, and applicable
  code/source evidence.
- The reviewed design is captured in a new source-backed task and handoff.
