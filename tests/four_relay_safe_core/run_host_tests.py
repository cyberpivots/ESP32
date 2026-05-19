#!/usr/bin/env python3
"""Build and run host tests for the four-relay safe core."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "firmware" / "projects" / "four-relay-xbee-wifi" / "components" / "safe_core"
BUILD = ROOT / "build" / "tests" / "four_relay_safe_core"


CORE_SOURCES = [
    CORE / "src" / "api_contract.c",
    CORE / "src" / "api_model.c",
    CORE / "src" / "config_store.c",
    CORE / "src" / "relay_state.c",
    CORE / "src" / "safety_supervisor.c",
    CORE / "src" / "storage_status.c",
    CORE / "src" / "xbee_frame.c",
]

TEST_SOURCES = [
    ROOT / "tests" / "four_relay_safe_core" / "test_relay_safety.c",
    ROOT / "tests" / "four_relay_safe_core" / "test_http_api_contracts.c",
    ROOT / "tests" / "four_relay_safe_core" / "test_storage_contracts.c",
    ROOT / "tests" / "four_relay_safe_core" / "test_xbee_frame_codec.c",
]


def build_and_run(compiler: str, test_source: Path) -> None:
    output = BUILD / test_source.stem
    command = [
        compiler,
        "-std=c99",
        "-Wall",
        "-Wextra",
        "-Werror",
        "-I",
        str(CORE / "include"),
        "-I",
        str(ROOT / "tests" / "four_relay_safe_core"),
        *[str(source) for source in CORE_SOURCES],
        str(test_source),
        "-o",
        str(output),
    ]
    subprocess.run(command, check=True, cwd=ROOT)
    subprocess.run([str(output)], check=True, cwd=ROOT)


def main() -> int:
    compiler = os.environ.get("CC", "cc")
    BUILD.mkdir(parents=True, exist_ok=True)
    for test_source in TEST_SOURCES:
        build_and_run(compiler, test_source)
    print("PASS: four_relay_safe_core split host tests succeeded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
