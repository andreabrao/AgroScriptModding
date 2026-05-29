using System.Drawing;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Windows.Forms;
using Microsoft.Win32;

namespace AgroScriptInstaller;

public sealed class MainForm : Form
{
    private readonly HttpClient httpClient = new();
    private readonly TextBox keyInput = new();
    private readonly TextBox gamePathInput = new();
    private readonly Button browseButton = new();
    private readonly Button installButton = new();
    private readonly ProgressBar progressBar = new();
    private readonly Label statusLabel = new();
    private readonly Label versionLabel = new();

    private string? selectedGameRoot;
    private string? detectedVersion;

    public MainForm()
    {
        Text = "AGRO SCRIPT MODDING - Instalador FS22/FS25";
        Width = 1000;                       // <-- Alterado para 1000
        Height = 1000;                      // <-- Alterado para 1000
        MinimumSize = new Size(1000, 1000); // <-- Alterado para 1000
        MaximumSize = new Size(1000, 1000); // <-- Alterado para 1000
        MaximizeBox = false;              
        StartPosition = FormStartPosition.CenterScreen;
        BackColor = Color.FromArgb(7, 20, 11);
        ForeColor = Color.White;
        Font = new Font("Segoe UI", 10f);

        BuildInterface();
    }

    protected override void Dispose(bool disposing)
    {
        if (disposing)
        {
            httpClient.Dispose();
        }
        base.Dispose(disposing);
    }

    private void BuildInterface()
    {
        var root = new TableLayoutPanel
        {
            Dock = DockStyle.Fill,
            Padding = new Padding(24),
            RowCount = 10, // Aumentado para 10 linhas para os novos títulos
            ColumnCount = 1,
        };
        
        for (int i = 0; i < 9; i++) root.RowStyles.Add(new RowStyle(SizeType.AutoSize));
        root.RowStyles.Add(new RowStyle(SizeType.Percent, 100));

        var title = new Label
        {
            Text = "AGRO SCRIPT MODDING",
            AutoSize = true,
            Font = new Font("Segoe UI", 18f, FontStyle.Bold),
            ForeColor = Color.FromArgb(242, 201, 76),
            Margin = new Padding(0, 0, 0, 10),
        };

        var subtitle = new Label
        {
            Text = "Instalador de mods Farming Simulator 22/25 com validacao por Key + HWID.",
            AutoSize = true,
            ForeColor = Color.FromArgb(200, 209, 202),
            Margin = new Padding(0, 0, 0, 18),
        };

        // --- NOVO TÍTULO DA KEY ---
        var keyLabel = new Label
        {
            Text = "Chave de Ativacao:",
            AutoSize = true,
            ForeColor = Color.White,
            Margin = new Padding(0, 0, 0, 5)
        };

        keyInput.PlaceholderText = "Cole sua key aqui...";
        keyInput.Margin = new Padding(0, 0, 0, 14);
        keyInput.Height = 36;

        // --- NOVO TÍTULO DA PASTA ---
        var pathLabel = new Label
        {
            Text = "Diretorio do Jogo:",
            AutoSize = true,
            ForeColor = Color.White,
            Margin = new Padding(0, 0, 0, 5)
        };

        var pathPanel = new TableLayoutPanel
        {
            Dock = DockStyle.Top,
            ColumnCount = 2,
            RowCount = 1,
            Margin = new Padding(0, 0, 0, 10),
        };
        pathPanel.ColumnStyles.Add(new ColumnStyle(SizeType.Percent, 100));
        pathPanel.ColumnStyles.Add(new ColumnStyle(SizeType.AutoSize));

        gamePathInput.PlaceholderText = "Diretorio raiz do Farming Simulator";
        gamePathInput.ReadOnly = true;
        gamePathInput.Height = 36;
        gamePathInput.Dock = DockStyle.Fill;

        browseButton.Text = "Localizar Jogo";
        browseButton.AutoSize = true;
        browseButton.Height = 36;
        browseButton.Margin = new Padding(10, 0, 0, 0);
        browseButton.Click += BrowseButton_Click;

        pathPanel.Controls.Add(gamePathInput, 0, 0);
        pathPanel.Controls.Add(browseButton, 1, 0);

        versionLabel.Text = "Versao detectada: aguardando pasta";
        versionLabel.AutoSize = true;
        versionLabel.ForeColor = Color.FromArgb(200, 209, 202);
        versionLabel.Margin = new Padding(0, 0, 0, 18);

        installButton.Text = "Validar e instalar";
        installButton.Height = 42;
        installButton.Dock = DockStyle.Top;
        installButton.BackColor = Color.FromArgb(31, 111, 47);
        installButton.ForeColor = Color.White;
        installButton.FlatStyle = FlatStyle.Flat;
        installButton.FlatAppearance.BorderColor = Color.FromArgb(242, 201, 76);
        installButton.Click += InstallButton_Click;

        progressBar.Minimum = 0;
        progressBar.Maximum = 100;
        progressBar.Height = 24;
        progressBar.Margin = new Padding(0, 16, 0, 10);

        statusLabel.Text = "Informe a key e selecione a pasta do jogo.";
        statusLabel.Dock = DockStyle.Fill;
        statusLabel.ForeColor = Color.FromArgb(200, 209, 202);

        // Adicionando os controles na ordem correta
        root.Controls.Add(title);
        root.Controls.Add(subtitle);
        root.Controls.Add(keyLabel); // Adicionado
        root.Controls.Add(keyInput);
        root.Controls.Add(pathLabel); // Adicionado
        root.Controls.Add(pathPanel);
        root.Controls.Add(versionLabel);
        root.Controls.Add(installButton);
        root.Controls.Add(progressBar);
        root.Controls.Add(statusLabel);
        
        Controls.Add(root);
    }

    private void BrowseButton_Click(object? sender, EventArgs e)
    {
        using var dialog = new FolderBrowserDialog
        {
            Description = "Selecione a pasta raiz do Farming Simulator 22 ou 25",
            UseDescriptionForTitle = true,
        };

        if (dialog.ShowDialog(this) != DialogResult.OK) return;

        selectedGameRoot = dialog.SelectedPath;
        gamePathInput.Text = selectedGameRoot;
        detectedVersion = DetectGameVersion(selectedGameRoot);

        versionLabel.Text = detectedVersion is null
            ? "Versao detectada: nao encontrada"
            : $"Versao detectada: {detectedVersion}";
    }

    private async void InstallButton_Click(object? sender, EventArgs e)
    {
        await RunInstallAsync();
    }

    private async Task RunInstallAsync()
    {
        var key = keyInput.Text.Trim();
        if (string.IsNullOrWhiteSpace(key))
        {
            SetStatus("Informe a key de ativacao.", true);
            return;
        }

        if (string.IsNullOrWhiteSpace(selectedGameRoot) || !Directory.Exists(selectedGameRoot))
        {
            SetStatus("Selecione a pasta raiz do Farming Simulator.", true);
            return;
        }

        detectedVersion ??= DetectGameVersion(selectedGameRoot);
        if (detectedVersion is null)
        {
            SetStatus("Nao foi possivel detectar FS22 ou FS25 na pasta escolhida.", true);
            return;
        }

        ToggleUi(false);
        progressBar.Value = 0;

        try
        {
            if (InstallerSettings.InstallerApiToken.StartsWith("TROQUE_", StringComparison.OrdinalIgnoreCase))
            {
                throw new InvalidOperationException("Configure InstallerApiToken antes de compilar o instalador.");
            }

            SetStatus("Gerando HWID e validando key...");
            var hwid = GetHardwareId();
            var license = await VerifyKeyAsync(key, hwid);

            SetStatus("Localizando pasta mods...");
            var modsDirectory = LocateModsDirectory(selectedGameRoot, detectedVersion);

            SetStatus("Baixando mod protegido...");
            var tempFile = await DownloadModAsync(license);

            SetStatus("Instalando mod...");
            var installedPath = InstallModFile(tempFile, modsDirectory, license.FileName, detectedVersion);

            SetStatus($"Instalado com sucesso em: {installedPath}");
            MessageBox.Show(this, "Mod instalado com sucesso.", "AGRO SCRIPT MODDING", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
        catch (Exception ex)
        {
            progressBar.Value = 0;
            SetStatus(ex.Message, true);
            MessageBox.Show(this, ex.Message, "Falha na instalacao", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
        finally
        {
            ToggleUi(true);
        }
    }

    private async Task<VerifyKeyResponse> VerifyKeyAsync(string key, string hwid)
    {
        using var request = new HttpRequestMessage(HttpMethod.Post, $"{InstallerSettings.ApiBaseUrl}/api/verify-key");
        request.Headers.Add("X-Installer-Token", InstallerSettings.InstallerApiToken);
        request.Content = JsonContent(new
        {
            key,
            hwid,
            modId = InstallerSettings.ModId,
        });

        using var response = await httpClient.SendAsync(request);
        var responseText = await response.Content.ReadAsStringAsync();

        if (!response.IsSuccessStatusCode)
        {
            var error = TryReadApiError(responseText);
            throw new InvalidOperationException(error ?? $"Key recusada pela API: {(int)response.StatusCode}");
        }

        var data = JsonSerializer.Deserialize<VerifyKeyResponse>(responseText, JsonOptions);
        if (data is null || string.IsNullOrWhiteSpace(data.DownloadToken))
        {
            throw new InvalidOperationException("Resposta invalida da API de licenca.");
        }

        return data;
    }

    private async Task<string> DownloadModAsync(VerifyKeyResponse license)
    {
        var modId = string.IsNullOrWhiteSpace(license.ModId) ? InstallerSettings.ModId : license.ModId;
        var fileName = SanitizeFileName(license.FileName);
        var tempFile = Path.Combine(Path.GetTempPath(), $"asm-{Guid.NewGuid():N}-{fileName}");

        using var request = new HttpRequestMessage(
            HttpMethod.Post,
            $"{InstallerSettings.ApiBaseUrl}/api/mods/{Uri.EscapeDataString(modId)}/download");
        request.Content = JsonContent(new
        {
            token = license.DownloadToken,
        });

        using var response = await httpClient.SendAsync(request, HttpCompletionOption.ResponseHeadersRead);
        if (!response.IsSuccessStatusCode)
        {
            var responseText = await response.Content.ReadAsStringAsync();
            var error = TryReadApiError(responseText);
            throw new InvalidOperationException(error ?? $"Download recusado pela API: {(int)response.StatusCode}");
        }

        var contentDisposition = response.Content.Headers.ContentDisposition;
        if (!string.IsNullOrWhiteSpace(contentDisposition?.FileNameStar))
        {
            fileName = SanitizeFileName(contentDisposition.FileNameStar);
            tempFile = Path.Combine(Path.GetTempPath(), $"asm-{Guid.NewGuid():N}-{fileName}");
        }
        else if (!string.IsNullOrWhiteSpace(contentDisposition?.FileName))
        {
            fileName = SanitizeFileName(contentDisposition.FileName.Trim('"'));
            tempFile = Path.Combine(Path.GetTempPath(), $"asm-{Guid.NewGuid():N}-{fileName}");
        }

        var totalBytes = response.Content.Headers.ContentLength;
        await using var input = await response.Content.ReadAsStreamAsync();
        await using var output = File.Create(tempFile);

        var buffer = new byte[81920];
        long receivedBytes = 0;
        int read;

        while ((read = await input.ReadAsync(buffer)) > 0)
        {
            await output.WriteAsync(buffer.AsMemory(0, read));
            receivedBytes += read;

            if (totalBytes is > 0)
            {
                var progress = (int)Math.Clamp(receivedBytes * 100 / totalBytes.Value, 0, 100);
                progressBar.Value = progress;
            }
        }

        progressBar.Value = 100;
        return tempFile;
    }

    private static string InstallModFile(string tempFile, string modsDirectory, string fileName, string version)
    {
        Directory.CreateDirectory(modsDirectory);

        var prefix = version == "FS25" ? "FS25_" : "FS22_";
        var safeName = EnsureVersionPrefix(SanitizeFileName(fileName), prefix);
        var destination = Path.Combine(modsDirectory, safeName);

        File.Copy(tempFile, destination, overwrite: true);
        File.Delete(tempFile);

        return destination;
    }

    private static string LocateModsDirectory(string selectedRoot, string version)
    {
        var directMods = Directory
            .EnumerateDirectories(selectedRoot, "mods", SearchOption.AllDirectories)
            .FirstOrDefault();

        if (!string.IsNullOrWhiteSpace(directMods))
        {
            return directMods;
        }

        var year = version == "FS25" ? "2025" : "2022";
        var documentsMods = Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments),
            "My Games",
            $"FarmingSimulator{year}",
            "mods");

        Directory.CreateDirectory(documentsMods);
        return documentsMods;
    }

    private static string? DetectGameVersion(string root)
    {
        if (File.Exists(Path.Combine(root, "FarmingSimulator2025.exe")) ||
            root.Contains("25", StringComparison.OrdinalIgnoreCase) ||
            root.Contains("2025", StringComparison.OrdinalIgnoreCase))
        {
            return "FS25";
        }

        if (File.Exists(Path.Combine(root, "FarmingSimulator2022.exe")) ||
            root.Contains("22", StringComparison.OrdinalIgnoreCase) ||
            root.Contains("2022", StringComparison.OrdinalIgnoreCase))
        {
            return "FS22";
        }

        return null;
    }

    private static string GetHardwareId()
    {
        var machineGuid = Registry.GetValue(
            @"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Cryptography",
            "MachineGuid",
            string.Empty)?.ToString() ?? string.Empty;

        var raw = $"{machineGuid}|{Environment.MachineName}|{Environment.ProcessorCount}";
        using var sha = SHA256.Create();
        return Convert.ToHexString(sha.ComputeHash(Encoding.UTF8.GetBytes(raw)));
    }

    private static string EnsureVersionPrefix(string fileName, string prefix)
    {
        var name = Path.GetFileName(fileName);
        if (name.StartsWith("FS22_", StringComparison.OrdinalIgnoreCase) ||
            name.StartsWith("FS25_", StringComparison.OrdinalIgnoreCase))
        {
            name = name[5..];
        }

        return $"{prefix}{name}";
    }

    private static string SanitizeFileName(string? fileName)
    {
        var clean = string.IsNullOrWhiteSpace(fileName) ? "agro-script-mod.zip" : Path.GetFileName(fileName);
        foreach (var invalidChar in Path.GetInvalidFileNameChars())
        {
            clean = clean.Replace(invalidChar, '-');
        }

        return clean.EndsWith(".zip", StringComparison.OrdinalIgnoreCase) ? clean : $"{clean}.zip";
    }

    private static StringContent JsonContent(object payload)
    {
        return new StringContent(JsonSerializer.Serialize(payload, JsonOptions), Encoding.UTF8, "application/json");
    }

    private static string? TryReadApiError(string responseText)
    {
        try
        {
            var error = JsonSerializer.Deserialize<ApiErrorResponse>(responseText, JsonOptions);
            return error?.Message;
        }
        catch
        {
            return null;
        }
    }

    private void ToggleUi(bool enabled)
    {
        keyInput.Enabled = enabled;
        browseButton.Enabled = enabled;
        installButton.Enabled = enabled;
    }

    private void SetStatus(string message, bool isError = false)
    {
        statusLabel.Text = message;
        statusLabel.ForeColor = isError ? Color.FromArgb(255, 138, 138) : Color.FromArgb(200, 209, 202);
    }

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase,
        PropertyNameCaseInsensitive = true,
    };

    private sealed record VerifyKeyResponse(
        bool Ok,
        string Email,
        string? Name,
        string Plan,
        string PlanLabel,
        string ModId,
        string FileName,
        string DownloadToken);

    private sealed record ApiErrorResponse(string? Error, string? Message);
}