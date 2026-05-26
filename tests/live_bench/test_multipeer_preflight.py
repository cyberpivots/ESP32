#!/usr/bin/env python3
"""Fixture tests for the ESP-NOW BBS multi-peer live preflight gate."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "live_bench_preflight",
    ROOT / "scripts" / "live_bench_preflight.py",
)
assert SPEC is not None and SPEC.loader is not None
live_bench_preflight = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(live_bench_preflight)


PORTS = ["COM4", "COM5", "COM6"]
REMAP_PORTS = ["COM9", "COM6", "COM7"]
CURRENT_REMAP_PORTS = ["COM6", "COM10", "COM12"]


def serial_entry(port: str) -> dict[str, object]:
    return {
        "Caption": f"Silicon Labs CP210x USB to UART Bridge ({port})",
        "Description": "Silicon Labs CP210x USB to UART Bridge",
        "DeviceID": port,
        "PNPDeviceID": f"USB\\VID_10C4&PID_EA60\\{port}",
        "Status": "OK",
        "ConfigManagerErrorCode": 0,
        "Name": f"Silicon Labs CP210x USB to UART Bridge ({port})",
        "MaxBaudRate": 921600,
    }


def identity(mac: str, *, malformed: bool = False, flash: str = "4MB") -> dict[str, object]:
    if malformed:
        commands = {
            "chip-id": {"returncode": 0, "stdout": ["esptool.py v5.0"], "stderr": []},
            "read-mac": {"returncode": 0, "stdout": ["no mac here"], "stderr": []},
            "flash-id": {"returncode": 0, "stdout": ["no flash size"], "stderr": []},
        }
    else:
        commands = {
            "chip-id": {
                "returncode": 0,
                "stdout": ["Chip is ESP32-D0WDQ6 (revision v1.0)"],
                "stderr": [],
            },
            "read-mac": {"returncode": 0, "stdout": [f"MAC: {mac}"], "stderr": []},
            "flash-id": {
                "returncode": 0,
                "stdout": [f"Detected flash size: {flash}", "Manufacturer: e0", "Device: 4016"],
                "stderr": [],
            },
        }
    record: dict[str, object] = {
        "commands": commands,
        "port": "COM4",
        "portKind": "windows",
    }
    live_bench_preflight.finalize_esp32_identity(record)
    return record


def legacy_identity(mac: str) -> dict[str, object]:
    record: dict[str, object] = {
        "commands": {
            "chip_id": {
                "returncode": 0,
                "stdout": [
                    "Warning: Deprecated: Command 'chip_id' is deprecated. Use 'chip-id' instead.",
                    "Chip is ESP32-D0WDQ6 (revision v1.0)",
                ],
                "stderr": [],
            },
            "read_mac": {"returncode": 0, "stdout": [f"MAC: {mac}"], "stderr": []},
            "flash_id": {
                "returncode": 0,
                "stdout": ["Detected flash size: 4MB", "Manufacturer: e0", "Device: 4016"],
                "stderr": [],
            },
        },
        "port": "COM4",
        "portKind": "windows",
    }
    live_bench_preflight.finalize_esp32_identity(record)
    return record


def pi_items(*, stale_listener: bool = False, missing_usb: bool = False) -> list[dict[str, object]]:
    return [
        {"name": "hostname", "ok": True},
        {"name": "model", "ok": True},
        {"name": "serial", "ok": True},
        {"name": "rootSource", "ok": True},
        {"name": "eth0Address", "ok": True},
        {
            "name": "closedTcpPorts",
            "ok": not stale_listener,
            "code": "stalePiListener",
            "value": ["LISTEN 0 4096 127.0.0.1:31332"] if stale_listener else [],
        },
        {"name": "noBridgeDosboxOrModalProcesses", "ok": True},
        {
            "name": "coordinatorUsbPresent",
            "ok": not missing_usb,
            "code": "coordinatorUsbMissing",
            "value": [] if missing_usb else "/dev/ttyUSB0",
        },
    ]


def base_record() -> dict[str, object]:
    parsed = {"serialPorts": [serial_entry(port) for port in PORTS]}
    return {
        "expectedPeerPorts": PORTS,
        "coordinatorPort": "/dev/ttyUSB0",
        "windowsPeerInventory": {
            "parsed": parsed,
            "expectedChecks": live_bench_preflight.check_windows_peers(parsed, PORTS),
        },
        "peerEsp32Identities": {
            "ports": {
                "COM4": identity("78:e3:6d:0a:90:14"),
                "COM5": identity("78:e3:6d:0a:90:15"),
                "COM6": identity("78:e3:6d:0a:90:16"),
            }
        },
        "piIdentity": {
            "target": "dospi@172.16.0.2",
            "fingerprintCheck": {"ok": True},
            "identityChecks": {"ok": True, "items": pi_items()},
            "coordinatorEsp32Identity": identity("78:e3:6d:10:4d:6c"),
        },
    }


def failure_codes(record: dict[str, object]) -> set[str]:
    return {
        str(failure.get("code"))
        for failure in record.get("failures", [])
        if isinstance(failure, dict)
    }


class MultiPeerPreflightTests(unittest.TestCase):
    def test_forwarded_pi_host_uses_expected_identity_profile(self) -> None:
        self.assertTrue(live_bench_preflight.uses_expected_pi_profile("172.16.0.2"))
        self.assertTrue(live_bench_preflight.uses_expected_pi_profile("192.168.137.93"))
        self.assertTrue(live_bench_preflight.uses_expected_pi_profile("192.168.137.105"))
        self.assertFalse(live_bench_preflight.uses_expected_pi_profile("192.168.200.104"))

    def test_pi_coordinator_identity_uses_no_stub(self) -> None:
        script = live_bench_preflight.build_pi_remote_script("/dev/ttyUSB0", False)
        self.assertIn(live_bench_preflight.REMOTE_ESPNOW_ESPTOOL, script)
        self.assertIn('$ESPTOOL_STUB_ARGS --port "$COORDINATOR_PORT"', script)
        self.assertIn('ESPTOOL_STUB_ARGS="--no-stub"', script)
        self.assertIn("chip-id", script)
        self.assertIn("read-mac", script)
        self.assertIn("flash-id", script)
        self.assertNotIn("chip_id", script)
        self.assertNotIn("read_mac", script)
        self.assertNotIn("flash_id", script)

    def test_identity_commands_use_hyphenated_names(self) -> None:
        self.assertEqual(
            live_bench_preflight.ALLOWED_ESPTOOL_COMMANDS,
            ("chip-id", "read-mac", "flash-id"),
        )

    def test_legacy_identity_records_still_parse_and_surface_warnings(self) -> None:
        record = legacy_identity("78:e3:6d:0a:90:14")
        parsed = record["parsedIdentity"]
        self.assertTrue(record["ok"])
        self.assertTrue(parsed["usesLegacyCommandNames"])
        self.assertEqual(parsed["mac"], "78:e3:6d:0a:90:14")
        self.assertEqual(parsed["commandSources"]["read-mac"], "read_mac")
        self.assertEqual(parsed["esptoolWarnings"][0]["command"], "chip_id")

    def test_good_inventory_maps_ports_by_order(self) -> None:
        record = live_bench_preflight.validate_preflight_record(base_record())
        self.assertTrue(record["ok"])
        self.assertEqual(record["peerMap"]["peer01"]["windowsPort"], "COM4")
        self.assertEqual(record["peerMap"]["peer02"]["windowsPort"], "COM5")
        self.assertEqual(record["peerMap"]["peer03"]["windowsPort"], "COM6")
        self.assertEqual(record["coordinatorMap"]["mac"], "78:e3:6d:10:4d:6c")

    def test_accepted_mac_remap_maps_roles_by_mac(self) -> None:
        record = base_record()
        parsed = {"serialPorts": [serial_entry(port) for port in REMAP_PORTS]}
        record["expectedPeerPorts"] = REMAP_PORTS
        record["peerPortPolicy"] = {
            "mode": "accepted_mac_remap",
            "acceptedPeerRoleMacs": live_bench_preflight.ACCEPTED_PEER_ROLE_MACS,
        }
        record["windowsPeerInventory"]["parsed"] = parsed
        record["windowsPeerInventory"]["expectedChecks"] = (
            live_bench_preflight.check_windows_peers(parsed, REMAP_PORTS)
        )
        record["peerEsp32Identities"]["ports"] = {
            "COM9": identity("94:b9:7e:da:17:d0"),
            "COM6": identity("78:e3:6d:0a:90:14"),
            "COM7": identity("94:b9:7e:da:9a:50"),
        }
        checked = live_bench_preflight.validate_preflight_record(record)
        self.assertTrue(checked["ok"])
        self.assertEqual(checked["peerMap"]["peer01"]["windowsPort"], "COM9")
        self.assertEqual(checked["peerMap"]["peer02"]["windowsPort"], "COM6")
        self.assertEqual(checked["peerMap"]["peer03"]["windowsPort"], "COM7")

    def test_current_accepted_peer_remap_maps_roles_by_mac(self) -> None:
        record = base_record()
        parsed = {"serialPorts": [serial_entry(port) for port in CURRENT_REMAP_PORTS]}
        record["expectedPeerPorts"] = CURRENT_REMAP_PORTS
        record["peerPortPolicy"] = {
            "mode": "accepted_mac_remap",
            "acceptedPeerRoleMacs": live_bench_preflight.ACCEPTED_PEER_ROLE_MACS,
            "currentAcceptedRolePorts": {
                "peer01": "COM6",
                "peer02": "COM10",
                "peer03": "COM12",
            },
        }
        record["windowsPeerInventory"]["parsed"] = parsed
        record["windowsPeerInventory"]["expectedChecks"] = (
            live_bench_preflight.check_windows_peers(parsed, CURRENT_REMAP_PORTS)
        )
        record["peerEsp32Identities"]["ports"] = {
            "COM6": identity("94:b9:7e:da:17:d0"),
            "COM10": identity("78:e3:6d:0a:90:14"),
            "COM12": identity("94:b9:7e:da:9a:50"),
        }
        checked = live_bench_preflight.validate_preflight_record(record)
        self.assertTrue(checked["ok"])
        self.assertEqual(checked["peerMap"]["peer01"]["windowsPort"], "COM6")
        self.assertEqual(checked["peerMap"]["peer02"]["windowsPort"], "COM10")
        self.assertEqual(checked["peerMap"]["peer03"]["windowsPort"], "COM12")
        self.assertIn("peer01=COM6", " ".join(checked["verifiedFacts"]))

    def test_accepted_mac_remap_rejects_unexpected_mac_set(self) -> None:
        record = base_record()
        parsed = {"serialPorts": [serial_entry(port) for port in REMAP_PORTS]}
        record["expectedPeerPorts"] = REMAP_PORTS
        record["peerPortPolicy"] = {
            "mode": "accepted_mac_remap",
            "acceptedPeerRoleMacs": live_bench_preflight.ACCEPTED_PEER_ROLE_MACS,
        }
        record["windowsPeerInventory"]["parsed"] = parsed
        record["windowsPeerInventory"]["expectedChecks"] = (
            live_bench_preflight.check_windows_peers(parsed, REMAP_PORTS)
        )
        record["peerEsp32Identities"]["ports"] = {
            "COM9": identity("94:b9:7e:da:17:d0"),
            "COM6": identity("78:e3:6d:0a:90:14"),
            "COM7": identity("78:e3:6d:0a:90:17"),
        }
        checked = live_bench_preflight.validate_preflight_record(record)
        self.assertFalse(checked["ok"])
        self.assertIn("unexpectedPeerMacSet", failure_codes(checked))

    def test_summary_reports_ready_gate_without_command_logs(self) -> None:
        record = live_bench_preflight.validate_preflight_record(base_record())
        summary = live_bench_preflight.summarize_preflight_record(record)
        self.assertTrue(summary["ok"])
        self.assertEqual(summary["readiness"], "ready_for_prepare")
        self.assertEqual(summary["peers"]["COM4"]["mac"], "78:e3:6d:0a:90:14")
        self.assertNotIn("commands", summary["peers"]["COM4"])
        self.assertIn("esptoolWarnings", summary)

    def test_summary_reports_esptool_warnings(self) -> None:
        record = live_bench_preflight.validate_preflight_record(base_record())
        record["peerEsp32Identities"]["ports"]["COM4"] = legacy_identity(
            "78:e3:6d:0a:90:14"
        )
        summary = live_bench_preflight.summarize_preflight_record(record)
        self.assertEqual(
            summary["peers"]["COM4"]["esptoolWarnings"][0]["command"],
            "chip_id",
        )

    def test_discovered_pi_host_can_use_expected_identity_profile(self) -> None:
        lines = [
            "__hostnamectl__",
            "Static hostname: dos-pi4-poe",
            "__model__",
            "Raspberry Pi 4 Model B Rev 1.2",
            "__serial__",
            "10000000aaaa5b24",
            "__root_source__",
            "/dev/mmcblk0p2",
            "__eth0_addr__",
            "eth0 UP 172.16.0.2/24",
            "__listeners__",
            "__processes__",
            "__usb_inventory__",
            "crw-rw---- 1 root dialout 188, 0 May 25 12:00 /dev/ttyUSB0",
        ]
        checked = live_bench_preflight.check_pi_identity(
            lines,
            "172.16.0.44",
            "/dev/ttyUSB0",
            allow_discovered_host=True,
        )
        self.assertTrue(checked["ok"])

    def test_missing_peer_fails(self) -> None:
        record = base_record()
        parsed = {"serialPorts": [serial_entry("COM4"), serial_entry("COM6")]}
        record["windowsPeerInventory"]["expectedChecks"] = (
            live_bench_preflight.check_windows_peers(parsed, PORTS)
        )
        checked = live_bench_preflight.validate_preflight_record(record)
        self.assertFalse(checked["ok"])
        self.assertIn("missingWindowsPeer", failure_codes(checked))

    def test_duplicate_mac_fails(self) -> None:
        record = base_record()
        record["peerEsp32Identities"]["ports"]["COM5"] = identity("78:e3:6d:0a:90:14")
        checked = live_bench_preflight.validate_preflight_record(record)
        self.assertFalse(checked["ok"])
        self.assertIn("duplicatePeerMac", failure_codes(checked))

    def test_wrong_pi_host_key_fails(self) -> None:
        record = base_record()
        record["piIdentity"]["fingerprintCheck"] = {
            "ok": False,
            "expected": {"ED25519": "expected"},
            "observed": {"ED25519": "wrong"},
        }
        checked = live_bench_preflight.validate_preflight_record(record)
        self.assertFalse(checked["ok"])
        self.assertIn("piFingerprintMismatch", failure_codes(checked))
        summary = live_bench_preflight.summarize_preflight_record(checked)
        self.assertEqual(summary["readiness"], "blocked_pi_identity")
        self.assertIn("172.16.0.2", summary["nextAction"])

    def test_stale_listener_fails(self) -> None:
        record = base_record()
        items = pi_items(stale_listener=True)
        record["piIdentity"]["identityChecks"] = {"ok": False, "items": items}
        checked = live_bench_preflight.validate_preflight_record(record)
        self.assertFalse(checked["ok"])
        self.assertIn("stalePiListener", failure_codes(checked))

    def test_missing_coordinator_usb_fails(self) -> None:
        record = base_record()
        items = pi_items(missing_usb=True)
        record["piIdentity"]["identityChecks"] = {"ok": False, "items": items}
        record["piIdentity"]["coordinatorEsp32Identity"] = {
            "ok": False,
            "error": "coordinator USB serial device missing",
            "parsedIdentity": live_bench_preflight.parse_esptool_identity({}),
        }
        checked = live_bench_preflight.validate_preflight_record(record)
        self.assertFalse(checked["ok"])
        self.assertIn("coordinatorUsbMissing", failure_codes(checked))

    def test_missing_pi_esptool_has_specific_blocker(self) -> None:
        record = base_record()
        record["piIdentity"]["coordinatorEsp32Identity"] = {
            "ok": False,
            "error": "Pi esptool command is not available",
            "commands": {
                command: {"returncode": 127, "stdout": ["esptool not found"], "stderr": []}
                for command in live_bench_preflight.ALLOWED_ESPTOOL_COMMANDS
            },
            "parsedIdentity": live_bench_preflight.parse_esptool_identity({}),
        }
        checked = live_bench_preflight.validate_preflight_record(record)
        self.assertFalse(checked["ok"])
        self.assertIn("piCoordinatorToolMissing", failure_codes(checked))
        summary = live_bench_preflight.summarize_preflight_record(checked)
        self.assertEqual(summary["readiness"], "blocked_pi_esptool")

    def test_malformed_esptool_output_fails(self) -> None:
        record = base_record()
        record["peerEsp32Identities"]["ports"]["COM4"] = identity(
            "78:e3:6d:0a:90:14",
            malformed=True,
        )
        checked = live_bench_preflight.validate_preflight_record(record)
        self.assertFalse(checked["ok"])
        self.assertIn("malformedPeerIdentity", failure_codes(checked))
        self.assertIn("missingMac", failure_codes(checked))


if __name__ == "__main__":
    unittest.main()
