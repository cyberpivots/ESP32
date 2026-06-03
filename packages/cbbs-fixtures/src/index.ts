import {
  CBBS_CLIENT_SCHEMA,
  CLOSED_SURFACE_IDS,
  type AppRole,
  type ClosedSurfaceId,
  type ViewId
} from "@cbbs/protocol";

export interface CbbsFixtureSnapshot {
  schema: typeof CBBS_CLIENT_SCHEMA;
  generatedAt: string;
  mode: "fixture-only";
  activeRole: AppRole;
  roleProfiles: FixtureRoleProfile[];
  views: FixtureView[];
  rows: FixtureRow[];
  evidence: FixtureEvidence[];
  closedSurfaces: FixtureClosedSurface[];
}

export interface FixtureRoleProfile {
  role: AppRole;
  label: string;
  mode: "client" | "sysop" | "monitor" | "devconfig";
  viewIds: ViewId[];
}

export interface FixtureView {
  id: ViewId;
  label: string;
  summary: string;
}

export interface FixtureRow {
  id: string;
  view: ViewId;
  title: string;
  status: "ready" | "queued" | "blocked" | "disabled" | "local";
  detail: string;
}

export interface FixtureEvidence {
  id: string;
  label: string;
  transcriptFirst: true;
  summary: string;
}

export interface FixtureClosedSurface {
  id: ClosedSurfaceId;
  label: string;
  gateLabel: string;
}

export const cbbsFixtureSnapshot: CbbsFixtureSnapshot = {
  schema: CBBS_CLIENT_SCHEMA,
  generatedAt: "2026-06-02T00:00:00Z",
  mode: "fixture-only",
  activeRole: "sysop",
  roleProfiles: [
    {
      role: "client",
      label: "Client",
      mode: "client",
      viewIds: ["home", "messages", "downloads", "peers", "network", "evidence"]
    },
    {
      role: "sysop",
      label: "Sysop",
      mode: "sysop",
      viewIds: ["home", "downloads", "peers", "network", "diagnostics", "safety", "config", "evidence"]
    },
    {
      role: "monitor",
      label: "Monitor",
      mode: "monitor",
      viewIds: ["home", "peers", "network", "diagnostics", "evidence"]
    },
    {
      role: "devconfig",
      label: "Dev Config",
      mode: "devconfig",
      viewIds: ["home", "diagnostics", "safety", "config", "evidence"]
    }
  ],
  views: [
    { id: "home", label: "Home", summary: "Fixture board overview" },
    { id: "messages", label: "Messages", summary: "Draft-only message queue" },
    { id: "downloads", label: "Downloads", summary: "Local request staging" },
    { id: "peers", label: "Peers", summary: "Redacted peer summaries" },
    { id: "network", label: "Network", summary: "No live discovery" },
    { id: "diagnostics", label: "Diagnostics", summary: "Host validation state" },
    { id: "safety", label: "Safety", summary: "Closed authority surfaces" },
    { id: "config", label: "Config", summary: "Read-only staged manifest" },
    { id: "evidence", label: "Evidence", summary: "Transcript-first proof notes" }
  ],
  rows: [
    {
      id: "row-home-local",
      view: "home",
      title: "CBBS fixture lane",
      status: "local",
      detail: "Host-only fixture state; no transport attached."
    },
    {
      id: "row-message-draft",
      view: "messages",
      title: "Draft staging",
      status: "queued",
      detail: "Draft text stays local and is not transmitted."
    },
    {
      id: "row-download-request",
      view: "downloads",
      title: "File request staging",
      status: "queued",
      detail: "Request is a local placeholder with no file name or content."
    },
    {
      id: "row-network-closed",
      view: "network",
      title: "Live discovery closed",
      status: "blocked",
      detail: "No LAN, SoftAP, BLE, Web Serial, or Web Bluetooth access."
    },
    {
      id: "row-safety-disabled",
      view: "safety",
      title: "Unsafe actions disabled",
      status: "disabled",
      detail: "Serial, RF, flash, relay, load, and mains actions are closed."
    }
  ],
  evidence: [
    {
      id: "proof-local-transcript-note",
      label: "Transcript-first fixture",
      transcriptFirst: true,
      summary: "Fixture-only transcript note; no live browser, native device, Windows runner, or CBBS hardware proof."
    }
  ],
  closedSurfaces: CLOSED_SURFACE_IDS.map((id) => ({
    id,
    label: closedSurfaceLabel(id),
    gateLabel: "Disabled until a separate source-backed gate accepts this surface."
  }))
};

function closedSurfaceLabel(id: ClosedSurfaceId): string {
  const labels: Record<ClosedSurfaceId, string> = {
    bridge_abi: "Bridge ABI changes",
    serial_abi: "Serial ABI changes",
    firmware_abi: "Firmware ABI changes",
    gate_f_service_code: "Gate F service-code changes",
    serial_write: "Serial writes",
    rf_xbee_write: "RF/XBee writes",
    ble_pairing: "BLE pairing",
    web_bluetooth: "Web Bluetooth",
    web_serial: "Web Serial",
    softap_probe: "SoftAP probing",
    local_network_discovery: "Local-network discovery",
    flash_erase_monitor: "Flash, erase, or monitor",
    relay_or_load: "Relay, load, or mains action",
    persistent_config_write: "Persistent config writes",
    native_prebuild: "Native prebuild",
    native_windows_project: "Windows native project generation",
    external_service_build: "EAS, App Center, signing, or release automation"
  };
  return labels[id];
}
