#!/usr/bin/env python3
"""Regression tests for the ESP-NOW BBS live prepare/flash gate."""

from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace


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


def sha256(path: Path) -> str:
    return espnow_bbs_live_gate.sha256_file(path)


def write_json(path: Path, payload: dict[str, object] | list[object]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def completion_transcript() -> list[dict[str, object]]:
    peers = [
        {"id": "peer01", "link": "espnow-enc", "rx": 126, "tx": 126, "acks": 126},
        {"id": "peer02", "link": "espnow-enc", "rx": 126, "tx": 126, "acks": 126},
        {"id": "peer03", "link": "espnow-enc", "rx": 126, "tx": 126, "acks": 126},
    ]
    return [
        {"request": {"type": "hello"}, "response": {"type": "hello", "serial_errors": 0}},
        {"request": {"type": "state_get"}, "response": {"type": "state", "rx": 126, "tx": 126, "acks": 126}},
        {"request": {"type": "peer_list"}, "response": {"type": "peer_list", "peers": peers}},
        {"request": {"type": "diag_get"}, "response": {"type": "diag", "rx": 129, "tx": 129, "acks": 129, "serial_errors": 0}},
        {"request": {"type": "fw_inventory"}, "response": {"type": "fw_inventory", "peers": peers}},
        {"request": {"type": "msg_post"}, "response": {"type": "ack", "message": "msg_post"}},
        {"request": {"type": "msg_pull"}, "response": {"type": "msg_pull", "messages": []}},
        {"request": {"type": "msg_search"}, "response": {"type": "msg_search", "messages": []}},
        {"request": {"type": "msg_ack"}, "response": {"type": "ack", "message": "msg_ack"}},
    ]


class CompletionGateTests(unittest.TestCase):
    def write_completion_fixture(
        self,
        root: Path,
        *,
        vision_ok: bool = True,
        transcript_payload: list[dict[str, object]] | None = None,
    ) -> SimpleNamespace:
        backups: dict[str, object] = {}
        builds: dict[str, object] = {}
        devices: dict[str, object] = {}
        for role in espnow_bbs_live_gate.FLASH_ORDER:
            backup = root / f"{role}-backup.bin"
            backup.write_bytes(f"backup-{role}".encode("ascii"))
            build_file = root / f"{role}.bin"
            build_file.write_bytes(f"build-{role}".encode("ascii"))
            backups[role] = {
                "path": str(backup),
                "sha256": sha256(backup),
                "bytes": backup.stat().st_size,
            }
            builds[role] = {
                "writeFlashArgs": ["--flash-mode", "dio"],
                "files": [
                    {
                        "offset": "0x1000",
                        "path": str(build_file),
                        "sha256": sha256(build_file),
                        "bytes": build_file.stat().st_size,
                    }
                ],
            }
            devices[role] = {"role": role}

        manifest_path = root / "manifest.json"
        write_json(
            manifest_path,
            {
                "devices": devices,
                "backups": backups,
                "builds": builds,
                "flashGate": {
                    "requiresConfirmWriteFlash": True,
                    "flashOrder": espnow_bbs_live_gate.FLASH_ORDER,
                },
            },
        )
        flash_path = root / "flash-evidence.json"
        write_json(
            flash_path,
            {
                "ok": True,
                "manifest": str(manifest_path),
                "results": {
                    role: {
                        "writeFlash": {"returncode": 0},
                        "verifyFlash": {"returncode": 0},
                    }
                    for role in espnow_bbs_live_gate.FLASH_ORDER
                },
            },
        )
        transcript_path = root / "bridge-json-transcript.json"
        write_json(transcript_path, transcript_payload or completion_transcript())
        cleanup_path = root / "cleanup.txt"
        cleanup_path.write_text(
            "\n".join(
                [
                    "no dosbox-x process",
                    "no zenity modal",
                    "no espnow_bbs_bridge.py process",
                    "31331 listener none",
                    "31332 listener none",
                    "8080 listener none",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        vision_path = root / "vision-gate.json"
        write_json(
            vision_path,
            {
                "ok": vision_ok,
                "status": "pass" if vision_ok else "needs_manual_review",
                "screenshots": [{"path": "opcon.png", "sha256": "0" * 64}],
                "views": {
                    "opcon_dashboard": {"ok": vision_ok, "required": True},
                    "peers": {"ok": True, "required": True},
                    "message_board": {"ok": True, "required": True},
                    "network": {"ok": True, "required": True},
                    "diagnostics": {"ok": True, "required": True},
                    "safety": {"ok": True, "required": True},
                    "disabled_unsafe_controls": {"ok": True, "required": True},
                },
                "transcript": {"ok": True},
                "cleanup": {"ok": True},
            },
        )
        return SimpleNamespace(
            manifest=manifest_path,
            flash_evidence=flash_path,
            bridge_transcript=transcript_path,
            cleanup_proof=cleanup_path,
            vision_gate=vision_path,
            out=root / "completion.json",
        )

    def test_complete_gate_passes_with_transcript_cleanup_and_vision(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = self.write_completion_fixture(Path(tmp))
            status = espnow_bbs_live_gate.command_complete(fixture)
            payload = json.loads(fixture.out.read_text(encoding="utf-8"))
        self.assertEqual(status, 0)
        self.assertTrue(payload["ok"], payload.get("failures"))

    def test_complete_gate_fails_when_vision_gate_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = self.write_completion_fixture(Path(tmp), vision_ok=False)
            status = espnow_bbs_live_gate.command_complete(fixture)
            payload = json.loads(fixture.out.read_text(encoding="utf-8"))
        self.assertEqual(status, 2)
        self.assertFalse(payload["ok"])
        self.assertIn("vision_gate_not_pass", payload["failures"])


if __name__ == "__main__":
    unittest.main()
