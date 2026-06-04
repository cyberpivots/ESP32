import {
  CBBS_PRODUCT_WINDOWS_APP_IDS,
  PRODUCT_EXECUTION_MODES,
  cbbsProductWindowsApps,
  canAppendProductTranscript,
  getCbbsProductWindowsAppProfile,
  getProductActionsForPage,
  hardwareToolsMenu,
  isActionEnabled,
  isProductActionEnabled,
  win31ParityContract,
  win31StatusLine,
  win31SysopPageOrder,
  productActionStateLabel
} from "../src";

describe("CBBS product model", () => {
  test("pins the three Windows product apps", () => {
    expect(CBBS_PRODUCT_WINDOWS_APP_IDS).toEqual(["client", "sysop", "hardware-tools"]);
    expect(cbbsProductWindowsApps.map((app) => app.title)).toEqual([
      "OG Communication Retro3.1",
      "OG Communication Retro3.1",
      "OG Communication Retro3.1"
    ]);
    expect(cbbsProductWindowsApps.map((app) => app.subtitle)).toEqual([
      "CBBS Client",
      "CBBS Sysop",
      "CBBS Hardware Tools"
    ]);
  });

  test("loads the generated Win31 parity contract", () => {
    expect(win31ParityContract.schema).toBe("cbbs_rnw_win31_parity.v1");
    expect(win31ParityContract.visiblePlatform).toBe("OG Communication Retro3.1");
    expect(win31ParityContract.moduleName).toBe("CBBS");
    expect(win31SysopPageOrder).toEqual([
      "Status",
      "Messages",
      "Files",
      "Devices",
      "Help",
      "Peers",
      "Link",
      "Updates",
      "Setup",
      "Diagnostics",
      "Locks"
    ]);
    expect(win31StatusLine).toBe("Link wait | In 0 | Out 0 Err 0 | Queue 0");
    expect(win31ParityContract.requestNames).toEqual([
      "hello",
      "state_get",
      "peer_list",
      "msg_pull",
      "msg_search",
      "msg_post",
      "msg_ack",
      "diag_get",
      "fw_inventory",
      "coordinator_state",
      "maint_intent",
      "download_list",
      "download_queue",
      "download_status",
      "discovery_snapshot",
      "discovery_events",
      "service_catalog",
      "capability_report",
      "otap_status",
      "otap_intent"
    ]);
  });

  test("loads the generated Hardware Tools menu", () => {
    expect(hardwareToolsMenu.schema).toBe("cbbs_rnw_menu.v1");
    expect(hardwareToolsMenu.sourceXml).toBe("cbbs_rnw_menu.v1.xml");
    expect(hardwareToolsMenu.pages.map((page) => page.label)).toEqual([
      "Bench",
      "Radio",
      "Mesh",
      "Firmware",
      "Fabrication",
      "Safety",
      "Activity"
    ]);
    expect(PRODUCT_EXECUTION_MODES).toEqual([
      "localOnly",
      "artifactReview",
      "bridgePreviewUnavailable",
      "tier3Closed"
    ]);
  });

  test("keeps developer labels and raw live terms out of user-facing product copy", () => {
    const visibleCopy = cbbsProductWindowsApps
      .flatMap((app) => [
        app.title,
        app.subtitle,
        app.audience,
        app.statusLine,
        ...app.menuLabels,
        ...app.views.flatMap((view) => [view.label, view.summary]),
        ...app.actions.flatMap((action) => [action.label, action.summary]),
        ...app.panels.flatMap((panel) => [panel.title, panel.body]),
        ...(app.menu?.pages.flatMap((page) => [
          page.label,
          page.summary,
          ...page.sections.flatMap((section) => [
            section.label,
            section.summary,
            ...section.items.flatMap((item) => [item.label, item.summary])
          ])
        ]) ?? [])
      ])
      .join("\n");
    expect(visibleCopy).not.toMatch(
      /RNW|fixture-only|local-only|source evidence|source-backed|developer|Dev Config|schema|ADR|task log|package|Advanced Details|Confirmation text|COM6|COM15|serial|XBee|\bRF\b|flash|relay|mains|PMK|LMK|private key/i
    );
  });

  test("pins Sysop Win31 page order and actions", () => {
    const sysop = getCbbsProductWindowsAppProfile("sysop");
    expect(sysop.views.map((view) => view.label)).toEqual(win31SysopPageOrder);
    expect(sysop.views.map((view) => view.pageId)).toEqual([
      "status",
      "messages",
      "files",
      "devices",
      "help",
      "peers",
      "link",
      "updates",
      "setup",
      "diagnostics",
      "locks"
    ]);
    expect(sysop.actions.map((action) => action.label)).toEqual([
      "Connect",
      "Refresh Status",
      "Pull Messages",
      "Post Message",
      "Search Board",
      "Acknowledge Message",
      "Refresh Catalog",
      "Queue Selected File",
      "Update Gate Status",
      "Record Update Intent"
    ]);
    expect(sysop.actions.map((action) => action.menuId)).toEqual([
      "session",
      "session",
      "messages",
      "messages",
      "messages",
      "messages",
      "files",
      "files",
      "devices",
      "devices"
    ]);
  });

  test("pins role-adapted client parity coverage", () => {
    const client = getCbbsProductWindowsAppProfile("client");
    expect(client.views.map((view) => view.pageId)).toEqual(["status", "messages", "files", "help", "peers"]);
    expect(client.parityCoverage?.map((entry) => entry.pageId)).toEqual([
      "status",
      "messages",
      "files",
      "devices",
      "help",
      "peers",
      "link",
      "updates",
      "setup",
      "diagnostics",
      "locks"
    ]);
    expect(client.parityCoverage?.find((entry) => entry.pageId === "devices")?.disposition).toBe(
      "notRenderedRoleBoundary"
    );
    expect(client.parityCoverage?.find((entry) => entry.pageId === "link")?.disposition).toBe("evidenceOnly");
  });

  test("pins page-scoped Hardware Tools bridge action mapping without executable wording", () => {
    const hardware = getCbbsProductWindowsAppProfile("hardware-tools");
    expect(getProductActionsForPage(hardware, "bench").map((action) => action.id)).toEqual([
      "hardware.benchTargetReview"
    ]);
    expect(getProductActionsForPage(hardware, "radio").map((action) => action.id)).toEqual([
      "hardware.radioInventory",
      "hardware.radioReadStatusPlan",
      "hardware.radioProfileCompare",
      "hardware.radioChangePlan"
    ]);
    expect(getProductActionsForPage(hardware, "mesh").map((action) => action.bridgeActionId)).toEqual([
      "mesh.statusSnapshot",
      "mesh.serviceList"
    ]);
    const visibleActionCopy = hardware.actions.flatMap((action) => [action.label, action.summary]).join("\n");
    expect(visibleActionCopy).not.toMatch(/serial|xbee|\bRF\b|flash|erase|monitor|relay|COM\d+|child_process|exec|spawn|powershell|esptool|idf\.py/i);
  });

  test("maps action states and transcript modes", () => {
    const hardware = getCbbsProductWindowsAppProfile("hardware-tools");
    const inventory = hardware.actions.find((action) => action.id === "hardware.radioInventory");
    const updatePlan = hardware.actions.find((action) => action.id === "hardware.deviceUpdatePlan");

    expect(isActionEnabled("ready")).toBe(true);
    expect(isActionEnabled("needsSafetyCheck")).toBe(false);
    expect(inventory && isProductActionEnabled(inventory)).toBe(true);
    expect(updatePlan && isProductActionEnabled(updatePlan)).toBe(false);
    expect(productActionStateLabel("needsConfirmation")).toBe("Authority needed");
    expect(inventory && canAppendProductTranscript(inventory)).toBe(true);
    expect(updatePlan && canAppendProductTranscript(updatePlan)).toBe(false);
  });

  test("keeps bridge-preview and Tier 3 modes disabled even when state is ready", () => {
    const hardware = getCbbsProductWindowsAppProfile("hardware-tools");
    const inventory = hardware.actions.find((action) => action.id === "hardware.radioInventory");
    expect(inventory).toBeTruthy();
    expect(
      inventory &&
        isProductActionEnabled({
          ...inventory,
          executionMode: "bridgePreviewUnavailable",
          state: "ready"
        })
    ).toBe(false);
    expect(
      inventory &&
        isProductActionEnabled({
          ...inventory,
          executionMode: "tier3Closed",
          state: "complete"
        })
    ).toBe(false);
  });
});
