# Workspace Review Command Matrix

This matrix classifies commands by side-effect class for future review gates.
It is planning guidance, not authority to run any command.

| Command or surface | Class | Gate note |
| --- | --- | --- |
| `git status --short --branch --untracked-files=all` | read-only | Safe preflight. |
| `git diff --check` | read-only | Safe whitespace validation. |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/verify_scaffold.py` | read-only | Full scaffold audit; may read many repo files. |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_records.py --min-task-id N` | read-only | Durable-record audit. |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/scaffold_audit_react_native.py` | read-only | Rejects generated RNW output and checks local records. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/custom_wireless_protocol -p 'test_*.py'` | read-only | Host-only protocol tests. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/lcd_bbs_menu -p 'test_*.py'` | read-only | Host-only LCD simulator tests. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/rnw_menu -p 'test_*.py'` | read-only | Host-only RNW menu generator tests. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/esp32_gateway_tcp -p 'test_*.py'` | read-only | Host-only TCP simulator tests. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/live_bench -p 'test_*.py'` | read-only | Unit tests only; not a live-bench run. |
| `python3 tests/four_relay_safe_core/run_host_tests.py` | temp-mutating | Builds C host-test artifacts in temporary paths. |
| `pnpm install --frozen-lockfile` | temp-mutating | Installs dependencies into workspace state; no lockfile mutation expected. |
| `pnpm lint`, `pnpm typecheck`, `pnpm test` | read-only/temp-mutating | May write cache output; no source mutation expected. |
| `python3 scripts/build_github_pages.py --out build/github-pages` | repo-mutating generated output | Writes generated public artifact under `build/`. |
| `python3 scripts/audit_public_manifest.py` | read-only | Reads generated Pages artifact. |
| `python3 scripts/smoke_github_pages.py` | read-only/temp-mutating | May start a local static server only through explicit script behavior. |
| `scripts/live_bench_preflight.py` | live/device-adjacent read-only | Requires explicit live-gate routing before use against devices. |
| `scripts/espnow_bbs_live_gate.py prepare` | live/device backup manifest gate | Requires Tier 3 same-session evidence and explicit authority. |
| `scripts/espnow_bbs_live_gate.py flash` | live/device write gate | Requires Tier 3 same-session evidence, rollback, and explicit authority. |
| `scripts/espnow_bbs_live_gate.py complete` | live/device completion gate | Requires accepted proof packet and cleanup evidence. |
| `xbee_read_only_probe.py --confirm-sends-read-commands` | live/serial read gate | Opens serial and sends read commands; explicit authority required. |
| XBee `WR`, `AC`, `KY`, profile writes, API transmit | live/RF write gate | Tier 3; currently blocked. |
| RNW `run-windows`, `msbuild`, package install, signing, Store/App Installer | release/runtime gate | Closed unless a separate gate explicitly opens it. |
| `git commit`, `git push`, PR, tag, deploy, release | publication gate | Requires publication hygiene plus explicit user authority. |
| `git reset --hard`, destructive checkout/clean | destructive | Do not run unless explicitly requested. |
