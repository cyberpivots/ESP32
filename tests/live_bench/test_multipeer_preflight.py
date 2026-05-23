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
            "chip_id": {"returncode": 0, "stdout": ["esptool.py v5.0"], "stderr": []},
            "read_mac": {"returncode": 0, "stdout": ["no mac here"], "stderr": []},
            "flash_id": {"returncode": 0, "stdout": ["no flash size"], "stderr": []},
        }
    else:
        commands = {
            "chip_id": {
                "returncode": 0,
                "stdout": ["Chip is ESP32-D0WDQ6 (revision v1.0)"],
                "stderr": [],
            },
            "read_mac": {"returncode": 0, "stdout": [f"MAC: {mac}"], "stderr": []},
            "flash_id": {
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
        self.assertFalse(live_bench_preflight.uses_expected_pi_profile("192.168.200.104"))

    def test_pi_coordinator_identity_uses_no_stub(self) -> None:
        script = live_bench_preflight.build_pi_remote_script("/dev/ttyUSB0", False)
        self.assertIn('--no-stub --port "$COORDINATOR_PORT"', script)

    def test_good_inventory_maps_ports_by_order(self) -> None:
        record = live_bench_preflight.validate_preflight_record(base_record())
        self.assertTrue(record["ok"])
        self.assertEqual(record["peerMap"]["peer01"]["windowsPort"], "COM4")
        self.assertEqual(record["peerMap"]["peer02"]["windowsPort"], "COM5")
        self.assertEqual(record["peerMap"]["peer03"]["windowsPort"], "COM6")
        self.assertEqual(record["coordinatorMap"]["mac"], "78:e3:6d:10:4d:6c")

    def test_summary_reports_ready_gate_without_command_logs(self) -> None:
        record = live_bench_preflight.validate_preflight_record(base_record())
        summary = live_bench_preflight.summarize_preflight_record(record)
        self.assertTrue(summary["ok"])
        self.assertEqual(summary["readiness"], "ready_for_prepare")
        self.assertEqual(summary["peers"]["COM4"]["mac"], "78:e3:6d:0a:90:14")
        self.assertNotIn("commands", summary["peers"]["COM4"])

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
