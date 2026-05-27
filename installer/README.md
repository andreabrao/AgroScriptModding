# Instalador Windows AGRO SCRIPT MODDING

Projeto Windows Forms em C# para validar uma key, vincular HWID e instalar o ZIP do mod em Farming Simulator 22 ou 25.

## Fluxo

1. O usuario informa a key.
2. O instalador gera um HWID local.
3. O instalador chama `POST /api/verify-key` com `X-Installer-Token`.
4. A API vincula a key ao HWID na primeira instalacao.
5. O instalador baixa o ZIP por `/api/mods/:id/download`.
6. O ZIP e copiado para a pasta `mods` com prefixo `FS22_` ou `FS25_`.

## Configuracao

Edite `AgroScriptInstaller/InstallerSettings.cs` antes de compilar:

```csharp
public const string ApiBaseUrl = "https://agroscriptmodding.onrender.com";
public const string InstallerApiToken = "TROQUE_PELO_INSTALLER_API_TOKEN";
public const string ModId = "asm-8r";
```

Use no Render o mesmo valor em:

```env
INSTALLER_API_TOKEN=token-privado-do-instalador
INSTALLER_DEFAULT_MOD_ID=asm-8r
```

Nao coloque o token real em repositorio publico. Em uma build publica, esse token ainda pode ser extraido por usuarios avancados, entao a protecao principal deve continuar sendo o backend, a key e o HWID.

## Compilar

```bash
dotnet publish installer/AgroScriptInstaller/AgroScriptInstaller.csproj -c Release -r win-x64 --self-contained true
```

O executavel fica em:

```text
installer/AgroScriptInstaller/bin/Release/net8.0-windows/win-x64/publish/
```

## Observacao de seguranca

O instalador nao aplica `attrib +s +h`. Esconder arquivos como sistema/oculto pode confundir o usuario, ser marcado por antivirus e prejudicar suporte. A protecao real fica no download autenticado, key vinculada ao HWID e controle de cota no servidor.
