# Four Relay XBee API Protocol

## Verified facts

- Digi documents XBee-PRO 900HP API mode and `AP=2` escaped API mode. Source ID:
  `SRC-DIGI-XBEE-900HP-AP`.
- Digi documents AO API Options; AO value 0 selects API Rx Indicator `0x90` for
  standard data frames. Source ID: `SRC-DIGI-XBEE-900HP-AO`.
- Digi's XBee-PRO 900HP/XSC user guide covers Transmit Request `0x10`,
  Transmit Status `0x89`, Receive Packet `0x90`, and checksum behavior. Source
  ID: `SRC-DIGI-XBEE-900HP-USER-GUIDE`.
- Digi delivery-method documentation says the TxOptions field in API mode can
  override the TO command when non-zero. Source ID:
  `SRC-DIGI-XBEE-900HP-DELIVERY`.
- Digi NP documentation reads the maximum RF payload bytes and notes encryption
  can reduce maximum payload size. Source ID: `SRC-DIGI-XBEE-900HP-NP`.
- The photo archive shows the exact radio label `XBP9B-DPUT-001 RevF` and a
  Waveshare `XBee USB Adapter` as the first PC dock candidate. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Waveshare documents the XBee USB Adapter as a UART communication board with
  XBee and USB interfaces for testing and configuring modules. Source ID:
  `SRC-WAVESHARE-XBEE-USB-ADAPTER`.

## Assumptions

- Initial payloads are compact JSON objects inside RF data, encoded as UTF-8.
- The hub/controller pairing is point-to-multipoint, aligned with the requested
  and photographed `XBP9B-DPUT-001 RevF` model.
- The controller maintains a monotonic per-source sequence window in volatile
  memory and stores allowlisted XBee source addresses in NVS.
- Initial XBee settings discovery happens through the Waveshare USB adapter
  before any ESP32-mounted carrier path is selected.

## XBee module configuration target

| Parameter | Target | Reason |
| --- | --- | --- |
| `AP` | `2` | Escaped API mode keeps control characters representable in serial data. |
| `AO` | `0` | Standard receive packets use `0x90`. |
| `EE` | `1` | AES encryption must be enabled before relay commands are accepted. |
| `KY` | Provisioned out of band | Key material must not be committed to this repository. |
| `TO` / TxOptions | Point-to-multipoint default unless a frame requires override | Matches requested part and initial topology. |

Source IDs: `SRC-DIGI-XBEE-900HP-AP`, `SRC-DIGI-XBEE-900HP-AO`,
`SRC-DIGI-XBEE-900HP-USER-GUIDE`, `SRC-DIGI-XBEE-900HP-DELIVERY`,
`SRC-DIGI-XBP9B-DPUT-001`, `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
`SRC-WAVESHARE-XBEE-USB-ADAPTER`.

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
- Verify Transmit Status `0x89` frame ID correlation.
- Verify sequence replay rejection.
- Verify each reject reason maps to an acknowledgement payload.
- Verify payload length remains under the current `NP` value after security
  settings are applied.

## Unknowns

- Final XBee baud rate.
- Final radio addresses and device ID.
- PC serial port and read-only discovery procedure for the Waveshare adapter.
- Whether the Waveshare adapter is usable only as a PC dock or as any final
  ESP32-mounted carrier path.
- Final AES key provisioning process.
- Final telemetry interval and retry policy.
- Whether payloads remain JSON or move to a binary schema after parser tests.
