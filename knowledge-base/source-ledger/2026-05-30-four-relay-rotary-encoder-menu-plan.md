# Source Ledger - 2026-05-30 Four Relay Rotary Encoder Menu Plan

## Scope

Tier 1 documentation-only planning record for a future rotary encoder input on
the `four-relay-xbee-wifi` LCD menu path.

This record does not authorize wiring, firmware mutation, flashing, serial
monitoring, XBee/RF action, relay output work, relay/load/mains work, or live
encoder testing.

## Sources

- Accepted LCD display-status proof:
  `SRC-LOCAL-FOUR-RELAY-LCD-I2C-TEST-FIRMWARE-2026-05-30`.
- Accepted COM6 XBee bridge proof:
  `SRC-LOCAL-ESP32-XBEE-UART-BRIDGE-FLASH-RETEST-2026-05-30`.
- ESP32 GPIO, strapping, flash-related pin, and input-only pin context:
  `SRC-ESP-IDF-GPIO`.
- Current relay-candidate and photo-lineage context:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- Candidate/reference-only encoder family context: `SRC-BOURNS-PEC11R`.

## Verified Facts

- GPIO21/GPIO22 are kept reserved for the accepted LCD display-status path.
- GPIO17/GPIO16 are kept reserved for the accepted UART2 XBee bridge path.
- GPIO25, GPIO26, GPIO27, and GPIO33 remain relay candidates and are not
  consumed by this encoder plan.
- GPIO34 through GPIO39 are treated as input-only candidate-class pins when the
  exact board/shield exposes them.
- No final encoder GPIO assignment is accepted.
- No firmware interface, runtime behavior, or public API is changed by this
  record.
- No live bench, wiring, flash, serial, RF, relay, load, or mains action was
  performed.

## Assumptions

- The future encoder is for LCD menu navigation only.
- Future firmware should expose encoder activity as UI intents such as
  `rotate_left`, `rotate_right`, `select`, and optionally `long_press` or
  `back`.
- Selected hardware must remain in the ESP32 3.3 V logic domain.

## Unknowns

- Exact encoder part, module/bare form, pinout, PPR, detents, switch option,
  pullups, debounce behavior, voltage, ESD/noise needs, cable length, and
  mounting.
- Exact exposed header continuity and boot behavior for any future encoder
  candidate pins.
- Rail-current margin after the accepted LCD and XBee bridge paths plus future
  panel wiring.

## Owner and QA Lenses

- Hardware lens: approves the documentation-only plan because it preserves
  accepted LCD/XBee pins, avoids relay candidates, keeps final pin assignment
  unresolved, and requires 3.3 V pullup verification before wiring.
- Firmware lens: approves the interface boundary because future encoder events
  are UI intents only and cannot directly trigger relay, radio, flash, or
  persistent configuration paths.
- QA lens: approves the record because it separates verified facts,
  assumptions, and unknowns, cites existing sources, and leaves concrete stop
  gates before any live action.

Weighted Tier 1 local decision: approved for documentation-only mutation with
no live authority.

## Validation Plan

- Documentation/source audits.
- Agent-process audit.
- Scaffold verifier.
- `git diff --check`.

## Validation Results

Passed:

- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_docs.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_sources.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_agent_process.py`
- `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py`
- `git diff --check`

## Closed Surfaces

- No encoder GPIO implementation.
- No final pin assignment.
- No firmware mutation, build, flash, erase, monitor, serial write, RF test, or
  XBee setting write.
- No relay GPIO writes, relay expander outputs, relay command payloads,
  relay/load/mains action, or mains preparation.
- No claim that a selected encoder, module, pullup network, or boot behavior is
  electrically verified.
