/**
 * HDFC Mutual Fund FAQ Assistant — Frontend
 */

const chatArea = document.getElementById("chatArea");
const queryInput = document.getElementById("queryInput");
const sendBtn = document.getElementById("sendBtn");
const mainContent = document.getElementById("mainContent");
const schemeList = document.getElementById("schemeList");
const schemeSearch = document.getElementById("schemeSearch");
const recentList = document.getElementById("recentList");
const suggestionsGrid = document.getElementById("suggestionsGrid");
const sidebarLeft = document.getElementById("sidebarLeft");
const sidebarRight = document.getElementById("sidebarRight");
const drawerBackdrop = document.getElementById("drawerBackdrop");

let selectedSchemes = [];
let isLoading = false;
let activeDrawer = null;

function openDrawer(side) {
  closeDrawers();
  activeDrawer = side;
  document.body.classList.add("drawer-open");
  drawerBackdrop.classList.add("visible");
  drawerBackdrop.setAttribute("aria-hidden", "false");
  if (side === "left") sidebarLeft.classList.add("open");
  if (side === "right") sidebarRight.classList.add("open");
}

function closeDrawers() {
  activeDrawer = null;
  document.body.classList.remove("drawer-open");
  sidebarLeft.classList.remove("open");
  sidebarRight.classList.remove("open");
  drawerBackdrop.classList.remove("visible");
  drawerBackdrop.setAttribute("aria-hidden", "true");
}

function isDrawerMode(sidebar) {
  const style = window.getComputedStyle(sidebar);
  return style.position === "fixed";
}

const SCHEMES = [
  { name: "HDFC Mid Cap Fund Direct Plan Growth", short_name: "Mid Cap Fund", category: "Equity", sub_category: "Mid Cap" },
  { name: "HDFC Small Cap Fund Direct Plan Growth", short_name: "Small Cap Fund", category: "Equity", sub_category: "Small Cap" },
  { name: "HDFC Large Cap Fund Direct Plan Growth", short_name: "Large Cap Fund", category: "Equity", sub_category: "Large Cap" },
  { name: "HDFC ELSS Tax Saver Fund Direct Plan Growth", short_name: "ELSS Tax Saver", category: "Equity", sub_category: "ELSS" },
  { name: "HDFC Gold ETF Fund of Fund Direct Plan Growth", short_name: "Gold ETF FoF", category: "Index, ETFs & FoF", sub_category: "Gold FoF" },
];

function getGroupLabel(category) {
  if (category === "Equity") return "EQUITY & HYBRID FUNDS";
  if (category.includes("Index")) return "INDEX, ETFs & FOF";
  return category.toUpperCase() + " FUNDS";
}

function renderSchemes(filter = "", category = "all") {
  const filtered = SCHEMES.filter((s) => {
    const matchSearch =
      !filter ||
      s.name.toLowerCase().includes(filter.toLowerCase()) ||
      s.short_name.toLowerCase().includes(filter.toLowerCase()) ||
      s.sub_category.toLowerCase().includes(filter.toLowerCase());
    const matchCategory =
      category === "all" ||
      (category === "equity" && s.category === "Equity") ||
      (category === "index" && s.category.includes("Index"));
    return matchSearch && matchCategory;
  });

  const groups = {};
  filtered.forEach((s) => {
    const group = getGroupLabel(s.category);
    if (!groups[group]) groups[group] = [];
    groups[group].push(s);
  });

  schemeList.innerHTML = "";
  for (const [group, schemes] of Object.entries(groups)) {
    const label = document.createElement("div");
    label.className = "scheme-group-label";
    label.textContent = group;
    schemeList.appendChild(label);

    schemes.forEach((s) => {
      const item = document.createElement("div");
      item.className = "scheme-item";
      const checked = selectedSchemes.includes(s.short_name) ? "checked" : "";
      item.innerHTML = `
        <input type="checkbox" id="scheme-${s.short_name.replace(/\s/g, '-')}"
               value="${s.short_name}" ${checked} />
        <label for="scheme-${s.short_name.replace(/\s/g, '-')}">${s.short_name}</label>
      `;
      item.querySelector("input").addEventListener("change", (e) => {
        if (e.target.checked) {
          if (!selectedSchemes.includes(s.short_name)) selectedSchemes.push(s.short_name);
        } else {
          selectedSchemes = selectedSchemes.filter((n) => n !== s.short_name);
        }
        updateScope();
        if (isDrawerMode(sidebarLeft)) closeDrawers();
      });
      schemeList.appendChild(item);
    });
  }

  appendSchemeActions();
}

function appendSchemeActions() {
  schemeList.querySelector(".scheme-actions")?.remove();

  const actions = document.createElement("div");
  actions.className = "scheme-actions";
  actions.innerHTML = `
    <button type="button" class="scheme-action-btn" data-action="select-all">Select All</button>
    <button type="button" class="scheme-action-btn" data-action="clear-all">Clear Selection</button>
  `;

  const goldItem = schemeList.querySelector('input[value="Gold ETF FoF"]')?.closest(".scheme-item");
  if (goldItem) {
    goldItem.after(actions);
  } else {
    schemeList.appendChild(actions);
  }
}

function updateScope() {
  const scopeLabel = document.getElementById("scopeLabel");
  if (selectedSchemes.length === 0) {
    scopeLabel.textContent = "HDFC MF Portfolios";
  } else if (selectedSchemes.length === 1) {
    scopeLabel.textContent = selectedSchemes[0];
  } else {
    scopeLabel.textContent = `${selectedSchemes.length} schemes selected`;
  }
}

function addMessage(text, role, meta = {}) {
  mainContent.classList.add("has-chat");
  const div = document.createElement("div");
  div.className = "chat-message";

  if (role === "user") {
    div.innerHTML = `<div class="msg-user">${escapeHtml(text)}</div>`;
  } else {
    const refusedClass = meta.refused ? " refused" : "";
    let html = `<div class="msg-assistant${refusedClass}">${formatAnswer(text)}`;
    if (meta.source_url) {
      html += `<div class="msg-source"><a href="${meta.source_url}" target="_blank" rel="noopener">${meta.source_url}</a></div>`;
    }
    const footerText = meta.footer ? escapeHtml(meta.footer) : "";
    html += `<div class="msg-meta">${footerText}${footerText ? " · " : ""}Facts-only. No investment advice.</div>`;
    html += `</div>`;
    div.innerHTML = html;
  }

  chatArea.appendChild(div);
  chatArea.scrollTop = chatArea.scrollHeight;
}

function showLoading() {
  const div = document.createElement("div");
  div.className = "chat-message";
  div.id = "loadingMsg";
  div.innerHTML = `
    <div class="msg-assistant msg-loading">
      <div class="loading-dots" aria-label="Loading">
        <span></span><span></span><span></span>
      </div>
      <span class="loading-text">Retrieving verified facts...</span>
    </div>`;
  chatArea.appendChild(div);
  chatArea.scrollTop = chatArea.scrollHeight;
}

function hideLoading() {
  const el = document.getElementById("loadingMsg");
  if (el) el.remove();
}

async function sendQuery(question) {
  if (!question.trim() || isLoading) return;
  isLoading = true;
  sendBtn.disabled = true;
  closeDrawers();

  addMessage(question, "user");
  queryInput.value = "";
  showLoading();

  try {
    const res = await fetch("/api/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: question.trim(),
        selected_schemes: selectedSchemes,
      }),
    });
    if (!res.ok) {
      throw new Error(`Server error (${res.status})`);
    }
    const data = await res.json();
    hideLoading();
    addMessage(data.answer, "assistant", {
      source_url: data.source_url,
      footer: data.footer,
      refused: data.refused,
    });
    refreshRecent();
  } catch (err) {
    hideLoading();
    addMessage("Unable to reach the assistant. Please try again.", "assistant", {
      source_url: "https://www.hdfcfund.com",
      refused: true,
    });
  }

  isLoading = false;
  sendBtn.disabled = false;
  queryInput.focus();
}

async function refreshRecent() {
  try {
    const res = await fetch("/api/recent");
    const data = await res.json();
    if (!data.queries || data.queries.length === 0) return;

    recentList.innerHTML = "";
    data.queries.forEach((q) => {
      const item = document.createElement("div");
      item.className = "recent-item";
      const tag = q.refused
        ? q.classification === "out_of_scope"
          ? "Out of scope"
          : "Refused"
        : "Answered";
      item.innerHTML = `
        <div class="recent-q">${escapeHtml(q.question)}</div>
        <div class="recent-meta">${tag} · ${q.classification}</div>
      `;
      item.addEventListener("click", () => sendQuery(q.question));
      recentList.appendChild(item);
    });
  } catch (_) {}
}

function escapeHtml(text) {
  const d = document.createElement("div");
  d.textContent = text;
  return d.innerHTML;
}

function formatAnswer(text) {
  return escapeHtml(text).replace(/\n/g, "<br/>");
}

function newSession() {
  chatArea.innerHTML = "";
  mainContent.classList.remove("has-chat");
  queryInput.focus();
}

// Event listeners
sendBtn.addEventListener("click", () => sendQuery(queryInput.value));
queryInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendQuery(queryInput.value);
});

suggestionsGrid.addEventListener("click", (e) => {
  const card = e.target.closest(".suggestion-card");
  if (card) sendQuery(card.dataset.question);
});

schemeSearch.addEventListener("input", (e) => {
  const activeTab = document.querySelector(".tab-btn.active");
  renderSchemes(e.target.value, activeTab?.dataset.category || "all");
});

document.getElementById("categoryTabs").addEventListener("click", (e) => {
  if (!e.target.classList.contains("tab-btn")) return;
  document.querySelectorAll(".tab-btn").forEach((b) => b.classList.remove("active"));
  e.target.classList.add("active");
  renderSchemes(schemeSearch.value, e.target.dataset.category);
});

schemeList.addEventListener("click", (e) => {
  const btn = e.target.closest("[data-action]");
  if (!btn) return;

  if (btn.dataset.action === "select-all") {
    const activeTab = document.querySelector(".tab-btn.active");
    const category = activeTab?.dataset.category || "all";
    const visible = SCHEMES.filter((s) => {
      const matchCategory =
        category === "all" ||
        (category === "equity" && s.category === "Equity") ||
        (category === "index" && s.category.includes("Index"));
      return matchCategory;
    });
    selectedSchemes = visible.map((s) => s.short_name);
    renderSchemes(schemeSearch.value, category);
    updateScope();
    return;
  }

  if (btn.dataset.action === "clear-all") {
    selectedSchemes = [];
    renderSchemes(schemeSearch.value);
    updateScope();
  }
});

document.getElementById("newSessionBtn").addEventListener("click", newSession);
document.getElementById("homeBtn").addEventListener("click", newSession);

document.getElementById("openSchemesBtn").addEventListener("click", () => openDrawer("left"));
document.getElementById("openInfoBtn").addEventListener("click", () => openDrawer("right"));
document.getElementById("closeSchemesBtn").addEventListener("click", closeDrawers);
document.getElementById("closeInfoBtn").addEventListener("click", closeDrawers);
drawerBackdrop.addEventListener("click", closeDrawers);

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeDrawers();
});

window.addEventListener("resize", () => {
  if (activeDrawer === "left" && !isDrawerMode(sidebarLeft)) closeDrawers();
  if (activeDrawer === "right" && !isDrawerMode(sidebarRight)) closeDrawers();
});

// Init
renderSchemes();
queryInput.focus();
