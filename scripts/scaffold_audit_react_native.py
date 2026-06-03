#!/usr/bin/env python3
"""Audit the host-only CBBS React Native client scaffold."""

from __future__ import annotations

import json
import re
import sys
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

NATIVE_DIRS = [
    Path("apps/cbbs-client/android"),
    Path("apps/cbbs-client/ios"),
    Path("apps/cbbs-client/windows"),
    Path("apps/cbbs-client/macos"),
    Path("apps/cbbs-windows/android"),
    Path("apps/cbbs-windows/ios"),
    Path("apps/cbbs-windows/windows"),
    Path("apps/cbbs-windows/macos"),
]
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
    for rel in FORBIDDEN_CONFIG_FILES:
        if (root / rel).exists():
            failures.append(f"external service/native config file must not exist: {rel.as_posix()}")

    package_blob = "\n".join(_read(path) for path in _package_json_paths(root))
    for term in FORBIDDEN_PACKAGE_TERMS:
        if term.lower() in package_blob.lower():
            failures.append(f"package manifests contain forbidden dependency/config term: {term}")
    if FORBIDDEN_SCRIPT_RE.search(package_blob):
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
            for name in ["react-native-windows"]:
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
        "no generated native Windows",
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
        "../research/cbbs-react-native/README.md",
        "../.agents/TASK_LOG/0150-cbbs-react-native-windows-client-sysop-w0-w1.md",
        "../.agents/handoffs/0111-cbbs-react-native-windows-client-sysop-w0-w1-to-qa.md",
        "../.agents/TASK_LOG/0151-cbbs-react-native-windows-w2-dependency-lane.md",
        "../.agents/handoffs/0112-cbbs-react-native-windows-w2-to-qa.md",
        "../.agents/TASK_LOG/0153-cbbs-react-native-windows-w21-local-shell.md",
        "../.agents/handoffs/0113-cbbs-react-native-windows-w21-local-shell-to-qa.md",
        "../.agents/TASK_LOG/0154-cbbs-react-native-windows-w3a-toolchain-preflight.md",
        "../.agents/handoffs/0114-cbbs-react-native-windows-w3a-toolchain-to-qa.md",
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
