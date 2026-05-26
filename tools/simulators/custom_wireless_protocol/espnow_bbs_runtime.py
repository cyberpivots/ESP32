#!/usr/bin/env python3
"""Host-only runtime scheduler model for ESP-NOW BBS protocol planning."""

from __future__ import annotations

from collections import deque
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from typing import Any

from espnow_bbs_custom_protocol import (
    BRIDGE_PROTOCOL_VERSION,
    RADIO_MAX_BODY_BYTES,
    RADIO_MAX_FRAGMENT_COUNT,
    CUSTODY_CODES,
    ProtocolError,
    ProtocolSimulator,
    WirelessPacket,
    compact_json_bytes,
    decode_bridge_frame,
    encode_bridge_frame,
    encode_packet,
    fragment_body,
)


TERMINAL_CUSTODY = frozenset({"delivered", "acked", "expired"})
RUNTIME_COUNTERS = (
    "queued",
    "sent",
    "delivered",
    "acked",
    "failed",
    "expired",
    "dropped",
    "backpressure",
    "backpressure_coalesced",
    "retries",
    "duplicates",
    "control_intents",
)


@dataclass(frozen=True)
class RuntimeConfig:
    """Host-only runtime defaults selected by the Phase 5/6 design review."""

    outbound_radio_jobs: int = 32
    inbound_packets: int = 32
    custody_ack_events: int = 16
    telemetry_reports: int = 8
    node_status_reports: int = 8
    control_intent_records: int = 8
    duplicate_window: int = 64
    max_attempts: int = 3
    tick_ms: int = 250
    retry_delay_ticks: int = 2
    job_expiry_ticks: int = 20

    def __post_init__(self) -> None:
        for name, value in self.__dict__.items():
            if value <= 0:
                raise ValueError(f"{name} must be positive")


@dataclass
class PacketJob:
    """One bounded radio packet slot tracked by the host-only runtime."""

    packet: WirelessPacket
    created_tick: int = 0
    expires_tick: int = 0
    next_retry_tick: int = 0
    attempts: int = 0
    last_reason: str = ""
    sequence: int = 0

    def sort_key(self) -> tuple[int, int, int, int]:
        return (
            self.created_tick,
            self.sequence,
            self.packet.message_id,
            self.packet.fragment_index,
        )


@dataclass
class RuntimeState:
    """Bounded queues and counters exposed to host tests and future gates."""

    outbound_radio_jobs: list[PacketJob] = field(default_factory=list)
    inbound_packets: list[WirelessPacket] = field(default_factory=list)
    custody_ack_events: list[PacketJob] = field(default_factory=list)
    telemetry_reports: dict[str, dict[str, Any]] = field(default_factory=dict)
    node_status_reports: dict[str, dict[str, Any]] = field(default_factory=dict)
    control_intent_records: list[dict[str, Any]] = field(default_factory=list)
    duplicate_keys: deque[str] = field(default_factory=deque)
    duplicate_key_set: set[str] = field(default_factory=set)
    counters: dict[str, int] = field(default_factory=lambda: {key: 0 for key in RUNTIME_COUNTERS})


class RuntimeScheduler:
    """Simulator-backed runtime model; it never writes serial or firmware state."""

    def __init__(
        self,
        simulator: ProtocolSimulator | None = None,
        config: RuntimeConfig | None = None,
    ) -> None:
        self.simulator = simulator if simulator is not None else ProtocolSimulator()
        self.config = config if config is not None else RuntimeConfig()
        self.state = RuntimeState()
        self.current_tick = 0
        self._queue_sequence = 0

    def submit_bridge_line(self, line: bytes) -> dict[str, Any]:
        """Decode and submit one compact bridge line."""

        try:
            return self.submit_bridge_frame(decode_bridge_frame(line))
        except ProtocolError as exc:
            return self._error(exc.reason, exc.detail)

    def submit_bridge_frame(self, frame: Mapping[str, Any]) -> dict[str, Any]:
        """Translate one bridge request into bounded host-only runtime work."""

        try:
            self._validate_bridge_frame(frame)
            message_type = self._require_str(frame, "type")
            if message_type in {"protocol_report", "state_get"}:
                return self.protocol_report()
            if message_type == "msg_post":
                return self._submit_direct_message(frame)
            if message_type == "download_queue":
                return self._submit_file(frame)
            if message_type == "telemetry_report":
                return self._submit_telemetry(frame)
            if message_type == "node_status":
                return self._submit_node_status(frame)
            if message_type == "control_intent":
                return self._submit_control_intent(frame)
            if message_type in {"relay_set", "flash", "erase", "radio_set"}:
                raise ProtocolError("state_changing_command_blocked", message_type)
            raise ProtocolError("message_type_unknown", message_type)
        except ProtocolError as exc:
            return self._error(exc.reason, exc.detail)

    def enqueue_packet_job(self, job: PacketJob) -> dict[str, Any]:
        """Queue an already encoded packet job if the bounded queue has room."""

        try:
            encode_packet(job.packet)
            self._admit_packet_jobs([job])
            return self._ack("enqueue_packet_job", service=job.packet.service, status="queued")
        except ProtocolError as exc:
            return self._error(exc.reason, exc.detail)

    def apply_inbound_packet(self, packet: WirelessPacket) -> dict[str, Any]:
        """Accept one inbound packet, dropping duplicates with visible counters."""

        try:
            encode_packet(packet)
            if not self._accept_duplicate_key(packet.duplicate_key()):
                self.state.counters["duplicates"] += 1
                self.state.counters["dropped"] += 1
                return self._error("duplicate_packet", packet.duplicate_key())
            if packet.service == "custody_ack":
                return self.apply_custody_ack(packet)
            if len(self.state.inbound_packets) >= self.config.inbound_packets:
                return self._backpressure("inbound_packets", 1, 0)
            self.state.inbound_packets.append(packet)
            return self._ack("inbound_packet", service=packet.service, status="delivered")
        except ProtocolError as exc:
            return self._error(exc.reason, exc.detail)

    def apply_custody_ack(self, packet: WirelessPacket) -> dict[str, Any]:
        """Apply an inbound custody ACK and release terminal queued packet jobs."""

        try:
            self.simulator.apply_ack(packet)
            record = self.simulator.custody[packet.message_id]
            self._release_message_jobs(record.message_id)
            if record.status in self.state.counters:
                self.state.counters[record.status] += 1
            return self._ack(
                "custody_ack",
                id=record.message_id,
                service=record.service,
                status=record.status,
            )
        except ProtocolError as exc:
            return self._error(exc.reason, exc.detail)

    def tick(self, n: int = 1) -> dict[str, Any]:
        """Advance the logical clock; tests use ticks, not wall time."""

        if n <= 0:
            raise ValueError("n must be positive")
        for _ in range(n):
            self.current_tick += 1
            self._expire_due_jobs()
        return self.snapshot()

    def dispatch_one(self) -> WirelessPacket | None:
        """Dispatch one packet according to deterministic scheduler order."""

        self._expire_due_jobs()
        for selector in (
            self._custody_ack_job,
            self._due_retry_job,
            self._queued_direct_message_job,
            self._queued_file_chunk_job,
            self._queued_telemetry_status_job,
        ):
            job = selector()
            if job is not None:
                return self._send_job(job)
        return None

    def snapshot(self) -> dict[str, Any]:
        """Expose queue depths, custody rollups, and runtime counters."""

        return {
            "v": BRIDGE_PROTOCOL_VERSION,
            "type": "runtime_snapshot",
            "tick": self.current_tick,
            "tick_ms": self.config.tick_ms,
            "queues": {
                "outbound_radio_jobs": len(self.state.outbound_radio_jobs),
                "inbound_packets": len(self.state.inbound_packets),
                "custody_ack_events": len(self.state.custody_ack_events),
                "telemetry_reports": len(self.state.telemetry_reports),
                "node_status_reports": len(self.state.node_status_reports),
                "control_intent_records": len(self.state.control_intent_records),
                "duplicate_window": len(self.state.duplicate_keys),
            },
            "custody": self._custody_counts(),
            "counters": dict(self.state.counters),
        }

    def protocol_report(self) -> dict[str, Any]:
        """Bridge-visible runtime report with compact queue/counter rollups."""

        report = self.simulator.reporting_frame()
        report["runtime"] = {
            "tick": self.current_tick,
            "counters": dict(self.state.counters),
        }
        encode_bridge_frame(report)
        return report

    def reset(self) -> None:
        """Clear all volatile runtime state."""

        self.simulator = ProtocolSimulator(node_id=self.simulator.node_id)
        self.state = RuntimeState()
        self.current_tick = 0
        self._queue_sequence = 0

    def _submit_direct_message(self, frame: Mapping[str, Any]) -> dict[str, Any]:
        to_peer = self._require_str(frame, "to")
        sender = self._require_str(frame, "from")
        body = self._require_str(frame, "body")
        payload = compact_json_bytes({"from": sender, "to": to_peer, "body": body})
        needed = self._fragment_count(payload)
        available = self._outbound_available()
        if needed > available:
            return self._backpressure("outbound_radio_jobs", needed, available)
        packets = self.simulator.queue_direct_message(to_peer, sender, body)
        self._admit_packets(packets)
        return self._ack(
            "msg_post",
            id=packets[0].message_id,
            service="direct_message",
            status="queued",
            fragments=len(packets),
            packetized=True,
        )

    def _submit_file(self, frame: Mapping[str, Any]) -> dict[str, Any]:
        file_id = self._require_int(frame, "id")
        peer_id = self._require_str(frame, "peer")
        content = self._bridge_content_bytes(frame)
        needed = self._fragment_count(content)
        available = self._outbound_available()
        if needed > available:
            return self._backpressure("outbound_radio_jobs", needed, available)
        packets = self.simulator.queue_file(file_id, peer_id, content)
        self._admit_packets(packets)
        return self._ack(
            "download_queue",
            id=file_id,
            service="file_chunk",
            status="queued",
            fragments=len(packets),
            packetized=True,
        )

    def _submit_telemetry(self, frame: Mapping[str, Any]) -> dict[str, Any]:
        node_id = self._require_str(frame, "node")
        report_class = self._require_str(frame, "class")
        values = self._require_mapping(frame, "values")
        sensor = self._require_str(frame, "sensor") if "sensor" in frame else "generic"
        if (
            len(self.state.telemetry_reports) >= self.config.telemetry_reports
            and node_id not in self.state.telemetry_reports
        ):
            self.state.counters["dropped"] += 1
            return self._backpressure("telemetry_reports", 1, 0)
        coalesced = node_id in self.state.telemetry_reports
        packet = self.simulator.record_telemetry(node_id, report_class, values, sensor)
        self.state.telemetry_reports[node_id] = {
            "class": report_class,
            "sensor": sensor,
            "values": dict(values),
            "message_id": packet.message_id,
        }
        if coalesced:
            self.state.counters["backpressure_coalesced"] += 1
        return self._ack(
            "telemetry_report",
            id=packet.message_id,
            service="telemetry_report",
            status="delivered",
            coalesced=coalesced,
        )

    def _submit_node_status(self, frame: Mapping[str, Any]) -> dict[str, Any]:
        node_id = self._require_str(frame, "node")
        link = self._require_str(frame, "link")
        rssi = self._require_int(frame, "rssi")
        seen_ms = self._require_int(frame, "seen_ms")
        if (
            len(self.state.node_status_reports) >= self.config.node_status_reports
            and node_id not in self.state.node_status_reports
        ):
            self.state.counters["dropped"] += 1
            return self._backpressure("node_status_reports", 1, 0)
        coalesced = node_id in self.state.node_status_reports
        packet = self.simulator.record_node_status(node_id, link, rssi, seen_ms)
        encode_packet(packet)
        self.state.node_status_reports[node_id] = {
            "link": link,
            "rssi": rssi,
            "seen_ms": seen_ms,
            "message_id": packet.message_id,
        }
        if coalesced:
            self.state.counters["backpressure_coalesced"] += 1
        return self._ack(
            "node_status",
            id=packet.message_id,
            service="node_status",
            status="delivered",
            coalesced=coalesced,
        )

    def _submit_control_intent(self, frame: Mapping[str, Any]) -> dict[str, Any]:
        peer_id = self._require_str(frame, "peer")
        action = self._require_str(frame, "action")
        if len(self.state.control_intent_records) >= self.config.control_intent_records:
            return self._backpressure("control_intent_records", 1, 0)
        intent = self.simulator.record_control_intent(peer_id, action)
        self.state.control_intent_records.append(intent)
        self.state.counters["control_intents"] += 1
        return self._versioned(
            {
                "type": "control_intent",
                "accepted": True,
                "executed": False,
                "peer": intent["peer"],
                "action": intent["action"],
                "reason": intent["reason"],
            }
        )

    def _admit_packets(self, packets: list[WirelessPacket]) -> None:
        self._admit_packet_jobs([PacketJob(packet=packet) for packet in packets])

    def _admit_packet_jobs(self, jobs: list[PacketJob]) -> None:
        available = self._outbound_available()
        if len(jobs) > available:
            raise ProtocolError(
                "backpressure_queue_full",
                f"outbound_radio_jobs needed={len(jobs)} available={available}",
            )
        for job in jobs:
            self._queue_sequence += 1
            job.created_tick = self.current_tick
            job.expires_tick = self.current_tick + self.config.job_expiry_ticks
            job.next_retry_tick = self.current_tick
            job.sequence = self._queue_sequence
            self.state.outbound_radio_jobs.append(job)
            if job.packet.service == "custody_ack":
                self.state.custody_ack_events.append(job)
        self.state.counters["queued"] += len(jobs)

    def _send_job(self, job: PacketJob) -> WirelessPacket:
        record = self.simulator.custody.get(job.packet.message_id)
        if job.packet.service == "custody_ack":
            self._release_job(job)
            self.state.counters["sent"] += 1
            return replace(job.packet, custody="acked")
        if record is None:
            raise ProtocolError("custody_missing", str(job.packet.message_id))
        if record.attempts >= self.config.max_attempts:
            record.mark_ack("failed", "retry_limit")
            self.state.counters["failed"] += 1
            self._release_message_jobs(record.message_id)
            return replace(job.packet, custody="failed")
        was_retry = record.attempts > 0
        record.mark_sent()
        job.attempts = record.attempts
        job.next_retry_tick = self.current_tick + self.config.retry_delay_ticks
        job.last_reason = ""
        self.state.counters["sent"] += 1
        if was_retry:
            self.state.counters["retries"] += 1
        return replace(job.packet, custody="sent")

    def _expire_due_jobs(self) -> None:
        for job in list(self.state.outbound_radio_jobs):
            record = self.simulator.custody.get(job.packet.message_id)
            if record is None or record.status in TERMINAL_CUSTODY:
                continue
            if self.current_tick >= job.expires_tick:
                record.mark_ack("expired", "job_expired")
                job.last_reason = "job_expired"
                self.state.counters["expired"] += 1
                self._release_message_jobs(record.message_id)

    def _custody_ack_job(self) -> PacketJob | None:
        return self._first_job(lambda job: job.packet.service == "custody_ack")

    def _due_retry_job(self) -> PacketJob | None:
        def is_due_retry(job: PacketJob) -> bool:
            record = self.simulator.custody.get(job.packet.message_id)
            return (
                record is not None
                and record.status in {"sent", "failed"}
                and self.current_tick >= job.next_retry_tick
            )

        return self._first_job(is_due_retry)

    def _queued_direct_message_job(self) -> PacketJob | None:
        return self._first_queued_job("direct_message")

    def _queued_file_chunk_job(self) -> PacketJob | None:
        return self._first_queued_job("file_chunk")

    def _queued_telemetry_status_job(self) -> PacketJob | None:
        return self._first_job(
            lambda job: job.packet.service in {"telemetry_report", "node_status"}
            and self._record_status(job) == "queued"
        )

    def _first_queued_job(self, service: str) -> PacketJob | None:
        return self._first_job(
            lambda job: job.packet.service == service and self._record_status(job) == "queued"
        )

    def _first_job(self, predicate: Any) -> PacketJob | None:
        candidates = [job for job in self.state.outbound_radio_jobs if predicate(job)]
        if not candidates:
            return None
        return sorted(candidates, key=lambda job: job.sort_key())[0]

    def _record_status(self, job: PacketJob) -> str:
        record = self.simulator.custody.get(job.packet.message_id)
        return "" if record is None else record.status

    def _release_job(self, target: PacketJob) -> None:
        self.state.outbound_radio_jobs = [
            job for job in self.state.outbound_radio_jobs if job is not target
        ]
        self.state.custody_ack_events = [job for job in self.state.custody_ack_events if job is not target]

    def _release_message_jobs(self, message_id: int) -> None:
        self.state.outbound_radio_jobs = [
            job for job in self.state.outbound_radio_jobs if job.packet.message_id != message_id
        ]
        self.state.custody_ack_events = [
            job for job in self.state.custody_ack_events if job.packet.message_id != message_id
        ]

    def _accept_duplicate_key(self, key: str) -> bool:
        if key in self.state.duplicate_key_set:
            return False
        self.state.duplicate_key_set.add(key)
        self.state.duplicate_keys.append(key)
        while len(self.state.duplicate_keys) > self.config.duplicate_window:
            removed = self.state.duplicate_keys.popleft()
            self.state.duplicate_key_set.discard(removed)
        return True

    def _outbound_available(self) -> int:
        return self.config.outbound_radio_jobs - len(self.state.outbound_radio_jobs)

    def _fragment_count(self, body: bytes) -> int:
        count = max(1, (len(body) + RADIO_MAX_BODY_BYTES - 1) // RADIO_MAX_BODY_BYTES)
        if count > RADIO_MAX_FRAGMENT_COUNT:
            fragment_body(
                service="file_chunk",
                source=self.simulator.node_id,
                destination="peer01",
                message_id=0,
                seq=0,
                body=body,
            )
        return count

    def _custody_counts(self) -> dict[str, int]:
        counts = {status: 0 for status in CUSTODY_CODES if status != "none"}
        for record in self.simulator.custody.values():
            counts[record.status] = counts.get(record.status, 0) + 1
        return counts

    def _backpressure(self, queue: str, needed: int, available: int) -> dict[str, Any]:
        self.state.counters["backpressure"] += 1
        self.state.counters["dropped"] += 1
        return self._versioned(
            {
                "type": "error",
                "accepted": False,
                "reason": "backpressure_queue_full",
                "queue": queue,
                "needed": needed,
                "available": available,
            }
        )

    def _error(self, reason: str, detail: str | None = None) -> dict[str, Any]:
        response: dict[str, Any] = {
            "type": "error",
            "accepted": False,
            "reason": reason,
        }
        if detail:
            response["detail"] = detail
        return self._versioned(response)

    def _ack(self, request_type: str, **extra: Any) -> dict[str, Any]:
        response: dict[str, Any] = {
            "type": f"{request_type}_ack",
            "accepted": True,
            "request": request_type,
        }
        response.update(extra)
        return self._versioned(response)

    def _versioned(self, response: Mapping[str, Any]) -> dict[str, Any]:
        versioned = dict(response)
        versioned.setdefault("v", BRIDGE_PROTOCOL_VERSION)
        encode_bridge_frame(versioned)
        return versioned

    def _validate_bridge_frame(self, frame: Mapping[str, Any]) -> None:
        if not isinstance(frame, Mapping):
            raise ProtocolError("payload_invalid", "frame must be an object")
        version = frame.get("v")
        if version != BRIDGE_PROTOCOL_VERSION or isinstance(version, bool):
            reason = "version_required" if "v" not in frame else "version_invalid"
            raise ProtocolError(reason, str(version))

    def _require_int(self, payload: Mapping[str, Any], key: str) -> int:
        value = payload.get(key)
        if not isinstance(value, int) or isinstance(value, bool):
            raise ProtocolError("field_type_invalid", key)
        return value

    def _require_str(self, payload: Mapping[str, Any], key: str) -> str:
        value = payload.get(key)
        if not isinstance(value, str):
            raise ProtocolError("field_type_invalid", key)
        try:
            value.encode("ascii")
        except UnicodeEncodeError as exc:
            raise ProtocolError("non_ascii", key) from exc
        return value

    def _require_mapping(self, payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
        value = payload.get(key)
        if not isinstance(value, Mapping):
            raise ProtocolError("field_type_invalid", key)
        compact_json_bytes(value)
        return value

    def _bridge_content_bytes(self, frame: Mapping[str, Any]) -> bytes:
        if "content" in frame:
            return self._require_str(frame, "content").encode("ascii")
        if "content_hex" in frame:
            raw = self._require_str(frame, "content_hex")
            try:
                return bytes.fromhex(raw)
            except ValueError as exc:
                raise ProtocolError("hex_invalid", "content_hex") from exc
        raise ProtocolError("field_type_invalid", "content")
