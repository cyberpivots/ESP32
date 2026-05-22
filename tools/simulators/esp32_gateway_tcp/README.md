# ESP32 Gateway TCP Simulator

Simulator-only bridge for the DOS-C Windows 3.1 operator console.

## Protocol

- TCP port: `31331`.
- Framing: newline-delimited ASCII JSON.
- Maximum line length: 512 bytes before the newline.
- Messages accepted: `hello`, `ping`, `state_get`, and visible-but-disabled
  `relay_set`.
- Messages emitted: `ack`, `state`, and `error`.
- Relay public channels are `1..4`.
- `relay_set` returns `control_disabled` in v1.

## Run

```bash
python3 tools/simulators/esp32_gateway_tcp/esp32_gateway_sim.py --host 127.0.0.1 --port 31331
```

The simulator does not flash firmware, write relay GPIO, transmit XBee frames,
write XBee settings, or touch live ESP32 hardware.
