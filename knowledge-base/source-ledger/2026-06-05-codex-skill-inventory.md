# Codex Skill Inventory Ledger

Date: 2026-06-05

Source ID:
`SRC-LOCAL-CODEX-SKILL-INVENTORY-2026-06-05`

## Scope

Same-session local inventory for Codex skill path claims used by
`research/skills/available-skills.md` and the scaffold skill audit.

## Verified Facts

- Current GitHub plugin skill files are under
  `/home/cyber/.codex/plugins/cache/openai-curated/github/9c1190e4/skills/`.
- Current Canva plugin skill files are under
  `/home/cyber/.codex/plugins/cache/openai-curated/canva/9c1190e4/skills/`.
- The prior plugin cache hash `2b564709` is stale for the local GitHub and
  Canva plugin skill paths in this session.
- ESP32-local skills remain under `/mnt/h/esp32/.codex/skills`.

## Evidence

- `find /home/cyber/.codex/plugins/cache/openai-curated -maxdepth 5 -type f -path '*/skills/*/SKILL.md' -print`
  listed the GitHub plugin skills `github`, `gh-address-comments`,
  `gh-fix-ci`, and `yeet` under hash `9c1190e4`.
- The same command listed the Canva plugin skills
  `canva-branded-presentation`, `canva-resize-for-all-social-media`, and
  `canva-translate-design` under hash `9c1190e4`.
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_skills.py`
  failed before the refresh because `research/skills/available-skills.md`
  still referenced `2b564709`.

## Assumptions

- Plugin cache paths are local runtime paths and can drift independently of the
  ESP32 repository.
- Future sessions must refresh this inventory before relying on plugin cache
  paths.

## Unknowns

- Future plugin cache hash values are unknown.
- Whether additional plugins will be installed later is unknown.

## Authority Limits

This record does not install, remove, create, or modify Codex skills or
plugins. It does not authorize `/etc/codex` mutation, admin-strict
installation, release, publication, live hardware, serial/RF/XBee writes,
firmware flashing, bridge dispatch, credentials, or external-service
automation.
