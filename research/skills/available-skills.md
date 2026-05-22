# Available Skills Inventory

Verified on 2026-05-22 from
`SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-05-22`.

## Relevant for the Prototype Build Packet task

| Skill | Path | Current use |
| --- | --- | --- |
| expert-agent-panels | `/home/cyber/.codex/skills/expert-agent-panels` | Controls the evidence-first specialist review loop and task/source-record updates. |
| imagegen | `/home/cyber/.codex/skills/.system/imagegen` | Relevant only for label-free public-safe raster backplates; exact factual labels stay in HTML/Markdown. |

## Conditional future use

| Skill | Path | Conditional use |
| --- | --- | --- |
| github:github | `/home/cyber/.codex/plugins/cache/openai-curated/github/004da724/skills/github` | Future GitHub repository, PR, issue, or Pages deployment orientation. |
| github:gh-address-comments | `/home/cyber/.codex/plugins/cache/openai-curated/github/004da724/skills/gh-address-comments` | Future actionable PR review comment handling. |
| github:gh-fix-ci | `/home/cyber/.codex/plugins/cache/openai-curated/github/004da724/skills/gh-fix-ci` | Future GitHub Actions failure investigation. |
| github:yeet | `/home/cyber/.codex/plugins/cache/openai-curated/github/004da724/skills/yeet` | Future commit, push, and draft PR publishing when explicitly requested. |
| openai-docs | `/home/cyber/.codex/skills/.system/openai-docs` | Future OpenAI API, model, Codex, or prompt-upgrade documentation checks. |
| plugin-creator | `/home/cyber/.codex/skills/.system/plugin-creator` | Future local plugin scaffolding. |
| skill-creator | `/home/cyber/.codex/skills/.system/skill-creator` | Future skill creation or update work. |
| skill-installer | `/home/cyber/.codex/skills/.system/skill-installer` | Future curated or repo-hosted skill installation. |

## Not relevant to this implementation

| Skill | Path | Reason |
| --- | --- | --- |
| canva:canva-branded-presentation | `/home/cyber/.codex/plugins/cache/openai-curated/canva/004da724/skills/canva-branded-presentation` | No Canva deck requested. |
| canva:canva-resize-for-all-social-media | `/home/cyber/.codex/plugins/cache/openai-curated/canva/004da724/skills/canva-resize-for-all-social-media` | No Canva social resize requested. |
| canva:canva-translate-design | `/home/cyber/.codex/plugins/cache/openai-curated/canva/004da724/skills/canva-translate-design` | No Canva localization requested. |
| davinci-resolve-audio-production | `/home/cyber/.codex/skills/davinci-resolve-audio-production` | DaVinci Resolve audio automation is out of scope. |
| davinci-resolve-automation | `/home/cyber/.codex/skills/davinci-resolve-automation` | DaVinci Resolve diagnostics and scripting are out of scope. |
| davinci-resolve-color-automation | `/home/cyber/.codex/skills/davinci-resolve-color-automation` | DaVinci Resolve color automation is out of scope. |
| davinci-resolve-editing | `/home/cyber/.codex/skills/davinci-resolve-editing` | DaVinci Resolve edit-page automation is out of scope. |
| davinci-resolve-fusion-composition | `/home/cyber/.codex/skills/davinci-resolve-fusion-composition` | DaVinci Resolve Fusion composition is out of scope. |
| davinci-resolve-production-review | `/home/cyber/.codex/skills/davinci-resolve-production-review` | DaVinci Resolve render review is out of scope. |
| davinci-resolve-project-factory | `/home/cyber/.codex/skills/davinci-resolve-project-factory` | DaVinci Resolve project creation is out of scope. |
| davinci-resolve-world-regeneration | `/home/cyber/.codex/skills/davinci-resolve-world-regeneration` | Source-backed Resolve world regeneration is out of scope. |

## Notes

- Plugin skill paths currently use cache hash `004da724`.
- The prior checked-in `36878fcb` and `eed16198` plugin cache hashes are stale.
- Future sessions must re-inventory skills before relying on path claims
  because skills and plugin cache paths can change independently of the ESP32
  repo.
