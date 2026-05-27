const adminTokenKey = "asm-admin-token";
const apiBaseUrl = (window.ASM_CONFIG?.apiBaseUrl || "").replace(/\/$/, "");

const adminTokenForm = document.querySelector("#adminTokenForm");
const adminTokenInput = document.querySelector("#adminToken");
const clearAdminToken = document.querySelector("#clearAdminToken");
const adminDashboard = document.querySelector("#adminDashboard");
const adminStatus = document.querySelector("#adminStatus");
const refreshAdmin = document.querySelector("#refreshAdmin");
const createBackup = document.querySelector("#createBackup");
const adminStats = document.querySelector("#adminStats");
const modFilesTable = document.querySelector("#modFilesTable");
const subscribersTable = document.querySelector("#subscribersTable");
const backupsList = document.querySelector("#backupsList");
const paymentEventsList = document.querySelector("#paymentEventsList");
const privateDownloadDir = document.querySelector("#privateDownloadDir");

function apiUrl(path) {
  return `${apiBaseUrl}${path}`;
}

function getAdminToken() {
  return sessionStorage.getItem(adminTokenKey) || "";
}

function setAdminToken(token) {
  sessionStorage.setItem(adminTokenKey, token);
}

function clearToken() {
  sessionStorage.removeItem(adminTokenKey);
  adminTokenInput.value = "";
  adminDashboard.hidden = true;
  setStatus("Token removido.", "is-warning");
}

function setStatus(message, tone = "") {
  adminStatus.textContent = message;
  adminStatus.className = `result-count ${tone}`.trim();
}

async function adminFetch(path, options = {}) {
  const response = await fetch(apiUrl(path), {
    ...options,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getAdminToken()}`,
      ...(options.headers || {}),
    },
  });
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.message || "Falha ao carregar painel admin.");
  }

  return data;
}

async function loadDashboard() {
  if (!getAdminToken()) {
    setStatus("Informe o token administrativo", "is-warning");
    return;
  }

  setStatus("Carregando painel...");

  try {
    const [summary, subscribers, modFiles, backups, events] = await Promise.all([
      adminFetch("/api/admin/summary"),
      adminFetch("/api/admin/subscribers"),
      adminFetch("/api/admin/mod-files"),
      adminFetch("/api/admin/backups"),
      adminFetch("/api/admin/payment-events"),
    ]);

    adminDashboard.hidden = false;
    renderStats(summary);
    renderModFiles(modFiles);
    renderSubscribers(subscribers.subscribers || []);
    renderBackups(backups.backups || []);
    renderPaymentEvents(events.events || []);
    setStatus(`Atualizado em ${formatDate(summary.generatedAt)}`, "is-valid");
  } catch (error) {
    adminDashboard.hidden = true;
    setStatus(error.message, "is-error");
  }
}

function renderStats(summary) {
  const totals = summary.totals || {};
  adminStats.innerHTML = [
    ["Assinantes", totals.activeSubscribers || 0],
    ["Mods", totals.mods || 0],
    ["ZIPs prontos", `${totals.filesReady || 0}/${totals.mods || 0}`],
    ["Downloads do mes", totals.monthlyDownloads || 0],
    ["Backups", totals.backups || 0],
  ]
    .map(
      ([label, value]) => `
        <article class="admin-stat">
          <strong>${escapeHtml(value)}</strong>
          <span>${escapeHtml(label)}</span>
        </article>
      `
    )
    .join("");
}

function renderModFiles(data) {
  privateDownloadDir.textContent = data.privateDownloadDir || "";

  modFilesTable.innerHTML = (data.files || [])
    .map(
      (file) => `
        <tr>
          <td>${escapeHtml(file.modId)}</td>
          <td>${escapeHtml(file.fileName)}</td>
          <td>
            <span class="admin-badge ${file.exists ? "is-valid" : "is-error"}">
              ${file.exists ? "Pronto" : "Faltando"}
            </span>
          </td>
          <td>${escapeHtml(file.sizeLabel)}</td>
        </tr>
      `
    )
    .join("");
}

function renderSubscribers(subscribers) {
  if (!subscribers.length) {
    subscribersTable.innerHTML = `
      <tr>
        <td colspan="4">Nenhum assinante liberado ainda.</td>
      </tr>
    `;
    return;
  }

  subscribersTable.innerHTML = subscribers
    .map(
      (subscriber) => `
        <tr>
          <td>${escapeHtml(subscriber.email)}</td>
          <td>${escapeHtml(subscriber.planLabel || subscriber.plan)}</td>
          <td>${escapeHtml(subscriber.code)}</td>
          <td>${formatDate(subscriber.updatedAt)}</td>
        </tr>
      `
    )
    .join("");
}

function renderBackups(backups) {
  if (!backups.length) {
    backupsList.innerHTML = `<p>Nenhum backup salvo ainda.</p>`;
    return;
  }

  backupsList.innerHTML = backups
    .map(
      (backup) => `
        <article class="admin-list-item">
          <strong>${escapeHtml(backup.fileName)}</strong>
          <span>${escapeHtml(backup.sizeLabel)} - ${formatDate(backup.updatedAt)}</span>
        </article>
      `
    )
    .join("");
}

function renderPaymentEvents(events) {
  if (!events.length) {
    paymentEventsList.innerHTML = `<p>Nenhum evento recebido ainda.</p>`;
    return;
  }

  paymentEventsList.innerHTML = events
    .slice(0, 8)
    .map((event) => {
      const payload = event.payload || {};
      const paymentId = payload?.data?.id || payload?.id || "sem ID";
      const type = payload?.type || payload?.topic || "evento";
      return `
        <article class="admin-list-item">
          <strong>${escapeHtml(type)}</strong>
          <span>${escapeHtml(paymentId)} - ${formatDate(event.receivedAt)}</span>
        </article>
      `;
    })
    .join("");
}

function formatDate(value) {
  if (!value) return "-";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "-";

  return new Intl.DateTimeFormat("pt-BR", {
    dateStyle: "short",
    timeStyle: "short",
  }).format(date);
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

adminTokenForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const token = adminTokenInput.value.trim();
  if (!token) return;

  setAdminToken(token);
  loadDashboard();
});

clearAdminToken.addEventListener("click", clearToken);
refreshAdmin.addEventListener("click", loadDashboard);

createBackup.addEventListener("click", async () => {
  createBackup.disabled = true;
  createBackup.textContent = "Gerando...";

  try {
    await adminFetch("/api/admin/backups/create", { method: "POST" });
    await loadDashboard();
    setStatus("Backup criado com sucesso.", "is-valid");
  } catch (error) {
    setStatus(error.message, "is-error");
  } finally {
    createBackup.disabled = false;
    createBackup.textContent = "Gerar backup";
  }
});

const savedToken = getAdminToken();
if (savedToken) {
  adminTokenInput.value = savedToken;
  loadDashboard();
}
