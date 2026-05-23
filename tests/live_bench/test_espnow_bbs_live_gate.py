#!/usr/bin/env python3
"""Regression tests for the ESP-NOW BBS live prepare/flash gate."""

from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "espnow_bbs_live_gate",
    ROOT / "scripts" / "espnow_bbs_live_gate.py",
)
assert SPEC is not None and SPEC.loader is not None
espnow_bbs_live_gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(espnow_bbs_live_gate)


class CoordinatorEsptoolSelectionTests(unittest.TestCase):
    def test_windows_peer_file_arguments_use_windows_drive_paths(self) -> None:
        device = {"portKind": "windows"}
        path = ROOT / "example.bin"
        self.assertEqual(
            espnow_bbs_live_gate.local_file_arg(device, path),
            "H:\\ESP32\\example.bin",
        )

    def test_local_peer_flash_args_translate_build_file_paths(self) -> None:
        device = {"portKind": "windows"}
        build = {
            "writeFlashArgs": ["--flash-mode", "dio"],
            "files": [{"offset": "0x1000", "path": str(ROOT / "bootloader.bin")}],
        }
        args = espnow_bbs_live_gate.write_flash_args(
            build,
            path_arg=lambda path: espnow_bbs_live_gate.local_file_arg(device, path),
        )
        self.assertEqual(args[-2:], ["0x1000", "H:\\ESP32\\bootloader.bin"])

    def test_remote_selector_prefers_proven_pi_esptool_runtime(self) -> None:
        script = espnow_bbs_live_gate.remote_esptool_setup_script()
        self.assertIn(espnow_bbs_live_gate.REMOTE_ESPNOW_ESPTOOL, script)
        self.assertIn('elif [ -x "$REMOTE_ESPNOW_ESPTOOL" ]', script)
        self.assertIn("__espnow_bbs_esptool__", script)
        self.assertIn("ESPTOOL_STUB_ARGS='--no-stub'", script)

    def test_remote_invocation_does_not_force_no_stub_for_preferred_runtime(self) -> None:
        script = espnow_bbs_live_gate.remote_esptool_invocation(
            "/dev/ttyUSB0",
            "read_flash",
            ["0", "ALL", "/tmp/full.bin"],
        )
        self.assertIn("run_esptool $ESPTOOL_STUB_ARGS --port /dev/ttyUSB0", script)
        self.assertIn("read_flash 0 ALL /tmp/full.bin", script)
        self.assertNotIn("run_esptool --no-stub --port", script)

    def test_recovery_command_names_proven_pi_esptool_runtime(self) -> None:
        commands = espnow_bbs_live_gate.recovery_commands(
            {
                "coordinator": {"target": "dospi@192.168.137.93", "port": "/dev/ttyUSB0"},
                "peer01": {
                    "tool": {"argv": ["/mnt/c/Python314/Scripts/esptool.exe"]},
                    "port": "COM4",
                },
                "peer02": {
                    "tool": {"argv": ["/mnt/c/Python314/Scripts/esptool.exe"]},
                    "port": "COM5",
                },
                "peer03": {
                    "tool": {"argv": ["/mnt/c/Python314/Scripts/esptool.exe"]},
                    "port": "COM6",
                },
            },
            {
                "coordinator": {"path": "/private/coordinator.bin"},
                "peer01": {"path": "/private/peer01.bin"},
                "peer02": {"path": "/private/peer02.bin"},
                "peer03": {"path": "/private/peer03.bin"},
            },
        )
        self.assertIn(espnow_bbs_live_gate.REMOTE_ESPNOW_ESPTOOL, commands["coordinator"])
        self.assertIn("write-flash 0x0 <backup-file>", commands["coordinator"])

    def test_idf_py_command_uses_activated_idf_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            idf_script = root / "esp-idf" / "tools" / "idf.py"
            python = root / "venv" / "bin" / "python"
            idf_script.parent.mkdir(parents=True)
            python.parent.mkdir(parents=True)
            idf_script.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
            python.write_text("#!/usr/bin/env python3\n", encoding="utf-8")
            os.chmod(idf_script, 0o755)
            os.chmod(python, 0o755)
            command = espnow_bbs_live_gate.idf_py_command(
                {
                    "PATH": "/usr/bin",
                    "IDF_PATH": str(root / "esp-idf"),
                    "IDF_PYTHON_ENV_PATH": str(root / "venv"),
                }
            )
        self.assertEqual(command, [str(python), str(idf_script)])

    def test_idf_build_command_sets_private_sdkconfig(self) -> None:
        command = espnow_bbs_live_gate.idf_build_command(
            {"PATH": "/usr/bin"},
            ROOT / "project",
            ROOT / "builds" / "peer02",
            ROOT / "sdkconfigs" / "peer02.sdkconfig",
        )
        self.assertIn("-D", command)
        self.assertIn(f"SDKCONFIG={ROOT / 'sdkconfigs' / 'peer02.sdkconfig'}", command)
        self.assertEqual(command[-1], "build")


if __name__ == "__main__":
    unittest.main()
