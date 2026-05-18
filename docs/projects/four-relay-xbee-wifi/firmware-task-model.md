# Firmware Task Model

## Verified facts

- ESP-IDF stable v6.0.1 includes the project APIs used for Wi-Fi, HTTP server,
  GPIO, UART, NVS, FatFS/VFS, and SDSPI design. Source IDs: `SRC-ESP-IDF-WIFI`,
  `SRC-ESP-IDF-HTTP-SERVER`, `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-UART`,
  `SRC-ESP-IDF-NVS`, `SRC-ESP-IDF-FATFS`, `SRC-ESP-IDF-SDSPI`.
- HTTP Server APIs are not thread-safe and require application-layer
  synchronization if multiple tasks interact with server state. Source ID:
  `SRC-ESP-IDF-HTTP-SERVER`.

## Assumptions

- Relay state is owned by one internal relay manager rather than directly by
  HTTP handlers or XBee handlers.
- Runtime state is small enough to publish through `/api/state` and periodic
  XBee telemetry without external storage.
- All state-changing paths use a queue or equivalent synchronization boundary in
  the future ESP-IDF implementation.
- Static web assets and append-only event logs are SD-card responsibilities
  after `/sdcard` is mounted, while NVS remains the safety-critical config
  store.

## Proposed tasks

| Task | Responsibility | Inputs | Outputs |
| --- | --- | --- | --- |
| `relay_manager` | Own relay state, safety lock, boot default, all-off, and polarity config. | HTTP commands, XBee commands, watchdog/reset events. | GPIO writes, state snapshot, reject reasons. |
| `http_server` | Serve static UI and REST endpoints. | Browser requests. | State responses and queued relay requests. |
| `storage_manager` | Mount `/sdcard`, expose static asset and log health, and keep storage failures non-fatal for safety state. | SDSPI mount result, FatFS/VFS paths, asset manifest, log append status. | Storage summary for `/api/state`, `/api/storage/status`, asset manifest response, logger availability. |
| `event_logger` | Append relay, safety, XBee, storage, and rejected-command events when storage is writable. | State transitions, command rejects, XBee link events, storage faults. | JSONL files under `/sdcard/logs/events` and `/sdcard/logs/relay`. |
| `xbee_uart` | Read/write escaped API frames over UART. | UART bytes, outbound telemetry queue. | Decoded radio messages, transmit status. |
| `telemetry` | Publish periodic and event-driven state snapshots. | State snapshot, link status, last command source. | XBee transmit payloads and HTTP state fields. |
| `config_store` | Load and save NVS configuration. | Admin provisioning, allowlist updates, relay polarity setup. | Credentials, allowlist, safety settings. |
| `safety_supervisor` | Reject unsafe state transitions and force all-off on fault conditions. | Config validity, watchdog/reset flags, command validity. | Safety lock state and all-off requests. |

## Boot sequence

1. Initialize NVS.
2. Initialize GPIO pins in inactive relay state.
3. Load relay polarity, admin credential state, XBee allowlist, and safety-lock
   default.
4. If configuration is incomplete, keep relay-changing commands disabled.
5. Start SoftAP and HTTP server.
6. Attempt SDSPI/FatFS mount at `/sdcard` if the MicroSD hardware gate is
   enabled by verified configuration.
7. Register HTTP file handlers for `/sdcard/www` if the asset manifest is
   readable; otherwise serve a tiny embedded fallback page.
8. Start XBee UART parser only after serial configuration is loaded.
9. Publish first state snapshot with safety-lock, config-valid, and storage
   summary fields.

Source IDs: `SRC-ESP-IDF-NVS`, `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-WIFI`,
`SRC-ESP-IDF-HTTP-SERVER`, `SRC-ESP-IDF-UART`, `SRC-ESP-IDF-FATFS`,
`SRC-ESP-IDF-SDSPI`, `SRC-ESP-IDF-RESTFUL-SERVER-EXAMPLE`.

## Reject reasons

- `admin_required`
- `safety_locked`
- `relay_config_missing`
- `relay_channel_invalid`
- `payload_invalid`
- `sequence_replay`
- `source_not_allowed`
- `xbee_link_unverified`
- `hardware_gate_open`
- `storage_unavailable`
- `log_append_failed`

## Unknowns

- Final RTOS task priorities, stack sizes, and queue lengths.
- Watchdog policy and reset reason handling details.
- Final persistence policy for last-known relay states.
- Final admin provisioning flow.
- Final telemetry cadence and retry/backoff parameters.
- Final SDSPI bus frequency, card detect/write protect behavior, log rotation,
  low-space response, and fallback-page implementation.
