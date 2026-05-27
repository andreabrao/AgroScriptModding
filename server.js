const http = require("http");
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const rootDir = __dirname;
loadEnv();

const dataDir = resolveDataDir();
const privateDownloadDir = resolvePrivateDownloadDir();
const subscribersPath = path.join(dataDir, "subscribers.json");
const paymentEventsPath = path.join(dataDir, "payment-events.jsonl");
const downloadUsagePath = path.join(dataDir, "download-usage.json");

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
  "asm-8r": "asm-8r-performance-br.zip",
  "case-axial": "case-axial-flow-9250-br.zip",
  "nh-t9": "new-holland-t9-smarttrax-custom.zip",
  "plantadeira-asm": "plantadeira-asm-32-linhas.zip",
  "mapa-sertao": "mapa-sertao-verde.zip",
  "script-hud": "hud-safra-realista.zip",
  "mf-serie-s": "massey-serie-s-pro.zip",
  "grade-asm": "grade-pesada-asm-48-discos.zip",
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
      return sendJson(res, 200, { ok: true, service: "agro-script-modding-api" });
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

    if (req.method === "POST" && requestUrl.pathname === "/api/subscriptions/verify") {
      return handleVerifySubscription(req, res);
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
  res.setHeader("Access-Control-Allow-Headers", "Content-Type,Authorization");
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
  return existing || subscription;
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

async function handleProtectedDownload(req, res, pathname) {
  const modId = decodeURIComponent(pathname.replace(/^\/api\/mods\//, "").replace(/\/download$/, ""));
  const fileName = modFiles[modId];
  if (!fileName) {
    return sendJson(res, 404, { error: "mod_not_found", message: "Mod nao cadastrado no servidor." });
  }

  const body = await readJson(req);
  const member = verifyDownloadToken(body.token);
  if (!member) {
    return sendJson(res, 401, {
      error: "invalid_token",
      message: "Sessao invalida. Verifique seu plano novamente.",
    });
  }

  const plan = plans[member.plan];
  if (!plan) {
    return sendJson(res, 403, { error: "invalid_plan", message: "Plano invalido." });
  }

  const usage = readDownloadUsage();
  const usageKey = `${normalize(member.email)}:${new Date().toISOString().slice(0, 7)}`;
  const usedMods = Array.isArray(usage[usageKey]) ? usage[usageKey] : [];
  const alreadyDownloaded = usedMods.includes(modId);

  if (plan.quota !== null && !alreadyDownloaded && usedMods.length >= plan.quota) {
    return sendJson(res, 403, {
      error: "quota_exceeded",
      message: "Limite mensal atingido para esse plano.",
    });
  }

  const filePath = path.normalize(path.join(privateDownloadDir, fileName));
  if (!isPathInside(filePath, privateDownloadDir)) {
    return sendJson(res, 403, { error: "invalid_path", message: "Caminho de arquivo invalido." });
  }

  if (!fs.existsSync(filePath)) {
    return sendJson(res, 404, {
      error: "file_missing",
      message: `Arquivo privado nao encontrado: ${fileName}. Coloque o ZIP em private-downloads no servidor.`,
    });
  }

  if (!alreadyDownloaded) {
    usedMods.push(modId);
    usage[usageKey] = usedMods;
    fs.writeFileSync(downloadUsagePath, JSON.stringify(usage, null, 2));
  }

  res.writeHead(200, {
    "Content-Type": "application/zip",
    "Content-Disposition": `attachment; filename="${fileName}"`,
    "Cache-Control": "no-store",
  });
  fs.createReadStream(filePath).pipe(res);
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
