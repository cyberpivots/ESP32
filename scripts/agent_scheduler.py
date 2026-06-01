#!/usr/bin/env python3
"""Host-only advisory scheduler for coordinating local Codex windows."""

from __future__ import annotations

import argparse
import contextlib
import dataclasses
import datetime as _dt
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import socket
import socketserver
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
from typing import Any
import uuid

import server_lifecycle


SCHEMA_VERSION = "multi_window_coordination.v1"
MAX_ACTIVE_WINDOWS = 5
WINDOW_STALE_SECONDS = 300
CLAIM_LEASE_SECONDS = 900
CLIENT_TIMEOUT_SECONDS = 2.0
PRETOOL_TIMEOUT_SECONDS = 0.75
STATE_ENV = "ESP32_SCHEDULER_STATE_HOME"
DAEMON_TOOL_NAME = "esp32_agent_scheduler"
DAEMON_COMMAND_MARKER = "agent_scheduler.py daemon run"
_DAEMON_PROCESSES: list[subprocess.Popen[Any]] = []


@dataclasses.dataclass(frozen=True)
class StatePaths:
    repo: Path
    repo_id: str
    state_dir: Path
    db: Path
    socket: Path
    pid: Path
    log: Path


class SchedulerError(RuntimeError):
    """Raised for scheduler request errors that should be returned as JSON."""


def _now() -> float:
    return time.time()


def _iso(ts: float | None = None) -> str:
    value = _now() if ts is None else ts
    return (
        _dt.datetime.fromtimestamp(value, _dt.timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def _read_json(data: str) -> dict[str, Any]:
    try:
        parsed = json.loads(data)
    except json.JSONDecodeError as exc:
        raise SchedulerError(f"invalid JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise SchedulerError("JSON payload must be an object")
    return parsed


def _emit(data: dict[str, Any]) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def _repo_root(repo: str | Path) -> Path:
    candidate = Path(repo).expanduser().resolve()
    try:
        result = subprocess.run(
            ["git", "-C", str(candidate), "rev-parse", "--show-toplevel"],
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError):
        return candidate
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip()).resolve()
    return candidate


def _repo_id(repo: Path) -> str:
    digest = hashlib.sha256(str(repo).encode("utf-8")).hexdigest()[:12]
    base = re.sub(r"[^A-Za-z0-9_.-]+", "-", repo.name).strip("-") or "repo"
    return f"{base}-{digest}"


def _state_home() -> Path:
    if os.environ.get(STATE_ENV):
        return Path(os.environ[STATE_ENV]).expanduser().resolve()
    if os.environ.get("XDG_STATE_HOME"):
        root = Path(os.environ["XDG_STATE_HOME"]).expanduser().resolve()
    else:
        root = Path.home() / ".local" / "state"
    return root / "codex" / "esp32-scheduler"


def state_paths(repo: str | Path) -> StatePaths:
    root = _repo_root(repo)
    rid = _repo_id(root)
    directory = _state_home() / rid
    sock = directory / "scheduler.sock"
    if len(str(sock)) >= 100:
        sock = directory / f"s-{hashlib.sha256(str(sock).encode()).hexdigest()[:10]}.sock"
    return StatePaths(
        repo=root,
        repo_id=rid,
        state_dir=directory,
        db=directory / "scheduler.sqlite3",
        socket=sock,
        pid=directory / "scheduler.pid",
        log=directory / "daemon.log",
    )


def _git_dirty(repo: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "status", "--porcelain=v1", "-z"],
            text=False,
            capture_output=True,
            check=False,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    if result.returncode != 0:
        return []
    paths: list[str] = []
    for entry in result.stdout.decode("utf-8", errors="replace").split("\0"):
        if not entry:
            continue
        path = entry[3:] if len(entry) > 3 else entry
        if path and not re.match(r"^[A-Z? ][A-Z? ]$", path):
            paths.append(path)
    return sorted(set(paths))


def _normalize_path_glob(value: str) -> str:
    cleaned = value.replace("\\", "/").strip()
    while cleaned.startswith("./"):
        cleaned = cleaned[2:]
    return cleaned.rstrip("/") or "."


def _has_glob(value: str) -> bool:
    return any(char in value for char in "*?[")


def _literal_prefix(pattern: str) -> str:
    indexes = [pattern.find(char) for char in "*?[" if pattern.find(char) >= 0]
    if not indexes:
        return pattern
    prefix = pattern[: min(indexes)]
    if "/" in prefix:
        return prefix.rsplit("/", 1)[0] + "/"
    return prefix


def globs_overlap(left: str, right: str) -> bool:
    a = _normalize_path_glob(left)
    b = _normalize_path_glob(right)
    if a in {".", "**", "**/*"} or b in {".", "**", "**/*"}:
        return True
    if a == b:
        return True
    if fnmatch.fnmatchcase(b, a) or fnmatch.fnmatchcase(a, b):
        return True
    if not _has_glob(a) and not _has_glob(b):
        return a.startswith(b.rstrip("/") + "/") or b.startswith(a.rstrip("/") + "/")
    prefix_a = _literal_prefix(a)
    prefix_b = _literal_prefix(b)
    if prefix_a and prefix_b:
        return prefix_a.startswith(prefix_b) or prefix_b.startswith(prefix_a)
    return False


def glob_matches_path(pattern: str, path: str) -> bool:
    normalized = _normalize_path_glob(path)
    candidate = _normalize_path_glob(pattern)
    return globs_overlap(candidate, normalized) or fnmatch.fnmatchcase(normalized, candidate)


def _row_dict(row: sqlite3.Row) -> dict[str, Any]:
    data = dict(row)
    for key in ("path_globs", "payload"):
        if key in data and isinstance(data[key], str):
            with contextlib.suppress(json.JSONDecodeError):
                data[key] = json.loads(data[key])
    for key in (
        "started_at",
        "heartbeat_at",
        "created_at",
        "updated_at",
        "lease_expires_at",
        "finalized_at",
        "event_at",
        "reserved_at",
    ):
        if key in data and data[key] is not None:
            data[f"{key}_iso"] = _iso(float(data[key]))
    return data


class SchedulerCore:
    def __init__(
        self,
        repo: str | Path,
        *,
        baseline_dirty: list[str] | None = None,
        capture_baseline: bool = False,
    ) -> None:
        self.paths = state_paths(repo)
        self.paths.state_dir.mkdir(parents=True, exist_ok=True)
        self._init_db()
        if baseline_dirty is not None:
            self.set_dirty_baseline(baseline_dirty, source="test-fixture")
        elif capture_baseline:
            self.set_dirty_baseline(_git_dirty(self.paths.repo), source="git-status")

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.paths.db), timeout=30, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA busy_timeout = 30000")
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        return conn

    @contextlib.contextmanager
    def _transaction(self) -> Any:
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
            yield conn
            conn.execute("COMMIT")
        except Exception:
            with contextlib.suppress(sqlite3.Error):
                conn.execute("ROLLBACK")
            raise
        finally:
            conn.close()

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS windows (
                    id TEXT PRIMARY KEY,
                    role TEXT NOT NULL,
                    pid INTEGER,
                    session_hint TEXT,
                    started_at REAL NOT NULL,
                    heartbeat_at REAL NOT NULL,
                    status TEXT NOT NULL,
                    queued_reason TEXT
                );
                CREATE TABLE IF NOT EXISTS claims (
                    id TEXT PRIMARY KEY,
                    window_id TEXT NOT NULL,
                    tier TEXT NOT NULL,
                    owner_role TEXT NOT NULL,
                    path_globs TEXT NOT NULL,
                    mode TEXT NOT NULL,
                    validation_plan TEXT NOT NULL,
                    lease_expires_at REAL NOT NULL,
                    status TEXT NOT NULL,
                    dirty_baseline_ack INTEGER NOT NULL DEFAULT 0,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    finalized_at REAL
                );
                CREATE TABLE IF NOT EXISTS events (
                    seq INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    event_at REAL NOT NULL,
                    window_id TEXT,
                    claim_id TEXT,
                    record_kind TEXT,
                    ordinal INTEGER,
                    payload TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS record_reservations (
                    kind TEXT NOT NULL,
                    ordinal INTEGER NOT NULL,
                    slug TEXT NOT NULL,
                    window_id TEXT,
                    status TEXT NOT NULL,
                    reserved_at REAL NOT NULL,
                    finalized_at REAL,
                    path TEXT NOT NULL,
                    PRIMARY KEY (kind, ordinal)
                );
                """
            )
            conn.execute(
                "INSERT OR REPLACE INTO metadata(key, value) VALUES(?, ?)",
                ("schema_version", SCHEMA_VERSION),
            )
            conn.execute(
                "INSERT OR REPLACE INTO metadata(key, value) VALUES(?, ?)",
                ("repo", str(self.paths.repo)),
            )
            conn.execute(
                "INSERT OR REPLACE INTO metadata(key, value) VALUES(?, ?)",
                ("repo_id", self.paths.repo_id),
            )

    def _event(
        self,
        conn: sqlite3.Connection,
        event_type: str,
        payload: dict[str, Any],
        *,
        window_id: str | None = None,
        claim_id: str | None = None,
        record_kind: str | None = None,
        ordinal: int | None = None,
    ) -> None:
        conn.execute(
            """
            INSERT INTO events(event_type, event_at, window_id, claim_id, record_kind, ordinal, payload)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            """,
            (event_type, _now(), window_id, claim_id, record_kind, ordinal, _json(payload)),
        )

    def _metadata(self, conn: sqlite3.Connection, key: str, default: Any = None) -> Any:
        row = conn.execute("SELECT value FROM metadata WHERE key = ?", (key,)).fetchone()
        if not row:
            return default
        with contextlib.suppress(json.JSONDecodeError):
            return json.loads(row["value"])
        return row["value"]

    def set_dirty_baseline(self, paths: list[str], *, source: str) -> None:
        with self._transaction() as conn:
            payload = {
                "paths": sorted(set(_normalize_path_glob(path) for path in paths)),
                "capturedAt": _iso(),
                "source": source,
            }
            conn.execute(
                "INSERT OR REPLACE INTO metadata(key, value) VALUES(?, ?)",
                ("dirty_baseline", _json(payload)),
            )
            self._event(conn, "baseline-capture", payload)

    def _dirty_baseline_paths(self, conn: sqlite3.Connection) -> list[str]:
        baseline = self._metadata(conn, "dirty_baseline", {"paths": []})
        if isinstance(baseline, dict) and isinstance(baseline.get("paths"), list):
            return [str(path) for path in baseline["paths"]]
        return []

    def _reap_stale(self, conn: sqlite3.Connection) -> list[dict[str, Any]]:
        now = _now()
        reaped: list[dict[str, Any]] = []
        for row in conn.execute(
            "SELECT * FROM claims WHERE status = 'active' AND lease_expires_at <= ?",
            (now,),
        ).fetchall():
            conn.execute(
                "UPDATE claims SET status = 'expired', updated_at = ?, finalized_at = ? WHERE id = ?",
                (now, now, row["id"]),
            )
            payload = {"target": "claim", "reason": "lease-expired", "claim": _row_dict(row)}
            self._event(conn, "stale-reap", payload, window_id=row["window_id"], claim_id=row["id"])
            reaped.append(payload)
        stale_before = now - WINDOW_STALE_SECONDS
        for row in conn.execute(
            "SELECT * FROM windows WHERE status = 'active' AND heartbeat_at <= ?",
            (stale_before,),
        ).fetchall():
            conn.execute("UPDATE windows SET status = 'stale' WHERE id = ?", (row["id"],))
            payload = {"target": "window", "reason": "heartbeat-stale", "window": _row_dict(row)}
            self._event(conn, "stale-reap", payload, window_id=row["id"])
            reaped.append(payload)
        if reaped:
            self._promote_queued(conn)
        return reaped

    def _promote_queued(self, conn: sqlite3.Connection) -> None:
        active = conn.execute("SELECT COUNT(*) AS count FROM windows WHERE status = 'active'").fetchone()[
            "count"
        ]
        slots = max(0, MAX_ACTIVE_WINDOWS - int(active))
        if slots <= 0:
            return
        queued = conn.execute(
            "SELECT * FROM windows WHERE status = 'queued' ORDER BY started_at ASC LIMIT ?",
            (slots,),
        ).fetchall()
        now = _now()
        for row in queued:
            conn.execute(
                "UPDATE windows SET status = 'active', heartbeat_at = ?, queued_reason = NULL WHERE id = ?",
                (now, row["id"]),
            )
            self._event(
                conn,
                "window-promote",
                {"windowId": row["id"], "reason": "slot-available"},
                window_id=row["id"],
            )

    def status(self) -> dict[str, Any]:
        with self._transaction() as conn:
            reaped = self._reap_stale(conn)
            windows = [_row_dict(row) for row in conn.execute("SELECT * FROM windows ORDER BY started_at").fetchall()]
            claims = [_row_dict(row) for row in conn.execute("SELECT * FROM claims ORDER BY created_at").fetchall()]
            events = [
                _row_dict(row)
                for row in conn.execute("SELECT * FROM events ORDER BY seq DESC LIMIT 50").fetchall()
            ]
            return {
                "ok": True,
                "schema": SCHEMA_VERSION,
                "repo": str(self.paths.repo),
                "repoId": self.paths.repo_id,
                "stateDir": str(self.paths.state_dir),
                "socket": str(self.paths.socket),
                "activeWindowCount": sum(1 for item in windows if item["status"] == "active"),
                "windows": windows,
                "claims": claims,
                "events": events,
                "reaped": reaped,
                "dirtyBaseline": self._metadata(conn, "dirty_baseline", {"paths": []}),
            }

    def open_window(
        self,
        *,
        role: str,
        pid: int | None = None,
        session_hint: str | None = None,
        on_full: str = "reject",
    ) -> dict[str, Any]:
        if on_full not in {"reject", "queue"}:
            raise SchedulerError("on_full must be reject or queue")
        with self._transaction() as conn:
            self._reap_stale(conn)
            active = conn.execute("SELECT COUNT(*) AS count FROM windows WHERE status = 'active'").fetchone()[
                "count"
            ]
            if int(active) >= MAX_ACTIVE_WINDOWS and on_full == "reject":
                payload = {
                    "decision": "reject",
                    "reason": "max-active-windows",
                    "maxActiveWindows": MAX_ACTIVE_WINDOWS,
                    "activeWindowCount": int(active),
                }
                self._event(conn, "window-reject", payload)
                return {"ok": False, **payload}
            status = "queued" if int(active) >= MAX_ACTIVE_WINDOWS else "active"
            window_id = f"win-{uuid.uuid4().hex[:12]}"
            now = _now()
            queued_reason = "max-active-windows" if status == "queued" else None
            conn.execute(
                """
                INSERT INTO windows(id, role, pid, session_hint, started_at, heartbeat_at, status, queued_reason)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (window_id, role, pid, session_hint, now, now, status, queued_reason),
            )
            event_type = "window-queued" if status == "queued" else "window-open"
            self._event(
                conn,
                event_type,
                {"windowId": window_id, "role": role, "status": status},
                window_id=window_id,
            )
            return {
                "ok": True,
                "window": {
                    "id": window_id,
                    "role": role,
                    "pid": pid,
                    "sessionHint": session_hint,
                    "status": status,
                    "startedAt": _iso(now),
                    "heartbeatAt": _iso(now),
                },
            }

    def heartbeat_window(self, window_id: str) -> dict[str, Any]:
        with self._transaction() as conn:
            self._reap_stale(conn)
            row = conn.execute("SELECT * FROM windows WHERE id = ?", (window_id,)).fetchone()
            if not row:
                return {"ok": False, "decision": "reject", "reason": "unknown-window", "windowId": window_id}
            now = _now()
            conn.execute(
                "UPDATE windows SET heartbeat_at = ?, status = CASE WHEN status = 'stale' THEN 'active' ELSE status END WHERE id = ?",
                (now, window_id),
            )
            self._event(conn, "window-heartbeat", {"windowId": window_id}, window_id=window_id)
            return {"ok": True, "windowId": window_id, "heartbeatAt": _iso(now)}

    def close_window(self, window_id: str) -> dict[str, Any]:
        with self._transaction() as conn:
            row = conn.execute("SELECT * FROM windows WHERE id = ?", (window_id,)).fetchone()
            if not row:
                return {"ok": False, "decision": "reject", "reason": "unknown-window", "windowId": window_id}
            now = _now()
            conn.execute("UPDATE windows SET status = 'closed', heartbeat_at = ? WHERE id = ?", (now, window_id))
            active_claims = conn.execute(
                "SELECT * FROM claims WHERE window_id = ? AND status = 'active'",
                (window_id,),
            ).fetchall()
            for claim in active_claims:
                conn.execute(
                    "UPDATE claims SET status = 'released', updated_at = ?, finalized_at = ? WHERE id = ?",
                    (now, now, claim["id"]),
                )
                self._event(
                    conn,
                    "claim-release",
                    {"claimId": claim["id"], "reason": "window-close"},
                    window_id=window_id,
                    claim_id=claim["id"],
                )
            self._event(conn, "window-close", {"windowId": window_id}, window_id=window_id)
            self._promote_queued(conn)
            return {"ok": True, "windowId": window_id, "status": "closed"}

    def _closed_surface_reasons(
        self,
        *,
        tier: str,
        path_globs: list[str],
        validation_plan: str,
    ) -> list[str]:
        text = " ".join([tier, validation_plan, *path_globs]).lower()
        reasons: list[str] = []
        if "tier 3" in tier.lower() or tier.strip().lower() == "3":
            reasons.append("Tier 3 requires separate same-session live-gate authority")
        closed_tokens = [
            "/etc/codex",
            "credential",
            "secret",
            ".env",
            "external service",
            "release",
            "git push",
            "git reset",
            "serial",
            " rf",
            "radio",
            "flash",
            "relay",
            "load",
            "mains",
        ]
        for token in closed_tokens:
            if token in text:
                reasons.append(f"closed-surface token: {token.strip()}")
        return sorted(set(reasons))

    def acquire_claim(
        self,
        *,
        window_id: str,
        tier: str,
        owner_role: str,
        path_globs: list[str],
        mode: str,
        validation_plan: str,
        lease_seconds: int = CLAIM_LEASE_SECONDS,
        ack_dirty_baseline: bool = False,
        closed_surface_authority: bool = False,
    ) -> dict[str, Any]:
        mode = mode.lower().strip()
        if mode not in {"read", "review", "write"}:
            raise SchedulerError("mode must be read, review, or write")
        normalized_globs = [_normalize_path_glob(item) for item in (path_globs or ["**"])]
        with self._transaction() as conn:
            self._reap_stale(conn)
            window = conn.execute("SELECT * FROM windows WHERE id = ?", (window_id,)).fetchone()
            if not window or window["status"] != "active":
                payload = {"decision": "reject", "reason": "window-not-active", "windowId": window_id}
                self._event(conn, "claim-reject", payload, window_id=window_id)
                return {"ok": False, **payload}
            closed_reasons = self._closed_surface_reasons(
                tier=tier,
                path_globs=normalized_globs,
                validation_plan=validation_plan,
            )
            if closed_reasons and not closed_surface_authority:
                payload = {
                    "decision": "reject",
                    "reason": "closed-surface-authority-required",
                    "closedSurfaceReasons": closed_reasons,
                }
                self._event(conn, "claim-reject", payload, window_id=window_id)
                return {"ok": False, **payload}

            conflicts: list[dict[str, Any]] = []
            stale_warnings: list[dict[str, Any]] = []
            active_writes = conn.execute(
                "SELECT * FROM claims WHERE status = 'active' AND mode = 'write'"
            ).fetchall()
            for row in active_writes:
                existing_globs = json.loads(row["path_globs"])
                overlapping = [
                    [new, old]
                    for new in normalized_globs
                    for old in existing_globs
                    if globs_overlap(new, old)
                ]
                entry = {
                    "claimId": row["id"],
                    "windowId": row["window_id"],
                    "pathOverlap": overlapping,
                }
                if mode == "write":
                    if overlapping:
                        conflicts.append(entry)
                else:
                    stale_warnings.append(entry)
            if conflicts:
                payload = {
                    "decision": "reject",
                    "reason": "overlapping-write-claim",
                    "conflicts": conflicts,
                }
                self._event(conn, "conflict", payload, window_id=window_id)
                return {"ok": False, **payload}

            baseline_paths = self._dirty_baseline_paths(conn)
            dirty_hits = [
                path
                for path in baseline_paths
                if any(glob_matches_path(pattern, path) for pattern in normalized_globs)
            ]
            warnings: list[str] = []
            if stale_warnings:
                warnings.append("stale-evidence-warning: active write claim overlaps this read/review claim")
            if dirty_hits:
                warnings.append("dirty-baseline-overlap: claim touches paths dirty when daemon started")

            now = _now()
            claim_id = f"claim-{uuid.uuid4().hex[:12]}"
            lease_expires = now + max(0, int(lease_seconds))
            conn.execute(
                """
                INSERT INTO claims(
                    id, window_id, tier, owner_role, path_globs, mode, validation_plan,
                    lease_expires_at, status, dirty_baseline_ack, created_at, updated_at
                )
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, 'active', ?, ?, ?)
                """,
                (
                    claim_id,
                    window_id,
                    tier,
                    owner_role,
                    _json(normalized_globs),
                    mode,
                    validation_plan,
                    lease_expires,
                    1 if ack_dirty_baseline else 0,
                    now,
                    now,
                ),
            )
            event_payload = {
                "claimId": claim_id,
                "windowId": window_id,
                "mode": mode,
                "tier": tier,
                "ownerRole": owner_role,
                "pathGlobs": normalized_globs,
                "dirtyBaselineOverlap": dirty_hits,
                "dirtyBaselineAcknowledged": bool(ack_dirty_baseline),
                "warnings": warnings,
                "staleEvidence": stale_warnings,
            }
            self._event(conn, "claim-acquire", event_payload, window_id=window_id, claim_id=claim_id)
            return {
                "ok": True,
                "claim": {
                    "id": claim_id,
                    "windowId": window_id,
                    "tier": tier,
                    "ownerRole": owner_role,
                    "pathGlobs": normalized_globs,
                    "mode": mode,
                    "validationPlan": validation_plan,
                    "leaseExpiresAt": _iso(lease_expires),
                    "status": "active",
                },
                "warnings": warnings,
                "staleEvidence": stale_warnings,
                "dirtyBaselineOverlap": dirty_hits,
                "dirtyBaselineAcknowledged": bool(ack_dirty_baseline),
            }

    def renew_claim(self, claim_id: str, *, lease_seconds: int = CLAIM_LEASE_SECONDS) -> dict[str, Any]:
        with self._transaction() as conn:
            self._reap_stale(conn)
            row = conn.execute("SELECT * FROM claims WHERE id = ?", (claim_id,)).fetchone()
            if not row or row["status"] != "active":
                return {"ok": False, "decision": "reject", "reason": "claim-not-active", "claimId": claim_id}
            expires = _now() + max(0, int(lease_seconds))
            conn.execute(
                "UPDATE claims SET lease_expires_at = ?, updated_at = ? WHERE id = ?",
                (expires, _now(), claim_id),
            )
            self._event(conn, "claim-renew", {"claimId": claim_id, "leaseExpiresAt": _iso(expires)}, claim_id=claim_id)
            return {"ok": True, "claimId": claim_id, "leaseExpiresAt": _iso(expires)}

    def finish_claim(self, claim_id: str, *, status: str, outcome: str = "") -> dict[str, Any]:
        if status not in {"released", "finalized"}:
            raise SchedulerError("claim status must be released or finalized")
        event_type = "claim-release" if status == "released" else "claim-finalize"
        with self._transaction() as conn:
            row = conn.execute("SELECT * FROM claims WHERE id = ?", (claim_id,)).fetchone()
            if not row:
                return {"ok": False, "decision": "reject", "reason": "unknown-claim", "claimId": claim_id}
            now = _now()
            conn.execute(
                "UPDATE claims SET status = ?, updated_at = ?, finalized_at = ? WHERE id = ?",
                (status, now, now, claim_id),
            )
            self._event(conn, event_type, {"claimId": claim_id, "outcome": outcome}, claim_id=claim_id)
            return {"ok": True, "claimId": claim_id, "status": status, "outcome": outcome}

    def reserve_record(self, *, kind: str, slug: str, window_id: str | None = None) -> dict[str, Any]:
        if kind not in {"task-log", "handoff"}:
            raise SchedulerError("record kind must be task-log or handoff")
        clean_slug = re.sub(r"[^a-z0-9-]+", "-", slug.strip().lower()).strip("-") or "record"
        directory = self.paths.repo / (".agents/TASK_LOG" if kind == "task-log" else ".agents/handoffs")
        directory.mkdir(parents=True, exist_ok=True)
        pattern = re.compile(r"^(\d{4})-")
        with self._transaction() as conn:
            existing = []
            for path in directory.iterdir():
                if not path.is_file():
                    continue
                match = pattern.match(path.name)
                if match:
                    existing.append(int(match.group(1)))
            reserved = [
                int(row["ordinal"])
                for row in conn.execute("SELECT ordinal FROM record_reservations WHERE kind = ?", (kind,)).fetchall()
            ]
            ordinal = max(existing + reserved + [0]) + 1
            rel_path = f".agents/{'TASK_LOG' if kind == 'task-log' else 'handoffs'}/{ordinal:04d}-{clean_slug}.md"
            now = _now()
            conn.execute(
                """
                INSERT INTO record_reservations(kind, ordinal, slug, window_id, status, reserved_at, path)
                VALUES(?, ?, ?, ?, 'reserved', ?, ?)
                """,
                (kind, ordinal, clean_slug, window_id, now, rel_path),
            )
            payload = {"kind": kind, "ordinal": ordinal, "slug": clean_slug, "path": rel_path}
            self._event(conn, "record-reserve", payload, window_id=window_id, record_kind=kind, ordinal=ordinal)
            return {"ok": True, **payload}

    def finalize_record(self, *, kind: str, ordinal: int, path: str | None = None) -> dict[str, Any]:
        with self._transaction() as conn:
            row = conn.execute(
                "SELECT * FROM record_reservations WHERE kind = ? AND ordinal = ?",
                (kind, ordinal),
            ).fetchone()
            if not row:
                return {"ok": False, "decision": "reject", "reason": "unknown-record-reservation"}
            now = _now()
            final_path = path or row["path"]
            conn.execute(
                """
                UPDATE record_reservations
                SET status = 'finalized', finalized_at = ?, path = ?
                WHERE kind = ? AND ordinal = ?
                """,
                (now, final_path, kind, ordinal),
            )
            payload = {"kind": kind, "ordinal": ordinal, "path": final_path}
            self._event(conn, "record-finalize", payload, record_kind=kind, ordinal=ordinal)
            return {"ok": True, **payload}

    def pretool_check(self, payload: dict[str, Any]) -> dict[str, Any]:
        command = _extract_command(payload.get("tool_input"))
        tool_name = str(payload.get("tool_name") or "")
        permission_mode = str(payload.get("permission_mode") or "")
        warnings: list[str] = []
        with self._transaction() as conn:
            self._reap_stale(conn)
            active_writes = [
                _row_dict(row)
                for row in conn.execute(
                    "SELECT * FROM claims WHERE status = 'active' AND mode = 'write' ORDER BY created_at"
                ).fetchall()
            ]
        if permission_mode == "bypassPermissions":
            warnings.append("permission_mode=bypassPermissions: scheduler context is advisory only; no deny/block")
        if active_writes:
            claims = ", ".join(f"{item['id']}:{item['path_globs']}" for item in active_writes)
            warnings.append(f"active-write-claims: {claims}")
        lower = f"{tool_name} {command}".lower()
        closed = [
            token
            for token in ["idf.py flash", "idf.py monitor", "serial", "rf", "relay", "mains", "git reset --hard"]
            if token in lower
        ]
        if closed:
            warnings.append(
                "closed-surface-advisory: separate explicit authority is required for "
                + ", ".join(sorted(set(closed)))
            )
        return {
            "ok": True,
            "advisory": True,
            "schema": SCHEMA_VERSION,
            "warnings": warnings,
            "activeWriteClaimCount": len(active_writes),
        }


def _extract_command(tool_input: Any) -> str:
    if isinstance(tool_input, dict):
        for key in ("command", "cmd"):
            value = tool_input.get(key)
            if isinstance(value, str):
                return value
    if isinstance(tool_input, str):
        return tool_input
    return ""


def _request_lease_seconds(request: dict[str, Any]) -> int:
    if "lease_seconds" not in request:
        return CLAIM_LEASE_SECONDS
    value = request.get("lease_seconds")
    if value is None:
        return CLAIM_LEASE_SECONDS
    if isinstance(value, str) and not value.strip():
        return CLAIM_LEASE_SECONDS
    return int(value)


class SchedulerServer(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    daemon_threads = True

    def __init__(self, server_address: str, core: SchedulerCore) -> None:
        self.core = core
        super().__init__(server_address, SchedulerHandler)

    def dispatch(self, request: dict[str, Any]) -> dict[str, Any]:
        op = request.get("op")
        if op == "status":
            return self.core.status()
        if op == "daemon_stop":
            threading.Thread(target=self.shutdown, daemon=True).start()
            return {"ok": True, "status": "stopping"}
        if op == "window_open":
            return self.core.open_window(
                role=str(request.get("role") or "unspecified"),
                pid=request.get("pid") if isinstance(request.get("pid"), int) else None,
                session_hint=request.get("session_hint") if isinstance(request.get("session_hint"), str) else None,
                on_full=str(request.get("on_full") or "reject"),
            )
        if op == "window_heartbeat":
            return self.core.heartbeat_window(str(request.get("window_id") or ""))
        if op == "window_close":
            return self.core.close_window(str(request.get("window_id") or ""))
        if op == "claim_acquire":
            return self.core.acquire_claim(
                window_id=str(request.get("window_id") or ""),
                tier=str(request.get("tier") or "Tier 1"),
                owner_role=str(request.get("owner_role") or "unspecified"),
                path_globs=[str(item) for item in request.get("path_globs") or ["**"]],
                mode=str(request.get("mode") or "write"),
                validation_plan=str(request.get("validation_plan") or ""),
                lease_seconds=_request_lease_seconds(request),
                ack_dirty_baseline=bool(request.get("ack_dirty_baseline")),
                closed_surface_authority=bool(request.get("closed_surface_authority")),
            )
        if op == "claim_renew":
            return self.core.renew_claim(
                str(request.get("claim_id") or ""),
                lease_seconds=_request_lease_seconds(request),
            )
        if op == "claim_release":
            return self.core.finish_claim(str(request.get("claim_id") or ""), status="released", outcome=str(request.get("outcome") or ""))
        if op == "claim_finalize":
            return self.core.finish_claim(str(request.get("claim_id") or ""), status="finalized", outcome=str(request.get("outcome") or ""))
        if op == "record_reserve":
            return self.core.reserve_record(
                kind=str(request.get("kind") or ""),
                slug=str(request.get("slug") or "record"),
                window_id=request.get("window_id") if isinstance(request.get("window_id"), str) else None,
            )
        if op == "record_finalize":
            return self.core.finalize_record(
                kind=str(request.get("kind") or ""),
                ordinal=int(request.get("ordinal") or 0),
                path=request.get("path") if isinstance(request.get("path"), str) else None,
            )
        if op == "pretool_check":
            payload = request.get("payload") if isinstance(request.get("payload"), dict) else {}
            return self.core.pretool_check(payload)
        return {"ok": False, "decision": "reject", "reason": f"unknown-op:{op}"}


class SchedulerHandler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        raw = self.rfile.readline(1024 * 1024)
        try:
            request = _read_json(raw.decode("utf-8"))
            response = self.server.dispatch(request)  # type: ignore[attr-defined]
        except Exception as exc:  # noqa: BLE001 - daemon must return JSON for all request failures.
            response = {"ok": False, "decision": "reject", "reason": str(exc)}
        self.wfile.write((json.dumps(response, sort_keys=True) + "\n").encode("utf-8"))


def _client_request(paths: StatePaths, payload: dict[str, Any], *, timeout: float) -> dict[str, Any]:
    if not hasattr(socket, "AF_UNIX"):
        raise SchedulerError("Unix sockets are unavailable on this platform")
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
        client.settimeout(timeout)
        client.connect(str(paths.socket))
        client.sendall((json.dumps(payload, sort_keys=True) + "\n").encode("utf-8"))
        chunks: list[bytes] = []
        while True:
            chunk = client.recv(65536)
            if not chunk:
                break
            chunks.append(chunk)
            if b"\n" in chunk:
                break
    raw = b"".join(chunks).decode("utf-8").strip()
    if not raw:
        raise SchedulerError("daemon returned no response")
    return _read_json(raw)


def daemon_status(repo: str | Path) -> dict[str, Any]:
    paths = state_paths(repo)
    if not paths.socket.exists():
        return {
            "ok": True,
            "running": False,
            "schema": SCHEMA_VERSION,
            "repo": str(paths.repo),
            "repoId": paths.repo_id,
            "stateDir": str(paths.state_dir),
            "socket": str(paths.socket),
        }
    try:
        response = _client_request(paths, {"op": "status"}, timeout=CLIENT_TIMEOUT_SECONDS)
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "running": False,
            "repo": str(paths.repo),
            "repoId": paths.repo_id,
            "stateDir": str(paths.state_dir),
            "socket": str(paths.socket),
            "error": str(exc),
        }
    response["running"] = True
    return response


def daemon_run(repo: str | Path) -> int:
    core = SchedulerCore(repo, capture_baseline=True)
    paths = core.paths
    paths.state_dir.mkdir(parents=True, exist_ok=True)
    _prepare_daemon_endpoint(paths, replace_existing=False)
    server = SchedulerServer(str(paths.socket), core)
    with contextlib.suppress(OSError):
        paths.socket.chmod(0o600)
    paths.pid.write_text(str(os.getpid()), encoding="utf-8")
    server_lifecycle.write_metadata(
        tool_name=DAEMON_TOOL_NAME,
        host="unix",
        port=0,
        endpoint="unix",
        socket_path=paths.socket,
        command_marker=DAEMON_COMMAND_MARKER,
        cwd=paths.repo,
        state_dir=_daemon_lifecycle_state_dir(paths),
    )

    def _stop(signum: int, _frame: Any) -> None:
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    try:
        server.serve_forever(poll_interval=0.2)
    finally:
        server.server_close()
        with contextlib.suppress(OSError):
            paths.socket.unlink()
        with contextlib.suppress(OSError):
            paths.pid.unlink()
        server_lifecycle.clear_metadata(
            tool_name=DAEMON_TOOL_NAME,
            host="unix",
            port=0,
            endpoint="unix",
            socket_path=paths.socket,
            cwd=paths.repo,
            state_dir=_daemon_lifecycle_state_dir(paths),
        )
    return 0


def _reap_known_daemons() -> None:
    for process in list(_DAEMON_PROCESSES):
        if process.poll() is not None:
            with contextlib.suppress(OSError):
                process.wait(timeout=0)
            _DAEMON_PROCESSES.remove(process)


def _daemon_lifecycle_state_dir(paths: StatePaths) -> Path:
    return paths.state_dir / "server-lifecycle"


def _prepare_daemon_endpoint(paths: StatePaths, *, replace_existing: bool) -> dict[str, Any]:
    try:
        result = server_lifecycle.prepare_for_reopen(
            tool_name=DAEMON_TOOL_NAME,
            host="unix",
            port=0,
            endpoint="unix",
            socket_path=paths.socket,
            command_marker=DAEMON_COMMAND_MARKER,
            cwd=paths.repo,
            state_dir=_daemon_lifecycle_state_dir(paths),
            replace_existing=replace_existing,
        )
    except server_lifecycle.LifecycleError as exc:
        payload = exc.to_dict()
        payload["status"] = "listener-cleanup-failed"
        raise SchedulerError(_json(payload)) from exc
    return result.to_dict()


def daemon_start(repo: str | Path, *, replace_existing: bool = False) -> dict[str, Any]:
    paths = state_paths(repo)
    current = daemon_status(repo)
    if current.get("running") and not replace_existing:
        return {"ok": True, "running": True, "status": "already-running", "stateDir": str(paths.state_dir)}
    try:
        cleanup = _prepare_daemon_endpoint(paths, replace_existing=replace_existing)
    except SchedulerError as exc:
        return {
            "ok": False,
            "running": bool(current.get("running")),
            "status": "listener-cleanup-failed",
            "error": str(exc),
            "stateDir": str(paths.state_dir),
        }
    paths.state_dir.mkdir(parents=True, exist_ok=True)
    log_handle = paths.log.open("ab")
    try:
        process = subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve()), "daemon", "run", "--repo", str(paths.repo)],
            stdout=log_handle,
            stderr=log_handle,
            stdin=subprocess.DEVNULL,
            cwd=str(paths.repo),
            start_new_session=True,
        )
        _DAEMON_PROCESSES.append(process)
    finally:
        log_handle.close()
    deadline = _now() + 5
    last: dict[str, Any] = {}
    while _now() < deadline:
        time.sleep(0.05)
        last = daemon_status(repo)
        if last.get("running"):
            return {
                "ok": True,
                "running": True,
                "status": "started",
                "stateDir": str(paths.state_dir),
                "lifecycle": cleanup,
            }
    return {"ok": False, "running": False, "status": "start-timeout", "lastStatus": last}


def daemon_restart(repo: str | Path) -> dict[str, Any]:
    paths = state_paths(repo)
    try:
        cleanup = _prepare_daemon_endpoint(paths, replace_existing=True)
    except SchedulerError as exc:
        return {
            "ok": False,
            "running": bool(daemon_status(repo).get("running")),
            "status": "listener-cleanup-failed",
            "error": str(exc),
            "stateDir": str(paths.state_dir),
        }
    _reap_known_daemons()
    started = daemon_start(repo, replace_existing=False)
    started["restartLifecycle"] = cleanup
    if started.get("ok"):
        started["status"] = "restarted"
    return started


def daemon_stop(repo: str | Path) -> dict[str, Any]:
    paths = state_paths(repo)
    if not paths.socket.exists():
        return {"ok": True, "running": False, "status": "already-stopped"}
    try:
        response = _client_request(paths, {"op": "daemon_stop"}, timeout=CLIENT_TIMEOUT_SECONDS)
    except Exception as exc:  # noqa: BLE001
        response = {"ok": False, "status": "stop-request-failed", "error": str(exc)}
    deadline = _now() + 5
    while _now() < deadline and paths.socket.exists():
        time.sleep(0.05)
    response["running"] = paths.socket.exists()
    _reap_known_daemons()
    return response


def request_or_error(repo: str | Path, payload: dict[str, Any]) -> dict[str, Any]:
    return _client_request(state_paths(repo), payload, timeout=CLIENT_TIMEOUT_SECONDS)


def preflight(repo: str | Path) -> dict[str, Any]:
    paths = state_paths(repo)
    warnings: list[str] = []
    try:
        paths.state_dir.relative_to(paths.repo)
        warnings.append("state-dir-inside-repo: use a user state directory outside the Windows-mounted repo")
    except ValueError:
        pass
    return {
        "ok": not any(item.startswith("state-dir-inside-repo") for item in warnings),
        "schema": SCHEMA_VERSION,
        "repo": str(paths.repo),
        "repoId": paths.repo_id,
        "stateDir": str(paths.state_dir),
        "socket": str(paths.socket),
        "dirtyBaselineNow": _git_dirty(paths.repo),
        "warnings": warnings,
        "authorityLimits": [
            "advisory-only",
            "no /etc/codex mutation",
            "no hard yolo block",
            "no live hardware",
            "no credentials",
            "no external services",
            "no commit/push/release",
        ],
    }


def doctor(repo: str | Path) -> dict[str, Any]:
    paths = state_paths(repo)
    status = daemon_status(repo)
    checks = {
        "stateDirOutsideRepo": True,
        "stateDirExistsOrCreatable": True,
        "sqliteOpen": True,
        "daemonResponding": bool(status.get("running")),
    }
    warnings: list[str] = []
    try:
        paths.state_dir.relative_to(paths.repo)
        checks["stateDirOutsideRepo"] = False
        warnings.append("state directory is inside the repo")
    except ValueError:
        pass
    try:
        paths.state_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        checks["stateDirExistsOrCreatable"] = False
        warnings.append(f"state directory is not creatable: {exc}")
    try:
        core = SchedulerCore(repo)
        with core._connect() as conn:
            schema = core._metadata(conn, "schema_version")
    except Exception as exc:  # noqa: BLE001
        checks["sqliteOpen"] = False
        schema = None
        warnings.append(f"sqlite open failed: {exc}")
    if not checks["daemonResponding"]:
        warnings.append("daemon is not running; advisory scheduler checks will report scheduler-unavailable")
    return {
        "ok": checks["stateDirOutsideRepo"] and checks["stateDirExistsOrCreatable"] and checks["sqliteOpen"],
        "schema": schema or SCHEMA_VERSION,
        "repo": str(paths.repo),
        "repoId": paths.repo_id,
        "stateDir": str(paths.state_dir),
        "socket": str(paths.socket),
        "checks": checks,
        "daemonStatus": status,
        "warnings": warnings,
    }


def hook_context(text: str) -> dict[str, Any]:
    return {"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": text}}


def pretool_check(repo: str | Path, payload: dict[str, Any], *, timeout: float = PRETOOL_TIMEOUT_SECONDS) -> dict[str, Any]:
    paths = state_paths(repo)
    permission_mode = str(payload.get("permission_mode") or "")
    prefix = "ESP32 multi-window scheduler advisory"
    try:
        response = _client_request(paths, {"op": "pretool_check", "payload": payload}, timeout=timeout)
    except Exception as exc:  # noqa: BLE001
        mode_note = (
            " permission_mode=bypassPermissions is advisory only; no deny/block."
            if permission_mode == "bypassPermissions"
            else " no deny/block."
        )
        return hook_context(f"{prefix}: scheduler-unavailable ({exc});{mode_note}")
    warnings = response.get("warnings") if isinstance(response.get("warnings"), list) else []
    if not warnings:
        warnings = ["no active scheduler conflict reported"]
    return hook_context(f"{prefix}: " + "; ".join(str(item) for item in warnings))


def self_test() -> dict[str, Any]:
    results: list[str] = []
    with tempfile.TemporaryDirectory(prefix="esp32-scheduler-selftest-") as tmp:
        old_state = os.environ.get(STATE_ENV)
        os.environ[STATE_ENV] = str(Path(tmp) / "state")
        try:
            repo = Path(tmp) / "repo"
            (repo / ".agents" / "TASK_LOG").mkdir(parents=True)
            (repo / ".agents" / "handoffs").mkdir(parents=True)
            core = SchedulerCore(repo, baseline_dirty=["dirty.txt"])
            windows = [core.open_window(role=f"role-{index}")["window"]["id"] for index in range(MAX_ACTIVE_WINDOWS)]
            assert not core.open_window(role="sixth")["ok"]
            results.append("window-limit")
            for index, window_id in enumerate(windows):
                response = core.acquire_claim(
                    window_id=window_id,
                    tier="Tier 2",
                    owner_role="Tooling",
                    path_globs=[f"scripts/selftest-{index}.py"],
                    mode="write",
                    validation_plan="self-test",
                )
                assert response["ok"], response
            assert not core.acquire_claim(
                window_id=windows[0],
                tier="Tier 2",
                owner_role="Tooling",
                path_globs=["scripts/selftest-1.py"],
                mode="write",
                validation_plan="self-test",
            )["ok"]
            results.append("write-conflict")
            dirty = core.acquire_claim(
                window_id=windows[0],
                tier="Tier 2",
                owner_role="Tooling",
                path_globs=["dirty.txt"],
                mode="read",
                validation_plan="self-test",
            )
            assert dirty["dirtyBaselineOverlap"] == ["dirty.txt"]
            results.append("dirty-baseline")
            expiring = core.acquire_claim(
                window_id=windows[0],
                tier="Tier 2",
                owner_role="Tooling",
                path_globs=["docs/selftest.md"],
                mode="read",
                validation_plan="self-test",
                lease_seconds=0,
            )
            assert expiring["ok"]
            status = core.status()
            assert any(item["target"] == "claim" for item in status["reaped"])
            results.append("stale-reap")
            reservations = [core.reserve_record(kind="task-log", slug="self-test") for _ in range(3)]
            assert [item["ordinal"] for item in reservations] == [1, 2, 3]
            results.append("record-reserve")
        finally:
            if old_state is None:
                os.environ.pop(STATE_ENV, None)
            else:
                os.environ[STATE_ENV] = old_state
    return {"ok": True, "schema": SCHEMA_VERSION, "results": results}


def _read_hook_payload(args: argparse.Namespace) -> dict[str, Any]:
    if getattr(args, "hook_json", None) and args.hook_json != "-":
        return _read_json(args.hook_json)
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    return _read_json(raw)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    daemon = sub.add_parser("daemon")
    daemon_sub = daemon.add_subparsers(dest="daemon_command", required=True)
    for name in ["ensure", "stop", "status", "run", "restart"]:
        item = daemon_sub.add_parser(name)
        item.add_argument("--repo", default=os.getcwd())
    item = daemon_sub.add_parser("start")
    item.add_argument("--repo", default=os.getcwd())
    item.add_argument("--replace-existing", action="store_true")

    window = sub.add_parser("window")
    window_sub = window.add_subparsers(dest="window_command", required=True)
    item = window_sub.add_parser("open")
    item.add_argument("--repo", default=os.getcwd())
    item.add_argument("--role", default="unspecified")
    item.add_argument("--pid", type=int)
    item.add_argument("--session-hint")
    item.add_argument("--on-full", choices=["reject", "queue"], default="reject")
    for name in ["heartbeat", "close"]:
        item = window_sub.add_parser(name)
        item.add_argument("--repo", default=os.getcwd())
        item.add_argument("--window-id", required=True)

    claim = sub.add_parser("claim")
    claim_sub = claim.add_subparsers(dest="claim_command", required=True)
    item = claim_sub.add_parser("acquire")
    item.add_argument("--repo", default=os.getcwd())
    item.add_argument("--window-id", required=True)
    item.add_argument("--tier", default="Tier 2")
    item.add_argument("--owner-role", default="unspecified")
    item.add_argument("--path-glob", action="append", dest="path_globs", default=[])
    item.add_argument("--mode", choices=["read", "review", "write"], default="write")
    item.add_argument("--validation-plan", default="")
    item.add_argument("--lease-seconds", type=int, default=CLAIM_LEASE_SECONDS)
    item.add_argument("--ack-dirty-baseline", action="store_true")
    item.add_argument("--closed-surface-authority", action="store_true")
    item = claim_sub.add_parser("renew")
    item.add_argument("--repo", default=os.getcwd())
    item.add_argument("--claim-id", required=True)
    item.add_argument("--lease-seconds", type=int, default=CLAIM_LEASE_SECONDS)
    for name in ["release", "finalize"]:
        item = claim_sub.add_parser(name)
        item.add_argument("--repo", default=os.getcwd())
        item.add_argument("--claim-id", required=True)
        item.add_argument("--outcome", default="")

    record = sub.add_parser("record")
    record_sub = record.add_subparsers(dest="record_command", required=True)
    item = record_sub.add_parser("reserve")
    item.add_argument("--repo", default=os.getcwd())
    item.add_argument("--kind", choices=["task-log", "handoff"], required=True)
    item.add_argument("--slug", required=True)
    item.add_argument("--window-id")
    item = record_sub.add_parser("finalize")
    item.add_argument("--repo", default=os.getcwd())
    item.add_argument("--kind", choices=["task-log", "handoff"], required=True)
    item.add_argument("--ordinal", type=int, required=True)
    item.add_argument("--path")

    item = sub.add_parser("preflight")
    item.add_argument("--repo", default=os.getcwd())
    item = sub.add_parser("pretool-check")
    item.add_argument("--repo", default=os.getcwd())
    item.add_argument("--hook-json", default="-")
    item.add_argument("--timeout", type=float, default=PRETOOL_TIMEOUT_SECONDS)
    item = sub.add_parser("doctor")
    item.add_argument("--repo", default=os.getcwd())
    sub.add_parser("self-test")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "daemon":
            if args.daemon_command == "run":
                return daemon_run(args.repo)
            if args.daemon_command == "start":
                result = daemon_start(args.repo, replace_existing=args.replace_existing)
            elif args.daemon_command == "ensure":
                result = daemon_start(args.repo, replace_existing=False)
            elif args.daemon_command == "restart":
                result = daemon_restart(args.repo)
            elif args.daemon_command == "stop":
                result = daemon_stop(args.repo)
            else:
                result = daemon_status(args.repo)
        elif args.command == "window":
            if args.window_command == "open":
                result = request_or_error(
                    args.repo,
                    {
                        "op": "window_open",
                        "role": args.role,
                        "pid": args.pid,
                        "session_hint": args.session_hint,
                        "on_full": args.on_full,
                    },
                )
            elif args.window_command == "heartbeat":
                result = request_or_error(args.repo, {"op": "window_heartbeat", "window_id": args.window_id})
            else:
                result = request_or_error(args.repo, {"op": "window_close", "window_id": args.window_id})
        elif args.command == "claim":
            if args.claim_command == "acquire":
                result = request_or_error(
                    args.repo,
                    {
                        "op": "claim_acquire",
                        "window_id": args.window_id,
                        "tier": args.tier,
                        "owner_role": args.owner_role,
                        "path_globs": args.path_globs or ["**"],
                        "mode": args.mode,
                        "validation_plan": args.validation_plan,
                        "lease_seconds": args.lease_seconds,
                        "ack_dirty_baseline": args.ack_dirty_baseline,
                        "closed_surface_authority": args.closed_surface_authority,
                    },
                )
            elif args.claim_command == "renew":
                result = request_or_error(
                    args.repo,
                    {"op": "claim_renew", "claim_id": args.claim_id, "lease_seconds": args.lease_seconds},
                )
            elif args.claim_command == "release":
                result = request_or_error(
                    args.repo,
                    {"op": "claim_release", "claim_id": args.claim_id, "outcome": args.outcome},
                )
            else:
                result = request_or_error(
                    args.repo,
                    {"op": "claim_finalize", "claim_id": args.claim_id, "outcome": args.outcome},
                )
        elif args.command == "record":
            if args.record_command == "reserve":
                result = request_or_error(
                    args.repo,
                    {"op": "record_reserve", "kind": args.kind, "slug": args.slug, "window_id": args.window_id},
                )
            else:
                result = request_or_error(
                    args.repo,
                    {"op": "record_finalize", "kind": args.kind, "ordinal": args.ordinal, "path": args.path},
                )
        elif args.command == "preflight":
            result = preflight(args.repo)
        elif args.command == "pretool-check":
            result = pretool_check(args.repo, _read_hook_payload(args), timeout=args.timeout)
            _emit(result)
            return 0
        elif args.command == "doctor":
            result = doctor(args.repo)
        elif args.command == "self-test":
            result = self_test()
        else:
            raise SchedulerError(f"unknown command: {args.command}")
    except Exception as exc:  # noqa: BLE001 - CLI should produce machine-readable failures.
        result = {"ok": False, "decision": "reject", "reason": str(exc)}
    _emit(result)
    return 0 if result.get("ok", False) else 1


if __name__ == "__main__":
    raise SystemExit(main())
