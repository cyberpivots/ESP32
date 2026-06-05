from __future__ import annotations

import sys
import tempfile
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

    def test_non_windows_native_project_directories_are_absent(self) -> None:
        for rel in rn_audit.NATIVE_DIRS:
            self.assertFalse((ROOT / rel).exists(), rel.as_posix())

    def test_package_lock_outputs_are_absent(self) -> None:
        for rel in ["package-lock.json", "apps/cbbs-client/package-lock.json", "apps/cbbs-windows/package-lock.json"]:
            self.assertFalse((ROOT / rel).exists(), rel)

    def test_windows_native_surface_is_w3b_gated(self) -> None:
        windows_dir = ROOT / rn_audit.WINDOWS_NATIVE_DIR
        if not windows_dir.exists():
            return

        for rel in rn_audit.W3B_RECORD_FILES:
            self.assertTrue((ROOT / rel).exists(), rel.as_posix())
        for rel in rn_audit.W4_RECORD_FILES:
            self.assertTrue((ROOT / rel).exists(), rel.as_posix())
        self.assertEqual([], rn_audit._inspect_windows_native_surface(ROOT))

    def test_windows_entrypoint_status_is_build_launch_ready(self) -> None:
        source = (ROOT / "apps/cbbs-windows/src/index.tsx").read_text(encoding="utf-8")
        for marker in [
            'WINDOWS_APP_COMPONENT_NAME = "CbbsWindows"',
            "AppRegistry.registerComponent(WINDOWS_APP_COMPONENT_NAME",
            "legacyWindowsMigrationStatus",
            'defaultProductApp: "sysop"',
            "packageIdentityAccepted: false",
            "capabilityUseAccepted: false",
            "liveExecutionAvailable: false",
            "ProductWindowsShell",
        ]:
            self.assertIn(marker, source)

    def test_product_windows_apps_are_split(self) -> None:
        product = (ROOT / "packages/cbbs-product/src/index.ts").read_text(encoding="utf-8")
        for marker in ["CBBS Client", "CBBS Sysop", "CBBS Hardware Tools"]:
            self.assertIn(marker, product)
        for app in rn_audit.PRODUCT_WINDOWS_APPS:
            for rel in ["package.json", "index.js", "src/index.tsx", "tsconfig.json"]:
                self.assertTrue((ROOT / app / rel).exists(), f"{app}/{rel}")

    def test_windows_dependency_lane_is_scoped(self) -> None:
        for app in rn_audit.RNW_WINDOWS_APP_PACKAGES:
            windows_package = rn_audit._load_json(ROOT / app / "package.json")
            windows_deps = rn_audit._deps(windows_package)
            for name, version in rn_audit.WINDOWS_RNW_DEPENDENCIES.items():
                self.assertEqual(version, windows_deps.get(name), f"{app}:{name}")

        for rel in [
            "package.json",
            "apps/cbbs-client/package.json",
            "packages/cbbs-ui/package.json",
            "packages/cbbs-protocol/package.json",
        ]:
            deps = rn_audit._deps(rn_audit._load_json(ROOT / rel))
            self.assertNotIn("react-native-windows", deps, rel)

    def test_product_ui_uses_peer_react_native_boundary(self) -> None:
        package = rn_audit._load_json(ROOT / "packages/cbbs-product-ui/package.json")
        runtime_deps = package.get("dependencies")
        self.assertIsInstance(runtime_deps, dict)
        for name in ["react", "react-native", "react-native-windows", "expo", "expo-router", "react-native-web"]:
            self.assertNotIn(name, runtime_deps)

        peer_deps = package.get("peerDependencies")
        self.assertIsInstance(peer_deps, dict)
        self.assertEqual("19.2.3", peer_deps.get("react"))
        self.assertEqual(">=0.83.9 <0.86.0", peer_deps.get("react-native"))

    def test_current_windows_docs_do_not_expose_runtime_command_surface(self) -> None:
        readme = (ROOT / "apps/cbbs-windows/README.md").read_text(encoding="utf-8")
        self.assertIn("Future Tier 3 runtime command stays closed", readme)
        self.assertIsNone(rn_audit.FORBIDDEN_CURRENT_DOC_COMMAND_RE.search(readme))

    def test_windows_source_does_not_import_expo_ui_lane(self) -> None:
        source = "\n".join(
            path.read_text(encoding="utf-8")
            for path in rn_audit._repo_ts_files(ROOT, "apps/cbbs-windows")
        )
        for marker in ["@cbbs/ui", "expo", "expo-router", "react-native-web"]:
            self.assertFalse(rn_audit._has_package_reference(source, marker), marker)

    def test_tracked_generated_rnw_evidence_is_pinned(self) -> None:
        self.assertEqual([], rn_audit._audit_tracked_generated_evidence(ROOT))
        self.assertEqual(
            {
                Path("research/bench-records/react-native-windows/cbbs-windows-index.bundle"),
                Path("research/bench-records/react-native-windows/cbbs-windows-index.map"),
                Path("research/bench-records/react-native-windows/live-index.bundle"),
            },
            set(rn_audit.TRACKED_GENERATED_EVIDENCE),
        )

    def test_rnw_native_bridge_surface_audit_blocks_dispatch_symbols(self) -> None:
        self.assertEqual([], rn_audit._inspect_rnw_native_bridge_surfaces(ROOT))

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            source_dir = temp_root / "apps/cbbs-hardware-tools-windows/windows/CbbsHardwareToolsWindows"
            source_dir.mkdir(parents=True)
            (source_dir / "HostCommandBridge.cpp").write_text(
                """
                REACT_MODULE(HostCommandBridge);
                REACT_METHOD(OpenPort);
                void Start() { CreateProcessW(nullptr, nullptr, nullptr, nullptr, false, 0, nullptr, nullptr, nullptr, nullptr); }
                """,
                encoding="utf-8",
            )

            failures = rn_audit._inspect_rnw_native_bridge_surfaces(temp_root)

        self.assertTrue(any("HostCommandBridge native symbol" in failure for failure in failures), failures)
        self.assertTrue(any("REACT_MODULE" in failure for failure in failures), failures)
        self.assertTrue(any("REACT_METHOD" in failure for failure in failures), failures)
        self.assertTrue(any("CreateProcess" in failure for failure in failures), failures)


if __name__ == "__main__":
    unittest.main()
