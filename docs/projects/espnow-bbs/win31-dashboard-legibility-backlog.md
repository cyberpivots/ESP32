# Win31 Dashboard Local ML/CV Legibility Research Backlog

Analysis date: 2026-05-24

Source index: [../../../knowledge-base/source-index.md](../../../knowledge-base/source-index.md)

## Scope

This is a local-only, advisory research backlog for Win31 OPCON dashboard
visual legibility. It reads copied screenshots and `vision-gate.json` from
the accepted baseline packet and does not change firmware, bridge wire
protocol, live hardware behavior, or completion acceptance.

The pass/fail path remains transcript-first: DOS-C `win31_dashboard_vision_gate.py`
and ESP32 `scripts/espnow_bbs_live_gate.py complete` own acceptance. This
document ranks UI hypotheses and before/after acceptance evidence only.

## Sources

- `SRC-LOCAL-WIN31-DASHBOARD-ML-LIVE-GATE-2026-05-23`
- `SRC-LOCAL-WIN31-DASHBOARD-LEGIBILITY-RESEARCH-2026-05-24`
- `SRC-OPENCV-TEMPLATE-MATCHING-2026-05-23`
- `SRC-TESSERACT-IMAGE-QUALITY-2026-05-23`
- `SRC-WCAG-CONTRAST-MINIMUM-2026-05-24`
- `SRC-MICROSOFT-WIN32-UI-PRINCIPLES-2026-05-24`
- `SRC-MICROSOFT-MENU-GUIDELINES-2026-05-24`
- `SRC-NNG-HEURISTICS-SUMMARY-2026-05-24`
- `SRC-LOCAL-WIN31-DASHBOARD-1024X600-2026-05-26`

## Verified Facts

- The input packet is copied local evidence; no live bench mutation is performed.
- The existing DOS-C vision gate remains the pass/fail screenshot gate.
- This analyzer reports advisory legibility and layout-fit metrics for backlog ranking only.
- Evidence root: `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-24-win31-viewfinder-full-completion/full-completion-20260524T135020Z`.
- Accepted DOS-C vision gate status: `pass`; failures: `[]`.
- Screenshots analyzed: 17; target views mapped: 10/10.
- Total OCR words: 2964; lowest OCR confidence: 48.21; median OCR confidence: 50.63.
- Lowest estimated layout safe margin: bottom 0 px; right 9 px.

## 2026-05-26 Visual Design Continuation

Verified facts:

- DOS-C source was updated at
  `/mnt/h/dos-c/software/win31-operator/src/operator.c`.
- The operator client target is now 640x360, with a two-row navigation strip
  using `HOME`, `BBS BOARD`, `DOWNLOADS`, `NETWORK`, `PEERS`, `DEVICES`,
  `OTAP`, `SETTINGS`, `WIZARD`, `DIAGNOSTICS`, and `SAFETY`.
- Action captions are now `PULL MSG`, `POST`, `SEARCH`, `ACK`, `CATALOG`,
  `QUEUE`, and `OTAP INTENT`, backed by the existing request handlers.
- Relay, Flash, Serial, and PCAP footer controls remain disabled; Safety and
  Diagnostics now name the external live gates that own those actions.
- The latest copied structured Gate H packet at
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-25-gate-h-structured-live/gate-h-structured-live-20260525T155900Z/`
  still passes the DOS-C vision gate: `status: pass`, `failures: []`.
- Advisory analysis of that same copied packet reports 14 screenshots, mapped
  target views `7/10`, lowest OCR confidence `51.42`, median OCR confidence
  `54.99`, no `console_fit_risk`, no `log_region_overflow`, lowest layout
  bottom margin `120 px`, and lowest layout right margin `384 px`.

Assumptions:

- The fixed Win3.1 viewfinder remains the accepted operator surface for this
  lane until a later accepted gate changes the client direction.
- OCR/CV remains advisory and secondary to bridge transcript behavior.

Unknowns:

- No fresh revised-UI screenshot packet exists yet, so the 2026-05-26 source
  change has not proven OCR confidence >= 60 or removed navigation-label gaps.
- The latest structured Gate H copied packet lacks Settings, Wizard, and
  Devices screenshots, so it cannot satisfy the advisory `10/10` mapped-view
  target by itself.

## 2026-05-26 1024x600 Layout Refactor

Verified facts:

- The proof screen being targeted is 1024x600.
- DOS-C source was updated again at
  `/mnt/h/dos-c/software/win31-operator/src/operator.c`.
- The operator client target is now 1000x500. It is intentionally smaller than
  a full 1024x600 client because `AdjustWindowRect` adds Win3.1 frame and menu
  chrome around the requested client.
- The two-row navigation labels remain `HOME`, `BBS BOARD`, `DOWNLOADS`,
  `NETWORK`, `PEERS`, `DEVICES`, `OTAP`, `SETTINGS`, `WIZARD`, `DIAGNOSTICS`,
  and `SAFETY`.
- The status strip, navigation strip, carousel controls, list/detail panes,
  action row, disabled footer, and console log were widened and reflowed for the
  1024 px proof-screen width.
- Relay, Flash, Serial, and PCAP controls remain disabled; Safety and
  Diagnostics still assign hardware mutation to external live gates.
- Source-level validation passed after the refactor. The latest copied
  structured Gate H packet still passes the DOS-C vision gate.
- Advisory analysis of that copied packet still reports mapped target views
  `7/10`, lowest OCR confidence `51.42`, median OCR confidence `54.99`, no
  `console_fit_risk`, no `log_region_overflow`, lowest layout bottom margin
  `120 px`, and lowest layout right margin `384 px`.

Assumptions:

- A 1000x500 client is the safer screen-oriented target for a top-left Win3.1
  window on a 1024x600 capture because it leaves room for window chrome and
  bottom quiet space.
- OCR/CV remains advisory and secondary to bridge transcript behavior.

Unknowns:

- No fresh copied screenshot packet exists yet for the 1000x500 layout; the
  copied-evidence metrics above are from the previous 640 px source capture.
- The revised layout has not yet proven mean OCR confidence >= 60, eliminated
  navigation-label gaps, or mapped all 10 target views in copied evidence.

## 2026-05-26 Adaptive Visual Quality Refactor

Verified facts:

- DOS-C source now computes the Win31 OPCON startup client size from screen and
  window metrics, then reflows controls from one computed layout on resize.
- ESP32 analyzer output now separates functional gate status from advisory
  visual-fit status and records capture sizes, coordinate-stack metadata,
  normalized safe margins, and proof-target mismatch risks.
- The current copied Gate H packet still passes the DOS-C vision gate and
  paired ESP32 completion gate.
- The current copied Gate H screenshots are `1920x1080`, not the intended
  `1024x600` proof target.
- A rerun against that current packet reports advisory visual-fit status
  `fail`, capture size `1920x1080`, mapped target views `10/10`, median OCR
  confidence `51.25`, `proof_capture_size_mismatch` on 18 screens,
  `console_fit_risk` on 18 screens, and `log_region_overflow` on 18 screens.

Assumptions:

- The adaptive source change is the correct code-side response, but a fresh
  copied packet must verify whether Pi display mode, DOSBox-X fullscreen
  behavior, and capture tooling now align with the intended 1024x600 proof.

Unknowns:

- Whether the 1920x1080 capture mismatch comes from current Pi display mode,
  DOSBox-X scaling/fullscreen behavior, capture tool geometry, or stale proof
  context.
- No fresh adaptive-layout proof packet exists yet, so this section does not
  claim visual-fit closure.

## Assumptions

- Tesseract OCR confidence and word count are useful legibility proxies, not human usability proof.
- Pixel-level contrast and density heuristics should be compared across revisions, not used alone for acceptance.
- Estimated Win31 client regions are derived from local foreground pixels and must be compared against live screenshots.

## Unknowns

- No revised UI screenshot packet has been measured by this task.
- No user study, PaddleOCR benchmark, or hosted vision critique is approved by this task.

## Per-Screen Metrics

| Screen | View | OCR words | OCR conf | Foreground | Edge | Contrast | Layout bottom/right | Layout fit risks | Risk score | Top risks |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | ---: | --- |
| `00-maximized-launch-compact.png` | Launch | 161 | 48.30 | 33.8% | 12.4% | 1.95 | 0/9 | console_fit_risk, log_region_overflow, navigation_label_gap | 25 | weak_ocr_confidence, excessive_visual_density, edge_noise_load, decorative_ocr_noise |
| `00-opcon-dashboard-maximized-compact.png` | Home | 161 | 48.30 | 33.8% | 12.4% | 1.95 | 0/9 | console_fit_risk, log_region_overflow, navigation_label_gap | 25 | weak_ocr_confidence, excessive_visual_density, edge_noise_load, decorative_ocr_noise |
| `01-message-board-actions.png` | BBS | 167 | 51.32 | 33.1% | 12.0% | 1.92 | 0/9 | console_fit_risk, log_region_overflow, navigation_label_gap | 22 | weak_ocr_confidence, excessive_visual_density, edge_noise_load, contrast_risk |
| `02-views-dropdown.png` | Navigation | 117 | 70.20 | 39.1% | 12.2% | 2.45 | 0/9 | console_fit_risk, log_region_overflow | 19 | excessive_visual_density, edge_noise_load, contrast_risk, color_complexity |
| `03-home-dashboard.png` | Home | 157 | 50.02 | 33.8% | 12.4% | 1.95 | 0/9 | console_fit_risk, log_region_overflow, navigation_label_gap | 24 | weak_ocr_confidence, excessive_visual_density, edge_noise_load, decorative_ocr_noise |
| `04-message-board.png` | BBS | 254 | 53.44 | 33.8% | 12.4% | 1.95 | 0/9 | console_fit_risk, log_region_overflow, navigation_label_gap | 25 | weak_ocr_confidence, excessive_text_density, excessive_visual_density, edge_noise_load |
| `05-downloads.png` | Downloads | 122 | 72.82 | 39.3% | 12.3% | 2.48 | 0/9 | console_fit_risk, log_region_overflow | 19 | excessive_visual_density, edge_noise_load, contrast_risk, color_complexity |
| `06-network.png` | Network | 161 | 49.19 | 32.8% | 11.9% | 1.92 | 0/9 | console_fit_risk, log_region_overflow, navigation_label_gap | 25 | weak_ocr_confidence, excessive_visual_density, edge_noise_load, decorative_ocr_noise |
| `07-peers.png` | Peers | 227 | 48.21 | 34.8% | 13.0% | 2.00 | 0/9 | console_fit_risk, log_region_overflow, navigation_label_gap | 27 | weak_ocr_confidence, excessive_text_density, excessive_visual_density, edge_noise_load |
| `08-devices.png` | Devices | 254 | 53.44 | 33.8% | 12.4% | 1.95 | 0/9 | console_fit_risk, log_region_overflow, navigation_label_gap | 25 | weak_ocr_confidence, excessive_text_density, excessive_visual_density, edge_noise_load |
| `09-otap.png` | OTAP | 167 | 51.32 | 33.1% | 12.0% | 1.92 | 0/9 | console_fit_risk, log_region_overflow, navigation_label_gap | 22 | weak_ocr_confidence, excessive_visual_density, edge_noise_load, contrast_risk |
| `10-settings.png` | Settings | 168 | 51.16 | 31.9% | 11.4% | 1.86 | 0/9 | console_fit_risk, log_region_overflow, navigation_label_gap | 22 | weak_ocr_confidence, excessive_visual_density, edge_noise_load, contrast_risk |
| `11-wizard.png` | Wizard | 150 | 55.33 | 32.7% | 11.8% | 1.92 | 0/9 | console_fit_risk, log_region_overflow, navigation_label_gap | 22 | weak_ocr_confidence, excessive_visual_density, edge_noise_load, contrast_risk |
| `12-diagnostics.png` | Diagnostics | 231 | 50.33 | 34.3% | 12.7% | 1.97 | 0/9 | console_fit_risk, log_region_overflow, navigation_label_gap | 26 | weak_ocr_confidence, excessive_text_density, excessive_visual_density, edge_noise_load |
| `13-safety.png` | Safety | 153 | 50.63 | 33.4% | 12.2% | 1.93 | 0/9 | console_fit_risk, log_region_overflow, navigation_label_gap | 22 | weak_ocr_confidence, excessive_visual_density, edge_noise_load, contrast_risk |
| `14-final-refresh.png` | Home | 157 | 49.20 | 33.8% | 12.4% | 1.95 | 0/9 | console_fit_risk, log_region_overflow, navigation_label_gap | 25 | weak_ocr_confidence, excessive_visual_density, edge_noise_load, decorative_ocr_noise |
| `15-pre-cleanup.png` | Home | 157 | 49.20 | 33.8% | 12.4% | 1.95 | 0/9 | console_fit_risk, log_region_overflow, navigation_label_gap | 25 | weak_ocr_confidence, excessive_visual_density, edge_noise_load, decorative_ocr_noise |

## View Weak Spots

| View | Screens | Lowest OCR conf | Max words | Weak spots |
| --- | ---: | ---: | ---: | --- |
| Home | 4 | 48.30 | 161 | OCR confidence floor is 48.30. Contrast risk appears on 4 screen(s). ASCII/decorative edge load competes with readable text. Text or foreground density is high enough to slow scanning. Screenshot quiet-zone margins are tight. Estimated client/log regions do not preserve the required safe margin. Navigation labels were not consistently readable in OCR. |
| BBS | 2 | 51.32 | 254 | OCR confidence floor is 51.32. Contrast risk appears on 2 screen(s). ASCII/decorative edge load competes with readable text. Text or foreground density is high enough to slow scanning. Screenshot quiet-zone margins are tight. Estimated client/log regions do not preserve the required safe margin. Navigation labels were not consistently readable in OCR. |
| Downloads | 1 | 72.82 | 122 | Contrast risk appears on 1 screen(s). ASCII/decorative edge load competes with readable text. Text or foreground density is high enough to slow scanning. Screenshot quiet-zone margins are tight. Estimated client/log regions do not preserve the required safe margin. |
| Network | 1 | 49.19 | 161 | OCR confidence floor is 49.19. Contrast risk appears on 1 screen(s). ASCII/decorative edge load competes with readable text. Text or foreground density is high enough to slow scanning. Screenshot quiet-zone margins are tight. Estimated client/log regions do not preserve the required safe margin. Navigation labels were not consistently readable in OCR. |
| Peers | 1 | 48.21 | 227 | OCR confidence floor is 48.21. Contrast risk appears on 1 screen(s). ASCII/decorative edge load competes with readable text. Text or foreground density is high enough to slow scanning. Screenshot quiet-zone margins are tight. Estimated client/log regions do not preserve the required safe margin. Navigation labels were not consistently readable in OCR. |
| OTAP | 1 | 51.32 | 167 | OCR confidence floor is 51.32. Contrast risk appears on 1 screen(s). ASCII/decorative edge load competes with readable text. Text or foreground density is high enough to slow scanning. Screenshot quiet-zone margins are tight. Estimated client/log regions do not preserve the required safe margin. Navigation labels were not consistently readable in OCR. |
| Settings | 1 | 51.16 | 168 | OCR confidence floor is 51.16. Contrast risk appears on 1 screen(s). ASCII/decorative edge load competes with readable text. Text or foreground density is high enough to slow scanning. Screenshot quiet-zone margins are tight. Estimated client/log regions do not preserve the required safe margin. Navigation labels were not consistently readable in OCR. |
| Wizard | 1 | 55.33 | 150 | Contrast risk appears on 1 screen(s). ASCII/decorative edge load competes with readable text. Text or foreground density is high enough to slow scanning. Screenshot quiet-zone margins are tight. Estimated client/log regions do not preserve the required safe margin. Navigation labels were not consistently readable in OCR. |
| Diagnostics | 1 | 50.33 | 231 | OCR confidence floor is 50.33. Contrast risk appears on 1 screen(s). ASCII/decorative edge load competes with readable text. Text or foreground density is high enough to slow scanning. Screenshot quiet-zone margins are tight. Estimated client/log regions do not preserve the required safe margin. Navigation labels were not consistently readable in OCR. |
| Safety | 1 | 50.63 | 153 | OCR confidence floor is 50.63. Contrast risk appears on 1 screen(s). ASCII/decorative edge load competes with readable text. Text or foreground density is high enough to slow scanning. Screenshot quiet-zone margins are tight. Estimated client/log regions do not preserve the required safe margin. Navigation labels were not consistently readable in OCR. |

## Ranked Backlog

| Rank | Hypothesis | Grounded finding | Local measurement | Implement-later acceptance criteria |
| ---: | --- | --- | --- | --- |
| 1 | Shrink the drawn shell and log/footer region so the whole OPCON client stays inside the 1024x600 proof capture with a visible quiet zone. | 17/17 screens had estimated client fit risk; 17/17 had log-region bottom overflow. | Track layout.safeMarginsPx, consoleLog region bounds, region overlaps, and DOS-C vision-gate status on before/after screenshots. | Every target screen keeps layout bottom margin >= 16px, right margin >= 4px, no console_fit_risk, no log_region_overflow, and the existing DOS-C vision gate passes. |
| 2 | Use fewer dim foreground colors for body text and reserve low-contrast cyan/amber treatments for decoration or inactive hints. | 17/17 screens had estimated contrast risk; 15/17 had OCR confidence below 60. | Track median foreground/background contrast ratio, lowContrastForegroundShare, and OCR confidence by view. | Target views reach median contrast ratio >= 4.5, lowContrastForegroundShare <= 0.25, and mean OCR confidence >= 60 without weakening the existing gate. |
| 3 | Give the status/action strip a fixed quiet zone and move transient log lines away from the bottom edge. | 17/17 screens had tight bottom or right quiet-zone margins. | Measure bottomMarginPx, rightMarginPx, foregroundRatio, and OCR word count on every captured view. | Target screens keep bottomMarginPx >= 16 and rightMarginPx >= 4 while preserving the accepted transcript-first proof path. |
| 4 | Keep the retro ANSI style but reserve repeated glyph borders for section boundaries so OCR and human scanning see fewer false words. | 6/17 screens produced decorative OCR noise and 17/17 exceeded edge-load thresholds. | Compare edgeRatio, decorativeNoiseTokenRatio, Tesseract meanConfidence, and required view detection before and after a layout revision. | Every target view stays gate-passable, decorativeNoiseTokenRatio is below 0.07 on target screens, and no target screen has edgeRatio above 0.105. |
| 5 | Recognition improves when the menu, tab, card title, and action label all use the same task name. | The baseline includes abbreviated tab/menu labels while view titles and tasks use longer names such as Message Board, Downloads, Diagnostics, and Safety. | OCR each navigation area and compare normalized menu/tab labels against expected task names for every target view. | The analyzer detects the same plain label for Home, BBS, Downloads, Network, Peers, OTAP, Settings, Wizard, Diagnostics, and Safety in both navigation and page title regions. |
| 6 | Plain-language helper text should translate OTAP, gate, serial-readonly, PCAP, and mesh state into user-visible operational meaning. | High-risk terms observed in OCR include OTAP, gate, serial-readonly, PCAP, mesh state. | Check OCR for approved phrase pairs such as OTAP -> update request only and serial-readonly -> hardware writes disabled. | Each high-risk concept has a readable plain-language phrase on the relevant target view and the footer uses those phrases consistently. |
| 7 | Separate current view, system health, safe actions, and primary task into predictable regions with stronger headings. | 4/17 screens were text-dense and 0/17 target screens had weak title OCR; 0/17 had tight estimated region spacing. | Use template matching for heading/control regions, OCR title detection, word count per region, and screenshot bounds checks. | Each target view exposes one readable view title, one health summary, one primary task region, and one safety/action region in local CV templates. |
| 8 | Disabled Relay, Flash, Serial, and PCAP controls should state why they are disabled and which external path owns the action. | The baseline footer repeats disabled/gated control names; the Safety view has the clearest explanation but the footer remains terse. | OCR footer/control regions for disabled control name, reason phrase, and owner path phrase. | Each disabled control exposes a readable reason and owner path while live hardware mutation remains outside this advisory analyzer. |
| 9 | A stable local JSON/Markdown report lets design revisions improve legibility while preserving the existing completion gate. | The current pass/fail gate is transcript-first; this analyzer adds advisory metrics that can compare later UI revisions without changing acceptance. | Run this analyzer on each copied packet and diff screen metrics, view summaries, and ranked backlog scores. | A later UI-change task includes before/after analyzer JSON, the existing DOS-C vision gate result, ESP32 completion gate result, and no live bench mutation outside the approved lane. |

## Measurement Notes

- `foregroundRatio`, `edgeRatio`, color clusters, contrast estimates, and bounds come from local image pixels.
- `layout.safeMarginsPx`, `layout.regions`, and layout fit risks come from local foreground-region estimates.
- OCR word counts, OCR text, and mean confidence come from the copied `vision-gate.json` records.
- OpenCV foreground/component analysis is used here for stable title, footer, disabled-control, primary-action, and console-log region checks.
- A later revision must show before/after analyzer JSON plus unchanged DOS-C vision-gate and ESP32 completion-gate behavior before claiming improvement.
