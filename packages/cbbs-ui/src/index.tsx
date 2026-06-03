import { Text, Pressable, ScrollView, StyleSheet, View } from "react-native";
import { describeProof } from "@cbbs/evidence";
import type { CbbsFixtureSnapshot, FixtureClosedSurface, FixtureRow } from "@cbbs/fixtures";
import { INTENT_IDS, localIntent, type UiIntentRecord, type ViewId } from "@cbbs/protocol";
import type { CbbsClientState } from "@cbbs/state";
import { cbbsTheme } from "@cbbs/theme";

export interface OperatorShellProps {
  snapshot: CbbsFixtureSnapshot;
  state: CbbsClientState;
  onIntent: (intent: UiIntentRecord) => void;
}

export function OperatorShell({ snapshot, state, onIntent }: OperatorShellProps) {
  const rows = snapshot.rows.filter((row) => row.view === state.activeView);
  const proof = snapshot.evidence[0];
  const roleProfile =
    snapshot.roleProfiles.find((profile) => profile.role === state.role) ?? snapshot.roleProfiles[0];
  const visibleViewIds = roleProfile?.viewIds ?? snapshot.views.map((view) => view.id);

  return (
    <ScrollView contentContainerStyle={styles.shell}>
      <View style={styles.header}>
        <Text style={styles.title}>CBBS</Text>
        <Text style={styles.subtitle}>Fixture-only {roleProfile?.label ?? state.role} console</Text>
      </View>

      <View style={styles.tabs}>
        {visibleViewIds.map((viewId) => (
          <Pressable
            key={viewId}
            testID={`cbbs-view-tab-${viewId}`}
            accessibilityLabel={`Open ${viewId} fixture view`}
            accessibilityRole="button"
            accessibilityState={{ selected: state.activeView === viewId }}
            onPress={() => onIntent(localIntent("navigate", state.role, state.activeView, { targetView: viewId }))}
            style={[styles.tab, state.activeView === viewId ? styles.tabActive : undefined]}
          >
            <Text style={state.activeView === viewId ? styles.tabTextActive : styles.tabText}>
              {viewId.toUpperCase()}
            </Text>
          </Pressable>
        ))}
      </View>

      <View style={styles.panel}>
        <Text style={styles.panelTitle}>{state.activeView.toUpperCase()}</Text>
        <Text style={styles.panelBody}>
          {snapshot.views.find((view) => view.id === state.activeView)?.summary}
        </Text>
        {rows.map((row) => (
          <FixtureRowView key={row.id} row={row} state={state} onIntent={onIntent} />
        ))}
      </View>

      <View style={styles.panel}>
        <Text style={styles.panelTitle}>Local Actions</Text>
        <View style={styles.actionGrid}>
          {INTENT_IDS.filter((intent) => intent !== "navigate" && intent !== "select_row").map((intent) => (
            <LocalActionButton
              key={intent}
              intent={intent}
              proofId={proof?.id}
              rowId={rows[0]?.id}
              state={state}
              onIntent={onIntent}
            />
          ))}
        </View>
      </View>

      <View style={styles.panel}>
        <Text style={styles.panelTitle}>Closed Authority</Text>
        {snapshot.closedSurfaces.map((surface) => (
          <ClosedSurfaceControl key={surface.id} surface={surface} />
        ))}
      </View>

      <View style={styles.panel}>
        <Text style={styles.panelTitle}>Evidence</Text>
        <Text style={styles.panelBody}>
          {proof
            ? `${proof.id}: ${describeProof(proof.label)} ${proof.summary}`
            : "Transcript-first fixture evidence only. Fixture-only; no live browser or device proof."}
        </Text>
      </View>
    </ScrollView>
  );
}

function LocalActionButton({
  intent,
  proofId,
  rowId,
  state,
  onIntent
}: {
  intent: Exclude<UiIntentRecord["intent"], "navigate" | "select_row">;
  proofId?: string;
  rowId?: string;
  state: CbbsClientState;
  onIntent: (intent: UiIntentRecord) => void;
}) {
  return (
    <Pressable
      testID={`cbbs-action-${intent}`}
      accessibilityLabel={`${intent.replaceAll("_", " ")} local fixture action`}
      accessibilityRole="button"
      onPress={() => onIntent(buildLocalActionIntent(intent, state.role, state.activeView, rowId, proofId))}
      style={styles.actionButton}
    >
      <Text style={styles.actionText}>{intent.replaceAll("_", " ").toUpperCase()}</Text>
    </Pressable>
  );
}

function buildLocalActionIntent(
  intent: Exclude<UiIntentRecord["intent"], "navigate" | "select_row">,
  role: CbbsClientState["role"],
  activeView: ViewId,
  rowId?: string,
  proofId?: string
): UiIntentRecord {
  switch (intent) {
    case "filter":
      return localIntent(intent, role, activeView, { filter: "fixture-filter" });
    case "open_detail":
      return localIntent(intent, role, activeView, { rowId: rowId ?? "row-home-local" });
    case "compose_draft":
      return localIntent(intent, role, activeView, { draftText: "local draft placeholder" });
    case "queue_file_request":
      return localIntent(intent, role, activeView, { rowId: "row-download-request" });
    case "view_proof":
      return localIntent(intent, role, activeView, { proofId: proofId ?? "proof-local-transcript-note" });
    case "refresh":
    case "ack_local":
      return localIntent(intent, role, activeView);
  }
}

function ClosedSurfaceControl({ surface }: { surface: FixtureClosedSurface }) {
  return (
    <Pressable
      testID={`cbbs-closed-surface-${surface.id}`}
      accessibilityLabel={`${surface.label} disabled`}
      accessibilityRole="button"
      accessibilityState={{ disabled: true }}
      disabled
      style={styles.disabledControl}
    >
      <Text style={styles.rowTitle}>{surface.label}</Text>
      <Text style={styles.panelBody}>{surface.gateLabel}</Text>
    </Pressable>
  );
}

function FixtureRowView({
  row,
  state,
  onIntent
}: {
  row: FixtureRow;
  state: CbbsClientState;
  onIntent: (intent: UiIntentRecord) => void;
}) {
  return (
    <Pressable
      testID={`cbbs-row-${row.id}`}
      accessibilityLabel={`Select ${row.title}`}
      accessibilityRole="button"
      accessibilityState={{ selected: state.selectedRowId === row.id }}
      onPress={() => onIntent(localIntent("select_row", state.role, state.activeView, { rowId: row.id }))}
      style={styles.row}
    >
      <Text style={styles.rowTitle}>{row.title}</Text>
      <Text style={styles.rowMeta}>{row.status.toUpperCase()}</Text>
      <Text style={styles.panelBody}>{row.detail}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  shell: {
    backgroundColor: cbbsTheme.colors.background,
    gap: cbbsTheme.spacing.md,
    minHeight: "100%",
    padding: cbbsTheme.spacing.lg
  },
  header: {
    gap: cbbsTheme.spacing.xs
  },
  title: {
    color: cbbsTheme.colors.text,
    fontSize: 28,
    fontWeight: "700"
  },
  subtitle: {
    color: cbbsTheme.colors.mutedText,
    fontSize: 14
  },
  tabs: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: cbbsTheme.spacing.sm
  },
  tab: {
    borderColor: cbbsTheme.colors.line,
    borderRadius: cbbsTheme.radius.sm,
    borderWidth: 1,
    paddingHorizontal: cbbsTheme.spacing.md,
    paddingVertical: cbbsTheme.spacing.sm
  },
  tabActive: {
    backgroundColor: cbbsTheme.colors.command,
    borderColor: cbbsTheme.colors.command
  },
  tabText: {
    color: cbbsTheme.colors.text,
    fontSize: 12,
    fontWeight: "600"
  },
  tabTextActive: {
    color: "#FFFFFF",
    fontSize: 12,
    fontWeight: "700"
  },
  panel: {
    backgroundColor: cbbsTheme.colors.panel,
    borderColor: cbbsTheme.colors.line,
    borderRadius: cbbsTheme.radius.md,
    borderWidth: 1,
    gap: cbbsTheme.spacing.sm,
    padding: cbbsTheme.spacing.md
  },
  panelTitle: {
    color: cbbsTheme.colors.text,
    fontSize: 16,
    fontWeight: "700"
  },
  panelBody: {
    color: cbbsTheme.colors.mutedText,
    fontSize: 14,
    lineHeight: 20
  },
  row: {
    borderColor: cbbsTheme.colors.line,
    borderRadius: cbbsTheme.radius.sm,
    borderWidth: 1,
    gap: cbbsTheme.spacing.xs,
    padding: cbbsTheme.spacing.sm
  },
  rowTitle: {
    color: cbbsTheme.colors.text,
    fontSize: 14,
    fontWeight: "700"
  },
  rowMeta: {
    color: cbbsTheme.colors.disabled,
    fontSize: 11,
    fontWeight: "700"
  },
  actionGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    gap: cbbsTheme.spacing.sm
  },
  actionButton: {
    borderColor: cbbsTheme.colors.command,
    borderRadius: cbbsTheme.radius.sm,
    borderWidth: 1,
    paddingHorizontal: cbbsTheme.spacing.md,
    paddingVertical: cbbsTheme.spacing.sm
  },
  actionText: {
    color: cbbsTheme.colors.command,
    fontSize: 11,
    fontWeight: "700"
  },
  disabledControl: {
    borderColor: cbbsTheme.colors.line,
    borderRadius: cbbsTheme.radius.sm,
    borderWidth: 1,
    gap: cbbsTheme.spacing.xs,
    opacity: 0.65,
    padding: cbbsTheme.spacing.sm
  }
});
