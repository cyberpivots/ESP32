# ADR-0003: ESP-NOW BBS Firmware Framework

Status: Accepted

Date: 2026-05-20

## Context

The DOS-C workspace is adding an off-grid BBS lane where Windows 3.1 talks to a
Raspberry Pi bridge, and the Pi bridge will later talk to an ESP32 DevKitC
coordinator over USB serial. The coordinator will use ESP-NOW to exchange
messages with ESP32 client devices.

This is a separate project lane from `four-relay-xbee-wifi`. It must not change
that project's safety gates or relay/XBee scope.

## Decision

Use ESP-IDF stable v6.0.1 as the project-local framework target for future
`espnow-bbs` coordinator and client firmware.

No firmware code is added by this ADR. Before code or flashing:

- Record toolchain evidence for `idf.py`, esptool, CMake, Ninja, Python, and
  shell path.
- Record the exact first flash target and recovery method.
- Keep serial diagnostics read-only until an explicit flash/write gate opens.
- Keep relay, XBee, mains/load, and SD imaging actions out of this lane.

## Rationale

ESP-IDF is Espressif's official ESP32 framework and provides source-backed
ESP-NOW, Wi-Fi, UART, NVS, and build/flash tooling documentation. ESP-NOW is
central to this lane, and using ESP-IDF avoids relying on a third-party Arduino
or PlatformIO abstraction before the radio and provisioning contract is proven.

## Consequences

- The workspace remains framework-neutral outside accepted project ADRs.
- `espnow-bbs` may later add ESP-IDF project files after toolchain and flash
  gates are recorded.
- Windows 3.1 remains a dashboard/client surface; ESP32 build and flashing
  remain Windows 11/Pi tooling responsibilities.

## Sources

- `SRC-ESP-IDF-STABLE-ESP32`
- `SRC-ESP-IDF-GET-STARTED`
- `SRC-ESP-IDF-ESPNOW`
- `SRC-ESPTOOL-BASIC`
