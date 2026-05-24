# Live Completion Evidence

Required inputs for `scripts/espnow_bbs_live_gate.py complete`:

- private prepare manifest from `prepare`
- private flash evidence from `flash`
- bridge JSON transcript copied from the Pi runtime proof
- cleanup proof copied from the Pi runtime proof
- DOS-C `scripts/win31_dashboard_vision_gate.py` JSON output

Acceptance shape:

- manifest records coordinator, `peer01`, `peer02`, and `peer03`
- flash evidence reports write and verify success for all four roles
- transcript proves `hello`, `state_get`, `peer_list`, `diag_get`, `fw_inventory`, `msg_post`, `msg_pull`, `msg_search`, and `msg_ack`
- transcript reports three `espnow-enc` peers, zero serial errors, and moving RX/TX/ACK counters
- vision-gate output passes required visible views and disabled unsafe controls
- cleanup proof shows no DOSBox-X, modal/zenity, bridge process, or `31331`/`31332`/`8080` listener
