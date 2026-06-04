import { AppRegistry } from "react-native";
import { ProductWindowsShell } from "@cbbs/product-ui";
import {
  CBBS_PRODUCT_WINDOWS_APP_IDS,
  cbbsProductWindowsApps,
  type CbbsProductWindowsAppId
} from "@cbbs/product";
import type { UiIntentRecord } from "@cbbs/protocol";

export const WINDOWS_APP_COMPONENT_NAME = "CbbsWindows";

export const legacyWindowsMigrationStatus = {
  componentName: WINDOWS_APP_COMPONENT_NAME,
  legacyPackage: "apps/cbbs-windows",
  defaultProductApp: "sysop",
  productApps: CBBS_PRODUCT_WINDOWS_APP_IDS,
  packageIdentityAccepted: false,
  capabilityUseAccepted: false,
  signingConfigured: false,
  releaseConfigured: false,
  liveExecutionAvailable: false
} as const;

export const windowsProductAppProfiles = cbbsProductWindowsApps;

export interface WindowsProductMigrationShellProps {
  appId?: CbbsProductWindowsAppId;
  onIntent?: (intent: UiIntentRecord) => void;
}

export function WindowsProductMigrationShell({
  appId = "sysop",
  onIntent
}: WindowsProductMigrationShellProps) {
  return <ProductWindowsShell appId={appId} onIntent={onIntent} />;
}

AppRegistry.registerComponent(WINDOWS_APP_COMPONENT_NAME, () => WindowsProductMigrationShell);

export { CBBS_PRODUCT_WINDOWS_APP_IDS, cbbsProductWindowsApps, ProductWindowsShell };
export type { CbbsProductWindowsAppId };
