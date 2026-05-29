namespace AgroScriptInstaller;

internal static class InstallerSettings
{
    public const string ApiBaseUrl = "https://agroscriptmodding.onrender.com";

    // Troque somente na build privada. Se o repositorio for publico, nao comite o token real.
    public const string InstallerApiToken = "fe15b95b08838141a9425ed0f5dc1a0f";

    // Mod principal baixado por este instalador. O backend tambem aceita INSTALLER_DEFAULT_MOD_ID.
    public const string ModId = "asm-8r";
}
