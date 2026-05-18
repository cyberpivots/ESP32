# ESP-WROOM-32 Development Board Profile

## Status

Current photographed target for `four-relay-xbee-wifi`. This is a
verification-only profile until the carrier-board vendor, revision, regulator,
USB-UART bridge, and expansion-shield routing are identified.

## Verified facts

- The photo archive shows an ESP32 development board populated with an
  ESP-WROOM-32-family module. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- The photo archive shows a black ESP32 I/O expansion shield with labeled GPIO
  positions, barrel jack, USB connector, and visible `DC6.5-16V`, `USB5V`,
  `5V`, and `3.3V` markings. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Espressif's ESP32-WROOM-32 datasheet identifies ESP32-WROOM-32 as a Wi-Fi
  plus Bluetooth MCU module with 3.0 V to 3.6 V module supply, GPIO, UART, and
  boot-strap constraints. Source ID: `SRC-ESP32-WROOM-32-DATASHEET`.
- Espressif's ESP32 hardware design guidelines provide board-level review
  points for 3.3 V supply/current, reset timing, UART, strapping pins, and
  GPIO. Source ID: `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.
- A third-party NodeMCU ESP32 expansion-board page is a non-authoritative
  identity candidate for a similar shield class only; it does not verify this
  photographed shield's exact revision, schematic, regulator, or safe power
  path. Source ID: `SRC-ESP32-IO-SHIELD-CANDIDATE`.
- Espressif's ESP32 GPIO documentation identifies strapping pins and flash pins
  that require first-pass avoidance or review before use. Source ID:
  `SRC-ESP-IDF-GPIO`.

## Provisional project use

| Project signal | Provisional pin | Status |
| --- | --- | --- |
| Relay channel 1 | GPIO25 | Visible shield label; blocked on shield routing and relay verification |
| Relay channel 2 | GPIO26 | Visible shield label; blocked on shield routing and relay verification |
| Relay channel 3 | GPIO27 | Visible shield label; blocked on shield routing and relay verification |
| Relay channel 4 | GPIO33 | Visible shield label; blocked on shield routing and relay verification |
| XBee UART | Unassigned | Final ESP32 carrier/path not selected |

Source IDs: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
`SRC-ESP32-WROOM-32-DATASHEET`, `SRC-ESP-IDF-GPIO`,
`SRC-ESP-IDF-UART`, `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.

## Closure evidence required

| Item | Closure evidence |
| --- | --- |
| Dev-board identity | Photo/inspection record or exact vendor source identifying board vendor, revision, USB-UART bridge, regulator, reset/boot circuit, and module marking. |
| Shield identity | Exact shield source or inspection record; `SRC-ESP32-IO-SHIELD-CANDIDATE` may only support candidate matching and cannot close this item by itself. |
| Power path | Measured single-source input, jumper position, regulator output, current budget, and no dual-power conflict. |
| Candidate GPIO routing | Continuity record for `GPIO25`, `GPIO26`, `GPIO27`, and `GPIO33` from shield labels to expected ESP32 board pins. |
| Boot-pin risk | Review against Espressif strapping, reset, UART0, and flash-pin constraints. |

## Assumptions

- The photographed ESP32 board and expansion shield are the current target for
  planning and bench gates.
- The expansion shield may be useful for bench wiring after its jumper state,
  input power path, and continuity to the ESP32 board are verified.

## Unknowns

- Exact dev-board vendor, board revision, and whether it matches any Espressif
  reference devkit pinout.
- Exact module ordering code, flash size, and chip revision.
- USB-UART bridge identity and serial-port behavior.
- Expansion-shield schematic, regulator current budget, jumper behavior, and
  whether `DC6.5-16V`, `USB5V`, `5V`, and `3.3V` labels match the actual power
  path.
- Whether the photographed shield routes GPIO25, GPIO26, GPIO27, and GPIO33 to
  the inserted ESP32 board pins without swap or conflict.
- Whether the board and shield can safely power the relay module or XBee radio.
- Whether the third-party candidate shield page matches the photographed shield.

## Bring-up blockers

- Do not power the ESP32 board and expansion shield from multiple sources.
- Do not use the shield barrel jack until jumper position, regulator behavior,
  output voltage, and current limit are measured.
- Do not wire relay inputs until relay trigger polarity, input current, and
  3.3 V compatibility are verified.
- Do not connect the XBee DIN/DOUT path to ESP32 GPIO until carrier voltage and
  routing are verified.
