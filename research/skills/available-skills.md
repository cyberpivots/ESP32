# Available Skills Inventory

Verified on 2026-05-28 from
`SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-05-28`.

## Relevant for BBS UI system operation work

| Skill | Path | Current use |
| --- | --- | --- |
| expert-agent-panels | `/home/cyber/.codex/skills/expert-agent-panels` | Controls the evidence-first specialist review loop and task/source-record updates. |
| esp32-live-gate-coordinator | `/mnt/h/esp32/.codex/skills/esp32-live-gate-coordinator` | Use for ESP-NOW BBS live-gate boundary checks, same-session evidence requirements, and accepted-path preservation. |
| win31-dashboard-vision-gate | `/mnt/h/esp32/.codex/skills/win31-dashboard-vision-gate` | Use only for copied Win31 screenshots, OCR/CV JSON, and bridge transcript corroboration. |

## Conditional future use

| Skill | Path | Conditional use |
| --- | --- | --- |
| github:github | `/home/cyber/.codex/plugins/cache/openai-curated/github/be69e54e/skills/github` | Future GitHub repository, PR, issue, or Pages deployment orientation. |
| github:gh-address-comments | `/home/cyber/.codex/plugins/cache/openai-curated/github/be69e54e/skills/gh-address-comments` | Future actionable PR review comment handling. |
| github:gh-fix-ci | `/home/cyber/.codex/plugins/cache/openai-curated/github/be69e54e/skills/gh-fix-ci` | Future GitHub Actions failure investigation. |
| github:yeet | `/home/cyber/.codex/plugins/cache/openai-curated/github/be69e54e/skills/yeet` | Future commit, push, and draft PR publishing when explicitly requested. |
| imagegen | `/home/cyber/.codex/skills/.system/imagegen` | Future generated raster assets only; exact factual labels stay in HTML/Markdown. |
| openai-docs | `/home/cyber/.codex/skills/.system/openai-docs` | Future OpenAI API, model, Codex, or prompt-upgrade documentation checks. |
| plugin-creator | `/home/cyber/.codex/skills/.system/plugin-creator` | Future local plugin scaffolding. |
| skill-creator | `/home/cyber/.codex/skills/.system/skill-creator` | Use only if a later authorized edit updates or creates skills. |
| skill-installer | `/home/cyber/.codex/skills/.system/skill-installer` | Future curated or repo-hosted skill installation. |

## Not relevant to this implementation

| Skill | Path | Reason |
| --- | --- | --- |
| canva:canva-branded-presentation | `/home/cyber/.codex/plugins/cache/openai-curated/canva/be69e54e/skills/canva-branded-presentation` | No Canva deck requested. |
| canva:canva-resize-for-all-social-media | `/home/cyber/.codex/plugins/cache/openai-curated/canva/be69e54e/skills/canva-resize-for-all-social-media` | No Canva social resize requested. |
| canva:canva-translate-design | `/home/cyber/.codex/plugins/cache/openai-curated/canva/be69e54e/skills/canva-translate-design` | No Canva localization requested. |
| davinci-resolve-audio-production | `/home/cyber/.codex/skills/davinci-resolve-audio-production` | DaVinci Resolve audio automation is out of scope. |
| davinci-resolve-automation | `/home/cyber/.codex/skills/davinci-resolve-automation` | DaVinci Resolve diagnostics and scripting are out of scope. |
| davinci-resolve-color-automation | `/home/cyber/.codex/skills/davinci-resolve-color-automation` | DaVinci Resolve color automation is out of scope. |
| davinci-resolve-editing | `/home/cyber/.codex/skills/davinci-resolve-editing` | DaVinci Resolve edit-page automation is out of scope. |
| davinci-resolve-fusion-composition | `/home/cyber/.codex/skills/davinci-resolve-fusion-composition` | DaVinci Resolve Fusion composition is out of scope. |
| davinci-resolve-production-review | `/home/cyber/.codex/skills/davinci-resolve-production-review` | DaVinci Resolve render review is out of scope. |
| davinci-resolve-project-factory | `/home/cyber/.codex/skills/davinci-resolve-project-factory` | DaVinci Resolve project creation is out of scope. |
| davinci-resolve-world-regeneration | `/home/cyber/.codex/skills/davinci-resolve-world-regeneration` | Source-backed Resolve world regeneration is out of scope. |

## Notes

- Plugin skill paths currently use cache hash `be69e54e`.
- The prior checked-in `004da724`, `36878fcb`, and `eed16198` plugin cache
  hashes are stale.
- ESP32-local skills are present under `/mnt/h/esp32/.codex/skills`.
- Future sessions must re-inventory skills before relying on path claims
  because skills and plugin cache paths can change independently of the ESP32
  repo.
