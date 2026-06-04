import { useState } from "react";
import { Pressable, ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import {
  canAppendProductTranscript,
  getCbbsProductWindowsAppProfile,
  getProductActionsForPage,
  getProductPageForView,
  isProductActionEnabled,
  productActionStateLabel,
  productExecutionModeLabel,
  type CbbsProductWindowsAppId,
  type ProductAction,
  type ProductActionState,
  type ProductSection,
  type ProductView
} from "@cbbs/product";
import {
  HOST_COMMAND_UNAVAILABLE_REASON,
  createUnavailableHostCommandResult,
  localIntent,
  type AppRole,
  type HostCommandBridgeResult,
  type UiIntentRecord,
  type ViewId
} from "@cbbs/protocol";

export interface ProductWindowsShellProps {
  appId: CbbsProductWindowsAppId;
  onIntent?: (intent: UiIntentRecord) => void;
}

interface TranscriptEntry {
  id: string;
  title: string;
  detail: string;
  status: string;
  result?: HostCommandBridgeResult;
}

type MenuName = "session" | "views" | "messages" | "files" | "devices" | "style" | "help";

const menuOrder: readonly MenuName[] = ["session", "views", "messages", "files", "devices", "style", "help"];

const initialTranscript: TranscriptEntry[] = [
  {
    id: "transcript-001",
    title: "Surface opened",
    detail: "Link wait; In 0; Out 0 Err 0; Queue 0.",
    status: "Evidence"
  }
];

export function ProductWindowsShell({ appId, onIntent = () => undefined }: ProductWindowsShellProps) {
  const profile = getCbbsProductWindowsAppProfile(appId);
  const [activeViewId, setActiveViewId] = useState(profile.views[0]?.id ?? "home");
  const [selectedActionId, setSelectedActionId] = useState("");
  const [openMenu, setOpenMenu] = useState<MenuName | null>(null);
  const [gatePhrase, setGatePhrase] = useState("");
  const [transcript, setTranscript] = useState<TranscriptEntry[]>(initialTranscript);
  const activeView = profile.views.find((view) => view.id === activeViewId) ?? profile.views[0];
  const activePageId = activeView?.pageId ?? activeView?.id ?? "home";
  const activePage = activeView ? getProductPageForView(profile, activeView) : undefined;
  const pageActions = getProductActionsForPage(profile, activePageId);

  const appendTranscript = (entry: Omit<TranscriptEntry, "id">) => {
    setTranscript((entries) => {
      const nextNumber =
        entries.reduce((maxNumber, transcriptEntry) => {
          const entryNumber = Number(transcriptEntry.id.replace("transcript-", ""));
          return Number.isFinite(entryNumber) ? Math.max(maxNumber, entryNumber) : maxNumber;
        }, 0) + 1;

      return [
        {
          id: `transcript-${String(nextNumber).padStart(3, "0")}`,
          ...entry
        },
        ...entries
      ].slice(0, 6);
    });
  };

  const selectView = (view: ProductView) => {
    setActiveViewId(view.id);
    setOpenMenu(null);
    onIntent(localIntent("navigate", roleForApp(appId), view.viewId, { targetView: view.viewId }));
    appendTranscript({
      title: `${view.label} opened`,
      detail: view.summary,
      status: "View"
    });
  };

  const recordLocalIntent = (action: ProductAction) => {
    setSelectedActionId(action.id);
    setOpenMenu(null);
    if (!isProductActionEnabled(action) || !canAppendProductTranscript(action)) {
      return;
    }
    onIntent(
      localIntent(action.intent, roleForApp(appId), action.viewId, {
        proofId: `${appId}-${aliasForAction(action.id)}-note`
      })
    );
    appendTranscript({
      title: action.label,
      detail: action.summary,
      status: productExecutionModeLabel(action.executionMode),
      result: action.bridgeActionId ? unavailableResultForAction(action) : undefined
    });
  };

  return (
    <ScrollView testID={`windows-${appId}-shell`} contentContainerStyle={styles.shell}>
      <View testID={`windows-${appId}-banner`} style={styles.titleBar}>
        <View>
          <Text style={styles.eyebrow}>{profile.audience}</Text>
          <Text style={styles.title}>{profile.title}</Text>
          <Text style={styles.subtitle}>{profile.subtitle}</Text>
        </View>
        <View style={styles.statusBlock}>
          <View style={[styles.statusLamp, styles.statusLampAmber]} />
          <Text style={styles.statusText}>{profile.statusLine}</Text>
        </View>
      </View>

      <View testID={`windows-${appId}-menubar`} style={styles.menuBar}>
        {menuOrder.map((menuName, index) => (
          <Pressable
            key={menuName}
            testID={`windows-${appId}-menu-${menuName}`}
            accessibilityLabel={`${menuName} menu`}
            accessibilityRole="button"
            accessibilityState={{ expanded: openMenu === menuName }}
            onPress={() => setOpenMenu((current) => (current === menuName ? null : menuName))}
            style={[styles.menuButton, openMenu === menuName ? styles.menuButtonOpen : undefined]}
          >
            <Text style={styles.menuText}>{profile.menuLabels[index] ?? labelForMenu(menuName)}</Text>
          </Pressable>
        ))}
      </View>
      {openMenu ? (
        <View testID={`windows-${appId}-dropdown-${openMenu}`} style={styles.dropdown}>
          {renderDropdown(openMenu, appId, profile.views, profile.actions, pageActions, selectView, recordLocalIntent)}
        </View>
      ) : null}

      <View testID={`windows-${appId}-body`} style={styles.body}>
        <View testID={`windows-${appId}-nav`} style={styles.pageList}>
          <Text style={styles.columnHeader}>Pages</Text>
          {profile.views.map((view) => (
            <Pressable
              key={view.id}
              testID={`windows-${appId}-page-${view.pageId ?? view.id}`}
              accessibilityLabel={`Open ${view.label}`}
              accessibilityRole="button"
              accessibilityState={{ selected: activeView?.id === view.id }}
              onPress={() => selectView(view)}
              style={[styles.pageButton, activeView?.id === view.id ? styles.pageButtonActive : undefined]}
            >
              <View style={[styles.statusLamp, activeView?.id === view.id ? styles.statusLampGreen : styles.statusLampViolet]} />
              <Text style={[styles.pageText, activeView?.id === view.id ? styles.pageTextActive : undefined]}>
                {view.label}
              </Text>
            </Pressable>
          ))}
        </View>

        <View testID={`windows-${appId}-workspace`} style={styles.workspace}>
          <View style={styles.workspaceHeader}>
            <View>
              <Text style={styles.sectionTitle}>{activeView?.label ?? "Home"}</Text>
              <Text style={styles.bodyText}>{activeView?.summary ?? profile.subtitle}</Text>
            </View>
            <Text style={styles.modeText}>
              {activePage ? productExecutionModeLabel(activePage.executionMode) : "Local review"}
            </Text>
          </View>

          {activePage ? (
            activePage.sections.map((section) => (
              <SectionView
                key={section.id}
                appId={appId}
                section={section}
                actions={pageActions.filter((action) => action.menuItemId && section.items.some((item) => item.id === action.menuItemId))}
                selectedActionId={selectedActionId}
                onAction={recordLocalIntent}
              />
            ))
          ) : (
            <SectionView
              appId={appId}
              section={{
                id: `${activePageId}-section`,
                label: activeView?.label ?? "Work",
                pageId: activePageId,
                targetPage: activePageId,
                capabilityGroup: "activity",
                executionMode: "localOnly",
                state: "ready",
                summary: activeView?.summary ?? profile.subtitle,
                items: []
              }}
              actions={pageActions}
              selectedActionId={selectedActionId}
              onAction={recordLocalIntent}
            />
          )}
        </View>

        <View testID={`windows-${appId}-side-panel`} style={styles.evidenceRail}>
          <Text style={styles.columnHeader}>Evidence</Text>
          {activePage ? (
            <View testID={`windows-${appId}-evidence-${activePage.id}`} style={styles.railPanel}>
              <Text style={styles.panelTitle}>{activePage.label}</Text>
              <Text style={styles.panelBody}>{activePage.summary}</Text>
              <Text style={styles.panelState}>{productActionStateLabel(activePage.state)}</Text>
            </View>
          ) : null}
          {profile.panels.map((panel) => (
            <View key={panel.id} testID={`windows-${appId}-panel-${panel.id}`} style={styles.railPanel}>
              <Text style={styles.panelTitle}>{panel.title}</Text>
              <Text style={styles.panelBody}>{panel.body}</Text>
              <Text style={styles.panelState}>{productActionStateLabel(panel.state)}</Text>
            </View>
          ))}

          {appId === "hardware-tools" ? (
            <View style={styles.railPanel}>
              <Text style={styles.panelTitle}>Gate Phrase</Text>
              <TextInput
                testID="windows-hardware-tools-gate-phrase"
                accessibilityLabel="Gate phrase"
                value={gatePhrase}
                onChangeText={setGatePhrase}
                placeholder="Record gate phrase"
                placeholderTextColor="#93A4B8"
                style={styles.input}
              />
              <Text style={styles.panelBody}>Gate phrase records notes but does not unlock closed work.</Text>
            </View>
          ) : null}
        </View>
      </View>

      <View testID={`windows-${appId}-transcript`} style={styles.transcript}>
        <View style={styles.transcriptHeader}>
          <Text style={styles.columnHeader}>Transcript</Text>
          <Text style={styles.modeText}>bounded</Text>
        </View>
        {transcript.map((entry) => (
          <View key={entry.id} testID={`windows-${appId}-${entry.id}`} style={styles.transcriptRow}>
            <Text style={styles.transcriptTitle}>{entry.title}</Text>
            <Text style={styles.transcriptText}>{entry.detail}</Text>
            <Text style={styles.transcriptMeta}>{entry.status}</Text>
            {entry.result ? (
              <View testID={`windows-${appId}-${entry.id}-bridge-result`} style={styles.bridgeResult}>
                <Text style={styles.transcriptMeta}>reason: {entry.result.reason}</Text>
                <Text style={styles.transcriptMeta}>executed: {String(entry.result.executed)}</Text>
                <Text style={styles.transcriptMeta}>available: {String(entry.result.available)}</Text>
                <Text style={styles.transcriptMeta}>noSecretScan: {String(entry.result.noSecretScan)}</Text>
                <Text style={styles.transcriptMeta}>transcriptRef: {entry.result.transcriptRef}</Text>
              </View>
            ) : null}
          </View>
        ))}
      </View>
    </ScrollView>
  );
}

function SectionView({
  appId,
  section,
  actions,
  selectedActionId,
  onAction
}: {
  appId: CbbsProductWindowsAppId;
  section: ProductSection;
  actions: readonly ProductAction[];
  selectedActionId: string;
  onAction: (action: ProductAction) => void;
}) {
  return (
    <View testID={`windows-${appId}-section-${section.id}`} style={styles.section}>
      <View style={styles.sectionHeader}>
        <Text style={styles.sectionSubtitle}>{section.label}</Text>
        <Text style={styles.modeText}>{productExecutionModeLabel(section.executionMode)}</Text>
      </View>
      <Text style={styles.bodyText}>{section.summary}</Text>
      <View style={styles.table}>
        {actions.map((action) => {
          const enabled = isProductActionEnabled(action);
          return (
            <Pressable
              key={action.id}
              testID={`windows-${appId}-action-${action.id}`}
              accessibilityLabel={action.label}
              accessibilityRole="button"
              accessibilityState={{ disabled: !enabled, selected: selectedActionId === action.id }}
              disabled={!enabled}
              onPress={enabled ? () => onAction(action) : undefined}
              style={[styles.tableRow, enabled ? styles.tableRowReady : styles.tableRowDisabled]}
            >
              <View style={styles.rowTitleCell}>
                <View style={[styles.statusLamp, lampStyleForState(action.state)]} />
                <Text style={styles.actionLabel}>{action.label}</Text>
              </View>
              <Text style={styles.actionState}>{productActionStateLabel(action.state)}</Text>
              <Text style={styles.actionMode}>{productExecutionModeLabel(action.executionMode)}</Text>
              <Text style={styles.actionSummary}>{action.summary}</Text>
            </Pressable>
          );
        })}
      </View>
    </View>
  );
}

function renderDropdown(
  menuName: MenuName,
  appId: CbbsProductWindowsAppId,
  views: readonly ProductView[],
  allActions: readonly ProductAction[],
  pageActions: readonly ProductAction[],
  selectView: (view: ProductView) => void,
  recordLocalIntent: (action: ProductAction) => void
) {
  if (menuName === "views") {
    return views.map((view) => (
      <Pressable
        key={view.id}
        testID={`windows-${appId}-dropdown-views-${view.pageId ?? view.id}`}
        accessibilityRole="menuitem"
        onPress={() => selectView(view)}
        style={styles.dropdownItem}
      >
        <Text style={styles.dropdownText}>{view.label}</Text>
      </Pressable>
    ));
  }
  if (menuName === "style") {
    return (
      <View testID={`windows-${appId}-dropdown-style-summary`} style={styles.dropdownStatic}>
        <Text style={styles.dropdownText}>Windows 3.1</Text>
        <Text style={styles.dropdownHint}>ANSI Terminal</Text>
      </View>
    );
  }
  if (menuName === "help") {
    return (
      <View testID={`windows-${appId}-dropdown-help-summary`} style={styles.dropdownStatic}>
        <Text style={styles.dropdownText}>About</Text>
        <Text style={styles.dropdownHint}>OG Communication Retro3.1 CBBS</Text>
      </View>
    );
  }
  const menuActions = actionsForMenu(menuName, appId, allActions, pageActions);
  if (menuActions.length > 0) {
    return menuActions.map((action) => {
      const enabled = isProductActionEnabled(action);
      return (
      <Pressable
        key={action.id}
        testID={`windows-${appId}-dropdown-${menuName}-${action.id}`}
        accessibilityRole="menuitem"
        accessibilityState={{ disabled: !enabled }}
        disabled={!enabled}
        onPress={enabled ? () => recordLocalIntent(action) : undefined}
        style={styles.dropdownItem}
      >
        <Text style={styles.dropdownText}>{action.label}</Text>
      </Pressable>
      );
    });
  }
  return (
    <View testID={`windows-${appId}-dropdown-${menuName}-summary`} style={styles.dropdownStatic}>
      <Text style={styles.dropdownText}>{labelForMenu(menuName)}</Text>
      <Text style={styles.dropdownHint}>{HOST_COMMAND_UNAVAILABLE_REASON}</Text>
    </View>
  );
}

function actionsForMenu(
  menuName: MenuName,
  appId: CbbsProductWindowsAppId,
  allActions: readonly ProductAction[],
  pageActions: readonly ProductAction[]
): readonly ProductAction[] {
  if (appId === "hardware-tools" && menuName === "devices") {
    return pageActions;
  }
  if (menuName === "session") {
    return allActions.filter((action) => action.menuId === "session" || action.intent === "refresh");
  }
  if (menuName === "messages") {
    return allActions.filter((action) => action.menuId === "messages" || action.viewId === "messages");
  }
  if (menuName === "files") {
    return allActions.filter((action) => action.menuId === "files" || action.viewId === "downloads");
  }
  if (menuName === "devices") {
    return allActions.filter((action) => action.menuId === "devices" || action.viewId === "diagnostics" || action.viewId === "config");
  }
  return [];
}

function labelForMenu(menuName: MenuName): string {
  switch (menuName) {
    case "session":
      return "Session";
    case "views":
      return "Views";
    case "messages":
      return "Messages";
    case "files":
      return "Files";
    case "devices":
      return "Devices";
    case "style":
      return "Style";
    case "help":
      return "Help";
  }
}

function roleForApp(appId: CbbsProductWindowsAppId): AppRole {
  if (appId === "client") {
    return "client";
  }
  return "sysop";
}

export function firstViewForApp(appId: CbbsProductWindowsAppId): ViewId {
  return getCbbsProductWindowsAppProfile(appId).views[0]?.viewId ?? "home";
}

function unavailableResultForAction(action: ProductAction): HostCommandBridgeResult {
  return createUnavailableHostCommandResult(
    { requestId: `${aliasForAction(action.id)}-preview`.slice(0, 64) },
    "2026-06-03T00:00:00.000Z"
  );
}

function aliasForAction(value: string): string {
  return value
    .replace(/([a-z])([A-Z])/g, "$1-$2")
    .replace(/[^a-z0-9]+/gi, "-")
    .replace(/^-+|-+$/g, "")
    .toLowerCase()
    .slice(0, 48);
}

function lampStyleForState(state: ProductActionState) {
  switch (state) {
    case "ready":
    case "complete":
      return styles.statusLampGreen;
    case "needsDevice":
    case "needsSafetyCheck":
    case "needsConfirmation":
      return styles.statusLampAmber;
    case "running":
      return styles.statusLampViolet;
    case "failed":
    case "unavailable":
      return styles.statusLampRed;
  }
}

const styles = StyleSheet.create({
  shell: {
    backgroundColor: "#05070A",
    gap: 8,
    minHeight: "100%",
    padding: 10
  },
  titleBar: {
    alignItems: "center",
    backgroundColor: "#0B1118",
    borderColor: "#2A3B47",
    borderRadius: 4,
    borderWidth: 1,
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-between",
    gap: 10,
    padding: 10
  },
  eyebrow: {
    color: "#66D9EF",
    fontSize: 11,
    fontWeight: "700"
  },
  title: {
    color: "#F8FAFC",
    fontSize: 22,
    fontWeight: "800"
  },
  subtitle: {
    color: "#C9D6E2",
    fontSize: 13,
    lineHeight: 18
  },
  statusBlock: {
    alignItems: "center",
    borderColor: "#2A3B47",
    borderRadius: 4,
    borderWidth: 1,
    flexDirection: "row",
    flexShrink: 1,
    gap: 6,
    paddingHorizontal: 8,
    paddingVertical: 5
  },
  statusLamp: {
    borderRadius: 2,
    height: 9,
    width: 9
  },
  statusLampGreen: {
    backgroundColor: "#22C55E"
  },
  statusLampAmber: {
    backgroundColor: "#F59E0B"
  },
  statusLampRed: {
    backgroundColor: "#EF4444"
  },
  statusLampViolet: {
    backgroundColor: "#8B5CF6"
  },
  statusText: {
    color: "#E7F7EE",
    fontSize: 12,
    fontWeight: "800"
  },
  menuBar: {
    backgroundColor: "#111827",
    borderColor: "#2A3B47",
    borderRadius: 4,
    borderWidth: 1,
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 4,
    padding: 4
  },
  menuButton: {
    borderColor: "#334155",
    borderRadius: 3,
    borderWidth: 1,
    paddingHorizontal: 10,
    paddingVertical: 5
  },
  menuButtonOpen: {
    backgroundColor: "#173549",
    borderColor: "#38BDF8"
  },
  menuText: {
    color: "#D7E3EE",
    fontSize: 11,
    fontWeight: "800"
  },
  dropdown: {
    alignSelf: "flex-start",
    backgroundColor: "#0F172A",
    borderColor: "#38BDF8",
    borderRadius: 4,
    borderWidth: 1,
    minWidth: 220,
    padding: 4
  },
  dropdownItem: {
    borderBottomColor: "#1F3340",
    borderBottomWidth: 1,
    paddingHorizontal: 8,
    paddingVertical: 7
  },
  dropdownStatic: {
    gap: 2,
    paddingHorizontal: 8,
    paddingVertical: 7
  },
  dropdownText: {
    color: "#FFFFFF",
    fontSize: 12,
    fontWeight: "800"
  },
  dropdownHint: {
    color: "#A5B4C3",
    fontSize: 11,
    fontWeight: "700"
  },
  body: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 8
  },
  pageList: {
    backgroundColor: "#0B1118",
    borderColor: "#2A3B47",
    borderRadius: 4,
    borderWidth: 1,
    gap: 5,
    flexGrow: 0,
    flexShrink: 0,
    minWidth: 148,
    padding: 8
  },
  columnHeader: {
    color: "#E2E8F0",
    fontSize: 12,
    fontWeight: "900"
  },
  pageButton: {
    alignItems: "center",
    borderColor: "#2A3B47",
    borderRadius: 3,
    borderWidth: 1,
    flexDirection: "row",
    gap: 7,
    paddingHorizontal: 8,
    paddingVertical: 7
  },
  pageButtonActive: {
    backgroundColor: "#173549",
    borderColor: "#38BDF8"
  },
  pageText: {
    color: "#D7E3EE",
    fontSize: 12,
    fontWeight: "800"
  },
  pageTextActive: {
    color: "#FFFFFF"
  },
  workspace: {
    backgroundColor: "#0B1118",
    borderColor: "#2A3B47",
    borderRadius: 4,
    borderWidth: 1,
    flex: 1,
    flexBasis: 320,
    flexShrink: 1,
    gap: 8,
    minWidth: 280,
    padding: 10
  },
  workspaceHeader: {
    alignItems: "flex-start",
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-between",
    gap: 8
  },
  sectionTitle: {
    color: "#FFFFFF",
    fontSize: 18,
    fontWeight: "900"
  },
  sectionSubtitle: {
    color: "#F8FAFC",
    fontSize: 14,
    fontWeight: "900"
  },
  modeText: {
    color: "#C4B5FD",
    fontSize: 11,
    fontWeight: "800"
  },
  bodyText: {
    color: "#C9D6E2",
    flexShrink: 1,
    fontSize: 12,
    lineHeight: 17
  },
  section: {
    borderColor: "#1F3340",
    borderRadius: 4,
    borderWidth: 1,
    gap: 7,
    padding: 8
  },
  sectionHeader: {
    alignItems: "center",
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-between",
    gap: 8
  },
  table: {
    borderColor: "#2A3B47",
    borderRadius: 3,
    borderWidth: 1
  },
  tableRow: {
    borderBottomColor: "#1F3340",
    borderBottomWidth: 1,
    gap: 5,
    minHeight: 72,
    padding: 8
  },
  tableRowReady: {
    backgroundColor: "#071F28"
  },
  tableRowDisabled: {
    backgroundColor: "#190F13",
    opacity: 0.82
  },
  rowTitleCell: {
    alignItems: "center",
    flexDirection: "row",
    flexWrap: "wrap",
    gap: 7
  },
  actionLabel: {
    color: "#FFFFFF",
    flexShrink: 1,
    fontSize: 13,
    fontWeight: "900"
  },
  actionState: {
    color: "#FDE68A",
    fontSize: 11,
    fontWeight: "800"
  },
  actionMode: {
    color: "#BAE6FD",
    fontSize: 11,
    fontWeight: "800"
  },
  actionSummary: {
    color: "#C9D6E2",
    fontSize: 12,
    lineHeight: 16
  },
  evidenceRail: {
    backgroundColor: "#0B1118",
    borderColor: "#2A3B47",
    borderRadius: 4,
    borderWidth: 1,
    gap: 8,
    flexBasis: 260,
    flexGrow: 1,
    flexShrink: 1,
    maxWidth: 340,
    minWidth: 260,
    padding: 8
  },
  railPanel: {
    borderColor: "#1F3340",
    borderRadius: 4,
    borderWidth: 1,
    gap: 6,
    padding: 8
  },
  panelTitle: {
    color: "#FFFFFF",
    fontSize: 13,
    fontWeight: "900"
  },
  panelBody: {
    color: "#C9D6E2",
    fontSize: 12,
    lineHeight: 17
  },
  panelState: {
    color: "#C4B5FD",
    fontSize: 11,
    fontWeight: "900"
  },
  input: {
    borderColor: "#64748B",
    borderRadius: 3,
    borderWidth: 1,
    color: "#FFFFFF",
    fontSize: 12,
    paddingHorizontal: 8,
    paddingVertical: 7
  },
  transcript: {
    backgroundColor: "#0B1118",
    borderColor: "#2A3B47",
    borderRadius: 4,
    borderWidth: 1,
    gap: 7,
    padding: 8
  },
  transcriptHeader: {
    alignItems: "center",
    flexDirection: "row",
    justifyContent: "space-between"
  },
  transcriptRow: {
    borderColor: "#1F3340",
    borderRadius: 3,
    borderWidth: 1,
    gap: 4,
    padding: 7
  },
  transcriptTitle: {
    color: "#FFFFFF",
    fontSize: 12,
    fontWeight: "900"
  },
  transcriptText: {
    color: "#C9D6E2",
    fontSize: 12,
    lineHeight: 16
  },
  transcriptMeta: {
    color: "#BAE6FD",
    fontSize: 11,
    fontWeight: "800"
  },
  bridgeResult: {
    borderColor: "#334155",
    borderRadius: 3,
    borderWidth: 1,
    gap: 2,
    padding: 6
  }
});
