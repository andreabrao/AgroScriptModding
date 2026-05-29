namespace AgroScriptInstaller;

internal static class Program
{
    [STAThread]
    private static void Main(string[] args)
    {
        ApplicationConfiguration.Initialize();

        // 1. Tenta pegar do argumento (caso venha de um atalho)
        string modId = args.Length > 0 ? args[0] : "";

        // 2. Se não veio argumento, tenta detectar pelo nome do arquivo
        if (string.IsNullOrEmpty(modId) || modId == "padrao")
        {
            string fileName = System.AppDomain.CurrentDomain.FriendlyName; // Ex: "Instalador_asm-8r.exe"
            if (fileName.Contains("_"))
            {
                // Pega tudo que está depois do underline
                modId = fileName.Split('_')[1].Replace(".exe", "").ToLower();
            }
        }

        // 3. Fallback final
        if (string.IsNullOrEmpty(modId)) modId = "asm-8r";

        Application.Run(new MainForm(modId));
    }
}