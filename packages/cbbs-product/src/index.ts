import type { HostCommandActionClass, HostCommandActionId, IntentId, ViewId } from "@cbbs/protocol";
import { CBBS_RNW_MENU_SCHEMA, hardwareToolsMenu as generatedHardwareToolsMenu } from "./hardwareToolsMenu.generated";
import { CBBS_RNW_WIN31_PARITY_SCHEMA, win31ParityContract as generatedWin31ParityContract } from "./win31Parity.generated";

export const CBBS_PRODUCT_WINDOWS_APP_IDS = ["client", "sysop", "hardware-tools"] as const;
export const CBBS_PRODUCT_WINDOWS_APP_SUBTITLES = {
  client: "CBBS Client",
  sysop: "CBBS Sysop",
  "hardware-tools": "CBBS Hardware Tools"
} as const;
export const PRODUCT_CAPABILITY_GROUPS = [
  "bench",
  "radio",
  "mesh",
  "firmware",
  "fabrication",
  "safety",
  "activity"
] as const;
export const PRODUCT_EXECUTION_MODES = [
  "localOnly",
  "artifactReview",
  "bridgePreviewUnavailable",
  "tier3Closed"
] as const;

export type CbbsProductWindowsAppId = (typeof CBBS_PRODUCT_WINDOWS_APP_IDS)[number];
export type ProductCapabilityGroup = (typeof PRODUCT_CAPABILITY_GROUPS)[number];
export type ProductExecutionMode = (typeof PRODUCT_EXECUTION_MODES)[number];
export type Win31ParityMenuId = (typeof generatedWin31ParityContract.menus)[number]["id"];
export type Win31ParityPageId = (typeof generatedWin31ParityContract.pages)[number]["id"];
export type Win31ParityCategoryDisposition =
  (typeof generatedWin31ParityContract.roleCoverage.client)[number]["disposition"];
export type DoscWin31RequestName = (typeof generatedWin31ParityContract.requestNames)[number];
export type ProductActionState =
  | "ready"
  | "needsDevice"
  | "needsSafetyCheck"
  | "needsConfirmation"
  | "running"
  | "complete"
  | "failed"
  | "unavailable";

export interface ProductMenuItem {
  id: string;
  actionId: string;
  label: string;
  pageId: string;
  targetPage: string;
  capabilityGroup: ProductCapabilityGroup;
  executionMode: ProductExecutionMode;
  state: ProductActionState;
  viewId: ViewId;
  intent: Exclude<IntentId, "navigate" | "select_row">;
  summary: string;
  bridgeActionId?: HostCommandActionId;
  actionClass?: HostCommandActionClass;
  evidenceRef?: string;
}

export interface ProductSection {
  id: string;
  label: string;
  pageId: string;
  targetPage: string;
  capabilityGroup: ProductCapabilityGroup;
  executionMode: ProductExecutionMode;
  state: ProductActionState;
  summary: string;
  evidenceRef?: string;
  items: readonly ProductMenuItem[];
}

export interface ProductPage {
  id: string;
  label: string;
  targetPage: string;
  capabilityGroup: ProductCapabilityGroup;
  executionMode: ProductExecutionMode;
  state: ProductActionState;
  viewId: ViewId;
  summary: string;
  evidenceRef?: string;
  sections: readonly ProductSection[];
}

export interface ProductMenu {
  schema: typeof CBBS_RNW_MENU_SCHEMA;
  appId: CbbsProductWindowsAppId;
  menuId: string;
  label: string;
  sourceXml: string;
  pages: readonly ProductPage[];
}

export interface ProductView {
  id: string;
  label: string;
  viewId: ViewId;
  summary: string;
  pageId?: string;
  parityPageId?: Win31ParityPageId;
  parityDisposition?: Win31ParityCategoryDisposition;
}

export interface ProductAction {
  id: string;
  label: string;
  state: ProductActionState;
  intent: Exclude<IntentId, "navigate" | "select_row">;
  viewId: ViewId;
  summary: string;
  pageId: string;
  executionMode: ProductExecutionMode;
  capabilityGroup?: ProductCapabilityGroup;
  bridgeActionId?: HostCommandActionId;
  actionClass?: HostCommandActionClass;
  evidenceRef?: string;
  menuItemId?: string;
  menuId?: Win31ParityMenuId;
  doscRequestName?: DoscWin31RequestName;
}

export interface ProductPanel {
  id: string;
  title: string;
  body: string;
  state: ProductActionState;
  capabilityGroup?: ProductCapabilityGroup;
  evidenceRef?: string;
}

export interface CbbsProductWindowsAppProfile {
  id: CbbsProductWindowsAppId;
  title: string;
  subtitle: string;
  audience: string;
  platformTitle: string;
  moduleName: string;
  statusLine: string;
  menuLabels: readonly string[];
  parityCoverage?: readonly {
    pageId: Win31ParityPageId;
    disposition: Win31ParityCategoryDisposition;
    reason: string;
  }[];
  views: readonly ProductView[];
  actions: readonly ProductAction[];
  panels: readonly ProductPanel[];
  menu?: ProductMenu;
}

export const win31ParityContract = generatedWin31ParityContract;
export const CBBS_RNW_WIN31_PARITY_CONTRACT_SCHEMA = CBBS_RNW_WIN31_PARITY_SCHEMA;
export const win31SysopPageOrder = win31ParityContract.pages.map((page) => page.label);
export const win31MenuLabels = win31ParityContract.menus.map((menu) => menu.label);
export const win31StatusLine = [
  win31ParityContract.status.label,
  ...win31ParityContract.status.counters
].join(" | ");

const platformTitle = win31ParityContract.visiblePlatform;
const moduleName = win31ParityContract.moduleName;

const clientCoverage = win31ParityContract.roleCoverage.client;
const sysopCoverage = win31ParityContract.roleCoverage.sysop;

const clientViews: ProductView[] = win31ParityContract.pages
  .map((page) => {
    const coverage = clientCoverage.find((entry) => entry.pageId === page.id);
    return { page, coverage };
  })
  .filter(({ coverage }) => coverage?.disposition === "represented")
  .map(({ page, coverage }) => ({
    id: `client-${page.id}`,
    pageId: page.id,
    parityPageId: page.id,
    parityDisposition: coverage?.disposition,
    label: page.label,
    viewId: page.viewId,
    summary: page.summary
  }));

const sysopViews: ProductView[] = win31ParityContract.pages.map((page) => ({
  id: `sysop-${page.id}`,
  pageId: page.id,
  parityPageId: page.id,
  parityDisposition: "represented",
  label: page.label,
  viewId: page.viewId,
  summary: page.summary
}));

export const hardwareToolsMenu = normalizeGeneratedMenu(generatedHardwareToolsMenu);

const hardwareViews: ProductView[] = hardwareToolsMenu.pages.map((page) => ({
  id: `hardware-${page.id}`,
  pageId: page.id,
  label: page.label,
  viewId: page.viewId,
  summary: page.summary
}));

const hardwareActions: ProductAction[] = hardwareToolsMenu.pages.flatMap((page) =>
  page.sections.flatMap((section) =>
    section.items.map((item) => ({
      id: item.actionId,
      label: item.label,
      state: item.state,
      intent: item.intent,
      viewId: item.viewId,
      summary: item.summary,
      pageId: page.id,
      executionMode: item.executionMode,
      capabilityGroup: item.capabilityGroup,
      bridgeActionId: item.bridgeActionId,
      actionClass: item.actionClass,
      evidenceRef: item.evidenceRef,
      menuItemId: item.id
    }))
  )
);

export const cbbsProductWindowsApps: CbbsProductWindowsAppProfile[] = [
  {
    id: "client",
    title: platformTitle,
    subtitle: CBBS_PRODUCT_WINDOWS_APP_SUBTITLES.client,
    audience: "End users and callers",
    platformTitle,
    moduleName,
    statusLine: win31StatusLine,
    menuLabels: win31MenuLabels,
    parityCoverage: clientCoverage,
    views: clientViews,
    actions: [
      {
        id: "client.compose",
        label: "Compose message",
        state: "ready",
        intent: "compose_draft",
        viewId: "messages",
        pageId: "messages",
        executionMode: "localOnly",
        summary: "Start a message draft on this device."
      },
      {
        id: "client.requestDownload",
        label: "Request download",
        state: "ready",
        intent: "queue_file_request",
        viewId: "downloads",
        pageId: "files",
        executionMode: "localOnly",
        summary: "Stage a file request for later transfer."
      },
      {
        id: "client.refresh",
        label: "Refresh status",
        state: "ready",
        intent: "refresh",
        viewId: "home",
        pageId: "status",
        executionMode: "localOnly",
        summary: "Update readiness, counters, and queue notes."
      }
    ],
    panels: [
      {
        id: "client-mailbox",
        title: "Mailbox",
        body: "Unread messages, drafts, and download requests stay easy to scan.",
        state: "ready"
      },
      {
        id: "client-connection",
        title: "Connection",
        body: "Connection notes use redacted station names and do not reveal private identifiers.",
        state: "complete"
      }
    ]
  },
  {
    id: "sysop",
    title: platformTitle,
    subtitle: CBBS_PRODUCT_WINDOWS_APP_SUBTITLES.sysop,
    audience: "System operators",
    platformTitle,
    moduleName,
    statusLine: win31StatusLine,
    menuLabels: win31MenuLabels,
    parityCoverage: sysopCoverage,
    views: sysopViews,
    actions: win31ParityContract.actions.map((action) => ({
      id: action.id,
      label: action.label,
      state: action.state,
      intent: action.intent,
      viewId: action.viewId,
      pageId: action.pageId,
      executionMode: action.executionMode,
      summary: action.summary,
      menuId: action.menuId,
      doscRequestName: action.requestName
    })),
    panels: [
      {
        id: "sysop-link",
        title: "Link Wait",
        body: "Readiness, counters, and queue depth mirror the Win31 status strip.",
        state: "ready"
      },
      {
        id: "sysop-coverage",
        title: "Win31 Coverage",
        body: "Status, messages, files, devices, help, peers, link, updates, setup, diagnostics, and locks are represented.",
        state: "complete"
      }
    ]
  },
  {
    id: "hardware-tools",
    title: platformTitle,
    subtitle: CBBS_PRODUCT_WINDOWS_APP_SUBTITLES["hardware-tools"],
    audience: "Sysops and equipment creators",
    platformTitle,
    moduleName,
    statusLine: win31StatusLine,
    menuLabels: win31MenuLabels,
    parityCoverage: sysopCoverage,
    views: hardwareViews,
    actions: hardwareActions,
    menu: hardwareToolsMenu,
    panels: [
      {
        id: "hardware-target",
        title: "Target Required",
        body: "Targets stay aliased until evidence and authority are complete.",
        state: "needsDevice",
        capabilityGroup: "bench",
        evidenceRef: "bench-readiness"
      },
      {
        id: "hardware-closed-work",
        title: "Closed Work",
        body: "Risky work stays unavailable until target, recovery, and authority steps are complete.",
        state: "needsSafetyCheck",
        capabilityGroup: "safety",
        evidenceRef: "safety-gates"
      },
      {
        id: "hardware-evidence",
        title: "Evidence",
        body: "The tool records reviewed actions, unavailable results, and unresolved gaps.",
        state: "complete",
        capabilityGroup: "activity",
        evidenceRef: "activity-records"
      }
    ]
  }
] as const;

export function getCbbsProductWindowsAppProfile(appId: CbbsProductWindowsAppId): CbbsProductWindowsAppProfile {
  const profile = cbbsProductWindowsApps.find((candidate) => candidate.id === appId);
  if (!profile) {
    throw new Error(`Unknown CBBS product app: ${appId}`);
  }
  return profile;
}

export function getProductPageForView(profile: CbbsProductWindowsAppProfile, view: ProductView): ProductPage | undefined {
  return profile.menu?.pages.find((page) => page.id === view.pageId);
}

export function getProductActionsForPage(
  profile: CbbsProductWindowsAppProfile,
  pageId: string
): readonly ProductAction[] {
  return profile.actions.filter((action) => action.pageId === pageId);
}

export function isActionEnabled(state: ProductActionState): boolean {
  return state === "ready" || state === "complete";
}

export function isProductActionEnabled(action: ProductAction): boolean {
  return (
    isActionEnabled(action.state) &&
    action.executionMode !== "tier3Closed" &&
    action.executionMode !== "bridgePreviewUnavailable"
  );
}

export function canAppendProductTranscript(action: ProductAction): boolean {
  return isProductActionEnabled(action) && (action.executionMode === "localOnly" || action.executionMode === "artifactReview");
}

export function productActionStateLabel(state: ProductActionState): string {
  switch (state) {
    case "ready":
      return "Ready";
    case "needsDevice":
      return "Needs target";
    case "needsSafetyCheck":
      return "Safety check needed";
    case "needsConfirmation":
      return "Authority needed";
    case "running":
      return "Running";
    case "complete":
      return "Complete";
    case "failed":
      return "Failed";
    case "unavailable":
      return "Unavailable";
  }
}

export function productExecutionModeLabel(mode: ProductExecutionMode): string {
  switch (mode) {
    case "localOnly":
      return "Local review";
    case "artifactReview":
      return "Artifact review";
    case "bridgePreviewUnavailable":
      return "Bridge unavailable";
    case "tier3Closed":
      return "Gate closed";
  }
}

function normalizeGeneratedMenu(value: typeof generatedHardwareToolsMenu): ProductMenu {
  return {
    schema: value.schema,
    appId: value.appId,
    menuId: value.menuId,
    label: value.label,
    sourceXml: value.sourceXml,
    pages: value.pages.map((page) => ({
      id: page.id,
      label: page.label,
      targetPage: page.targetPage,
      capabilityGroup: page.capabilityGroup,
      executionMode: page.executionMode,
      state: page.state,
      viewId: page.viewId,
      summary: page.summary,
      evidenceRef: page.evidenceRef || undefined,
      sections: page.sections.map((section) => ({
        id: section.id,
        label: section.label,
        pageId: section.pageId,
        targetPage: section.targetPage,
        capabilityGroup: section.capabilityGroup,
        executionMode: section.executionMode,
        state: section.state,
        summary: section.summary,
        evidenceRef: section.evidenceRef || undefined,
        items: section.items.map((item) => {
          const bridgeActionId = "bridgeActionId" in item ? item.bridgeActionId : undefined;
          return {
            id: item.id,
            actionId: item.actionId,
            label: item.label,
            pageId: item.pageId,
            targetPage: item.targetPage,
            capabilityGroup: item.capabilityGroup,
            executionMode: item.executionMode,
            state: item.state,
            viewId: item.viewId,
            intent: item.intent,
            summary: item.summary,
            bridgeActionId,
            actionClass: bridgeActionId ? actionClassForItem(item.actionId, item.executionMode) : undefined,
            evidenceRef: item.evidenceRef || undefined
          };
        })
      }))
    }))
  };
}

function actionClassForItem(actionId: string, mode: ProductExecutionMode): HostCommandActionClass {
  if (mode === "tier3Closed" && actionId.includes("deviceUpdate")) {
    return "install";
  }
  if (mode === "tier3Closed" || actionId.includes("Change")) {
    return "change";
  }
  return "read";
}
