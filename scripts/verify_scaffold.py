#!/usr/bin/env python3
"""Validate the ESP32 workspace scaffold."""

from __future__ import annotations

import sys

from scaffold_audit_docs import audit_docs
from scaffold_audit_firmware import audit_firmware
from scaffold_audit_pages import audit_pages
from scaffold_audit_paths import audit_paths
from scaffold_audit_sources import audit_sources


AUDITS = [
    audit_paths,
    audit_sources,
    audit_docs,
    audit_firmware,
    audit_pages,
]


def main() -> int:
    failures: list[str] = []
    for audit in AUDITS:
        failures.extend(audit())

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print("PASS: ESP32 scaffold validation succeeded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
