const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const http = require("http");

const rootDir = __dirname;
loadEnv();

const dataDir = resolveDataDir();
const privateDownloadDir = resolvePrivateDownloadDir();
const subscribersPath = path.join(dataDir, "subscribers.json");
const paymentEventsPath = path.join(dataDir, "payment-events.jsonl");
const downloadUsagePath = path.join(dataDir, "download-usage.json");
const backupDir = path.join(dataDir, "backups");
let r2Client;
let r2Sdk;

const plans = {
  bronze: { label: "Bronze", quota: 3, price: 9.9 },
  prata: { label: "Prata", quota: 6, price: 14.9 },
  ouro: { label: "Ouro", quota: 10, price: 24.9 },
  platina: { label: "Platina", quota: 15, price: 34.9 },
  rubi: { label: "Rubi", quota: 25, price: 49.9 },
  esmeralda: { label: "Esmeralda", quota: 40, price: 69.9 },
  diamante: { label: "Diamante", quota: null, price: 99.9 },
};

function resolvePrivateDownloadDir() {
  const configuredPath = process.env.PRIVATE_DOWNLOADS_DIR;
  if (!configuredPath) return path.join(rootDir, "private-downloads");

  return path.isAbsolute(configuredPath)
    ? path.normalize(configuredPath)
    : path.normalize(path.join(rootDir, configuredPath));
}

function resolveDataDir() {
  const configuredPath = process.env.DATA_DIR;
  if (!configuredPath) return path.join(rootDir, "data");

  return path.isAbsolute(configuredPath)
    ? path.normalize(configuredPath)
    : path.normalize(path.join(rootDir, configuredPath));
}

function isR2Configured() {
  return getR2MissingConfig().length === 0;
}

function getR2MissingConfig() {
  const missing = [];
  if (!process.env.R2_BUCKET) missing.push("R2_BUCKET");
  if (!process.env.R2_ACCESS_KEY_ID) missing.push("R2_ACCESS_KEY_ID");
  if (!process.env.R2_SECRET_ACCESS_KEY) missing.push("R2_SECRET_ACCESS_KEY");
  if (!process.env.R2_ENDPOINT && !process.env.R2_ACCOUNT_ID) {
    missing.push("R2_ACCOUNT_ID ou R2_ENDPOINT");
  }
  return missing;
}

function getDownloadStorageMode() {
  return isR2Configured() ? "cloudflare-r2" : "local-private-downloads";
}

function getR2Endpoint() {
  const configuredEndpoint = String(process.env.R2_ENDPOINT || "").trim();
  if (/^https?:\/\//i.test(configuredEndpoint)) {
    try {
      const endpointUrl = new URL(configuredEndpoint);
      return `${endpointUrl.protocol}//${endpointUrl.host}`;
    } catch {
      return configuredEndpoint.replace(/\/$/, "");
    }
  }
  return `https://${process.env.R2_ACCOUNT_ID}.r2.cloudflarestorage.com`;
}

function getR2ExpiresIn() {
  const seconds = Number(process.env.R2_SIGNED_URL_EXPIRES_SECONDS || 300);
  return Number.isFinite(seconds) && seconds > 0 ? seconds : 300;
}

function getR2ObjectKey(fileName) {
  const prefix = String(process.env.R2_KEY_PREFIX || "").replace(/^\/+|\/+$/g, "");
  const bucket = String(process.env.R2_BUCKET || "").replace(/^\/+|\/+$/g, "");
  const safePrefix = prefix === bucket ? "" : prefix;
  return safePrefix ? `${safePrefix}/${fileName}` : fileName;
}

function getR2Sdk() {
  if (!r2Sdk) {
    try {
      r2Sdk = {
        ...require("@aws-sdk/client-s3"),
        ...require("@aws-sdk/s3-request-presigner"),
      };
    } catch (error) {
      throw new Error(
        "Dependencias do Cloudflare R2 ausentes. Rode npm install e redeploy no Render."
      );
    }
  }
  return r2Sdk;
}

function getR2Client() {
  if (!r2Client) {
    const { S3Client } = getR2Sdk();
    r2Client = new S3Client({
      region: "auto",
      endpoint: getR2Endpoint(),
      requestChecksumCalculation: "WHEN_REQUIRED",
      responseChecksumValidation: "WHEN_REQUIRED",
      credentials: {
        accessKeyId: process.env.R2_ACCESS_KEY_ID,
        secretAccessKey: process.env.R2_SECRET_ACCESS_KEY,
      },
    });
  }
  return r2Client;
}

async function createR2SignedDownload(fileName) {
  const { GetObjectCommand, getSignedUrl } = getR2Sdk();
  const command = new GetObjectCommand({
    Bucket: process.env.R2_BUCKET,
    Key: getR2ObjectKey(fileName),
    ResponseContentType: "application/zip",
    ResponseContentDisposition: `attachment; filename="${fileName}"`,
  });
  const expiresIn = getR2ExpiresIn();
  const downloadUrl = await getSignedUrl(getR2Client(), command, { expiresIn });
  return { downloadUrl, expiresIn };
}

const mimeTypes = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".webp": "image/webp",
  ".svg": "image/svg+xml",
  ".txt": "text/plain; charset=utf-8",
  ".mp4": "video/mp4",
};

const modFiles = {
  "asm-8r": "https://agroscriptmodding.onrender.com/modsprivados/FS22_ASM-8R-PERF-BR.zip",
  "case-axial": "https://agroscriptmodding.onrender.com/modsprivados/FS22_CASE_AXIAL.zip",
  "nh-t9": "https://agroscriptmodding.onrender.com/modsprivados/FS22_NH_T9.zip",
  "plantadeira-asm": "https://agroscriptmodding.onrender.com/modsprivados/FS22_plantadeira-asm.zip",
  "mapa-sertao": "https://agroscriptmodding.onrender.com/modsprivados/FS22_mapa_sertao.zip",
  "script-hud": "https://agroscriptmodding.onrender.com/modsprivados/FS22_script_hud.zip",
  "mf-serie-s": "https://agroscriptmodding.onrender.com/modsprivados/FS22_mf_serie_s.zip",
  "grade-asm": "https://agroscriptmodding.onrender.com/modsprivados/FS22_grade_asm.zip",
};

ensureDataFiles();

const port = Number(process.env.PORT || 3000);

const server = http.createServer(async (req, res) => {
  try {
    const requestUrl = new URL(req.url, getBaseUrl(req));
    setCorsHeaders(req, res);

    if (req.method === "OPTIONS") {
      res.writeHead(204);
      return res.end();
    }

    if (req.method === "GET" && requestUrl.pathname === "/api/plans") {
      return sendJson(res, 200, { plans });
    }

    if (req.method === "GET" && requestUrl.pathname === "/api/health") {
      return sendJson(res, 200, {
        ok: true,
        service: "agro-script-modding-api",
        downloadStorage: getDownloadStorageMode(),
      });
    }

    if (requestUrl.pathname.startsWith("/api/admin/")) {
      return handleAdminRequest(req, res, requestUrl);
    }

    if (req.method === "POST" && requestUrl.pathname === "/api/payments/create-preference") {
      return handleCreatePreference(req, res);
    }

    if (req.method === "POST" && requestUrl.pathname === "/api/payments/webhook") {
      return handleWebhook(req, res);
    }

    if (req.method === "POST" && requestUrl.pathname === "/api/payments/claim") {
      return handlePaymentClaim(req, res);
    }

    if (req.method === "POST" && requestUrl.pathname === "/api/verify-key") {
      return handleVerifyKey(req, res);
    }

    if (req.method === "POST" && requestUrl.pathname === "/api/subscriptions/verify") {
      return handleVerifySubscription(req, res);
    }

    if (req.method === "POST" && requestUrl.pathname === "/api/generate-key") {
      return handleGenerateKey(req, res);
    }

    if (
      req.method === "POST" &&
      requestUrl.pathname.startsWith("/api/mods/") &&
      requestUrl.pathname.endsWith("/download")
    ) {
      return handleProtectedDownload(req, res, requestUrl.pathname);
    }

    return serveStatic(req, res, requestUrl.pathname);
  } catch (error) {
    console.error(error);
    return sendJson(res, 500, { error: "server_error", message: "Erro interno do servidor." });
  }
});

server.listen(port, () => {
  console.log(`AGRO SCRIPT MODDING rodando em http://localhost:${port}`);
});

function loadEnv() {
  const envPath = path.join(rootDir, ".env");
  if (!fs.existsSync(envPath)) return;

  const lines = fs.readFileSync(envPath, "utf8").split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;

    const separator = trimmed.indexOf("=");
    if (separator === -1) continue;

    const key = trimmed.slice(0, separator).trim();
    const value = trimmed.slice(separator + 1).trim().replace(/^["']|["']$/g, "");
    if (!process.env[key]) process.env[key] = value;
  }
}

function ensureDataFiles() {
  fs.mkdirSync(dataDir, { recursive: true });
  fs.mkdirSync(privateDownloadDir, { recursive: true });
  fs.mkdirSync(backupDir, { recursive: true });
  if (!fs.existsSync(subscribersPath)) {
    fs.writeFileSync(subscribersPath, JSON.stringify({ subscribers: [] }, null, 2));
  }
  if (!fs.existsSync(downloadUsagePath)) {
    fs.writeFileSync(downloadUsagePath, JSON.stringify({}, null, 2));
  }
}

function setCorsHeaders(req, res) {
  const allowedOrigin = process.env.FRONTEND_ORIGIN || req.headers.origin || "*";
  res.setHeader("Access-Control-Allow-Origin", allowedOrigin);
  res.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type,Authorization,X-Admin-Token,X-Installer-Token");
  res.setHeader("Access-Control-Expose-Headers", "Content-Disposition");
}

function getBaseUrl(req) {
  if (process.env.SITE_URL) return process.env.SITE_URL.replace(/\/$/, "");

  const protocol = process.env.NODE_ENV === "production" ? "https" : "http";
  return `${protocol}://${req.headers.host || `localhost:${port}`}`;
}

async function handleCreatePreference(req, res) {
  const accessToken = process.env.MERCADO_PAGO_ACCESS_TOKEN;
  if (!accessToken) {
    return sendJson(res, 503, {
      error: "payment_not_configured",
      message: "Configure MERCADO_PAGO_ACCESS_TOKEN no arquivo .env.",
    });
  }

  const body = await readJson(req);
  const planId = String(body.planId || "").toLowerCase();
  const plan = plans[planId];

  if (!plan) {
    return sendJson(res, 400, { error: "invalid_plan", message: "Plano invalido." });
  }

  const baseUrl = getBaseUrl(req);
  const payerEmail = String(body.email || "").trim();
  const preferencePayload = {
    items: [
      {
        id: `asm-${planId}`,
        title: `Plano ${plan.label} - AGRO SCRIPT MODDING`,
        description:
          plan.quota === null
            ? "Acesso mensal a todos os mods FS22."
            : `Acesso mensal a ${plan.quota} mods FS22.`,
        quantity: 1,
        currency_id: "BRL",
        unit_price: plan.price,
      },
    ],
    back_urls: {
      success: `${baseUrl}/?payment=success&plan=${planId}#acesso`,
      failure: `${baseUrl}/?payment=failure&plan=${planId}#planos`,
      pending: `${baseUrl}/?payment=pending&plan=${planId}#acesso`,
    },
    auto_return: "approved",
    external_reference: `asm_${planId}_${Date.now()}`,
    metadata: {
      plan_id: planId,
      quota: plan.quota === null ? "all" : plan.quota,
      source: "agro_script_modding",
    },
  };

  if (payerEmail) {
    preferencePayload.payer = { email: payerEmail };
  }

  if (process.env.MERCADO_PAGO_WEBHOOK_URL) {
    preferencePayload.notification_url = process.env.MERCADO_PAGO_WEBHOOK_URL;
  }

  const response = await fetch("https://api.mercadopago.com/checkout/preferences", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${accessToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(preferencePayload),
  });

  const data = await response.json();
  if (!response.ok) {
    return sendJson(res, response.status, {
      error: "mercado_pago_error",
      message: data.message || "Mercado Pago recusou a criacao do checkout.",
      details: data,
    });
  }

  const useSandbox = process.env.MERCADO_PAGO_USE_SANDBOX === "true";
  const checkoutUrl = useSandbox ? data.sandbox_init_point || data.init_point : data.init_point;

  return sendJson(res, 200, {
    preferenceId: data.id,
    checkoutUrl,
  });
}

async function handleWebhook(req, res) {
  const payload = await readJson(req).catch(() => ({}));
  appendJsonLine(paymentEventsPath, {
    receivedAt: new Date().toISOString(),
    payload,
  });

  const paymentId = payload?.data?.id || payload?.id;
  if (paymentId) {
    await tryActivateSubscriptionFromPayment(paymentId);
  }

  return sendJson(res, 200, { received: true });
}

async function handlePaymentClaim(req, res) {
  const body = await readJson(req);
  const paymentId = String(body.paymentId || "").trim();

  if (!paymentId) {
    return sendJson(res, 400, { error: "missing_payment", message: "Pagamento nao informado." });
  }

  const subscriber = await tryActivateSubscriptionFromPayment(paymentId);
  if (!subscriber) {
  novaChave = "OURO-123456";
  subscribers.push({ key: novaChave, hwid: null, active: true });
    return sendJson(res, 404, {
      error: "payment_not_approved",
      message: "Pagamento ainda nao aprovado ou nao encontrado.",
    });
  }

  return sendJson(res, 200, {
    member: {
      email: subscriber.email,
      plan: subscriber.plan,
      name: subscriber.name,
      active: true,
      code: subscriber.code,
    },
    accessCode: subscriber.code,
    downloadToken: createDownloadToken(subscriber),
  });
}


async function handleVerifyKey(req, res) {
  const auth = getInstallerAuth(req);
  if (!auth.ok) {
    return sendJson(res, auth.status, {
      error: auth.error,
      message: auth.message,
    });
  }

  const body = await readJson(req);
  const key = String(body.key || "").trim().toUpperCase();
  const hwid = String(body.hwid || "").trim();
  const modId = String(body.modId || "asm-8r").trim();
  const fileName = modFiles[modId];

  if (!key || !hwid) {
    return sendJson(res, 400, {
      error: "missing_license_data",
      message: "Informe a key e o HWID.",
    });
  }

  if (!fileName) {
    return sendJson(res, 404, {
      error: "mod_not_found",
      message: "Mod nao cadastrado no servidor.",
    });
  }

  const database = readSubscribers();
  const subscriber = database.subscribers.find(
    (entry) => entry.active && String(entry.code || "").trim().toUpperCase() === key
  );

  if (!subscriber) {
    return sendJson(res, 404, {
      error: "invalid_key",
      message: "Key nao encontrada ou assinatura inativa.",
    });
  }

  const linkedHwid = String(subscriber.hwid || "").trim();
  if (linkedHwid && linkedHwid !== hwid) {
    return sendJson(res, 409, {
      error: "hwid_mismatch",
      message: "Esta key ja esta vinculada a outro computador.",
    });
  }

  if (!linkedHwid) {
    subscriber.hwid = hwid;
    subscriber.hwidLinkedAt = new Date().toISOString();
    fs.writeFileSync(subscribersPath, JSON.stringify(database, null, 2));
    createBackup("installer-hwid-linked");
  }

  return sendJson(res, 200, {
    ok: true,
    email: subscriber.email,
    name: subscriber.name,
    plan: subscriber.plan,
    planLabel: plans[subscriber.plan]?.label || subscriber.plan,
    modId,
    fileName,
    downloadToken: createDownloadToken(subscriber),
  });
}

async function tryActivateSubscriptionFromPayment(paymentId) {
  const accessToken = process.env.MERCADO_PAGO_ACCESS_TOKEN;
  if (!accessToken) return null;

  const response = await fetch(`https://api.mercadopago.com/v1/payments/${paymentId}`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  if (!response.ok) return null;

  const payment = await response.json();
  if (payment.status !== "approved") return null;

  const planId = payment.metadata?.plan_id || parsePlanFromReference(payment.external_reference);
  const plan = plans[planId];
  const email = payment.payer?.email;
  if (!plan || !email) return null;

  const code = createAccessCode(planId, paymentId);
  const database = readSubscribers();
  const existing = database.subscribers.find(
    (subscriber) => normalize(subscriber.email) === normalize(email)
  );
  const alreadyActivated =
    existing?.paymentId && String(existing.paymentId) === String(paymentId);

  const subscription = {
    email,
    code,
    plan: planId,
    name: payment.payer?.first_name || `Cliente ${plan.label}`,
    active: true,
    paymentId,
    updatedAt: new Date().toISOString(),
  };

  if (existing) {
    Object.assign(existing, subscription);
  } else {
    database.subscribers.push(subscription);
  }

  fs.writeFileSync(subscribersPath, JSON.stringify(database, null, 2));
  const savedSubscriber = existing || subscription;

  if (!alreadyActivated) {
    createBackup("subscription-activated");
    await sendAccessEmail(savedSubscriber).catch((error) => {
      console.error("Falha ao enviar email de acesso:", error);
    });
  }

  return savedSubscriber;
}

async function handleAdminRequest(req, res, requestUrl) {
  const auth = getAdminAuth(req);
  if (!auth.ok) {
    return sendJson(res, auth.status, {
      error: auth.error,
      message: auth.message,
    });
  }

  if (req.method === "GET" && requestUrl.pathname === "/api/admin/summary") {
    return sendJson(res, 200, getAdminSummary());
  }

  if (req.method === "GET" && requestUrl.pathname === "/api/admin/subscribers") {
    return sendJson(res, 200, {
      subscribers: readSubscribers().subscribers.map(sanitizeSubscriber),
    });
  }

  if (req.method === "GET" && requestUrl.pathname === "/api/admin/mod-files") {
    return sendJson(res, 200, {
      privateDownloadDir,
      files: getModFileStatuses(),
    });
  }

  if (req.method === "GET" && requestUrl.pathname === "/api/admin/payment-events") {
    return sendJson(res, 200, {
      events: readPaymentEvents(80),
    });
  }

  if (req.method === "GET" && requestUrl.pathname === "/api/admin/backups") {
    return sendJson(res, 200, {
      backups: listBackups(),
    });
  }

  if (req.method === "POST" && requestUrl.pathname === "/api/admin/backups/create") {
    return sendJson(res, 200, {
      backup: createBackup("manual-admin"),
      backups: listBackups(),
    });
  }

  return sendJson(res, 404, {
    error: "admin_route_not_found",
    message: "Rota administrativa nao encontrada.",
  });
}

async function handleVerifySubscription(req, res) {
  const body = await readJson(req);
  const email = String(body.email || "");
  const code = String(body.code || "").trim().toUpperCase();

  const database = readSubscribers();
  const subscriber = database.subscribers.find(
    (entry) =>
      entry.active &&
      normalize(entry.email) === normalize(email) &&
      String(entry.code || "").toUpperCase() === code
  );

  if (!subscriber) {
    return sendJson(res, 404, { error: "not_found", message: "Assinatura nao encontrada." });
  }

  return sendJson(res, 200, {
    member: {
      email: subscriber.email,
      plan: subscriber.plan,
      name: subscriber.name || `Cliente ${plans[subscriber.plan]?.label || ""}`.trim(),
      active: true,
      code: subscriber.code,
    },
    accessCode: subscriber.code,
    downloadToken: createDownloadToken(subscriber),
  });
}

function createDownloadToken(subscriber) {
  const payload = {
    email: subscriber.email,
    plan: subscriber.plan,
    name: subscriber.name || `Cliente ${plans[subscriber.plan]?.label || ""}`.trim(),
    exp: Math.floor(Date.now() / 1000) + 60 * 60 * 24 * 30,
  };
  const encodedPayload = Buffer.from(JSON.stringify(payload)).toString("base64url");
  const signature = signTokenPayload(encodedPayload);
  return `${encodedPayload}.${signature}`;
}

function verifyDownloadToken(token) {
  if (!token || typeof token !== "string" || !token.includes(".")) return null;

  const [encodedPayload, signature] = token.split(".");
  const expectedSignature = signTokenPayload(encodedPayload);
  if (signature.length !== expectedSignature.length) return null;
  if (!crypto.timingSafeEqual(Buffer.from(signature), Buffer.from(expectedSignature))) return null;

  try {
    const payload = JSON.parse(Buffer.from(encodedPayload, "base64url").toString("utf8"));
    if (!payload.email || !payload.plan || payload.exp < Math.floor(Date.now() / 1000)) return null;
    return payload;
  } catch {
    return null;
  }
}

function signTokenPayload(encodedPayload) {
  const secret =
    process.env.DOWNLOAD_TOKEN_SECRET ||
    process.env.MERCADO_PAGO_ACCESS_TOKEN ||
    "dev-only-change-this-secret";

  return crypto.createHmac("sha256", secret).update(encodedPayload).digest("base64url");
}

function parsePlanFromReference(reference = "") {
  const match = String(reference).match(/^asm_([a-z]+)_/);
  return match ? match[1] : "";
}

function createAccessCode(planId, paymentId) {
  const tail = String(paymentId).slice(-6).padStart(6, "0");
  return `${planId.toUpperCase()}-${tail}`;
}

function readSubscribers() {
  try {
    return JSON.parse(fs.readFileSync(subscribersPath, "utf8"));
  } catch {
    return { subscribers: [] };
  }
}

function readDownloadUsage() {
  try {
    return JSON.parse(fs.readFileSync(downloadUsagePath, "utf8"));
  } catch {
    return {};
  }
}

function getAdminAuth(req) {
  const configuredToken = process.env.ADMIN_TOKEN;
  if (!configuredToken) {
    return {
      ok: false,
      status: 503,
      error: "admin_not_configured",
      message: "Configure ADMIN_TOKEN no backend antes de usar o painel admin.",
    };
  }

  const authorization = String(req.headers.authorization || "");
  const bearerToken = authorization.startsWith("Bearer ")
    ? authorization.slice("Bearer ".length).trim()
    : "";
  const headerToken = String(req.headers["x-admin-token"] || "").trim();
  const receivedToken = bearerToken || headerToken;

  if (!receivedToken || !safeEqual(receivedToken, configuredToken)) {
    return {
      ok: false,
      status: 401,
      error: "unauthorized_admin",
      message: "Token administrativo invalido.",
    };
  }

  return { ok: true };
}

function getInstallerAuth(req) {
  const configuredToken = process.env.INSTALLER_API_TOKEN;
  if (!configuredToken) {
    return {
      ok: false,
      status: 503,
      error: "installer_not_configured",
      message: "Configure INSTALLER_API_TOKEN no backend antes de usar o instalador.",
    };
  }

  const authorization = String(req.headers.authorization || "");
  const bearerToken = authorization.startsWith("Bearer ")
    ? authorization.slice("Bearer ".length).trim()
    : "";
  const headerToken = String(req.headers["x-installer-token"] || "").trim();
  const receivedToken = bearerToken || headerToken;

  if (!receivedToken || !safeEqual(receivedToken, configuredToken)) {
    return {
      ok: false,
      status: 401,
      error: "unauthorized_installer",
      message: "Token do instalador invalido.",
    };
  }

  return { ok: true };
}

function safeEqual(left, right) {
  const leftBuffer = Buffer.from(String(left));
  const rightBuffer = Buffer.from(String(right));
  if (leftBuffer.length !== rightBuffer.length) return false;
  return crypto.timingSafeEqual(leftBuffer, rightBuffer);
}

function getAdminSummary() {
  const database = readSubscribers();
  const usage = readDownloadUsage();
  const activeSubscribers = database.subscribers.filter((subscriber) => subscriber.active);
  const currentMonth = new Date().toISOString().slice(0, 7);
  const files = getModFileStatuses();

  const byPlan = Object.fromEntries(
    Object.keys(plans).map((planId) => [
      planId,
      activeSubscribers.filter((subscriber) => subscriber.plan === planId).length,
    ])
  );

  const monthlyDownloads = Object.entries(usage)
    .filter(([key]) => key.endsWith(`:${currentMonth}`))
    .reduce((total, [, downloadedMods]) => {
      return total + (Array.isArray(downloadedMods) ? downloadedMods.length : 0);
    }, 0);

  return {
    generatedAt: new Date().toISOString(),
    totals: {
      activeSubscribers: activeSubscribers.length,
      plans: Object.keys(plans).length,
      mods: Object.keys(modFiles).length,
      filesReady: files.filter((file) => file.exists).length,
      monthlyDownloads,
      backups: listBackups().length,
    },
    byPlan,
    files,
    recentSubscribers: activeSubscribers
      .slice()
      .sort((left, right) => String(right.updatedAt).localeCompare(String(left.updatedAt)))
      .slice(0, 8)
      .map(sanitizeSubscriber),
  };
}

function sanitizeSubscriber(subscriber) {
  return {
    email: subscriber.email,
    code: subscriber.code,
    plan: subscriber.plan,
    planLabel: plans[subscriber.plan]?.label || subscriber.plan,
    name: subscriber.name,
    active: Boolean(subscriber.active),
    paymentId: subscriber.paymentId,
    hwid: maskSecret(subscriber.hwid),
    hwidLinkedAt: subscriber.hwidLinkedAt,
    updatedAt: subscriber.updatedAt,
  };
}

function maskSecret(value) {
  const text = String(value || "");
  if (!text) return "";
  if (text.length <= 10) return "********";
  return `${text.slice(0, 6)}...${text.slice(-4)}`;
}

function getModFileStatuses() {
  if (isR2Configured()) {
    return Object.entries(modFiles).map(([modId, fileName]) => ({
      modId,
      fileName,
      exists: true,
      size: 0,
      sizeLabel: "Cloudflare R2",
      updatedAt: null,
      storage: "cloudflare-r2",
      bucket: process.env.R2_BUCKET,
      key: getR2ObjectKey(fileName),
    }));
  }

  return Object.entries(modFiles).map(([modId, fileName]) => {
    const filePath = path.normalize(path.join(privateDownloadDir, fileName));
    const exists = isPathInside(filePath, privateDownloadDir) && fs.existsSync(filePath);
    const stat = exists ? fs.statSync(filePath) : null;

    return {
      modId,
      fileName,
      exists,
      size: stat?.size || 0,
      sizeLabel: stat ? formatBytes(stat.size) : "0 B",
      updatedAt: stat ? stat.mtime.toISOString() : null,
    };
  });
}

function listBackups() {
  if (!fs.existsSync(backupDir)) return [];

  return fs
    .readdirSync(backupDir)
    .filter((fileName) => fileName.endsWith(".json"))
    .map((fileName) => {
      const filePath = path.join(backupDir, fileName);
      const stat = fs.statSync(filePath);
      return {
        fileName,
        size: stat.size,
        sizeLabel: formatBytes(stat.size),
        createdAt: stat.birthtime.toISOString(),
        updatedAt: stat.mtime.toISOString(),
      };
    })
    .sort((left, right) => String(right.updatedAt).localeCompare(String(left.updatedAt)));
}

function createBackup(reason = "manual") {
  fs.mkdirSync(backupDir, { recursive: true });
  const createdAt = new Date().toISOString();
  const safeTimestamp = createdAt.replace(/[:.]/g, "-");
  const fileName = `backup-${safeTimestamp}.json`;
  const filePath = path.join(backupDir, fileName);
  const payload = {
    createdAt,
    reason,
    subscribers: readSubscribers(),
    downloadUsage: readDownloadUsage(),
    paymentEvents: readPaymentEvents(200),
    plans,
    modFiles,
  };

  fs.writeFileSync(filePath, JSON.stringify(payload, null, 2));
  const stat = fs.statSync(filePath);
  return {
    fileName,
    size: stat.size,
    sizeLabel: formatBytes(stat.size),
    createdAt,
  };
}

function readPaymentEvents(limit = 50) {
  if (!fs.existsSync(paymentEventsPath)) return [];

  return fs
    .readFileSync(paymentEventsPath, "utf8")
    .split(/\r?\n/)
    .filter(Boolean)
    .slice(-limit)
    .map((line) => {
      try {
        return JSON.parse(line);
      } catch {
        return { raw: line };
      }
    })
    .reverse();
}

async function sendAccessEmail(subscriber) {
  const apiKey = process.env.RESEND_API_KEY;
  const from = process.env.EMAIL_FROM;
  if (!apiKey || !from || !subscriber?.email) {
    return { skipped: true };
  }

  const plan = plans[subscriber.plan];
  const siteUrl = (process.env.SITE_URL || "").replace(/\/$/, "");
  const loginUrl = siteUrl ? `${siteUrl}/#acesso` : "#acesso";
  const subject = `Codigo do Plano ${plan?.label || subscriber.plan} - AGRO SCRIPT MODDING`;
  const text = [
    `Seu Plano ${plan?.label || subscriber.plan} foi aprovado.`,
    `Email: ${subscriber.email}`,
    `Codigo de acesso: ${subscriber.code}`,
    `Entrar: ${loginUrl}`,
    "Nao compartilhe este codigo. Ele libera os downloads do seu plano mensal.",
  ].join("\n");
  const html = `
    <div style="font-family:Arial,sans-serif;line-height:1.5;color:#111">
      <h1>AGRO SCRIPT MODDING</h1>
      <p>Seu Plano ${escapeHtml(plan?.label || subscriber.plan)} foi aprovado.</p>
      <p><strong>Codigo de acesso:</strong> ${escapeHtml(subscriber.code)}</p>
      <p><strong>Email:</strong> ${escapeHtml(subscriber.email)}</p>
      <p><a href="${escapeHtml(loginUrl)}">Entrar na area do assinante</a></p>
      <p>Nao compartilhe este codigo. Ele libera os downloads do seu plano mensal.</p>
    </div>
  `;

  const response = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from,
      to: subscriber.email,
      subject,
      text,
      html,
    }),
  });

  if (!response.ok) {
    const details = await response.text().catch(() => "");
    console.error("Resend recusou o email de acesso:", response.status, details);
    return { sent: false };
  }

  return { sent: true };
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function formatBytes(bytes) {
  const value = Number(bytes) || 0;
  if (value < 1024) return `${value} B`;
  const units = ["KB", "MB", "GB"];
  let size = value / 1024;
  let unitIndex = 0;

  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024;
    unitIndex += 1;
  }

  return `${size.toFixed(size >= 10 ? 0 : 1)} ${units[unitIndex]}`;
}

function appendJsonLine(filePath, data) {
  fs.appendFileSync(filePath, `${JSON.stringify(data)}\n`);
}

function normalize(value) {
  return String(value)
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

function readJson(req) {
  return new Promise((resolve, reject) => {
    let raw = "";
    req.on("data", (chunk) => {
      raw += chunk;
      if (raw.length > 1_000_000) {
        req.destroy();
        reject(new Error("Payload grande demais."));
      }
    });
    req.on("end", () => {
      try {
        resolve(raw ? JSON.parse(raw) : {});
      } catch (error) {
        reject(error);
      }
    });
    req.on("error", reject);
  });
}

function serveStatic(req, res, pathname) {
  const safePath = pathname === "/" ? "/index.html" : decodeURIComponent(pathname);
  const filePath = path.normalize(path.join(rootDir, safePath));
  const normalizedDataDir = path.normalize(dataDir);
  const normalizedPrivateDir = path.normalize(privateDownloadDir);

  if (!isPathInside(filePath, rootDir)) {
    return sendText(res, 403, "Acesso negado.");
  }

  if (
    isPathInside(filePath, normalizedDataDir) ||
    isPathInside(filePath, normalizedPrivateDir) ||
    path.basename(filePath).startsWith(".env")
  ) {
    return sendText(res, 403, "Arquivo protegido.");
  }

  fs.stat(filePath, (error, stat) => {
    if (error || !stat.isFile()) {
      return sendText(res, 404, "Arquivo nao encontrado.");
    }

    const extension = path.extname(filePath).toLowerCase();
    res.writeHead(200, { "Content-Type": mimeTypes[extension] || "application/octet-stream" });
    fs.createReadStream(filePath).pipe(res);
  });
}

function isPathInside(childPath, parentPath) {
  const relative = path.relative(parentPath, childPath);
  return relative === "" || (!relative.startsWith("..") && !path.isAbsolute(relative));
}

function sendJson(res, statusCode, data) {
  res.writeHead(statusCode, { "Content-Type": "application/json; charset=utf-8" });
  res.end(JSON.stringify(data));
}

function sendText(res, statusCode, text) {
  res.writeHead(statusCode, { "Content-Type": "text/plain; charset=utf-8" });
  res.end(text);
}

// ==========================================
// NOVAS FUNCOES ADICIONADAS PARA GERACAO MANUAL DE KEYS
// ==========================================

async function handleGenerateKey(req, res) {
  const auth = getAdminAuth(req);
  if (!auth.ok) {
    return sendJson(res, auth.status, {
      error: auth.error,
      message: auth.message,
    });
  }

  const body = await readJson(req).catch(() => ({}));
  const planId = String(body.planId || "diamante").toLowerCase();
  const plan = plans[planId];

  if (!plan) {
    return sendJson(res, 400, { error: "invalid_plan", message: "Plano invalido." });
  }

  const novaKey = gerarChaveAtivacao();
  const database = readSubscribers();

  const subscription = {
    email: body.email || `manual_${Date.now()}@agroscript.com`,
    code: novaKey,
    plan: planId,
    name: body.name || "Cliente Avulso (Gerado Manualmente)",
    active: true,
    paymentId: `manual_${Date.now()}`,
    hwid: null,
    updatedAt: new Date().toISOString(),
  };

  database.subscribers.push(subscription);
  fs.writeFileSync(subscribersPath, JSON.stringify(database, null, 2));
  createBackup("manual-key-generated");

  return sendJson(res, 201, {
    success: true,
    key: novaKey,
    member: subscription
  });
}

function gerarChaveAtivacao() {
  const caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  const gerarBloco = () => {
    let bloco = '';
    for (let i = 0; i < 4; i++) {
      const index = crypto.randomInt(0, caracteres.length);
      bloco += caracteres[index];
    }
    return bloco;
  };
  return `AGRO-${gerarBloco()}-${gerarBloco()}-${gerarBloco()}`;
}