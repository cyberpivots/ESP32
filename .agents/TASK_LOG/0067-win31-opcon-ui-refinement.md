# Task Log 0067 - Win31 OPCON UI Refinement

- ID: 0067-win31-opcon-ui-refinement
- Date: 2026-05-27
- Contract: `AGENTS.md`
- Status: fixed and left open for panel confirmation

## Goal

Record the ESP32-side advisory analyzer update and paired DOS-C live proof for
the Win31 OPCON UI refinement on the accepted serial-nullmodem path.

Accepted path:
`OPCON.EXE -> COM1 -> DOSBox-X nullmodem -> Pi bridge -> /dev/ttyUSB0 -> ESP32 coordinator`.

## Verified Facts

- DOS-C `software/win31-operator/src/operator.c` was refined to compute the
  Win31 dashboard layout, shorten crowded captions, remove the dithered
  viewfinder fill, move carousel arrows into the header, fit list/detail text,
  and open maximized.
- ESP32 `scripts/win31_dashboard_legibility_analyzer.py` now has opt-in
  `--visual-only` mode so copied live-open screenshots can be analyzed without
  requiring DOS-C cleanup proof or `vision-gate.json`.
- Existing analyzer behavior is unchanged without `--visual-only`; missing
  `vision-gate.json` still fails unless the flag is present.
- Final live proof packet:
  `/mnt/h/dos-c/artifacts/pi4-poe/integration/2026-05-27-win31-opcon-ui-refinement/live-ui-refinement-20260527T022745Z/`.
- Pi proof packet:
  `/home/dospi/dos-c/artifacts/pi4-poe/integration/2026-05-27-win31-opcon-ui-refinement/live-ui-refinement-20260527T022745Z/`.
- Rebuilt staged `OPCON.EXE` SHA-256:
  `68c803a553bac8ece52fa953046ebe97facfdbece10c6539edc98e83ad64a6b6`.
- Final proof screenshots are all `1024x600`: Home, BBS, Downloads, Network,
  Peers, OTAP, Settings, Wizard, Diagnostics, and Safety.
- ESP32 advisory visual-only analyzer result:
  `visual_only_pass`, target views `10/10`, capture size `1024x600`, lowest
  layout margin bottom `29 px` and right `15 px`, `console_fit_risk: 0`,
  `log_region_overflow: 0`, and `proof_capture_size_mismatch: 0`.
- Final open state intentionally leaves the refined dashboard visible with
  bridge PID `8182`, DOSBox-X PID `8184`, and listener `127.0.0.1:31332`.
- A stale quit-warning modal from the previous left-open DOSBox-X session was
  removed; final open state shows no `zenity` process.

## Screenshot Hashes

- `00-home.png`:
  `7f62eac423edb064e26fb22a258ab1760d66763bbd7f60a4040a055ff4487300`
- `01-bbs.png`:
  `2921dac949d9c694fcd665530a582f314d47a2df2a49da8dbf3173d39e7f62b9`
- `02-downloads.png`:
  `87a120b26cf99bedc4644c30f4568d259252c704d593335cb021596cc744ffd3`
- `03-network.png`:
  `c86fe4b53ed7d8afb2dad58ca2138a7e811b33d869b496fb6f425eb10056dc78`
- `04-peers.png`:
  `8afef492a12e4315a8b944bce977284ee9f07a0235204196ba5f3da08aafd3d7`
- `05-otap.png`:
  `b42b8d89a520affb47f5dfc8c70d36f34b81f1630203b6fc2c30e1655371eb93`
- `06-settings.png`:
  `b6209a1b82975c59b7946b0d278e473a15f9fee04d7b52a30525525503507d70`
- `07-wizard.png`:
  `8cbd8d715be5f37facaaa96a97a5bf8735f03a6bb98e52bdc9d41358fa9e0ce0`
- `08-diagnostics.png`:
  `9e36582661ed417f854bf17706c40f6c2d49b1235ba21a41d78b0b27024201a5`
- `09-safety.png`:
  `54793038b5589d53453d46e30a2a8b5a5ea771d8ce1cca909dca3d9c236dfcee`

## Assumptions

- The active Pi display remains the verified 1024x600 X11 DOSBox-X path from
  the fullscreen recovery task.
- Visual-only analysis is advisory and does not replace transcript-first
  completion gates.

## Unknowns

- Human usability confirmation on the physical panel is still pending.
- DOS-C `win31_dashboard_vision_gate.py` was not run against this packet
  because cleanup proof is intentionally deferred while the screen remains
  open.

## Validation

- PASS: `/mnt/h/dos-c` `bash tests/win31_operator/run_host_tests.sh`
- PASS: `/mnt/h/dos-c` `bash software/win31-operator/build-watcom.sh`
- PASS: `/mnt/h/dos-c` `python3 tests/test_win31_dashboard_vision_gate.py`
- PASS: `python3 tests/live_bench/test_win31_dashboard_legibility_analyzer.py`
- PASS: `python3 scripts/win31_dashboard_legibility_analyzer.py --visual-only ...`
  against the final live packet.

## Handoff

Continue with
[../handoffs/0057-win31-opcon-ui-refinement-to-qa.md](../handoffs/0057-win31-opcon-ui-refinement-to-qa.md).

## Closed Surfaces

Firmware flashing, prepare/flash/complete live-gate mutation, PCAP, packet
driver work, router/admin mutation, BLE, mesh, relay/XBee, TFT, MicroSD, load,
mains, erase, monitor, serial-write expansion, and Gate G export remain closed.
