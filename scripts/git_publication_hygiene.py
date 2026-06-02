#!/usr/bin/env python3
"""Read-only Git publication hygiene report for the ESP32 workspace."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def _run(args: list[str], cwd: Path = ROOT) -> dict[str, Any]:
    try:
        result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False, timeout=15)
    except (OSError, subprocess.SubprocessError) as exc:
        return {"ok": False, "args": args, "stdout": "", "stderr": str(exc), "returncode": None}
    return {
        "ok": result.returncode == 0,
        "args": args,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
    }


def _lines(command: dict[str, Any]) -> list[str]:
    return [line.strip() for line in str(command.get("stdout", "")).splitlines() if line.strip()]


def _git_lines(*args: str) -> tuple[list[str], dict[str, Any]]:
    command = _run(["git", *args])
    return _lines(command), command


def _current_branch() -> tuple[str | None, dict[str, Any]]:
    lines, command = _git_lines("branch", "--show-current")
    return (lines[0] if lines else None), command


def _upstream() -> tuple[str | None, dict[str, Any]]:
    lines, command = _git_lines("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    return (lines[0] if command["ok"] and lines else None), command


def _ahead_behind(upstream: str | None) -> tuple[dict[str, int] | None, dict[str, Any] | None]:
    if not upstream:
        return None, None
    lines, command = _git_lines("rev-list", "--left-right", "--count", f"{upstream}...HEAD")
    if not command["ok"] or not lines:
        return None, command
    parts = lines[0].split()
    if len(parts) != 2:
        return None, command
    return {"behind": int(parts[0]), "ahead": int(parts[1])}, command


def _local_branches() -> tuple[list[str], dict[str, Any]]:
    return _git_lines("branch", "--format=%(refname:short)")


def _remote_branches() -> tuple[list[str], dict[str, Any]]:
    return _git_lines("branch", "-r", "--format=%(refname:short)")


def _remote_heads() -> tuple[list[str], dict[str, Any]]:
    command = _run(["git", "ls-remote", "--heads", "origin"])
    heads: list[str] = []
    if command["ok"]:
        for line in _lines(command):
            parts = line.split()
            if len(parts) == 2 and parts[1].startswith("refs/heads/"):
                heads.append(parts[1].removeprefix("refs/heads/"))
    return heads, command


def _unmerged_refs(remote: bool = False) -> tuple[list[str], dict[str, Any]]:
    args = ["branch", "--format=%(refname:short)", "--no-merged"]
    if remote:
        args.insert(1, "-r")
    return _git_lines(*args)


def _open_prs() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    command = _run([
        "gh",
        "pr",
        "list",
        "--state",
        "open",
        "--json",
        "number,title,headRefName,baseRefName,state,url",
    ])
    if not command["ok"]:
        return [], command
    try:
        data = json.loads(command["stdout"] or "[]")
    except json.JSONDecodeError:
        command["ok"] = False
        command["stderr"] = "gh output was not JSON"
        return [], command
    return data if isinstance(data, list) else [], command


def hygiene_report() -> dict[str, Any]:
    status_lines, status_cmd = _git_lines("status", "--short", "--branch", "--untracked-files=all")
    branch, branch_cmd = _current_branch()
    upstream, upstream_cmd = _upstream()
    ahead_behind, ahead_behind_cmd = _ahead_behind(upstream)
    local_branches, local_cmd = _local_branches()
    remote_branches, remote_cmd = _remote_branches()
    remote_heads, remote_heads_cmd = _remote_heads()
    local_unmerged, local_unmerged_cmd = _unmerged_refs(remote=False)
    remote_unmerged, remote_unmerged_cmd = _unmerged_refs(remote=True)
    open_prs, open_prs_cmd = _open_prs()

    local_codex = sorted(branch for branch in local_branches if branch.startswith("codex/"))
    remote_codex = sorted(
        branch for branch in remote_branches
        if branch.startswith("origin/codex/") or branch.startswith("codex/")
    )
    dirty_entries = [line for line in status_lines if not line.startswith("## ")]
    commands = {
        "status": status_cmd,
        "branch": branch_cmd,
        "upstream": upstream_cmd,
        "aheadBehind": ahead_behind_cmd,
        "localBranches": local_cmd,
        "remoteBranches": remote_cmd,
        "remoteHeads": remote_heads_cmd,
        "localUnmerged": local_unmerged_cmd,
        "remoteUnmerged": remote_unmerged_cmd,
        "openPrs": open_prs_cmd,
    }
    return {
        "schema": "git_publication_hygiene.v1",
        "repo": str(ROOT),
        "currentBranch": branch,
        "upstream": upstream,
        "aheadBehind": ahead_behind,
        "status": status_lines,
        "dirty": bool(dirty_entries),
        "dirtyEntries": dirty_entries,
        "openPullRequests": open_prs,
        "localBranches": local_branches,
        "remoteBranches": remote_branches,
        "remoteHeads": remote_heads,
        "localCodexBranches": local_codex,
        "remoteCodexBranches": remote_codex,
        "localUnmergedRefs": local_unmerged,
        "remoteUnmergedRefs": remote_unmerged,
        "policy": {
            "commitPushPrRequiresExplicitAuthority": True,
            "prMustBeMergedOrClosedInSameGate": True,
            "leftoverFeatureBranchesAllowed": False,
            "destructiveGitRequiresExplicitAuthority": True,
        },
        "commandStatus": {
            name: {
                "ok": command["ok"] if command is not None else None,
                "returncode": command["returncode"] if command is not None else None,
                "stderr": command["stderr"] if command is not None else "",
            }
            for name, command in commands.items()
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser("check", help="emit a read-only publication hygiene report")
    check.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args()
    if args.command != "check":
        parser.error("unsupported command")
    report = hygiene_report()
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"branch: {report['currentBranch']} upstream: {report['upstream']} dirty: {report['dirty']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
