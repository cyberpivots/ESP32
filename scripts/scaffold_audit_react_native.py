#!/usr/bin/env python3
"""Audit the host-only CBBS React Native client scaffold."""

from __future__ import annotations

import json
import hashlib
import os
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
    "SRC-REACT-NATIVE-WINDOWS-RUN-WINDOWS-2026-06-03",
    "SRC-REACT-NATIVE-WINDOWS-STORE-PUBLISHING-2026-06-03",
    "SRC-WINDOWS-APP-CAPABILITIES-2026-06-02",
    "SRC-MICROSOFT-MSIX-SIGNING-2026-06-03",
    "SRC-MICROSOFT-WINDOWS-CODE-SIGNING-OPTIONS-2026-06-03",
    "SRC-MICROSOFT-WINDOWS-SIDELOADING-2026-06-03",
    "SRC-MICROSOFT-MSIX-UNSIGNED-2026-06-03",
    "SRC-MICROSOFT-MSIX-APP-INSTALLER-2026-06-03",
    "SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W0-W1-2026-06-02",
    "SRC-NPM-RNW-DEPENDENCY-METADATA-2026-06-02",
    "SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W2-2026-06-02",
    "SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W21-2026-06-02",
    "SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W3A-2026-06-03",
    "SRC-REACT-NATIVE-WINDOWS-CPP-APP-TEMPLATE-2026-06-03",
    "SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W3B-2026-06-03",
    "SRC-LOCAL-CBBS-REACT-NATIVE-WINDOWS-W4-PRE-RELEASE-2026-06-03",
    "SRC-LOCAL-CBBS-RNW-SOURCE-UI-MUTATION-2026-06-03",
    "SRC-LOCAL-CBBS-RNW-SPLIT-RUNTIME-PROOF-AND-AGENTS-2026-06-03",
    "SRC-LOCAL-CBBS-RNW-SPLIT-NATIVE-GENERATION-2026-06-04",
    "SRC-LOCAL-CBBS-RNW-SPLIT-BUILD-INSTALL-LAUNCH-2026-06-04",
    "SRC-LOCAL-CBBS-HOST-COMMAND-BRIDGE-LIVE-GATE-BLOCKED-2026-06-04",
    "SRC-LOCAL-CBBS-XBEE-KNOWN-PROFILE-WRITE-GATE-BLOCKED-2026-06-04",
    "SRC-REACT-NATIVE-USE-WINDOW-DIMENSIONS-2026-06-05",
    "SRC-MICROSOFT-WINDOWS-APPWINDOW-DISPLAYAREA-2026-06-05",
    "SRC-ESPRESSIF-ESPTOOL-FIRMWARE-2026-06-05",
    "SRC-ESP-IDF-OTA-PLANNING-2026-06-05",
    "SRC-ESP-IDF-WIFI-SNIFFER-2026-06-05",
    "SRC-LOCAL-CBBS-RNW-HARDWARE-TOOLS-HOST-ONLY-IMPROVEMENTS-2026-06-05",
]

WINDOWS_RNW_DEPENDENCIES = {
    "react": "19.2.3",
    "react-native": "0.83.9",
    "react-native-windows": "0.83.0",
}
PRODUCT_WINDOWS_APPS = [
    "apps/cbbs-client-windows",
    "apps/cbbs-sysop-windows",
    "apps/cbbs-hardware-tools-windows",
]
RNW_WINDOWS_APP_PACKAGES = [
    "apps/cbbs-windows",
    *PRODUCT_WINDOWS_APPS,
]

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
SPLIT_WINDOWS_NATIVE_DIRS = [
    Path("apps/cbbs-client-windows/windows"),
    Path("apps/cbbs-sysop-windows/windows"),
    Path("apps/cbbs-hardware-tools-windows/windows"),
]
NATIVE_DIRS = [
    Path("apps/cbbs-client/android"),
    Path("apps/cbbs-client/ios"),
    Path("apps/cbbs-client/windows"),
    Path("apps/cbbs-client/macos"),
    Path("apps/cbbs-windows/android"),
    Path("apps/cbbs-windows/ios"),
    Path("apps/cbbs-windows/macos"),
    *[Path(app) / "android" for app in PRODUCT_WINDOWS_APPS],
    *[Path(app) / "ios" for app in PRODUCT_WINDOWS_APPS],
    *[Path(app) / "macos" for app in PRODUCT_WINDOWS_APPS],
]
W3B_RECORD_FILES = [
    Path(".agents/TASK_LOG/0155-cbbs-react-native-windows-w3b-native-generation.md"),
    Path(".agents/handoffs/0115-cbbs-react-native-windows-w3b-native-generation-to-qa.md"),
    Path("knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-w3b.md"),
]
W4_RECORD_FILES = [
    Path(".agents/TASK_LOG/0156-cbbs-react-native-windows-w4-pre-release.md"),
    Path(".agents/handoffs/0116-cbbs-react-native-windows-w4-pre-release-to-qa-release.md"),
    Path("knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-w4-pre-release.md"),
]
SPLIT_NATIVE_RECORD_FILES = [
    Path(".agents/TASK_LOG/0163-cbbs-rnw-split-native-generation.md"),
    Path(".agents/handoffs/0122-cbbs-rnw-split-native-generation-to-qa.md"),
    Path("knowledge-base/source-ledger/2026-06-04-cbbs-rnw-split-native-generation.md"),
]
EXPECTED_WINDOWS_NATIVE_FILES = [
    Path("CbbsWindows.sln"),
    Path("CbbsWindows/CbbsWindows.vcxproj"),
    Path("CbbsWindows.Package/Package.appxmanifest"),
]
EXPECTED_SPLIT_WINDOWS_NATIVE_FILES = {
    Path("apps/cbbs-client-windows/windows"): [
        Path("CbbsClientWindows.sln"),
        Path("CbbsClientWindows/CbbsClientWindows.vcxproj"),
        Path("CbbsClientWindows.Package/Package.appxmanifest"),
    ],
    Path("apps/cbbs-sysop-windows/windows"): [
        Path("CbbsSysopWindows.sln"),
        Path("CbbsSysopWindows/CbbsSysopWindows.vcxproj"),
        Path("CbbsSysopWindows.Package/Package.appxmanifest"),
    ],
    Path("apps/cbbs-hardware-tools-windows/windows"): [
        Path("CbbsHardwareToolsWindows.sln"),
        Path("CbbsHardwareToolsWindows/CbbsHardwareToolsWindows.vcxproj"),
        Path("CbbsHardwareToolsWindows.Package/Package.appxmanifest"),
    ],
}
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
    *[Path(app) / "eas.json" for app in PRODUCT_WINDOWS_APPS],
    *[Path(app) / "appcenter-config.json" for app in PRODUCT_WINDOWS_APPS],
    *[Path(app) / "AppCenter-Config.plist" for app in PRODUCT_WINDOWS_APPS],
    *[Path(app) / "Package.appxmanifest" for app in PRODUCT_WINDOWS_APPS],
    *[Path(app) / "AndroidManifest.xml" for app in PRODUCT_WINDOWS_APPS],
    *[Path(app) / "Info.plist" for app in PRODUCT_WINDOWS_APPS],
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
FORBIDDEN_CURRENT_DOC_COMMAND_RE = re.compile(
    r"\breact-native\s+run-windows\b|\bW4B\b.*\bactive\b|\bW4C\b.*\bactive\b|"
    r"\blocal build and launch command\b",
    re.IGNORECASE | re.DOTALL,
)
FORBIDDEN_LIVE_SOURCE_RE = re.compile(
    r"\b(fetch\s*\(|new\s+WebSocket|navigator\.bluetooth|navigator\.serial|"
    r"BluetoothDevice|SerialPort|BLEManager|writeFlash)\b",
    re.IGNORECASE,
)
RNW_BRIDGE_SURFACE_SCAN_DIRS = [
    Path("apps/cbbs-windows/src"),
    Path("apps/cbbs-windows/windows"),
    Path("apps/cbbs-client-windows/src"),
    Path("apps/cbbs-client-windows/windows"),
    Path("apps/cbbs-sysop-windows/src"),
    Path("apps/cbbs-sysop-windows/windows"),
    Path("apps/cbbs-hardware-tools-windows/src"),
    Path("apps/cbbs-hardware-tools-windows/windows"),
]
RNW_BRIDGE_SURFACE_SCAN_SUFFIXES = {
    ".c",
    ".cc",
    ".cpp",
    ".cxx",
    ".h",
    ".hpp",
    ".js",
    ".jsx",
    ".mm",
    ".ts",
    ".tsx",
}
RNW_FORBIDDEN_NATIVE_BRIDGE_PATTERNS = [
    ("NativeModules.HostCommandBridge", re.compile(r"NativeModules\s*\.\s*HostCommandBridge")),
    ("HostCommandBridge native symbol", re.compile(r"\bHostCommandBridge\b")),
    ("REACT_MODULE", re.compile(r"\bREACT_MODULE\b")),
    ("REACT_METHOD", re.compile(r"\bREACT_METHOD\b")),
    ("CreateProcess", re.compile(r"\bCreateProcess[AW]?\b")),
    ("ShellExecute", re.compile(r"\bShellExecute(?:Ex)?[AW]?\b")),
    ("CreateFile", re.compile(r"\bCreateFile[AW]?\b")),
    ("WriteFile", re.compile(r"\bWriteFile\b")),
    ("Windows.Devices.SerialCommunication", re.compile(r"\bWindows\.Devices\.SerialCommunication\b")),
    ("System.IO.Ports", re.compile(r"\bSystem\.IO\.Ports\b")),
    ("SerialPort", re.compile(r"\bSerialPort\b")),
    ("child_process", re.compile(r"\bchild_process\b")),
    ("process exec", re.compile(r"\b(?:exec|spawn|execFile)\s*\(")),
    ("navigator.serial", re.compile(r"\bnavigator\.serial\b")),
    ("navigator.bluetooth", re.compile(r"\bnavigator\.bluetooth\b")),
    ("esptool", re.compile(r"\besptool(?:\.py)?\b", re.IGNORECASE)),
    ("idf.py", re.compile(r"\bidf\.py\b", re.IGNORECASE)),
]
SECRET_FIXTURE_RE = re.compile(
    r"\b(token|secret|pmk|lmk|password|privateKey|deviceId|androidId|macAddress|"
    r"messageBody|fileContent|preciseLocation)\b",
    re.IGNORECASE,
)
DOSC_ROOT = Path(os.environ.get("DOSC_ROOT", "/mnt/h/dos-c"))
DOSC_RNW_SOURCE_MARKERS = {
    Path("software/win31-operator/README.md"): [
        "OG Communication Retro3.1",
        "Two-row view selector with plain primary tasks",
        "Operator Protocol",
        "maint_intent",
        "otap_intent",
    ],
    Path("software/win31-operator/include/operator_protocol.h"): [
        "OPCON_REQ_HELLO",
        "OPCON_REQ_MAINT_INTENT",
        "OPCON_REQ_OTAP_INTENT",
    ],
    Path("software/win31-operator/src/operator_protocol.c"): [
        '\\"type\\":\\"state_get\\"',
        '\\"type\\":\\"maint_intent\\"',
        '\\"type\\":\\"otap_intent\\"',
    ],
    Path("docs/architecture/win31-dashboard-vision-gate.md"): [
        "vision gate",
        "OCR",
        "CV",
    ],
}
TRACKED_GENERATED_EVIDENCE_RECORD_FILES = [
    Path(".agents/TASK_LOG/0157-cbbs-react-native-windows-build-launch-integrated.md"),
    Path(".agents/handoffs/0117-cbbs-react-native-windows-build-launch-integrated-to-qa.md"),
    Path("knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-build-launch-integrated.md"),
    Path(".agents/TASK_LOG/0172-workspace-review-follow-up-hardening.md"),
    Path("knowledge-base/source-ledger/2026-06-05-workspace-review-follow-up-hardening.md"),
]
TRACKED_GENERATED_EVIDENCE = {
    Path("research/bench-records/react-native-windows/cbbs-windows-index.bundle"): {
        "bytes": 5_133_785,
        "max_bytes": 6_000_000,
        "sha256": "07c301fedfa809e20f8b3b95a891f6090ea2a39d3be2389f18697e0001bbb9a0",
    },
    Path("research/bench-records/react-native-windows/cbbs-windows-index.map"): {
        "bytes": 10_328_346,
        "max_bytes": 11_000_000,
        "sha256": "f64c8a6f20763a6bcd55c7684f8600717fe7462e63b011b22401eaab999100bb",
    },
    Path("research/bench-records/react-native-windows/live-index.bundle"): {
        "bytes": 5_133_923,
        "max_bytes": 6_000_000,
        "sha256": "fdd80512d04989c0a8f83fc4bd16181a5bcae38acffe0da5d5a944eb72633bc9",
    },
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(_read(path))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def _inspect_dosc_rnw_sources(dosc_root: Path = DOSC_ROOT) -> list[str]:
    failures: list[str] = []
    if not dosc_root.exists():
        return [f"DOS-C source root missing for RNW parity audit: {dosc_root}"]
    for rel, markers in DOSC_RNW_SOURCE_MARKERS.items():
        path = dosc_root / rel
        if not path.exists():
            failures.append(f"DOS-C RNW parity source missing: {rel.as_posix()}")
            continue
        failures.extend(_require_text(path, markers, f"DOS-C RNW parity source {rel.as_posix()}"))
    return failures


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


def _repo_source_ts_files(root: Path, rel: str) -> list[Path]:
    return [
        path
        for path in _repo_ts_files(root, rel)
        if "__tests__" not in path.relative_to(root).parts
    ]


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


def _forbidden_output_group(rel: Path) -> Path | None:
    """Return the shortest generated-output directory represented by rel."""
    parts = rel.parts
    for index, part in enumerate(parts):
        if part in FORBIDDEN_WINDOWS_OUTPUT_DIRS:
            return Path(*parts[: index + 1])
    return None


def summarize_forbidden_output_groups(paths: list[Path]) -> list[tuple[Path, int]]:
    groups: dict[Path, int] = {}
    for rel in paths:
        group = _forbidden_output_group(rel)
        if group is None:
            continue
        groups[group] = groups.get(group, 0) + 1
    return sorted(groups.items(), key=lambda item: item[0].as_posix())


def _inspect_single_windows_native_surface(
    root: Path,
    native_dir_rel: Path,
    expected_files: list[Path],
    record_files: list[Path],
    label: str,
) -> list[str]:
    failures: list[str] = []
    native_dir = root / native_dir_rel
    if not native_dir.exists():
        return failures

    for rel in record_files:
        if not (root / rel).exists():
            failures.append(f"{label} native surface exists without record: {rel.as_posix()}")
    for rel in expected_files:
        if not (native_dir / rel).exists():
            failures.append(f"{label} Windows native surface missing expected file: {rel.as_posix()}")

    forbidden_output_paths: list[Path] = []
    for path in sorted(native_dir.rglob("*")):
        rel = path.relative_to(native_dir)
        if _forbidden_output_group(rel) is not None:
            forbidden_output_paths.append(rel)
        if path.is_file():
            if path.name in FORBIDDEN_WINDOWS_OUTPUT_NAMES:
                failures.append(f"{label} Windows native surface contains store/signing file: {rel.as_posix()}")
            if path.suffix.lower() in FORBIDDEN_WINDOWS_OUTPUT_SUFFIXES:
                failures.append(f"{label} Windows native surface contains package/signing artifact: {rel.as_posix()}")
    for group, count in summarize_forbidden_output_groups(forbidden_output_paths):
        failures.append(
            f"{label} Windows native surface contains generated output group: "
            f"{group.as_posix()} ({count} entries)"
        )

    manifests = sorted(native_dir.rglob("Package.appxmanifest"))
    if len(manifests) != 1:
        failures.append(f"{label} Windows native surface must contain exactly one Package.appxmanifest, found {len(manifests)}")
        return failures

    manifest = manifests[0]
    try:
        capabilities = _manifest_capabilities(manifest)
    except ET.ParseError as exc:
        failures.append(f"{label} Package.appxmanifest is not valid XML: {exc}")
        return failures
    extra_capabilities = capabilities - ALLOWED_WINDOWS_TEMPLATE_CAPABILITIES
    missing_capabilities = ALLOWED_WINDOWS_TEMPLATE_CAPABILITIES - capabilities
    if extra_capabilities:
        failures.append(
            f"{label} Package.appxmanifest has unapproved capabilities: "
            + ", ".join(sorted(extra_capabilities))
        )
    if missing_capabilities:
        failures.append(
            f"{label} Package.appxmanifest missing reviewed template capabilities: "
            + ", ".join(sorted(missing_capabilities))
        )

    manifest_text = _read(manifest)
    for marker in ["Identity", "Publisher=", "TargetDeviceFamily", "internetClient", "runFullTrust"]:
        if marker not in manifest_text:
            failures.append(f"{label} Package.appxmanifest missing marker: {marker}")

    return failures


def _inspect_windows_native_surface(root: Path) -> list[str]:
    failures: list[str] = []
    failures.extend(
        _inspect_single_windows_native_surface(
            root,
            WINDOWS_NATIVE_DIR,
            EXPECTED_WINDOWS_NATIVE_FILES,
            W3B_RECORD_FILES,
            "W3B",
        )
    )
    for native_dir, expected_files in EXPECTED_SPLIT_WINDOWS_NATIVE_FILES.items():
        failures.extend(
            _inspect_single_windows_native_surface(
                root,
                native_dir,
                expected_files,
                SPLIT_NATIVE_RECORD_FILES,
                "split-native",
            )
        )
    return failures


def _iter_rnw_bridge_surface_files(root: Path) -> list[Path]:
    ignored_parts = {"node_modules", "bin", "obj", "Debug", "Release", ".vs"}
    files: list[Path] = []
    for rel in RNW_BRIDGE_SURFACE_SCAN_DIRS:
        base = root / rel
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if (
                path.is_file()
                and path.suffix in RNW_BRIDGE_SURFACE_SCAN_SUFFIXES
                and not ignored_parts.intersection(path.relative_to(base).parts)
                and "__tests__" not in path.relative_to(root).parts
            ):
                files.append(path)
    return files


def _inspect_rnw_native_bridge_surfaces(root: Path = ROOT) -> list[str]:
    failures: list[str] = []
    for path in _iter_rnw_bridge_surface_files(root):
        text = _read(path)
        rel = path.relative_to(root).as_posix()
        for label, pattern in RNW_FORBIDDEN_NATIVE_BRIDGE_PATTERNS:
            if pattern.search(text):
                failures.append(f"RNW native/live surface contains forbidden {label}: {rel}")
    return failures


def _audit_tracked_generated_evidence(root: Path) -> list[str]:
    failures: list[str] = []
    record_text = "\n".join(
        _read(root / rel)
        for rel in TRACKED_GENERATED_EVIDENCE_RECORD_FILES
        if (root / rel).exists()
    )
    lower_record_text = record_text.lower()
    for rel, expected in TRACKED_GENERATED_EVIDENCE.items():
        path = root / rel
        rel_text = rel.as_posix()
        if not path.exists():
            failures.append(f"tracked RNW generated evidence missing: {rel_text}")
            continue
        actual_bytes = path.stat().st_size
        if actual_bytes != expected["bytes"]:
            failures.append(f"tracked RNW generated evidence byte mismatch: {rel_text}")
        if actual_bytes > expected["max_bytes"]:
            failures.append(f"tracked RNW generated evidence exceeds size ceiling: {rel_text}")
        expected_hash = str(expected["sha256"])
        actual_hash = _sha256(path)
        if actual_hash != expected_hash:
            failures.append(f"tracked RNW generated evidence sha256 mismatch: {rel_text}")
        if rel_text not in record_text:
            failures.append(f"tracked RNW generated evidence lacks source-record linkage: {rel_text}")
        if expected_hash not in lower_record_text:
            failures.append(f"tracked RNW generated evidence hash missing from records: {rel_text}")
    for marker in [
        "tracked generated rnw evidence",
        "not a publication artifact",
        "local review evidence",
    ]:
        if marker not in lower_record_text:
            failures.append(f"tracked RNW generated evidence records missing classification marker: {marker}")
    return failures


def audit_react_native(root: Path = ROOT) -> list[str]:
    failures: list[str] = []

    source_index = _read(root / "knowledge-base" / "source-index.md")
    for source_id in REQUIRED_SOURCE_IDS:
        if source_id not in source_index:
            failures.append(f"source index missing {source_id}")
    failures.extend(_inspect_dosc_rnw_sources())

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
        "packages/cbbs-product/src/index.ts",
        "packages/cbbs-product/src/hardwareToolsMenu.generated.ts",
        "packages/cbbs-product/src/win31Parity.generated.ts",
        "packages/cbbs-product-ui/src/index.tsx",
        "packages/cbbs-fixtures/src/index.ts",
        "packages/cbbs-state/src/index.ts",
        "packages/cbbs-ui/src/index.tsx",
        "docs/projects/cbbs-react-native/README.md",
        "research/cbbs-react-native/README.md",
        "tools/react-native/README.md",
        "tools/react-native/cbbs_rnw_menu.v1.xml",
        "tools/react-native/generate_rnw_menu.py",
        "tools/react-native/cbbs_rnw_win31_parity.v1.xml",
        "tools/react-native/generate_win31_parity.py",
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
        ".agents/TASK_LOG/0156-cbbs-react-native-windows-w4-pre-release.md",
        ".agents/handoffs/0116-cbbs-react-native-windows-w4-pre-release-to-qa-release.md",
        "knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-w4-pre-release.md",
        ".agents/TASK_LOG/0161-cbbs-rnw-source-ui-mutation.md",
        ".agents/handoffs/0120-cbbs-rnw-source-ui-mutation-to-qa.md",
        "knowledge-base/source-ledger/2026-06-03-cbbs-rnw-source-ui-mutation.md",
        ".agents/TASK_LOG/0162-cbbs-rnw-split-runtime-proof-and-agents.md",
        ".agents/handoffs/0121-cbbs-rnw-split-runtime-proof-and-agents-to-qa.md",
        "knowledge-base/source-ledger/2026-06-03-cbbs-rnw-split-runtime-proof-and-agents.md",
        ".agents/TASK_LOG/0163-cbbs-rnw-split-native-generation.md",
        ".agents/handoffs/0122-cbbs-rnw-split-native-generation-to-qa.md",
        "knowledge-base/source-ledger/2026-06-04-cbbs-rnw-split-native-generation.md",
        ".agents/TASK_LOG/0164-cbbs-host-command-bridge-live-gate-blocked.md",
        ".agents/handoffs/0123-cbbs-host-command-bridge-live-gate-blocked-to-qa.md",
        "knowledge-base/source-ledger/2026-06-04-cbbs-host-command-bridge-live-gate-blocked.md",
        ".agents/TASK_LOG/0165-cbbs-xbee-known-profile-write-gate-blocked.md",
        ".agents/handoffs/0124-cbbs-xbee-known-profile-write-gate-blocked-to-qa.md",
        "knowledge-base/source-ledger/2026-06-04-cbbs-xbee-known-profile-write-gate-blocked.md",
        ".agents/TASK_LOG/0174-rnw-hardware-tools-host-only-improvements.md",
        "knowledge-base/source-ledger/2026-06-05-rnw-hardware-tools-host-only-improvements.md",
    ]:
        if not (root / rel).exists():
            failures.append(f"missing React Native scaffold file: {rel}")
    for rel in PRODUCT_WINDOWS_APPS:
        for package_rel in ["package.json", "index.js", "src/index.tsx", "tsconfig.json"]:
            if not (root / rel / package_rel).exists():
                failures.append(f"missing React Native product app file: {rel}/{package_rel}")

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
    failures.extend(_inspect_rnw_native_bridge_surfaces(root))
    failures.extend(_audit_tracked_generated_evidence(root))
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

    for rel in RNW_WINDOWS_APP_PACKAGES:
        package_rel = f"{rel}/package.json"
        windows_package = _load_json(root / package_rel)
        windows_deps = _deps(windows_package)
        for name, version in WINDOWS_RNW_DEPENDENCIES.items():
            if windows_deps.get(name) != version:
                failures.append(f"{package_rel} must pin {name} to {version}")
        for forbidden in ["@cbbs/ui", "expo", "expo-router", "react-native-web"]:
            if forbidden in windows_deps:
                failures.append(f"{package_rel} must not depend on {forbidden}")

    product_ui_package = _load_json(root / "packages" / "cbbs-product-ui" / "package.json")
    product_ui_runtime_deps = product_ui_package.get("dependencies")
    if not isinstance(product_ui_runtime_deps, dict):
        failures.append("packages/cbbs-product-ui/package.json must declare dependencies")
        product_ui_runtime_deps = {}
    for forbidden in ["react", "react-native", "react-native-windows", "expo", "expo-router", "react-native-web"]:
        if forbidden in product_ui_runtime_deps:
            failures.append(f"packages/cbbs-product-ui/package.json must keep {forbidden} out of dependencies")
    product_ui_peer_deps = product_ui_package.get("peerDependencies")
    if not isinstance(product_ui_peer_deps, dict):
        failures.append("packages/cbbs-product-ui/package.json must declare React Native peerDependencies")
        product_ui_peer_deps = {}
    if product_ui_peer_deps.get("react") != "19.2.3":
        failures.append("packages/cbbs-product-ui/package.json peerDependencies.react must be 19.2.3")
    if product_ui_peer_deps.get("react-native") != ">=0.83.9 <0.86.0":
        failures.append("packages/cbbs-product-ui/package.json peerDependencies.react-native must cover RNW 0.83 and Expo RN 0.85")

    for path in _package_json_paths(root):
        rel = path.relative_to(root).as_posix()
        deps = _deps(_load_json(path))
        allowed_rnw_package_jsons = {f"{package_path}/package.json" for package_path in RNW_WINDOWS_APP_PACKAGES}
        if rel not in allowed_rnw_package_jsons:
            for name in ["react-native-windows", "@rnx-kit/jest-preset"]:
                if name in deps:
                    failures.append(f"{rel} must not depend on {name}")
        if rel in {"package.json", "apps/cbbs-client/package.json"} or rel.startswith("packages/"):
            if deps.get("react-native") == WINDOWS_RNW_DEPENDENCIES["react-native"]:
                failures.append(f"{rel} must not use the Windows RN {WINDOWS_RNW_DEPENDENCIES['react-native']} lane")

    importers = _lockfile_importers(root)
    for importer_name in RNW_WINDOWS_APP_PACKAGES:
        windows_importer = importers.get(importer_name)
        if not isinstance(windows_importer, dict):
            failures.append(f"pnpm-lock.yaml missing {importer_name} importer")
            continue
        importer_deps: dict[str, str] = {}
        for section in ["dependencies", "devDependencies", "peerDependencies"]:
            values = windows_importer.get(section)
            if isinstance(values, dict):
                for name, meta in values.items():
                    if isinstance(meta, dict) and "specifier" in meta:
                        importer_deps[str(name)] = str(meta["specifier"])
        for name, version in WINDOWS_RNW_DEPENDENCIES.items():
            if importer_deps.get(name) != version:
                failures.append(f"pnpm-lock.yaml {importer_name} importer must pin {name} to {version}")

    product_ui_importer = importers.get("packages/cbbs-product-ui")
    if isinstance(product_ui_importer, dict):
        runtime_deps = product_ui_importer.get("dependencies")
        if isinstance(runtime_deps, dict):
            for forbidden in ["react", "react-native", "react-native-windows", "expo", "expo-router", "react-native-web"]:
                if forbidden in runtime_deps:
                    entry = runtime_deps.get(forbidden)
                    peer_specifier = product_ui_peer_deps.get(forbidden)
                    if (
                        forbidden in {"react", "react-native"}
                        and peer_specifier is not None
                        and isinstance(entry, dict)
                        and entry.get("specifier") == peer_specifier
                    ):
                        continue
                    failures.append(f"pnpm-lock.yaml packages/cbbs-product-ui runtime deps must not include {forbidden}")
    for importer_name, importer in importers.items():
        if importer_name in RNW_WINDOWS_APP_PACKAGES or not isinstance(importer, dict):
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
        "HOST_COMMAND_BRIDGE_SCHEMA",
        "HOST_COMMAND_ACTION_IDS",
        "validateHostCommandBridgeRequest",
        "createUnavailableHostCommandResult",
        "adapter_unavailable",
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

    product_text = "\n".join(
        [
            _read(root / "packages" / "cbbs-product" / "src" / "index.ts"),
            _read(root / "packages" / "cbbs-product" / "src" / "hardwareToolsMenu.generated.ts"),
            _read(root / "packages" / "cbbs-product" / "src" / "win31Parity.generated.ts"),
        ]
    )
    for marker in [
        "CBBS_PRODUCT_WINDOWS_APP_IDS",
        "CBBS Client",
        "CBBS Sysop",
        "CBBS Hardware Tools",
        "CBBS_RNW_MENU_SCHEMA",
        "CBBS_RNW_WIN31_PARITY_SCHEMA",
        "win31ParityContract",
        "OG Communication Retro3.1",
        "PRODUCT_EXECUTION_MODES",
        "hardwareToolsMenu",
        "radio.queryPreview",
        "firmware.installPreview",
        "hardwareToolsFirmwareCatalog",
        "hardwareToolsCommunicationAnalysisRecords",
    ]:
        if marker not in product_text:
            failures.append(f"product contract missing marker: {marker}")
    product_ui_text = _read(root / "packages" / "cbbs-product-ui" / "src" / "index.tsx")
    for marker in [
        "ProductWindowsShell",
        "windows-${appId}-shell",
        "windows-${appId}-action-",
        "windows-${appId}-menubar",
        "windows-${appId}-transcript",
        "deriveProductShellLayout",
        "windows-${appId}-layout-metadata",
        "windows-${appId}-firmware-catalog",
        "windows-${appId}-communications-analysis",
        "Gate phrase records notes but does not unlock closed work.",
        "HOST_COMMAND_UNAVAILABLE_REASON",
    ]:
        if marker not in product_ui_text:
            failures.append(f"product UI missing marker: {marker}")

    app_source = "\n".join(_read(path) for path in _repo_source_ts_files(root, "apps"))
    package_source = "\n".join(_read(path) for path in _repo_source_ts_files(root, "packages"))
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
        "AppRegistry.registerComponent",
        "WINDOWS_APP_COMPONENT_NAME",
        "legacyWindowsMigrationStatus",
        "ProductWindowsShell",
        "CBBS_PRODUCT_WINDOWS_APP_IDS",
        'defaultProductApp: "sysop"',
        "packageIdentityAccepted: false",
        "capabilityUseAccepted: false",
        "liveExecutionAvailable: false",
    ]:
        if marker not in windows_text:
            failures.append(f"Windows product migration shell missing marker: {marker}")
    for app_rel, component_name in {
        "apps/cbbs-client-windows/src/index.tsx": "CbbsClientWindows",
        "apps/cbbs-sysop-windows/src/index.tsx": "CbbsSysopWindows",
        "apps/cbbs-hardware-tools-windows/src/index.tsx": "CbbsHardwareToolsWindows",
    }.items():
        app_text = _read(root / app_rel)
        for marker in ["AppRegistry.registerComponent", component_name, "ProductWindowsShell"]:
            if marker not in app_text:
                failures.append(f"{app_rel} missing split native marker: {marker}")
    windows_readme = _read(root / "apps" / "cbbs-windows" / "README.md")
    for marker in [
        "package-only RNW dependency selection",
        "react-native-windows",
        "0.83.0",
        "react-native` `0.83.9",
        "19.2.3",
        "W3B native generation gate",
        "W4 Pre-Release Planning",
        "Runtime Gate",
        "Mesh And XBee Integration",
        "AppRegistry",
        "generated template facts only",
        "Azure Artifact Signing",
        "Future Tier 3 runtime command stays closed",
        "split native generation",
        "CbbsClientWindows",
        "CbbsSysopWindows",
        "CbbsHardwareToolsWindows",
    ]:
        if marker not in windows_readme:
            failures.append(f"Windows README missing W2 marker: {marker}")
    if "No RNW dependency" in windows_readme:
        failures.append("Windows README must not claim W2 has no RNW dependency")
    if FORBIDDEN_CURRENT_DOC_COMMAND_RE.search(windows_readme):
        failures.append("Windows README must not expose active run-windows/build/launch command surface")
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
        "pnpm --filter @cbbs/client-windows typecheck",
        "pnpm --filter @cbbs/client-windows test:windows",
        "pnpm --filter @cbbs/sysop-windows typecheck",
        "pnpm --filter @cbbs/sysop-windows test:windows",
        "pnpm --filter @cbbs/hardware-tools-windows typecheck",
        "pnpm --filter @cbbs/hardware-tools-windows test:windows",
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
        "../knowledge-base/source-ledger/2026-06-03-cbbs-react-native-windows-w4-pre-release.md",
        "../knowledge-base/source-ledger/2026-06-03-cbbs-rnw-source-ui-mutation.md",
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
        "../.agents/TASK_LOG/0156-cbbs-react-native-windows-w4-pre-release.md",
        "../.agents/handoffs/0116-cbbs-react-native-windows-w4-pre-release-to-qa-release.md",
        "../.agents/TASK_LOG/0161-cbbs-rnw-source-ui-mutation.md",
        "../.agents/handoffs/0120-cbbs-rnw-source-ui-mutation-to-qa.md",
        "../knowledge-base/source-ledger/2026-06-03-cbbs-rnw-source-ui-mutation.md",
        "../.agents/TASK_LOG/0162-cbbs-rnw-split-runtime-proof-and-agents.md",
        "../.agents/handoffs/0121-cbbs-rnw-split-runtime-proof-and-agents-to-qa.md",
        "../knowledge-base/source-ledger/2026-06-03-cbbs-rnw-split-runtime-proof-and-agents.md",
        "../.agents/TASK_LOG/0163-cbbs-rnw-split-native-generation.md",
        "../.agents/handoffs/0122-cbbs-rnw-split-native-generation-to-qa.md",
        "../knowledge-base/source-ledger/2026-06-04-cbbs-rnw-split-native-generation.md",
        "../.agents/TASK_LOG/0164-cbbs-host-command-bridge-live-gate-blocked.md",
        "../.agents/handoffs/0123-cbbs-host-command-bridge-live-gate-blocked-to-qa.md",
        "../knowledge-base/source-ledger/2026-06-04-cbbs-host-command-bridge-live-gate-blocked.md",
        "../.agents/TASK_LOG/0165-cbbs-xbee-known-profile-write-gate-blocked.md",
        "../.agents/handoffs/0124-cbbs-xbee-known-profile-write-gate-blocked-to-qa.md",
        "../knowledge-base/source-ledger/2026-06-04-cbbs-xbee-known-profile-write-gate-blocked.md",
        "../.agents/TASK_LOG/0174-rnw-hardware-tools-host-only-improvements.md",
        "../knowledge-base/source-ledger/2026-06-05-rnw-hardware-tools-host-only-improvements.md",
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
