# ADR-0001 - Firmware Framework Choice

## Status

Proposed

## Decision

The workspace remains framework-neutral. No Arduino, ESP-IDF, PlatformIO, or
other firmware framework is selected in the initial scaffold.

## Rationale

The workspace is intended for broad ESP32 device development across multiple
boards, radios, relay integrations, web interfaces, wired communication, and
custom protocols. Selecting a framework before requirements and board constraints
are verified would create avoidable coupling.

## Consequences

- Framework-specific files are prohibited until this ADR is accepted or replaced.
- Interface and documentation work may proceed.
- Firmware implementation waits for a source-backed framework decision.

