#!/usr/bin/env python3
"""Simulator-only TCP bridge for the DOS-C Windows 3.1 operator console."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import socketserver
import sys
import threading
import time
from dataclasses import dataclass, field
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import server_lifecycle  # noqa: E402


PROTOCOL_PORT = 31331
MAX_LINE_BYTES = 512
DEVICE_ID = "bench-four-relay-01"
CONTROL_DISABLED_REASON = "control_disabled"
LIFECYCLE_TOOL_NAME = "esp32_gateway_tcp"
LIFECYCLE_COMMAND_MARKER = "esp32_gateway_sim.py"


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
        *,
        register_lifecycle: bool = True,
    ) -> None:
        self.state = state
        self._thread: threading.Thread | None = None
        self._serving = False
        self._closed = False
        self._lifecycle: server_lifecycle.LifecycleRegistration | None = None
        super().__init__(server_address, GatewayHandler)
        if register_lifecycle:
            host, port = self.server_address
            self._lifecycle = server_lifecycle.register_instance(
                tool_name=LIFECYCLE_TOOL_NAME,
                host=str(host),
                port=int(port),
                command_marker=LIFECYCLE_COMMAND_MARKER,
                cwd=ROOT,
                close_callback=self.close,
            )

    def serve_forever(self, poll_interval: float = 0.5) -> None:
        self._serving = True
        try:
            super().serve_forever(poll_interval=poll_interval)
        finally:
            self._serving = False

    def start_background(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self.serve_forever, daemon=True)
        self._thread.start()

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            if self._serving:
                self.shutdown()
            self.server_close()
            if (
                self._thread is not None
                and self._thread.is_alive()
                and threading.current_thread() is not self._thread
            ):
                self._thread.join(timeout=2.0)
        finally:
            if self._lifecycle is not None:
                registration = self._lifecycle
                self._lifecycle = None
                registration.unregister()

    def server_close(self) -> None:
        super().server_close()
        if self._lifecycle is not None:
            registration = self._lifecycle
            self._lifecycle = None
            registration.unregister()

    def __enter__(self) -> "GatewayServer":
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.close()


def _prepare_gateway_for_reopen(host: str, port: int) -> server_lifecycle.LifecycleResult | None:
    if port <= 0:
        return None
    return server_lifecycle.prepare_for_reopen(
        tool_name=LIFECYCLE_TOOL_NAME,
        host=host,
        port=port,
        command_marker=LIFECYCLE_COMMAND_MARKER,
        cwd=ROOT,
    )


def serve(host: str, port: int, *, keep_existing: bool = False) -> None:
    if not keep_existing:
        _prepare_gateway_for_reopen(host, port)
    state = SimulatorState()
    with GatewayServer((host, port), state) as server:
        print(f"ESP32 gateway simulator listening on {host}:{port}", flush=True)
        server.serve_forever()


def start_background_server(
    host: str = "127.0.0.1",
    port: int = 0,
    *,
    keep_existing: bool = False,
) -> GatewayServer:
    if not keep_existing:
        _prepare_gateway_for_reopen(host, port)
    server = GatewayServer((host, port), SimulatorState())
    server.start_background()
    return server


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=PROTOCOL_PORT)
    parser.add_argument(
        "--keep-existing",
        action="store_true",
        help="Do not close a recorded same-tool listener before binding.",
    )
    args = parser.parse_args()
    serve(args.host, args.port, keep_existing=args.keep_existing)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
