# Device Matrix

| Device family | Initial target | Source status | Profile status |
| --- | --- | --- | --- |
| ESP32 boards | Photographed ESP-WROOM-32 development board plus ESP32 I/O expansion shield for `four-relay-xbee-wifi`; DevKitC retained as prior reference | Photo-backed module/shield identity plus source-backed ESP32-WROOM-32 docs and hardware-design guidelines; third-party shield page is candidate evidence only | Project pin map remains provisional until board/shield routing, power, and boot-pin risks are verified |
| Storage | Generic SPI MicroSD reader for `four-relay-xbee-wifi` static assets and logs | ESP-IDF FatFS/VFS, SDSPI, SD/MMC, HTTP server, and example docs support the planned storage/web-serving architecture; no exact reader is identified | Wiring is blocked until reader identity, 3.3 V power, pull-ups, shield continuity, and boot-pin risks are verified |
| XBee | Digi `XBP9B-DPUT-001 RevF` with Waveshare XBee USB Adapter as first PC dock | Photo-backed exact radio label; source-backed part ID, adapter docs, and API-mode docs | PC dock read-only discovery only; needs adapter voltage, DIN/DOUT, carrier, address, and configuration validation before writes or ESP32 wiring |
| Relay boards | Four-channel module populated with Songle `SRD-05VDC-SL-C` relays for first project; 1/8/16 channel future profiles | Photo-backed relay can identity plus Songle relay component source | Four-channel profile is verification-only; module trigger/isolation behavior and direct-GPIO 3.3 V/current gate unresolved |
| Heltec | WiFi LoRa 32(V2) | Product-level source | Needs physical revision validation |

## Source IDs

- ESP32 photographed target: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
  `SRC-ESP32-WROOM-32-DATASHEET`, `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`,
  `SRC-ESP32-IO-SHIELD-CANDIDATE`, `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-UART`
- ESP32 DevKitC reference: `SRC-ESP32-DEVKITC`, `SRC-ESP-IDF-GPIO`,
  `SRC-ESP-IDF-UART`
- Storage: `SRC-ESP-IDF-FATFS`, `SRC-ESP-IDF-SDSPI`,
  `SRC-ESP-IDF-SDMMC`, `SRC-ESP-IDF-SD-PULLUP`,
  `SRC-ESP-IDF-HTTP-SERVER`, `SRC-ESP-IDF-RESTFUL-SERVER-EXAMPLE`,
  `SRC-ESP-IDF-SDSPI-EXAMPLE`
- XBee: `SRC-DIGI-XBP9B-DPUT-001`, `SRC-DIGI-XBEE-PRO-900HP`,
  `SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`,
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
  `SRC-WAVESHARE-XBEE-USB-ADAPTER`
- Relay boards: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
  `SRC-SONGLE-SRD-05VDC-SL-C`, `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`; exact
  module schematic/source remains unresolved

## Unknowns

- Mains readiness is hard blocked until load type, enclosure, overcurrent
  protection, grounding/bonding, strain relief, GFCI/de-energization,
  separation, labels/disconnect, and qualified review evidence exist. Source
  IDs: `SRC-NIOSH-ELECTRICAL-SAFETY`, `SRC-OSHA-DEENERGIZED-WORK`,
  `SRC-OSHA-GFCI`, `SRC-OSHA-AEGCP`, `SRC-OSHA-GROUNDING-OVERCURRENT`,
  `SRC-NEMA-ENCLOSURES`.
