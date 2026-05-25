#!/usr/bin/env python3
"""Fixture tests for the advisory Win31 dashboard legibility analyzer."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "win31_dashboard_legibility_analyzer",
    ROOT / "scripts" / "win31_dashboard_legibility_analyzer.py",
)
assert SPEC is not None and SPEC.loader is not None
analyzer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analyzer)


def font(size: int = 18) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def write_screen(
    path: Path,
    lines: list[str],
    *,
    background: tuple[int, int, int] = (0, 0, 0),
    foreground: tuple[int, int, int] = (230, 230, 230),
    size: tuple[int, int] = (640, 360),
    start_y: int = 18,
    step: int = 30,
) -> None:
    image = Image.new("RGB", size, background)
    draw = ImageDraw.Draw(image)
    line_font = font()
    y = start_y
    for line in lines:
        draw.text((18, y), line, fill=foreground, font=line_font)
        y += step
    image.save(path)


def write_cropped_screen(path: Path) -> None:
    image = Image.new("RGB", (420, 260), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    line_font = font()
    draw.text((18, 18), "SAFETY control disabled", fill=(240, 240, 240), font=line_font)
    draw.text((250, 238), "PCAP blocked", fill=(240, 240, 240), font=line_font)
    image.save(path)


def write_win31_layout_screen(path: Path, *, clipped: bool) -> None:
    image = Image.new("RGB", (640, 360), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    line_font = font(14)
    draw.rectangle((0, 0, 639, 14), fill=(0, 0, 170))
    draw.text((220, 0), "RETRO-CBBS-NOW Dashboard", fill=(255, 255, 255), font=line_font)
    draw.rectangle((0, 15, 639, 29), fill=(255, 255, 255))
    draw.text((8, 15), "Session Views BBS Transfers Devices Help", fill=(0, 0, 0), font=line_font)
    draw.text((8, 42), "ok COM1 f=0031 RX bytes 1875 TX bytes 147 Queue: 4", fill=(0, 255, 255), font=line_font)
    draw.text((8, 64), "HOME BBS FILES NET PEERS DEV OTAP SETUP WIZ DIAG SAFE", fill=(0, 255, 255), font=line_font)
    draw.rectangle((8, 88, 252, 205), outline=(0, 170, 170))
    draw.rectangle((260, 88, 610, 205), outline=(0, 170, 170))
    draw.text((20, 98), "HOME CARD 1/3", fill=(0, 255, 255), font=line_font)
    draw.text((272, 98), "Coordinator Telemetry", fill=(0, 255, 255), font=line_font)
    draw.text((8, 225), "sysop note   PULL POST FIND ACK CAT QFILE OTAP", fill=(0, 255, 255), font=line_font)
    draw.text((8, 250), "Relay disabled Flash gated Serial disabled PCAP blocked", fill=(220, 220, 220), font=line_font)
    log_bottom = 359 if clipped else 320
    draw.rectangle((8, 278, 631, log_bottom), outline=(0, 170, 170))
    draw.text((12, 282), "rx hello", fill=(0, 255, 255), font=line_font)
    image.save(path)


def vision_record(path: Path, text: str, confidence: float, words: int) -> dict[str, object]:
    return {
        "path": str(path),
        "sha256": analyzer.sha256_file(path),
        "ocr": {
            "text": text,
            "wordCount": words,
            "meanConfidence": confidence,
        },
    }


def analyze(root: Path, records: list[dict[str, object]]) -> dict[str, object]:
    paths = [Path(str(record["path"])) for record in records]
    return analyzer.build_analysis(
        root,
        paths,
        {"ok": True, "status": "pass", "failures": [], "screenshots": records},
        "fixture",
    )


def only_screen(result: dict[str, object]) -> dict[str, object]:
    screens = result["screens"]
    assert isinstance(screens, list)
    return screens[0]


def risk_codes(screen: dict[str, object]) -> set[str]:
    return {str(risk["code"]) for risk in screen["risks"]}  # type: ignore[index]


class Win31DashboardLegibilityAnalyzerTests(unittest.TestCase):
    def test_low_contrast_is_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "03-home-dashboard.png"
            write_screen(
                path,
                ["HOME", "status ok", "serial physical"],
                background=(80, 80, 80),
                foreground=(94, 94, 94),
            )
            result = analyze(root, [vision_record(path, "HOME status ok serial physical", 88.0, 64)])
        self.assertIn("contrast_risk", risk_codes(only_screen(result)))

    def test_excessive_density_and_decorative_noise_are_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "04-message-board.png"
            lines = [f"BBS BOARD SEEEEEEEEEEEEE {index:02d}" for index in range(24)]
            write_screen(path, lines, size=(720, 520), step=20)
            ocr_text = " ".join(lines) + " " + " ".join(["EEEEEEEEEEEE"] * 40)
            result = analyze(root, [vision_record(path, ocr_text, 58.0, 260)])
        codes = risk_codes(only_screen(result))
        self.assertIn("excessive_text_density", codes)
        self.assertIn("decorative_ocr_noise", codes)

    def test_missing_view_title_is_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "03-home-dashboard.png"
            write_screen(path, ["status ok", "serial physical", "peers 3"])
            result = analyze(root, [vision_record(path, "status ok serial physical peers 3", 84.0, 90)])
        self.assertIn("missing_view_title", risk_codes(only_screen(result)))

    def test_cropped_console_margin_is_flagged(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "13-safety.png"
            write_cropped_screen(path)
            result = analyze(root, [vision_record(path, "SAFETY control disabled PCAP blocked", 82.0, 70)])
        self.assertIn("overflow_margin_risk", risk_codes(only_screen(result)))

    def test_layout_fit_metrics_flag_log_overflow(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "03-home-dashboard.png"
            write_win31_layout_screen(path, clipped=True)
            text = (
                "HOME BBS FILES NET PEERS DEV OTAP SETUP WIZ DIAG SAFE "
                "HOME CARD Coordinator Telemetry Relay disabled PCAP blocked"
            )
            result = analyze(root, [vision_record(path, text, 82.0, 96)])
        screen = only_screen(result)
        layout = screen["layout"]  # type: ignore[index]
        self.assertTrue(layout["available"])  # type: ignore[index]
        self.assertIn("console_fit_risk", risk_codes(screen))
        self.assertIn("log_region_overflow", risk_codes(screen))

    def test_layout_fit_metrics_accept_safe_bottom_margin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "03-home-dashboard.png"
            write_win31_layout_screen(path, clipped=False)
            text = (
                "HOME BBS FILES NET PEERS DEV OTAP SETUP WIZ DIAG SAFE "
                "HOME CARD Coordinator Telemetry Relay disabled PCAP blocked"
            )
            result = analyze(root, [vision_record(path, text, 82.0, 96)])
        screen = only_screen(result)
        layout = screen["layout"]  # type: ignore[index]
        margins = layout["safeMarginsPx"]  # type: ignore[index]
        self.assertGreaterEqual(margins["bottom"], analyzer.SAFE_BOTTOM_MARGIN_PX)  # type: ignore[index]
        self.assertNotIn("console_fit_risk", risk_codes(screen))
        self.assertNotIn("log_region_overflow", risk_codes(screen))

    def test_strong_and_weak_ocr_cases_are_separated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            strong = root / "05-downloads.png"
            weak = root / "06-network.png"
            write_screen(strong, ["Downloads", "Download Catalog", "File Queue"])
            write_screen(weak, ["Network", "serial readonly", "mesh proposed"])
            result = analyze(
                root,
                [
                    vision_record(strong, "Downloads Download Catalog File Queue", 82.0, 80),
                    vision_record(weak, "Network serial readonly mesh proposed", 42.0, 80),
                ],
            )
        screens = {str(screen["file"]): screen for screen in result["screens"]}  # type: ignore[index]
        self.assertNotIn("weak_ocr_confidence", risk_codes(screens["05-downloads.png"]))
        self.assertIn("weak_ocr_confidence", risk_codes(screens["06-network.png"]))


if __name__ == "__main__":
    unittest.main()
