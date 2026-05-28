# Device Matrix

| Device family | Initial target | Source status | Profile status |
| --- | --- | --- | --- |
| ESP32 boards | Photographed ESP-WROOM-32 development board plus ESP32 I/O expansion shield for `four-relay-xbee-wifi`; DevKitC retained as prior reference | Photo-backed module/shield identity plus source-backed ESP32-WROOM-32 docs and hardware-design guidelines; third-party shield page is candidate evidence only | Project pin map remains provisional until board/shield routing, power, and boot-pin risks are verified |
| Storage | Generic SPI MicroSD reader for `four-relay-xbee-wifi` static assets and logs | ESP-IDF FatFS/VFS, SDSPI, SD/MMC, HTTP server, and example docs support the planned storage/web-serving architecture; no exact reader is identified | Wiring is blocked until reader identity, 3.3 V power, pull-ups, shield continuity, and boot-pin risks are verified |
| Display | User-requested Open-Smart R61509V TFT planning target | External R61509V references provide parallel-TFT pin-pressure context only | Exact module, pinout, power/backlight, touch interface, and driver path are unresolved |
| Remote LCD client display | 20x4 I2C LCD requested for `remote-lcd-xbee-solar-client` | PCF8574/74A source is candidate/reference-only for an I2C expander class; no exact LCD/backpack is verified | Exact LCD module, controller, backpack IC, I2C address, pullups, logic voltage, backlight current, and enclosure fit are unresolved |
| Remote LCD client input | Rotary encoder requested for `remote-lcd-xbee-solar-client` | Bourns PEC11R source is candidate/reference-only for an encoder family; no exact encoder is verified | Exact encoder part, PPR, detents, switch option, pullups, debounce, voltage, and boot-pin impact are unresolved |
| Remote LCD client power | 18650 cell, BMS/protection, solar charger/power path requested for `remote-lcd-xbee-solar-client` | TI BQ25185, BQ2970, BQ27441-G1, and UL lithium-ion safety guidance are candidate/reference-only or broad safety context; no exact power hardware is verified | Exact cell, BMS board, panel, charger module, current limits, charge voltage, protection, enclosure, and power budget are unresolved |
| Interface expansion | CD74HC4067 input mux plus MCP23017/TCA9555 relay expander candidates | TI and Espressif sources cover component classes; exact breakout/board selection is unresolved | Mux is input-only; relay expander proof starts with LEDs or logic analyzer, not relay inputs |
| XBee | Digi `XBP9B-DPUT-001 RevF` with Waveshare XBee USB Adapter as first PC dock | Photo-backed exact radio label; source-backed part ID, adapter docs, and API-mode docs | PC dock read-only discovery only; needs adapter voltage, DIN/DOUT, carrier, address, and configuration validation before writes or ESP32 wiring |
| Relay boards | Four-channel module populated with Songle `SRD-05VDC-SL-C` relays for first project; 1/8/16 channel future profiles | Photo-backed relay can identity plus Songle relay component source | Four-channel profile is verification-only; module trigger/isolation behavior and direct-GPIO 3.3 V/current gate unresolved |
| Heltec | WiFi LoRa 32(V2) | Product-level source | Needs physical revision validation |
| Fabrication printer - smaller engineering parts | User-stated Creality K1 with user-stated hardened-nozzle upgrade | Official K1 support specs cover FFF/CoreXY, direct-drive extrusion, 0.4 mm nozzle, nozzle temperature below 300 C, heatbed below 100 C, and listed engineering/CF filament families; hardened-nozzle upgrade is not locally verified | Default only for smaller brackets, fixtures, cable anchors, and engineering-material trials after nozzle, SDS, ventilation, drying, and calibration evidence |
| Fabrication printer - large parts | User-stated Anycubic Kobra 2 Max | Official Anycubic Kobra 2 Max records cover 420 x 420 x 500 mm volume and PLA/ABS/PETG/TPU support | Default only for large enclosures, panels, and jigs after bed calibration, adhesion proof, material profile, and ventilation decision |
| Fabrication printer - batch/long parts | User-stated Creality CR-30 | Official Creality CR-30 records identify the printer as a 3DPrintMill / infinite-Z belt printer for batch and long-model production | Use only after belt adhesion, slicer-angle, calibration, first-article, and continuous-run stop-rule proof |
| 3D scanning | User-stated Creality CR-Scan Lizard | Official Creality materials claim 0.05 mm precision and STL/OBJ/PLY output | Fit/reference scans only; dimensional evidence requires known-dimension or caliper validation before use in CAD acceptance |

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
- Display: `SRC-NOPNOP2002-ESP-IDF-PARALLEL-TFT`,
  `SRC-LCDWIKI-R61509V-MRB2802`
- Remote LCD client display: `SRC-NXP-PCF8574-74A`,
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`,
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-PRIVATE-SUBMODULES-2026-05-26`
- Remote LCD client input: `SRC-BOURNS-PEC11R`,
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`,
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-PRIVATE-SUBMODULES-2026-05-26`
- Remote LCD client power: `SRC-TI-BQ25185`, `SRC-TI-BQ2970`,
  `SRC-TI-BQ27441-G1`, `SRC-UL-LIION-SAFETY`,
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`,
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-PRIVATE-SUBMODULES-2026-05-26`
- Remote LCD client ESP32 node: `SRC-ESP-IDF-GPIO`, `SRC-ESP-IDF-UART`,
  `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`,
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-SCAFFOLD-2026-05-26`,
  `SRC-LOCAL-REMOTE-LCD-XBEE-SOLAR-CLIENT-PRIVATE-SUBMODULES-2026-05-26`
- Interface expansion: `SRC-TI-CD74HC4067`, `SRC-TI-TCA9555`,
  `SRC-ESPRESSIF-MCP23017-COMPONENT`, `SRC-TI-TPIC6B595`
- XBee: `SRC-DIGI-XBP9B-DPUT-001`, `SRC-DIGI-XBEE-PRO-900HP`,
  `SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`,
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
  `SRC-WAVESHARE-XBEE-USB-ADAPTER`
- Relay boards: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
  `SRC-SONGLE-SRD-05VDC-SL-C`, `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`; exact
  module schematic/source remains unresolved
- Fabrication and scanning: `SRC-LOCAL-HARDWARE-RAPID-PROTOTYPING-2026-05-28`,
  `SRC-CREALITY-K1-SUPPORT-2026-05-28`,
  `SRC-ANYCUBIC-KOBRA2-MAX-2026-05-28`, `SRC-CREALITY-CR30-2026-05-28`,
  `SRC-CREALITY-CR-SCAN-LIZARD-2026-05-28`,
  `SRC-NIOSH-SAFE-3D-PRINTING-2024-103`,
  `SRC-PRUSA-FILAMENT-MATERIAL-GUIDE-2026-05-28`,
  `SRC-BAMBULAB-PA6-CF-2026-05-28`
- CAD and fit workflow: `SRC-OPENSCAD-DOCS-2026-05-28`,
  `SRC-CADQUERY-DOCS-2026-05-28`,
  `SRC-FREECAD-FEATURES-2026-05-28`,
  `SRC-KICAD9-PCBNEW-3D-EXPORT-2026-05-28`

## Unknowns

- Mains readiness is hard blocked until load type, enclosure, overcurrent
  protection, grounding/bonding, strain relief, GFCI/de-energization,
  separation, labels/disconnect, and qualified review evidence exist. Source
  IDs: `SRC-NIOSH-ELECTRICAL-SAFETY`, `SRC-OSHA-DEENERGIZED-WORK`,
  `SRC-OSHA-GFCI`, `SRC-OSHA-AEGCP`, `SRC-OSHA-GROUNDING-OVERCURRENT`,
  `SRC-NEMA-ENCLOSURES`.
- 3D-printing and scanner readiness is blocked until local equipment identity,
  K1 hardened-nozzle proof, filament SDS, dry-state/humidity record,
  ventilation/exposure controls, printer/material calibration coupons, CR-30
  belt proof, CR-Scan Lizard known-dimension validation, and lane-specific
  measurements are recorded. Source IDs:
  `SRC-LOCAL-HARDWARE-RAPID-PROTOTYPING-2026-05-28`,
  `SRC-NIOSH-SAFE-3D-PRINTING-2024-103`.
