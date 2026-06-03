import { Text, View } from "react-native";

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

export const windowsClientSysopPlan = {
  appShape: "single-role-aware-windows-app",
  modes: [
    {
      role: "client",
      views: ["home", "messages", "downloads", "peers", "network", "evidence"],
      localActions: ["compose_draft", "queue_file_request", "filter", "select_row", "view_proof"]
    },
    {
      role: "sysop",
      views: ["home", "downloads", "peers", "network", "diagnostics", "safety", "config", "evidence"],
      localActions: ["refresh", "filter", "select_row", "open_detail", "ack_local", "view_proof"]
    }
  ],
  localOnlyReason: "fixture-only-ui-intent",
  protocolClosedSurfaces: [
    "bridge_abi",
    "serial_abi",
    "firmware_abi",
    "gate_f_service_code",
    "serial_write",
    "rf_xbee_write",
    "ble_pairing",
    "web_bluetooth",
    "web_serial",
    "softap_probe",
    "local_network_discovery",
    "flash_erase_monitor",
    "relay_or_load",
    "persistent_config_write",
    "native_prebuild",
    "native_windows_project",
    "external_service_build"
  ],
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

export function WindowsDependencyProof() {
  return (
    <View>
      <Text>CBBS Windows package-only RNW dependency lane</Text>
    </View>
  );
}
