# Available Skills Inventory

Verified on 2026-05-19 from `SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-05-19`.

## Relevant for this task

| Skill | Path | Current use |
| --- | --- | --- |
| skill-creator | `/home/cyber/.codex/skills/.system/skill-creator` | Used to scaffold and validate the new global skill. |
| openai-docs | `/home/cyber/.codex/skills/.system/openai-docs` | Used to verify current OpenAI model, reasoning, Codex subagent, and Codex config guidance from official docs. |
| expert-agent-panels | `/home/cyber/.codex/skills/expert-agent-panels` | New output of this task; future trigger for evidence-first specialist panel loops. |

## Conditional future use

| Skill | Path | Conditional use |
| --- | --- | --- |
| github:github | `/home/cyber/.codex/plugins/cache/openai-curated/github/eed16198/skills/github` | Future GitHub repository, PR, or issue orientation. |
| github:gh-address-comments | `/home/cyber/.codex/plugins/cache/openai-curated/github/eed16198/skills/gh-address-comments` | Future actionable PR review comment handling. |
| github:gh-fix-ci | `/home/cyber/.codex/plugins/cache/openai-curated/github/eed16198/skills/gh-fix-ci` | Future GitHub Actions failure investigation. |
| github:yeet | `/home/cyber/.codex/plugins/cache/openai-curated/github/eed16198/skills/yeet` | Future commit, push, and draft PR publishing when explicitly requested. |
| plugin-creator | `/home/cyber/.codex/skills/.system/plugin-creator` | Future local plugin scaffolding. |
| skill-installer | `/home/cyber/.codex/skills/.system/skill-installer` | Future curated or repo-hosted skill installation. |

## Not relevant to this skill creation task

| Skill | Path | Reason |
| --- | --- | --- |
| imagegen | `/home/cyber/.codex/skills/.system/imagegen` | No raster image generation or editing requested. |
| canva:canva-branded-presentation | `/home/cyber/.codex/plugins/cache/openai-curated/canva/eed16198/skills/canva-branded-presentation` | No Canva deck requested. |
| canva:canva-resize-for-all-social-media | `/home/cyber/.codex/plugins/cache/openai-curated/canva/eed16198/skills/canva-resize-for-all-social-media` | No Canva social resize requested. |
| canva:canva-translate-design | `/home/cyber/.codex/plugins/cache/openai-curated/canva/eed16198/skills/canva-translate-design` | No Canva localization requested. |
| davinci-resolve-audio-production | `/home/cyber/.codex/skills/davinci-resolve-audio-production` | DaVinci Resolve audio automation is out of scope. |
| davinci-resolve-automation | `/home/cyber/.codex/skills/davinci-resolve-automation` | DaVinci Resolve diagnostics and scripting are out of scope. |
| davinci-resolve-color-automation | `/home/cyber/.codex/skills/davinci-resolve-color-automation` | DaVinci Resolve color automation is out of scope. |
| davinci-resolve-editing | `/home/cyber/.codex/skills/davinci-resolve-editing` | DaVinci Resolve edit-page automation is out of scope. |
| davinci-resolve-fusion-composition | `/home/cyber/.codex/skills/davinci-resolve-fusion-composition` | DaVinci Resolve Fusion composition is out of scope. |
| davinci-resolve-production-review | `/home/cyber/.codex/skills/davinci-resolve-production-review` | DaVinci Resolve render review is out of scope. |
| davinci-resolve-project-factory | `/home/cyber/.codex/skills/davinci-resolve-project-factory` | DaVinci Resolve project creation is out of scope. |
| davinci-resolve-world-regeneration | `/home/cyber/.codex/skills/davinci-resolve-world-regeneration` | Source-backed Resolve world regeneration is out of scope. |

## Notes

- Plugin skill paths currently use cache hash `eed16198`; older workspace notes
  with different plugin cache hashes are stale.
- Future sessions must re-inventory skills before relying on this list because
  skills and plugin cache paths can change independently of the ESP32 repo.
