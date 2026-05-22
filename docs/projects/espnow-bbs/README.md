# ESP-NOW BBS Coordinator and Client Firmware

Source index: [../../../knowledge-base/source-index.md](../../../knowledge-base/source-index.md)

## Purpose

This project lane supports the DOS-C off-grid BBS architecture:

`Windows 3.1 dashboard -> DOSBox-X/NETTSR -> Raspberry Pi bridge -> USB serial -> ESP32 coordinator -> ESP-NOW clients`

The ESP32 firmware responsibility is limited to the coordinator and client
radio/device behavior. Durable BBS storage, sysop UI, and firmware management
remain outside the ESP32 firmware image.

## Firmware Roles

- Coordinator: USB serial command endpoint, ESP-NOW peer table, channel/key
  policy, ACK/retry handling, duplicate suppression, TTL enforcement, and
  compact telemetry back to the Pi bridge.
- Client: provisioned identity, bounded receive/send queues, app-level ACKs,
  diagnostics, firmware version reporting, and store-and-forward message
  handling.

## Safety Boundaries

- This lane does not control relays, XBee modules, mains/load wiring, or SD
  imaging.
- The current COM6 DevKitC-class board is only a candidate coordinator until
  physical carrier-board inspection and flash/recovery evidence are recorded.
- Firmware flashing requires a separate explicit gate and recovery plan.

## Implementation Order

1. Close the DOS-C SLIRP receive blocker or keep using host-only bridge tests.
2. Record ESP-IDF v6.0.1 toolchain evidence.
3. Record first flash target and recovery method.
4. Implement coordinator USB serial identity/diagnostic firmware.
5. Add ESP-NOW ping/ACK between one coordinator and one client.
6. Add chunked message delivery and custody telemetry.
7. Add provisioning and firmware inventory flows.
