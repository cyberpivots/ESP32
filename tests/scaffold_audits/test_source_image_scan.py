#!/usr/bin/env python3
"""Regression tests for scaffold source-image scanning."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from scaffold_audit_paths import audit_source_image_paths  # noqa: E402


class SourceImageScanTests(unittest.TestCase):
    def test_ignored_build_webp_does_not_fail(self) -> None:
        failures = audit_source_image_paths(
            relative_files=[
                "build/alternate-pages/assets/generated-preview.webp",
                "site/github-pages/assets/workbench/hero-workbench.webp",
            ]
        )
        self.assertEqual([], failures)

    def test_unallowlisted_source_image_fails(self) -> None:
        failures = audit_source_image_paths(
            relative_files=["docs/projects/four-relay-xbee-wifi/unreviewed.png"]
        )
        self.assertEqual(
            ["image binary present in source path: docs/projects/four-relay-xbee-wifi/unreviewed.png"],
            failures,
        )


if __name__ == "__main__":
    unittest.main()
