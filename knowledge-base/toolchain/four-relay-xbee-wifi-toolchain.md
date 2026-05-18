# Four Relay XBee Wi-Fi Toolchain

## Verified facts

- ESP-IDF Get Started documentation for stable v6.0.1 lists the required
  software categories as ESP32 toolchain, CMake, Ninja, ESP-IDF, and scripts to
  operate the toolchain. Source ID: `SRC-ESP-IDF-GET-STARTED`.
- ESP-IDF Get Started documentation describes ESP-IDF Installation Manager
  options, including GUI and CLI. Source ID: `SRC-ESP-IDF-GET-STARTED`.
- Digi XCTU is a free multi-platform application for XBee/RF solutions and
  includes an API Frame Builder. Source ID: `SRC-DIGI-XCTU`.
- The photo archive identifies a Waveshare `XBee USB Adapter` as the first
  PC-side XBee configuration/debug dock candidate. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Waveshare documents the XBee USB Adapter as a UART communication board with
  USB and XBee interfaces. Source ID: `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- Current shell probe found Python 3.12.3 and Git 2.43.0; `idf.py`,
  `esptool.py`, CMake, Ninja, and XCTU were not found on PATH. Source ID:
  `SRC-LOCAL-TOOLCHAIN-PROBE-2026-05-18`.

## Required tools before firmware implementation

| Tool | Purpose | Current shell status |
| --- | --- | --- |
| ESP-IDF v6.0.1 | Project firmware framework target. | Not found through `idf.py`. |
| ESP-IDF Installation Manager | Install/manage ESP-IDF and toolchain. | Not verified. |
| `idf.py` | Build, flash, monitor workflow entry point. | Not found on PATH. |
| CMake | ESP-IDF build generator dependency. | Not found on PATH. |
| Ninja | ESP-IDF build backend dependency. | Not found on PATH. |
| esptool | Flashing and chip communication utility. | `esptool.py` not found on PATH. |
| Python | ESP-IDF tooling runtime. | Python 3.12.3 found. |
| Git | Source checkout and version operations. | Git 2.43.0 found. |
| Digi XBee Studio or XCTU | XBee discovery/configuration and API frame inspection. | XCTU not found on PATH. |
| Waveshare XBee USB Adapter | XBee PC configuration/debug dock candidate. | Photographed; serial port and voltage path not verified. |
| Final ESP32 XBee carrier | XBee bench connection to controller. | Not selected. |
| Multimeter | Voltage and continuity checks. | Not verified. |
| Bench supply | Current-limited power testing. | Not verified. |
| Logic analyzer | UART/API-frame observation. | Not verified. |
| Browser dev tools | Local UI debug. | Not verified. |
| `curl` | REST endpoint smoke tests. | Not verified. |

## Deferred commands

- `idf.py build` waits until ESP-IDF v6.0.1 is installed and firmware source
  exists.
- `idf.py flash` and `idf.py monitor` wait until board identity, power, boot
  mode, and relay isolation gates are closed.
- XBee configuration writes wait until read-only adapter discovery, current
  settings backup, carrier/adapter identity, and radio addresses are documented.

## Unknowns

- Whether ESP-IDF should be installed in Windows, WSL, or both.
- Which serial port maps to the photographed ESP-WROOM-32 development board.
- Which serial port maps to the Waveshare XBee USB Adapter.
- Whether Digi XBee Studio or XCTU is preferred for this bench.
