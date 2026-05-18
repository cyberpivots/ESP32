# ADR-0002 - Four Relay XBee Wi-Fi Framework Target

## Status

Accepted

## Context

The first project design originally used ESP32 DevKitC as a source-backed
reference while targeting a four-channel relay board, a Digi XBee-PRO 900HP S3B
`XBP9B-DPUT-001`, and a local Wi-Fi control interface. A later photo-analysis
pass reframed the current physical target as a photographed ESP-WROOM-32
development board plus ESP32 I/O expansion shield, four-channel Songle relay
module candidate, Digi `XBP9B-DPUT-001 RevF`, and Waveshare XBee USB Adapter.
The workspace-level scaffold remains broadly reusable, but this project needs a
concrete firmware target for architecture, toolchain, and future build planning.

Source IDs: `SRC-ESP-IDF-STABLE-ESP32`, `SRC-ESP-IDF-GET-STARTED`,
`SRC-ESP-IDF-WIFI`, `SRC-ESP-IDF-HTTP-SERVER`, `SRC-ESP-IDF-GPIO`,
`SRC-ESP-IDF-UART`, `SRC-ESP-IDF-NVS`,
`SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
`SRC-ESP32-WROOM-32-DATASHEET`.

## Decision

The `four-relay-xbee-wifi` project targets ESP-IDF stable v6.0.1 for future
firmware implementation.

This ADR does not add firmware source, CMake files, sdkconfig files, or flash
steps. Hardware wiring and relay switching remain blocked until the physical
relay board, photographed ESP32 board/shield, XBee carrier/dock path, and load
safety design are verified.

## Rationale

Verified ESP-IDF stable documentation covers the project surfaces needed for a
first implementation:

- Wi-Fi AP mode for local bench control.
- HTTP server URI handlers and REST-style serving for the local UI.
- GPIO and GPIO matrix behavior for relay outputs and alternate UART routing.
- UART controllers for XBee host communication.
- NVS key-value storage for local credentials, admin token state, and safety
  configuration.
- Build, flash, and monitor workflows once ESP-IDF tools are installed.

## Consequences

- The workspace remains framework-neutral for other projects unless they receive
  their own accepted ADR.
- This project can include ESP-IDF-specific design notes and future build
  requirements.
- This design pass must not add framework project files or framework-dependent
  firmware source.
- Any future firmware implementation must preserve the relay safety gates
  documented in the project package.
