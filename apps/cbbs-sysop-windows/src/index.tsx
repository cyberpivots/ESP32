import { AppRegistry } from "react-native";
import { ProductWindowsShell } from "@cbbs/product-ui";
import type { UiIntentRecord } from "@cbbs/protocol";

export const WINDOWS_SYSOP_APP_COMPONENT_NAME = "CbbsSysopWindows";

export interface CbbsSysopWindowsAppProps {
  onIntent?: (intent: UiIntentRecord) => void;
}

export function CbbsSysopWindowsApp({ onIntent }: CbbsSysopWindowsAppProps = {}) {
  return <ProductWindowsShell appId="sysop" onIntent={onIntent} />;
}

AppRegistry.registerComponent(WINDOWS_SYSOP_APP_COMPONENT_NAME, () => CbbsSysopWindowsApp);
