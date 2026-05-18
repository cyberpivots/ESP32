const endpoints = {
  state: "/api/state",
  relay: (channel) => `/api/relay/${channel}`,
  allOff: "/api/all-off",
  safetyLock: "/api/safety-lock",
  storage: "/api/storage/status",
  manifest: "/api/assets/manifest",
  logs: (limit = 50, type = "all") =>
    `/api/logs/recent?limit=${encodeURIComponent(limit)}&type=${encodeURIComponent(type)}`,
};

const relayLabelStorageKey = "esp32.relayLabels.v1";
const maxRelayLabelLength = 32;
const defaultRelayChannels = [
  {
    channel: 1,
    label: "Output A",
    pin: "GPIO25",
  },
  {
    channel: 2,
    label: "Output B",
    pin: "GPIO26",
  },
  {
    channel: 3,
    label: "Output C",
    pin: "GPIO27",
  },
  {
    channel: 4,
    label: "Output D",
    pin: "GPIO33",
  },
];

const assetManifest = {
  name: "four-relay-admin-hmi",
  version: "2026-05-18-admin-hmi",
  files: ["index.html", "styles.css", "app.js", "manifest.json"],
  generatedAt: "2026-05-18",
  assetRoot: "/sdcard/www",
};

const baseState = {
  deviceId: "bench-four-relay-01",
  uptimeMs: 0,
  safetyLocked: true,
  adminProvisioned: false,
  hardwareGateClosed: false,
  xbee: {
    configured: false,
    link: "unknown",
    lastStatus: "none",
    allowlist: "missing",
    lastFrame: "none",
    telemetry: "idle",
  },
  storage: {
    mounted: true,
    mode: "sdcard",
    cardType: "SDHC",
    capacityBytes: 31_914_983_424,
    freeBytes: 28_000_000_000,
    assetRoot: "/sdcard/www",
    assetVersion: assetManifest.version,
    manifestReadable: true,
    logRoot: "/sdcard/logs",
    logWritable: true,
    lastLogWrite: "2026-05-18T12:00:00Z",
    fallbackActive: false,
  },
  relays: [
    { channel: 1, label: "Output A", pin: "GPIO25", state: false, enabled: false },
    { channel: 2, label: "Output B", pin: "GPIO26", state: false, enabled: false },
    { channel: 3, label: "Output C", pin: "GPIO27", state: false, enabled: false },
    { channel: 4, label: "Output D", pin: "GPIO33", state: false, enabled: false },
  ],
  lastCommand: {
    source: "boot",
    sequence: 0,
    result: "safe_default",
  },
  config: {
    safety: "pending",
    relayPolarity: "unverified",
    allowlist: "missing",
  },
};

const commonLogs = [
  {
    time: "2026-05-18T12:00:00Z",
    type: "storage",
    severity: "info",
    source: "boot",
    message: "MicroSD mounted and manifest loaded",
    result: "mounted",
  },
  {
    time: "2026-05-18T12:00:02Z",
    type: "safety",
    severity: "warn",
    source: "boot",
    message: "Safety lock closed on boot",
    result: "safe_default",
  },
  {
    time: "2026-05-18T12:00:03Z",
    type: "rejected",
    severity: "warn",
    source: "http",
    message: "Relay command rejected",
    channel: 1,
    result: "admin_required",
  },
  {
    time: "2026-05-18T12:00:04Z",
    type: "xbee",
    severity: "info",
    source: "xbee",
    message: "Radio link not configured",
    result: "unconfigured",
  },
];

const mockScenarios = {
  mounted: {
    label: "SD mounted",
    state: baseState,
    manifest: assetManifest,
    logs: commonLogs,
  },
  missing: {
    label: "SD missing",
    state: {
      ...baseState,
      storage: {
        ...baseState.storage,
        mounted: false,
        mode: "fallback",
        cardType: "missing",
        capacityBytes: 0,
        freeBytes: 0,
        assetVersion: "fallback",
        manifestReadable: false,
        logWritable: false,
        lastLogWrite: "none",
        fallbackActive: true,
      },
    },
    manifest: { ...assetManifest, version: "fallback", files: [] },
    logs: [
      {
        time: "2026-05-18T12:00:00Z",
        type: "storage",
        severity: "error",
        source: "boot",
        message: "MicroSD mount failed",
        result: "card_missing",
      },
      ...commonLogs.slice(1),
    ],
  },
  readonly: {
    label: "SD read-only",
    state: {
      ...baseState,
      storage: {
        ...baseState.storage,
        mode: "sdcard_readonly",
        freeBytes: 18_000_000_000,
        logWritable: false,
        lastLogWrite: "write_error",
        fallbackActive: false,
      },
      lastCommand: {
        source: "logger",
        sequence: 4,
        result: "log_append_failed",
      },
    },
    manifest: assetManifest,
    logs: [
      {
        time: "2026-05-18T12:00:05Z",
        type: "storage",
        severity: "error",
        source: "logger",
        message: "Event log append failed",
        result: "log_append_failed",
      },
      ...commonLogs,
    ],
  },
  empty: {
    label: "Empty logs",
    state: {
      ...baseState,
      storage: {
        ...baseState.storage,
        lastLogWrite: "none",
      },
    },
    manifest: assetManifest,
    logs: [],
  },
  lowspace: {
    label: "Low space",
    state: {
      ...baseState,
      storage: {
        ...baseState.storage,
        freeBytes: 2_097_152,
        logWritable: true,
        lastLogWrite: "2026-05-18T12:05:00Z",
      },
      lastCommand: {
        source: "storage",
        sequence: 5,
        result: "low_space",
      },
    },
    manifest: assetManifest,
    logs: [
      {
        time: "2026-05-18T12:05:00Z",
        type: "storage",
        severity: "warn",
        source: "storage",
        message: "MicroSD free space below warning threshold",
        result: "low_space",
      },
      ...commonLogs,
    ],
  },
};

const staticDemoMode = window.location.hostname.endsWith(".github.io");
const prototypeMode =
  window.location.protocol === "file:" ||
  ["127.0.0.1", "localhost", "::1", ""].includes(window.location.hostname) ||
  staticDemoMode;

let currentScenario = "mounted";
let state = clone(mockScenarios[currentScenario].state);
let manifest = clone(mockScenarios[currentScenario].manifest);
let logs = clone(mockScenarios[currentScenario].logs);
let currentFilter = "all";
let sequence = 1;
let readOnlyApiStatus = {
  storage: "ok",
  manifest: "ok",
  logs: "ok",
};
let savedRelayLabels = readSavedRelayLabels();

const els = {
  deviceId: document.querySelector("#deviceId"),
  safetyBadge: document.querySelector("#safetyBadge"),
  gateBadge: document.querySelector("#gateBadge"),
  storageBadge: document.querySelector("#storageBadge"),
  xbeeBadge: document.querySelector("#xbeeBadge"),
  adminBadge: document.querySelector("#adminBadge"),
  relayGrid: document.querySelector("#relayGrid"),
  allOffButton: document.querySelector("#allOffButton"),
  lockButton: document.querySelector("#lockButton"),
  controlGateText: document.querySelector("#controlGateText"),
  safetySummary: document.querySelector("#safetySummary"),
  storageSummary: document.querySelector("#storageSummary"),
  xbeeSummary: document.querySelector("#xbeeSummary"),
  logsSummary: document.querySelector("#logsSummary"),
  configSummary: document.querySelector("#configSummary"),
  message: document.querySelector("#message"),
  logList: document.querySelector("#logList"),
  relayLabelEditor: document.querySelector("#relayLabelEditor"),
  resetLabelsButton: document.querySelector("#resetLabelsButton"),
  scenarioControl: document.querySelector("#scenarioControl"),
  mockScenarioSelect: document.querySelector("#mockScenarioSelect"),
};

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function normalizeRelayLabel(value) {
  return String(value || "")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, maxRelayLabelLength);
}

function readSavedRelayLabels() {
  try {
    const raw = window.localStorage.getItem(relayLabelStorageKey);
    const parsed = raw ? JSON.parse(raw) : {};
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
      return {};
    }
    return Object.fromEntries(
      Object.entries(parsed)
        .map(([channel, label]) => [String(Number(channel)), normalizeRelayLabel(label)])
        .filter(([channel, label]) => channel !== "NaN" && label)
    );
  } catch (_error) {
    return {};
  }
}

function writeSavedRelayLabels() {
  try {
    window.localStorage.setItem(
      relayLabelStorageKey,
      JSON.stringify(savedRelayLabels),
    );
  } catch (_error) {
    return;
  }
}

function defaultRelayForChannel(channel) {
  return (
    defaultRelayChannels.find((item) => Number(item.channel) === Number(channel)) ||
    { channel, label: `Output ${channel}`, pin: "GPIO unresolved" }
  );
}

function relayLabel(relay) {
  const fallback = defaultRelayForChannel(relay.channel);
  const channel = String(Number(relay.channel));
  const apiLabel = normalizeRelayLabel(relay.label);
  const savedLabel = savedRelayLabels[channel] || "";
  if (prototypeMode) {
    return savedLabel || apiLabel || fallback.label;
  }
  return apiLabel || savedLabel || fallback.label;
}

function relayPin(relay) {
  return relay.pin || defaultRelayForChannel(relay.channel).pin;
}

function saveRelayLabel(channel, label) {
  const key = String(Number(channel));
  const nextLabel = normalizeRelayLabel(label);
  if (!key || key === "NaN") {
    return;
  }
  if (nextLabel) {
    savedRelayLabels[key] = nextLabel;
  } else {
    delete savedRelayLabels[key];
  }
  writeSavedRelayLabels();
  renderRelays();
}

function resetRelayLabels() {
  savedRelayLabels = {};
  try {
    window.localStorage.removeItem(relayLabelStorageKey);
  } catch (_error) {
    // Keep the in-memory reset even if browser storage is unavailable.
  }
  renderRelays();
  renderRelayLabelEditor(true);
}

function text(id, value) {
  const element = document.querySelector(`#${id}`);
  if (element) {
    element.textContent = value;
  }
}

function formatUptime(ms) {
  const seconds = Math.floor((Number(ms) || 0) / 1000);
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  if (hours > 0) {
    return `${hours}h ${minutes}m`;
  }
  if (minutes > 0) {
    return `${minutes}m ${seconds % 60}s`;
  }
  return `${seconds}s`;
}

function formatBytes(value) {
  const bytes = Number(value) || 0;
  const units = ["B", "KB", "MB", "GB", "TB"];
  let size = bytes;
  let unit = 0;
  while (size >= 1024 && unit < units.length - 1) {
    size /= 1024;
    unit += 1;
  }
  return `${size.toFixed(unit === 0 ? 0 : 1)} ${units[unit]}`;
}

function canChangeRelay(relay, nextState = state) {
  return (
    nextState.adminProvisioned &&
    nextState.hardwareGateClosed &&
    !nextState.safetyLocked &&
    Boolean(relay.enabled)
  );
}

function relayGateReason(relay, nextState = state) {
  if (!nextState.adminProvisioned) {
    return "Admin missing";
  }
  if (!nextState.hardwareGateClosed) {
    return "Hardware gate open";
  }
  if (nextState.safetyLocked) {
    return "Safety lock closed";
  }
  if (!relay.enabled) {
    return "Relay disabled";
  }
  return "Ready";
}

function setStatus(element, label, status) {
  element.textContent = label;
  element.parentElement.dataset.state = status;
}

function normalizeState(nextState) {
  const normalized = {
    ...clone(baseState),
    ...nextState,
    xbee: { ...baseState.xbee, ...(nextState.xbee || {}) },
    storage: { ...baseState.storage, ...(nextState.storage || {}) },
    lastCommand: { ...baseState.lastCommand, ...(nextState.lastCommand || {}) },
    config: { ...baseState.config, ...(nextState.config || {}) },
  };

  if (!Array.isArray(normalized.relays) || normalized.relays.length === 0) {
    normalized.relays = clone(baseState.relays);
  }
  normalized.relays = normalized.relays.map((relay, index) => {
    const channel = relay.channel || index + 1;
    const fallback = defaultRelayForChannel(channel);
    const label = normalizeRelayLabel(relay.label);
    return {
      ...relay,
      channel,
      label,
      pin: relay.pin || fallback.pin,
    };
  });

  return normalized;
}

function render(nextState = state) {
  state = normalizeState(nextState);

  els.deviceId.textContent = state.deviceId || "bench-four-relay-01";
  setStatus(
    els.safetyBadge,
    state.safetyLocked ? "Locked" : "Open",
    state.safetyLocked ? "bad" : "ok",
  );
  setStatus(
    els.gateBadge,
    state.hardwareGateClosed ? "Closed" : "Open",
    state.hardwareGateClosed ? "ok" : "bad",
  );
  setStatus(
    els.storageBadge,
    state.storage.mounted ? state.storage.mode : "Fallback",
    state.storage.mounted && state.storage.logWritable ? "ok" : "warn",
  );
  setStatus(
    els.xbeeBadge,
    state.xbee.link || "unknown",
    state.xbee.configured ? "ok" : "warn",
  );
  setStatus(
    els.adminBadge,
    state.adminProvisioned ? "Ready" : "Missing",
    state.adminProvisioned ? "ok" : "bad",
  );

  renderRelays();
  renderRelayLabelEditor();
  renderSafety();
  renderStorage();
  renderXbee();
  renderLogs();
  renderConfig();

  els.lockButton.disabled = !state.adminProvisioned;
  els.allOffButton.disabled = !state.adminProvisioned;
}

function renderRelays() {
  const relaysReady =
    state.adminProvisioned && state.hardwareGateClosed && !state.safetyLocked;
  els.controlGateText.textContent = relaysReady
    ? "Relay commands available for enabled channels"
    : "Relay commands blocked";
  els.relayGrid.replaceChildren();

  state.relays.forEach((relay) => {
    const card = document.createElement("article");
    card.className = `relay-card ${relay.state ? "is-on" : "is-off"}`;

    const header = document.createElement("header");
    const title = document.createElement("h3");
    title.textContent = relayLabel(relay);
    const badge = document.createElement("span");
    badge.className = relay.enabled ? "mini-badge ok" : "mini-badge bad";
    badge.textContent = relay.enabled ? "enabled" : "blocked";
    header.append(title, badge);

    const pinLabel = document.createElement("span");
    pinLabel.className = "relay-pin";
    pinLabel.textContent = `CH ${relay.channel} / ${relayPin(relay)}`;

    const stateLabel = document.createElement("strong");
    stateLabel.className = "relay-state";
    stateLabel.textContent = relay.state ? "On" : "Off";

    const reason = document.createElement("p");
    reason.textContent = relayGateReason(relay);

    const button = document.createElement("button");
    button.type = "button";
    button.textContent = relay.state ? "Turn off" : "Turn on";
    button.disabled = !canChangeRelay(relay);
    button.addEventListener("click", () => {
      sendCommand(endpoints.relay(relay.channel), {
        state: !relay.state,
        sequence: sequence++,
      });
    });

    card.append(header, pinLabel, stateLabel, reason, button);
    els.relayGrid.appendChild(card);
  });
}

function renderRelayLabelEditor(force = false) {
  if (!els.relayLabelEditor) {
    return;
  }
  if (!force && els.relayLabelEditor.contains(document.activeElement)) {
    return;
  }

  els.relayLabelEditor.replaceChildren(
    ...state.relays.map((relay) => {
      const label = document.createElement("label");
      const title = document.createElement("span");
      const input = document.createElement("input");
      const detail = document.createElement("small");
      const channel = String(Number(relay.channel));

      title.textContent = `Channel ${channel}`;
      input.type = "text";
      input.maxLength = maxRelayLabelLength;
      input.autocomplete = "off";
      input.value = relayLabel(relay);
      input.dataset.relayLabelInput = channel;
      input.addEventListener("input", () => {
        if (input.value.length > maxRelayLabelLength) {
          input.value = input.value.slice(0, maxRelayLabelLength);
        }
        saveRelayLabel(channel, input.value);
      });
      detail.textContent = `${relayPin(relay)} provisional`;
      label.append(title, input, detail);
      return label;
    })
  );
}

function renderSafety() {
  const lastCommand = state.lastCommand || {};
  els.safetySummary.textContent = state.safetyLocked
    ? "Safety lock is closed"
    : "Safety lock is open";
  text("safetyLockValue", state.safetyLocked ? "locked" : "open");
  text("hardwareGateValue", state.hardwareGateClosed ? "closed" : "open");
  text("lastCommandValue", lastCommand.source || "unknown");
  text("rejectValue", lastCommand.result || "none");
  text("uptimeValue", formatUptime(state.uptimeMs));
  text("sequenceValue", String(lastCommand.sequence ?? 0));
}

function renderStorage() {
  const storage = state.storage || baseState.storage;
  const lowSpace = storage.mounted && storage.freeBytes > 0 && storage.freeBytes < 10_000_000;
  const degraded =
    !storage.mounted ||
    storage.fallbackActive ||
    !storage.logWritable ||
    !storage.manifestReadable ||
    lowSpace ||
    readOnlyApiStatus.storage !== "ok" ||
    readOnlyApiStatus.manifest !== "ok";

  if (!storage.mounted) {
    els.storageSummary.textContent = "MicroSD unavailable; fallback active";
  } else if (lowSpace) {
    els.storageSummary.textContent = "MicroSD mounted; free space low";
  } else if (degraded) {
    els.storageSummary.textContent = "MicroSD mounted with degraded services";
  } else {
    els.storageSummary.textContent = "MicroSD mounted";
  }

  text("storageMountValue", storage.mounted ? "mounted" : "not mounted");
  text("storageCardValue", storage.cardType || "unknown");
  text("storageCapacityValue", formatBytes(storage.capacityBytes));
  text("storageFreeValue", formatBytes(storage.freeBytes));
  text("assetModeValue", storage.mode || "unknown");
  text("manifestVersionValue", manifest.version || storage.assetVersion || "unknown");
  text("logStatusValue", storage.logWritable ? "writable" : "not writable");
  text("fallbackValue", storage.fallbackActive ? "active" : "inactive");
  text("assetRootValue", storage.assetRoot || "/sdcard/www");
  text("logRootValue", storage.logRoot || "/sdcard/logs");
}

function renderXbee() {
  const xbee = state.xbee || baseState.xbee;
  els.xbeeSummary.textContent = xbee.configured
    ? `Link ${xbee.link || "unknown"}`
    : "Radio configuration pending";
  text("xbeeConfiguredValue", String(Boolean(xbee.configured)));
  text("xbeeLinkValue", xbee.link || "unknown");
  text("xbeeLastStatusValue", xbee.lastStatus || "none");
  text("xbeeAllowlistValue", xbee.allowlist || state.config.allowlist || "missing");
  text("xbeeLastFrameValue", xbee.lastFrame || "none");
  text("xbeeTelemetryValue", xbee.telemetry || "idle");
}

function renderLogs() {
  const visibleLogs = logs.filter((item) => {
    if (currentFilter === "all") {
      return true;
    }
    if (currentFilter === "rejected") {
      return item.type === "rejected" || String(item.result || "").includes("reject");
    }
    return item.type === currentFilter;
  });

  const apiNote = readOnlyApiStatus.logs === "ok" ? "" : "Log API unavailable; ";
  els.logsSummary.textContent = `${apiNote}${visibleLogs.length} visible of ${logs.length} recent`;
  els.logList.replaceChildren();

  if (visibleLogs.length === 0) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent = "No matching log records";
    els.logList.appendChild(empty);
    return;
  }

  visibleLogs.forEach((item) => {
    const row = document.createElement("article");
    row.className = `log-row ${item.severity || "info"}`;

    const meta = document.createElement("div");
    meta.className = "log-meta";
    const type = document.createElement("span");
    type.textContent = item.type || "event";
    const time = document.createElement("time");
    time.dateTime = item.time || "";
    time.textContent = formatTime(item.time);
    meta.append(type, time);

    const message = document.createElement("strong");
    message.textContent = item.message || "event";

    const detail = document.createElement("p");
    const channel = item.channel ? ` ch ${item.channel}` : "";
    detail.textContent = `${item.source || "unknown"}${channel} / ${item.result || "none"}`;

    row.append(meta, message, detail);
    els.logList.appendChild(row);
  });
}

function renderConfig() {
  const storage = state.storage || baseState.storage;
  els.configSummary.textContent = "Read-only status";
  text("configAdminValue", String(Boolean(state.adminProvisioned)));
  text("configSafetyValue", state.config.safety || "pending");
  text("configRelayValue", state.config.relayPolarity || "unverified");
  text("configAllowlistValue", state.config.allowlist || state.xbee.allowlist || "missing");
  text("configAssetValue", manifest.version || storage.assetVersion || "unknown");
  text("configFallbackValue", storage.fallbackActive ? "active" : "inactive");
}

function formatTime(value) {
  if (!value) {
    return "unknown";
  }
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

async function requestJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { "content-type": "application/json" },
    ...options,
  });
  const textBody = await response.text();
  const body = textBody ? JSON.parse(textBody) : {};
  if (!response.ok) {
    throw new Error(body.reason || body.message || response.statusText);
  }
  return body;
}

async function refresh() {
  if (prototypeMode) {
    const scenario = mockScenarios[currentScenario] || mockScenarios.mounted;
    const nextState = clone(scenario.state);
    nextState.uptimeMs = (state.uptimeMs || 0) + 1000;
    state = nextState;
    manifest = clone(scenario.manifest);
    logs = clone(scenario.logs);
    readOnlyApiStatus = { storage: "ok", manifest: "ok", logs: "ok" };
    els.message.textContent = "Prototype mode: mock device API active.";
    render(state);
    return;
  }

  try {
    const liveState = await requestJson(endpoints.state);
    state = normalizeState(liveState);
    els.message.textContent = "";
  } catch (error) {
    const scenario = mockScenarios.missing;
    state = normalizeState(scenario.state);
    manifest = clone(scenario.manifest);
    logs = clone(scenario.logs);
    readOnlyApiStatus = { storage: "failed", manifest: "failed", logs: "failed" };
    els.message.textContent = `State API unavailable: ${error.message}`;
    render(state);
    return;
  }

  await loadReadOnlyResources();
  render(state);
}

async function loadReadOnlyResources() {
  readOnlyApiStatus = { storage: "ok", manifest: "ok", logs: "ok" };

  try {
    const storage = await requestJson(endpoints.storage);
    state = normalizeState({
      ...state,
      storage: {
        ...state.storage,
        ...storage,
      },
    });
  } catch (error) {
    readOnlyApiStatus.storage = "failed";
  }

  try {
    manifest = await requestJson(endpoints.manifest);
  } catch (error) {
    readOnlyApiStatus.manifest = "failed";
    manifest = {
      ...assetManifest,
      version: state.storage.assetVersion || "unknown",
    };
  }

  try {
    const recent = await requestJson(endpoints.logs(50, currentFilter));
    logs = Array.isArray(recent.items) ? recent.items : [];
  } catch (error) {
    readOnlyApiStatus.logs = "failed";
    logs = [];
  }
}

async function sendCommand(url, payload) {
  if (prototypeMode) {
    applyMockCommand(url, payload);
    return;
  }

  try {
    const nextState = await requestJson(url, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    els.message.textContent = "";
    render(nextState);
  } catch (error) {
    els.message.textContent = `Rejected: ${error.message}`;
  }
}

function applyMockCommand(url, payload) {
  const nextState = clone(state);

  if (url === endpoints.allOff) {
    nextState.relays = nextState.relays.map((relay) => ({ ...relay, state: false }));
    nextState.lastCommand = {
      source: "mock-http",
      sequence: payload.sequence,
      result: "all_off",
    };
  } else if (url === endpoints.safetyLock) {
    if (!nextState.adminProvisioned) {
      nextState.lastCommand = {
        source: "mock-http",
        sequence: payload.sequence,
        result: "admin_required",
      };
      els.message.textContent = "Rejected: admin_required";
      render(nextState);
      return;
    }
    nextState.safetyLocked = Boolean(payload.locked);
    nextState.lastCommand = {
      source: "mock-http",
      sequence: payload.sequence,
      result: nextState.safetyLocked ? "locked" : "unlocked",
    };
  } else {
    const channel = Number(url.split("/").pop());
    nextState.relays = nextState.relays.map((relay) => {
      if (relay.channel !== channel) {
        return relay;
      }
      if (!canChangeRelay(relay, nextState)) {
        nextState.lastCommand = {
          source: "mock-http",
          sequence: payload.sequence,
          result: relayGateReason(relay, nextState).toLowerCase().replaceAll(" ", "_"),
        };
        return relay;
      }
      nextState.lastCommand = {
        source: "mock-http",
        sequence: payload.sequence,
        result: "accepted",
      };
      return { ...relay, state: Boolean(payload.state) };
    });
  }

  els.message.textContent = "";
  render(nextState);
}

function activateTab(target) {
  document.querySelectorAll(".tab").forEach((button) => {
    const active = button.dataset.tabTarget === target;
    button.classList.toggle("is-active", active);
    button.setAttribute("aria-selected", String(active));
  });

  document.querySelectorAll(".panel").forEach((panel) => {
    const active = panel.id === `panel-${target}`;
    panel.classList.toggle("is-active", active);
    panel.hidden = !active;
  });
}

document.querySelectorAll(".tab").forEach((button) => {
  button.addEventListener("click", () => activateTab(button.dataset.tabTarget));
});

document.querySelectorAll("[data-log-filter]").forEach((button) => {
  button.addEventListener("click", () => {
    currentFilter = button.dataset.logFilter;
    document.querySelectorAll("[data-log-filter]").forEach((candidate) => {
      candidate.classList.toggle("is-active", candidate === button);
    });
    if (!prototypeMode) {
      loadReadOnlyResources().then(() => render(state));
    } else {
      render(state);
    }
  });
});

window.addEventListener("storage", (event) => {
  if (event.key === relayLabelStorageKey) {
    savedRelayLabels = readSavedRelayLabels();
    renderRelays();
    renderRelayLabelEditor(true);
  }
});

els.allOffButton.addEventListener("click", () => {
  sendCommand(endpoints.allOff, { sequence: sequence++ });
});

els.lockButton.addEventListener("click", () => {
  sendCommand(endpoints.safetyLock, {
    locked: !state.safetyLocked,
    sequence: sequence++,
  });
});

if (els.resetLabelsButton) {
  els.resetLabelsButton.addEventListener("click", resetRelayLabels);
}

if (prototypeMode) {
  els.scenarioControl.hidden = false;
  els.mockScenarioSelect.value = currentScenario;
  els.mockScenarioSelect.addEventListener("change", () => {
    currentScenario = els.mockScenarioSelect.value;
    state = clone(mockScenarios[currentScenario].state);
    manifest = clone(mockScenarios[currentScenario].manifest);
    logs = clone(mockScenarios[currentScenario].logs);
    render(state);
  });
}

window.__fourRelayHmi = {
  setMockScenario(name) {
    if (mockScenarios[name]) {
      currentScenario = name;
      if (els.mockScenarioSelect) {
        els.mockScenarioSelect.value = name;
      }
      state = clone(mockScenarios[name].state);
      manifest = clone(mockScenarios[name].manifest);
      logs = clone(mockScenarios[name].logs);
      render(state);
    }
  },
  getState() {
    return clone(state);
  },
  setRelayLabel(channel, label) {
    saveRelayLabel(channel, label);
    renderRelayLabelEditor(true);
  },
  resetRelayLabels,
};

refresh();
window.setInterval(refresh, 5000);
