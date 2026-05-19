# Bench Bring-Up Runbook

## Verified facts

- The current hardware set and its visible labels are recorded in the local
  photo ledger. Source ID: `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- ESP32 module and hardware-integration review must use Espressif sources.
  Source IDs: `SRC-ESP32-WROOM-32-DATASHEET`,
  `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.
- Relay component facts do not prove relay-module input behavior. Source ID:
  `SRC-SONGLE-SRD-05VDC-SL-C`.
- Waveshare documents the XBee USB Adapter as a USB/XBee UART communication
  board. Source ID: `SRC-WAVESHARE-XBEE-USB-ADAPTER`.
- CD74HC4067, TCA9555, MCP23017, and TPIC6B595 sources support the revised
  expansion proof sequence. Source IDs: `SRC-TI-CD74HC4067`,
  `SRC-TI-TCA9555`, `SRC-ESPRESSIF-MCP23017-COMPONENT`,
  `SRC-TI-TPIC6B595`.

## Assumptions

- This runbook is executed only by someone doing low-voltage bench inspection.
- Mains wiring, relay load wiring, relay switching, ESP32 flashing, and XBee
  setting writes are excluded.
- TFT wiring and expander-to-relay wiring are excluded until exact module and
  relay input evidence exists.
- A multimeter is available and the operator records each result before moving
  to the next stage.

## Unknowns

- Actual board/shield regulator behavior, rail tolerance, and jumper routing.
- Relay trigger polarity, input current, and 3.3 V compatibility.
- Waveshare adapter serial-port path, UART voltage, and DIN/DOUT direction.
- Open-Smart R61509V TFT identity, pinout, power/backlight, and touch behavior.
- Expander I2C address, pullups, inactive defaults, output latch behavior, and
  relay driver-stage fit.
- CD74HC4067 breakout wiring, ADC protection, and input-only scan behavior.

## Stage 1 - ESP32 board and expansion shield

Tools needed:

- Digital multimeter.
- USB data/power cable.
- Current-limited bench supply only if the shield source and input range have
  already been verified from inspection/source evidence.
- Notebook or bench log.

Power-off checks:

- Confirm no relay module or XBee adapter is connected to the ESP32/shield.
- Record shield jumper position, visible power labels, and selected single
  power source.
- Check resistance between `5V` and `GND`, then `3.3V` and `GND`; record the
  values and stop on a short or unstable reading.
- Continuity-check `GPIO25`, `GPIO26`, `GPIO27`, and `GPIO33` shield labels to
  the inserted ESP32 board header pins; record pass/fail for each candidate.

Expected measurement:

- No low-resistance short between power rails and ground.
- Each candidate GPIO label maps to one expected board pin with no adjacent-pin
  short.
- When powered from the selected single source, the `3.3V` rail measures within
  the board/source-backed expected range and remains stable while idle.

Pass result:

- Board/shield identity and power/routing evidence can be added to the hardware
  profile and the relay stage may remain a documentation target.

Fail result:

- Board/shield use stays blocked; do not connect relay inputs or XBee signals.

Stop condition:

- Stop immediately for rail shorts, heat, unstable voltage, dual-power
  ambiguity, unexpected boot mode, wrong GPIO continuity, or missing source for
  the selected power input.

## Stage 2 - Four-channel relay module, contacts disconnected

Tools needed:

- Digital multimeter.
- Current-limited 5 V supply only after the relay module supply pins are
  identified.
- Inline current measurement method or meter current range suitable for the
  expected input current.
- Low-voltage signal source for 3.3 V tests only after the module supply path is
  understood.
- Notebook or bench log.

Power-off checks:

- Confirm all relay screw terminals are empty or attached only to an approved
  low-voltage dummy load.
- Inspect and photograph relay input labels, `JD-VCC`/`VCC` jumper state, and
  visible isolation components.
- Check for unintended continuity between input ground, relay supply ground,
  and contact terminals; record results without claiming isolation until the
  schematic or measurements support it.

Expected measurement:

- Relay input polarity is identified from exact-module source evidence or by a
  controlled low-voltage measurement.
- Input current per channel is recorded.
- 3.3 V input behavior is recorded without exceeding the source-backed ESP32
  GPIO current gate.
- `JD-VCC`/`VCC` behavior is recorded as common-supply, split-supply, or still
  unresolved.

Pass result:

- Direct GPIO drive may be proposed only after measured 3.3 V behavior and
  current draw pass the documented gate and owner review records the evidence.

Fail result:

- Direct GPIO drive is blocked and the next design must use a driver-stage
  plan before any relay wiring.

Stop condition:

- Stop for unclear supply pins, unclear jumper behavior, unexpected relay
  actuation, input current above the selected source-backed GPIO gate, heat,
  smoke, arcing, or any mains/load wiring.

## Stage 3 - Waveshare XBee USB Adapter read-only discovery

Tools needed:

- PC with USB port.
- USB cable.
- Serial-port listing tool or Digi read-only discovery tool.
- Digital multimeter for adapter header voltage checks.
- Notebook or bench log.
- Optional local probe script:
  `python3 scripts/xbee_read_only_probe.py`.

Power-off checks:

- Confirm the adapter is not connected to ESP32 GPIO.
- Inspect and record adapter revision markings, socket orientation, antenna
  connection, and header labels.
- Confirm the XBee radio is seated correctly before USB connection.

Expected measurement:

- Host OS reports a serial device for the adapter.
- Adapter power/header voltage readings are recorded without connecting those
  headers to the ESP32.
- Read-only identity confirms or rejects the expected Digi
  `XBP9B-DPUT-001 RevF` target.
- Tier A passive discovery records serial candidates, adapter inspection, header
  voltage, and optional read-only byte observation without serial writes.
- Tier B read-query discovery is run only with
  `--confirm-sends-read-commands`; it sends the command-mode guard sequence and
  only fixed reads for `VR`, `HV`, `SH`, `SL`, `AP`, `AO`, `BD`, and `NP`.

Pass result:

- The adapter remains approved only as a PC dock for read-only discovery.
- Tier B results may be used as a current-settings readback record only; they
  do not authorize setting writes, API transmit frames, relay commands, or ESP32
  carrier wiring.

Fail result:

- XBee work stays blocked until serial driver, power, seating, or tool issues
  are resolved.

Stop condition:

- Stop if the tool prompts for setting writes, the serial device is unstable,
  adapter voltage is unclear, the radio heats unexpectedly, or anyone proposes
  ESP32 DIN/DOUT wiring before carrier review.
- Stop if `WR`, `AC`, parameter writes, firmware updates, API transmit frames,
  relay commands, adapter/radio setting changes, or unredacted public serial
  address publication are introduced.

## Stage 4 - Mains-readiness review only

Tools needed:

- None for DIY bench wiring; this is a documentation gate only.
- Qualified electrical review is required before any mains design moves
  forward.

Power-off checks:

- Confirm no mains conductors, loads, or plugs are attached to relay contacts.
- Confirm the prototype remains low-voltage or disconnected at relay contacts.

Expected measurement:

- No mains measurement is performed in this runbook.
- A future review package must identify load type, enclosure, overcurrent
  protection, grounding/bonding, strain relief, GFCI/de-energization process,
  and applicable source/code evidence.

Pass result:

- None in this runbook; mains remains blocked until a separate qualified review
  package is accepted.

Fail result:

- Any request to wire mains from this runbook is a hard stop.

Stop condition:

- Stop if mains wiring, live-load switching, or relay-contact energization is
  introduced.

## Expansion Proof Addendum - TFT, mux, and relay expander

Tools needed:

- Digital multimeter.
- Current-limited low-voltage logic supply after the exact expander or mux board
  power path is known.
- LEDs with suitable current limiting or a logic analyzer for expander outputs.
- ADC1 test-voltage source for mux input proof.
- Notebook or bench log.

Power-off checks:

- Confirm relay module inputs, relay coils, relay contacts, TFT module, and XBee
  carrier wiring are disconnected from the expansion proof.
- Record exact CD74HC4067 breakout, address/enable pins, signal pin, and power
  rail.
- Record exact MCP23017 or TCA9555 expander board, address pins, pullups, reset
  pin behavior, and power rail.
- Record the Open-Smart R61509V module only as an inspection target until exact
  pinout and power evidence exist.

Expected measurement:

- CD74HC4067 selects one low-voltage input at a time into an ADC1 test path and
  does not connect to relay outputs.
- Expander I2C address is detected, all expander outputs default inactive, and
  commanded output states remain latched on LEDs or a logic analyzer during
  unrelated mux scans.
- TFT pin-conflict notes identify bus width, control pins, touch pins, power,
  backlight, boot-pin, flash-pin, UART0, MicroSD, XBee, and relay conflicts
  before any wiring.

Pass result:

- The expansion branch may move to firmware-interface planning with
  `relay_expander` and `mux_scan` tasks. Relay-module input wiring remains
  blocked.

Fail result:

- Keep `hardwareGateClosed=false`; do not accept relay commands through the
  expander branch.

Stop condition:

- Stop if the mux is proposed as relay output state holding.
- Stop if expander outputs are connected to relay-module inputs before exact
  relay trigger polarity, input current, logic voltage, and isolation behavior
  are verified.
- Stop if TFT wiring would consume boot, flash, UART0, XBee, MicroSD, or relay
  pins before the conflict review is complete.
