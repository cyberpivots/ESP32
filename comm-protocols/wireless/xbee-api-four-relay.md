# Four Relay XBee API Protocol

## Verified facts

- Digi documents XBee-PRO 900HP API mode and `AP=2` escaped API mode. Source ID:
  `SRC-DIGI-XBEE-900HP-AP`.
- Digi documents AO API Options; AO value 0 selects API Rx Indicator `0x90` for
  standard data frames. Source ID: `SRC-DIGI-XBEE-900HP-AO`.
- Digi's XBee-PRO 900HP/XSC user guide covers Transmit Request `0x10`,
  Extended Transmit Status `0x8B`, Receive Packet `0x90`, and checksum
  behavior. Source ID:
  `SRC-DIGI-XBEE-900HP-USER-GUIDE-REFRESH-2026-06-05`.
- Digi delivery-method documentation says the TxOptions field in API mode can
  override the TO command when non-zero. Source ID:
  `SRC-DIGI-XBEE-900HP-DELIVERY`.
- Digi TO documentation records the 10k product default as `0x40` and says
  DigiMesh bits are not available on the 10k build. Source ID:
  `SRC-DIGI-XBEE-900HP-TO-2026-06-05`.
- Digi NP documentation reads the maximum RF payload bytes and notes encryption
  can reduce maximum payload size. Source ID: `SRC-DIGI-XBEE-900HP-NP`.
- The photo archive shows the exact radio label `XBP9B-DPUT-001 RevF` and a
  Waveshare `XBee USB Adapter` as the first PC dock candidate. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Waveshare documents the XBee USB Adapter as a UART communication board with
  XBee and USB interfaces for testing and configuring modules. Source ID:
  `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- Relay-expander and mux health fields are part of the project state contract.
  Source IDs for the underlying hardware planning branch: `SRC-TI-TCA9555`,
  `SRC-ESPRESSIF-MCP23017-COMPONENT`, `SRC-TI-CD74HC4067`.

## Assumptions

- Initial payloads are compact JSON objects inside RF data, encoded as UTF-8.
- The hub/controller pairing is point-to-multipoint, aligned with the requested
  and photographed `XBP9B-DPUT-001 RevF` model.
- The controller maintains a monotonic per-source sequence window in volatile
  memory and stores allowlisted XBee source addresses in NVS.
- Initial XBee settings discovery happens through the Waveshare USB adapter
  before any ESP32-mounted carrier path is selected.

## XBee module configuration target

The table below is a future configuration target, not an approval to write
settings during bench discovery. The current bench path is
[XBee read-only discovery](../../docs/projects/four-relay-xbee-wifi/xbee-read-only-bench-proof.md):
passive discovery first, then explicitly confirmed AT reads for `VR`, `HV`,
`SH`, `SL`, `AP`, `AO`, `BD`, and `NP`.

| Parameter | Target | Reason |
| --- | --- | --- |
| `AP` | `2` | Escaped API mode keeps control characters representable in serial data. |
| `AO` | `0` | Standard receive packets use `0x90`. |
| `EE` | `1` | AES encryption must be enabled before relay commands are accepted. |
| `KY` | Provisioned out of band | Key material must not be committed to this repository. |
| `TO` / TxOptions | Point-to-multipoint default unless a frame requires override | Matches requested 10k part and initial topology; DigiMesh remains blocked without variant proof. |

Source IDs: `SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`,
`SRC-DIGI-XBEE-900HP-USER-GUIDE-REFRESH-2026-06-05`,
`SRC-DIGI-XBEE-900HP-DELIVERY`, `SRC-DIGI-XBEE-900HP-TO-2026-06-05`,
`SRC-DIGI-XBP9B-DPUT-001`, `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
`SRC-WAVESHARE-XBEE-USB-ADAPTER`.

## Hub-spoke host-only planning matrix

The checked-in hub-spoke planning surface is host-only. It models one hub and
at least 10 redacted spoke aliases using synthetic `0x90` receive and `0x8B`
status metadata. It does not open serial ports, launch XCTU or XBee Studio,
build live API transmit frames, transmit RF, write settings, flash firmware, or
touch relay/load/mains paths.

Additional use cases accepted for host-only planning:

1. BBS custody acknowledgement backhaul.
2. Remote node heartbeat/status rollup.
3. Direct low-bandwidth BBS message exchange.
4. Packetized bulletin or small-file queue metadata.
5. Remote LCD field-console status feed.
6. Service catalog and capability report sideband.
7. Commissioning/link-probe and profile-readback evidence lane.
8. Remote telemetry snapshots from field spokes.
9. Hardware Tools saved-evidence analysis.
10. Non-executing control-intent audit trail.
11. Hub-spoke lock/safety-state broadcast.
12. Remote solar-client health beacon.

Source IDs: `SRC-DIGI-XBP9B-DPUT-001`,
`SRC-DIGI-XBEE-900HP-USER-GUIDE-REFRESH-2026-06-05`,
`SRC-DIGI-XBEE-900HP-TO-2026-06-05`,
`SRC-LOCAL-XBEE-HUB-SPOKE-HOST-PLAN-2026-06-05`.

## Device status message

Direction: controller to hub.

Frame: Transmit Request `0x10`.

Payload:

```json
{
  "type": "status",
  "device": "bench-four-relay-01",
  "seq": 42,
  "uptime_ms": 120000,
  "safety_locked": true,
  "hardware_gate_closed": false,
  "relay_expander": {
    "present": false,
    "ready": false,
    "last_write": "none"
  },
  "mux": {
    "ready": false
  },
  "relays": [false, false, false, false],
  "last_command": {
    "source": "http",
    "seq": 12,
    "result": "accepted"
  }
}
```

## Relay command message

Direction: hub to controller.

Frame: Receive Packet `0x90` after the remote sends Transmit Request `0x10`.

Payload:

```json
{
  "type": "relay_set",
  "device": "bench-four-relay-01",
  "seq": 43,
  "channel": 1,
  "state": true
}
```

Validation:

- `type` must be `relay_set`.
- `device` must match local configured device ID.
- `seq` must be newer than the accepted per-source sequence.
- `channel` must be 1 through 4.
- Source 64-bit address from the `0x90` frame must be allowlisted.
- AES/security configuration must be complete.
- Safety lock must be open.
- Hardware gate must be closed.
- If the selected relay path requires an expander, relay expander health must be
  ready.
- Relay polarity configuration must be valid.

## All-off command message

Direction: hub to controller.

Payload:

```json
{
  "type": "all_off",
  "device": "bench-four-relay-01",
  "seq": 44
}
```

All-off still requires an allowlisted source and valid sequence. It should remain
available when the safety lock is closed.

## Acknowledgement message

Direction: controller to hub.

Payload:

```json
{
  "type": "ack",
  "device": "bench-four-relay-01",
  "seq": 43,
  "accepted": true,
  "relays": [true, false, false, false]
}
```

Reject payload:

```json
{
  "type": "ack",
  "device": "bench-four-relay-01",
  "seq": 43,
  "accepted": false,
  "reason": "safety_locked"
}
```

## Reject reasons

- `source_not_allowed`
- `sequence_replay`
- `payload_invalid`
- `device_mismatch`
- `channel_invalid`
- `safety_locked`
- `hardware_gate_open`
- `relay_config_missing`
- `security_not_configured`
- `xbee_frame_invalid`

## Parser test plan

- Verify escaped `AP=2` delimiter, escape, XON, and XOFF handling.
- Verify checksum failure rejects frame without state change.
- Verify Receive Packet `0x90` source address extraction.
- Verify Extended Transmit Status `0x8B` frame ID correlation for `0x10`
  transmit requests.
- Verify sequence replay rejection.
- Verify each reject reason maps to an acknowledgement payload.
- Verify payload length remains under the current `NP` value after security
  settings are applied.
- Verify `relay_expander` and `mux` health fields remain informational in status
  messages and never authorize relay state changes by themselves.
- Verify expander failure maps relay commands to `hardware_gate_open`.

## Unknowns

- Final XBee baud rate.
- Final radio addresses and device ID.
- PC serial port and read-only discovery procedure for the Waveshare adapter.
- Whether the Waveshare adapter is usable only as a PC dock or as any final
  ESP32-mounted carrier path.
- Whether Tier B AT read-query discovery can complete cleanly through the
  current adapter without any setting writes.
- Final AES key provisioning process.
- Final telemetry interval and retry policy.
- Whether payloads remain JSON or move to a binary schema after parser tests.
