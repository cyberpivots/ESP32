#!/usr/bin/env python3
"""Path, framework, and source-image audits for the ESP32 scaffold."""

from __future__ import annotations

import subprocess
from pathlib import Path

from scaffold_audit_data import (
    ALLOWED_IMAGE_BINARY_PATHS,
    ALLOWED_PROJECT_FRAMEWORK_FILES,
    IMAGE_SUFFIXES,
    PROHIBITED_FRAMEWORK_FILES,
    REQUIRED_PATHS,
    ROOT,
)


def git_source_files(root: Path = ROOT) -> list[str]:
    """Return tracked plus unignored files, matching what source audits own."""
    command = ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"]
    try:
        result = subprocess.run(
            command,
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError):
        return [
            path.relative_to(root).as_posix()
            for path in root.rglob("*")
            if path.is_file() and ".git" not in path.parts and "build" not in path.parts
        ]
    return [
        item.decode("utf-8")
        for item in result.stdout.split(b"\0")
        if item
    ]


def audit_required_paths(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    for rel in REQUIRED_PATHS:
        if not (root / rel).exists():
            failures.append(f"missing required path: {rel}")
    return failures


def audit_framework_files(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    for rel in git_source_files(root):
        candidate = root / rel
        if (
            candidate.name in PROHIBITED_FRAMEWORK_FILES
            or candidate.name.startswith("sdkconfig")
        ) and rel not in ALLOWED_PROJECT_FRAMEWORK_FILES:
            failures.append(
                "framework file present before implementation gate: "
                f"{rel}"
            )
    return failures


def audit_source_image_paths(
    root: Path = ROOT,
    relative_files: list[str] | None = None,
) -> list[str]:
    failures: list[str] = []
    files = relative_files if relative_files is not None else git_source_files(root)
    for rel in files:
        if rel.startswith("build/") or rel.startswith("user_uploads/"):
            continue
        if Path(rel).suffix.lower() in IMAGE_SUFFIXES and rel not in ALLOWED_IMAGE_BINARY_PATHS:
            failures.append(f"image binary present in source path: {rel}")
    return failures


def audit_paths(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    failures.extend(audit_required_paths(root))
    failures.extend(audit_framework_files(root))
    failures.extend(audit_source_image_paths(root))
    return failures
