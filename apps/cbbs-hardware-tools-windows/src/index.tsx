import { AppRegistry } from "react-native";
import { ProductWindowsShell } from "@cbbs/product-ui";
import type { UiIntentRecord } from "@cbbs/protocol";

export const WINDOWS_HARDWARE_TOOLS_APP_COMPONENT_NAME = "CbbsHardwareToolsWindows";

export interface CbbsHardwareToolsWindowsAppProps {
  onIntent?: (intent: UiIntentRecord) => void;
}

export function CbbsHardwareToolsWindowsApp({ onIntent }: CbbsHardwareToolsWindowsAppProps = {}) {
  return <ProductWindowsShell appId="hardware-tools" onIntent={onIntent} />;
}

AppRegistry.registerComponent(WINDOWS_HARDWARE_TOOLS_APP_COMPONENT_NAME, () => CbbsHardwareToolsWindowsApp);
