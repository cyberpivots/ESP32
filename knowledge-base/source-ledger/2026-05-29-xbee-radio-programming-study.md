# Source Ledger - 2026-05-29 XBee Radio Programming Study

## Scope

Tier 2 XBee radio programming study package for the ESP32 workspace. This
records official-source refresh, a repo-local offline-first CLI wrapper, tests,
skill routing, and private XBee submodule notes.

No live serial probe, XBee setting write, `WR`, `AC`, API transmit frame,
firmware update/recovery, range test, ESP32 DIN/DOUT wiring, relay/load/mains
action, or host GUI installation was performed by the original study task.
The later XCTU host install proof is recorded separately by
`SRC-LOCAL-XCTU-INSTALL-PROOF-2026-05-29`.

## Verified facts

- Digi identifies `XBP9B-DPUT-001` as an XBee-PRO 900HP S3B
  Point2Multipoint model. Source ID: `SRC-DIGI-XBP9B-DPUT-001`.
- Digi's XCTU product page lists XCTU as a free Windows, macOS, and Linux GUI
  with graphical network view, API frame builder/interpreter, AT/API consoles,
  firmware explorer, recovery, range test, and update features. Source ID:
  `SRC-DIGI-XCTU-FEATURES-2026-05-29`.
- Digi's XCTU support page currently lists XCTU 6.5.13 Windows, macOS, Linux
  x64, and Linux x86 assets. The Windows detail page lists file
  `40003026_AL.exe`, size 230.5 MB, version `v. 6.5.13`, and version date
  2023-07-17. Source ID: `SRC-DIGI-XCTU-SUPPORT-2026-05-29`.
- Digi's XBee Studio product page describes multi-platform discovery,
  configuration, communication, recovery, and update features for XBee
  devices. Source ID: `SRC-DIGI-XBEE-STUDIO-2026-05-29`.
- Digi's `xbee-python` GitHub release API reports release `1.5.0` published
  2024-08-27, and PyPI reports `digi-xbee` version `1.5.0`. Source ID:
  `SRC-DIGI-XBEE-PYTHON-2026-05-29`.
- The new CLI is `scripts/xbee_radio_study.py`; it implements
  `inventory`, `readonly`, `profile-diff`, and `write-plan`. Source ID:
  `SRC-LOCAL-XBEE-RADIO-STUDY-2026-05-29`.

## Implementation evidence

- `inventory` reports host/tool state without opening serial ports.
- Pre-install same-session `inventory --json` validation ran in WSL2 with
  pyserial 3.5, found Windows CP210x candidate host ports with PnP identifiers
  redacted by default, found no `xctu` command or known XCTU install path,
  found no XBee Studio command or known install path, and found `digi-xbee` not
  installed/importable.
- `readonly` delegates to `scripts/xbee_read_only_probe.py at-query` and
  requires `--confirm-sends-read-commands`.
- `profile-diff` compares JSON files offline, redacts `SH`, `SL`, and `KY` by
  default, and marks write-like targets as review evidence only.
- `write-plan` emits `applyAllowed: false`, no apply command exists in v1, and
  all proposed actions are blocked pending a future Tier 3 gate.
- `.codex/skills/xbee-radio-integration/SKILL.md` routes future XBee/XCTU/900HP
  work to the existing source-backed boundaries.
- A later Tier 2 host-tooling continuation installed XCTU as a reference GUI
  and updated inventory detection for the per-user Windows `XCTU-NG` path.
  Source ID: `SRC-LOCAL-XCTU-INSTALL-PROOF-2026-05-29`.

## Reviewer quorum

Read-only reviewer quorum found no P1/P2 blockers for the Tier 2 docs/tooling
boundary. The communications and QA reviews required precise wording:
`readonly` may send non-persistent serial read-query bytes after confirmation,
so only `inventory`, `profile-diff`, and `write-plan` are no-serial-open/no-
serial-write operations.

## Blocked items

- Future XCTU application or firmware-library update prompts remain unresolved
  beyond the first-run 6.5.13 change-log screen captured by the later
  host-tooling continuation.
- Any host ports remain candidate ports only until disconnect/delta evidence or
  read-only identification proves the adapter.
- Future radio programming remains blocked until a Tier 3 gate records
  same-session adapter identity, current-setting backup, address/security plan,
  antenna and regulatory review, carrier voltage/DIN/DOUT proof, rollback
  procedure, reviewer quorum, and explicit operator authority.
