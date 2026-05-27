#!/usr/bin/env python3
"""Advisory legibility analysis for copied Win31 OPCON dashboard evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}

TARGET_VIEWS = [
    "Home",
    "BBS",
    "Downloads",
    "Network",
    "Peers",
    "OTAP",
    "Settings",
    "Wizard",
    "Diagnostics",
    "Safety",
]

VIEW_RULES: list[tuple[str, tuple[str, ...], tuple[str, ...]]] = [
    ("BBS", ("message-board", "bbs"), ("bbs", "message board")),
    ("Downloads", ("downloads",), ("download", "downloads", "catalog")),
    ("Network", ("network",), ("network",)),
    ("Peers", ("peers",), ("peers", "peer inventory")),
    ("OTAP", ("otap",), ("otap", "update")),
    ("Settings", ("settings", "setup"), ("settings", "setup")),
    ("Wizard", ("wizard", "wiz"), ("wizard", "first run")),
    ("Diagnostics", ("diagnostics", "diag"), ("diagnostics", "diag")),
    ("Safety", ("safety", "safe"), ("safety", "safety gates")),
    (
        "Home",
        ("home", "opcon-dashboard", "final-refresh", "pre-cleanup"),
        ("home", "dashboard", "coordinator telemetry"),
    ),
    ("Navigation", ("views-dropdown",), ("home", "downloads", "network")),
    ("Launch", ("maximized-launch",), ("dashboard", "opcon")),
    ("Devices", ("devices", "dev"), ("devices",)),
]

SOURCE_IDS = [
    "SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23",
    "SRC-LOCAL-WIN31-DASHBOARD-LEGIBILITY-RESEARCH-2026-05-24",
    "SRC-LOCAL-WIN31-DASHBOARD-ADAPTIVE-VISUAL-QUALITY-2026-05-26",
    "SRC-SUNFOUNDER-7INCH-HDMI-1024X600-2026-05-26",
    "SRC-RASPBERRY-PI-CONFIGURATION",
    "SRC-DOSBOX-X-REFERENCE-CONFIG-2026-05-26",
    "SRC-MICROSOFT-WIN32-GEOMETRY-2026-05-26",
    "SRC-OPENCV-TEMPLATE-MATCHING-2026-05-23",
    "SRC-TESSERACT-IMAGE-QUALITY-2026-05-23",
    "SRC-WCAG-CONTRAST-MINIMUM-2026-05-24",
    "SRC-MICROSOFT-WIN32-UI-PRINCIPLES-2026-05-24",
    "SRC-MICROSOFT-MENU-GUIDELINES-2026-05-24",
    "SRC-NNG-HEURISTICS-SUMMARY-2026-05-24",
]

HIGH_RISK_TERMS = {
    "OTAP": ("otap",),
    "gate": ("gate", "gated"),
    "serial-readonly": ("serial-readonly", "serial readonly", "serial-readon"),
    "PCAP": ("pcap", "poap"),
    "mesh state": ("mesh", "root", "parent", "heal"),
}

SAFE_BOTTOM_MARGIN_PX = 16
SAFE_RIGHT_MARGIN_PX = 4
MIN_REGION_GAP_PX = 4
PROOF_TARGET_WIDTH_PX = 1024
PROOF_TARGET_HEIGHT_PX = 600
DESKTOP_GRAY_RGB = (192, 192, 192)
DESKTOP_GRAY_TOLERANCE = 32
DESKTOP_ROW_SHARE = 0.70

EXPECTED_NAV_LABELS = {
    "Home": ("home",),
    "BBS": ("bbs", "bbs board"),
    "Downloads": ("files", "downloads", "download"),
    "Network": ("net", "network"),
    "Peers": ("peers",),
    "Devices": ("dev", "devices"),
    "OTAP": ("otap",),
    "Settings": ("setup", "settings"),
    "Wizard": ("wiz", "wizard"),
    "Diagnostics": ("diag", "diagnostics"),
    "Safety": ("safe", "safety"),
}

LAYOUT_BANDS: tuple[tuple[str, float, float], ...] = (
    ("windowChrome", 0.000, 0.090),
    ("statusStrip", 0.090, 0.145),
    ("navigationTabs", 0.145, 0.215),
    ("viewTitle", 0.215, 0.255),
    ("mainContent", 0.255, 0.550),
    ("actionStrip", 0.550, 0.690),
    ("consoleLog", 0.690, 1.000),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def json_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def text_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"expected JSON object: {path}")
    return value


def load_optional_json(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    resolved = path.resolve()
    if not resolved.exists():
        raise SystemExit(f"JSON file missing: {resolved}")
    return load_json(resolved)


def parse_display_config(path: Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    resolved = path.resolve()
    if not resolved.exists():
        raise SystemExit(f"DOSBox-X config missing: {resolved}")
    values: dict[str, dict[str, str]] = {}
    current_section = ""
    for raw_line in resolved.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1].strip().lower()
            values.setdefault(current_section, {})
            continue
        if "=" not in line or current_section not in {"sdl", "render"}:
            continue
        key, value = line.split("=", 1)
        key = key.strip().lower()
        if key in {
            "fullscreen",
            "fullresolution",
            "windowresolution",
            "output",
            "showmenu",
            "scaler",
        }:
            values.setdefault(current_section, {})[key] = value.strip()
    return {
        "path": str(resolved),
        "sdl": values.get("sdl", {}),
        "render": values.get("render", {}),
        "assumption": "Parsed display-related DOSBox-X keys only; runtime behavior still requires copied screenshot evidence.",
    }


def normalize_text(text: str) -> str:
    text = text.lower()
    return re.sub(r"[^a-z0-9]+", " ", text)


def compact_text(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def parse_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError:
            return None
    return None


def parse_int(value: Any) -> int:
    if isinstance(value, bool):
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str) and value.strip().isdigit():
        return int(value.strip())
    return 0


def infer_view(path: Path, ocr_text: str) -> str:
    stem = normalize_text(path.stem)
    text = normalize_text(ocr_text)
    compacted = compact_text(f"{stem} {text}")
    for view, stem_tokens, text_tokens in VIEW_RULES:
        if any(normalize_text(token) in stem for token in stem_tokens):
            return view
    for view, _stem_tokens, text_tokens in VIEW_RULES:
        if any(compact_text(token) in compacted for token in text_tokens):
            return view
    return "Unclassified"


def title_present(view: str, text: str) -> bool:
    for candidate, _stem_tokens, text_tokens in VIEW_RULES:
        if candidate != view:
            continue
        normalized = normalize_text(text)
        compacted = compact_text(text)
        return any(token in normalized or compact_text(token) in compacted for token in text_tokens)
    return True


def decorative_noise_ratio(text: str) -> dict[str, Any]:
    tokens = re.findall(r"[A-Za-z0-9][A-Za-z0-9_:/.-]{1,}", text)
    if not tokens:
        return {"tokenCount": 0, "noiseTokenCount": 0, "noiseTokenRatio": 0.0}

    noisy = []
    for token in tokens:
        lowered = token.lower()
        compacted = compact_text(lowered)
        if len(compacted) < 8:
            continue
        repeated = bool(re.search(r"([a-z0-9])\1{3,}", compacted))
        low_variety = len(set(compacted)) <= 3
        digit_filler = bool(re.fullmatch(r"[0-9:.]+", lowered)) and len(compacted) >= 12
        if repeated or low_variety or digit_filler:
            noisy.append(token)

    return {
        "tokenCount": len(tokens),
        "noiseTokenCount": len(noisy),
        "noiseTokenRatio": round(len(noisy) / len(tokens), 4),
        "examples": noisy[:6],
    }


def relative_luminance(rgb: Any) -> Any:
    import numpy as np  # type: ignore

    rgb = np.asarray(rgb, dtype=np.float64) / 255.0
    linear = np.where(rgb <= 0.03928, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    return 0.2126 * linear[..., 0] + 0.7152 * linear[..., 1] + 0.0722 * linear[..., 2]


def rect_from_mask(mask: Any, x_offset: int = 0, y_offset: int = 0) -> dict[str, int] | None:
    import numpy as np  # type: ignore

    if not np.any(mask):
        return None
    ys, xs = np.where(mask)
    left = int(xs.min()) + x_offset
    top = int(ys.min()) + y_offset
    right = int(xs.max()) + x_offset
    bottom = int(ys.max()) + y_offset
    return {
        "left": left,
        "top": top,
        "right": right,
        "bottom": bottom,
        "width": int(right - left + 1),
        "height": int(bottom - top + 1),
    }


def rect_margins(rect: dict[str, int] | None, width: int, height: int) -> dict[str, int] | None:
    if rect is None:
        return None
    return {
        "top": int(rect["top"]),
        "left": int(rect["left"]),
        "right": int(width - 1 - rect["right"]),
        "bottom": int(height - 1 - rect["bottom"]),
    }


def normalized_margin_values(margins: dict[str, int] | None, width: int, height: int) -> dict[str, int] | None:
    if margins is None:
        return None
    scale_x = width / PROOF_TARGET_WIDTH_PX if width > 0 else 1.0
    scale_y = height / PROOF_TARGET_HEIGHT_PX if height > 0 else 1.0
    if scale_x <= 0:
        scale_x = 1.0
    if scale_y <= 0:
        scale_y = 1.0
    return {
        "top": int(round(margins["top"] / scale_y)),
        "left": int(round(margins["left"] / scale_x)),
        "right": int(round(margins["right"] / scale_x)),
        "bottom": int(round(margins["bottom"] / scale_y)),
    }


def rects_overlap(first: dict[str, int], second: dict[str, int]) -> bool:
    return not (
        first["right"] < second["left"]
        or second["right"] < first["left"]
        or first["bottom"] < second["top"]
        or second["bottom"] < first["top"]
    )


def vertical_gap(first: dict[str, int], second: dict[str, int]) -> int:
    return max(0, int(second["top"] - first["bottom"] - 1))


def foreground_mask(arr: Any) -> tuple[Any, Any, Any]:
    import cv2  # type: ignore
    import numpy as np  # type: ignore

    height, width = arr.shape[:2]
    border = max(4, min(width, height) // 75)
    desktop_start_y = estimate_desktop_start_y(arr)
    side_bottom = desktop_start_y if desktop_start_y is not None else height
    border_parts = [
        arr[:border].reshape(-1, 3),
        arr[:side_bottom, :border].reshape(-1, 3),
        arr[:side_bottom, -border:].reshape(-1, 3),
    ]
    if desktop_start_y is None:
        border_parts.append(arr[-border:].reshape(-1, 3))
    border_pixels = np.concatenate(border_parts, axis=0)
    quantized_border = (border_pixels // 16).astype(np.int16)
    values, counts = np.unique(quantized_border, axis=0, return_counts=True)
    background = (values[int(counts.argmax())] * 16 + 8).astype(np.int16)
    arr_i = arr.astype(np.int16)
    distance = np.abs(arr_i - background).sum(axis=2)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    background_gray = int(round(float(np.mean(background))))
    foreground = (distance > 35) | (np.abs(gray.astype(np.int16) - background_gray) > 12)
    return gray, background, foreground


def estimate_desktop_start_y(arr: Any) -> int | None:
    import numpy as np  # type: ignore

    height = arr.shape[0]
    target = np.asarray(DESKTOP_GRAY_RGB, dtype=np.int16)
    distance = np.abs(arr.astype(np.int16) - target).max(axis=2)
    grey_rows = np.mean(distance <= DESKTOP_GRAY_TOLERANCE, axis=1) >= DESKTOP_ROW_SHARE
    min_run = max(5, height // 75)
    earliest = int(height * 0.35)
    start = None
    for index, present in enumerate(grey_rows):
        if index < earliest:
            continue
        if present and start is None:
            start = index
        if (not present or index == height - 1) and start is not None:
            end = index - 1 if not present else index
            if end - start + 1 >= min_run:
                return int(start)
            start = None
    return None


def analysis_area_mask(arr: Any, foreground: Any) -> tuple[Any, int | None]:
    import numpy as np  # type: ignore

    height, width = foreground.shape
    desktop_start_y = estimate_desktop_start_y(arr)
    area = np.ones((height, width), dtype=bool)
    if desktop_start_y is not None:
        area[desktop_start_y:, :] = False
    return area, desktop_start_y


def meaningful_client_mask(foreground: Any, analysis_area: Any, chrome_cutoff: int) -> Any:
    meaningful = foreground & analysis_area
    meaningful[:chrome_cutoff, :] = False
    if not meaningful.any():
        return meaningful
    row_ratio = meaningful.mean(axis=1)
    col_ratio = meaningful.mean(axis=0)
    meaningful = meaningful.copy()
    meaningful[row_ratio > 0.70, :] = False
    meaningful[:, col_ratio > 0.75] = False
    return meaningful


def image_metrics(path: Path) -> dict[str, Any]:
    try:
        import cv2  # type: ignore
        import numpy as np  # type: ignore
        from PIL import Image  # type: ignore
    except Exception as exc:  # pragma: no cover - optional dependency guard
        return {"available": False, "error": str(exc)}

    try:
        with Image.open(path) as opened:
            rgb = opened.convert("RGB")
            arr = np.asarray(rgb, dtype=np.uint8)
    except Exception as exc:
        return {"available": False, "error": str(exc)}

    height, width = arr.shape[:2]
    gray, background, foreground = foreground_mask(arr)
    analysis_area, desktop_start_y = analysis_area_mask(arr, foreground)
    analysis_foreground = foreground & analysis_area
    area_pixels = max(1, int(np.sum(analysis_area)))
    foreground_ratio = float(np.sum(analysis_foreground) / area_pixels)

    bbox = rect_from_mask(analysis_foreground)
    if bbox is not None:
        bbox.update(
            {
                "rightMarginPx": int(width - 1 - bbox["right"]),
                "bottomMarginPx": int(height - 1 - bbox["bottom"]),
            }
        )

    edges = cv2.Canny(gray, 50, 150)
    edge_ratio = float(np.sum((edges > 0) & analysis_area) / area_pixels)

    component_count = 0
    if np.any(analysis_foreground):
        _count, _labels, stats, _centroids = cv2.connectedComponentsWithStats(
            analysis_foreground.astype(np.uint8),
            8,
        )
        areas = stats[1:, cv2.CC_STAT_AREA] if len(stats) > 1 else []
        component_count = int(sum(1 for area in areas if int(area) >= 3))

    lum = relative_luminance(arr)
    background_lum = float(relative_luminance(background))
    contrast_ratio = None
    low_contrast_share = None
    if np.any(analysis_foreground):
        fg_lum = lum[analysis_foreground]
        ratios = (np.maximum(fg_lum, background_lum) + 0.05) / (
            np.minimum(fg_lum, background_lum) + 0.05
        )
        contrast_ratio = round(float(np.median(ratios)), 3)
        low_contrast_share = round(float(np.mean(ratios < 4.5)), 4)

    foreground_pixels = (
        arr[analysis_foreground] if np.any(analysis_foreground) else arr[analysis_area]
    )
    quantized = foreground_pixels // 32
    palette_values, palette_counts = np.unique(quantized, axis=0, return_counts=True)
    dominant_ratio = float(palette_counts.max() / palette_counts.sum()) if palette_counts.size else 0.0
    chroma = foreground_pixels.max(axis=1) - foreground_pixels.min(axis=1)

    return {
        "available": True,
        "width": int(width),
        "height": int(height),
        "dominantBackgroundRgb": [int(part) for part in background],
        "desktopStartY": desktop_start_y,
        "foregroundRatio": round(foreground_ratio, 4),
        "edgeRatio": round(edge_ratio, 4),
        "componentCount": component_count,
        "bounds": bbox,
        "contrastRatioMedian": contrast_ratio,
        "lowContrastForegroundShare": low_contrast_share,
        "foregroundColorClusters": int(len(palette_values)),
        "dominantForegroundClusterShare": round(dominant_ratio, 4),
        "highChromaForegroundShare": round(float(np.mean(chroma > 40)), 4)
        if len(chroma)
        else 0.0,
    }


def layout_metrics(path: Path, ocr_text: str) -> dict[str, Any]:
    try:
        import numpy as np  # type: ignore
        from PIL import Image  # type: ignore
    except Exception as exc:  # pragma: no cover - optional dependency guard
        return {"available": False, "error": str(exc)}

    try:
        with Image.open(path) as opened:
            arr = np.asarray(opened.convert("RGB"), dtype=np.uint8)
    except Exception as exc:
        return {"available": False, "error": str(exc)}

    height, width = arr.shape[:2]
    _gray, _background, foreground = foreground_mask(arr)
    analysis_area, desktop_start_y = analysis_area_mask(arr, foreground)
    analysis_foreground = foreground & analysis_area
    frame_bounds = rect_from_mask(analysis_foreground)

    chrome_cutoff = max(1, int(round(height * LAYOUT_BANDS[0][2])))
    client_foreground = meaningful_client_mask(foreground, analysis_area, chrome_cutoff)
    client_bounds = rect_from_mask(client_foreground)
    safe_margins = rect_margins(client_bounds, width, height)
    normalized_safe_margins = normalized_margin_values(safe_margins, width, height)
    app_bottom = desktop_start_y - 1 if desktop_start_y is not None else height - 1
    app_height = max(1, app_bottom + 1)
    app_bounds = {
        "left": 0,
        "top": 0,
        "right": int(width - 1),
        "bottom": int(app_bottom),
        "width": int(width),
        "height": int(app_height),
    }

    regions: dict[str, dict[str, int]] = {}
    for name, start, end in LAYOUT_BANDS:
        top = max(0, min(app_bottom, int(round(app_height * start))))
        bottom = max(top + 1, min(app_bottom + 1, int(round(app_height * end))))
        rect = rect_from_mask(analysis_foreground[top:bottom, :], y_offset=top)
        if rect is not None:
            regions[name] = rect

    overlaps = []
    for first_name, second_name in [
        ("navigationTabs", "viewTitle"),
        ("mainContent", "actionStrip"),
        ("actionStrip", "consoleLog"),
    ]:
        first = regions.get(first_name)
        second = regions.get(second_name)
        if first is not None and second is not None and rects_overlap(first, second):
            overlaps.append(f"{first_name}:{second_name}")

    ordered_regions = [
        regions[name]
        for name, _start, _end in LAYOUT_BANDS
        if name in regions
    ]
    gaps = [
        vertical_gap(first, second)
        for first, second in zip(ordered_regions, ordered_regions[1:])
    ]
    min_vertical_gap = min(gaps) if gaps else None

    normalized_ocr = normalize_text(ocr_text)
    compacted_ocr = compact_text(ocr_text)
    nav_labels = {
        label: any(token in normalized_ocr or compact_text(token) in compacted_ocr for token in tokens)
        for label, tokens in EXPECTED_NAV_LABELS.items()
    }
    missing_nav_labels = [label for label, present in nav_labels.items() if not present]

    fit_risks: list[dict[str, str]] = []
    fit_margins = normalized_safe_margins or safe_margins
    if fit_margins is None:
        add_risk(fit_risks, "console_fit_risk", "high", "Client content bounds could not be detected")
    else:
        bottom_margin = fit_margins["bottom"]
        right_margin = fit_margins["right"]
        if bottom_margin < SAFE_BOTTOM_MARGIN_PX or right_margin < SAFE_RIGHT_MARGIN_PX:
            add_risk(
                fit_risks,
                "console_fit_risk",
                "high",
                (
                    f"Client content leaves normalized bottom margin {bottom_margin}px and "
                    f"normalized right margin {right_margin}px"
                ),
            )

    log_region = regions.get("consoleLog")
    if log_region is not None:
        log_margins = rect_margins(log_region, width, height) or {}
        if int(log_margins.get("bottom", height)) < SAFE_BOTTOM_MARGIN_PX:
            add_risk(
                fit_risks,
                "log_region_overflow",
                "high",
                f"Console log reaches bottom margin {log_margins.get('bottom')}px",
            )

    if overlaps:
        add_risk(
            fit_risks,
            "layout_region_overlap",
            "high",
            "Estimated regions overlap: " + ", ".join(overlaps),
        )
    if overlaps and min_vertical_gap is not None and min_vertical_gap < MIN_REGION_GAP_PX:
        add_risk(
            fit_risks,
            "tight_region_spacing",
            "medium",
            f"Minimum vertical region gap is {min_vertical_gap}px",
        )
    if len(missing_nav_labels) > 2:
        add_risk(
            fit_risks,
            "navigation_label_gap",
            "medium",
            "Navigation OCR missed labels: " + ", ".join(missing_nav_labels[:6]),
        )

    return {
        "available": True,
        "captureSize": {"width": int(width), "height": int(height)},
        "desktopStartY": desktop_start_y,
        "appBounds": app_bounds,
        "frameBounds": frame_bounds,
        "clientBounds": client_bounds,
        "windowFrameBounds": frame_bounds,
        "clientEstimateBounds": client_bounds,
        "contentBounds": client_bounds or frame_bounds,
        "safeMarginsPx": safe_margins,
        "normalizedSafeMarginsPx": normalized_safe_margins,
        "proofTargetSize": {"width": PROOF_TARGET_WIDTH_PX, "height": PROOF_TARGET_HEIGHT_PX},
        "captureScaleToProof": {
            "x": round(width / PROOF_TARGET_WIDTH_PX, 4),
            "y": round(height / PROOF_TARGET_HEIGHT_PX, 4),
        },
        "fitMetricSpace": "normalized-proof" if (width, height) != (PROOF_TARGET_WIDTH_PX, PROOF_TARGET_HEIGHT_PX) else "native-capture",
        "regions": regions,
        "regionBounds": regions,
        "regionOverlaps": overlaps,
        "minVerticalRegionGapPx": min_vertical_gap,
        "navigationLabels": nav_labels,
        "missingNavigationLabels": missing_nav_labels,
        "fitRisks": fit_risks,
        "assumption": "Bounds are estimated from local pixel foreground regions; this is advisory CV evidence.",
    }


def severity_value(severity: str) -> int:
    return {"low": 1, "medium": 2, "high": 3}.get(severity, 0)


def add_risk(risks: list[dict[str, str]], code: str, severity: str, detail: str) -> None:
    risks.append({"code": code, "severity": severity, "detail": detail})


def screen_risks(
    view: str,
    ocr: dict[str, Any],
    visual: dict[str, Any],
    noise: dict[str, Any],
    layout: dict[str, Any] | None = None,
) -> list[dict[str, str]]:
    risks: list[dict[str, str]] = []
    confidence = parse_float(ocr.get("meanConfidence"))
    word_count = parse_int(ocr.get("wordCount"))

    if confidence is None:
        add_risk(risks, "weak_ocr_confidence", "high", "OCR confidence is missing")
    elif confidence < 50:
        add_risk(
            risks,
            "weak_ocr_confidence",
            "high",
            f"OCR confidence {confidence:.2f} is below 50",
        )
    elif confidence < 60:
        add_risk(
            risks,
            "weak_ocr_confidence",
            "medium",
            f"OCR confidence {confidence:.2f} is below 60",
        )

    if word_count < 40:
        add_risk(risks, "low_ocr_word_count", "medium", f"OCR found only {word_count} words")
    elif word_count > 220:
        add_risk(
            risks,
            "excessive_text_density",
            "high",
            f"OCR found {word_count} words on one 1024x600 screen",
        )
    elif word_count > 170:
        add_risk(
            risks,
            "excessive_text_density",
            "medium",
            f"OCR found {word_count} words on one screen",
        )

    if view in TARGET_VIEWS and not title_present(view, str(ocr.get("text", ""))):
        add_risk(risks, "missing_view_title", "medium", f"{view} title was not readable in OCR")

    if not visual.get("available"):
        add_risk(risks, "visual_metrics_unavailable", "high", str(visual.get("error", "unknown error")))
        return risks

    foreground_ratio = parse_float(visual.get("foregroundRatio")) or 0.0
    edge_ratio = parse_float(visual.get("edgeRatio")) or 0.0
    contrast_ratio = parse_float(visual.get("contrastRatioMedian"))
    low_contrast_share = parse_float(visual.get("lowContrastForegroundShare")) or 0.0
    noise_ratio = parse_float(noise.get("noiseTokenRatio")) or 0.0
    color_clusters = parse_int(visual.get("foregroundColorClusters"))
    bounds = visual.get("bounds") if isinstance(visual.get("bounds"), dict) else {}
    bottom_margin = parse_int(bounds.get("bottomMarginPx")) if bounds else 0
    right_margin = parse_int(bounds.get("rightMarginPx")) if bounds else 0
    capture_width = parse_int(visual.get("width"))
    capture_height = parse_int(visual.get("height"))
    if capture_width and capture_height and (
        capture_width != PROOF_TARGET_WIDTH_PX or capture_height != PROOF_TARGET_HEIGHT_PX
    ):
        add_risk(
            risks,
            "proof_capture_size_mismatch",
            "medium",
            (
                f"Screenshot is {capture_width}x{capture_height}; "
                f"target proof size is {PROOF_TARGET_WIDTH_PX}x{PROOF_TARGET_HEIGHT_PX}"
            ),
        )
    if layout and layout.get("available"):
        margins = (
            layout.get("normalizedSafeMarginsPx")
            if isinstance(layout.get("normalizedSafeMarginsPx"), dict)
            else layout.get("safeMarginsPx")
        )
        margins = margins if isinstance(margins, dict) else {}
        if margins:
            bottom_margin = parse_int(margins.get("bottom"))
            right_margin = parse_int(margins.get("right"))

    if foreground_ratio > 0.36:
        add_risk(
            risks,
            "excessive_visual_density",
            "high",
            f"Foreground ratio {foreground_ratio:.3f} is above 0.36",
        )
    elif foreground_ratio > 0.30:
        add_risk(
            risks,
            "excessive_visual_density",
            "medium",
            f"Foreground ratio {foreground_ratio:.3f} is above 0.30",
        )

    if edge_ratio > 0.125:
        add_risk(risks, "edge_noise_load", "high", f"Edge ratio {edge_ratio:.3f} is above 0.125")
    elif edge_ratio > 0.105:
        add_risk(risks, "edge_noise_load", "medium", f"Edge ratio {edge_ratio:.3f} is above 0.105")

    if noise_ratio > 0.14:
        add_risk(
            risks,
            "decorative_ocr_noise",
            "high",
            f"Decorative/noise token ratio {noise_ratio:.3f} is above 0.14",
        )
    elif noise_ratio > 0.07:
        add_risk(
            risks,
            "decorative_ocr_noise",
            "medium",
            f"Decorative/noise token ratio {noise_ratio:.3f} is above 0.07",
        )

    if contrast_ratio is None:
        add_risk(risks, "contrast_risk", "medium", "Contrast ratio could not be estimated")
    elif contrast_ratio < 3.0 or low_contrast_share > 0.50:
        add_risk(
            risks,
            "contrast_risk",
            "high",
            f"Median contrast {contrast_ratio:.2f}, low-contrast share {low_contrast_share:.2f}",
        )
    elif contrast_ratio < 4.5 or low_contrast_share > 0.25:
        add_risk(
            risks,
            "contrast_risk",
            "medium",
            f"Median contrast {contrast_ratio:.2f}, low-contrast share {low_contrast_share:.2f}",
        )

    if color_clusters > 140:
        add_risk(
            risks,
            "color_complexity",
            "medium",
            f"Foreground quantized color clusters {color_clusters} are high for OCR comparison",
        )

    if bottom_margin < 12 or right_margin < 4:
        add_risk(
            risks,
            "overflow_margin_risk",
            "high",
            f"Foreground reaches bottom margin {bottom_margin}px and right margin {right_margin}px",
        )
    elif bottom_margin < 24 or right_margin < 12:
        add_risk(
            risks,
            "overflow_margin_risk",
            "medium",
            f"Bottom margin {bottom_margin}px and right margin {right_margin}px are tight",
        )

    if layout and layout.get("available"):
        for risk in layout.get("fitRisks", []):
            if isinstance(risk, dict):
                add_risk(
                    risks,
                    str(risk.get("code", "layout_fit_risk")),
                    str(risk.get("severity", "medium")),
                    str(risk.get("detail", "Layout fit risk")),
                )
    elif layout:
        add_risk(risks, "layout_metrics_unavailable", "high", str(layout.get("error", "unknown error")))

    return risks


def vision_records_by_name(vision_gate: dict[str, Any]) -> dict[str, dict[str, Any]]:
    records = {}
    for record in vision_gate.get("screenshots", []):
        if not isinstance(record, dict):
            continue
        path = Path(str(record.get("path", "")))
        records[path.name] = record
    return records


def collect_screenshots(evidence_root: Path, screenshot_dir: Path | None) -> list[Path]:
    directory = screenshot_dir or evidence_root / "screenshots"
    if not directory.exists():
        raise SystemExit(f"screenshot directory missing: {directory}")
    paths = sorted(path for path in directory.iterdir() if path.suffix.lower() in IMAGE_SUFFIXES)
    if not paths:
        raise SystemExit(f"no screenshots found in: {directory}")
    return paths


def analyze_screen(path: Path, vision_record: dict[str, Any] | None) -> dict[str, Any]:
    ocr = dict((vision_record or {}).get("ocr", {}))
    if "text" not in ocr:
        ocr["text"] = ""
    if "wordCount" not in ocr:
        ocr["wordCount"] = 0

    view = infer_view(path, str(ocr.get("text", "")))
    visual = image_metrics(path)
    layout = layout_metrics(path, str(ocr.get("text", "")))
    noise = decorative_noise_ratio(str(ocr.get("text", "")))
    risks = screen_risks(view, ocr, visual, noise, layout)
    return {
        "file": path.name,
        "path": str(path),
        "sha256": (vision_record or {}).get("sha256") or sha256_file(path),
        "view": view,
        "ocr": {
            "wordCount": parse_int(ocr.get("wordCount")),
            "meanConfidence": parse_float(ocr.get("meanConfidence")),
        },
        "visual": visual,
        "layout": layout,
        "ocrNoise": noise,
        "risks": risks,
        "riskScore": sum(severity_value(risk["severity"]) for risk in risks),
    }


def summarize_view(view: str, screens: list[dict[str, Any]]) -> dict[str, Any]:
    if not screens:
        return {
            "screenCount": 0,
            "lowestOcrConfidence": None,
            "maxWordCount": 0,
            "maxRiskScore": 0,
            "weakSpots": ["No accepted baseline screenshot mapped to this view."],
        }

    confidences = [
        screen["ocr"]["meanConfidence"]
        for screen in screens
        if screen["ocr"].get("meanConfidence") is not None
    ]
    risk_counts: Counter[str] = Counter()
    for screen in screens:
        for risk in screen["risks"]:
            risk_counts[str(risk["code"])] += 1

    weak_spots: list[str] = []
    if confidences and min(confidences) < 55:
        weak_spots.append(f"OCR confidence floor is {min(confidences):.2f}.")
    if risk_counts.get("contrast_risk"):
        weak_spots.append(f"Contrast risk appears on {risk_counts['contrast_risk']} screen(s).")
    if risk_counts.get("decorative_ocr_noise") or risk_counts.get("edge_noise_load"):
        weak_spots.append("ASCII/decorative edge load competes with readable text.")
    if risk_counts.get("excessive_text_density") or risk_counts.get("excessive_visual_density"):
        weak_spots.append("Text or foreground density is high enough to slow scanning.")
    if risk_counts.get("missing_view_title"):
        weak_spots.append("Visible view title was weak or missing in OCR.")
    if risk_counts.get("overflow_margin_risk"):
        weak_spots.append("Screenshot quiet-zone margins are tight.")
    if risk_counts.get("console_fit_risk") or risk_counts.get("log_region_overflow"):
        weak_spots.append("Estimated client/log regions do not preserve the required safe margin.")
    if risk_counts.get("layout_region_overlap") or risk_counts.get("tight_region_spacing"):
        weak_spots.append("Estimated layout regions overlap or have tight visual spacing.")
    if risk_counts.get("navigation_label_gap"):
        weak_spots.append("Navigation labels were not consistently readable in OCR.")
    if not weak_spots:
        weak_spots.append("No view-specific weak spot beyond global comparison risks.")

    return {
        "screenCount": len(screens),
        "screens": [screen["file"] for screen in screens],
        "lowestOcrConfidence": round(min(confidences), 2) if confidences else None,
        "maxWordCount": max(screen["ocr"]["wordCount"] for screen in screens),
        "maxRiskScore": max(screen["riskScore"] for screen in screens),
        "riskCounts": dict(sorted(risk_counts.items())),
        "weakSpots": weak_spots,
    }


def aggregate_counts(screens: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for screen in screens:
        for risk in screen["risks"]:
            counts[str(risk["code"])] += 1
            counts[f"{risk['severity']}:{risk['code']}"] += 1
    return dict(sorted(counts.items()))


def layout_margin_values(screens: list[dict[str, Any]], side: str) -> list[int]:
    values = []
    for screen in screens:
        layout = screen.get("layout") if isinstance(screen.get("layout"), dict) else {}
        margins = (
            layout.get("normalizedSafeMarginsPx")
            if isinstance(layout.get("normalizedSafeMarginsPx"), dict)
            else layout.get("safeMarginsPx")
        )
        margins = margins if isinstance(margins, dict) else {}
        if margins:
            values.append(parse_int(margins.get(side)))
    return values


def advisory_visual_fit_status(aggregate: dict[str, Any]) -> str:
    risks = aggregate.get("riskCounts") if isinstance(aggregate.get("riskCounts"), dict) else {}
    visual_only = bool(aggregate.get("visualOnly"))
    if visual_only:
        if risks.get("console_fit_risk") or risks.get("log_region_overflow"):
            return "fail"
        if risks.get("proof_capture_size_mismatch"):
            return "needs_manual_review"
        return "visual_only_pass"
    if aggregate.get("visionGateStatus") != "pass":
        return "needs_manual_review"
    if risks.get("console_fit_risk") or risks.get("log_region_overflow"):
        return "fail"
    if risks.get("proof_capture_size_mismatch") or risks.get("navigation_label_gap"):
        return "needs_manual_review"
    return "pass"


def build_backlog(screens: list[dict[str, Any]], view_summary: dict[str, Any]) -> list[dict[str, Any]]:
    counts = Counter(aggregate_counts(screens))
    total = len(screens)
    target_missing = sum(1 for view in TARGET_VIEWS if view_summary[view]["screenCount"] == 0)
    high_risk_term_hits = high_risk_terms(screens)

    candidates = [
        {
            "title": "Make the full Win31 console fit in the capture",
            "score": (
                counts["console_fit_risk"] * 5
                + counts["log_region_overflow"] * 4
                + counts["overflow_margin_risk"] * 3
            ),
            "finding": (
                f"{counts['console_fit_risk']}/{total} screens had estimated client fit risk; "
                f"{counts['log_region_overflow']}/{total} had log-region bottom overflow."
            ),
            "hypothesis": (
                "Shrink the drawn shell and log/footer region so the whole OPCON client stays "
                "inside the 1024x600 proof capture with a visible quiet zone."
            ),
            "measurement": (
                "Track layout.safeMarginsPx, consoleLog region bounds, region overlaps, and "
                "DOS-C vision-gate status on before/after screenshots."
            ),
            "acceptance": (
                "Every target screen keeps layout bottom margin >= 16px, right margin >= 4px, "
                "no console_fit_risk, no log_region_overflow, and the existing DOS-C vision gate passes."
            ),
            "sourceIds": [
                "SRC-LOCAL-WIN31-DASHBOARD-LEGIBILITY-RESEARCH-2026-05-24",
                "SRC-OPENCV-TEMPLATE-MATCHING-2026-05-23",
            ],
        },
        {
            "title": "Reduce ASCII border and decoration density",
            "score": counts["decorative_ocr_noise"] * 4 + counts["edge_noise_load"] * 3,
            "finding": (
                f"{counts['decorative_ocr_noise']}/{total} screens produced decorative OCR "
                f"noise and {counts['edge_noise_load']}/{total} exceeded edge-load thresholds."
            ),
            "hypothesis": (
                "Keep the retro ANSI style but reserve repeated glyph borders for section "
                "boundaries so OCR and human scanning see fewer false words."
            ),
            "measurement": (
                "Compare edgeRatio, decorativeNoiseTokenRatio, Tesseract meanConfidence, "
                "and required view detection before and after a layout revision."
            ),
            "acceptance": (
                "Every target view stays gate-passable, decorativeNoiseTokenRatio is below "
                "0.07 on target screens, and no target screen has edgeRatio above 0.105."
            ),
            "sourceIds": [
                "SRC-OPENCV-TEMPLATE-MATCHING-2026-05-23",
                "SRC-TESSERACT-IMAGE-QUALITY-2026-05-23",
            ],
        },
        {
            "title": "Raise contrast floor for operational text",
            "score": counts["contrast_risk"] * 4 + counts["weak_ocr_confidence"] * 3,
            "finding": (
                f"{counts['contrast_risk']}/{total} screens had estimated contrast risk; "
                f"{counts['weak_ocr_confidence']}/{total} had OCR confidence below 60."
            ),
            "hypothesis": (
                "Use fewer dim foreground colors for body text and reserve low-contrast "
                "cyan/amber treatments for decoration or inactive hints."
            ),
            "measurement": (
                "Track median foreground/background contrast ratio, lowContrastForegroundShare, "
                "and OCR confidence by view."
            ),
            "acceptance": (
                "Target views reach median contrast ratio >= 4.5, lowContrastForegroundShare "
                "<= 0.25, and mean OCR confidence >= 60 without weakening the existing gate."
            ),
            "sourceIds": [
                "SRC-WCAG-CONTRAST-MINIMUM-2026-05-24",
                "SRC-TESSERACT-IMAGE-QUALITY-2026-05-23",
            ],
        },
        {
            "title": "Preserve screenshot quiet zones",
            "score": counts["overflow_margin_risk"] * 3 + counts["excessive_visual_density"] * 2,
            "finding": (
                f"{counts['overflow_margin_risk']}/{total} screens had tight bottom or right "
                "quiet-zone margins."
            ),
            "hypothesis": (
                "Give the status/action strip a fixed quiet zone and move transient log lines "
                "away from the bottom edge."
            ),
            "measurement": (
                "Measure bottomMarginPx, rightMarginPx, foregroundRatio, and OCR word count "
                "on every captured view."
            ),
            "acceptance": (
                "Target screens keep bottomMarginPx >= 16 and rightMarginPx >= 4 while "
                "preserving the accepted transcript-first proof path."
            ),
            "sourceIds": [
                "SRC-MICROSOFT-WIN32-UI-PRINCIPLES-2026-05-24",
                "SRC-TESSERACT-IMAGE-QUALITY-2026-05-23",
            ],
        },
        {
            "title": "Make view hierarchy obvious at a glance",
            "score": (
                counts["excessive_text_density"] * 3
                + counts["missing_view_title"] * 3
                + counts["layout_region_overlap"] * 3
                + counts["tight_region_spacing"] * 2
            ),
            "finding": (
                f"{counts['excessive_text_density']}/{total} screens were text-dense and "
                f"{counts['missing_view_title']}/{total} target screens had weak title OCR; "
                f"{counts['tight_region_spacing']}/{total} had tight estimated region spacing."
            ),
            "hypothesis": (
                "Separate current view, system health, safe actions, and primary task into "
                "predictable regions with stronger headings."
            ),
            "measurement": (
                "Use template matching for heading/control regions, OCR title detection, "
                "word count per region, and screenshot bounds checks."
            ),
            "acceptance": (
                "Each target view exposes one readable view title, one health summary, one "
                "primary task region, and one safety/action region in local CV templates."
            ),
            "sourceIds": [
                "SRC-MICROSOFT-WIN32-UI-PRINCIPLES-2026-05-24",
                "SRC-NNG-HEURISTICS-SUMMARY-2026-05-24",
                "SRC-OPENCV-TEMPLATE-MATCHING-2026-05-23",
            ],
        },
        {
            "title": "Use the same plain task names in menus, tabs, cards, and buttons",
            "score": 12 + target_missing + counts["navigation_label_gap"] * 2,
            "finding": (
                "The baseline includes abbreviated tab/menu labels while view titles and "
                "tasks use longer names such as Message Board, Downloads, Diagnostics, and Safety."
            ),
            "hypothesis": (
                "Recognition improves when the menu, tab, card title, and action label all "
                "use the same task name."
            ),
            "measurement": (
                "OCR each navigation area and compare normalized menu/tab labels against "
                "expected task names for every target view."
            ),
            "acceptance": (
                "The analyzer detects the same plain label for Home, BBS, Downloads, Network, "
                "Peers, OTAP, Settings, Wizard, Diagnostics, and Safety in both navigation "
                "and page title regions."
            ),
            "sourceIds": [
                "SRC-MICROSOFT-MENU-GUIDELINES-2026-05-24",
                "SRC-NNG-HEURISTICS-SUMMARY-2026-05-24",
            ],
        },
        {
            "title": "Add novice wording for high-risk concepts",
            "score": 10 + len(high_risk_term_hits) * 2,
            "finding": (
                "High-risk terms observed in OCR include "
                + ", ".join(high_risk_term_hits or ["none"])
                + "."
            ),
            "hypothesis": (
                "Plain-language helper text should translate OTAP, gate, serial-readonly, "
                "PCAP, and mesh state into user-visible operational meaning."
            ),
            "measurement": (
                "Check OCR for approved phrase pairs such as OTAP -> update request only "
                "and serial-readonly -> hardware writes disabled."
            ),
            "acceptance": (
                "Each high-risk concept has a readable plain-language phrase on the relevant "
                "target view and the footer uses those phrases consistently."
            ),
            "sourceIds": [
                "SRC-MICROSOFT-WIN32-UI-PRINCIPLES-2026-05-24",
                "SRC-NNG-HEURISTICS-SUMMARY-2026-05-24",
            ],
        },
        {
            "title": "Explain disabled controls where they appear",
            "score": 10 + counts["missing_view_title"],
            "finding": (
                "The baseline footer repeats disabled/gated control names; the Safety view "
                "has the clearest explanation but the footer remains terse."
            ),
            "hypothesis": (
                "Disabled Relay, Flash, Serial, and PCAP controls should state why they are "
                "disabled and which external path owns the action."
            ),
            "measurement": (
                "OCR footer/control regions for disabled control name, reason phrase, and "
                "owner path phrase."
            ),
            "acceptance": (
                "Each disabled control exposes a readable reason and owner path while live "
                "hardware mutation remains outside this advisory analyzer."
            ),
            "sourceIds": [
                "SRC-MICROSOFT-WIN32-UI-PRINCIPLES-2026-05-24",
                "SRC-NNG-HEURISTICS-SUMMARY-2026-05-24",
            ],
        },
        {
            "title": "Keep a local revision comparison harness",
            "score": 8,
            "finding": (
                "The current pass/fail gate is transcript-first; this analyzer adds advisory "
                "metrics that can compare later UI revisions without changing acceptance."
            ),
            "hypothesis": (
                "A stable local JSON/Markdown report lets design revisions improve legibility "
                "while preserving the existing completion gate."
            ),
            "measurement": (
                "Run this analyzer on each copied packet and diff screen metrics, view summaries, "
                "and ranked backlog scores."
            ),
            "acceptance": (
                "A later UI-change task includes before/after analyzer JSON, the existing DOS-C "
                "vision gate result, ESP32 completion gate result, and no live bench mutation "
                "outside the approved lane."
            ),
            "sourceIds": [
                "SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23",
                "SRC-LOCAL-WIN31-DASHBOARD-LEGIBILITY-RESEARCH-2026-05-24",
            ],
        },
    ]

    ranked = sorted(candidates, key=lambda item: (-int(item["score"]), str(item["title"])))
    for index, item in enumerate(ranked, start=1):
        item["rank"] = index
    return ranked


def high_risk_terms(screens: list[dict[str, Any]]) -> list[str]:
    text = normalize_text(
        "\n".join(str(screen.get("ocrText", "")) for screen in screens)
        + "\n"
        + "\n".join(screen["file"] for screen in screens)
    )
    hits = []
    for label, tokens in HIGH_RISK_TERMS.items():
        if any(token in text for token in tokens):
            hits.append(label)
    return hits


def build_analysis(
    evidence_root: Path,
    screenshot_paths: list[Path],
    vision_gate: dict[str, Any],
    analysis_date: str,
    display_probe: dict[str, Any] | None = None,
    dosbox_display_config: dict[str, Any] | None = None,
    visual_only: bool = False,
) -> dict[str, Any]:
    records_by_name = vision_records_by_name(vision_gate)
    screens = [
        analyze_screen(path, records_by_name.get(path.name))
        for path in sorted(screenshot_paths)
    ]
    for screen in screens:
        record = records_by_name.get(screen["file"]) or {}
        ocr = record.get("ocr", {}) if isinstance(record.get("ocr"), dict) else {}
        screen["ocrText"] = str(ocr.get("text", ""))

    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for screen in screens:
        grouped[screen["view"]].append(screen)

    view_summary = {
        view: summarize_view(view, grouped.get(view, []))
        for view in TARGET_VIEWS
    }
    extra_views = {
        view: summarize_view(view, grouped[view])
        for view in sorted(grouped)
        if view not in TARGET_VIEWS
    }

    ocr_confidences = [
        screen["ocr"]["meanConfidence"]
        for screen in screens
        if screen["ocr"].get("meanConfidence") is not None
    ]
    bottom_margins = layout_margin_values(screens, "bottom")
    right_margins = layout_margin_values(screens, "right")
    capture_sizes = sorted(
        {
            (
                parse_int(screen.get("visual", {}).get("width")),
                parse_int(screen.get("visual", {}).get("height")),
            )
            for screen in screens
            if isinstance(screen.get("visual"), dict)
            and screen.get("visual", {}).get("available")
        }
    )
    aggregate = {
        "screenCount": len(screens),
        "targetViewCount": len(TARGET_VIEWS),
        "mappedTargetViewCount": sum(1 for view in TARGET_VIEWS if view_summary[view]["screenCount"]),
        "captureSizes": [
            {"width": width, "height": height}
            for width, height in capture_sizes
            if width > 0 and height > 0
        ],
        "totalOcrWords": sum(screen["ocr"]["wordCount"] for screen in screens),
        "lowestOcrConfidence": round(min(ocr_confidences), 2) if ocr_confidences else None,
        "medianOcrConfidence": round(sorted(ocr_confidences)[len(ocr_confidences) // 2], 2)
        if ocr_confidences
        else None,
        "riskCounts": aggregate_counts(screens),
        "lowestLayoutBottomMarginPx": min(bottom_margins) if bottom_margins else None,
        "lowestLayoutRightMarginPx": min(right_margins) if right_margins else None,
        "visionGateStatus": vision_gate.get("status"),
        "visionGateOk": bool(vision_gate.get("ok")),
        "visionGateFailures": vision_gate.get("failures", []),
        "visualOnly": visual_only,
    }
    aggregate["advisoryVisualFitStatus"] = advisory_visual_fit_status(aggregate)
    coordinate_stack = {
        "displayProbe": display_probe,
        "dosboxDisplayConfig": dosbox_display_config,
        "captureSizes": aggregate["captureSizes"],
        "win31WindowMetrics": {
            "screenFields": [
                "layout.windowFrameBounds",
                "layout.clientEstimateBounds",
                "layout.contentBounds",
                "layout.safeMarginsPx",
            ],
            "source": "copied screenshot foreground analysis",
        },
        "acceptanceMarginsPx": {
            "bottom": SAFE_BOTTOM_MARGIN_PX,
            "right": SAFE_RIGHT_MARGIN_PX,
        },
        "assumption": (
            "Display and DOSBox-X config records explain the coordinate stack; "
            "screenshots remain the proof for actual rendered fit."
        ),
    }
    ranked_backlog = build_backlog(screens, view_summary)
    for screen in screens:
        screen.pop("ocrText", None)
    revised_packet = "visual-fit" in str(evidence_root).lower()
    verified_facts = [
        "The input packet is copied local evidence; no live bench mutation is performed.",
        "The existing DOS-C vision gate remains the pass/fail screenshot gate.",
        "This analyzer reports advisory legibility and layout-fit metrics for backlog ranking only.",
    ]
    unknowns = [
        "No user study, PaddleOCR benchmark, or hosted vision critique is approved by this task.",
    ]
    if revised_packet:
        verified_facts.append("This run measures a revised visual-fit screenshot packet.")
    else:
        unknowns.insert(0, "No revised UI screenshot packet has been measured by this task.")
    if visual_only:
        verified_facts.append(
            "Visual-only mode was selected; cleanup proof and DOS-C vision-gate JSON are not required for this advisory run."
        )
        unknowns.append(
            "Without DOS-C vision-gate JSON, OCR confidence and transcript-first acceptance remain unverified by this analyzer."
        )

    return {
        "tool": "scripts/win31_dashboard_legibility_analyzer.py",
        "analysisDate": analysis_date,
        "advisoryOnly": True,
        "visualOnly": visual_only,
        "evidenceRoot": str(evidence_root),
        "sources": SOURCE_IDS,
        "verifiedFacts": verified_facts,
        "assumptions": [
            "Tesseract OCR confidence and word count are useful legibility proxies, not human usability proof.",
            "Pixel-level contrast and density heuristics should be compared across revisions, not used alone for acceptance.",
            "Estimated Win31 client regions are derived from local foreground pixels and must be compared against live screenshots.",
        ],
        "unknowns": unknowns,
        "coordinateStack": coordinate_stack,
        "aggregate": aggregate,
        "screens": screens,
        "viewSummary": view_summary,
        "extraViews": extra_views,
        "rankedBacklog": ranked_backlog,
    }


def analyze_evidence(
    evidence_root: Path,
    vision_gate_path: Path | None,
    screenshot_dir: Path | None,
    analysis_date: str,
    display_probe_path: Path | None = None,
    dosbox_config_path: Path | None = None,
    visual_only: bool = False,
) -> dict[str, Any]:
    root = evidence_root.resolve()
    if not root.exists():
        raise SystemExit(f"evidence root missing: {root}")
    vision_path = (vision_gate_path or root / "vision-gate.json").resolve()
    if not vision_path.exists() and not visual_only:
        raise SystemExit(f"vision gate JSON missing: {vision_path}")
    screenshots = collect_screenshots(root, screenshot_dir.resolve() if screenshot_dir else None)
    if vision_path.exists():
        vision_gate = load_json(vision_path)
    else:
        vision_gate = {
            "ok": False,
            "status": "visual_only",
            "failures": ["vision_gate_not_supplied"],
            "screenshots": [],
        }
    return build_analysis(
        root,
        screenshots,
        vision_gate,
        analysis_date,
        load_optional_json(display_probe_path),
        parse_display_config(dosbox_config_path),
        visual_only,
    )


def format_percent(value: Any) -> str:
    parsed = parse_float(value)
    if parsed is None:
        return "n/a"
    return f"{parsed * 100:.1f}%"


def format_number(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def risk_codes(screen: dict[str, Any]) -> str:
    if not screen["risks"]:
        return "none"
    return ", ".join(str(risk["code"]) for risk in screen["risks"][:4])


def layout_margin_text(screen: dict[str, Any]) -> str:
    layout = screen.get("layout") if isinstance(screen.get("layout"), dict) else {}
    margins = (
        layout.get("normalizedSafeMarginsPx")
        if isinstance(layout.get("normalizedSafeMarginsPx"), dict)
        else layout.get("safeMarginsPx")
    )
    margins = margins if isinstance(margins, dict) else {}
    if margins:
        return f"{margins.get('bottom', 'n/a')}/{margins.get('right', 'n/a')}"
    visual = screen["visual"]
    bounds = visual.get("bounds") if isinstance(visual.get("bounds"), dict) else {}
    if bounds:
        return f"{bounds.get('bottomMarginPx', 'n/a')}/{bounds.get('rightMarginPx', 'n/a')}"
    return "n/a"


def layout_risk_codes(screen: dict[str, Any]) -> str:
    layout = screen.get("layout") if isinstance(screen.get("layout"), dict) else {}
    risks = layout.get("fitRisks") if isinstance(layout.get("fitRisks"), list) else []
    codes = [str(risk.get("code")) for risk in risks if isinstance(risk, dict)]
    return ", ".join(codes[:3]) if codes else "none"


def render_report(analysis: dict[str, Any]) -> str:
    aggregate = analysis["aggregate"]
    lines = [
        "# Win31 Dashboard Local ML/CV Legibility Research Backlog",
        "",
        f"Analysis date: {analysis['analysisDate']}",
        "",
        "Source index: [../../../knowledge-base/source-index.md](../../../knowledge-base/source-index.md)",
        "",
        "## Scope",
        "",
        "This is a local-only, advisory research backlog for Win31 OPCON dashboard",
        "visual legibility. It reads copied screenshots plus `vision-gate.json`",
        "when available; `--visual-only` allows screenshot/layout checks while a",
        "live dashboard is intentionally left open. It does not change firmware,",
        "bridge wire protocol, live hardware behavior, or completion acceptance.",
        "",
        "The pass/fail path remains transcript-first: DOS-C `win31_dashboard_vision_gate.py`",
        "and ESP32 `scripts/espnow_bbs_live_gate.py complete` own acceptance. This",
        "document ranks UI hypotheses and before/after acceptance evidence only.",
        "",
        "## Sources",
        "",
    ]
    lines.extend(f"- `{source_id}`" for source_id in analysis["sources"])
    lines.extend(
        [
            "",
            "## Verified Facts",
            "",
        ]
    )
    lines.extend(f"- {fact}" for fact in analysis["verifiedFacts"])
    lines.extend(
        [
            f"- Evidence root: `{analysis['evidenceRoot']}`.",
            f"- Accepted DOS-C vision gate status: `{aggregate['visionGateStatus']}`; failures: `{aggregate['visionGateFailures']}`.",
            f"- Advisory visual-fit status: `{aggregate['advisoryVisualFitStatus']}`.",
            f"- Screenshots analyzed: {aggregate['screenCount']}; target views mapped: {aggregate['mappedTargetViewCount']}/{aggregate['targetViewCount']}.",
            f"- Capture sizes: `{aggregate['captureSizes']}`.",
            f"- Total OCR words: {aggregate['totalOcrWords']}; lowest OCR confidence: {format_number(aggregate['lowestOcrConfidence'])}; median OCR confidence: {format_number(aggregate['medianOcrConfidence'])}.",
            f"- Lowest estimated layout safe margin: bottom {format_number(aggregate['lowestLayoutBottomMarginPx'])} px; right {format_number(aggregate['lowestLayoutRightMarginPx'])} px.",
            "",
            "## Coordinate Stack",
            "",
            f"- Proof target size: `{PROOF_TARGET_WIDTH_PX}x{PROOF_TARGET_HEIGHT_PX}`.",
            f"- Display probe supplied: `{analysis['coordinateStack']['displayProbe'] is not None}`.",
            f"- DOSBox-X display config supplied: `{analysis['coordinateStack']['dosboxDisplayConfig'] is not None}`.",
            "- Per-screen layout fields include `captureSize`, `windowFrameBounds`, `clientEstimateBounds`, `contentBounds`, `normalizedSafeMarginsPx`, and `captureScaleToProof`.",
            "",
            "## Assumptions",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in analysis["assumptions"])
    lines.extend(["", "## Unknowns", ""])
    lines.extend(f"- {item}" for item in analysis["unknowns"])

    lines.extend(
        [
            "",
            "## Per-Screen Metrics",
            "",
            "| Screen | View | OCR words | OCR conf | Foreground | Edge | Contrast | Layout bottom/right | Layout fit risks | Risk score | Top risks |",
            "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: | --- |",
        ]
    )
    for screen in analysis["screens"]:
        visual = screen["visual"]
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{screen['file']}`",
                    screen["view"],
                    str(screen["ocr"]["wordCount"]),
                    format_number(screen["ocr"].get("meanConfidence")),
                    format_percent(visual.get("foregroundRatio")),
                    format_percent(visual.get("edgeRatio")),
                    format_number(visual.get("contrastRatioMedian")),
                    layout_margin_text(screen),
                    layout_risk_codes(screen),
                    str(screen["riskScore"]),
                    risk_codes(screen),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## View Weak Spots",
            "",
            "| View | Screens | Lowest OCR conf | Max words | Weak spots |",
            "| --- | ---: | ---: | ---: | --- |",
        ]
    )
    for view in TARGET_VIEWS:
        summary = analysis["viewSummary"][view]
        lines.append(
            "| "
            + " | ".join(
                [
                    view,
                    str(summary["screenCount"]),
                    format_number(summary["lowestOcrConfidence"]),
                    str(summary["maxWordCount"]),
                    " ".join(summary["weakSpots"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Ranked Backlog",
            "",
            "| Rank | Hypothesis | Grounded finding | Local measurement | Implement-later acceptance criteria |",
            "| ---: | --- | --- | --- | --- |",
        ]
    )
    for item in analysis["rankedBacklog"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(item["rank"]),
                    item["hypothesis"],
                    item["finding"],
                    item["measurement"],
                    item["acceptance"],
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Measurement Notes",
            "",
            "- `foregroundRatio`, `edgeRatio`, color clusters, contrast estimates, and bounds come from local image pixels.",
            "- `layout.safeMarginsPx`, `layout.regions`, and layout fit risks come from local foreground-region estimates.",
            "- OCR word counts, OCR text, and mean confidence come from the copied `vision-gate.json` records.",
            "- OpenCV foreground/component analysis is used here for stable title, footer, disabled-control, primary-action, and console-log region checks.",
            "- A later revision must show before/after analyzer JSON plus unchanged DOS-C vision-gate and ESP32 completion-gate behavior before claiming improvement.",
        ]
    )

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-root", type=Path, required=True)
    parser.add_argument("--vision-gate", type=Path)
    parser.add_argument("--screenshot-dir", type=Path)
    parser.add_argument("--display-probe", type=Path)
    parser.add_argument("--dosbox-config", type=Path)
    parser.add_argument(
        "--visual-only",
        action="store_true",
        help="Analyze screenshots without requiring DOS-C vision-gate JSON or cleanup proof.",
    )
    parser.add_argument("--analysis-date", default="2026-05-24")
    parser.add_argument("--out-json", type=Path)
    parser.add_argument("--out-report", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    analysis = analyze_evidence(
        args.evidence_root,
        args.vision_gate,
        args.screenshot_dir,
        args.analysis_date,
        args.display_probe,
        args.dosbox_config,
        args.visual_only,
    )
    if args.out_json:
        json_write(args.out_json.resolve(), analysis)
    if args.out_report:
        text_write(args.out_report.resolve(), render_report(analysis))
    print(json.dumps(analysis, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
