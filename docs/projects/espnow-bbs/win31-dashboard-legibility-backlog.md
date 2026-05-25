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

## Verified Facts

- The input packet is copied local evidence; no live bench mutation is performed.
- The existing DOS-C vision gate remains the pass/fail screenshot gate.
- This analyzer reports advisory legibility and layout-fit metrics for backlog ranking only.
- Evidence root: `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-24-win31-viewfinder-full-completion/full-completion-20260524T135020Z`.
- Accepted DOS-C vision gate status: `pass`; failures: `[]`.
- Screenshots analyzed: 17; target views mapped: 10/10.
- Total OCR words: 2964; lowest OCR confidence: 48.21; median OCR confidence: 50.63.
- Lowest estimated layout safe margin: bottom 0 px; right 9 px.

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
