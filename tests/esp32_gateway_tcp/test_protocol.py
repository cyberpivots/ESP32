#!/usr/bin/env python3
"""Protocol tests for the DOS-C ESP32 gateway simulator."""

from __future__ import annotations

import json
import socket
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "simulators" / "esp32_gateway_tcp"))

from esp32_gateway_sim import (  # noqa: E402
    CONTROL_DISABLED_REASON,
    MAX_LINE_BYTES,
    SimulatorState,
    encode_response,
    process_line,
    start_background_server,
)


def payload(message: dict[str, object]) -> bytes:
    return json.dumps(message, separators=(",", ":")).encode("ascii")


class ProtocolTests(unittest.TestCase):
    def test_hello_ack(self) -> None:
        state = SimulatorState()
        response = process_line(payload({"type": "hello"}), state)
        self.assertEqual(response["type"], "ack")
        self.assertTrue(response["accepted"])
        self.assertEqual(response["message"], "hello")

    def test_state_uses_public_relay_channels(self) -> None:
        state = SimulatorState()
        response = process_line(payload({"type": "state_get"}), state)
        self.assertEqual(response["type"], "state")
        self.assertEqual([relay["channel"] for relay in response["relays"]], [1, 2, 3, 4])
        self.assertTrue(response["safety"]["locked"])
        self.assertFalse(response["safety"]["hardware_gate_closed"])
        self.assertEqual(response["control"], CONTROL_DISABLED_REASON)
        self.assertLessEqual(len(encode_response(response)) - 1, MAX_LINE_BYTES)

    def test_relay_set_is_disabled(self) -> None:
        state = SimulatorState()
        response = process_line(
            payload({"type": "relay_set", "channel": 1, "state": True}),
            state,
        )
        self.assertEqual(response["type"], "error")
        self.assertFalse(response["accepted"])
        self.assertEqual(response["reason"], CONTROL_DISABLED_REASON)

    def test_invalid_channel_rejects(self) -> None:
        state = SimulatorState()
        response = process_line(payload({"type": "relay_set", "channel": 0}), state)
        self.assertEqual(response["reason"], "channel_invalid")

    def test_line_size_and_ascii_gates(self) -> None:
        state = SimulatorState()
        self.assertEqual(
            process_line(b"{" + (b" " * (MAX_LINE_BYTES + 1)), state)["reason"],
            "line_too_long",
        )
        self.assertEqual(process_line(b"\xff", state)["reason"], "non_ascii")

    def test_socket_round_trip(self) -> None:
        server = start_background_server()
        try:
            host, port = server.server_address
            with socket.create_connection((host, port), timeout=2) as sock:
                sock.sendall(payload({"type": "state_get"}) + b"\n")
                data = sock.recv(2048)
            response = json.loads(data.decode("ascii"))
            self.assertEqual(response["type"], "state")
            self.assertEqual(response["relays"][3]["channel"], 4)
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
