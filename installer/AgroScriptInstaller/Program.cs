namespace AgroScriptInstaller;

internal static class Program
{
    [STAThread]
    private static void Main(string[] args) // O 'args' recebe os parâmetros
    {
        ApplicationConfiguration.Initialize();
        
        // Se args for vazio, definimos como "padrao" ou tratamos erro
        string modId = args.Length > 0 ? args[0] : "padrao";
        
        Application.Run(new MainForm(modId));
    }
}