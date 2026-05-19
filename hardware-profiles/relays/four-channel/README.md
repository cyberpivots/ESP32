# Four-Channel Relay Board

## Status

Verification-only profile. The photo archive identifies the board as a blue
`4 Relay Module` populated with Songle `SRD-05VDC-SL-C` relay cans, but exact
board electrical behavior is still unresolved before wiring, firmware relay
polarity, current budget, isolation claims, or load-switching claims.

## Verified facts

- The photo archive shows a blue board labeled `4 Relay Module` with four
  relay channels and visible input/terminal areas. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- The photo archive shows relay cans marked `SRD-05VDC-SL-C`. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- The Songle `SRD-05VDC-SL-C` datasheet mirror provides relay component
  ordering and contact-rating context. Source ID:
  `SRC-SONGLE-SRD-05VDC-SL-C`.
- The photo archive shows a `JD-VCC`/`VCC` area on the relay module, but the
  jumper function and isolation behavior are not proven. Source ID:
  `SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`.
- The ESP32 direct-drive decision must use an ESP32 source-backed GPIO/current
  gate and measured relay input behavior, not relay-can markings alone. Source
  IDs: `SRC-ESP32-WROOM-32-DATASHEET`,
  `SRC-ESP32-HARDWARE-DESIGN-GUIDELINES`.
- TCA9555 and MCP23017 are source-backed relay-output expansion candidates, and
  TPIC6B595 is a relay-driver reference. Source IDs: `SRC-TI-TCA9555`,
  `SRC-ESPRESSIF-MCP23017-COMPONENT`, `SRC-TI-TPIC6B595`.
- CD74HC4067 is source-backed as an analog mux/demux and is rejected for direct
  relay output state holding. Source ID: `SRC-TI-CD74HC4067`.

## Assumptions

- The first bench proof should use disconnected relay outputs or low-voltage
  dummy loads until load safety is reviewed.
- Firmware must treat trigger polarity as a configuration item until the board
  is identified and tested.
- Relay pin relief should use a latched expander plus verified driver stage when
  TFT pin pressure is active.

## Required verification checklist

| Item | Required evidence before use |
| --- | --- |
| Board manufacturer and model | Purchase link, schematic, or product page for the exact four-channel module. |
| Input logic voltage | Source or measurement showing compatible trigger input voltage. |
| Trigger polarity | Source or measurement showing active-high or active-low behavior. |
| Input current | Source or measurement for each relay input. |
| Relay supply path | Source or measurement showing `JD-VCC`/`VCC` jumper behavior and coil/logic supply relationship. |
| Isolation method | Schematic/source or inspection showing optocoupler, jumper, ground, and relay-side isolation behavior. |
| Load rating | Source-backed module and relay contact rating for the intended voltage/current/load type. |
| Protection design | Flyback, snubber, MOV, fuse, enclosure, and grounding review for the intended load. |
| Expander/driver interface | Source or measurement showing the expander plus driver stage can present the required inactive and active relay-input behavior without defeating isolation. |

## Direct GPIO drive gate

Direct wiring from ESP32 `GPIO25`, `GPIO26`, `GPIO27`, or `GPIO33` to relay
inputs is blocked until these closure records exist:

| Item | Closure evidence |
| --- | --- |
| Shield routing | Continuity record from each shield label to the expected ESP32 pin. |
| Trigger polarity | Exact-module source or controlled measurement proving active-high or active-low behavior. |
| Input current | Measured or source-backed current per input channel. |
| 3.3 V compatibility | Measured relay input behavior that stays within the selected ESP32 source-backed GPIO current gate. |
| `JD-VCC`/`VCC` behavior | Source, schematic, or measurement showing coil/logic supply relationship and whether isolation is preserved. |

If the 3.3 V/current gate fails, this profile requires a future driver-stage
design before relay wiring.

## Expander Relay Gate

The preferred expansion architecture is:

```text
ESP32 I2C -> MCP23017 or TCA9555 -> verified driver stage -> relay module inputs
```

This path is still blocked for relay-module connection until these closure
records exist:

| Item | Closure evidence |
| --- | --- |
| Expander board | Exact source/schematic, I2C address pins, pullups, reset/default behavior, and power rail. |
| Inactive defaults | LED or logic-analyzer proof that outputs initialize inactive before relay commands are accepted. |
| Latch behavior | Proof that unrelated TFT, mux, storage, or XBee activity does not glitch outputs. |
| Driver stage | Exact driver selection after relay trigger polarity, input current, voltage, and isolation are verified. |
| Fault behavior | Expander init/write/readback failure sets `hardwareGateClosed=false` and returns `hardware_gate_open`. |

## Project placeholder

| Channel | Provisional ESP32 GPIO | Status |
| --- | --- | --- |
| 1 | GPIO25 | Visible shield-label candidate; blocked on relay board and shield verification |
| 2 | GPIO26 | Visible shield-label candidate; blocked on relay board and shield verification |
| 3 | GPIO27 | Visible shield-label candidate; blocked on relay board and shield verification |
| 4 | GPIO33 | Visible shield-label candidate; blocked on relay board and shield verification |
| 1-4 | MCP23017 or TCA9555 outputs | Preferred pin-relief branch; LED/logic-analyzer proof first, relay inputs blocked |

Source IDs for the provisional ESP32 side:
`SRC-LOCAL-ESP32PROJECT-PHOTOS-2026-05-18`,
`SRC-ESP32-WROOM-32-DATASHEET`, `SRC-ESP-IDF-GPIO`.

## Unknowns

- Exact four-channel relay module manufacturer/model.
- Whether the board is active-high or active-low.
- Whether the board can be driven directly from ESP32 GPIO.
- Relay input current per channel.
- Coil supply requirement, current draw, and `JD-VCC`/`VCC` behavior.
- Whether opto-isolation is present and how it is powered or defeated by
  jumpers.
- Contact ratings for the intended load.
- Whether the intended load is mains, DC, inductive, capacitive, or resistive.
- Whether any future load can satisfy the project mains-readiness gate.
- Exact relay expander and driver-stage selection.
- Whether direct GPIO remains useful after the Open-Smart R61509V TFT pin plan is
  verified.
