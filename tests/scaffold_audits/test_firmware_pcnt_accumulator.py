#!/usr/bin/env python3
"""Host-side checks for the PF0530V PCNT count-to-step policy."""

from __future__ import annotations

import unittest
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAIN_C = ROOT / "firmware/projects/four-relay-xbee-wifi/main/main.c"

COUNTS_PER_STEP = 4
MAX_STEPS_PER_POLL = 4


@dataclass(frozen=True)
class AccumResult:
    steps: int
    residual: int
    capped: bool = False
    direction_flipped: bool = False


def c_remainder(value: int, divisor: int) -> int:
    return value - int(value / divisor) * divisor


def accumulate(residual: int, delta: int) -> AccumResult:
    if delta == 0:
        return AccumResult(0, residual)
    combined = residual + delta
    flipped = residual != 0 and ((residual > 0 > delta) or (residual < 0 < delta))
    if flipped:
        combined = delta
    steps = int(combined / COUNTS_PER_STEP)
    next_residual = c_remainder(combined, COUNTS_PER_STEP)
    capped = abs(steps) > MAX_STEPS_PER_POLL
    if capped:
        steps = MAX_STEPS_PER_POLL if steps > 0 else -MAX_STEPS_PER_POLL
        next_residual = 0
    return AccumResult(steps, next_residual, capped, flipped)


class FirmwarePcntAccumulatorTests(unittest.TestCase):
    def test_source_exposes_pcnt_policy_constants(self) -> None:
        source = MAIN_C.read_text(encoding="utf-8")
        self.assertIn("FR_ENCODER_PCNT_COUNTS_PER_STEP 4", source)
        self.assertIn("FR_ENCODER_PCNT_MAX_STEPS_PER_POLL 4", source)
        self.assertIn("fr_encoder_pcnt_accumulate_steps", source)

    def test_four_counts_emit_one_step_each_direction(self) -> None:
        self.assertEqual(accumulate(0, 4), AccumResult(1, 0))
        self.assertEqual(accumulate(0, -4), AccumResult(-1, 0))

    def test_residual_counts_carry_across_polls(self) -> None:
        first = accumulate(0, 3)
        self.assertEqual(first, AccumResult(0, 3))
        self.assertEqual(accumulate(first.residual, 1), AccumResult(1, 0))

    def test_direction_reversal_clears_stale_residual(self) -> None:
        result = accumulate(3, -1)
        self.assertEqual(result, AccumResult(0, -1, direction_flipped=True))

    def test_burst_cap_prevents_runaway_steps(self) -> None:
        self.assertEqual(accumulate(0, 40), AccumResult(4, 0, capped=True))
        self.assertEqual(accumulate(0, -40), AccumResult(-4, 0, capped=True))

    def test_switch_guard_policy_is_source_visible(self) -> None:
        source = MAIN_C.read_text(encoding="utf-8")
        self.assertIn("fr_menu_resync_pcnt(menu, now_ms", source)
        self.assertIn("ENC_PCNT_SUPPRESS", source)
        self.assertIn("pcnt_suppressed_delta_count", source)


if __name__ == "__main__":
    unittest.main()
