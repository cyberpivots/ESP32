import { AppRegistry } from "react-native";
import { ProductWindowsShell } from "@cbbs/product-ui";
import type { UiIntentRecord } from "@cbbs/protocol";

export const WINDOWS_CLIENT_APP_COMPONENT_NAME = "CbbsClientWindows";

export interface CbbsClientWindowsAppProps {
  onIntent?: (intent: UiIntentRecord) => void;
}

export function CbbsClientWindowsApp({ onIntent }: CbbsClientWindowsAppProps = {}) {
  return <ProductWindowsShell appId="client" onIntent={onIntent} />;
}

AppRegistry.registerComponent(WINDOWS_CLIENT_APP_COMPONENT_NAME, () => CbbsClientWindowsApp);
