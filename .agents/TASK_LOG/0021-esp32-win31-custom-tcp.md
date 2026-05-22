# Task Log 0021 - DOS-C Windows 3.1 Custom TCP Bridge

## Task

- ID: 0021-esp32-win31-custom-tcp
- Owner role: Communications, QA
- Status: simulator compact-state update implemented; live hardware gates closed
- Created: 2026-05-20
- Updated: 2026-05-20

## Goal

Provide the ESP32-side simulator target for a DOS-C Windows 3.1 operator
console using newline-delimited TCP JSON on port `31331`.

## Scope

Included:

- Host-side simulator under `tools/simulators/esp32_gateway_tcp/`.
- Protocol tests under `tests/esp32_gateway_tcp/`.
- Project documentation for the DOS-C bridge.
- Source ledger entry for the simulator-first boundary.

Excluded:

- Live ESP32 firmware socket task.
- Relay GPIO writes, expander writes, XBee setting writes, XBee transmit
  frames, flashing, monitor automation, and mains/load work.
- PCAP bridge acceptance from DOSBox-X.

## Sources

- `SRC-ESP-IDF-LWIP-SOCKETS`
- `SRC-LOCAL-FOUR-RELAY-SAFE-CORE-CONTRACT-2026-05-19`

## Decisions

- `relay_set` remains visible to the operator UI but returns
  `control_disabled` in v1.
- Public relay channels remain `1..4`.
- The first proof remains simulator-first.
- The `state` response is compact enough for the DOS-C 512-byte line limit.

## Validation

Planned and run from this workspace:

- `python3 tests/esp32_gateway_tcp/test_protocol.py`
- `python3 scripts/verify_scaffold.py`
- Existing safe-core host tests remain part of the broader validation stack.

## Handoff

Next owner: Communications and DOS-C integration.

Next action: complete DOSBox-X SLIRP proof from the Windows 3.1 operator app to
the Pi-host simulator at `10.0.2.2:31331`, then document acceptance evidence in
the ignored integration record directory.
