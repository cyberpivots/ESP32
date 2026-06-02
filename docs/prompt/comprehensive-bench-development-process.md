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
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530N-LIVE-2026-06-01`,
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530O-REAL-MENU-CAL-2026-06-01`,
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530O-LIVE-2026-06-01`,
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530P-DEBOUNCE-CAL-2026-06-01`,
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530P-LIVE-2026-06-01`,
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530Q-QUIET-CAL-2026-06-01`,
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530Q-LIVE-2026-06-01`,
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530R-DETENT-CAL-2026-06-01`,
`SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530R-LIVE-2026-06-01`,
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

- The latest recorded COM6 LCD/menu live gate is PF0530W. PF0530W is written
  and separately verify-flashed with readiness proof while preserving the
  PF0530V PCNT encoder baseline; physical ART-page visual acceptance remains
  open.
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
- PF0530N added LCD/menu scrolling/XML source/test behavior and was later
  written, verify-flashed, and read-only monitored on COM6 with runtime LCD
  readiness/render proof but no accepted physical readability or input proof.
- PF0530O is the prior flashed real-menu calibration image. It keeps the closed
  bridge and input-only/display-only boundaries, changes the active firmware ID
  to `PF0530O`, uses one transition per menu step, two AB stable samples, a
  75 ms switch guard, a 650 ms long press, disables boot auto-cycle, and reports
  `cal=real-menu-v1`. PF0530O write-flash and separate verify-flash passed on
  COM6; reset and attended read-only monitors proved LCD readiness/render/
  heartbeat output with zero crash/unsafe markers, but captured zero input
  events.
- PF0530P is the flashed debounce calibration image.
  It keeps the closed bridge and input-only/display-only boundaries, changes
  the active firmware ID to `PF0530P`, keeps one transition per menu step and
  two AB stable samples, adds a 5 ms A/B candidate hold and a 40 ms step
  lockout, and reports `cal=debounce-v2 ab_ms=5 step_lockout_ms=40`. PF0530P
  write-flash and separate verify-flash passed on COM6; reset and attended
  read-only monitors proved LCD readiness/render/heartbeat output with zero
  crash/unsafe markers, but captured zero input events. The user later
  clarified that they did not rotate during that monitor, so the zero-input
  transcript is not diagnostic of debounce behavior.
- PF0530Q is the previous flashed quiet-window calibration image.
  It keeps the closed bridge and input-only/display-only boundaries, changes
  the active firmware ID to `PF0530Q`, keeps one transition per menu step, two
  AB stable samples, a 5 ms A/B candidate hold, 30 ms switch debounce, a 75 ms
  switch guard, and a 650 ms long press, adds a 10 ms combined A/B pair quiet
  window, raises step lockout to 60 ms, and reports
  `cal=quiet-v3 ab_ms=5 quiet_ms=10 step_lockout_ms=60`. PF0530Q write-flash
  and separate verify-flash passed on COM6; reset and idle read-only monitors
  proved LCD readiness/render/heartbeat output with zero crash/unsafe markers,
  but physical behavior was not accepted by monitor because no actuation
  occurred. The later user report says PF0530Q works but is not stable.
- PF0530R is a recorded written detent-gated calibration image in the lineage.
  It keeps the closed bridge and input-only/display-only boundaries, changes
  the active firmware ID to `PF0530R`, raises A/B candidate hold to 8 ms,
  raises combined A/B quiet time to 15 ms, changes
  `FR_ENCODER_TRANSITIONS_PER_STEP` to 2, raises step lockout to 90 ms, emits
  at most one menu step only when accepted quadrature returns to detent A/B
  `3`, and reports
  `cal=detent-v4 ab_ms=8 quiet_ms=15 step_lockout_ms=90 detent=3`. PF0530R
  write-flash and separate verify-flash passed on COM6; reset and attended
  read-only monitors proved LCD readiness/render/heartbeat output with zero
  crash/unsafe markers and zero bad render rows. The monitor captured zero
  input events, so physical behavior is not accepted by transcript.
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

- PF0530O user visual report, physical LCD readability, encoder direction,
  one-detent behavior, quick-rotation behavior, short-button behavior, and
  long-button behavior are not accepted.
- Relay module identity, final BBS/XBee payload display mapping, and live
  SoftAP/browser behavior are not accepted.
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
| `claimedBenchPort` | COM6, latest read-only identity refreshed by `SRC-LOCAL-FOUR-RELAY-KY040-BBS-LCD-MENU-PF0530W-LIVE-2026-06-02`; further live work still requires a fresh Tier 3 boundary. |
| `currentFirmwareLane` | PF0530W visual-art continuation is the current written/verify-flashed COM6 image, with read-only LCD readiness/render proof and preserved PF0530V PCNT encoder baseline. PF0530V remains the user-accepted real LCD menu encoder baseline. PF0530L remains the latest accepted visual, serial/menu, glyph, and electrical evidence image. |
| `deviceIdentity` | Latest recorded COM6 proof: ESP32-D0WDQ6, MAC `<redacted-mac>`, 4 MB flash, 3.3 V strap. |
| `rollbackRecovery` | Latest PF0530W rollback backup and private hashes retained only in ignored local evidence; refresh before any future flash. |
| `acceptedEvidence` | PF0530L write/verify/monitor proof, prior page/glyph auto-demo coverage, attended cursor/render/heartbeat proof, accepted serial/menu physical interaction proof, measured LCD high-side/LV-side voltage domain, post-reset LCD readiness/page/glyph serial proof, user-confirmed LCD visual/glyph readability, user-confirmed DMM continuity/toggle/current-margin pass for that gate, PF0530M non-live source/tests, PF0530N XML/generator/scroll-list tests and COM6 LCD readiness/render proof, PF0530O write/verify/read-only LCD readiness/render/heartbeat proof, PF0530P source/build calibration proof, PF0530P write/verify/read-only LCD readiness/render proof, PF0530Q source/build quiet-window calibration proof, PF0530Q write/verify/read-only LCD readiness/render proof, PF0530R source/build detent calibration proof, PF0530R write/verify/readiness proof, PF0530V PCNT source/build/live proof and user-accepted encoder functionality, PF0530W visual-art source/build/live readiness proof, XBee bridge narrow proof, ESP-NOW BBS accepted transcript lineage. |
| `openGaps` | PF0530W physical ART-page visual acceptance, final BBS/XBee payload mapping, relay identity/isolation/current, live SoftAP/browser, CBBS live acceptance, deployment readiness, publication. |
| `closedSurfaces` | Live hardware, flashing, serial writes/monitor, RF expansion, XBee setting writes, relay/load/mains, persistent config, credentials, destructive ops, external services, GitHub publication. |
| `nextAllowedAction` | User visual/input report, development work inside an explicitly named non-live boundary, or a fresh Tier 3 gate for any live device action. |

## Lane Router

| Lane | Current routing | Next safe action | Gate |
| --- | --- | --- | --- |
| COM6 identity/recovery | Latest read-only identity evidence exists from the LCD/electrical-domain attempt; rollback/recovery reference exists but recovery was not executed. | Refresh identity/recovery again before any new live gate. | Tier 3 before device access. |
| LCD/encoder/menu | PF0530W is the current written/verify-flashed visual-art image with COM6 read-only readiness/render proof and preserved PF0530V PCNT input. PF0530V is the accepted real LCD menu encoder baseline. PF0530L remains accepted for serial/menu interaction, readable rows/page changes/glyphs, and the closed LCD/DMM gate. | Collect operator visual report on the PF0530W ART page or run a read-only interaction monitor with confirmed actuation. | Separate COM6 Tier 3 for future flash or broader device access. |
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
