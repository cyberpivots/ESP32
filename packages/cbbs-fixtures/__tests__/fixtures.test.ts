import { CLOSED_SURFACE_IDS } from "@cbbs/protocol";
import { cbbsFixtureSnapshot } from "../src";

describe("CBBS fixtures", () => {
  test("keeps closed surfaces in protocol parity", () => {
    expect(cbbsFixtureSnapshot.closedSurfaces.map((surface) => surface.id)).toEqual(CLOSED_SURFACE_IDS);
  });

  test("provides client and sysop desktop role profiles", () => {
    const client = cbbsFixtureSnapshot.roleProfiles.find((profile) => profile.role === "client");
    const sysop = cbbsFixtureSnapshot.roleProfiles.find((profile) => profile.role === "sysop");

    expect(client?.viewIds).toEqual(["home", "messages", "downloads", "peers", "network", "evidence"]);
    expect(sysop?.viewIds).toEqual([
      "home",
      "downloads",
      "peers",
      "network",
      "diagnostics",
      "safety",
      "config",
      "evidence"
    ]);
  });
});
