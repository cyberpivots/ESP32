#!/usr/bin/env python3
"""Hardware-free tests for the XBee radio study wrapper."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import xbee_radio_study as study  # noqa: E402


class XBeeRadioStudyTests(unittest.TestCase):
    def test_emit_writes_out_under_safe_bench_root(self) -> None:
        study.OUT_ROOT.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=study.OUT_ROOT) as tmp:
            out_path = Path(tmp) / "record.json"
            record = study.base_record("inventory")
            with mock.patch("builtins.print"):
                exit_code = study.emit(record, argparse.Namespace(out=out_path))

            written = json.loads(out_path.read_text(encoding="utf-8"))

        self.assertEqual(0, exit_code)
        self.assertEqual("inventory", written["command"])
        self.assertEqual(study.repository_relative(out_path), written["outputPath"])

    def test_out_rejects_paths_outside_bench_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "record.json"
            with self.assertRaises(study.StudyError) as ctx:
                study.write_optional_output(study.base_record("inventory"), out_path)

        self.assertEqual("invalid_output_path", ctx.exception.code)

    def test_inventory_does_not_open_serial_ports(self) -> None:
        args = argparse.Namespace(local_show_identifiers=False)
        with (
            mock.patch.object(study.probe, "open_serial_port", side_effect=AssertionError("serial opened")),
            mock.patch.object(study.probe, "collect_serial_candidates", return_value=[]),
            mock.patch.object(study.probe, "collect_windows_com_hints", return_value={"ports": []}),
            mock.patch.object(study, "collect_windows_pnp", return_value={"devices": []}),
        ):
            record = study.command_inventory(args)

        self.assertTrue(record["ok"])
        self.assertFalse(record["serialOpenAttempted"])
        self.assertFalse(record["serialWritesAttempted"])
        self.assertFalse(record["serial"]["serialOpenAttempted"])
        self.assertFalse(record["v1Boundary"]["inventoryOpensSerialPorts"])

    def test_identity_delta_is_file_only_and_redacts_device_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            before = tmp_path / "before.json"
            after = tmp_path / "after.json"
            before.write_text(
                json.dumps(
                    {
                        "serial": {
                            "windowsPnp": {
                                "devices": [
                                    {
                                        "name": "Silicon Labs CP210x USB to UART Bridge (COM13)",
                                        "manufacturer": "Silicon Labs",
                                        "status": "OK",
                                        "deviceId": "USB\\\\VID_10C4&PID_EA60\\\\SECRET-A",
                                    }
                                ]
                            },
                            "windowsComHints": {"ports": [{"windowsPort": "COM13", "wslLegacyHint": "/dev/ttyS12"}]},
                        }
                    }
                ),
                encoding="utf-8",
            )
            after.write_text(
                json.dumps(
                    {
                        "serial": {
                            "windowsPnp": {
                                "devices": [
                                    {
                                        "name": "Silicon Labs CP210x USB to UART Bridge (COM14)",
                                        "manufacturer": "Silicon Labs",
                                        "status": "OK",
                                        "deviceId": "USB\\\\VID_10C4&PID_EA60\\\\SECRET-B",
                                    }
                                ]
                            },
                            "windowsComHints": {"ports": [{"windowsPort": "COM14", "wslLegacyHint": "/dev/ttyS13"}]},
                        }
                    }
                ),
                encoding="utf-8",
            )
            args = argparse.Namespace(before=before, after=after)
            with mock.patch.object(study.probe, "open_serial_port", side_effect=AssertionError("serial opened")):
                record = study.command_identity_delta(args)

        rendered = json.dumps(record)
        self.assertTrue(record["ok"])
        self.assertFalse(record["serialOpenAttempted"])
        self.assertFalse(record["serialWritesAttempted"])
        self.assertEqual(2, record["summary"]["added"])
        self.assertEqual(2, record["summary"]["removed"])
        self.assertNotIn("SECRET-A", rendered)
        self.assertNotIn("SECRET-B", rendered)
        self.assertNotIn("VID_10C4", rendered)

    def test_local_tool_presence_expands_known_path_globs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            tool_path = tmp_path / "Users" / "cyber" / "AppData" / "Local" / "Digi" / "XCTU-NG" / "XCTU.exe"
            tool_path.parent.mkdir(parents=True)
            tool_path.write_text("stub", encoding="utf-8")

            record = study.local_tool_presence(
                "xctu",
                [str(tmp_path / "Users" / "*" / "AppData" / "Local" / "Digi" / "XCTU-NG" / "XCTU.exe")],
            )

        self.assertIn(str(tool_path), record["knownInstallPathsFound"])

    def test_windows_pnp_default_output_redacts_raw_device_ids(self) -> None:
        raw_line = (
            '[{"Name":"Silicon Labs CP210x USB to UART Bridge (COM13)",'
            '"Manufacturer":"Silicon Labs","PNPClass":"Ports","Status":"OK",'
            '"DeviceID":"USB\\\\VID_10C4&PID_EA60\\\\ABC123"}]'
        )
        with (
            mock.patch.object(study.shutil, "which", return_value="powershell.exe"),
            mock.patch.object(
                study.probe,
                "run_short_command",
                return_value={"available": True, "returncode": 0, "lines": [raw_line], "stderr": []},
            ),
        ):
            record = study.collect_windows_pnp(local_show_identifiers=False)

        rendered = json.dumps(record)
        self.assertNotIn("ABC123", rendered)
        self.assertNotIn("VID_10C4", rendered)
        self.assertTrue(record["devices"][0]["deviceIdRedacted"])
        self.assertTrue(record["probe"]["rawOutputRedacted"])

    def test_readonly_requires_confirmation_before_delegation(self) -> None:
        args = argparse.Namespace(
            port="COM13",
            baud=9600,
            confirm_sends_read_commands=False,
            show_addresses=False,
        )
        with mock.patch.object(study.probe, "command_at_query", side_effect=AssertionError("delegated")):
            with self.assertRaises(study.StudyError) as ctx:
                study.command_readonly(args)

        self.assertEqual("confirmation_required", ctx.exception.code)

    def test_readonly_delegates_fixed_allowlist_after_confirmation(self) -> None:
        args = argparse.Namespace(
            port="COM13",
            baud=9600,
            confirm_sends_read_commands=True,
            show_addresses=False,
        )
        delegated = {"ok": True, "command": "at-query", "request": {"queries": list(study.READ_ONLY_AT_QUERIES)}}
        with mock.patch.object(study.probe, "command_at_query", return_value=delegated) as command_at_query:
            record = study.command_readonly(args)

        command_at_query.assert_called_once()
        self.assertEqual(list(study.READ_ONLY_AT_QUERIES), record["allowedQueries"])
        self.assertTrue(record["serialReadQueryTrafficSent"])
        self.assertFalse(record["persistentSettingWritesAttempted"])

    def test_profile_diff_is_offline_and_redacts_sensitive_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            readback = tmp_path / "readback.json"
            target = tmp_path / "target.json"
            readback.write_text(
                json.dumps(
                    {
                        "results": {
                            "AP": {"text": "1", "sha256": "ap-hash", "byteLength": 1},
                            "SH": {"text": "0013A200", "sha256": "sh-hash", "byteLength": 8},
                        }
                    }
                ),
                encoding="utf-8",
            )
            target.write_text(
                json.dumps({"targets": {"AP": "2", "SH": "0013A200", "KY": "secret", "WR": ""}}),
                encoding="utf-8",
            )
            args = argparse.Namespace(readback=readback, target=target, local_show_identifiers=False)
            with mock.patch.object(study.probe, "open_serial_port", side_effect=AssertionError("serial opened")):
                record = study.command_profile_diff(args)

        self.assertTrue(record["ok"])
        self.assertFalse(record["serialOpenAttempted"])
        self.assertFalse(record["serialWritesAttempted"])
        by_command = {item["command"]: item for item in record["diffs"]}
        self.assertEqual("diff", by_command["AP"]["status"])
        self.assertTrue(by_command["SH"]["readback"]["redacted"])
        self.assertNotIn("0013A200", json.dumps(by_command["SH"]))
        self.assertEqual("blocked_write", by_command["KY"]["status"])
        self.assertEqual("blocked_write", by_command["WR"]["status"])

    def test_profile_diff_flags_setting_value_at_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            readback = tmp_path / "readback.json"
            target = tmp_path / "target.json"
            readback.write_text(json.dumps({"results": {"AP": {"text": "1"}}}), encoding="utf-8")
            target.write_text(json.dumps({"targets": {"AP2": ""}}), encoding="utf-8")
            record = study.command_profile_diff(
                argparse.Namespace(readback=readback, target=target, local_show_identifiers=False)
            )

        violations = {(item["command"], item["reason"]) for item in record["safetyViolations"]}
        self.assertIn(("AP2", "setting_value_at_command"), violations)
        by_command = {item["command"]: item for item in record["diffs"]}
        self.assertEqual("blocked_write", by_command["AP2"]["status"])

    def test_write_plan_emits_blocked_actions_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            diff = Path(tmp) / "diff.json"
            diff.write_text(
                json.dumps(
                    {
                        "diffs": [
                            {"command": "AP", "status": "diff", "requiresWriteGate": True},
                            {"command": "AO", "status": "match", "requiresWriteGate": False},
                        ]
                    }
                ),
                encoding="utf-8",
            )
            record = study.command_write_plan(argparse.Namespace(diff=diff))

        self.assertTrue(record["ok"])
        self.assertFalse(record["applyAllowed"])
        self.assertFalse(record["applyCommandImplemented"])
        self.assertFalse(record["serialOpenAttempted"])
        self.assertFalse(record["serialWritesAttempted"])
        blocked_text = " ".join(record["blockedOperations"])
        for marker in ["WR", "AC", "firmware", "API transmit"]:
            self.assertIn(marker, blocked_text)
        self.assertEqual(1, len(record["proposedActions"]))
        self.assertEqual("blocked_pending_tier3", record["proposedActions"][0]["reviewStatus"])

    def test_xctu_discovery_plan_is_locked_and_does_not_touch_serial(self) -> None:
        args = argparse.Namespace(ports=["com13", "COM14"])
        with (
            mock.patch.object(study.probe, "open_serial_port", side_effect=AssertionError("serial opened")),
            mock.patch.object(study.probe, "run_short_command", side_effect=AssertionError("subprocess launched")),
        ):
            record = study.command_xctu_discovery_plan(args)

        self.assertTrue(record["ok"])
        self.assertEqual(["COM13", "COM14"], record["requestedPorts"])
        self.assertEqual("locked_pending_prerequisites", record["gateStatus"])
        self.assertFalse(record["serialOpenAttempted"])
        self.assertFalse(record["serialWritesAttempted"])
        self.assertFalse(record["xctuLaunchAttempted"])
        self.assertFalse(record["xctuDiscoveryAttempted"])
        blocked_text = " ".join(record["blockedOperations"])
        for marker in ["all-port discovery", "network discovery", "firmware", "throughput"]:
            self.assertIn(marker, blocked_text)

    def test_xctu_discovery_plan_rejects_non_com_ports(self) -> None:
        with self.assertRaises(study.StudyError) as ctx:
            study.command_xctu_discovery_plan(argparse.Namespace(ports=["/dev/ttyUSB0"]))

        self.assertEqual("invalid_port", ctx.exception.code)

    def test_parser_has_expected_commands_and_no_apply_command(self) -> None:
        parser = study.build_parser()
        subparser_action = next(action for action in parser._actions if action.dest == "command")
        for command in [
            "inventory",
            "identity-delta",
            "readonly",
            "profile-diff",
            "write-plan",
            "xctu-discovery-plan",
        ]:
            self.assertIn(command, subparser_action.choices)
        self.assertNotIn("apply", subparser_action.choices)


if __name__ == "__main__":
    unittest.main()
