# OPCON Visible States

Required visible corroboration:

- OPCON splash or dashboard
- Peers view
- Message Board view
- Downloads view
- Network view
- OTAP view
- Diagnostics and Safety views, or a combined Diagnostics/Safety capture
- disabled unsafe controls for relay, flash, serial write, and PCAP
- Program Manager dashboard item when that capture is present

Required transcript corroboration:

- three peers named or identified as `peer01`, `peer02`, and `peer03`
- each peer has `link=espnow-enc`
- `download_list`, `download_status`, `otap_status`, and non-executing `otap_intent` appear in the bridge transcript
- serial error count is zero
- RX, TX, and ACK counters move between samples
