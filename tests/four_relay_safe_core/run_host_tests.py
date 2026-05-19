#!/usr/bin/env python3
"""Build and run host tests for the four-relay safe core."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "firmware" / "projects" / "four-relay-xbee-wifi" / "components" / "safe_core"
BUILD = ROOT / "build" / "tests" / "four_relay_safe_core"


def main() -> int:
    compiler = os.environ.get("CC", "cc")
    BUILD.mkdir(parents=True, exist_ok=True)
    output = BUILD / "test_safe_core"
    sources = [
        CORE / "src" / "api_contract.c",
        CORE / "src" / "config_store.c",
        CORE / "src" / "relay_state.c",
        CORE / "src" / "safety_supervisor.c",
        CORE / "src" / "storage_status.c",
        CORE / "src" / "xbee_frame.c",
        ROOT / "tests" / "four_relay_safe_core" / "test_safe_core.c",
    ]
    command = [
        compiler,
        "-std=c99",
        "-Wall",
        "-Wextra",
        "-Werror",
        "-I",
        str(CORE / "include"),
        *[str(source) for source in sources],
        "-o",
        str(output),
    ]
    subprocess.run(command, check=True, cwd=ROOT)
    subprocess.run([str(output)], check=True, cwd=ROOT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
