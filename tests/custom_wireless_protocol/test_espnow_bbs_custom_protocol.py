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
    ANALYTICS_POLICY,
    ANALYTICS_RETENTION,
    ANALYTICS_SCHEMA_VERSION,
    BRIDGE_MAX_LINE_BYTES,
    BRIDGE_PROTOCOL_VERSION,
    BRIDGE_REQUEST_TYPES,
    BRIDGE_STABLE_ERROR_REASONS,
    CUSTODY_CODES,
    RADIO_HEADER_BYTES,
    RADIO_MAX_BODY_BYTES,
    RADIO_MAX_FRAGMENT_COUNT,
    RADIO_MAX_PAYLOAD_BYTES,
    RADIO_PROTOCOL_VERSION,
    SERVICE_CODES,
    CustodyRecord,
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
from espnow_bbs_runtime import (  # noqa: E402
    PacketJob,
    RuntimeConfig,
    RuntimeScheduler,
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

    def test_gate_f_abi_freeze_constants_and_header_layout(self) -> None:
        self.assertEqual(BRIDGE_PROTOCOL_VERSION, 1)
        self.assertEqual(BRIDGE_MAX_LINE_BYTES, 512)
        self.assertEqual(
            BRIDGE_REQUEST_TYPES,
            {
                "msg_post",
                "download_queue",
                "telemetry_report",
                "node_status",
                "protocol_report",
                "state_get",
                "control_intent",
            },
        )
        self.assertEqual(RADIO_PROTOCOL_VERSION, 1)
        self.assertEqual(RADIO_MAX_PAYLOAD_BYTES, 250)
        self.assertEqual(RADIO_HEADER_BYTES, 32)
        self.assertEqual(RADIO_MAX_BODY_BYTES, 190)
        self.assertEqual(RADIO_MAX_FRAGMENT_COUNT, 16)
        self.assertEqual(
            SERVICE_CODES,
            {
                "direct_message": 1,
                "file_chunk": 2,
                "telemetry_report": 3,
                "node_status": 4,
                "custody_ack": 5,
                "control_intent": 6,
            },
        )
        self.assertEqual(
            CUSTODY_CODES,
            {
                "none": 0,
                "queued": 1,
                "sent": 2,
                "delivered": 3,
                "acked": 4,
                "failed": 5,
                "expired": 6,
            },
        )

        packet = WirelessPacket(
            service="custody_ack",
            seq=0x01020304,
            source="src01",
            destination="dst02",
            message_id=0x05060708,
            body=b"ack",
            fragment_index=2,
            fragment_count=9,
            ttl=7,
            custody="acked",
            flags=0xA5,
        )
        encoded = encode_packet(packet)
        self.assertEqual(len(encoded), RADIO_HEADER_BYTES + len(packet.body))
        self.assertEqual(encoded[0], RADIO_PROTOCOL_VERSION)
        self.assertEqual(encoded[1], SERVICE_CODES["custody_ack"])
        self.assertEqual(encoded[2], 0xA5)
        self.assertEqual(encoded[3], 7)
        self.assertEqual(encoded[4:8], (0x01020304).to_bytes(4, "big"))
        self.assertEqual(encoded[8:12], (0x05060708).to_bytes(4, "big"))
        self.assertEqual(encoded[12], 2)
        self.assertEqual(encoded[13], 9)
        self.assertEqual(encoded[14:22], b"src01\0\0\0")
        self.assertEqual(encoded[22:30], b"dst02\0\0\0")
        self.assertEqual(encoded[30], len(packet.body))
        self.assertEqual(encoded[31], CUSTODY_CODES["acked"])
        self.assertEqual(encoded[32:], packet.body)
        self.assertEqual(decode_packet(encoded), packet)

    def test_gate_f_golden_packet_vectors(self) -> None:
        vectors = {
            "direct_message": (
                WirelessPacket(
                    service="direct_message",
                    seq=0x01020304,
                    source="coord01",
                    destination="peer01",
                    message_id=0x11121314,
                    body=b"dm",
                    custody="queued",
                ),
                "0101000401020304111213140001636f6f726430310070656572303100000201646d",
            ),
            "file_chunk": (
                WirelessPacket(
                    service="file_chunk",
                    seq=0x02030405,
                    source="coord01",
                    destination="peer02",
                    message_id=0x21222324,
                    body=b"file",
                    fragment_index=3,
                    fragment_count=5,
                    ttl=5,
                    custody="queued",
                    flags=2,
                ),
                "0102020502030405212223240305636f6f72643031007065657230320000040166696c65",
            ),
            "telemetry_report": (
                WirelessPacket(
                    service="telemetry_report",
                    seq=0x03040506,
                    source="soil01",
                    destination="coord01",
                    message_id=0x31323334,
                    body=b'{"v":1}',
                    custody="delivered",
                ),
                "0103000403040506313233340001736f696c30310000636f6f726430310007037b2276223a317d",
            ),
            "node_status": (
                WirelessPacket(
                    service="node_status",
                    seq=0x04050607,
                    source="peer01",
                    destination="coord01",
                    message_id=0x41424344,
                    body=b"stat",
                    ttl=3,
                    custody="delivered",
                    flags=1,
                ),
                "01040103040506074142434400017065657230310000636f6f7264303100040373746174",
            ),
            "custody_ack": (
                WirelessPacket(
                    service="custody_ack",
                    seq=0x05060708,
                    source="peer01",
                    destination="coord01",
                    message_id=0x51525354,
                    body=b"ack",
                    ttl=2,
                    custody="acked",
                    flags=0x80,
                ),
                "01058002050607085152535400017065657230310000636f6f7264303100030461636b",
            ),
            "control_intent": (
                WirelessPacket(
                    service="control_intent",
                    seq=0x06070809,
                    source="coord01",
                    destination="peer03",
                    message_id=0x61626364,
                    body=b"intent",
                ),
                "0106000406070809616263640001636f6f726430310070656572303300000600696e74656e74",
            ),
        }

        for name, (packet, expected_hex) in vectors.items():
            with self.subTest(name=name):
                encoded = encode_packet(packet)
                self.assertEqual(encoded.hex(), expected_hex)
                self.assertEqual(decode_packet(bytes.fromhex(expected_hex)), packet)

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

    def test_gate_f_runtime_requirements_pin_custody_retry_and_terminal_states(self) -> None:
        simulator = ProtocolSimulator()
        packet = simulator.queue_direct_message("peer01", "sysop", "runtime custody")[0]
        record = simulator.custody[packet.message_id]

        self.assertEqual(record.status, "queued")
        self.assertTrue(record.should_retry(max_attempts=3))

        simulator.mark_sent(packet)
        self.assertEqual(record.status, "sent")
        self.assertEqual(record.attempts, 1)
        self.assertTrue(record.should_retry(max_attempts=3))

        record.mark_ack("delivered")
        self.assertFalse(record.should_retry(max_attempts=3))

        for terminal_status in ("acked", "expired"):
            terminal = CustodyRecord(
                message_id=packet.message_id + len(terminal_status),
                service="direct_message",
                destination="peer01",
            )
            terminal.mark_ack(terminal_status)
            self.assertEqual(terminal.status, terminal_status)
            self.assertFalse(terminal.should_retry(max_attempts=3))

        retry_limited = CustodyRecord(
            message_id=packet.message_id + 99,
            service="direct_message",
            destination="peer01",
        )
        for attempt in range(1, 4):
            retry_limited.mark_sent()
            retry_limited.mark_ack("failed", "timeout")
            self.assertEqual(retry_limited.attempts, attempt)
            self.assertEqual(retry_limited.status, "failed")
            self.assertEqual(
                retry_limited.should_retry(max_attempts=3),
                attempt < 3,
            )

    def test_gate_f_runtime_requirements_pin_fragment_failure_and_control_boundary(self) -> None:
        body = b"runtime-fragments" * 24
        packets = fragment_body(
            service="file_chunk",
            source="coord01",
            destination="peer01",
            message_id=123,
            seq=44,
            body=body,
            custody="queued",
        )
        partial = [packets[0], packets[-1]]

        self.assertGreater(len(packets), 2)
        self.assertEqual(missing_fragment_indexes(partial), list(range(1, len(packets) - 1)))
        with self.assertRaisesRegex(ProtocolError, "fragment_missing"):
            reassemble_fragments(partial)

        simulator = ProtocolSimulator()
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
        self.assertEqual(control["reason"], "control_intent_non_executing")

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

    def test_gate_g_analytics_report_is_simulator_only(self) -> None:
        simulator = ProtocolSimulator()
        post = process_bridge_request(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "msg_post",
                "from": "sysop",
                "to": "peer01",
                "body": "analytics fixture",
            },
            simulator,
        )
        queued = process_bridge_request(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "download_queue",
                "id": 88,
                "peer": "peer02",
                "content": "file",
            },
            simulator,
        )
        telemetry = process_bridge_request(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "telemetry_report",
                "node": "soil01",
                "class": "soil_moisture",
                "values": {"vwc": 31},
            },
            simulator,
        )
        node = process_bridge_request(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "node_status",
                "node": "peer01",
                "link": "espnow-enc",
                "rssi": -60,
                "seen_ms": 100,
            },
            simulator,
        )
        control = process_bridge_request(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "control_intent",
                "peer": "peer01",
                "action": "relay_set",
            },
            simulator,
        )
        blocked = process_bridge_request(
            {"v": BRIDGE_PROTOCOL_VERSION, "type": "relay_set", "peer": "peer01"},
            simulator,
        )
        simulator.apply_ack(make_custody_ack(queued["id"], "acked", "peer02", "coord01", 21))
        report = simulator.analytics_report()

        self.assertTrue(post["accepted"])
        self.assertTrue(queued["accepted"])
        self.assertEqual(telemetry["status"], "delivered")
        self.assertEqual(node["status"], "delivered")
        self.assertFalse(control["executed"])
        self.assertFalse(blocked["accepted"])
        self.assertEqual(report["schema_version"], ANALYTICS_SCHEMA_VERSION)
        self.assertTrue(report["simulator_only"])
        self.assertEqual(report["privacy_policy"], ANALYTICS_POLICY)
        self.assertEqual(report["retention"], ANALYTICS_RETENTION)
        self.assertEqual(report["policy"]["adr"], "ADR-0005")
        self.assertEqual(report["policy"]["status"], "accepted")
        self.assertEqual(report["policy"]["access"], "local_operator_only")
        self.assertEqual(report["counters"]["direct_messages"], 1)
        self.assertEqual(report["counters"]["files"], 1)
        self.assertEqual(report["counters"]["telemetry_reports"], 1)
        self.assertEqual(report["counters"]["node_status_reports"], 1)
        self.assertEqual(report["counters"]["custody_acks"], 1)
        self.assertEqual(report["counters"]["control_intents"], 1)
        self.assertEqual(report["counters"]["blocked_state_changing_requests"], 1)
        self.assertEqual(report["custody"]["acked"], 1)
        self.assertEqual(report["files"]["completed"]["count"], 1)
        self.assertEqual(report["files"]["completed"]["bytes"], 4)
        self.assertEqual(report["telemetry"]["classes"]["soil_moisture"], 1)
        self.assertEqual(report["telemetry"]["node_count"], 1)
        self.assertEqual(report["client_user_summary"]["source"], "simulator_fixtures_only")
        self.assertEqual(
            report["client_user_summary"]["identity_policy"],
            "salted_sha256_required_for_live_export",
        )
        self.assertEqual(report["export_boundary"]["simulator_only"], True)
        self.assertEqual(report["export_boundary"]["privacy_policy"], ANALYTICS_POLICY)
        self.assertEqual(report["export_boundary"]["win31_control"], "absent")
        self.assertEqual(report["export_boundary"]["firmware_request"], "absent")

    def test_phase_6_runtime_defaults_are_host_only_design_values(self) -> None:
        config = RuntimeConfig()

        self.assertEqual(config.outbound_radio_jobs, 32)
        self.assertEqual(config.inbound_packets, 32)
        self.assertEqual(config.custody_ack_events, 16)
        self.assertEqual(config.telemetry_reports, 8)
        self.assertEqual(config.node_status_reports, 8)
        self.assertEqual(config.control_intent_records, 8)
        self.assertEqual(config.duplicate_window, 64)
        self.assertEqual(config.max_attempts, 3)
        self.assertEqual(config.tick_ms, 250)
        self.assertEqual(config.retry_delay_ticks, 2)
        self.assertEqual(config.job_expiry_ticks, 20)

    def test_phase_6_runtime_rejects_33rd_outbound_packet_job(self) -> None:
        runtime = RuntimeScheduler()

        for index in range(32):
            response = runtime.submit_bridge_frame(
                {
                    "v": BRIDGE_PROTOCOL_VERSION,
                    "type": "msg_post",
                    "from": "sysop",
                    "to": "peer01",
                    "body": f"slot-{index}",
                }
            )
            self.assertTrue(response["accepted"])

        rejected = runtime.submit_bridge_frame(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "msg_post",
                "from": "sysop",
                "to": "peer01",
                "body": "overflow",
            }
        )
        self.assertFalse(rejected["accepted"])
        self.assertEqual(rejected["reason"], "backpressure_queue_full")
        self.assertEqual(rejected["queue"], "outbound_radio_jobs")
        self.assertEqual(rejected["needed"], 1)
        self.assertEqual(rejected["available"], 0)
        self.assertEqual(runtime.snapshot()["counters"]["backpressure"], 1)

    def test_phase_6_runtime_file_fragment_limits_and_atomic_admission(self) -> None:
        runtime = RuntimeScheduler()
        sixteen_fragment_body = "x" * (RADIO_MAX_BODY_BYTES * RADIO_MAX_FRAGMENT_COUNT)
        accepted = runtime.submit_bridge_frame(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "download_queue",
                "id": 201,
                "peer": "peer01",
                "content": sixteen_fragment_body,
            }
        )
        self.assertTrue(accepted["accepted"])
        self.assertEqual(accepted["fragments"], RADIO_MAX_FRAGMENT_COUNT)

        too_large = RuntimeScheduler().submit_bridge_frame(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "download_queue",
                "id": 202,
                "peer": "peer01",
                "content": "x" * (RADIO_MAX_BODY_BYTES * (RADIO_MAX_FRAGMENT_COUNT + 1)),
            }
        )
        self.assertFalse(too_large["accepted"])
        self.assertEqual(too_large["reason"], "fragment_count_invalid")

        small_runtime = RuntimeScheduler(config=RuntimeConfig(outbound_radio_jobs=15))
        atomic_reject = small_runtime.submit_bridge_frame(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "download_queue",
                "id": 203,
                "peer": "peer01",
                "content": sixteen_fragment_body,
            }
        )
        self.assertFalse(atomic_reject["accepted"])
        self.assertEqual(atomic_reject["reason"], "backpressure_queue_full")
        self.assertNotIn(203, small_runtime.simulator.custody)
        self.assertNotIn(203, small_runtime.simulator.file_requests)
        self.assertEqual(small_runtime.snapshot()["queues"]["outbound_radio_jobs"], 0)

    def test_phase_6_runtime_dispatches_custody_ack_before_file_chunks(self) -> None:
        runtime = RuntimeScheduler()
        queued = runtime.submit_bridge_frame(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "download_queue",
                "id": 301,
                "peer": "peer01",
                "content": "x" * (RADIO_MAX_BODY_BYTES * 2),
            }
        )
        self.assertTrue(queued["accepted"])
        ack = make_custody_ack(999, "acked", "peer01", "coord01", 71)
        runtime.enqueue_packet_job(PacketJob(packet=ack))

        dispatched = runtime.dispatch_one()
        self.assertIsNotNone(dispatched)
        self.assertEqual(dispatched.service, "custody_ack")

    def test_phase_6_runtime_retry_limit_becomes_terminal_failure(self) -> None:
        runtime = RuntimeScheduler()
        queued = runtime.submit_bridge_frame(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "msg_post",
                "from": "sysop",
                "to": "peer01",
                "body": "retry me",
            }
        )
        message_id = queued["id"]

        first = runtime.dispatch_one()
        self.assertEqual(first.message_id, message_id)
        self.assertEqual(runtime.simulator.custody[message_id].attempts, 1)
        self.assertEqual(runtime.simulator.custody[message_id].status, "sent")

        runtime.tick(runtime.config.retry_delay_ticks)
        runtime.dispatch_one()
        self.assertEqual(runtime.simulator.custody[message_id].attempts, 2)

        runtime.tick(runtime.config.retry_delay_ticks)
        runtime.dispatch_one()
        self.assertEqual(runtime.simulator.custody[message_id].attempts, 3)

        runtime.tick(runtime.config.retry_delay_ticks)
        self.assertIsNotNone(runtime.dispatch_one())
        record = runtime.simulator.custody[message_id]
        self.assertEqual(record.status, "failed")
        self.assertFalse(record.should_retry(max_attempts=runtime.config.max_attempts))
        self.assertEqual(runtime.snapshot()["counters"]["failed"], 1)
        self.assertEqual(runtime.snapshot()["queues"]["outbound_radio_jobs"], 0)

    def test_phase_6_runtime_expiry_beats_retry_and_is_terminal(self) -> None:
        runtime = RuntimeScheduler(config=RuntimeConfig(retry_delay_ticks=30))
        queued = runtime.submit_bridge_frame(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "msg_post",
                "from": "sysop",
                "to": "peer01",
                "body": "expire me",
            }
        )
        message_id = queued["id"]
        runtime.dispatch_one()

        runtime.tick(runtime.config.job_expiry_ticks)
        record = runtime.simulator.custody[message_id]
        self.assertEqual(record.status, "expired")
        self.assertFalse(record.should_retry(max_attempts=runtime.config.max_attempts))
        self.assertEqual(runtime.snapshot()["counters"]["expired"], 1)

    def test_phase_6_runtime_duplicate_inbound_packet_is_counted_and_dropped(self) -> None:
        runtime = RuntimeScheduler()
        packet = WirelessPacket(
            service="direct_message",
            seq=1,
            source="peer01",
            destination="coord01",
            message_id=701,
            body=b"hello",
            custody="delivered",
        )

        accepted = runtime.apply_inbound_packet(packet)
        duplicate = runtime.apply_inbound_packet(packet)
        snapshot = runtime.snapshot()

        self.assertTrue(accepted["accepted"])
        self.assertFalse(duplicate["accepted"])
        self.assertEqual(duplicate["reason"], "duplicate_packet")
        self.assertEqual(snapshot["queues"]["inbound_packets"], 1)
        self.assertEqual(snapshot["counters"]["duplicates"], 1)
        self.assertEqual(snapshot["counters"]["dropped"], 1)

    def test_phase_6_runtime_control_intent_is_record_only(self) -> None:
        runtime = RuntimeScheduler()
        control = runtime.submit_bridge_frame(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "control_intent",
                "peer": "peer01",
                "action": "relay_set",
            }
        )
        blocked = runtime.submit_bridge_frame(
            {"v": BRIDGE_PROTOCOL_VERSION, "type": "relay_set", "peer": "peer01"}
        )
        snapshot = runtime.snapshot()

        self.assertTrue(control["accepted"])
        self.assertFalse(control["executed"])
        self.assertEqual(control["reason"], "control_intent_non_executing")
        self.assertFalse(blocked["accepted"])
        self.assertEqual(blocked["reason"], "state_changing_command_blocked")
        self.assertEqual(snapshot["queues"]["control_intent_records"], 1)
        self.assertEqual(snapshot["queues"]["outbound_radio_jobs"], 0)
        self.assertEqual(snapshot["counters"]["control_intents"], 1)

    def test_phase_6_runtime_bridge_line_rejections_remain_bounded(self) -> None:
        runtime = RuntimeScheduler()
        non_ascii = runtime.submit_bridge_line(
            b'{"v":1,"type":"msg_post","from":"sysop","to":"peer01","body":"bad-\xff"}\n'
        )
        bad_json = runtime.submit_bridge_line(b'{"v":1,"type":')
        too_long = runtime.submit_bridge_line(b"{" + (b'"x":' + b'"a"' * 260) + b"}")

        self.assertFalse(non_ascii["accepted"])
        self.assertEqual(non_ascii["reason"], "non_ascii")
        self.assertFalse(bad_json["accepted"])
        self.assertEqual(bad_json["reason"], "json_invalid")
        self.assertFalse(too_long["accepted"])
        self.assertEqual(too_long["reason"], "line_too_long")

    def test_phase_6_runtime_snapshot_and_report_expose_required_counters(self) -> None:
        runtime = RuntimeScheduler()
        runtime.submit_bridge_frame(
            {
                "v": BRIDGE_PROTOCOL_VERSION,
                "type": "msg_post",
                "from": "sysop",
                "to": "peer01",
                "body": "counter proof",
            }
        )
        runtime.dispatch_one()
        snapshot = runtime.snapshot()
        report = runtime.protocol_report()

        for counter in (
            "queued",
            "sent",
            "delivered",
            "acked",
            "failed",
            "expired",
            "dropped",
            "backpressure",
            "retries",
            "duplicates",
        ):
            self.assertIn(counter, snapshot["counters"])
            self.assertIn(counter, report["runtime"]["counters"])
        self.assertIn("outbound_radio_jobs", snapshot["queues"])
        self.assertIn("runtime", report)


if __name__ == "__main__":
    unittest.main()
