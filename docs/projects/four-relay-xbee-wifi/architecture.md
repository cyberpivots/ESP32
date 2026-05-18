# Architecture

## Verified facts

- ESP-IDF stable v6.0.1 documentation identifies ESP-IDF as Espressif's official
  development framework for ESP32-series SoCs. Source ID:
  `SRC-ESP-IDF-STABLE-ESP32`.
- ESP-IDF Wi-Fi supports AP mode where stations connect to the ESP32. Source ID:
  `SRC-ESP-IDF-WIFI`.
- ESP-IDF HTTP Server provides a lightweight web server on ESP32 with URI
  handlers for HTTP methods. Source ID: `SRC-ESP-IDF-HTTP-SERVER`.
- ESP-IDF FatFS support exposes mounted FAT volumes through VFS under a mount
  path such as `/sdcard`. Source ID: `SRC-ESP-IDF-FATFS`.
- ESP-IDF SDSPI provides SD-card access over SPI with flexible GPIO-matrix pin
  routing and lower throughput than SDMMC mode. Source ID:
  `SRC-ESP-IDF-SDSPI`.
- ESP-IDF UART documentation identifies three ESP32 UART controllers. Source ID:
  `SRC-ESP-IDF-UART`.
- ESP-IDF NVS stores key-value pairs in flash. Source ID: `SRC-ESP-IDF-NVS`.
- Digi documents API mode for XBee-PRO 900HP and API mode with escaping at
  `AP=2`. Source ID: `SRC-DIGI-XBEE-900HP-AP`.
- The photo archive identifies the current physical target set as an
  ESP-WROOM-32-family development board on an ESP32 I/O expansion shield, a
  blue four-relay module with Songle `SRD-05VDC-SL-C` relay cans, a Digi
  `XBP9B-DPUT-001 RevF` radio, and a Waveshare `XBee USB Adapter`. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Espressif's ESP32-WROOM-32 datasheet provides module-level context for the
  photographed ESP-WROOM-32 module family. Source ID:
  `SRC-ESP32-WROOM-32-DATASHEET`.

## Assumptions

- The initial control surface is local-only SoftAP plus HTTP REST endpoints.
- The ESP32 owns relay state and publishes state changes over both HTTP state
  responses and XBee telemetry.
- XBee radio commands are advisory until source address allowlisting, sequence
  validation, and safety-lock checks all pass.
- The Waveshare XBee USB Adapter is used first as a PC-side configuration dock;
  final ESP32-to-XBee carrier wiring is not selected.

## Hardware target boundary

| Item | Current status | Gate |
| --- | --- | --- |
| ESP32 controller | Photographed ESP-WROOM-32 development board plus ESP32 I/O expansion shield | Board vendor/revision, shield jumper state, power path, and GPIO continuity verification |
| Relay module | Photographed four-channel board with Songle `SRD-05VDC-SL-C` relay cans | Trigger polarity, input current, 3.3 V compatibility, `JD-VCC`/`VCC` behavior, and isolation verification |
| XBee radio | Photographed Digi `XBP9B-DPUT-001 RevF` | Read-only settings discovery, address allowlist, AES setup plan, and antenna/regulatory review |
| XBee dock | Photographed Waveshare XBee USB Adapter | PC serial detection, adapter voltage, DIN/DOUT routing, reset/sleep/flow-control verification |

Source IDs: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
`SRC-ESP32-WROOM-32-DATASHEET`, `SRC-SONGLE-SRD-05VDC-SL-C`,
`SRC-WAVESHARE-XBEE-USB-ADAPTER`, `SRC-DIGI-XBP9B-DPUT-001`.

## Components

| Component | Responsibility | Source IDs |
| --- | --- | --- |
| Relay state manager | Maintains desired relay state, safety lock, boot defaults, and all-off transition. | `SRC-ESP-IDF-GPIO` |
| HTTP control surface | Serves static UI and REST endpoints for state, relay changes, all-off, and safety lock. | `SRC-ESP-IDF-HTTP-SERVER`, `SRC-ESP-IDF-WIFI` |
| MicroSD asset store | Provides `/sdcard/www` static assets and `/sdcard/logs` event-log storage after SDSPI and FatFS/VFS mount succeeds. | `SRC-ESP-IDF-FATFS`, `SRC-ESP-IDF-SDSPI`, `SRC-ESP-IDF-SDMMC`, `SRC-ESP-IDF-SDSPI-EXAMPLE` |
| XBee transport | Encodes/decodes escaped API frames and carries telemetry/control payloads. | `SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`, `SRC-DIGI-XBEE-900HP-USER-GUIDE` |
| Credential/config store | Stores admin token/passphrase state, allowlisted radio addresses, relay polarity, and boot policy. | `SRC-ESP-IDF-NVS` |
| Safety supervisor | Forces all relays off on boot, invalid command, safety-lock close, watchdog/reset recovery, or config error. | unresolved design requirement |

## REST endpoints

| Endpoint | Method | State-changing | Gate |
| --- | --- | --- | --- |
| `/api/state` | `GET` | No | None |
| `/api/relay/{channel}` | `POST` | Yes | Admin credential in NVS and safety lock open |
| `/api/all-off` | `POST` | Yes | Always allowed once HTTP request is authenticated |
| `/api/safety-lock` | `POST` | Yes | Admin credential in NVS |
| `/api/storage/status` | `GET` | No | None |
| `/api/assets/manifest` | `GET` | No | None |
| `/api/logs/recent` | `GET` | No | None |

## Static asset and log storage

The future ESP-IDF implementation should mount the MicroSD card at `/sdcard`,
serve the static admin HMI from `/sdcard/www`, and append JSONL event logs under
`/sdcard/logs`. NVS remains authoritative for admin credential state, relay
polarity, safety settings, and XBee allowlists.

If the MicroSD card is missing or the asset manifest cannot be read, the HTTP
surface should still expose `/api/state` and a small embedded fallback page.
That fallback is a future firmware item; this pass only documents and mocks the
behavior.

Source IDs: `SRC-ESP-IDF-FATFS`, `SRC-ESP-IDF-SDSPI`,
`SRC-ESP-IDF-HTTP-SERVER`, `SRC-ESP-IDF-RESTFUL-SERVER-EXAMPLE`,
`SRC-ESP-IDF-NVS`.

## XBee telemetry flow

1. Firmware snapshots relay state, safety lock state, uptime, link state, and
   last command metadata.
2. XBee transport serializes the snapshot into the project status message.
3. Transport sends a Digi API Transmit Request `0x10` to an allowlisted
   destination or hub address.
4. Transmit Status `0x89` updates the link status field when a matching frame ID
   is returned.

Source IDs: `SRC-DIGI-XBEE-900HP-USER-GUIDE`,
`SRC-DIGI-XBEE-900HP-DELIVERY`.

## XBee command flow

1. UART frame parser accepts only escaped API frames when the module is
   configured for `AP=2`.
2. Receive Packet `0x90` is decoded when AO is 0.
3. Source 64-bit address is checked against the NVS allowlist.
4. Payload schema, sequence number, target channel, and requested state are
   validated.
5. Safety supervisor rejects unsafe changes before relay state changes.
6. Firmware returns an acknowledgement or reject message.

Source IDs: `SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`,
`SRC-DIGI-XBEE-900HP-USER-GUIDE`, `SRC-ESP-IDF-NVS`.

## Unknowns

- Final power tree and relay current budget.
- Final relay trigger polarity.
- Final XBee serial baud rate and flow-control use.
- Final REST authentication format.
- Final telemetry interval and backoff policy.
- Final MicroSD reader identity, wiring, card preparation, log rotation,
  low-space policy, and embedded fallback-page implementation.
