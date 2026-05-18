(function () {
  const byId = (id) => document.getElementById(id);

  async function readJson(path) {
    const response = await fetch(path, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`${path} returned ${response.status}`);
    }
    return response.json();
  }

  function renderLinks(container, items) {
    if (!container || !Array.isArray(items)) {
      return;
    }
    container.replaceChildren(
      ...items.map((item) => {
        const link = document.createElement("a");
        link.href = item.href;
        link.textContent = item.label;
        return link;
      })
    );
  }

  function renderGates(container, items) {
    if (!container || !Array.isArray(items)) {
      return;
    }
    container.replaceChildren(
      ...items.map((item) => {
        const article = document.createElement("article");
        const title = document.createElement("h3");
        const body = document.createElement("p");
        const link = document.createElement("a");
        title.textContent = item.title;
        body.textContent = item.summary;
        link.href = item.href;
        link.textContent = item.linkText;
        article.append(title, body, link);
        return article;
      })
    );
  }

  function renderTracks(container, items) {
    if (!container || !Array.isArray(items)) {
      return;
    }
    container.replaceChildren(
      ...items.map((item) => {
        const entry = document.createElement("li");
        entry.textContent = item;
        return entry;
      })
    );
  }

  async function hydrate() {
    try {
      const [siteData, manifest] = await Promise.all([
        readJson("site-data.json"),
        readJson("public-file-manifest.json"),
      ]);
      renderLinks(byId("bundleList"), siteData.bundleLinks);
      renderGates(byId("gateList"), siteData.safetyGates);
      renderTracks(byId("trackList"), siteData.futureTracks);

      const manifestCount = byId("manifestCount");
      if (manifestCount && Array.isArray(manifest.files)) {
        manifestCount.textContent = `${manifest.files.length} public files`;
      }
    } catch (error) {
      const manifestCount = byId("manifestCount");
      if (manifestCount) {
        manifestCount.textContent = "Allowlisted";
      }
      console.info("Public manifest enhancement skipped:", error.message);
    }
  }

  hydrate();
})();
