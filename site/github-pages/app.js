(function () {
  const LABEL_STORAGE_KEY = "esp32.relayLabels.v1";
  const MAX_LABEL_LENGTH = 32;
  const DEFAULT_RELAY_CHANNELS = [
    {
      channel: 1,
      label: "Output A",
      pin: "GPIO25",
      status: "Blocked",
      gate: "Shield routing plus relay trigger voltage, current, polarity, and isolation must be verified before wiring.",
    },
    {
      channel: 2,
      label: "Output B",
      pin: "GPIO26",
      status: "Blocked",
      gate: "Shield routing plus relay trigger voltage, current, polarity, and isolation must be verified before wiring.",
    },
    {
      channel: 3,
      label: "Output C",
      pin: "GPIO27",
      status: "Blocked",
      gate: "Shield routing plus relay trigger voltage, current, polarity, and isolation must be verified before wiring.",
    },
    {
      channel: 4,
      label: "Output D",
      pin: "GPIO33",
      status: "Blocked",
      gate: "Shield routing plus relay trigger voltage, current, polarity, and isolation must be verified before wiring.",
    },
  ];

  let relayChannels = DEFAULT_RELAY_CHANNELS;
  let savedRelayLabels = readSavedRelayLabels();

  const byId = (id) => document.getElementById(id);

  async function readJson(path, options = {}) {
    const response = await fetch(path, { cache: "no-store" });
    if (options.optional && response.status === 404) {
      return null;
    }
    if (!response.ok) {
      throw new Error(`${path} returned ${response.status}`);
    }
    return response.json();
  }

  function normalizeLabel(value) {
    return String(value || "")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, MAX_LABEL_LENGTH);
  }

  function readSavedRelayLabels() {
    try {
      const raw = window.localStorage.getItem(LABEL_STORAGE_KEY);
      const parsed = raw ? JSON.parse(raw) : {};
      if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) {
        return {};
      }
      return Object.fromEntries(
        Object.entries(parsed)
          .map(([channel, label]) => [String(Number(channel)), normalizeLabel(label)])
          .filter(([channel, label]) => channel !== "NaN" && label)
      );
    } catch (_error) {
      return {};
    }
  }

  function writeSavedRelayLabels() {
    try {
      window.localStorage.setItem(
        LABEL_STORAGE_KEY,
        JSON.stringify(savedRelayLabels)
      );
    } catch (_error) {
      return;
    }
  }

  function labelForChannel(item) {
    const channel = String(Number(item.channel));
    return (
      savedRelayLabels[channel] ||
      normalizeLabel(item.label) ||
      `Output ${channel}`
    );
  }

  function saveRelayLabel(channel, label) {
    const key = String(Number(channel));
    const nextLabel = normalizeLabel(label);
    if (!key || key === "NaN") {
      return;
    }
    if (nextLabel) {
      savedRelayLabels[key] = nextLabel;
    } else {
      delete savedRelayLabels[key];
    }
    writeSavedRelayLabels();
    renderRelayMap(byId("relayChannelMap"), relayChannels);
    renderDemoPreview(relayChannels);
  }

  function resetRelayLabels() {
    savedRelayLabels = {};
    try {
      window.localStorage.removeItem(LABEL_STORAGE_KEY);
    } catch (_error) {
      // Keep the in-memory reset even if browser storage is unavailable.
    }
    renderRelayEditor(byId("relayLabelEditor"), relayChannels);
    renderRelayMap(byId("relayChannelMap"), relayChannels);
    renderDemoPreview(relayChannels);
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

  function renderStatusRail(container, items) {
    if (!container || !Array.isArray(items)) {
      return;
    }
    container.replaceChildren(
      ...items.map((item) => {
        const article = document.createElement("article");
        const label = document.createElement("span");
        const value = document.createElement("strong");
        article.dataset.state = item.state || "review";
        label.textContent = item.label || "Status";
        value.textContent = item.value || "Unknown";
        article.append(label, value);
        return article;
      })
    );
  }

  function renderSequence(container, items) {
    if (!container || !Array.isArray(items)) {
      return;
    }
    container.replaceChildren(
      ...items.map((item, index) => {
        const article = document.createElement("article");
        const number = document.createElement("span");
        const title = document.createElement("h3");
        const body = document.createElement("p");
        number.textContent = String(index + 1).padStart(2, "0");
        title.textContent = item.title || "Build stage";
        body.textContent = item.summary || "Review required before proceeding.";
        article.append(number, title, body);
        return article;
      })
    );
  }

  function renderRelayMap(container, items) {
    if (!container || !Array.isArray(items)) {
      return;
    }
    container.replaceChildren(
      ...items.map((item) => {
        const article = document.createElement("article");
        const pin = document.createElement("span");
        const title = document.createElement("h3");
        const status = document.createElement("strong");
        const body = document.createElement("p");
        pin.className = "metric";
        pin.textContent = item.pin || "GPIO unresolved";
        title.textContent = labelForChannel(item);
        status.textContent = item.status || "Blocked";
        body.textContent = item.gate || "Verification gate unresolved.";
        article.append(pin, title, status, body);
        return article;
      })
    );
  }

  function renderRelayEditor(container, items) {
    if (!container || !Array.isArray(items)) {
      return;
    }
    container.replaceChildren(
      ...items.map((item) => {
        const label = document.createElement("label");
        const title = document.createElement("span");
        const input = document.createElement("input");
        const detail = document.createElement("small");
        const channel = String(Number(item.channel));

        title.textContent = `Channel ${channel}`;
        input.type = "text";
        input.maxLength = MAX_LABEL_LENGTH;
        input.autocomplete = "off";
        input.value = labelForChannel(item);
        input.dataset.relayLabelInput = channel;
        input.addEventListener("input", () => {
          if (input.value.length > MAX_LABEL_LENGTH) {
            input.value = input.value.slice(0, MAX_LABEL_LENGTH);
          }
          saveRelayLabel(channel, input.value);
        });
        detail.textContent = `${item.pin || "GPIO unresolved"} provisional`;
        label.append(title, input, detail);
        return label;
      })
    );
  }

  function renderDemoPreview(items) {
    if (!Array.isArray(items)) {
      return;
    }
    items.forEach((item) => {
      const channel = String(Number(item.channel));
      const label = document.querySelector(`[data-relay-preview="${channel}"]`);
      const pin = document.querySelector(`[data-relay-pin="${channel}"]`);
      if (label) {
        label.textContent = labelForChannel(item);
      }
      if (pin) {
        pin.textContent = item.pin || "GPIO unresolved";
      }
    });
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

  function updateManifestCount(manifest) {
    const manifestCount = byId("manifestCount");
    if (manifestCount && manifest && Array.isArray(manifest.files)) {
      manifestCount.textContent = `${manifest.files.length} public files`;
    } else if (manifestCount) {
      manifestCount.textContent = "Generated artifact only";
    }
  }

  async function hydrate() {
    try {
      const siteData = await readJson("site-data.json");
      relayChannels = Array.isArray(siteData.relayChannels)
        ? siteData.relayChannels
        : DEFAULT_RELAY_CHANNELS;
      renderLinks(byId("bundleList"), siteData.bundleLinks);
      renderStatusRail(byId("buildStatusRail"), siteData.buildStatus);
      renderStatusRail(byId("deploymentStatusRail"), siteData.deploymentStatus);
      renderSequence(byId("sequenceList"), siteData.constructionSequence);
      renderRelayMap(byId("relayChannelMap"), relayChannels);
      renderRelayEditor(byId("relayLabelEditor"), relayChannels);
      renderDemoPreview(relayChannels);
      renderGates(byId("gateList"), siteData.safetyGates);
      renderGates(byId("qualityGateList"), siteData.qualityGates);
    } catch (error) {
      renderRelayMap(byId("relayChannelMap"), relayChannels);
      renderRelayEditor(byId("relayLabelEditor"), relayChannels);
      renderDemoPreview(relayChannels);
      console.info("Site data enhancement skipped:", error.message);
    }

    try {
      const manifest = await readJson("public-file-manifest.json", { optional: true });
      updateManifestCount(manifest);
    } catch (error) {
      updateManifestCount(null);
    }
  }

  const resetButton = byId("resetLabelsButton");
  if (resetButton) {
    resetButton.addEventListener("click", resetRelayLabels);
  }

  window.addEventListener("storage", (event) => {
    if (event.key === LABEL_STORAGE_KEY) {
      savedRelayLabels = readSavedRelayLabels();
      renderRelayEditor(byId("relayLabelEditor"), relayChannels);
      renderRelayMap(byId("relayChannelMap"), relayChannels);
      renderDemoPreview(relayChannels);
    }
  });

  hydrate();
})();
