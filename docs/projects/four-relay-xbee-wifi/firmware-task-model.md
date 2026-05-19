# Firmware Task Model

## Verified facts

- ESP-IDF stable v6.0.1 includes the project APIs used for Wi-Fi, HTTP server,
  GPIO, UART, NVS, FatFS/VFS, and SDSPI design. Source IDs: `SRC-ESP-IDF-WIFI`,
  `SRC-ESP-IDF-HTTP-SERVER`, `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-UART`,
  `SRC-ESP-IDF-NVS`, `SRC-ESP-IDF-FATFS`, `SRC-ESP-IDF-SDSPI`.
- HTTP Server APIs are not thread-safe and require application-layer
  synchronization if multiple tasks interact with server state. Source ID:
  `SRC-ESP-IDF-HTTP-SERVER`.
- TCA9555 and MCP23017 are documented 16-bit I/O expansion options for a future
  latched relay-output path. Source IDs: `SRC-TI-TCA9555`,
  `SRC-ESPRESSIF-MCP23017-COMPONENT`.
- CD74HC4067 is a one-channel analog mux/demux for input routing, not relay
  state holding. Source ID: `SRC-TI-CD74HC4067`.

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
- Relay output writes are performed by a future `relay_expander` task when the
  expander branch is selected; HTTP, XBee, TFT, and mux input paths never write
  relay outputs directly.
- `mux_scan` only publishes filtered input observations or UI intents. It never
  emits relay state changes directly.

## Proposed tasks

| Task | Responsibility | Inputs | Outputs |
| --- | --- | --- | --- |
| `relay_manager` | Own relay state, safety lock, boot default, all-off, and polarity config. | HTTP commands, XBee commands, TFT UI intents, mux-derived UI intents, watchdog/reset events. | Approved relay state snapshot, expander write requests, state snapshot, reject reasons. |
| `relay_expander` | Initialize expander pins inactive, mirror approved relay states to the latched expander, and fault the hardware gate on init/write/readback failure. | Relay manager state, I2C health, expander config. | Expander output writes, readback status, `relayExpander` health fields. |
| `mux_scan` | Scan CD74HC4067 channels at low rate for touch/input observations only. | Mux address pins, ADC result, debounce/filter config. | `mux.ready`, input observations, UI-intent events. |
| `tft_ui` | Present local status and produce UI intents from touch/buttons after display proof. | State snapshots, touch/input observations. | UI-intent messages queued to relay manager; no direct relay writes. |
| `http_server` | Serve static UI and REST endpoints. | Browser requests. | State responses and queued relay requests. |
| `storage_manager` | Mount `/sdcard`, expose static asset and log health, and keep storage failures non-fatal for safety state. | SDSPI mount result, FatFS/VFS paths, asset manifest, log append status. | Storage summary for `/api/state`, `/api/storage/status`, asset manifest response, logger availability. |
| `event_logger` | Append relay, safety, XBee, storage, and rejected-command events when storage is writable. | State transitions, command rejects, XBee link events, storage faults. | JSONL files under `/sdcard/logs/events` and `/sdcard/logs/relay`. |
| `xbee_uart` | Read/write escaped API frames over UART. | UART bytes, outbound telemetry queue. | Decoded radio messages, transmit status. |
| `telemetry` | Publish periodic and event-driven state snapshots. | State snapshot, link status, last command source. | XBee transmit payloads and HTTP state fields. |
| `config_store` | Load and save NVS configuration. | Admin provisioning, allowlist updates, relay polarity setup. | Credentials, allowlist, safety settings. |
| `safety_supervisor` | Reject unsafe state transitions and force all-off on fault conditions. | Config validity, watchdog/reset flags, command validity. | Safety lock state and all-off requests. |

## Boot sequence

1. Initialize NVS.
2. Initialize relay expander hardware if selected, with all expander outputs in
   inactive relay state before relay commands are accepted.
3. Initialize direct GPIO pins in inactive relay state only if the direct-GPIO
   fallback is selected and verified.
4. Load relay polarity, admin credential state, XBee allowlist, and safety-lock
   default.
5. If configuration is incomplete or expander init/readback fails, keep
   relay-changing commands disabled and report `hardware_gate_open`.
6. Start SoftAP and HTTP server.
7. Attempt SDSPI/FatFS mount at `/sdcard` if the MicroSD hardware gate is
   enabled by verified configuration.
8. Register HTTP file handlers for `/sdcard/www` if the asset manifest is
   readable; otherwise serve a tiny embedded fallback page.
9. Start XBee UART parser only after serial configuration is loaded.
10. Start `mux_scan` only after voltage, ADC, and mux-address gates are verified.
11. Start `tft_ui` only after display power, pin, and driver gates are verified.
12. Publish first state snapshot with safety-lock, config-valid, storage summary,
    `relayExpander`, and `mux` fields.

Source IDs: `SRC-ESP-IDF-NVS`, `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-WIFI`,
`SRC-ESP-IDF-HTTP-SERVER`, `SRC-ESP-IDF-UART`, `SRC-ESP-IDF-FATFS`,
`SRC-ESP-IDF-SDSPI`, `SRC-ESP-IDF-RESTFUL-SERVER-EXAMPLE`.
Expansion source IDs: `SRC-TI-TCA9555`,
`SRC-ESPRESSIF-MCP23017-COMPONENT`, `SRC-TI-CD74HC4067`,
`SRC-TI-TPIC6B595`.

## State Snapshot Health Fields

```json
{
  "relayExpander": {
    "present": false,
    "ready": false,
    "lastWrite": "none"
  },
  "mux": {
    "ready": false
  }
}
```

If `relayExpander.ready` is required by the selected hardware profile and is
false, `hardwareGateClosed` must also be false.

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
- Final relay-expander part, I2C address, pullups, reset/default behavior,
  output readback policy, fault recovery, and driver-stage interface.
- Final mux scan list, ADC pins, protection network, debounce/filter policy, and
  whether touch input exists on the exact TFT module.
- Final TFT UI task shape, display driver, touch driver, and memory budget.
