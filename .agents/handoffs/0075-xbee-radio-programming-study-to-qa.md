# Handoff 0075 - XBee Radio Programming Study To QA

## Current State

The XBee radio programming study is implemented as a Tier 2 docs/tooling
package. The new CLI is offline-first:

- `inventory` does not open serial ports.
- `profile-diff` does not open serial ports or write bytes.
- `write-plan` does not open serial ports, write bytes, or apply settings.
- `readonly` delegates to the existing fixed AT read-query probe and requires
  `--confirm-sends-read-commands`.

## Files To Review

- `scripts/xbee_radio_study.py`
- `tests/scaffold_audits/test_xbee_radio_study.py`
- `docs/projects/four-relay-xbee-wifi/xbee-radio-programming-study.md`
- `knowledge-base/source-ledger/2026-05-29-xbee-radio-programming-study.md`
- `.codex/skills/xbee-radio-integration/SKILL.md`
- `research/skills/available-skills.md`
- `submodules/hardware/rlxsc-xbee-pro-s3b/docs/xbee-radio-programming-study.md`

## QA Focus

- Confirm no `apply` command or write path exists in `scripts/xbee_radio_study.py`.
- Confirm `readonly` wording remains precise: it is not persistent-setting
  writing, but it does send serial read-query bytes after explicit confirmation.
- Confirm `SH`, `SL`, and `KY` stay redacted by default.
- Confirm source-index references exist for all new source IDs.
- Confirm public docs do not include serial identifiers, raw passive bytes, AES
  keys, address plans, private COM mappings, or full setting snapshots.

## Still Blocked

XCTU host install proof, installer SHA-256, and first-run change-log evidence
are now recorded by Task 0087. Live adapter identity, current XBee settings,
settings backup, writes, `WR`, `AC`, API transmit frames, firmware
recovery/update, range tests, ESP32 carrier wiring, relay/load/mains work, and
live RF evidence all remain blocked until a later explicit gate.
