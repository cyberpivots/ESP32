# Handoff 0078 - Multi-Agentic Continuous Enforcement To QA

## Current State

This task adds repo-local continuous weighted-agent enforcement. The important
behavior change is that missing evidence now routes to a next safe action when
possible:

- `continue` for automatable evidence collection or missing reviewer work.
- `ask_user` only for one irreducible physical fact the agent cannot observe.
- `blocked` for hard safety or authority boundaries.
- `ready_for_mutation` only after the named gate passes.

The implementation does not install `/etc/codex/requirements.toml`, enable
`admin-strict`, open serial ports, launch XCTU, read radios, write settings, or
touch hardware.

## Files To Review

- `scripts/agent_process_decision.py`
- `.codex/hooks.json`
- `.codex/hooks/user_prompt_submit_agent_process.py`
- `.codex/hooks/pre_tool_use_agent_process.py`
- `.codex/hooks/subagent_start_agent_process.py`
- `.codex/admin/hooks/esp32_admin_policy.py`
- `tests/scaffold_audits/test_agent_process_decision.py`
- `tests/scaffold_audits/test_agent_process_hooks.py`
- `tests/scaffold_audits/test_admin_policy_hooks.py`
- `tests/scaffold_audits/test_xbee_radio_study.py`
- `scripts/scaffold_audit_agent_process.py`

## QA Focus

- Confirm weighted votes pass only with required roles present, at least 70
  percent approval, no P1/P2 blockers, and all Tier 3 prerequisites.
- Confirm missing automatable evidence yields `continue`, while
  machine-unobservable physical facts yield `ask_user`.
- Confirm `bypassPermissions` remains non-blocking for PreToolUse,
  PermissionRequest, SubagentStop, and Stop.
- Confirm stop hooks do not permit a mutation summary to end with
  `Decision: continue`, `Decision: ready_for_mutation`, pending validation, or
  missing durable records.
- Confirm XBee boundaries remain unchanged: no `apply`, no write path, no XCTU
  launch, no all-port discovery, no serial open for no-serial commands, and
  read-only AT queries disjoint from write/setting commands.

## Still Blocked

Live XBee adapter identity, one-at-a-time physical disconnect/reconnect
mapping, Tier B radio readback, XCTU Discover/Add, setting writes, `WR`, `AC`,
API transmit, firmware recovery/update, range/throughput tests, ESP32 carrier
wiring, relay/load/mains work, and public raw identifiers remain blocked until
a future explicit Tier 3 gate records same-session physical evidence, recovery
path, cleanup criteria, and reviewer quorum.
