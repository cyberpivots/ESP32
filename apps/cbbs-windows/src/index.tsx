import { Pressable, ScrollView, Text, View } from "react-native";
import {
  CLOSED_SURFACE_IDS,
  LOCAL_ONLY_REASON,
  localIntent,
  type AppRole,
  type ClosedSurfaceId,
  type IntentId,
  type UiIntentRecord,
  type ViewId
} from "@cbbs/protocol";

type WindowsRole = Extract<AppRole, "client" | "sysop">;

interface WindowsModeProfile {
  role: WindowsRole;
  label: string;
  views: ViewId[];
  localActions: IntentId[];
}

interface WindowsFixtureRow {
  id: string;
  view: ViewId;
  title: string;
  status: "local" | "queued" | "blocked" | "disabled";
  detail: string;
}

const clientRoleProfile: WindowsModeProfile = {
  role: "client",
  label: "Client",
  views: ["home", "messages", "downloads", "peers", "network", "evidence"],
  localActions: ["compose_draft", "queue_file_request", "filter", "select_row", "view_proof"]
};

const sysopRoleProfile: WindowsModeProfile = {
  role: "sysop",
  label: "Sysop",
  views: ["home", "downloads", "peers", "network", "diagnostics", "safety", "config", "evidence"],
  localActions: ["refresh", "filter", "select_row", "open_detail", "ack_local", "view_proof"]
};

const defaultWindowsRow: WindowsFixtureRow = {
  id: "row-home-fixture",
  view: "home",
  title: "CBBS fixture lane",
  status: "local",
  detail: "Local board overview with no transport attached."
};

export const windowsSpikeStatus = {
  status: "package-only-rnw-dependency-lane",
  nativeProjectGenerated: false,
  nativeDependencySelected: true,
  requiredGate: "windows-runner-toolchain-review"
} as const;

export const windowsDependencyLane = {
  react: "19.2.3",
  reactNative: "0.83.9",
  reactNativeWindows: "0.83.0",
  reactNativeWindowsPackage: "react-native-windows",
  packageOnly: true,
  nativeProjectGenerated: false
} as const;

export const windowsRoleProfiles: WindowsModeProfile[] = [clientRoleProfile, sysopRoleProfile];

export const windowsClientSysopPlan = {
  appShape: "single-role-aware-windows-app",
  modes: windowsRoleProfiles,
  localOnlyReason: LOCAL_ONLY_REASON,
  protocolClosedSurfaces: CLOSED_SURFACE_IDS,
  closedGates: [
    "native_windows_project",
    "windows_runner",
    "visual_studio_build",
    "package_identity",
    "windows_capabilities",
    "signing_release",
    "live_transport",
    "serial_or_rf",
    "firmware_or_bridge_abi"
  ]
} as const;

export const windowsFixtureRows: WindowsFixtureRow[] = [
  defaultWindowsRow,
  {
    id: "row-message-draft",
    view: "messages",
    title: "Draft staging",
    status: "queued",
    detail: "Draft text stays local until a later authority gate."
  },
  {
    id: "row-download-stage",
    view: "downloads",
    title: "Request staging",
    status: "queued",
    detail: "File request is staged by row id only."
  },
  {
    id: "row-peer-summary",
    view: "peers",
    title: "Peer summaries",
    status: "local",
    detail: "Peer rows are redacted fixture summaries."
  },
  {
    id: "row-link-status",
    view: "network",
    title: "Link status",
    status: "blocked",
    detail: "Discovery and transport surfaces are closed."
  },
  {
    id: "row-diagnostic-host",
    view: "diagnostics",
    title: "Host validation",
    status: "local",
    detail: "Package-only checks can run without Windows native proof."
  },
  {
    id: "row-safety-gates",
    view: "safety",
    title: "Authority gates",
    status: "disabled",
    detail: "Unsafe actions are visible as disabled controls."
  },
  {
    id: "row-config-readonly",
    view: "config",
    title: "Read-only manifest",
    status: "disabled",
    detail: "Configuration write authority is closed."
  },
  {
    id: "row-evidence-transcript",
    view: "evidence",
    title: "Transcript-first proof",
    status: "local",
    detail: "Evidence wording names fixture source before behavior claims."
  }
];

export interface WindowsClientSysopShellProps {
  activeRole?: WindowsRole;
  activeView?: ViewId;
  onIntent?: (intent: UiIntentRecord) => void;
}

export function createWindowsLocalIntent(
  intent: IntentId,
  role: WindowsRole,
  view: ViewId,
  extra: Omit<Partial<UiIntentRecord>, "schema" | "intent" | "role" | "view" | "localOnlyReason"> = {}
): UiIntentRecord {
  return localIntent(intent, role, view, extra);
}

export function WindowsClientSysopShell({
  activeRole = "client",
  activeView,
  onIntent = () => undefined
}: WindowsClientSysopShellProps) {
  const profile = getRoleProfile(activeRole);
  const view = activeView && profile.views.includes(activeView) ? activeView : profile.views[0] ?? "home";
  const rows = windowsFixtureRows.filter((row) => row.view === view);
  const primaryRow = rows[0] ?? defaultWindowsRow;

  const emit = (
    intent: IntentId,
    extra: Omit<Partial<UiIntentRecord>, "schema" | "intent" | "role" | "view" | "localOnlyReason"> = {}
  ) => onIntent(createWindowsLocalIntent(intent, profile.role, view, extra));

  return (
    <ScrollView testID="windows-client-sysop-shell">
      <View>
        <Text>Fixture-only {profile.label} Windows console</Text>
        <Text>Package-only RNW lane; no Windows native runtime proof.</Text>
        <Text>Local-only marker: {LOCAL_ONLY_REASON}</Text>
      </View>

      <View>
        {profile.views.map((viewId) => (
          <Pressable
            accessibilityRole="button"
            key={viewId}
            onPress={() => emit("navigate", { targetView: viewId })}
            testID={`windows-view-${profile.role}-${viewId}`}
          >
            <Text>{viewId.toUpperCase()}</Text>
          </Pressable>
        ))}
      </View>

      <View testID={`windows-view-panel-${view}`}>
        <Text>{viewLabel(view)}</Text>
        {rows.map((row) => (
          <Pressable
            accessibilityRole="button"
            key={row.id}
            onPress={() => emit("select_row", { rowId: row.id })}
            testID={`windows-row-${row.id}`}
          >
            <Text>{row.title}</Text>
            <Text>{row.status}</Text>
            <Text>{row.detail}</Text>
          </Pressable>
        ))}
      </View>

      <View>
        {profile.localActions.map((action) => (
          <Pressable
            accessibilityRole="button"
            key={action}
            onPress={() => emit(action, actionPayload(action, primaryRow.id))}
            testID={`windows-action-${profile.role}-${action}`}
          >
            <Text>{actionLabel(action)}</Text>
          </Pressable>
        ))}
      </View>

      <View>
        <Text>Transcript-first Windows fixture evidence</Text>
        <Text>proof-local-transcript-note</Text>
        <Text>No native device, Windows runner, transport, or CBBS hardware proof is claimed.</Text>
      </View>

      <View>
        {CLOSED_SURFACE_IDS.map((surface) => (
          <Pressable
            accessibilityRole="button"
            accessibilityState={{ disabled: true }}
            disabled
            key={surface}
            testID={`windows-closed-surface-${surface}`}
          >
            <Text>{closedSurfaceLabel(surface)}</Text>
            <Text>Disabled until a separate source-backed gate accepts this surface.</Text>
          </Pressable>
        ))}
      </View>
    </ScrollView>
  );
}

export function WindowsDependencyProof() {
  return <WindowsClientSysopShell />;
}

function getRoleProfile(role: WindowsRole): WindowsModeProfile {
  return windowsRoleProfiles.find((profile) => profile.role === role) ?? clientRoleProfile;
}

function actionPayload(
  action: IntentId,
  rowId: string
): Omit<Partial<UiIntentRecord>, "schema" | "intent" | "role" | "view" | "localOnlyReason"> {
  switch (action) {
    case "compose_draft":
      return { draftText: "Local fixture draft" };
    case "queue_file_request":
    case "select_row":
    case "open_detail":
      return { rowId };
    case "filter":
      return { filter: "ready" };
    case "view_proof":
      return { proofId: "proof-local-transcript-note" };
    default:
      return {};
  }
}

function actionLabel(action: IntentId): string {
  const labels: Record<IntentId, string> = {
    navigate: "Navigate locally",
    refresh: "Refresh fixture",
    filter: "Filter rows",
    select_row: "Select row",
    open_detail: "Open detail",
    compose_draft: "Compose draft",
    queue_file_request: "Stage request",
    ack_local: "Acknowledge locally",
    view_proof: "View proof"
  };
  return labels[action];
}

function viewLabel(view: ViewId): string {
  const labels: Record<ViewId, string> = {
    home: "Home",
    messages: "Messages",
    downloads: "Downloads",
    peers: "Peers",
    network: "Network",
    diagnostics: "Diagnostics",
    safety: "Safety",
    config: "Config",
    evidence: "Evidence"
  };
  return labels[view];
}

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
