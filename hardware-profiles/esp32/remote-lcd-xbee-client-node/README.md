# Remote LCD XBee Client Node ESP32 Profile

## Status

Planning stub for the `remote-lcd-xbee-solar-client` lane. Exact ESP32 board is
unresolved.

## Verified facts

- Espressif source coverage exists for ESP32 GPIO review, UART review, and
  hardware-design review points, but no exact client board is selected by this
  scaffold. Source IDs: `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-UART`,
  `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.
- This workspace has not verified the exact ESP32 board, module, regulator,
  USB-UART bridge, header mapping, carrier, boot/recovery method, or power
  input path for this project lane. Source ID:
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`.

## Assumptions

- The ESP32 board must preserve bootloader and serial recovery before any LCD,
  encoder, XBee, charger, or fuel-gauge pin plan is accepted.
- A project-specific framework ADR is required before firmware implementation.

## Unknowns

- Exact board vendor, revision, module, flash/PSRAM configuration, regulator,
  USB-UART bridge, and power input options.
- Exposed header pin mapping and whether labels match ESP32 GPIO numbers.
- Boot button, EN/reset circuit, UART0 accessibility, strapping-pin exposure,
  and recovery workflow.
- Power budget for ESP32 plus XBee transmit current, LCD backlight, charger SYS
  behavior, and any measurement devices.

## Risks

- Peripheral pullups or switches can force boot-strapping pins into unsafe
  states.
- Shared UART or USB serial assumptions can break flashing/recovery.
- Unverified regulator capacity can brown out under XBee transmit or LCD
  backlight load.
- Solar/battery power paths can backfeed USB or other rails if source selection
  is not understood.

## Required next evidence

- Exact board source and physical inspection record.
- Boot/recovery procedure with no peripherals attached.
- Power-path and regulator evidence before battery/solar use.
- Pin-risk review for LCD, encoder, XBee, and any power telemetry interface.
- Accepted project ADR before framework-specific firmware files are added.
