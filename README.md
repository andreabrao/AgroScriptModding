# AGRO SCRIPT MODDING

Site mobile-first para mods de Farming Simulator 22, com planos mensais, checkout Mercado Pago e download protegido por backend.

## Estrutura

- `index.html`: site publico.
- `styles.css`: visual responsivo e acabamento metalico.
- `app.js`: busca, planos, checkout, login do assinante e chamada de download protegido.
- `config.js`: URL publica do backend quando o site estiver no GitHub Pages.
- `server.js`: API Node para pagamento, verificacao de assinatura e entrega dos ZIPs.
- `assets/`: imagens do site.
- `private-downloads/`: pasta privada dos ZIPs no servidor. Nao coloque essa pasta no GitHub Pages.

## GitHub Pages + API

O GitHub Pages nao roda `server.js`; ele serve apenas HTML/CSS/JS. Por isso:

1. Hospede o site no GitHub Pages.
2. Hospede `server.js` em um backend Node, como Render, Railway, Fly.io, VPS ou outro host.
3. Edite `config.js` no site publico:

```js
window.ASM_CONFIG = {
  apiBaseUrl: "https://sua-api.onrender.com",
};
```

Sem essa API online, o botao de plano vai mostrar servidor de pagamentos offline.

## Pagamento

Copie `.env.example` para `.env` no backend e configure:

```env
MERCADO_PAGO_ACCESS_TOKEN=APP_USR_SEU_ACCESS_TOKEN_AQUI
DOWNLOAD_TOKEN_SECRET=uma-chave-grande-e-secreta
SITE_URL=https://seu-usuario.github.io/seu-repositorio
FRONTEND_ORIGIN=https://seu-usuario.github.io
MERCADO_PAGO_WEBHOOK_URL=https://sua-api.onrender.com/api/payments/webhook
DATA_DIR=private-data
PRIVATE_DOWNLOADS_DIR=private-downloads
```

Nunca envie `.env` para o GitHub.

## Downloads Protegidos

Nao coloque ZIPs dos mods em `downloads/`, `assets/`, ou qualquer pasta publica do GitHub Pages. Quem tiver a URL consegue baixar direto.

Coloque os ZIPs apenas na pasta privada do servidor:

```text
private-downloads/
  asm-8r-performance-br.zip
  case-axial-flow-9250-br.zip
  new-holland-t9-smarttrax-custom.zip
  plantadeira-asm-32-linhas.zip
  mapa-sertao-verde.zip
  hud-safra-realista.zip
  massey-serie-s-pro.zip
  grade-pesada-asm-48-discos.zip
```

O navegador chama `/api/mods/:id/download`, mas o servidor so entrega o ZIP se o token da assinatura for valido e se o plano ainda tiver cota mensal.

## Rodar Localmente

```bash
node server.js
```

Abra `http://localhost:3000`.
