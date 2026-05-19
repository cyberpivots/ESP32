# Web Interface

## Verified facts

- ESP-IDF HTTP Server can run a lightweight web server on ESP32 and route
  requests to registered URI handlers. Source ID: `SRC-ESP-IDF-HTTP-SERVER`.
- The ESP-IDF RESTful server example combines REST-style API endpoints with web
  assets in an ESP32 application. Source ID:
  `SRC-ESP-IDF-RESTFUL-SERVER-EXAMPLE`.
- ESP-IDF FatFS support can mount FAT volumes through VFS so standard C library
  and POSIX-style file APIs can access paths under a selected mount point such
  as `/sdcard`. Source ID: `SRC-ESP-IDF-FATFS`.
- ESP-IDF SDSPI supports SD-card access over SPI and allows flexible pin
  routing through the GPIO matrix, with lower throughput than SDMMC host access.
  Source ID: `SRC-ESP-IDF-SDSPI`.
- The ESP-IDF SDSPI example mounts an SD card over SPI, prints card
  information, performs file write/read operations, supports customizable pin
  assignments, and warns that formatting can delete data. Source ID:
  `SRC-ESP-IDF-SDSPI-EXAMPLE`.
- ESP-IDF NVS stores key-value pairs in flash and is the planned storage surface
  for local credential and safety configuration. Source ID: `SRC-ESP-IDF-NVS`.
- ESP-IDF Wi-Fi supports AP mode where stations connect to the ESP32. Source ID:
  `SRC-ESP-IDF-WIFI`.
- Relay-expander and mux health fields are architecture-level planning fields
  backed by the expander and mux sources. Source IDs: `SRC-TI-TCA9555`,
  `SRC-ESPRESSIF-MCP23017-COMPONENT`, `SRC-TI-CD74HC4067`.

## Assumptions

- The first UI is a local admin HMI served by the ESP32 with plain
  `index.html`, `styles.css`, `app.js`, and `manifest.json`; no external fonts,
  CDNs, build pipeline, or bulky assets are required.
- Static web assets live on MicroSD under `/sdcard/www` and are served from `/`
  by ESP32 HTTP server file handlers after the card mounts.
- Event logs live on MicroSD under `/sdcard/logs` and are surfaced through
  read-only API endpoints for browser display.
- NVS remains authoritative for admin credential state, safety config, relay
  polarity, and XBee allowlists.
- If MicroSD is missing or unreadable at runtime, future firmware should serve a
  tiny embedded fallback page from flash while keeping `/api/state` available.
- A future TFT touch surface or mux-scanned input is a UI intent source only; it
  does not bypass the relay-manager and safety-supervisor command path.

## Static asset contract

Required card layout:

```text
/sdcard/www/index.html
/sdcard/www/styles.css
/sdcard/www/app.js
/sdcard/www/assets/
/sdcard/www/manifest.json
```

`manifest.json` should be small JSON and should include:

```json
{
  "name": "four-relay-admin-hmi",
  "version": "2026-05-18-admin-hmi",
  "files": ["index.html", "styles.css", "app.js"],
  "generatedAt": "2026-05-18",
  "assetRoot": "/sdcard/www"
}
```

## Log contract

Required card layout:

```text
/sdcard/logs/events/YYYY-MM-DD.jsonl
/sdcard/logs/relay/YYYY-MM-DD.jsonl
```

Each JSONL record should be one compact object. The schema is still provisional,
but the UI expects these fields when available:

```json
{
  "time": "2026-05-18T12:00:00Z",
  "type": "relay",
  "severity": "info",
  "source": "http",
  "message": "relay command rejected",
  "channel": 1,
  "result": "safety_locked"
}
```

## Required UI surfaces

- Top status rail: safety lock, hardware gate, MicroSD mount, XBee link, and
  admin state.
- Tabs: Control, Safety, Storage, XBee, Logs, and Config.
- Control: four relay cards, per-channel enabled state, per-channel toggle
  action, and the most prominent All-off action.
- Safety: safety lock status, hardware gate status, relay-expander health, mux
  health, admin provisioning status, last command metadata, and reject reason
  visibility.
- Storage: MicroSD mount state, card type, capacity, free space, asset serving
  mode, web asset manifest version, log write status, and fallback mode.
- XBee: configured state, link state, last frame/status, allowlist state, and
  read-only telemetry metadata.
- Logs: recent event records with filters for all, relay, safety, XBee,
  storage, and rejected-command events.
- Config: read-only status for admin provisioning, safety config, relay
  polarity, allowlists, asset root, log root, and firmware fallback state.

## REST contract

`GET /api/state` returns a full state snapshot and must include a `storage`
object so the HMI can render even when storage-specific endpoints fail:

```json
{
  "deviceId": "bench-four-relay-01",
  "uptimeMs": 120000,
  "safetyLocked": true,
  "adminProvisioned": false,
  "hardwareGateClosed": false,
  "relayExpander": {
    "present": false,
    "ready": false,
    "lastWrite": "none"
  },
  "mux": {
    "ready": false
  },
  "xbee": {
    "configured": false,
    "link": "unknown",
    "lastStatus": "none",
    "allowlist": "missing",
    "lastFrame": "none"
  },
  "storage": {
    "mounted": false,
    "mode": "fallback",
    "cardType": "unknown",
    "capacityBytes": 0,
    "freeBytes": 0,
    "assetRoot": "/sdcard/www",
    "assetVersion": "fallback",
    "manifestReadable": false,
    "logRoot": "/sdcard/logs",
    "logWritable": false,
    "lastLogWrite": "none",
    "fallbackActive": true
  },
  "relays": [
    {"channel": 1, "state": false, "enabled": false}
  ],
  "lastCommand": {
    "source": "boot",
    "sequence": 0,
    "result": "safe_default"
  }
}
```

`POST /api/relay/{channel}` accepts:

```json
{"state": true, "sequence": 1}
```

The public `channel` path value is `1` through `4`. Channel `0` and values
above `4` are invalid public API routes; firmware may use zero-based internal
indexes only behind the API contract.

`POST /api/all-off` accepts:

```json
{"sequence": 2}
```

`POST /api/safety-lock` accepts:

```json
{"locked": true, "sequence": 3}
```

`GET /api/storage/status` returns:

```json
{
  "mounted": true,
  "mode": "sdcard",
  "cardType": "SDHC",
  "capacityBytes": 31914983424,
  "freeBytes": 28000000000,
  "assetRoot": "/sdcard/www",
  "manifestReadable": true,
  "logRoot": "/sdcard/logs",
  "logWritable": true,
  "lastLogWrite": "2026-05-18T12:00:00Z",
  "fallbackActive": false
}
```

`GET /api/assets/manifest` returns the parsed web asset manifest:

```json
{
  "name": "four-relay-admin-hmi",
  "version": "2026-05-18-admin-hmi",
  "files": ["index.html", "styles.css", "app.js"],
  "generatedAt": "2026-05-18",
  "assetRoot": "/sdcard/www"
}
```

`GET /api/logs/recent?limit=50&type=all` returns:

```json
{
  "items": [
    {
      "time": "2026-05-18T12:00:00Z",
      "type": "relay",
      "severity": "warn",
      "source": "http",
      "message": "relay command rejected",
      "channel": 1,
      "result": "safety_locked"
    }
  ],
  "truncated": false
}
```

## Interaction rules

- Relay toggles are disabled while `safetyLocked`, `adminProvisioned` is false,
  `hardwareGateClosed` is false, required `relayExpander.ready` is false, or a
  relay card reports `enabled: false`.
- All-off remains visually available and is the most prominent state-changing
  action.
- TFT touch controls and mux-derived buttons can request all-off only through
  the same authenticated all-off endpoint or internal relay-manager command path.
- The UI must display reject reasons returned by the device without retrying a
  state-changing command automatically.
- The UI must remain usable if `/api/storage/status`, `/api/assets/manifest`,
  or `/api/logs/recent` fails; failed read-only requests must not trigger any
  state-changing retry.
- The UI must not store admin secrets in the static asset bundle.
- The Config tab is read-only for this pass; no credential entry or writeable
  hardware configuration form is approved.

## Unknowns

- Final admin token entry and provisioning workflow.
- Final captive portal behavior.
- Final endpoint authentication header or cookie format.
- Whether WebSocket updates will replace polling after firmware proof.
- Final MicroSD reader identity, card capacity, filesystem preparation process,
  low-space behavior, log rotation policy, and embedded fallback page content.
- Final relay-expander readiness semantics, readback timing, fault recovery, and
  whether a missing mux disables only TFT/touch input or also closes a broader
  hardware gate.
