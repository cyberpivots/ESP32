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
- The historical 2026-05-18 shell probe found Python 3.12.3 and Git 2.43.0;
  `idf.py`, `esptool.py`, CMake, Ninja, and XCTU were not found on PATH.
  Source ID: `SRC-LOCAL-TOOLCHAIN-PROBE-2026-05-18`.
- The 2026-05-21 live-bench cycle installed EIM CLI v0.12.3 under
  `/home/cyber/.local/opt/eim-v0.12.3/eim`, installed ESP-IDF v6.0.1 under
  `/home/cyber/Espressif/v6.0.1/esp-idf`, and created activation script
  `/home/cyber/.espressif/tools/activate_idf_v6.0.1.sh`. Source IDs:
  `SRC-EIM-CLI-DOCS`, `SRC-EIM-RELEASE-V0-12-3`,
  `SRC-LOCAL-LIVE-BENCH-PREFLIGHT-2026-05-21`.
- After sourcing the activation script, `idf.py --version` reported
  `ESP-IDF v6.0.1`, `git describe` in `IDF_PATH` reported `v6.0.1`, Python
  reported `3.12.3`, and `xtensa-esp32-elf-gcc` reported
  `15.2.0`. Source ID: `SRC-LOCAL-LIVE-BENCH-PREFLIGHT-2026-05-21`.
- The disabled `four-relay-xbee-wifi` skeleton built with
  `idf.py -C firmware/projects/four-relay-xbee-wifi build`. The build
  generated ignored `sdkconfig` and `build/` artifacts and did not flash or
  monitor the board. Source IDs: `SRC-ESP-IDF-START-PROJECT`,
  `SRC-LOCAL-LIVE-BENCH-PREFLIGHT-2026-05-21`.
- EIM could not copy OpenOCD udev rules to `/etc/udev/rules.d/` without
  elevated permissions. This is not required for the no-flash build, but it
  remains a blocker for any future OpenOCD/JTAG gate until handled separately.
  Source ID: `SRC-LOCAL-LIVE-BENCH-PREFLIGHT-2026-05-21`.

## Required tools before firmware implementation

| Tool | Purpose | Current shell status |
| --- | --- | --- |
| ESP-IDF v6.0.1 | Project firmware framework target. | Installed under `/home/cyber/Espressif/v6.0.1/esp-idf`; activation script reports `ESP-IDF v6.0.1`. |
| ESP-IDF Installation Manager | Install/manage ESP-IDF and toolchain. | EIM CLI v0.12.3 installed at `/home/cyber/.local/opt/eim-v0.12.3/eim`; not on default PATH. |
| `idf.py` | Build, flash, monitor workflow entry point. | Available after `source /home/cyber/.espressif/tools/activate_idf_v6.0.1.sh`; not on default PATH. |
| CMake | ESP-IDF build generator dependency. | Default shell reports 3.28.3; EIM also installed 4.0.3 under the user tool cache. |
| Ninja | ESP-IDF build backend dependency. | Default shell reports 1.11.1; EIM also installed 1.12.1 under the user tool cache. |
| esptool | Flashing and chip communication utility. | Windows `C:\Python314\Scripts\esptool.exe` reports v5.2.0; ESP-IDF build uses bundled esptool output but flashing remains blocked. |
| Python | ESP-IDF tooling runtime. | Python 3.12.3 found and used by the ESP-IDF v6.0.1 environment. |
| Git | Source checkout and version operations. | Git 2.43.0 found; `IDF_PATH` describes as `v6.0.1`. |
| Digi XBee Studio or XCTU | XBee discovery/configuration and API frame inspection. | XCTU not found on PATH. |
| Waveshare XBee USB Adapter | XBee PC configuration/debug dock candidate. | Photographed; serial port and voltage path not verified. |
| Final ESP32 XBee carrier | XBee bench connection to controller. | Not selected. |
| Multimeter | Voltage and continuity checks. | Not verified. |
| Bench supply | Current-limited power testing. | Not verified. |
| Logic analyzer | UART/API-frame observation. | Not verified. |
| Browser dev tools | Local UI debug. | Not verified. |
| `curl` | REST endpoint smoke tests. | Not verified. |

## Deferred commands

- `idf.py flash` and `idf.py monitor` wait until board identity, power, boot
  mode, and relay isolation gates are closed.
- XBee configuration writes wait until read-only adapter discovery, current
  settings backup, carrier/adapter identity, and radio addresses are documented.

## Unknowns

- Which serial port maps to the photographed ESP-WROOM-32 development board.
- Which serial port maps to the Waveshare XBee USB Adapter.
- Whether Digi XBee Studio or XCTU is preferred for this bench.
- Whether to add the local EIM binary or activation script to a persistent shell
  profile; current evidence uses explicit `source ...activate_idf_v6.0.1.sh`.
- OpenOCD udev-rule installation for future JTAG/OpenOCD workflows.
