#!/usr/bin/env python3
"""Simulator-only custom wireless protocol model for ESP-NOW BBS planning."""

from __future__ import annotations

import argparse
import json
import struct
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any


BRIDGE_MAX_LINE_BYTES = 512
BRIDGE_PROTOCOL_VERSION = 1
BRIDGE_REQUEST_TYPES = frozenset(
    {
        "msg_post",
        "download_queue",
        "telemetry_report",
        "node_status",
        "protocol_report",
        "state_get",
        "control_intent",
    }
)
BRIDGE_STABLE_ERROR_REASONS = frozenset(
    {
        "version_required",
        "version_invalid",
        "line_too_long",
        "non_ascii",
        "json_invalid",
        "payload_invalid",
        "field_type_invalid",
        "hex_invalid",
        "message_type_unknown",
        "state_changing_command_blocked",
    }
)
RADIO_PROTOCOL_VERSION = 1
RADIO_MAX_PAYLOAD_BYTES = 250
RADIO_HEADER_BYTES = 32
RADIO_MAX_BODY_BYTES = 190
RADIO_MAX_FRAGMENT_COUNT = 16
ANALYTICS_SCHEMA_VERSION = "gate-g.analytics.v1"
ANALYTICS_POLICY = "adr-0005-redacted-local-operator-v1"
ANALYTICS_RETENTION = "7_days"

SERVICE_CODES = {
    "direct_message": 1,
    "file_chunk": 2,
    "telemetry_report": 3,
    "node_status": 4,
    "custody_ack": 5,
    "control_intent": 6,
}
CODE_SERVICES = {value: key for key, value in SERVICE_CODES.items()}

CUSTODY_CODES = {
    "none": 0,
    "queued": 1,
    "sent": 2,
    "delivered": 3,
    "acked": 4,
    "failed": 5,
    "expired": 6,
}
CODE_CUSTODY = {value: key for key, value in CUSTODY_CODES.items()}

_HEADER = struct.Struct("!BBBBIIBB8s8sBB")


class ProtocolError(ValueError):
    """Raised when a simulator protocol frame is malformed or unsafe."""

    def __init__(self, reason: str, detail: str | None = None) -> None:
        self.reason = reason
        self.detail = detail
        message = reason if detail is None else f"{reason}: {detail}"
        super().__init__(message)


@dataclass(frozen=True)
class WirelessPacket:
    """Bounded packet for simulator-only custom service tests."""

    service: str
    seq: int
    source: str
    destination: str
    message_id: int
    body: bytes = b""
    fragment_index: int = 0
    fragment_count: int = 1
    ttl: int = 4
    custody: str = "none"
    flags: int = 0

    def duplicate_key(self) -> str:
        return f"{self.source}:{self.destination}:{self.message_id}:{self.fragment_index}"

    def with_ttl(self, ttl: int) -> "WirelessPacket":
        return WirelessPacket(
            service=self.service,
            seq=self.seq,
            source=self.source,
            destination=self.destination,
            message_id=self.message_id,
            body=self.body,
            fragment_index=self.fragment_index,
            fragment_count=self.fragment_count,
            ttl=ttl,
            custody=self.custody,
            flags=self.flags,
        )


@dataclass
class CustodyRecord:
    message_id: int
    service: str
    destination: str
    status: str = "queued"
    attempts: int = 0
    reason: str = ""

    def mark_sent(self) -> None:
        self.attempts += 1
        self.status = "sent"

    def mark_ack(self, status: str = "acked", reason: str = "") -> None:
        if status not in CUSTODY_CODES or status == "none":
            raise ProtocolError("custody_status_invalid", status)
        self.status = status
        self.reason = reason

    def should_retry(self, max_attempts: int = 3) -> bool:
        return self.status in {"queued", "sent", "failed"} and self.attempts < max_attempts


class DuplicateWindow:
    """Small duplicate filter for simulator tests."""

    def __init__(self) -> None:
        self._seen: set[str] = set()

    def accept(self, packet: WirelessPacket) -> bool:
        key = packet.duplicate_key()
        if key in self._seen:
            return False
        self._seen.add(key)
        return True


@dataclass
class ProtocolSimulator:
    """In-memory simulator for packet services behind the BBS bridge."""

    node_id: str = "coord01"
    next_seq: int = 1
    next_message_id: int = 1000
    custody: dict[int, CustodyRecord] = field(default_factory=dict)
    duplicate_window: DuplicateWindow = field(default_factory=DuplicateWindow)
    direct_messages: list[dict[str, Any]] = field(default_factory=list)
    telemetry_reports: list[dict[str, Any]] = field(default_factory=list)
    node_status_reports: list[dict[str, Any]] = field(default_factory=list)
    file_requests: dict[int, dict[str, Any]] = field(default_factory=dict)
    control_intents: list[dict[str, Any]] = field(default_factory=list)
    client_user_labels: set[str] = field(default_factory=set)
    custody_ack_count: int = 0
    blocked_state_changing_requests: int = 0

    def allocate_message_id(self) -> int:
        self.next_message_id += 1
        return self.next_message_id

    def allocate_seq(self) -> int:
        self.next_seq += 1
        return self.next_seq

    def queue_direct_message(self, to_peer: str, sender: str, body: str) -> list[WirelessPacket]:
        payload = compact_json_bytes(
            {
                "from": sender,
                "to": to_peer,
                "body": body,
            }
        )
        message_id = self.allocate_message_id()
        packets = fragment_body(
            service="direct_message",
            source=self.node_id,
            destination=to_peer,
            message_id=message_id,
            seq=self.allocate_seq(),
            body=payload,
            custody="queued",
        )
        self.custody[message_id] = CustodyRecord(
            message_id=message_id,
            service="direct_message",
            destination=to_peer,
        )
        self.direct_messages.append(
            {
                "from": sender,
                "to": to_peer,
                "bytes": len(payload),
            }
        )
        self.client_user_labels.add(sender)
        return packets

    def queue_file(self, file_id: int, to_peer: str, content: bytes) -> list[WirelessPacket]:
        message_id = file_id
        packets = fragment_body(
            service="file_chunk",
            source=self.node_id,
            destination=to_peer,
            message_id=message_id,
            seq=self.allocate_seq(),
            body=content,
            custody="queued",
        )
        self.file_requests[file_id] = {
            "peer": to_peer,
            "bytes": len(content),
            "fragments": len(packets),
            "status": "queued",
        }
        self.custody[message_id] = CustodyRecord(
            message_id=message_id,
            service="file_chunk",
            destination=to_peer,
        )
        return packets

    def record_telemetry(
        self,
        node_id: str,
        report_class: str,
        values: Mapping[str, Any],
        sensor_profile: str = "generic",
    ) -> WirelessPacket:
        payload = {
            "node": node_id,
            "class": report_class,
            "sensor": sensor_profile,
            "values": dict(values),
        }
        body = compact_json_bytes(payload)
        packet = WirelessPacket(
            service="telemetry_report",
            seq=self.allocate_seq(),
            source=node_id,
            destination=self.node_id,
            message_id=self.allocate_message_id(),
            body=body,
            custody="delivered",
        )
        encode_packet(packet)
        self.telemetry_reports.append(payload)
        return packet

    def record_node_status(self, node_id: str, link: str, rssi: int, seen_ms: int) -> WirelessPacket:
        payload = {
            "node": node_id,
            "link": link,
            "rssi": rssi,
            "seen_ms": seen_ms,
        }
        body = compact_json_bytes(payload)
        self.node_status_reports.append(payload)
        return WirelessPacket(
            service="node_status",
            seq=self.allocate_seq(),
            source=node_id,
            destination=self.node_id,
            message_id=self.allocate_message_id(),
            body=body,
            custody="delivered",
        )

    def record_control_intent(self, peer_id: str, action: str) -> dict[str, Any]:
        intent = {
            "peer": peer_id,
            "action": action,
            "executed": False,
            "reason": "control_intent_non_executing",
        }
        self.control_intents.append(intent)
        return intent

    def mark_sent(self, packet: WirelessPacket) -> None:
        record = self.custody.get(packet.message_id)
        if record is None:
            raise ProtocolError("custody_missing", str(packet.message_id))
        record.mark_sent()

    def apply_ack(self, packet: WirelessPacket) -> None:
        if packet.service != "custody_ack":
            raise ProtocolError("ack_service_invalid", packet.service)
        payload = decode_packet_body(packet)
        ack_id = _require_int(payload, "ack")
        status = _require_str(payload, "status")
        reason = str(payload.get("reason", ""))
        record = self.custody.get(ack_id)
        if record is None:
            raise ProtocolError("custody_missing", str(ack_id))
        record.mark_ack(status, reason)
        self.custody_ack_count += 1
        if record.service == "file_chunk" and ack_id in self.file_requests:
            self.file_requests[ack_id]["status"] = status

    def reporting_frame(self) -> dict[str, Any]:
        custody_counts = {status: 0 for status in CUSTODY_CODES if status != "none"}
        for record in self.custody.values():
            custody_counts[record.status] = custody_counts.get(record.status, 0) + 1
        return {
            "v": BRIDGE_PROTOCOL_VERSION,
            "type": "protocol_report",
            "status": "sim",
            "node": self.node_id,
            "custody": custody_counts,
            "telemetry": len(self.telemetry_reports),
            "files": len(self.file_requests),
            "control_intents": len(self.control_intents),
        }

    def analytics_report(self) -> dict[str, Any]:
        custody_rollup = {status: 0 for status in CUSTODY_CODES}
        for record in self.custody.values():
            custody_rollup[record.status] = custody_rollup.get(record.status, 0) + 1

        file_rollup = {
            "queued": {"count": 0, "bytes": 0},
            "completed": {"count": 0, "bytes": 0},
            "failed": {"count": 0, "bytes": 0},
        }
        for request in self.file_requests.values():
            status = str(request.get("status", "queued"))
            bucket = _file_status_bucket(status)
            file_rollup[bucket]["count"] += 1
            file_rollup[bucket]["bytes"] += int(request.get("bytes", 0))

        telemetry_classes: dict[str, int] = {}
        telemetry_nodes: set[str] = set()
        for report in self.telemetry_reports:
            report_class = str(report.get("class", "unknown"))
            telemetry_classes[report_class] = telemetry_classes.get(report_class, 0) + 1
            telemetry_nodes.add(str(report.get("node", "unknown")))

        return {
            "schema_version": ANALYTICS_SCHEMA_VERSION,
            "type": "analytics_report",
            "status": "sim",
            "node": self.node_id,
            "simulator_only": True,
            "privacy_policy": ANALYTICS_POLICY,
            "retention": ANALYTICS_RETENTION,
            "policy": {
                "adr": "ADR-0005",
                "status": "accepted",
                "name": ANALYTICS_POLICY,
                "retention_days": 7,
                "access": "local_operator_only",
                "storage": "ignored_local_proof_packet",
            },
            "counters": {
                "direct_messages": len(self.direct_messages),
                "files": len(self.file_requests),
                "telemetry_reports": len(self.telemetry_reports),
                "node_status_reports": len(self.node_status_reports),
                "custody_acks": self.custody_ack_count,
                "control_intents": len(self.control_intents),
                "blocked_state_changing_requests": self.blocked_state_changing_requests,
            },
            "custody": custody_rollup,
            "files": file_rollup,
            "telemetry": {
                "classes": telemetry_classes,
                "node_count": len(telemetry_nodes),
            },
            "client_user_summary": {
                "source": "simulator_fixtures_only",
                "fixture_label_count": len(self.client_user_labels),
                "direct_message_count": len(self.direct_messages),
                "identity_policy": "salted_sha256_required_for_live_export",
            },
            "export_boundary": {
                "simulator_only": True,
                "privacy_policy": ANALYTICS_POLICY,
                "retention": ANALYTICS_RETENTION,
                "live_bridge_request": "absent",
                "win31_control": "absent",
                "firmware_request": "absent",
            },
        }


def process_bridge_request(
    frame: Mapping[str, Any],
    simulator: ProtocolSimulator,
    *,
    allow_legacy_unversioned: bool = False,
) -> dict[str, Any]:
    """Translate one compact bridge request into simulator-only protocol work."""

    try:
        response = _process_bridge_request(
            frame,
            simulator,
            allow_legacy_unversioned=allow_legacy_unversioned,
        )
        response = _with_bridge_version(response)
        encode_bridge_frame(response)
        return response
    except ProtocolError as exc:
        if exc.reason == "state_changing_command_blocked":
            simulator.blocked_state_changing_requests += 1
        response: dict[str, Any] = {
            "v": BRIDGE_PROTOCOL_VERSION,
            "type": "error",
            "accepted": False,
            "reason": exc.reason,
        }
        if exc.detail:
            response["detail"] = exc.detail
        encode_bridge_frame(response)
        return response


def _process_bridge_request(
    frame: Mapping[str, Any],
    simulator: ProtocolSimulator,
    *,
    allow_legacy_unversioned: bool = False,
) -> dict[str, Any]:
    if not isinstance(frame, Mapping):
        raise ProtocolError("payload_invalid", "frame must be an object")
    _validate_bridge_version(frame, allow_legacy_unversioned)
    message_type = _require_str(frame, "type")
    if message_type in {"protocol_report", "state_get"}:
        return simulator.reporting_frame()
    if message_type == "msg_post":
        to_peer = _require_str(frame, "to")
        sender = _require_str(frame, "from")
        body = _require_str(frame, "body")
        packets = simulator.queue_direct_message(to_peer, sender, body)
        return _bridge_ack(
            "msg_post",
            id=packets[0].message_id,
            service="direct_message",
            status="queued",
            fragments=len(packets),
            packetized=True,
        )
    if message_type == "download_queue":
        file_id = _require_int(frame, "id")
        peer_id = _require_str(frame, "peer")
        content = _bridge_content_bytes(frame)
        packets = simulator.queue_file(file_id, peer_id, content)
        return _bridge_ack(
            "download_queue",
            id=file_id,
            service="file_chunk",
            status="queued",
            fragments=len(packets),
            packetized=True,
        )
    if message_type == "telemetry_report":
        node_id = _require_str(frame, "node")
        report_class = _require_str(frame, "class")
        values = _require_mapping(frame, "values")
        sensor = _require_str(frame, "sensor") if "sensor" in frame else "generic"
        packet = simulator.record_telemetry(node_id, report_class, values, sensor)
        return _bridge_ack(
            "telemetry_report",
            id=packet.message_id,
            service="telemetry_report",
            status="delivered",
            packetized=True,
        )
    if message_type == "node_status":
        node_id = _require_str(frame, "node")
        link = _require_str(frame, "link")
        rssi = _require_int(frame, "rssi")
        seen_ms = _require_int(frame, "seen_ms")
        packet = simulator.record_node_status(node_id, link, rssi, seen_ms)
        encode_packet(packet)
        return _bridge_ack(
            "node_status",
            id=packet.message_id,
            service="node_status",
            status="delivered",
            packetized=True,
        )
    if message_type == "control_intent":
        peer_id = _require_str(frame, "peer")
        action = _require_str(frame, "action")
        intent = simulator.record_control_intent(peer_id, action)
        return {
            "type": "control_intent",
            "accepted": True,
            "executed": False,
            "peer": intent["peer"],
            "action": intent["action"],
            "reason": intent["reason"],
        }
    if message_type in {"relay_set", "flash", "erase", "radio_set"}:
        raise ProtocolError("state_changing_command_blocked", message_type)
    raise ProtocolError("message_type_unknown", message_type)


def compact_json_bytes(payload: Mapping[str, Any]) -> bytes:
    try:
        return json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("ascii")
    except UnicodeEncodeError as exc:
        raise ProtocolError("non_ascii") from exc


def encode_bridge_frame(frame: Mapping[str, Any]) -> bytes:
    payload = compact_json_bytes(frame) + b"\n"
    if len(payload) - 1 > BRIDGE_MAX_LINE_BYTES:
        raise ProtocolError("line_too_long", str(len(payload) - 1))
    return payload


def decode_bridge_frame(line: bytes) -> dict[str, Any]:
    if line.endswith(b"\n"):
        line = line[:-1]
    if line.endswith(b"\r"):
        line = line[:-1]
    if len(line) > BRIDGE_MAX_LINE_BYTES:
        raise ProtocolError("line_too_long", str(len(line)))
    try:
        text = line.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ProtocolError("non_ascii") from exc
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ProtocolError("json_invalid", str(exc)) from exc
    if not isinstance(payload, dict):
        raise ProtocolError("payload_invalid", "frame must be an object")
    return payload


def encode_packet(packet: WirelessPacket) -> bytes:
    _validate_packet(packet)
    header = _HEADER.pack(
        RADIO_PROTOCOL_VERSION,
        SERVICE_CODES[packet.service],
        packet.flags,
        packet.ttl,
        packet.seq,
        packet.message_id,
        packet.fragment_index,
        packet.fragment_count,
        _pack_node(packet.source),
        _pack_node(packet.destination),
        len(packet.body),
        CUSTODY_CODES[packet.custody],
    )
    payload = header + packet.body
    if len(payload) > RADIO_MAX_PAYLOAD_BYTES:
        raise ProtocolError("payload_too_large", str(len(payload)))
    return payload


def decode_packet(payload: bytes) -> WirelessPacket:
    if len(payload) < RADIO_HEADER_BYTES:
        raise ProtocolError("payload_too_short")
    if len(payload) > RADIO_MAX_PAYLOAD_BYTES:
        raise ProtocolError("payload_too_large", str(len(payload)))
    (
        version,
        service_code,
        flags,
        ttl,
        seq,
        message_id,
        fragment_index,
        fragment_count,
        raw_source,
        raw_destination,
        body_len,
        custody_code,
    ) = _HEADER.unpack(payload[:RADIO_HEADER_BYTES])
    if version != RADIO_PROTOCOL_VERSION:
        raise ProtocolError("version_unsupported", str(version))
    if service_code not in CODE_SERVICES:
        raise ProtocolError("service_unknown", str(service_code))
    if custody_code not in CODE_CUSTODY:
        raise ProtocolError("custody_status_unknown", str(custody_code))
    body = payload[RADIO_HEADER_BYTES:]
    if body_len != len(body):
        raise ProtocolError("body_length_mismatch", str(body_len))
    packet = WirelessPacket(
        service=CODE_SERVICES[service_code],
        seq=seq,
        source=_unpack_node(raw_source),
        destination=_unpack_node(raw_destination),
        message_id=message_id,
        body=body,
        fragment_index=fragment_index,
        fragment_count=fragment_count,
        ttl=ttl,
        custody=CODE_CUSTODY[custody_code],
        flags=flags,
    )
    _validate_packet(packet)
    return packet


def fragment_body(
    service: str,
    source: str,
    destination: str,
    message_id: int,
    seq: int,
    body: bytes,
    custody: str = "none",
) -> list[WirelessPacket]:
    if not body:
        chunks = [b""]
    else:
        chunks = [
            body[index : index + RADIO_MAX_BODY_BYTES]
            for index in range(0, len(body), RADIO_MAX_BODY_BYTES)
        ]
    if len(chunks) > RADIO_MAX_FRAGMENT_COUNT:
        raise ProtocolError("fragment_count_invalid", str(len(chunks)))
    packets = [
        WirelessPacket(
            service=service,
            seq=seq,
            source=source,
            destination=destination,
            message_id=message_id,
            body=chunk,
            fragment_index=index,
            fragment_count=len(chunks),
            custody=custody,
        )
        for index, chunk in enumerate(chunks)
    ]
    for packet in packets:
        encode_packet(packet)
    return packets


def reassemble_fragments(packets: list[WirelessPacket]) -> bytes:
    if not packets:
        raise ProtocolError("fragment_missing", "empty")
    first = packets[0]
    expected = first.fragment_count
    seen: dict[int, WirelessPacket] = {}
    for packet in packets:
        if (
            packet.service,
            packet.source,
            packet.destination,
            packet.message_id,
            packet.fragment_count,
        ) != (
            first.service,
            first.source,
            first.destination,
            first.message_id,
            expected,
        ):
            raise ProtocolError("fragment_group_mismatch")
        if packet.fragment_index in seen:
            raise ProtocolError("fragment_duplicate", str(packet.fragment_index))
        seen[packet.fragment_index] = packet
    missing = missing_fragment_indexes(packets)
    if missing:
        raise ProtocolError("fragment_missing", ",".join(str(index) for index in missing))
    return b"".join(seen[index].body for index in range(expected))


def missing_fragment_indexes(packets: list[WirelessPacket]) -> list[int]:
    if not packets:
        return []
    expected = packets[0].fragment_count
    present = {packet.fragment_index for packet in packets}
    return [index for index in range(expected) if index not in present]


def make_custody_ack(
    ack_message_id: int,
    status: str,
    source: str,
    destination: str,
    seq: int,
    reason: str = "",
) -> WirelessPacket:
    body = compact_json_bytes(
        {
            "ack": ack_message_id,
            "status": status,
            "reason": reason,
        }
    )
    return WirelessPacket(
        service="custody_ack",
        seq=seq,
        source=source,
        destination=destination,
        message_id=ack_message_id,
        body=body,
        custody=status,
    )


def forward_packet(packet: WirelessPacket) -> WirelessPacket:
    if packet.ttl <= 1:
        raise ProtocolError("ttl_expired")
    return packet.with_ttl(packet.ttl - 1)


def decode_packet_body(packet: WirelessPacket) -> dict[str, Any]:
    try:
        payload = json.loads(packet.body.decode("ascii"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ProtocolError("body_json_invalid", packet.service) from exc
    if not isinstance(payload, dict):
        raise ProtocolError("body_payload_invalid", packet.service)
    return payload


def _validate_packet(packet: WirelessPacket) -> None:
    if packet.service not in SERVICE_CODES:
        raise ProtocolError("service_unknown", packet.service)
    if packet.custody not in CUSTODY_CODES:
        raise ProtocolError("custody_status_unknown", packet.custody)
    if packet.seq < 0 or packet.seq > 0xFFFFFFFF:
        raise ProtocolError("sequence_invalid")
    if packet.message_id < 0 or packet.message_id > 0xFFFFFFFF:
        raise ProtocolError("message_id_invalid")
    if packet.ttl <= 0 or packet.ttl > 15:
        raise ProtocolError("ttl_invalid")
    if packet.fragment_count < 1 or packet.fragment_count > RADIO_MAX_FRAGMENT_COUNT:
        raise ProtocolError("fragment_count_invalid")
    if packet.fragment_index < 0 or packet.fragment_index >= packet.fragment_count:
        raise ProtocolError("fragment_index_invalid")
    if len(packet.body) > RADIO_MAX_BODY_BYTES:
        raise ProtocolError("body_too_large", str(len(packet.body)))
    _pack_node(packet.source)
    _pack_node(packet.destination)


def _pack_node(node: str) -> bytes:
    try:
        encoded = node.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ProtocolError("node_non_ascii", node[:16]) from exc
    if not encoded or len(encoded) > 8:
        raise ProtocolError("node_id_invalid", node[:16])
    return encoded.ljust(8, b"\0")


def _unpack_node(raw: bytes) -> str:
    return raw.rstrip(b"\0").decode("ascii")


def _require_int(payload: Mapping[str, Any], key: str) -> int:
    value = payload.get(key)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ProtocolError("field_type_invalid", key)
    return value


def _require_str(payload: Mapping[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str):
        raise ProtocolError("field_type_invalid", key)
    try:
        value.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ProtocolError("non_ascii", key) from exc
    return value


def _require_mapping(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise ProtocolError("field_type_invalid", key)
    compact_json_bytes(value)
    return value


def _bridge_content_bytes(frame: Mapping[str, Any]) -> bytes:
    if "content" in frame:
        return _require_str(frame, "content").encode("ascii")
    if "content_hex" in frame:
        raw = _require_str(frame, "content_hex")
        try:
            return bytes.fromhex(raw)
        except ValueError as exc:
            raise ProtocolError("hex_invalid", "content_hex") from exc
    raise ProtocolError("field_type_invalid", "content")


def _bridge_ack(request_type: str, **extra: Any) -> dict[str, Any]:
    ack: dict[str, Any] = {
        "type": f"{request_type}_ack",
        "accepted": True,
        "request": request_type,
    }
    ack.update(extra)
    return ack


def _file_status_bucket(status: str) -> str:
    if status in {"delivered", "acked"}:
        return "completed"
    if status in {"failed", "expired"}:
        return "failed"
    return "queued"


def _validate_bridge_version(frame: Mapping[str, Any], allow_legacy_unversioned: bool) -> None:
    if "v" not in frame:
        if allow_legacy_unversioned:
            return
        raise ProtocolError("version_required", "v")
    version = frame.get("v")
    if (
        not isinstance(version, int)
        or isinstance(version, bool)
        or version != BRIDGE_PROTOCOL_VERSION
    ):
        raise ProtocolError("version_invalid", str(version))


def _with_bridge_version(response: Mapping[str, Any]) -> dict[str, Any]:
    versioned = dict(response)
    versioned.setdefault("v", BRIDGE_PROTOCOL_VERSION)
    return versioned


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="print one compact simulator report")
    parser.add_argument(
        "--analytics-demo",
        action="store_true",
        help="print one simulator-only analytics report",
    )
    args = parser.parse_args()
    if args.demo or args.analytics_demo:
        simulator = ProtocolSimulator()
        packets = simulator.queue_direct_message("peer01", "sysop", "hello")
        simulator.mark_sent(packets[0])
        simulator.apply_ack(make_custody_ack(packets[0].message_id, "acked", "peer01", "coord01", 9))
        process_bridge_request(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "telemetry_report",
                "node": "soil01",
                "class": "soil_moisture",
                "sensor": "generic",
                "values": {"vwc": 31},
            },
            simulator,
        )
        if args.analytics_demo:
            process_bridge_request(
                {
                    "v": BRIDGE_PROTOCOL_VERSION,
                    "type": "control_intent",
                    "peer": "peer01",
                    "action": "relay_set",
                },
                simulator,
            )
            process_bridge_request(
                {"v": BRIDGE_PROTOCOL_VERSION, "type": "relay_set", "peer": "peer01"},
                simulator,
            )
            print(compact_json_bytes(simulator.analytics_report()).decode("ascii"))
        else:
            print(encode_bridge_frame(simulator.reporting_frame()).decode("ascii"), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
