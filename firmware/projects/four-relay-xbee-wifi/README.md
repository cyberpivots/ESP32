# Four Relay XBee Wi-Fi Firmware Skeleton

This directory contains the project-local ESP-IDF skeleton allowed by ADR-0002.
All hardware-facing behavior is disabled by default and the reusable core is
tested on the host before any ESP-IDF build or bench step.

## Verified facts

- ADR-0002 accepts ESP-IDF stable v6.0.1 for `four-relay-xbee-wifi` only.
  Source IDs: `SRC-ESP-IDF-STABLE-ESP32`, `SRC-ESP-IDF-GET-STARTED`.
- ESP-IDF stable v6.0.1 includes the APIs planned for Wi-Fi, HTTP server, GPIO,
  UART, NVS, FatFS/VFS, and SDSPI. Source IDs: `SRC-ESP-IDF-WIFI`,
  `SRC-ESP-IDF-HTTP-SERVER`, `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-UART`,
  `SRC-ESP-IDF-NVS`, `SRC-ESP-IDF-FATFS`, `SRC-ESP-IDF-SDSPI`.
- The current XBee lane remains read-only until a later gate authorizes writes.
  Source IDs: `SRC-LOCAL-XBEE-READONLY-PROBE-2026-05-18`,
  `SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`,
  `SRC-DIGI-XBEE-900HP-NP`.

## Assumptions

- `safe_core` stays pure C so it can be compiled by host tests without ESP-IDF
  tools.
- `app_main` may initialize in-memory defaults only. No GPIO, UART, I2C,
  storage mount, Wi-Fi, HTTP server, flash, or monitor action is performed.
- Future ESP-IDF work must preserve the relay manager and safety supervisor as
  the only path to relay state changes.

## Unknowns

- ESP-IDF v6.0.1, CMake, Ninja, and flashing tools are not proven installed in
  the current shell.
- Board/shield power, relay input polarity/current, XBee carrier wiring,
  MicroSD wiring, TFT wiring, mux wiring, expander wiring, and load/enclosure
  evidence remain blocked.
- Final FreeRTOS task layout, pins, authentication, telemetry cadence, storage
  policy, and rollback behavior are unresolved.

## Hard gates

- No GPIO writes to relay pins.
- No expander writes to relay hardware.
- No XBee setting writes or API transmit frames to hardware.
- No flash or monitor step in automated validation.
- No live bench mutation.

## Layout

- `CMakeLists.txt` and `main/` form the minimal ESP-IDF project shell.
- `components/safe_core/` contains host-testable state, safety, config, API,
  storage, and XBee frame logic.
- Public relay channels are `1..4`; `safe_core` maps those public numbers to
  zero-based internal relay-state indexes before touching desired-state arrays.
  Source ID: `SRC-LOCAL-FOUR-RELAY-SAFE-CORE-CONTRACT-2026-05-19`.
- `tests/four_relay_safe_core/` compiles the same core files with the host C
  compiler and verifies safe defaults and negative paths.
