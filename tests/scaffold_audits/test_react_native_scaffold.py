from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import scaffold_audit_react_native as rn_audit  # noqa: E402


class ReactNativeScaffoldAuditTests(unittest.TestCase):
    def test_react_native_scaffold_audit_passes(self) -> None:
        self.assertEqual([], rn_audit.audit_react_native(ROOT))

    def test_expected_contract_ids_are_pinned(self) -> None:
        protocol = (ROOT / "packages/cbbs-protocol/src/index.ts").read_text(encoding="utf-8")
        for marker in [*rn_audit.EXPECTED_ROLES, *rn_audit.EXPECTED_VIEWS, *rn_audit.EXPECTED_INTENTS]:
            self.assertIn(marker, protocol)

    def test_native_project_directories_are_absent(self) -> None:
        for rel in rn_audit.NATIVE_DIRS:
            self.assertFalse((ROOT / rel).exists(), rel.as_posix())

    def test_windows_dependency_lane_is_scoped(self) -> None:
        windows_package = rn_audit._load_json(ROOT / "apps/cbbs-windows/package.json")
        windows_deps = rn_audit._deps(windows_package)
        for name, version in rn_audit.WINDOWS_RNW_DEPENDENCIES.items():
            self.assertEqual(version, windows_deps.get(name))

        for rel in [
            "package.json",
            "apps/cbbs-client/package.json",
            "packages/cbbs-ui/package.json",
            "packages/cbbs-protocol/package.json",
        ]:
            deps = rn_audit._deps(rn_audit._load_json(ROOT / rel))
            self.assertNotIn("react-native-windows", deps, rel)

    def test_windows_source_does_not_import_expo_ui_lane(self) -> None:
        source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in rn_audit._repo_ts_files(ROOT, "apps/cbbs-windows")
        )
        for marker in ["@cbbs/ui", "expo", "expo-router", "react-native-web"]:
            self.assertFalse(rn_audit._has_package_reference(source, marker), marker)


if __name__ == "__main__":
    unittest.main()
