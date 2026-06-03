#!/usr/bin/env python3
"""Audit the host-only CBBS React Native client scaffold."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from scaffold_audit_data import ROOT


REQUIRED_SOURCE_IDS = [
    "SRC-REACT-NATIVE-VERSIONS-2026-06-02",
    "SRC-REACT-NATIVE-ENV-SETUP-2026-06-02",
    "SRC-EXPO-SDK-56-REFERENCE-2026-06-02",
    "SRC-EXPO-MONOREPOS-2026-06-02",
    "SRC-EXPO-ROUTER-2026-06-02",
    "SRC-EXPO-NEW-ARCHITECTURE-2026-06-02",
    "SRC-EXPO-EAS-BUILD-2026-06-02",
    "SRC-REACT-NATIVE-WEB-2026-06-02",
    "SRC-REACT-NATIVE-WINDOWS-SUPPORT-2026-06-02",
    "SRC-ANDROID-NETWORK-OPS-2026-06-02",
    "SRC-ANDROID-BLUETOOTH-PERMISSIONS-2026-06-02",
    "SRC-ANDROID-WIFI-PERMISSIONS-2026-06-02",
    "SRC-APPLE-LOCAL-NETWORK-PRIVACY-2026-06-02",
    "SRC-APPLE-CORE-BLUETOOTH-2026-06-02",
    "SRC-MICROSOFT-APP-CENTER-RETIREMENT-2026-06-02",
    "SRC-LOCAL-CBBS-REACT-NATIVE-CLIENT-PLATFORM-2026-06-02",
    "SRC-REACT-NATIVE-WINDOWS-DEPENDENCIES-2026-06-02",
    "SRC-REACT-NATIVE-WINDOWS-GETTING-STARTED-2026-06-02",
    "SRC-REACT-NATIVE-WINDOWS-CLI-2026-06-02",
    "SRC-REACT-NATIVE-WINDOWS-PACKAGE-DEPS-2026-06-03",
    "SRC-WINDOWS-APP-CAPABILITIES-2026-06-02",
    "SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W0-W1-2026-06-02",
    "SRC-NPM-RNW-DEPENDENCY-METADATA-2026-06-02",
    "SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W2-2026-06-02",
    "SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W21-2026-06-02",
    "SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W3A-2026-06-03",
    "SRC-REACT-NATIVE-WINDOWS-CPP-APP-TEMPLATE-2026-06-03",
    "SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W3B-2026-06-03",
]

WINDOWS_RNW_DEPENDENCIES = {
    "react": "19.2.3",
    "react-native": "0.83.9",
    "react-native-windows": "0.83.0",
}

EXPECTED_ROLES = ["client", "sysop", "monitor", "devconfig"]
EXPECTED_VIEWS = [
    "home",
    "messages",
    "downloads",
    "peers",
    "network",
    "diagnostics",
    "safety",
    "config",
    "evidence",
]
EXPECTED_INTENTS = [
    "navigate",
    "refresh",
    "filter",
    "select_row",
    "open_detail",
    "compose_draft",
    "queue_file_request",
    "ack_local",
    "view_proof",
]

WINDOWS_NATIVE_DIR = Path("apps/cbbs-windows/windows")
NATIVE_DIRS = [
    Path("apps/cbbs-client/android"),
    Path("apps/cbbs-client/ios"),
    Path("apps/cbbs-client/windows"),
    Path("apps/cbbs-client/macos"),
    Path("apps/cbbs-windows/android"),
    Path("apps/cbbs-windows/ios"),
    Path("apps/cbbs-windows/macos"),
]
W3B_RECORD_FILES = [
    Path(".agents/TASK_LOG/0155-cbbs-react-native-windows-w3b-native-generation.md"),
    Path(".agents/handoffs/0115-cbbs-react-native-windows-w3b-native-generation-to-qa.md"),
    Path("knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-w3b.md"),
]
EXPECTED_WINDOWS_NATIVE_FILES = [
    Path("CbbsWindows.sln"),
    Path("CbbsWindows/CbbsWindows.vcxproj"),
    Path("CbbsWindows.Package/Package.appxmanifest"),
]
ALLOWED_WINDOWS_TEMPLATE_CAPABILITIES = {"internetClient", "runFullTrust"}
FORBIDDEN_WINDOWS_OUTPUT_DIRS = {
    ".vs",
    "AppPackages",
    "bin",
    "obj",
    "Debug",
    "Release",
}
FORBIDDEN_WINDOWS_OUTPUT_SUFFIXES = {
    ".appx",
    ".appxbundle",
    ".cer",
    ".msix",
    ".msixbundle",
    ".p12",
    ".pem",
    ".pfx",
    ".pvk",
    ".snk",
}
FORBIDDEN_WINDOWS_OUTPUT_NAMES = {
    "Package.StoreAssociation.xml",
}
FORBIDDEN_CONFIG_FILES = [
    Path("eas.json"),
    Path("apps/cbbs-client/eas.json"),
    Path("apps/cbbs-client/appcenter-config.json"),
    Path("apps/cbbs-client/AppCenter-Config.plist"),
    Path("apps/cbbs-windows/eas.json"),
    Path("apps/cbbs-windows/appcenter-config.json"),
    Path("apps/cbbs-windows/AppCenter-Config.plist"),
    Path("apps/cbbs-windows/Package.appxmanifest"),
    Path("apps/cbbs-windows/AndroidManifest.xml"),
    Path("apps/cbbs-windows/Info.plist"),
]
FORBIDDEN_PACKAGE_TERMS = [
    "appcenter",
    "eas-cli",
    "expo-dev-client",
    "react-native-ble",
    "react-native-bluetooth",
    "react-native-tcp-socket",
    "react-native-udp",
]
FORBIDDEN_SCRIPT_RE = re.compile(
    r"\b(expo\s+prebuild|expo\s+run:|eas\s+(build|submit|update|deploy|login)|"
    r"react-native\s+run-|run-windows|init-windows|react-native-windows-init|"
    r"msbuild|devenv|MakeAppx|signtool|gradlew|xcodebuild|pod\s+install|appcenter|store\s+upload)\b",
    re.IGNORECASE,
)
FORBIDDEN_LIVE_SOURCE_RE = re.compile(
    r"\b(fetch\s*\(|new\s+WebSocket|navigator\.bluetooth|navigator\.serial|"
    r"BluetoothDevice|SerialPort|BLEManager|writeFlash)\b",
    re.IGNORECASE,
)
SECRET_FIXTURE_RE = re.compile(
    r"\b(token|secret|pmk|lmk|password|privateKey|deviceId|androidId|macAddress|"
    r"messageBody|fileContent|preciseLocation)\b",
    re.IGNORECASE,
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def _deps(package: dict[str, object]) -> dict[str, str]:
    deps: dict[str, str] = {}
    for section in ["dependencies", "devDependencies", "peerDependencies", "optionalDependencies"]:
        values = package.get(section)
        if isinstance(values, dict):
            deps.update({str(key): str(value) for key, value in values.items()})
    return deps


def _lockfile_importers(root: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        return {}
    lockfile = yaml.safe_load(_read(root / "pnpm-lock.yaml"))
    if not isinstance(lockfile, dict):
        return {}
    importers = lockfile.get("importers")
    return importers if isinstance(importers, dict) else {}


def _require_text(path: Path, markers: list[str], label: str) -> list[str]:
    text = _read(path)
    return [f"{label} missing marker: {marker}" for marker in markers if marker not in text]


def _package_json_paths(root: Path) -> list[Path]:
    return sorted([root / "package.json", *root.glob("apps/*/package.json"), *root.glob("packages/*/package.json")])


def _package_script_blob(root: Path) -> str:
    scripts: list[str] = []
    for path in _package_json_paths(root):
        package = _load_json(path)
        values = package.get("scripts")
        if isinstance(values, dict):
            for name, command in values.items():
                scripts.append(f"{path.relative_to(root).as_posix()}#{name}: {command}")
    return "\n".join(scripts)


def _repo_ts_files(root: Path, rel: str) -> list[Path]:
    ignored_parts = {"node_modules", "dist", "build", "coverage", ".expo"}
    base = root / rel
    return sorted(
        path
        for path in base.rglob("*.ts*")
        if path.is_file()
        and not path.name.endswith(".tsbuildinfo")
        and not ignored_parts.intersection(path.relative_to(base).parts)
    )


def _has_package_reference(text: str, package_name: str) -> bool:
    package_re = re.compile(rf"(?<![\w@.-]){re.escape(package_name)}(?=$|[\"'\s;/])")
    return bool(package_re.search(text))


def _xml_local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _manifest_capabilities(path: Path) -> set[str]:
    tree = ET.parse(path)
    capabilities: set[str] = set()
    for element in tree.iter():
        if _xml_local_name(element.tag) in {"Capability", "DeviceCapability"}:
            name = element.attrib.get("Name")
            if name:
                capabilities.add(name)
    return capabilities


def _inspect_windows_native_surface(root: Path) -> list[str]:
    failures: list[str] = []
    native_dir = root / WINDOWS_NATIVE_DIR
    if not native_dir.exists():
        return failures

    for rel in W3B_RECORD_FILES:
        if not (root / rel).exists():
            failures.append(f"W3B native surface exists without record: {rel.as_posix()}")
    for rel in EXPECTED_WINDOWS_NATIVE_FILES:
        if not (native_dir / rel).exists():
            failures.append(f"W3B Windows native surface missing expected file: {rel.as_posix()}")

    for path in sorted(native_dir.rglob("*")):
        rel = path.relative_to(native_dir)
        if any(part in FORBIDDEN_WINDOWS_OUTPUT_DIRS for part in rel.parts):
            failures.append(f"W3B Windows native surface contains build output dir: {rel.as_posix()}")
        if path.is_file():
            if path.name in FORBIDDEN_WINDOWS_OUTPUT_NAMES:
                failures.append(f"W3B Windows native surface contains store/signing file: {rel.as_posix()}")
            if path.suffix.lower() in FORBIDDEN_WINDOWS_OUTPUT_SUFFIXES:
                failures.append(f"W3B Windows native surface contains package/signing artifact: {rel.as_posix()}")

    manifests = sorted(native_dir.rglob("Package.appxmanifest"))
    if len(manifests) != 1:
        failures.append(f"W3B Windows native surface must contain exactly one Package.appxmanifest, found {len(manifests)}")
        return failures

    manifest = manifests[0]
    try:
        capabilities = _manifest_capabilities(manifest)
    except ET.ParseError as exc:
        failures.append(f"W3B Package.appxmanifest is not valid XML: {exc}")
        return failures
    extra_capabilities = capabilities - ALLOWED_WINDOWS_TEMPLATE_CAPABILITIES
    missing_capabilities = ALLOWED_WINDOWS_TEMPLATE_CAPABILITIES - capabilities
    if extra_capabilities:
        failures.append(
            "W3B Package.appxmanifest has unapproved capabilities: "
            + ", ".join(sorted(extra_capabilities))
        )
    if missing_capabilities:
        failures.append(
            "W3B Package.appxmanifest missing reviewed template capabilities: "
            + ", ".join(sorted(missing_capabilities))
        )

    manifest_text = _read(manifest)
    for marker in ["Identity", "Publisher=", "TargetDeviceFamily", "internetClient", "runFullTrust"]:
        if marker not in manifest_text:
            failures.append(f"W3B Package.appxmanifest missing marker: {marker}")

    return failures


def audit_react_native(root: Path = ROOT) -> list[str]:
    failures: list[str] = []

    source_index = _read(root / "knowledge-base" / "source-index.md")
    for source_id in REQUIRED_SOURCE_IDS:
        if source_id not in source_index:
            failures.append(f"source index missing {source_id}")

    adr = root / ".agents" / "DECISIONS" / "ADR-0010-cbbs-react-native-client-platform.md"
    if not adr.exists():
        failures.append("missing ADR-0010")
    else:
        failures.extend(_require_text(adr, ["Status: Accepted", "client/operator apps", "Stop Gates"], "ADR-0010"))

    for rel in [
        "pnpm-workspace.yaml",
        "package.json",
        "apps/cbbs-client/app.json",
        "apps/cbbs-client/app/index.tsx",
        "apps/cbbs-windows/README.md",
        "apps/cbbs-windows/src/index.tsx",
        "packages/cbbs-protocol/src/index.ts",
        "packages/cbbs-fixtures/src/index.ts",
        "packages/cbbs-state/src/index.ts",
        "packages/cbbs-ui/src/index.tsx",
        "docs/projects/cbbs-react-native/README.md",
        "research/cbbs-react-native/README.md",
        "tools/react-native/README.md",
        ".codex/skills/react-native-client-development/SKILL.md",
        ".agents/TASK_LOG/0150-cbbs-react-native-windows-client-sysop-w0-w1.md",
        ".agents/handoffs/0111-cbbs-react-native-windows-client-sysop-w0-w1-to-qa.md",
        "knowledge-base/source-ledger/2026-06-02-cbbs-react-native-windows-w0-w1.md",
        ".agents/TASK_LOG/0151-cbbs-react-native-windows-w2-dependency-lane.md",
        ".agents/handoffs/0112-cbbs-react-native-windows-w2-to-qa.md",
        "knowledge-base/source-ledger/2026-06-02-cbbs-react-native-windows-w2.md",
        ".agents/TASK_LOG/0153-cbbs-react-native-windows-w21-local-shell.md",
        ".agents/handoffs/0113-cbbs-react-native-windows-w21-local-shell-to-qa.md",
        "knowledge-base/source-ledger/2026-06-02-cbbs-react-native-windows-w21.md",
        ".agents/TASK_LOG/0154-cbbs-react-native-windows-w3a-toolchain-preflight.md",
        ".agents/handoffs/0114-cbbs-react-native-windows-w3a-toolchain-to-qa.md",
        "knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-w3a.md",
        ".agents/TASK_LOG/0155-cbbs-react-native-windows-w3b-native-generation.md",
        ".agents/handoffs/0115-cbbs-react-native-windows-w3b-native-generation-to-qa.md",
        "knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-w3b.md",
    ]:
        if not (root / rel).exists():
            failures.append(f"missing React Native scaffold file: {rel}")

    workspace = _read(root / "pnpm-workspace.yaml")
    for marker in ["apps/*", "packages/*"]:
        if marker not in workspace:
            failures.append(f"pnpm-workspace.yaml missing {marker}")

    root_package = _load_json(root / "package.json")
    if root_package.get("packageManager", "").split("@", 1)[0] != "pnpm":
        failures.append("root package.json must pin pnpm packageManager")
    engines = root_package.get("engines")
    if not isinstance(engines, dict) or "22.13.0" not in str(engines.get("node", "")):
        failures.append("root package.json must require Node >=22.13.0")

    for rel in NATIVE_DIRS:
        if (root / rel).exists():
            failures.append(f"native project directory must not exist: {rel.as_posix()}")
    failures.extend(_inspect_windows_native_surface(root))
    for rel in FORBIDDEN_CONFIG_FILES:
        if (root / rel).exists():
            failures.append(f"external service/native config file must not exist: {rel.as_posix()}")
    for path in sorted([root / "package-lock.json", *root.glob("apps/*/package-lock.json"), *root.glob("packages/*/package-lock.json")]):
        if path.exists():
            failures.append(f"npm package-lock output must not exist in tracked package roots: {path.relative_to(root).as_posix()}")

    package_blob = "\n".join(_read(path) for path in _package_json_paths(root))
    for term in FORBIDDEN_PACKAGE_TERMS:
        if term.lower() in package_blob.lower():
            failures.append(f"package manifests contain forbidden dependency/config term: {term}")
    if FORBIDDEN_SCRIPT_RE.search(_package_script_blob(root)):
        failures.append("package scripts contain native, EAS, App Center, or release commands")

    windows_package = _load_json(root / "apps" / "cbbs-windows" / "package.json")
    windows_deps = _deps(windows_package)
    for name, version in WINDOWS_RNW_DEPENDENCIES.items():
        if windows_deps.get(name) != version:
            failures.append(f"apps/cbbs-windows/package.json must pin {name} to {version}")
    for forbidden in ["@cbbs/ui", "expo", "expo-router", "react-native-web"]:
        if forbidden in windows_deps:
            failures.append(f"apps/cbbs-windows/package.json must not depend on {forbidden}")

    for path in _package_json_paths(root):
        rel = path.relative_to(root).as_posix()
        deps = _deps(_load_json(path))
        if rel != "apps/cbbs-windows/package.json":
            for name in ["react-native-windows", "@rnx-kit/jest-preset"]:
                if name in deps:
                    failures.append(f"{rel} must not depend on {name}")
        if rel in {"package.json", "apps/cbbs-client/package.json"} or rel.startswith("packages/"):
            if deps.get("react-native") == WINDOWS_RNW_DEPENDENCIES["react-native"]:
                failures.append(f"{rel} must not use the Windows RN {WINDOWS_RNW_DEPENDENCIES['react-native']} lane")

    importers = _lockfile_importers(root)
    windows_importer = importers.get("apps/cbbs-windows")
    if not isinstance(windows_importer, dict):
        failures.append("pnpm-lock.yaml missing apps/cbbs-windows importer")
    else:
        importer_deps: dict[str, str] = {}
        for section in ["dependencies", "devDependencies", "peerDependencies"]:
            values = windows_importer.get(section)
            if isinstance(values, dict):
                for name, meta in values.items():
                    if isinstance(meta, dict) and "specifier" in meta:
                        importer_deps[str(name)] = str(meta["specifier"])
        for name, version in WINDOWS_RNW_DEPENDENCIES.items():
            if importer_deps.get(name) != version:
                failures.append(f"pnpm-lock.yaml apps/cbbs-windows importer must pin {name} to {version}")
    for importer_name, importer in importers.items():
        if importer_name == "apps/cbbs-windows" or not isinstance(importer, dict):
            continue
        for section in ["dependencies", "devDependencies", "peerDependencies"]:
            values = importer.get(section)
            if isinstance(values, dict) and "react-native-windows" in values:
                failures.append(f"pnpm-lock.yaml importer {importer_name} must not include react-native-windows")

    protocol_text = _read(root / "packages" / "cbbs-protocol" / "src" / "index.ts")
    for marker in [
        *EXPECTED_ROLES,
        *EXPECTED_VIEWS,
        *EXPECTED_INTENTS,
        "MAX_UI_INTENT_BYTES = 512",
        "LOCAL_ONLY_REASON",
        "ALLOWED_UI_INTENT_KEYS",
        "findForbiddenMetadataFields",
        "localOnlyReason must be fixture-only-ui-intent",
    ]:
        if marker not in protocol_text:
            failures.append(f"protocol contract missing marker: {marker}")
    for marker in [
        "bridge_abi",
        "serial_abi",
        "firmware_abi",
        "gate_f_service_code",
        "native_windows_project",
        "external_service_build",
    ]:
        if marker not in protocol_text:
            failures.append(f"protocol closed-surface contract missing marker: {marker}")

    app_source = "\n".join(_read(path) for path in _repo_ts_files(root, "apps"))
    package_source = "\n".join(_read(path) for path in _repo_ts_files(root, "packages"))
    for label, text in [("app source", app_source), ("package source", package_source)]:
        if FORBIDDEN_LIVE_SOURCE_RE.search(text):
            failures.append(f"{label} contains forbidden live transport/native API marker")

    fixture_text = _read(root / "packages" / "cbbs-fixtures" / "src" / "index.ts")
    if SECRET_FIXTURE_RE.search(fixture_text):
        failures.append("fixtures contain secret-like field names")
    for marker in ["CLOSED_SURFACE_IDS.map", "roleProfiles", "client", "sysop"]:
        if marker not in fixture_text:
            failures.append(f"fixtures missing W1 parity marker: {marker}")

    ui_text = _read(root / "packages" / "cbbs-ui" / "src" / "index.tsx")
    for marker in [
        "cbbs-view-tab-",
        "cbbs-action-",
        "cbbs-closed-surface-",
        "accessibilityState={{ disabled: true }}",
        "proof.id",
    ]:
        if marker not in ui_text:
            failures.append(f"UI missing W1 parity marker: {marker}")

    windows_text = _read(root / "apps" / "cbbs-windows" / "src" / "index.tsx")
    for marker in [
        "package-only-rnw-dependency-lane",
        "WindowsClientSysopShell",
        "createWindowsLocalIntent",
        "single-role-aware-windows-app",
        "nativeDependencySelected: true",
        "react-native-windows",
        "0.83.0",
        "native_windows_project",
        "live_transport",
        "LOCAL_ONLY_REASON",
        "CLOSED_SURFACE_IDS",
        "localIntent(",
        "windows-view-",
        "windows-action-",
        "windows-closed-surface-",
        "accessibilityState={{ disabled: true }}",
        "Transcript-first Windows fixture evidence",
    ]:
        if marker not in windows_text:
            failures.append(f"Windows spike missing W0/W1 marker: {marker}")
    windows_readme = _read(root / "apps" / "cbbs-windows" / "README.md")
    for marker in [
        "package-only RNW dependency selection",
        "react-native-windows",
        "0.83.0",
        "react-native` `0.83.9",
        "19.2.3",
        "W3B native generation gate",
        "build/run remains closed",
    ]:
        if marker not in windows_readme:
            failures.append(f"Windows README missing W2 marker: {marker}")
    if "No RNW dependency" in windows_readme:
        failures.append("Windows README must not claim W2 has no RNW dependency")
    windows_source = "\n".join(_read(path) for path in _repo_ts_files(root, "apps/cbbs-windows"))
    for forbidden in ["@cbbs/ui", "expo", "expo-router", "react-native-web"]:
        if _has_package_reference(windows_source, forbidden):
            failures.append(f"apps/cbbs-windows source must not import or reference {forbidden}")

    ci_text = _read(root / ".github" / "workflows" / "scaffold-ci.yml")
    for marker in [
        "pnpm install --frozen-lockfile",
        "pnpm lint",
        "pnpm typecheck",
        "pnpm test",
        "pnpm --filter @cbbs/client exec expo-doctor",
        "pnpm --filter @cbbs/windows-spike typecheck",
    ]:
        if marker not in ci_text:
            failures.append(f"scaffold CI missing React Native validation marker: {marker}")

    docs_index = _read(root / "docs" / "index.md")
    for marker in [
        "projects/cbbs-react-native/README.md",
        "../.agents/DECISIONS/ADR-0010-cbbs-react-native-client-platform.md",
        "../knowledge-base/source-ledger/2026-06-02-cbbs-react-native-client-platform.md",
        "../knowledge-base/source-ledger/2026-06-02-cbbs-react-native-windows-w0-w1.md",
        "../knowledge-base/source-ledger/2026-06-02-cbbs-react-native-windows-w2.md",
        "../knowledge-base/source-ledger/2026-06-02-cbbs-react-native-windows-w21.md",
        "../knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-w3a.md",
        "../knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-w3b.md",
        "../research/cbbs-react-native/README.md",
        "../.agents/TASK_LOG/0150-cbbs-react-native-windows-client-sysop-w0-w1.md",
        "../.agents/handoffs/0111-cbbs-react-native-windows-client-sysop-w0-w1-to-qa.md",
        "../.agents/TASK_LOG/0151-cbbs-react-native-windows-w2-dependency-lane.md",
        "../.agents/handoffs/0112-cbbs-react-native-windows-w2-to-qa.md",
        "../.agents/TASK_LOG/0153-cbbs-react-native-windows-w21-local-shell.md",
        "../.agents/handoffs/0113-cbbs-react-native-windows-w21-local-shell-to-qa.md",
        "../.agents/TASK_LOG/0154-cbbs-react-native-windows-w3a-toolchain-preflight.md",
        "../.agents/handoffs/0114-cbbs-react-native-windows-w3a-toolchain-to-qa.md",
        "../.agents/TASK_LOG/0155-cbbs-react-native-windows-w3b-native-generation.md",
        "../.agents/handoffs/0115-cbbs-react-native-windows-w3b-native-generation-to-qa.md",
    ]:
        if marker not in docs_index:
            failures.append(f"docs index missing React Native link: {marker}")

    return failures


def main() -> int:
    failures = audit_react_native()
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1
    print("PASS: CBBS React Native scaffold audit succeeded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
