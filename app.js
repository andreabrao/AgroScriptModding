const mods = [
  {
    id: "asm-8r",
    title: "ASM 8R Performance BR",
    category: "Tratores",
    brand: "John Deere",
    version: "1.3.2",
    downloads: 12872,
    power: "385 cv",
    image: "assets/model-asm-8r.svg",
    description:
      "Trator pesado com som encorpado, rodado largo, luzes revisadas e ajuste fino para lavouras grandes.",
    tags: ["jd", "8r", "trator", "rodado", "performance"],
  },
  {
    id: "case-axial",
    title: "Axial Flow 9250 BR",
    category: "Colheitadeiras",
    brand: "Case IH",
    version: "1.1.0",
    downloads: 9340,
    power: "550 cv",
    image: "assets/model-case-axial.svg",
    description:
      "Colheitadeira com plataforma revisada, tanque ampliado e comportamento calibrado para mapas brasileiros.",
    tags: ["case", "colheita", "grãos", "plataforma"],
  },
  {
    id: "nh-t9",
    title: "T9 SmartTrax Custom",
    category: "Tratores",
    brand: "New Holland",
    version: "1.0.8",
    downloads: 7864,
    power: "620 cv",
    image: "assets/model-nh-t9.svg",
    description:
      "Configuração articulada com esteiras, iluminação de trabalho e torque forte para preparo pesado.",
    tags: ["new holland", "t9", "esteira", "articulado"],
  },
  {
    id: "plantadeira-asm",
    title: "Plantadeira ASM 32 Linhas",
    category: "Implementos",
    brand: "ASM",
    version: "2.0.1",
    downloads: 15420,
    power: "32 linhas",
    image: "assets/model-plantadeira-asm.svg",
    description:
      "Plantio de alta capacidade com largura de trabalho ajustada e visual robusto para fazendas extensas.",
    tags: ["plantadeira", "implemento", "soja", "milho"],
  },
  {
    id: "mapa-sertao",
    title: "Mapa Sertão Verde",
    category: "Mapas BR",
    brand: "ASM",
    version: "1.4.0",
    downloads: 22318,
    power: "4x",
    image: "assets/model-mapa-sertao.svg",
    description:
      "Mapa brasileiro com estradas de terra, fazendas médias, relevo natural e pontos de venda nacionais.",
    tags: ["mapa", "brasil", "fazenda", "interior"],
  },
  {
    id: "script-hud",
    title: "HUD Safra Realista",
    category: "Scripts",
    brand: "ASM",
    version: "1.2.5",
    downloads: 6418,
    power: "Script",
    image: "assets/model-script-hud.svg",
    description:
      "Interface limpa para acompanhar operação, consumo, horas de máquina e dados de safra durante o jogo.",
    tags: ["script", "hud", "realismo", "telemetria"],
  },
  {
    id: "mf-serie-s",
    title: "Massey Série S Pro",
    category: "Tratores",
    brand: "Massey Ferguson",
    version: "1.0.4",
    downloads: 5120,
    power: "305 cv",
    image: "assets/model-mf-serie-s.svg",
    description:
      "Modelo versátil com opções de peso, pneus nacionais e pintura preparada para operações médias.",
    tags: ["massey", "trator", "serie s", "pneus"],
  },
  {
    id: "grade-asm",
    title: "Grade Pesada ASM 48 discos",
    category: "Implementos",
    brand: "ASM",
    version: "1.1.7",
    downloads: 11880,
    power: "48 discos",
    image: "assets/model-grade-asm.svg",
    description:
      "Implemento de preparo com peso visual, desgaste calibrado e largura ideal para tratores de alta potência.",
    tags: ["grade", "implemento", "preparo", "solo"],
  },
];

const aliases = new Map([
  ["jd", "john deere"],
  ["deere", "john deere"],
  ["case", "case ih"],
  ["nh", "new holland"],
  ["mf", "massey ferguson"],
  ["mapa", "mapas br"],
  ["colheita", "colheitadeiras"],
  ["plantadeira", "implementos"],
  ["script", "scripts"],
]);

const planRules = {
  bronze: { label: "Bronze", quota: 3 },
  prata: { label: "Prata", quota: 6 },
  ouro: { label: "Ouro", quota: 10 },
  platina: { label: "Platina", quota: 15 },
  rubi: { label: "Rubi", quota: 25 },
  esmeralda: { label: "Esmeralda", quota: 40 },
  diamante: { label: "Diamante", quota: null },
};

const subscribers = [
  { email: "bronze@agroscript.com", code: "BRONZE-2026", plan: "bronze", name: "Cliente Bronze", active: true },
  { email: "prata@agroscript.com", code: "PRATA-2026", plan: "prata", name: "Cliente Prata", active: true },
  { email: "ouro@agroscript.com", code: "OURO-2026", plan: "ouro", name: "Cliente Ouro", active: true },
  { email: "platina@agroscript.com", code: "PLATINA-2026", plan: "platina", name: "Cliente Platina", active: true },
  { email: "rubi@agroscript.com", code: "RUBI-2026", plan: "rubi", name: "Cliente Rubi", active: true },
  {
    email: "esmeralda@agroscript.com",
    code: "ESMERALDA-2026",
    plan: "esmeralda",
    name: "Cliente Esmeralda",
    active: true,
  },
  {
    email: "diamante@agroscript.com",
    code: "DIAMANTE-2026",
    plan: "diamante",
    name: "Cliente Diamante",
    active: true,
  },
];

const activeMemberKey = "asm-active-member";
const memberMonthKey = new Date().toISOString().slice(0, 7);

const state = {
  category: "Todos",
  brand: "Todas",
  query: "",
  member: null,
};

const searchInput = document.querySelector("#searchInput");
const brandFilter = document.querySelector("#brandFilter");
const filterChips = Array.from(document.querySelectorAll(".filter-chip"));
const categoryCards = Array.from(document.querySelectorAll("[data-category-card]"));
const modGrid = document.querySelector("#modGrid");
const resultCount = document.querySelector("#resultCount");
const menuToggle = document.querySelector(".menu-toggle");
const siteNav = document.querySelector("#site-nav");
const featuredDownloadCount = document.querySelector("#featuredDownloadCount");
const accessForm = document.querySelector("#accessForm");
const memberEmail = document.querySelector("#memberEmail");
const memberCode = document.querySelector("#memberCode");
const memberLogout = document.querySelector("#memberLogout");
const accessStatus = document.querySelector("#accessStatus");
const memberSummary = document.querySelector("#memberSummary");
const checkoutButtons = Array.from(document.querySelectorAll("[data-checkout-plan]"));

const formatter = new Intl.NumberFormat("pt-BR");
const apiBaseUrl = (window.ASM_CONFIG?.apiBaseUrl || "").replace(/\/$/, "");

function apiUrl(path) {
  return `${apiBaseUrl}${path}`;
}

function normalize(value) {
  return value
    .toString()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

function findSubscriber(email, code) {
  const cleanEmail = normalize(email);
  const cleanCode = code.toString().trim().toUpperCase();

  return subscribers.find(
    (subscriber) =>
      subscriber.active &&
      normalize(subscriber.email) === cleanEmail &&
      subscriber.code === cleanCode
  );
}

async function verifySubscription(email, code) {
  try {
    const response = await fetch(apiUrl("/api/subscriptions/verify"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, code }),
    });

    if (response.ok) {
      const data = await response.json();
      return { ...data.member, token: data.downloadToken };
    }
  } catch {
    // Opening index.html directly will not have the backend API. Keep demo access working.
  }

  return findSubscriber(email, code);
}

function restoreActiveMember() {
  try {
    const savedMember = JSON.parse(localStorage.getItem(activeMemberKey));
    if (!savedMember?.email) return;

    state.member = savedMember;
  } catch {
    state.member = null;
  }
}

function saveActiveMember(member) {
  state.member = member;
  localStorage.setItem(
    activeMemberKey,
    JSON.stringify({
      email: member.email,
      plan: member.plan,
      name: member.name,
      active: member.active,
      token: member.token,
    })
  );
}

function clearActiveMember() {
  state.member = null;
  localStorage.removeItem(activeMemberKey);
}

function memberDownloadsKey(member) {
  return `asm-member-mods:${normalize(member.email)}:${memberMonthKey}`;
}

function getMemberDownloadedMods(member) {
  if (!member) return [];

  try {
    const downloadedMods = JSON.parse(localStorage.getItem(memberDownloadsKey(member)));
    return Array.isArray(downloadedMods) ? downloadedMods : [];
  } catch {
    return [];
  }
}

function setMemberDownloadedMods(member, downloadedMods) {
  localStorage.setItem(memberDownloadsKey(member), JSON.stringify(downloadedMods));
}

function getPlanRule(member) {
  return member ? planRules[member.plan] : null;
}

function isUnlimitedPlan(member) {
  return getPlanRule(member)?.quota === null;
}

function hasDownloadedMod(member, modId) {
  return getMemberDownloadedMods(member).includes(modId);
}

function getMemberUsage(member) {
  return getMemberDownloadedMods(member).length;
}

function getMemberRemaining(member) {
  const rule = getPlanRule(member);
  if (!rule) return 0;
  if (rule.quota === null) return Infinity;

  return Math.max(rule.quota - getMemberUsage(member), 0);
}

function canDownloadMod(member, modId) {
  if (!member) return false;
  if (isUnlimitedPlan(member) || hasDownloadedMod(member, modId)) return true;

  return getMemberRemaining(member) > 0;
}

function registerMemberDownload(member, modId) {
  if (!member || hasDownloadedMod(member, modId)) return;

  const downloadedMods = getMemberDownloadedMods(member);
  downloadedMods.push(modId);
  setMemberDownloadedMods(member, downloadedMods);
}

function quotaLabel(member) {
  const rule = getPlanRule(member);
  if (!rule) return "-";

  return rule.quota === null ? "Todos" : String(rule.quota);
}

function remainingLabel(member) {
  if (!member) return "-";

  const remaining = getMemberRemaining(member);
  return remaining === Infinity ? "Ilimitado" : String(remaining);
}

function setGuestAccessStatus(title, message, tone = "") {
  if (!accessStatus || !memberSummary) return;

  memberSummary.textContent = "Nenhum plano liberado";
  memberLogout.hidden = true;
  accessStatus.className = `access-status ${tone}`.trim();
  accessStatus.innerHTML = `
    <span class="status-pill">Aguardando verificacao</span>
    <h3>${title}</h3>
    <p>${message}</p>
    <div class="access-stats">
      <span><strong>-</strong> Plano</span>
      <span><strong>-</strong> Usados</span>
      <span><strong>-</strong> Restantes</span>
    </div>
  `;
}

function setAccessPanelMessage(title, message, tone = "is-warning") {
  if (!accessStatus || !memberSummary) return;

  memberSummary.textContent = title;
  accessStatus.className = `access-status ${tone}`;
  accessStatus.innerHTML = `
    <span class="status-pill">Pagamento</span>
    <h3>${title}</h3>
    <p>${message}</p>
    <div class="access-stats">
      <span><strong>-</strong> Plano</span>
      <span><strong>-</strong> Pagamento</span>
      <span><strong>-</strong> Acesso</span>
    </div>
  `;
}

function renderAccessState(message = "") {
  if (!accessStatus || !memberSummary) return;

  const member = state.member;
  if (!member) {
    setGuestAccessStatus(
      "Entre para liberar seus mods",
      "Os downloads ficam travados ate o plano mensal ser validado."
    );
    return;
  }

  const rule = getPlanRule(member);
  const usage = getMemberUsage(member);
  const remaining = remainingLabel(member);
  const usedText = isUnlimitedPlan(member) ? `${usage} baixados` : `${usage} de ${quotaLabel(member)}`;
  const statusTone = getMemberRemaining(member) === 0 ? "is-warning" : "is-valid";

  memberSummary.textContent = `${member.name || "Assinante"} - Plano ${rule.label} - ${remaining} restantes`;
  memberLogout.hidden = false;
  memberEmail.value = member.email;
  memberCode.value = "";
  accessStatus.className = `access-status ${statusTone}`;
  accessStatus.innerHTML = `
    <span class="status-pill">Plano ativo</span>
    <h3>${rule.label} liberado</h3>
    <p>${message || "Acesso mensal validado para esta conta."}</p>
    <div class="access-stats">
      <span><strong>${rule.label}</strong> Plano</span>
      <span><strong>${usedText}</strong> Usados</span>
      <span><strong>${remaining}</strong> Restantes</span>
    </div>
  `;
}

function scrollToAccessPanel() {
  document.querySelector("#acesso")?.scrollIntoView({ behavior: "smooth", block: "start" });
  memberEmail?.focus({ preventScroll: true });
}

function getModAccessLabel(modId) {
  const member = state.member;
  if (!member) return "Plano necessario";
  if (hasDownloadedMod(member, modId)) return "Ja liberado";
  if (canDownloadMod(member, modId)) return "Liberado";

  return "Limite mensal";
}

function getDownloadButtonLabel(modId) {
  if (!state.member) return "Verificar plano";
  if (!canDownloadMod(state.member, modId)) return "Limite atingido";

  return "Download";
}

async function startCheckout(planId, button) {
  const plan = planRules[planId];
  if (!plan) return;

  const originalText = button.textContent;
  button.disabled = true;
  button.textContent = "Abrindo checkout...";

  try {
    const response = await fetch(apiUrl("/api/payments/create-preference"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        planId,
        email: memberEmail.value || state.member?.email || "",
      }),
    });
    const data = await response.json();

    if (!response.ok) {
      setAccessPanelMessage(
        "Pagamento nao configurado",
        data.message || "Nao foi possivel criar o checkout agora.",
        "is-warning"
      );
      scrollToAccessPanel();
      return;
    }

    window.location.href = data.checkoutUrl;
  } catch {
    setAccessPanelMessage(
      "Servidor de pagamento offline",
      "Inicie o servidor com node server.js para criar pagamentos.",
      "is-error"
    );
    scrollToAccessPanel();
  } finally {
    button.disabled = false;
    button.textContent = originalText;
  }
}

async function downloadProtectedMod(mod) {
  if (!state.member?.token) {
    setAccessPanelMessage(
      "Assinatura sem token seguro",
      "No GitHub Pages, valide pelo backend online para liberar download protegido.",
      "is-warning"
    );
    scrollToAccessPanel();
    return false;
  }

  const response = await fetch(apiUrl(`/api/mods/${encodeURIComponent(mod.id)}/download`), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token: state.member.token }),
  });

  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    setAccessPanelMessage(
      "Download bloqueado",
      data.message || "O servidor nao liberou esse arquivo para o seu plano.",
      "is-error"
    );
    scrollToAccessPanel();
    return false;
  }

  const blob = await response.blob();
  const disposition = response.headers.get("Content-Disposition") || "";
  const filenameMatch = disposition.match(/filename="([^"]+)"/);
  const filename = filenameMatch?.[1] || `${mod.id}.zip`;
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
  return true;
}

async function claimApprovedPayment(paymentId) {
  try {
    const response = await fetch(apiUrl("/api/payments/claim"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ paymentId }),
    });
    const data = await response.json();

    if (!response.ok) {
      setAccessPanelMessage(
        "Pagamento aguardando confirmacao",
        data.message || "Assim que o pagamento for aprovado, o plano sera liberado.",
        "is-warning"
      );
      return false;
    }

    const member = { ...data.member, token: data.downloadToken };
    saveActiveMember(member);
    renderAccessState("Pagamento aprovado. Plano liberado automaticamente.");
    renderMods();
    return true;
  } catch {
    setAccessPanelMessage(
      "Nao foi possivel confirmar",
      "O pagamento voltou para o site, mas a API nao respondeu agora.",
      "is-error"
    );
    return false;
  }
}

async function showPaymentReturnMessage() {
  const params = new URLSearchParams(window.location.search);
  const paymentStatus = params.get("payment");
  const planId = params.get("plan");
  const paymentId =
    params.get("payment_id") ||
    params.get("collection_id") ||
    params.get("paymentId");
  if (!paymentStatus || !planId) return;

  const plan = planRules[planId];
  if (paymentStatus === "success") {
    if (paymentId) {
      const claimed = await claimApprovedPayment(paymentId);
      if (claimed) return;
    }

    setAccessPanelMessage(
      "Pagamento enviado para aprovacao",
      `Quando o Mercado Pago confirmar o Plano ${plan?.label || ""}, o backend libera o acesso dessa conta.`,
      "is-valid"
    );
    return;
  }

  if (paymentStatus === "pending") {
    setAccessPanelMessage(
      "Pagamento pendente",
      "Aguarde a confirmacao do Mercado Pago para liberar o plano.",
      "is-warning"
    );
    return;
  }

  if (paymentStatus === "failure") {
    setAccessPanelMessage(
      "Pagamento nao aprovado",
      "Tente novamente ou escolha outro meio de pagamento.",
      "is-error"
    );
  }
}

function expandedQuery(value) {
  const normalized = normalize(value);
  return aliases.get(normalized) || normalized;
}

function getDownloads(mod) {
  const saved = localStorage.getItem(`downloads:${mod.id}`);
  return saved ? Number(saved) : mod.downloads;
}

function setDownloads(modId, value) {
  localStorage.setItem(`downloads:${modId}`, String(value));
}

function modSearchText(mod) {
  return normalize(
    [mod.title, mod.category, mod.brand, mod.version, mod.power, mod.description, ...mod.tags].join(" ")
  );
}

function matchesMod(mod) {
  const categoryOk = state.category === "Todos" || mod.category === state.category;
  const brandOk = state.brand === "Todas" || mod.brand === state.brand;
  const query = expandedQuery(state.query);
  const queryOk = !query || modSearchText(mod).includes(normalize(query));

  return categoryOk && brandOk && queryOk;
}

function modCard(mod) {
  const downloads = formatter.format(getDownloads(mod));
  const accessLabel = getModAccessLabel(mod.id);
  const buttonLabel = getDownloadButtonLabel(mod.id);

  return `
    <article class="mod-card">
      <div class="mod-card-header">
        <img class="mod-thumb" src="${mod.image}" alt="${mod.title}" loading="lazy" />
        <div class="mod-meta">
          <span>${mod.category}</span>
          <span>${mod.brand}</span>
        </div>
      </div>
      <h3>${mod.title}</h3>
      <p>${mod.description}</p>
      <div class="mod-meta">
        <span>${mod.power}</span>
        <span>v${mod.version}</span>
        <span>${downloads} downloads</span>
        <span>${accessLabel}</span>
      </div>
      <div class="mod-card-footer">
        <button
          class="metal-button primary download-link"
          type="button"
          data-download-id="${mod.id}"
        >
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 3v12m0 0 5-5m-5 5-5-5M5 21h14" />
          </svg>
          ${buttonLabel}
        </button>
      </div>
    </article>
  `;
}

function renderMods() {
  const filteredMods = mods.filter(matchesMod);
  resultCount.textContent = `${formatter.format(filteredMods.length)} ${
    filteredMods.length === 1 ? "mod encontrado" : "mods encontrados"
  }`;

  if (!filteredMods.length) {
    modGrid.innerHTML = `
      <div class="empty-state">
        Nenhum mod encontrado com os filtros atuais.
      </div>
    `;
    return;
  }

  modGrid.innerHTML = filteredMods.map(modCard).join("");
}

function setCategory(category) {
  state.category = category;
  filterChips.forEach((chip) => {
    chip.classList.toggle("is-active", chip.dataset.category === category);
  });
  renderMods();
}

function refreshFeaturedCounter() {
  const featured = mods.find((mod) => mod.id === "asm-8r");
  if (!featured) return;

  featuredDownloadCount.textContent = formatter.format(getDownloads(featured));
}

accessForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const member = await verifySubscription(memberEmail.value, memberCode.value);
  if (!member) {
    clearActiveMember();
    setGuestAccessStatus(
      "Acesso nao encontrado",
      "Confira o e-mail e o codigo do plano mensal.",
      "is-error"
    );
    renderMods();
    return;
  }

  saveActiveMember(member);
  renderAccessState("Plano verificado. Downloads liberados.");
  renderMods();
});

checkoutButtons.forEach((button) => {
  button.addEventListener("click", () => {
    startCheckout(button.dataset.checkoutPlan, button);
  });
});

memberLogout.addEventListener("click", () => {
  clearActiveMember();
  accessForm.reset();
  renderAccessState();
  renderMods();
});

searchInput.addEventListener("input", (event) => {
  state.query = event.target.value;
  renderMods();
});

brandFilter.addEventListener("change", (event) => {
  state.brand = event.target.value;
  renderMods();
});

filterChips.forEach((chip) => {
  chip.addEventListener("click", () => setCategory(chip.dataset.category));
});

categoryCards.forEach((card) => {
  card.addEventListener("click", () => {
    setCategory(card.dataset.categoryCard);
    searchInput.focus({ preventScroll: true });
    document.querySelector(".search-band").scrollIntoView({ behavior: "smooth", block: "start" });
  });
});

document.addEventListener("click", async (event) => {
  const downloadLink = event.target.closest(".download-link");
  if (!downloadLink) return;
  event.preventDefault();

  const mod = mods.find((item) => item.id === downloadLink.dataset.downloadId);
  if (!mod) return;

  if (!state.member) {
    setGuestAccessStatus(
      "Plano necessario",
      "Verifique sua assinatura para liberar os downloads.",
      "is-warning"
    );
    scrollToAccessPanel();
    return;
  }

  if (!canDownloadMod(state.member, mod.id)) {
    renderAccessState("Limite mensal atingido para este plano.");
    scrollToAccessPanel();
    return;
  }

  const downloaded = await downloadProtectedMod(mod);
  if (!downloaded) return;

  registerMemberDownload(state.member, mod.id);

  const nextDownloads = getDownloads(mod) + 1;
  setDownloads(mod.id, nextDownloads);
  window.setTimeout(() => {
    renderAccessState("Download liberado.");
    refreshFeaturedCounter();
    renderMods();
  }, 0);
});

menuToggle.addEventListener("click", () => {
  const isOpen = siteNav.classList.toggle("is-open");
  menuToggle.setAttribute("aria-expanded", String(isOpen));
});

siteNav.addEventListener("click", (event) => {
  if (!event.target.matches("a")) return;

  siteNav.classList.remove("is-open");
  menuToggle.setAttribute("aria-expanded", "false");
});

restoreActiveMember();
renderAccessState();
showPaymentReturnMessage();
refreshFeaturedCounter();
renderMods();
