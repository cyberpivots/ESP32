# Source Ledger - 2026-05-18 Initial Scaffold

## Scope

Initial source-backed scaffold for ESP32 workspace governance, model routing,
and seed hardware profiles.

## Verified findings

- OpenAI latest-model guidance identifies `gpt-5.5` and recommends tuning
  reasoning effort by workload.
- Espressif documentation identifies ESP-IDF as the official development
  framework for ESP32-series SoCs.
- Digi model page identifies `XBP9B-DPUT-001` as an XBee-PRO 900HP S3B
  Point2Multipoint 900 MHz, 250 mW, U.FL, 10 kbps part.
- Heltec product documentation exists for WiFi LoRa 32(V2), but physical board
  revision must be checked before pin-level claims.

## Unresolved

- Exact relay board models and electrical characteristics.
- Exact Heltec board revision on hand.
- XBee carrier/adapter hardware and host interface wiring.
- First firmware framework and build system.

