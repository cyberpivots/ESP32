#!/usr/bin/env python3
"""Simulator-only tests for the ESP-NOW BBS custom wireless protocol model."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "simulators" / "custom_wireless_protocol"))

from espnow_bbs_custom_protocol import (  # noqa: E402
    BRIDGE_MAX_LINE_BYTES,
    BRIDGE_PROTOCOL_VERSION,
    BRIDGE_STABLE_ERROR_REASONS,
    RADIO_HEADER_BYTES,
    RADIO_MAX_BODY_BYTES,
    RADIO_MAX_FRAGMENT_COUNT,
    RADIO_MAX_PAYLOAD_BYTES,
    DuplicateWindow,
    ProtocolError,
    ProtocolSimulator,
    WirelessPacket,
    decode_bridge_frame,
    decode_packet,
    decode_packet_body,
    encode_bridge_frame,
    encode_packet,
    forward_packet,
    fragment_body,
    make_custody_ack,
    missing_fragment_indexes,
    process_bridge_request,
    reassemble_fragments,
)


class CustomWirelessProtocolTests(unittest.TestCase):
    def test_bridge_frame_bounds_and_ascii(self) -> None:
        frame = {
            "v": BRIDGE_PROTOCOL_VERSION,
            "type": "protocol_report",
            "status": "sim",
            "node": "coord01",
        }
        encoded = encode_bridge_frame(frame)
        self.assertLessEqual(len(encoded) - 1, BRIDGE_MAX_LINE_BYTES)
        self.assertEqual(decode_bridge_frame(encoded), frame)

        with self.assertRaisesRegex(ProtocolError, "line_too_long"):
            encode_bridge_frame({"type": "x", "body": "a" * BRIDGE_MAX_LINE_BYTES})
        with self.assertRaisesRegex(ProtocolError, "non_ascii"):
            encode_bridge_frame({"type": "protocol_report", "body": "snowman-\u2603"})
        with self.assertRaisesRegex(ProtocolError, "payload_invalid"):
            decode_bridge_frame(b"[1,2,3]")

    def test_gate_e_bridge_abi_versioning_and_stable_errors(self) -> None:
        self.assertEqual(BRIDGE_PROTOCOL_VERSION, 1)
        self.assertTrue(
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
            }.issubset(BRIDGE_STABLE_ERROR_REASONS)
        )
        simulator = ProtocolSimulator()

        missing_version = process_bridge_request({"type": "protocol_report"}, simulator)
        self.assertFalse(missing_version["accepted"])
        self.assertEqual(missing_version["v"], BRIDGE_PROTOCOL_VERSION)
        self.assertEqual(missing_version["reason"], "version_required")

        invalid_version = process_bridge_request(
            {"v": 2, "type": "protocol_report"},
            simulator,
        )
        self.assertFalse(invalid_version["accepted"])
        self.assertEqual(invalid_version["reason"], "version_invalid")

    def test_legacy_gate_b_c_unversioned_request_is_explicit(self) -> None:
        simulator = ProtocolSimulator()
        response = process_bridge_request(
            {"type": "protocol_report"},
            simulator,
            allow_legacy_unversioned=True,
        )
        self.assertEqual(response["v"], BRIDGE_PROTOCOL_VERSION)
        self.assertEqual(response["type"], "protocol_report")

    def test_radio_packet_encode_decode_and_bounds(self) -> None:
        packet = WirelessPacket(
            service="direct_message",
            seq=1,
            source="coord01",
            destination="peer01",
            message_id=7,
            body=b"hello",
            custody="queued",
        )
        encoded = encode_packet(packet)
        self.assertEqual(len(encoded), RADIO_HEADER_BYTES + 5)
        self.assertLessEqual(len(encoded), RADIO_MAX_PAYLOAD_BYTES)
        self.assertEqual(decode_packet(encoded), packet)

        with self.assertRaisesRegex(ProtocolError, "body_too_large"):
            encode_packet(
                WirelessPacket(
                    service="direct_message",
                    seq=1,
                    source="coord01",
                    destination="peer01",
                    message_id=8,
                    body=b"x" * (RADIO_MAX_BODY_BYTES + 1),
                )
            )
        with self.assertRaisesRegex(ProtocolError, "service_unknown"):
            encode_packet(
                WirelessPacket(
                    service="stream",
                    seq=1,
                    source="coord01",
                    destination="peer01",
                    message_id=9,
                )
            )

    def test_fragment_reassembly_and_file_resume(self) -> None:
        body = bytes(index % 251 for index in range(RADIO_MAX_BODY_BYTES * 2 + 25))
        packets = fragment_body(
            service="file_chunk",
            source="coord01",
            destination="peer01",
            message_id=42,
            seq=10,
            body=body,
            custody="queued",
        )
        self.assertEqual(len(packets), 3)
        self.assertEqual(reassemble_fragments(packets), body)
        self.assertEqual(missing_fragment_indexes([packets[0], packets[2]]), [1])
        with self.assertRaisesRegex(ProtocolError, "fragment_missing"):
            reassemble_fragments([packets[0], packets[2]])
        with self.assertRaisesRegex(ProtocolError, "fragment_count_invalid"):
            fragment_body(
                service="file_chunk",
                source="coord01",
                destination="peer01",
                message_id=43,
                seq=11,
                body=b"x" * (RADIO_MAX_BODY_BYTES * (RADIO_MAX_FRAGMENT_COUNT + 1)),
            )

    def test_duplicate_ttl_and_custody_ack_flow(self) -> None:
        simulator = ProtocolSimulator()
        packets = simulator.queue_direct_message("peer01", "sysop", "hello over packets")
        packet = packets[0]
        duplicate_window = DuplicateWindow()
        self.assertTrue(duplicate_window.accept(packet))
        self.assertFalse(duplicate_window.accept(packet))

        forwarded = forward_packet(packet)
        self.assertEqual(forwarded.ttl, packet.ttl - 1)
        with self.assertRaisesRegex(ProtocolError, "ttl_expired"):
            forward_packet(packet.with_ttl(1))

        simulator.mark_sent(packet)
        self.assertTrue(simulator.custody[packet.message_id].should_retry())
        ack = make_custody_ack(packet.message_id, "acked", "peer01", "coord01", 99)
        simulator.apply_ack(ack)
        self.assertEqual(simulator.custody[packet.message_id].status, "acked")
        self.assertFalse(simulator.custody[packet.message_id].should_retry())

    def test_direct_message_is_packetized_not_streamed(self) -> None:
        simulator = ProtocolSimulator()
        packets = simulator.queue_direct_message("peer02", "sysop", "bounded packet body")
        self.assertEqual(len(packets), 1)
        packet = packets[0]
        self.assertEqual(packet.service, "direct_message")
        self.assertEqual(packet.destination, "peer02")
        self.assertLessEqual(len(encode_packet(packet)), RADIO_MAX_PAYLOAD_BYTES)
        body = decode_packet_body(packet)
        self.assertEqual(body["from"], "sysop")
        self.assertEqual(body["to"], "peer02")
        self.assertEqual(simulator.custody[packet.message_id].status, "queued")

    def test_telemetry_node_status_and_reporting_fit_bridge_line(self) -> None:
        simulator = ProtocolSimulator()
        soil = simulator.record_telemetry(
            node_id="soil01",
            report_class="soil_moisture",
            sensor_profile="teros12",
            values={"vwc": 31, "temp_c": 22, "ec": 410},
        )
        pivot = simulator.record_telemetry(
            node_id="pivot01",
            report_class="center_pivot",
            sensor_profile="hypothesis",
            values={"state": "moving", "alert": "none"},
        )
        status = simulator.record_node_status("peer01", "espnow-enc", -61, 1200)
        self.assertEqual(soil.service, "telemetry_report")
        self.assertEqual(pivot.service, "telemetry_report")
        self.assertEqual(status.service, "node_status")
        self.assertLessEqual(len(encode_packet(status)), RADIO_MAX_PAYLOAD_BYTES)

        report = simulator.reporting_frame()
        encoded = encode_bridge_frame(report)
        self.assertLessEqual(len(encoded) - 1, BRIDGE_MAX_LINE_BYTES)
        self.assertEqual(json.loads(encoded.decode("ascii"))["telemetry"], 2)

    def test_file_ack_updates_resume_status_and_control_intent_does_not_execute(self) -> None:
        simulator = ProtocolSimulator()
        packets = simulator.queue_file(77, "peer03", b"file-bytes" * 35)
        self.assertGreater(len(packets), 1)
        self.assertEqual(simulator.file_requests[77]["status"], "queued")
        ack = make_custody_ack(77, "delivered", "peer03", "coord01", 88)
        simulator.apply_ack(ack)
        self.assertEqual(simulator.file_requests[77]["status"], "delivered")

        intent = simulator.record_control_intent("peer03", "relay_set")
        self.assertFalse(intent["executed"])
        self.assertEqual(intent["reason"], "control_intent_non_executing")
        report = decode_bridge_frame(encode_bridge_frame(simulator.reporting_frame()))
        self.assertEqual(report["control_intents"], 1)

    def test_bridge_msg_post_and_download_queue_create_packetized_jobs(self) -> None:
        simulator = ProtocolSimulator()
        post = process_bridge_request(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "msg_post",
                "from": "sysop",
                "to": "peer01",
                "body": "hello from opcon",
            },
            simulator,
        )
        self.assertTrue(post["accepted"])
        self.assertTrue(post["packetized"])
        self.assertEqual(post["service"], "direct_message")
        self.assertEqual(post["status"], "queued")
        self.assertLessEqual(len(encode_bridge_frame(post)) - 1, BRIDGE_MAX_LINE_BYTES)
        self.assertEqual(simulator.custody[post["id"]].status, "queued")

        queued = process_bridge_request(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "download_queue",
                "id": 88,
                "peer": "peer02",
                "content": "x" * (RADIO_MAX_BODY_BYTES + 5),
            },
            simulator,
        )
        self.assertTrue(queued["accepted"])
        self.assertTrue(queued["packetized"])
        self.assertEqual(queued["service"], "file_chunk")
        self.assertEqual(queued["fragments"], 2)
        self.assertEqual(simulator.file_requests[88]["status"], "queued")

    def test_bridge_telemetry_status_report_and_closed_controls(self) -> None:
        simulator = ProtocolSimulator()
        telemetry = process_bridge_request(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "telemetry_report",
                "node": "soil01",
                "class": "soil_moisture",
                "sensor": "teros12",
                "values": {"vwc": 31, "temp_c": 22},
            },
            simulator,
        )
        status = process_bridge_request(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "node_status",
                "node": "peer01",
                "link": "espnow-enc",
                "rssi": -59,
                "seen_ms": 900,
            },
            simulator,
        )
        report = process_bridge_request(
            {"v": BRIDGE_PROTOCOL_VERSION, "type": "protocol_report"},
            simulator,
        )
        self.assertEqual(telemetry["service"], "telemetry_report")
        self.assertEqual(status["service"], "node_status")
        self.assertEqual(report["telemetry"], 1)

        control = process_bridge_request(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "control_intent",
                "peer": "peer01",
                "action": "relay_set",
            },
            simulator,
        )
        self.assertTrue(control["accepted"])
        self.assertFalse(control["executed"])

        blocked = process_bridge_request(
            {"v": BRIDGE_PROTOCOL_VERSION, "type": "relay_set", "peer": "peer01"},
            simulator,
        )
        self.assertFalse(blocked["accepted"])
        self.assertEqual(blocked["reason"], "state_changing_command_blocked")

        non_ascii = process_bridge_request(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "msg_post",
                "from": "sysop",
                "to": "peer01",
                "body": "bad-\u2603",
            },
            simulator,
        )
        self.assertFalse(non_ascii["accepted"])
        self.assertEqual(non_ascii["reason"], "non_ascii")


if __name__ == "__main__":
    unittest.main()
