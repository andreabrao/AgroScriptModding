@echo off
:: Mudar para a pasta atual
cd /d "%~dp0"

echo Fechando instalador se estiver aberto...
taskkill /f /im AgroScriptInstaller.exe >nul 2>&1

echo Limpando arquivos de build antigos...
dotnet clean

echo Iniciando compilacao do projeto .NET 8.0...
:: Este comando limpa, compila e cria um unico ficheiro .exe
dotnet publish -c Release -r win-x64 --self-contained true -p:PublishSingleFile=true

if %errorlevel% equ 0 (
    echo.
    echo ===================================================================
    echo SUCESSO! O instalador foi compilado.
    echo O ficheiro encontra-se em: bin\Release\net8.0-windows\win-x64\publish\
    echo ===================================================================
) else (
    echo.
    echo [ERRO] Falha na compilacao. 
    echo Verifique se o seu antivírus não está bloqueando o arquivo.
)
pause