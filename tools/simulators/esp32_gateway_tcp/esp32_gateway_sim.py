#!/usr/bin/env python3
"""Simulator-only TCP bridge for the DOS-C Windows 3.1 operator console."""

from __future__ import annotations

import argparse
import json
import socketserver
import threading
import time
from dataclasses import dataclass, field
from typing import Any


PROTOCOL_PORT = 31331
MAX_LINE_BYTES = 512
DEVICE_ID = "bench-four-relay-01"
CONTROL_DISABLED_REASON = "control_disabled"


@dataclass
class RelayState:
    channel: int
    state: bool = False
    enabled: bool = False
    reject_reason: str = CONTROL_DISABLED_REASON


@dataclass
class SimulatorState:
    device: str = DEVICE_ID
    boot_time: float = field(default_factory=time.monotonic)
    sequence: int = 1
    relays: list[RelayState] = field(
        default_factory=lambda: [RelayState(channel=i) for i in range(1, 5)]
    )
    safety_locked: bool = True
    hardware_gate_closed: bool = False
    storage_mounted: bool = False
    storage_writable: bool = False
    xbee_link_verified: bool = False
    last_result: str = "safe_default"

    def next_sequence(self) -> int:
        self.sequence += 1
        return self.sequence

    def state_payload(self) -> dict[str, Any]:
        return {
            "type": "state",
            "device": self.device,
            "seq": self.next_sequence(),
            "uptime_ms": int((time.monotonic() - self.boot_time) * 1000),
            "safety": {
                "locked": self.safety_locked,
                "hardware_gate_closed": self.hardware_gate_closed,
                "last_result": self.last_result,
            },
            "relays": [
                {
                    "channel": relay.channel,
                    "state": relay.state,
                    "enabled": relay.enabled,
                }
                for relay in self.relays
            ],
            "storage": "rw" if self.storage_mounted and self.storage_writable else "unmounted",
            "xbee": "verified" if self.xbee_link_verified else "unverified",
            "control": CONTROL_DISABLED_REASON,
        }


def encode_response(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, separators=(",", ":"), sort_keys=True) + "\n").encode(
        "ascii"
    )


def error_response(reason: str, detail: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "type": "error",
        "accepted": False,
        "reason": reason,
    }
    if detail:
        payload["detail"] = detail
    return payload


def ack_response(message_type: str, state: SimulatorState) -> dict[str, Any]:
    return {
        "type": "ack",
        "accepted": True,
        "device": state.device,
        "seq": state.next_sequence(),
        "message": message_type,
    }


def process_line(line: bytes, state: SimulatorState) -> dict[str, Any]:
    if len(line) > MAX_LINE_BYTES:
        return error_response("line_too_long")
    try:
        text = line.decode("ascii")
    except UnicodeDecodeError:
        return error_response("non_ascii")
    try:
        message = json.loads(text)
    except json.JSONDecodeError as exc:
        return error_response("json_invalid", str(exc))
    if not isinstance(message, dict):
        return error_response("payload_invalid", "message must be a JSON object")

    message_type = message.get("type")
    if message_type == "hello":
        return ack_response("hello", state)
    if message_type == "ping":
        return ack_response("ping", state)
    if message_type == "state_get":
        return state.state_payload()
    if message_type == "relay_set":
        requested_channel = message.get("channel")
        if requested_channel not in [1, 2, 3, 4]:
            return error_response("channel_invalid")
        state.last_result = CONTROL_DISABLED_REASON
        return error_response(CONTROL_DISABLED_REASON)
    return error_response("message_type_unknown")


class GatewayHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        server = self.server
        assert isinstance(server, GatewayServer)
        while True:
            line = self.rfile.readline(MAX_LINE_BYTES + 2)
            if not line:
                return
            if line.endswith(b"\n"):
                line = line[:-1]
            if line.endswith(b"\r"):
                line = line[:-1]
            response = process_line(line, server.state)
            self.wfile.write(encode_response(response))


class GatewayServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True

    def __init__(
        self,
        server_address: tuple[str, int],
        state: SimulatorState,
    ) -> None:
        self.state = state
        super().__init__(server_address, GatewayHandler)


def serve(host: str, port: int) -> None:
    state = SimulatorState()
    with GatewayServer((host, port), state) as server:
        print(f"ESP32 gateway simulator listening on {host}:{port}", flush=True)
        server.serve_forever()


def start_background_server(host: str = "127.0.0.1", port: int = 0) -> GatewayServer:
    server = GatewayServer((host, port), SimulatorState())
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=PROTOCOL_PORT)
    args = parser.parse_args()
    serve(args.host, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
