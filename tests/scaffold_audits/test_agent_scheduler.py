#!/usr/bin/env python3
"""Regression tests for the host-only Codex window scheduler."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import agent_scheduler as scheduler  # noqa: E402
import server_lifecycle  # noqa: E402


HOOK = ROOT / ".codex" / "hooks" / "pre_tool_use_agent_process.py"
SCHEDULER = ROOT / "scripts" / "agent_scheduler.py"


def free_tcp_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_for_tcp(host: str, port: int, *, present: bool, timeout: float = 5.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.2):
                is_present = True
        except OSError:
            is_present = False
        if is_present == present:
            return True
        time.sleep(0.05)
    return False


def pid_alive(pid: int) -> bool:
    try:
        fields = (Path("/proc") / str(pid) / "stat").read_text(encoding="utf-8").split()
        if len(fields) > 2 and fields[2] == "Z":
            return False
    except OSError:
        pass
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


class SchedulerFixture:
    def __init__(self, baseline_dirty: list[str] | None = None) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="esp32-scheduler-test-")
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        (self.repo / ".agents" / "TASK_LOG").mkdir(parents=True)
        (self.repo / ".agents" / "handoffs").mkdir(parents=True)
        self.old_state = os.environ.get(scheduler.STATE_ENV)
        os.environ[scheduler.STATE_ENV] = str(self.root / "state")
        self.core = scheduler.SchedulerCore(self.repo, baseline_dirty=baseline_dirty or [])

    def cleanup(self) -> None:
        if self.old_state is None:
            os.environ.pop(scheduler.STATE_ENV, None)
        else:
            os.environ[scheduler.STATE_ENV] = self.old_state
        self.temp.cleanup()


class ServerLifecycleTests(unittest.TestCase):
    def make_paths(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
        temp = tempfile.TemporaryDirectory(prefix="esp32-lifecycle-test-")
        root = Path(temp.name)
        repo = root / "repo"
        state = root / "state"
        repo.mkdir()
        state.mkdir()
        self.addCleanup(temp.cleanup)
        return temp, repo, state

    def test_lifecycle_metadata_lives_outside_repo(self) -> None:
        _, repo, state = self.make_paths()

        path = server_lifecycle.metadata_path(
            tool_name="unit-tool",
            host="127.0.0.1",
            port=31331,
            cwd=repo,
            state_dir=state,
        )

        self.assertTrue(str(path).startswith(str(state)))
        with self.assertRaises(ValueError):
            path.relative_to(repo)

    def test_stale_metadata_is_removed_when_pid_is_gone(self) -> None:
        _, repo, state = self.make_paths()
        path = server_lifecycle.write_metadata(
            tool_name="unit-tool",
            host="127.0.0.1",
            port=free_tcp_port(),
            command_marker="unit-marker",
            cwd=repo,
            state_dir=state,
            pid=99999999,
        )
        self.assertTrue(path.exists())

        result = server_lifecycle.prepare_for_reopen(
            tool_name="unit-tool",
            host="127.0.0.1",
            port=int(json.loads(path.read_text(encoding="utf-8"))["port"]),
            command_marker="unit-marker",
            cwd=repo,
            state_dir=state,
        )

        self.assertTrue(result.ok)
        self.assertIn("stale_metadata_removed", result.actions)
        self.assertFalse(path.exists())

    def test_recorded_same_tool_process_is_gracefully_stopped(self) -> None:
        _, repo, state = self.make_paths()
        port = free_tcp_port()
        script = repo / "owned_listener.py"
        marker = "owned-lifecycle-marker"
        script.write_text(
            "\n".join(
                [
                    "import signal",
                    "import socket",
                    "import sys",
                    "import time",
                    "stop = False",
                    "def handle(_signum, _frame):",
                    "    global stop",
                    "    stop = True",
                    "signal.signal(signal.SIGTERM, handle)",
                    "sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)",
                    "sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)",
                    "sock.bind(('127.0.0.1', int(sys.argv[1])))",
                    "sock.listen()",
                    "print('ready', flush=True)",
                    "while not stop:",
                    "    time.sleep(0.05)",
                    "sock.close()",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        proc = subprocess.Popen(
            [sys.executable, str(script), str(port), marker],
            cwd=repo,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        self.addCleanup(lambda: proc.poll() is None and proc.kill())
        assert proc.stdout is not None
        self.assertEqual("ready", proc.stdout.readline().strip())
        self.assertTrue(wait_for_tcp("127.0.0.1", port, present=True))
        metadata = server_lifecycle.write_metadata(
            tool_name="unit-owned",
            host="127.0.0.1",
            port=port,
            command_marker=marker,
            cwd=repo,
            state_dir=state,
            pid=proc.pid,
        )

        result = server_lifecycle.prepare_for_reopen(
            tool_name="unit-owned",
            host="127.0.0.1",
            port=port,
            command_marker=marker,
            cwd=repo,
            state_dir=state,
            graceful_timeout=2.0,
        )

        proc.wait(timeout=3)
        if proc.stdout is not None:
            proc.stdout.close()
        if proc.stderr is not None:
            proc.stderr.close()
        self.assertTrue(result.ok)
        self.assertIn("process_sigterm", result.actions)
        self.assertIn("process_stopped", result.actions)
        self.assertFalse(metadata.exists())
        self.assertTrue(wait_for_tcp("127.0.0.1", port, present=False))

    def test_unrecorded_listener_fails_closed_and_is_not_killed(self) -> None:
        _, repo, state = self.make_paths()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            listener.bind(("127.0.0.1", 0))
            listener.listen()
            port = int(listener.getsockname()[1])

            with self.assertRaises(server_lifecycle.LifecycleError) as raised:
                server_lifecycle.prepare_for_reopen(
                    tool_name="unit-unowned",
                    host="127.0.0.1",
                    port=port,
                    command_marker="unit-marker",
                    cwd=repo,
                    state_dir=state,
                )

            self.assertEqual("listener_in_use_unowned", raised.exception.reason)
            self.assertTrue(wait_for_tcp("127.0.0.1", port, present=True))


class AgentSchedulerTests(unittest.TestCase):
    def make_fixture(self, baseline_dirty: list[str] | None = None) -> SchedulerFixture:
        fixture = SchedulerFixture(baseline_dirty)
        self.addCleanup(fixture.cleanup)
        return fixture

    def open_window(self, core: scheduler.SchedulerCore, role: str = "worker") -> str:
        response = core.open_window(role=role)
        self.assertTrue(response["ok"], response)
        return response["window"]["id"]

    def dispatch_server(self, core: scheduler.SchedulerCore) -> scheduler.SchedulerServer:
        server = object.__new__(scheduler.SchedulerServer)
        server.core = core
        return server

    def start_daemon(self, fixture: SchedulerFixture) -> scheduler.StatePaths:
        result = scheduler.daemon_start(fixture.repo)
        self.assertTrue(result["ok"], result)
        paths = scheduler.state_paths(fixture.repo)
        self.assertTrue(paths.pid.exists(), result)
        self.addCleanup(lambda: scheduler.daemon_stop(fixture.repo))
        return paths

    def acquire_write(
        self,
        core: scheduler.SchedulerCore,
        window_id: str,
        path: str,
        lease_seconds: int = scheduler.CLAIM_LEASE_SECONDS,
    ) -> dict[str, object]:
        return core.acquire_claim(
            window_id=window_id,
            tier="Tier 2",
            owner_role="Tooling",
            path_globs=[path],
            mode="write",
            validation_plan="unit test",
            lease_seconds=lease_seconds,
        )

    def test_five_windows_can_hold_disjoint_write_claims(self) -> None:
        fixture = self.make_fixture()
        windows = [self.open_window(fixture.core, role=f"role-{index}") for index in range(5)]

        for index, window_id in enumerate(windows):
            with self.subTest(index=index):
                response = self.acquire_write(fixture.core, window_id, f"scripts/disjoint-{index}.py")
                self.assertTrue(response["ok"], response)

        status = fixture.core.status()
        self.assertEqual(5, status["activeWindowCount"])
        self.assertEqual(5, len([claim for claim in status["claims"] if claim["status"] == "active"]))

    def test_sixth_window_is_deterministically_rejected_or_queued(self) -> None:
        fixture = self.make_fixture()
        for index in range(5):
            self.open_window(fixture.core, role=f"role-{index}")

        rejected = fixture.core.open_window(role="sixth", on_full="reject")
        self.assertFalse(rejected["ok"])
        self.assertEqual("max-active-windows", rejected["reason"])

        queued = fixture.core.open_window(role="sixth", on_full="queue")
        self.assertTrue(queued["ok"], queued)
        self.assertEqual("queued", queued["window"]["status"])

    def test_overlapping_write_claim_is_rejected(self) -> None:
        fixture = self.make_fixture()
        first = self.open_window(fixture.core, role="first")
        second = self.open_window(fixture.core, role="second")
        self.assertTrue(self.acquire_write(fixture.core, first, "scripts/*.py")["ok"])

        conflict = self.acquire_write(fixture.core, second, "scripts/agent_scheduler.py")

        self.assertFalse(conflict["ok"], conflict)
        self.assertEqual("overlapping-write-claim", conflict["reason"])
        self.assertIn("conflicts", conflict)

    def test_read_claim_warns_when_active_write_exists(self) -> None:
        fixture = self.make_fixture()
        writer = self.open_window(fixture.core, role="writer")
        reader = self.open_window(fixture.core, role="reader")
        self.assertTrue(self.acquire_write(fixture.core, writer, "scripts/agent_scheduler.py")["ok"])

        response = fixture.core.acquire_claim(
            window_id=reader,
            tier="Tier 2",
            owner_role="QA",
            path_globs=["docs/index.md"],
            mode="review",
            validation_plan="unit test",
        )

        self.assertTrue(response["ok"], response)
        self.assertTrue(any("stale-evidence-warning" in item for item in response["warnings"]))
        self.assertEqual(1, len(response["staleEvidence"]))

    def test_stale_lease_expiry_records_reap_event(self) -> None:
        fixture = self.make_fixture()
        window_id = self.open_window(fixture.core)
        response = self.acquire_write(fixture.core, window_id, "docs/stale.md", lease_seconds=0)
        self.assertTrue(response["ok"], response)

        status = fixture.core.status()

        self.assertTrue(any(item["target"] == "claim" for item in status["reaped"]))
        self.assertTrue(
            any(event["event_type"] == "stale-reap" for event in status["events"]),
            status["events"],
        )

    def test_dispatch_claim_acquire_preserves_zero_lease(self) -> None:
        fixture = self.make_fixture()
        server = self.dispatch_server(fixture.core)
        window = server.dispatch({"op": "window_open", "role": "worker"})["window"]["id"]

        response = server.dispatch(
            {
                "op": "claim_acquire",
                "window_id": window,
                "tier": "Tier 2",
                "owner_role": "Tooling",
                "path_globs": ["docs/dispatch-zero.md"],
                "mode": "write",
                "validation_plan": "unit test",
                "lease_seconds": 0,
            }
        )
        self.assertTrue(response["ok"], response)
        claim_id = response["claim"]["id"]

        status = server.dispatch({"op": "status"})

        self.assertTrue(
            any(item["target"] == "claim" and item["claim"]["id"] == claim_id for item in status["reaped"]),
            status["reaped"],
        )
        self.assertFalse(any(claim["id"] == claim_id and claim["status"] == "active" for claim in status["claims"]))

    def test_dispatch_claim_renew_preserves_zero_lease(self) -> None:
        fixture = self.make_fixture()
        server = self.dispatch_server(fixture.core)
        window = server.dispatch({"op": "window_open", "role": "worker"})["window"]["id"]
        acquired = server.dispatch(
            {
                "op": "claim_acquire",
                "window_id": window,
                "tier": "Tier 2",
                "owner_role": "Tooling",
                "path_globs": ["docs/dispatch-renew-zero.md"],
                "mode": "write",
                "validation_plan": "unit test",
            }
        )
        self.assertTrue(acquired["ok"], acquired)
        claim_id = acquired["claim"]["id"]

        renewed = server.dispatch({"op": "claim_renew", "claim_id": claim_id, "lease_seconds": 0})
        self.assertTrue(renewed["ok"], renewed)
        status = server.dispatch({"op": "status"})

        self.assertTrue(
            any(item["target"] == "claim" and item["claim"]["id"] == claim_id for item in status["reaped"]),
            status["reaped"],
        )
        self.assertFalse(any(claim["id"] == claim_id and claim["status"] == "active" for claim in status["claims"]))

    def test_dispatch_claim_lease_defaults_only_for_missing_none_or_blank(self) -> None:
        samples = [
            ("missing", {}),
            ("none", {"lease_seconds": None}),
            ("empty", {"lease_seconds": ""}),
            ("blank", {"lease_seconds": "   "}),
        ]
        for label, lease_payload in samples:
            with self.subTest(label=label):
                fixture = self.make_fixture()
                server = self.dispatch_server(fixture.core)
                window = server.dispatch({"op": "window_open", "role": "worker"})["window"]["id"]
                request = {
                    "op": "claim_acquire",
                    "window_id": window,
                    "tier": "Tier 2",
                    "owner_role": "Tooling",
                    "path_globs": [f"docs/dispatch-default-{label}.md"],
                    "mode": "read",
                    "validation_plan": "unit test",
                }
                request.update(lease_payload)

                response = server.dispatch(request)
                status = server.dispatch({"op": "status"})

                self.assertTrue(response["ok"], response)
                self.assertEqual([], status["reaped"])
                self.assertTrue(
                    any(claim["id"] == response["claim"]["id"] and claim["status"] == "active" for claim in status["claims"]),
                    status["claims"],
                )

    def test_dispatch_claim_lease_rejects_invalid_nonblank_values(self) -> None:
        fixture = self.make_fixture()
        server = self.dispatch_server(fixture.core)
        window = server.dispatch({"op": "window_open", "role": "worker"})["window"]["id"]

        with self.assertRaises(ValueError):
            server.dispatch(
                {
                    "op": "claim_acquire",
                    "window_id": window,
                    "tier": "Tier 2",
                    "owner_role": "Tooling",
                    "path_globs": ["docs/dispatch-invalid.md"],
                    "mode": "read",
                    "validation_plan": "unit test",
                    "lease_seconds": "not-an-int",
                }
            )

    def test_dirty_baseline_overlap_emits_warning_and_ack_field(self) -> None:
        fixture = self.make_fixture(baseline_dirty=["docs/dirty.md"])
        window_id = self.open_window(fixture.core)

        response = fixture.core.acquire_claim(
            window_id=window_id,
            tier="Tier 2",
            owner_role="Docs",
            path_globs=["docs/dirty.md"],
            mode="read",
            validation_plan="unit test",
        )

        self.assertTrue(response["ok"], response)
        self.assertEqual(["docs/dirty.md"], response["dirtyBaselineOverlap"])
        self.assertFalse(response["dirtyBaselineAcknowledged"])
        self.assertTrue(any("dirty-baseline-overlap" in item for item in response["warnings"]))

    def test_concurrent_task_log_and_handoff_reservations_are_unique(self) -> None:
        fixture = self.make_fixture()
        results: list[dict[str, object]] = []
        lock = threading.Lock()

        def reserve(kind: str) -> None:
            response = fixture.core.reserve_record(kind=kind, slug=f"{kind}-unit")
            with lock:
                results.append(response)

        threads = [
            threading.Thread(target=reserve, args=("task-log",)),
            threading.Thread(target=reserve, args=("task-log",)),
            threading.Thread(target=reserve, args=("handoff",)),
            threading.Thread(target=reserve, args=("handoff",)),
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        by_kind: dict[str, list[int]] = {"task-log": [], "handoff": []}
        for result in results:
            self.assertTrue(result["ok"], result)
            by_kind[str(result["kind"])].append(int(result["ordinal"]))
        self.assertEqual([1, 2], sorted(by_kind["task-log"]))
        self.assertEqual([1, 2], sorted(by_kind["handoff"]))

    def test_daemon_restart_stops_running_daemon_and_starts_fresh(self) -> None:
        fixture = self.make_fixture()
        paths = self.start_daemon(fixture)
        old_pid = int(paths.pid.read_text(encoding="utf-8"))

        restarted = scheduler.daemon_restart(fixture.repo)

        self.assertTrue(restarted["ok"], restarted)
        self.assertEqual("restarted", restarted["status"])
        new_pid = int(paths.pid.read_text(encoding="utf-8"))
        self.assertNotEqual(old_pid, new_pid)
        self.assertFalse(pid_alive(old_pid))

    def test_daemon_start_replace_existing_replaces_recorded_daemon(self) -> None:
        fixture = self.make_fixture()
        paths = self.start_daemon(fixture)
        old_pid = int(paths.pid.read_text(encoding="utf-8"))

        replaced = scheduler.daemon_start(fixture.repo, replace_existing=True)

        self.assertTrue(replaced["ok"], replaced)
        self.assertEqual("started", replaced["status"])
        new_pid = int(paths.pid.read_text(encoding="utf-8"))
        self.assertNotEqual(old_pid, new_pid)
        self.assertFalse(pid_alive(old_pid))

    def test_stale_socket_and_pid_files_do_not_block_restart(self) -> None:
        fixture = self.make_fixture()
        paths = scheduler.state_paths(fixture.repo)
        paths.state_dir.mkdir(parents=True, exist_ok=True)
        paths.socket.write_text("stale socket", encoding="utf-8")
        paths.pid.write_text("99999999", encoding="utf-8")
        server_lifecycle.write_metadata(
            tool_name=scheduler.DAEMON_TOOL_NAME,
            host="unix",
            port=0,
            endpoint="unix",
            socket_path=paths.socket,
            command_marker=scheduler.DAEMON_COMMAND_MARKER,
            cwd=paths.repo,
            state_dir=paths.state_dir / "server-lifecycle",
            pid=99999999,
        )
        self.addCleanup(lambda: scheduler.daemon_stop(fixture.repo))

        restarted = scheduler.daemon_restart(fixture.repo)

        self.assertTrue(restarted["ok"], restarted)
        self.assertEqual("restarted", restarted["status"])
        self.assertTrue(scheduler.daemon_status(fixture.repo).get("running"))

    def test_default_daemon_ensure_remains_non_destructive(self) -> None:
        fixture = self.make_fixture()
        paths = self.start_daemon(fixture)
        old_pid = int(paths.pid.read_text(encoding="utf-8"))

        ensured = scheduler.daemon_start(fixture.repo)

        self.assertTrue(ensured["ok"], ensured)
        self.assertEqual("already-running", ensured["status"])
        self.assertEqual(old_pid, int(paths.pid.read_text(encoding="utf-8")))
        self.assertTrue(pid_alive(old_pid))

    def test_bypass_permissions_hook_path_is_advisory_only(self) -> None:
        with tempfile.TemporaryDirectory(prefix="esp32-scheduler-hook-") as tmp:
            env = os.environ.copy()
            env[scheduler.STATE_ENV] = str(Path(tmp) / "state")
            prompt = (
                "Verified facts: hook fixture. Assumptions: none. Unknowns: none. "
                "Selected tier: Tier 2. Owner role: QA. Evidence need: local. "
                "Mutation boundary: tests. Validation plan: unittest."
            )
            payload = {
                "tool_name": "functions.exec_command",
                "permission_mode": "bypassPermissions",
                "tool_input": {"cmd": "touch advisory-only"},
                "prompt": prompt,
            }
            result = subprocess.run(
                [sys.executable, str(HOOK)],
                input=json.dumps(payload),
                text=True,
                capture_output=True,
                check=False,
                env=env,
            )

        self.assertEqual(0, result.returncode)
        self.assertEqual("", result.stderr)
        data = json.loads(result.stdout)
        hook = data["hookSpecificOutput"]
        self.assertNotIn("permissionDecision", hook)
        self.assertNotIn("decision", data)
        context = hook["additionalContext"]
        self.assertIn("scheduler-unavailable", context)
        self.assertIn("permission_mode=bypassPermissions", context)
        self.assertIn("no deny/block", context)

    def test_pretool_check_daemon_unavailable_fallback_is_advisory(self) -> None:
        with tempfile.TemporaryDirectory(prefix="esp32-scheduler-pretool-") as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            env = os.environ.copy()
            env[scheduler.STATE_ENV] = str(Path(tmp) / "state")
            payload = {
                "tool_name": "functions.exec_command",
                "tool_input": {"cmd": "touch advisory-only"},
                "permission_mode": "bypassPermissions",
            }
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCHEDULER),
                    "pretool-check",
                    "--repo",
                    str(repo),
                    "--hook-json",
                    json.dumps(payload),
                ],
                text=True,
                capture_output=True,
                check=False,
                env=env,
            )

        self.assertEqual(0, result.returncode)
        self.assertEqual("", result.stderr)
        data = json.loads(result.stdout)
        hook = data["hookSpecificOutput"]
        self.assertEqual("PreToolUse", hook["hookEventName"])
        self.assertNotIn("permissionDecision", hook)
        self.assertIn("scheduler-unavailable", hook["additionalContext"])
        self.assertIn("no deny/block", hook["additionalContext"])


if __name__ == "__main__":
    unittest.main()
