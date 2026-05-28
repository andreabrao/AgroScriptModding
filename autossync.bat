@echo off
:: Altera para o drive D: e entra na pasta RAIZ correta do projeto
cd /d "D:\Documentos\AgroScriptModding"

:: Puxa as alterações do GitHub para evitar o erro de rejeição
git pull origin main --no-rebase

:: Adiciona todas as alterações da raiz e subpastas
git add .

:: Cria o commit se houver alterações
git commit -m "Backup automatico - %date% %time%"

:: Envia tudo atualizado para o GitHub
git push origin main

pause