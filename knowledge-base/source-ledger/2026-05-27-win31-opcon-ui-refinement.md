# Win31 OPCON UI Refinement Source Ledger

Date: 2026-05-27

Source index ID: `SRC-LOCAL-WIN31-OPCON-UI-REFINEMENT-2026-05-27`

## Sources

- Local DOS-C source update:
  `/mnt/h/dos-c/software/win31-operator/src/operator.c`.
- Local DOS-C operator README update:
  `/mnt/h/dos-c/software/win31-operator/README.md`.
- Local ESP32 analyzer update:
  `scripts/win31_dashboard_legibility_analyzer.py`.
- Local ESP32 analyzer fixture test update:
  `tests/live_bench/test_win31_dashboard_legibility_analyzer.py`.
- Final copied live proof packet:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-27-win31-opcon-ui-refinement/live-ui-refinement-20260527T022745Z/`.
- Pi live proof packet:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-27-win31-opcon-ui-refinement/live-ui-refinement-20260527T022745Z/`.
- DOS-C task and handoff records:
  `/mnt/h/dos-c/.agents/tasks/0036-win31-opcon-ui-refinement.md` and
  `/mnt/h/dos-c/.agents/handoffs/0033-win31-opcon-ui-refinement-to-qa.md`.
- ESP32 task and handoff records:
  `.agents/TASK_LOG/0067-win31-opcon-ui-refinement.md` and
  `.agents/handoffs/0057-win31-opcon-ui-refinement-to-qa.md`.

## Verified Facts

- The accepted path remained:
  `OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.
- DOS-C source changed only the Win31 OPCON UI/layout behavior and README
  record; it did not change the bridge protocol, transport authority, firmware,
  PCAP, flashing, relay controls, or hardware authority.
- ESP32 source changed only the advisory analyzer and its fixture tests.
- `--visual-only` mode lets the ESP32 advisory analyzer run copied screenshot
  layout checks without DOS-C cleanup proof or `vision-gate.json`; without the
  flag, the analyzer still requires the existing vision-gate JSON.
- Final live screenshots covered Home, BBS, Downloads, Network, Peers, OTAP,
  Settings, Wizard, Diagnostics, and Safety at `1024x600`.
- Final visual-only analyzer result was `visual_only_pass`, target views
  `10/10`, capture size `1024x600`, lowest layout margins bottom `29 px` and
  right `15 px`, `console_fit_risk: 0`, `log_region_overflow: 0`, and
  `proof_capture_size_mismatch: 0`.
- The final proof intentionally left the dashboard open on the Pi with bridge
  PID `8182`, DOSBox-X PID `8184`, and listener `127.0.0.1:31332`.
- A stale quit-warning modal from the previous proof session was removed; the
  final open state had no `zenity` process.

## Assumptions

- The verified Pi display and X11 DOSBox-X mode from the fullscreen recovery
  task remained the active display path.
- Visual-only analyzer output is advisory and does not replace
  transcript-first DOS-C vision or ESP32 completion gates.

## Unknowns

- Human confirmation on the physical panel remains pending.
- DOS-C `win31_dashboard_vision_gate.py` was not run on the final packet
  because cleanup proof is intentionally deferred while the dashboard remains
  open.

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP, packet
driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT, MicroSD, load,
mains, erase, monitor, serial-write expansion, and Gate G export remain closed.
