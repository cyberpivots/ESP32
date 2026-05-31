# Task 0093 - XBee ESP32 Level-Shifting Wiring Plan

## Triage

- Verified facts: The target radio family remains Digi XBee-PRO 900HP / S3B,
  with local project evidence for `XBP9B-DPUT-001`.
- Verified facts: Digi's XBee-PRO 900HP user guide lists supply voltage
  `2.1 to 3.6 VDC`, notes reduced performance below 3.0 V, and lists GPIO
  voltage supply as `2.1 - 3.6 V`.
- Verified facts: Digi lists the only required pin connections for two-way
  UART communication as `VCC`, `GND`, `DOUT`, and `DIN`.
- Verified facts: Espressif's ESP32-DevKitC guide lists `3V3` as a 3.3 V
  power-supply pin and warns that Micro USB, 5V/GND, and 3V3/GND are mutually
  exclusive board power options.
- Verified facts: Espressif's ESP32 GPIO guide identifies GPIO0, GPIO2, GPIO5,
  GPIO12, and GPIO15 as strapping pins; GPIO6-11 and usually GPIO16-17 as
  flash/PSRAM-related pins; GPIO34-39 as input-only; and UART0 TXD/RXD as
  usually used for flashing/debugging.
- Assumptions: The first integration target is a bare XBee module or a carrier
  that exposes true XBee-side 3.3 V UART pins, not a 5 V host-side TTL header.
- Unknowns: Exact XBee carrier/breakout board, measured carrier VCC, current
  margin of the selected 3.3 V rail, final ESP32 module variant, final DIN/DOUT
  route, antenna condition, enclosure/grounding, and physical strain relief.
- Selected tier: Tier 2 source-backed hardware-adjacent planning only.
- Owner role: Hardware integration with XBee/radio and QA role lenses.
- Evidence need: Official Digi and Espressif voltage, UART, pinout, and
  boot-risk sources.
- Mutation boundary: Documentation task record only. No live wiring, no ESP32
  flash/monitor, no serial/radio writes, no firmware update/recovery, no
  relay/load/mains action.
- Validation plan: Provide wiring instructions with stop gates; require
  multimeter confirmation of 3.3 V VCC, common ground, no 5 V UART exposure,
  safe ESP32 pin selection, and antenna/power-current readiness before any
  physical connection.

## Sources

- Digi XBee-PRO 900HP/XSC RF Modules User Guide:
  `https://docs.digi.com/resources/documentation/digidocs/pdfs/90002173.pdf`
- Digi XBP9B-DPUT-001 model page:
  `https://www.digi.com/products/models/xbp9b-dput-001`
- Espressif ESP32-DevKitC V4 User Guide:
  `https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html`
- Espressif ESP32 GPIO & RTC GPIO guide:
  `https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/gpio.html`
- Espressif ESP32-WROOM-32 datasheet:
  `https://documentation.espressif.com/esp32-wroom-32_datasheet_en.html`

## Reviewer Quorum

- Coordinator: approved Tier 2 planning only, with no live wiring or radio
  mutation.
- Hardware: approved the 3.3 V-only wiring plan, contingent on measured VCC
  and current margin before bench connection.
- XBee/radio: approved UART-level guidance only; ESP32 carrier wiring and live
  radio changes remain closed.
- QA: approved the stop gates and multimeter checks as the next validation
  boundary.

No subagents were spawned; role lenses were run locally.

Weighted local decision result: approval ratio `1.0`, approval weight `12/12`,
no P1/P2 blockers, and decision `continue` for source-backed instructions only.

## Outcome

The source-backed recommendation is: no logic level shifter is required between
ESP32 UART pins and a bare XBee-PRO 900HP DIN/DOUT interface when both sides are
powered and signaled in the 3.3 V domain. A level shifter or different carrier
is required if any adapter/header exposes 5 V TTL or can drive ESP32/XBee signal
pins above 3.3 V.

Physical connection remains blocked until the exact XBee carrier/breakout and
3.3 V rail current margin are measured and recorded.
