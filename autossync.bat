@echo off
:: Navega até a pasta do seu projeto
cd "D:\Documentos\AgroScriptModding"

:: Adiciona todas as alterações
git add .

:: Cria um commit com a data e hora atuais
git commit -m "Backup automatico - %date% %time%"

:: Envia para o GitHub (certifique-se de que a branch se chama 'main' ou mude para 'master')
git push origin main
pause