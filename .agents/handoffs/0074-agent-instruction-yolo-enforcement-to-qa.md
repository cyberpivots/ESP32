# Handoff 0074: Agent Instruction Yolo Enforcement To QA

## Summary

Yolo/operator-sovereignty enforcement was moved into repo-local instruction
surfaces. `AGENTS.md` is explicit about the boundary, and every
`.codex/agents/*.toml` developer-instruction profile now inherits the rule.

## QA Focus

1. Verify each `.codex/agents/*.toml` profile includes the operator-sovereignty
   instruction markers.
2. Verify `scripts/scaffold_audit_agent_process.py` fails if any agent profile
   omits the rule.
3. Verify `/etc/codex/requirements.toml` remains absent unless the user
   explicitly requests the `admin-strict` profile by name.
4. Re-run the scaffold and admin hook tests after Codex upgrades.

## Closed Surfaces

This handoff does not authorize firmware/runtime/API/ABI/framework changes,
flashing, erase, monitor, serial-write expansion, BLE/live mesh, PCAP,
router/admin mutation, relay, XBee, TFT, MicroSD, load, mains, wiring, release
gates, or live bench work.
