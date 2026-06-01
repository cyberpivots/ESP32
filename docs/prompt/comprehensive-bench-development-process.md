# Comprehensive Bench Development Process

Source basis:
`SRC-LOCAL-COMPREHENSIVE-BENCH-DEVELOPMENT-PROCESS-2026-05-31`,
`SRC-LOCAL-DEVELOPMENT-AGENT-PANEL-2026-05-31`,
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530L-2026-05-31`,
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530L-LIVE-2026-05-31`,
`SRC-LOCAL-TIER3-COM6-ATTENDED-INTERACTION-PROOF-2026-05-31`,
`SRC-LOCAL-LCD-GLYPH-ELECTRICAL-ACCEPTANCE-2026-05-31`,
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530M-2026-06-01`,
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530N-SCROLLING-XML-2026-06-01`,
`SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`,
`SRC-LOCAL-ESPNOW-GATE-H-STRUCTURED-LIVE-ACCEPTANCE-2026-05-25`,
and `SRC-LOCAL-ESPNOW-BBS-LCD-BROWSER-QA-HARDENING-2026-05-31`.

## Intent

Use this process when continuing ESP32 bench development for the Windows 11
PC-attached device currently claimed as COM6. The process reduces routine
human interruption by routing evidence gathering to specialist reviewers, but
it does not bypass human gates for live hardware, flashing, serial writes,
RF transmit, relay control, persistent settings, credentials, destructive
operations, external service changes, GitHub publication, or safety-critical
decisions.

## Verified Facts

- The latest recorded COM6 LCD/menu live gate is PF0530L, not PF0530H or
  PF0530K.
- PF0530L same-session records include COM6 identity, 4 MB flash, 3.3 V strap,
  rollback backup, staged hashes, write-flash, separate verify-flash,
  read-only monitor, transcript scan, and cleanup proof.
- PF0530L is available for user visual testing. The 2026-05-31 restarted
  Tier 3 attended COM6 proof accepted serial/menu physical interaction with
  `ENC_RAW`, `ENC_EV`, `BBS_MENU_STEP` in both directions, and short/long
  `BBS_MENU_SELECT` events.
- The later LCD glyph/electrical acceptance attempt refreshed COM6 identity
  and captured another interaction-rich PF0530L monitor. The follow-up
  read-only reset/monitor hit `LCD_INIT_FAIL stage=probe detail=scan-error`
  for the full capture. User-reported follow-up evidence shows a
  bi-directional LCD level converter with LCD-side 4.73 V on `VCC`/`SDA`/
  `SCL`, visible LCD life, and KY-040 `+`/idle `CLK`/idle `DT`/idle `SW` at
  3.3 V, followed by ESP32-side/LV-side `SDA`/`SCL` at 3.3 V. A read-only
  retry restored `LCD_INIT_OK`, BBS LCD/input readiness, all 13 page names,
  all five glyph banks, and zero unsafe markers. User visual confirmation
  accepts LCD visual/glyph readability: four readable rows, visible page
  changes, and readable custom glyph/widget pages. User final DMM confirmation
  accepts remaining continuity, KY-040 toggle, and current-margin checks for
  this gate. No further DMM evidence is required for the PF0530L LCD
  glyph/electrical acceptance gate. The concise acceptance markers are:
  serial/menu physical interaction accepted on retry, LCD visual/glyph
  readability accepted, and hardware/electrical acceptance closed for this
  PF0530L gate.
- PF0530N is the current non-live LCD/menu scrolling/XML source/test
  continuation. It keeps the PF0530L/PF0530M closed bridge and input-only/
  display-only boundaries, adds build-time `bbs_lcd_menu.v1` XML, generated
  static firmware/simulator menu definitions, `bbs_lcd_render.v2` viewport
  metadata, scroll-list navigation, grouped multi-row items, selected-row
  marquee timing, table glyph bank constraints, and host-side 20-character
  display-bound tests. PF0530N has not been flashed.
- The XBee bridge lane has a narrow accepted state: COM6 exposes the ESP32
  UART bridge to the attached XBee at host baud `115200`, and a benign
  bidirectional `link_probe` RF proof passed after bridge firmware.
- ESP-NOW BBS accepted live status remains transcript/proof-packet based;
  screenshots and visual checks are corroboration only.
- LCD/browser mirror work is host-only and inert; no firmware HTTP, WebSocket,
  SoftAP, Windows Wi-Fi mutation, or live browser proof is accepted.
- Relay, power, load, mains, TFT, MicroSD, BLE, mesh, PCAP, serial-write
  expansion, erase, and future flash/monitor gates remain closed unless a
  separate source-backed Tier 3 gate opens the exact surface.
- Development-agent panel records are present as local advisory automation;
  release or publication readiness still depends on clean validation and
  explicit GitHub publication authority.

## Assumptions

- COM6 is treated as the claimed bench attachment until freshly proven in a
  same-session Tier 3 gate.
- This packet is a records and routing artifact. It is not live authority.
- Future agents should gather safe repo evidence automatically before asking
  the user for a physical fact or live-gate authority.

## Unknowns

- Current PF0530N runtime behavior, physical readability of the PF0530N
  scroll-list/table page, relay module identity, final BBS/XBee payload display
  mapping, and live SoftAP/browser behavior are not accepted.
- Current recovery path and COM6 identity must be refreshed before any future
  live gate.
- CBBS live acceptance still depends on its own current evidence and must not
  be inferred from ESP32 or LCD records.

## `bench_state_packet.v1`

Required fields for any current bench packet:

| Field | Required content |
| --- | --- |
| `schema` | Literal `bench_state_packet.v1`. |
| `generatedFrom` | Source IDs, task logs, and ledgers used for the packet. |
| `claimedBenchPort` | Claimed Windows port, WSL path if known, and proof freshness. |
| `currentFirmwareLane` | Firmware ID, source record, live record, acceptance status, and gaps. |
| `deviceIdentity` | Chip, MAC, flash size, flash strap, and whether evidence is same-session. |
| `rollbackRecovery` | Backup path/hash and recovery command status. |
| `acceptedEvidence` | Narrowly accepted proof, including transcript or artifact references. |
| `openGaps` | Unproven hardware, interaction, electrical, UI, protocol, and safety facts. |
| `closedSurfaces` | Explicit list of actions that remain unauthorized. |
| `nextAllowedAction` | Smallest safe next step, tier, owner, and validation. |
| `separateGates` | Lanes that require independent approval. |
| `reviewerQuorum` | Roles, weights, disposition, and P1/P2 blockers. |
| `validation` | Commands or evidence checks required before the packet is current. |

Current packet default:

| Field | Value |
| --- | --- |
| `schema` | `bench_state_packet.v1` |
| `claimedBenchPort` | COM6, latest read-only identity refreshed by `SRC-LOCAL-LCD-GLYPH-ELECTRICAL-ACCEPTANCE-2026-05-31`; further live work still requires a fresh Tier 3 boundary. |
| `currentFirmwareLane` | PF0530N LCD/menu scrolling/XML source/test update is current for development; PF0530L remains the latest flashed/accepted visual, serial/menu, glyph, and electrical evidence image. |
| `deviceIdentity` | Latest recorded COM6 proof: ESP32-D0WDQ6, MAC `<redacted-mac>`, 4 MB flash, 3.3 V strap. |
| `rollbackRecovery` | Last PF0530L rollback SHA256 `<redacted-sha256>`; refresh before flash. |
| `acceptedEvidence` | PF0530L write/verify/monitor proof, prior page/glyph auto-demo coverage, attended cursor/render/heartbeat proof, accepted serial/menu physical interaction proof, measured LCD high-side/LV-side voltage domain, post-reset LCD readiness/page/glyph serial proof, user-confirmed LCD visual/glyph readability, user-confirmed DMM continuity/toggle/current-margin pass for this gate, PF0530M non-live source/tests, PF0530N non-live XML/generator/scroll-list tests, XBee bridge narrow proof, ESP-NOW BBS accepted transcript lineage. |
| `openGaps` | PF0530N live runtime if later requested, physical readability of the PF0530N scroll-list/table page, direction-label expectation, final BBS/XBee payload mapping, relay identity/isolation/current, live SoftAP/browser, CBBS live acceptance, deployment readiness, publication. |
| `closedSurfaces` | Live hardware, flashing, serial writes/monitor, RF expansion, XBee setting writes, relay/load/mains, persistent config, credentials, destructive ops, external services, GitHub publication. |
| `nextAllowedAction` | Development work inside an explicitly named non-live boundary, or a fresh Tier 3 gate for any live device action. |

## Lane Router

| Lane | Current routing | Next safe action | Gate |
| --- | --- | --- | --- |
| COM6 identity/recovery | Latest read-only identity evidence exists from the LCD/electrical-domain attempt; rollback/recovery reference exists but recovery was not executed. | Refresh identity/recovery again before any new live gate. | Tier 3 before device access. |
| LCD/encoder/menu | PF0530L visual-test image is accepted for serial/menu interaction, readable rows/page changes/glyphs, and the closed LCD/DMM gate. PF0530N is current source/test-only scrolling/XML menu behavior work and has not been flashed. | Continue non-live menu/BBS payload development, or open a fresh Tier 3 gate for device action. | Separate COM6 Tier 3 for device access. |
| XBee/radio | Bridge and benign link proof accepted narrowly. | Offline protocol/profile planning or read-only evidence review. | Separate RF/serial gate. |
| Relay/power/load | Blocked. | Source-backed module identity and low-voltage evidence plan. | Separate hardware gate; load/mains stay blocked. |
| ESP-NOW/BBS/CBBS | ESP-NOW accepted by transcript lineage; CBBS must carry own proof. | Host-only mapping or evidence review. | Separate runtime/live gate. |
| SoftAP/browser mirror | Host-only/inert. | Host tests and threat model. | Separate network/security Tier 3. |
| DevEx/automation | Read-only panel profiles and audits. | Scaffold validation and dirty-tree stabilization. | Tier 2 records/tooling gate. |

## Prompt

```text
Apply the comprehensive ESP32 bench development process. Build or refresh a
bench_state_packet.v1 from source-indexed local records before proposing live
work. Keep LCD/encoder/UI intents separate from XBee, RF, relay, flash, serial
write, persistent config, SoftAP/browser, ESP-NOW/BBS/CBBS runtime, external
service, GitHub publication, and safety-critical actions. If live work is the
next step, stop at a Tier 3 gate request unless same-session identity, recovery
path, no-load safe state, explicit authority, and reviewer quorum are already
present.
```

## Validation

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/scaffold_audits -p 'test_*.py'`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `git diff --check`

## Stop Gates

This document does not authorize live hardware access, flashing, serial
writes, serial monitor, RF transmit, XBee setting writes, relay control,
persistent settings writes, credential access, destructive filesystem/device
operations, external service changes, GitHub publication, release gates,
framework changes beyond accepted ADRs, or action where device identity or
recovery path is not freshly proven.
