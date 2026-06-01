#!/usr/bin/env python3
"""Host-only lifecycle metadata for repo-owned local listeners."""

from __future__ import annotations

import dataclasses
import datetime as _dt
import hashlib
import json
import os
from pathlib import Path
import signal
import socket
import sys
import time
from collections.abc import Callable, Mapping
from typing import Any


SCHEMA_VERSION = "esp32_server_lifecycle.v1"
STATE_ENV = "ESP32_SERVER_LIFECYCLE_STATE_HOME"
DEFAULT_GRACEFUL_TIMEOUT_SECONDS = 2.0
DEFAULT_KILL_TIMEOUT_SECONDS = 1.0

_IN_PROCESS: dict[str, "LifecycleRegistration"] = {}


class LifecycleError(RuntimeError):
    """Raised when lifecycle cleanup must fail closed."""

    def __init__(self, reason: str, detail: str = "") -> None:
        self.reason = reason
        self.detail = detail
        message = reason if not detail else f"{reason}: {detail}"
        super().__init__(message)

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"ok": False, "reason": self.reason}
        if self.detail:
            result["detail"] = self.detail
        return result


@dataclasses.dataclass(frozen=True)
class LifecycleResult:
    ok: bool
    reason: str
    metadata_path: Path
    actions: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "reason": self.reason,
            "metadataPath": str(self.metadata_path),
            "actions": list(self.actions),
        }


@dataclasses.dataclass
class LifecycleRegistration:
    """In-process registration that clears metadata when closed."""

    key: str
    metadata_path: Path
    close_callback: Callable[[], None] | None = None
    closed: bool = False

    def unregister(self) -> None:
        if _IN_PROCESS.get(self.key) is self:
            _IN_PROCESS.pop(self.key, None)
        _remove_file(self.metadata_path)

    def close(self) -> None:
        if self.closed:
            return
        self.closed = True
        try:
            if self.close_callback is not None:
                self.close_callback()
        finally:
            self.unregister()


def state_root(state_dir: str | Path | None = None) -> Path:
    if state_dir is not None:
        return Path(state_dir).expanduser().resolve()
    if os.environ.get(STATE_ENV):
        return Path(os.environ[STATE_ENV]).expanduser().resolve()
    if os.environ.get("XDG_STATE_HOME"):
        root = Path(os.environ["XDG_STATE_HOME"]).expanduser().resolve()
    else:
        root = Path.home() / ".local" / "state"
    return root / "codex" / "esp32-server-lifecycle"


def metadata_path(
    *,
    tool_name: str,
    host: str,
    port: int,
    cwd: str | Path | None = None,
    endpoint: str = "tcp",
    socket_path: str | Path | None = None,
    state_dir: str | Path | None = None,
) -> Path:
    payload = _endpoint_payload(
        tool_name=tool_name,
        host=host,
        port=port,
        cwd=cwd,
        endpoint=endpoint,
        socket_path=socket_path,
    )
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()[:20]
    safe_tool = _safe_name(tool_name)
    return state_root(state_dir) / safe_tool / f"{digest}.json"


def prepare_for_reopen(
    *,
    tool_name: str,
    host: str,
    port: int,
    command_marker: str,
    cwd: str | Path | None = None,
    endpoint: str = "tcp",
    socket_path: str | Path | None = None,
    state_dir: str | Path | None = None,
    replace_existing: bool = True,
    graceful_timeout: float = DEFAULT_GRACEFUL_TIMEOUT_SECONDS,
    kill_timeout: float = DEFAULT_KILL_TIMEOUT_SECONDS,
) -> LifecycleResult:
    """Prepare a repo-owned listener endpoint before binding a replacement.

    Only an in-process registration or a recorded same-tool PID with a matching
    command marker may be closed. Live unrecorded listeners fail closed.
    """

    path = metadata_path(
        tool_name=tool_name,
        host=host,
        port=port,
        cwd=cwd,
        endpoint=endpoint,
        socket_path=socket_path,
        state_dir=state_dir,
    )
    key = _registry_key(path)
    actions: list[str] = []

    registration = _IN_PROCESS.get(key)
    if registration is not None:
        registration.close()
        actions.append("in_process_closed")

    metadata = _read_metadata(path)
    if metadata is not None:
        actions.extend(
            _prepare_recorded_process(
                metadata=metadata,
                metadata_path=path,
                tool_name=tool_name,
                host=host,
                port=port,
                command_marker=command_marker,
                cwd=cwd,
                endpoint=endpoint,
                socket_path=socket_path,
                replace_existing=replace_existing,
                graceful_timeout=graceful_timeout,
                kill_timeout=kill_timeout,
            )
        )

    if endpoint == "unix":
        sock = Path(str(socket_path or "")).expanduser()
        if sock.exists():
            if _unix_listener_present(sock):
                raise LifecycleError("listener_in_use_unowned", str(sock))
            _remove_file(sock)
            actions.append("stale_socket_removed")
    elif int(port) > 0 and _tcp_listener_present(host, int(port)):
        raise LifecycleError("listener_in_use_unowned", f"{host}:{port}")

    return LifecycleResult(
        ok=True,
        reason="ready",
        metadata_path=path,
        actions=tuple(actions),
    )


def register_instance(
    *,
    tool_name: str,
    host: str,
    port: int,
    command_marker: str,
    cwd: str | Path | None = None,
    endpoint: str = "tcp",
    socket_path: str | Path | None = None,
    state_dir: str | Path | None = None,
    close_callback: Callable[[], None] | None = None,
    extra: Mapping[str, Any] | None = None,
) -> LifecycleRegistration:
    path = write_metadata(
        tool_name=tool_name,
        host=host,
        port=port,
        command_marker=command_marker,
        cwd=cwd,
        endpoint=endpoint,
        socket_path=socket_path,
        state_dir=state_dir,
        extra=extra,
    )
    registration = LifecycleRegistration(
        key=_registry_key(path),
        metadata_path=path,
        close_callback=close_callback,
    )
    _IN_PROCESS[registration.key] = registration
    return registration


def write_metadata(
    *,
    tool_name: str,
    host: str,
    port: int,
    command_marker: str,
    cwd: str | Path | None = None,
    endpoint: str = "tcp",
    socket_path: str | Path | None = None,
    state_dir: str | Path | None = None,
    pid: int | None = None,
    extra: Mapping[str, Any] | None = None,
) -> Path:
    path = metadata_path(
        tool_name=tool_name,
        host=host,
        port=port,
        cwd=cwd,
        endpoint=endpoint,
        socket_path=socket_path,
        state_dir=state_dir,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    metadata: dict[str, Any] = {
        "schema": SCHEMA_VERSION,
        "tool_name": tool_name,
        "endpoint": endpoint,
        "host": host,
        "port": int(port),
        "socket_path": str(socket_path) if socket_path is not None else None,
        "pid": int(pid if pid is not None else os.getpid()),
        "command_marker": command_marker,
        "cwd": str(Path(cwd or os.getcwd()).expanduser().resolve()),
        "started_at": _iso_now(),
    }
    if extra:
        metadata["extra"] = dict(extra)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)
    return path


def clear_metadata(
    *,
    tool_name: str,
    host: str,
    port: int,
    cwd: str | Path | None = None,
    endpoint: str = "tcp",
    socket_path: str | Path | None = None,
    state_dir: str | Path | None = None,
) -> None:
    path = metadata_path(
        tool_name=tool_name,
        host=host,
        port=port,
        cwd=cwd,
        endpoint=endpoint,
        socket_path=socket_path,
        state_dir=state_dir,
    )
    _IN_PROCESS.pop(_registry_key(path), None)
    _remove_file(path)


def tcp_listener_present(host: str, port: int) -> bool:
    return _tcp_listener_present(host, port)


def unix_listener_present(path: str | Path) -> bool:
    return _unix_listener_present(Path(path))


def _prepare_recorded_process(
    *,
    metadata: Mapping[str, Any],
    metadata_path: Path,
    tool_name: str,
    host: str,
    port: int,
    command_marker: str,
    cwd: str | Path | None,
    endpoint: str,
    socket_path: str | Path | None,
    replace_existing: bool,
    graceful_timeout: float,
    kill_timeout: float,
) -> list[str]:
    expected = _endpoint_payload(
        tool_name=tool_name,
        host=host,
        port=port,
        cwd=cwd,
        endpoint=endpoint,
        socket_path=socket_path,
        command_marker=command_marker,
    )
    if not _metadata_matches(metadata, expected):
        raise LifecycleError("listener_in_use_unowned", str(metadata_path))
    pid = _metadata_pid(metadata)
    if pid is None or not _pid_alive(pid):
        _remove_file(metadata_path)
        return ["stale_metadata_removed"]
    if pid == os.getpid():
        if _endpoint_listener_present(endpoint, host, port, socket_path):
            raise LifecycleError("listener_in_use_owned", f"current process owns {metadata_path}")
        _remove_file(metadata_path)
        return ["stale_metadata_removed"]
    if not replace_existing:
        raise LifecycleError("listener_in_use_owned", f"pid {pid}")
    if not _process_matches(pid, command_marker, expected["cwd"]):
        raise LifecycleError("listener_in_use_unowned", f"pid {pid}")

    actions = _stop_pid(pid, graceful_timeout=graceful_timeout, kill_timeout=kill_timeout)
    _remove_file(metadata_path)
    return actions + ["metadata_removed"]


def _metadata_matches(metadata: Mapping[str, Any], expected: Mapping[str, Any]) -> bool:
    return (
        metadata.get("schema") == SCHEMA_VERSION
        and metadata.get("tool_name") == expected["tool_name"]
        and metadata.get("endpoint") == expected["endpoint"]
        and metadata.get("host") == expected["host"]
        and int(metadata.get("port", -1)) == int(expected["port"])
        and str(metadata.get("socket_path")) == str(expected.get("socket_path"))
        and str(metadata.get("command_marker")) == str(expected["command_marker"])
        and str(metadata.get("cwd")) == str(expected["cwd"])
    )


def _metadata_pid(metadata: Mapping[str, Any]) -> int | None:
    try:
        return int(metadata.get("pid"))
    except (TypeError, ValueError):
        return None


def _endpoint_payload(
    *,
    tool_name: str,
    host: str,
    port: int,
    cwd: str | Path | None,
    endpoint: str,
    socket_path: str | Path | None,
    command_marker: str = "",
) -> dict[str, Any]:
    return {
        "tool_name": str(tool_name),
        "endpoint": str(endpoint),
        "host": str(host),
        "port": int(port),
        "socket_path": str(Path(socket_path).expanduser().resolve()) if socket_path else None,
        "command_marker": command_marker,
        "cwd": str(Path(cwd or os.getcwd()).expanduser().resolve()),
    }


def _registry_key(path: Path) -> str:
    return str(path)


def _safe_name(value: str) -> str:
    return "".join(char if char.isalnum() or char in "._-" else "-" for char in value).strip("-") or "tool"


def _read_metadata(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise LifecycleError("metadata_invalid", f"{path}: {exc}") from exc
    if not isinstance(parsed, dict):
        raise LifecycleError("metadata_invalid", str(path))
    return parsed


def _remove_file(path: Path) -> None:
    try:
        path.unlink()
    except FileNotFoundError:
        return
    except OSError as exc:
        raise LifecycleError("metadata_remove_failed", f"{path}: {exc}") from exc


def _endpoint_listener_present(
    endpoint: str,
    host: str,
    port: int,
    socket_path: str | Path | None,
) -> bool:
    if endpoint == "unix":
        return bool(socket_path) and _unix_listener_present(Path(socket_path))
    return int(port) > 0 and _tcp_listener_present(host, int(port))


def _tcp_listener_present(host: str, port: int) -> bool:
    if port <= 0:
        return False
    target = "127.0.0.1" if host in {"", "0.0.0.0", "::"} else host
    try:
        with socket.create_connection((target, port), timeout=0.2):
            return True
    except OSError:
        return False


def _unix_listener_present(path: Path) -> bool:
    if not path.exists() or not hasattr(socket, "AF_UNIX"):
        return False
    try:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
            client.settimeout(0.2)
            client.connect(str(path))
            return True
    except OSError:
        return False


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if _process_is_zombie(pid):
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _process_is_zombie(pid: int) -> bool:
    try:
        fields = (Path("/proc") / str(pid) / "stat").read_text(encoding="utf-8").split()
    except OSError:
        return False
    return len(fields) > 2 and fields[2] == "Z"


def _process_matches(pid: int, command_marker: str, cwd: str) -> bool:
    cmdline = _process_cmdline(pid)
    if command_marker not in cmdline:
        return False
    process_cwd = _process_cwd(pid)
    if process_cwd is None:
        return False
    return str(Path(process_cwd).resolve()) == str(Path(cwd).resolve())


def _process_cmdline(pid: int) -> str:
    proc = Path("/proc") / str(pid) / "cmdline"
    try:
        raw = proc.read_bytes()
    except OSError:
        return ""
    return raw.replace(b"\x00", b" ").decode("utf-8", errors="replace")


def _process_cwd(pid: int) -> str | None:
    try:
        return os.readlink(Path("/proc") / str(pid) / "cwd")
    except OSError:
        return None


def _stop_pid(pid: int, *, graceful_timeout: float, kill_timeout: float) -> list[str]:
    actions: list[str] = []
    try:
        os.kill(pid, signal.SIGTERM)
        actions.append("process_sigterm")
    except ProcessLookupError:
        return ["process_already_gone"]
    if _wait_for_exit(pid, graceful_timeout):
        return actions + ["process_stopped"]
    kill_signal = getattr(signal, "SIGKILL", signal.SIGTERM)
    try:
        os.kill(pid, kill_signal)
        actions.append("process_sigkill" if kill_signal != signal.SIGTERM else "process_second_sigterm")
    except ProcessLookupError:
        return actions + ["process_stopped"]
    if _wait_for_exit(pid, kill_timeout):
        return actions + ["process_stopped"]
    raise LifecycleError("process_stop_timeout", f"pid {pid}")


def _wait_for_exit(pid: int, timeout: float) -> bool:
    deadline = time.monotonic() + max(0.0, timeout)
    while time.monotonic() < deadline:
        if not _pid_alive(pid):
            return True
        time.sleep(0.05)
    return not _pid_alive(pid)


def _iso_now() -> str:
    return (
        _dt.datetime.now(_dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def main() -> int:
    print(
        json.dumps(
            {
                "schema": SCHEMA_VERSION,
                "stateRoot": str(state_root()),
                "pid": os.getpid(),
                "argv": sys.argv,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
