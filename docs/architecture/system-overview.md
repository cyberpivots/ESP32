# System Overview

This workspace is organized around reusable device modules:

- board profiles,
- firmware interfaces,
- communication protocols,
- web or HTML control surfaces,
- verification and release gates,
- multi-agent knowledge capture.

The initial scaffold separates architecture and evidence from implementation so
future firmware can target multiple ESP32 boards without premature framework
coupling.

## Active project

The first project package is `four-relay-xbee-wifi`, a design-only package for
the photographed ESP-WROOM-32 development board plus ESP32 I/O expansion shield,
a four-channel Songle relay module candidate, Digi XBee-PRO 900HP S3B
`XBP9B-DPUT-001 RevF`, a Waveshare XBee USB Adapter PC dock, and local Wi-Fi
control surface. ADR-0002 accepts ESP-IDF stable v6.0.1 for that project only.

Source IDs: `SRC-ESP-IDF-STABLE-ESP32`,
`SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
`SRC-ESP32-WROOM-32-DATASHEET`, `SRC-DIGI-XBP9B-DPUT-001`,
`SRC-WAVESHARE-XBEE-USB-ADAPTER`, `SRC-SONGLE-SRD-05VDC-SL-C`.
