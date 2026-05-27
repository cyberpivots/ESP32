# Win31 Dashboard Adaptive Visual Quality

Source index: [../../../knowledge-base/source-index.md](../../../knowledge-base/source-index.md)

## Scope

This record defines the repeatable adaptive visual-quality process for Win31
OPCON dashboard work on the accepted serial-nullmodem path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

The process is advisory to Gate H acceptance. DOS-C `vision-gate.json`,
ESP32 completion output, `bridge-transcript.jsonl`, and cleanup proof remain
the authoritative pass/fail evidence for live behavior.

## Verified Facts

- The current Gate H proof packet still passes DOS-C vision and paired ESP32
  completion gates.
- The current Gate H screenshots in the copied packet are `1920x1080`, while
  the intended proof target is `1024x600`.
- The tracked DOSBox-X serial-nullmodem config uses fullscreen desktop output:
  `fullscreen=true`, `fullresolution=desktop`, `windowresolution=original`,
  `output=opengl`, `showmenu=false`, and `scaler=none`.
- The Win31 operator source now computes startup client size from screen/window
  metrics and reflows child controls on resize events.
- The ESP32 analyzer now reports capture size, coordinate stack, normalized
  safe margins, and an advisory visual-fit status separate from gate status.

## Weighted Review Method

Use this method when CV/OCR, display geometry, or adaptive layout decisions are
non-trivial.

| Weight | Role class | Use |
| ---: | --- | --- |
| 5 | Coordinator / architecture-risk reviewer | Tie breaker and safety/source boundary owner. |
| 3 | High-reasoning specialist | Win31 UI/protocol, vision-gate, live-bench, or evidence audit review. |
| 2 | Medium-reasoning specialist | Governance, source curation, prompt/token triage, or docs coverage. |
| 1 | Low-risk helper | Narrow formatting or inventory checks only. |

A decision passes when weighted approval is at least `70%`, and there is no
source, cleanup, live-gate, protocol, or unsafe-lane blocker. Record each vote
with role, weight, evidence reviewed, vote, blockers, conditions, and final
disposition.

## 2026-05-26 Vote

| Role | Weight | Vote | Conditions |
| --- | ---: | --- | --- |
| Win31 UI/protocol analyst | 3 | Approve | Preserve request formatting, queue sequence, line budget, disabled controls, and COM1/nullmodem path. |
| Win31 vision-gate analyst | 3 | Approve with visual-proof condition | Report `1920x1080` capture mismatch, coordinate stack, normalized margins, and advisory visual-fit status. |
| Evidence record auditor | 3 | Approve with record condition | Add source index, source ledger, task log, handoff, and paired DOS-C records. |
| Coordinator | 5 | Approve | Implement source/analyzer/records now; require fresh copied proof before visual-fit acceptance. |

Weighted result: `14/14`, pass. No live hardware mutation, flash, PCAP,
packet-driver, BLE, mesh, relay/XBee, TFT, MicroSD, load, mains, erase,
monitor, serial-write expansion, or Gate G export action is opened.

## Acceptance Criteria

- Current source validation passes in both repos.
- Analyzer report includes capture size, coordinate stack, normalized margins,
  and advisory visual-fit status.
- A later fresh proof packet captures the intended `1024x600` surface or
  records the exact display/capture mismatch as a blocker.
- Target-view mapping remains `10/10`.
- Target screens have no `console_fit_risk`, no `log_region_overflow`, bottom
  margin `>=16 px`, and right margin `>=4 px` after normalization.
- Unsafe controls remain visibly disabled or intent-only.

## Unknowns

- The exact installed LCD identity is not independently proven by EDID in this
  record; SunFounder is a user-stated display class plus candidate product
  source.
- A fresh 2026-05-26 Win31/DOSBox-X proof packet first captured the active Pi
  display path at `1024x600` with a 640x480 visible surface, then the follow-up
  fixed it with X11 fullscreen config and compact 640-logical-pixel OPCON
  layout positions.
- Human usability remains unmeasured.

## Fullscreen Recovery Follow-Up

The current fullscreen recovery status is `fixed-live-open`. Final proof
`final-live-20260527T014831Z` captured `1024x600`, bbox `(0,1)-(1023,599)`,
zero right/bottom margin, and the fixed dashboard was left open for human
panel confirmation.

## CBBS Rename And Input Follow-Up

The 2026-05-27 CBBS pass updates the current user-facing name, primary
navigation, icon, package/launcher prefixes, and copied-screenshot stale
branding guard in DOS-C. It is a local build/source validation pass only for
visual acceptance: live pointer behavior and the new Program Manager `CBBS`
icon are not accepted until fresh screenshots, physical input A/B proof, and
cleanup or explicit left-running proof are captured.
