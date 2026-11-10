@echo off
chcp 65001 > nul
title pendpost - Social Media Automation

cd /d "%~dp0"

echo ===================================================
echo           Avvio di pendpost in corso...
echo ===================================================
echo.
echo Dashboard: http://127.0.0.1:8090
echo.
echo Premi CTRL+C in questa finestra se vuoi fermare il server.
echo.

rem Apri il browser dopo 2 secondi
start "" powershell -NoProfile -Command "Start-Sleep -Seconds 2; if (Get-Command msedge -ErrorAction SilentlyContinue) { Start-Process msedge '--app=http://127.0.0.1:8090' } else { Start-Process 'http://127.0.0.1:8090' }"

rem Avvia il server Node
node bin\pendpost.mjs
pause
