# Initial Communication Scope

## Planned transports

- UART and USB serial for flashing/debugging and module communication.
- Wi-Fi and BLE where board support is verified.
- LoRa where Heltec board revision and radio chip are verified.
- XBee Point2Multipoint where radio settings, PC dock, and final
  carrier/interface hardware are verified.
- Custom message protocols after protocol contracts are written.

## Current status

No protocol implementation exists.

The first written protocol contract is
`comm-protocols/wireless/xbee-api-four-relay.md` for the
`four-relay-xbee-wifi` design package.

Source IDs: `SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`,
`SRC-DIGI-XBEE-900HP-USER-GUIDE`,
`SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
`SRC-WAVESHARE-XBEE-USB-ADAPTER`.

## Current XBee dock evidence

The photo archive identifies a Waveshare `XBee USB Adapter` as the first
PC-side configuration/debug dock candidate. It is not approved as the final
ESP32-mounted carrier until UART voltage, DIN/DOUT routing, power path, and
control pins are verified.

Source IDs: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
`SRC-WAVESHARE-XBEE-USB-ADAPTER`.
