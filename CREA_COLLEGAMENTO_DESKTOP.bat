@echo off
chcp 65001 > nul
title Crea Collegamento pendpost

cd /d "%~dp0"

echo ===================================================
echo     Configurazione Collegamenti pendpost
echo ===================================================
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\create-shortcut.ps1"

echo.
echo Vuoi attivare anche l'avvio automatico all'accensione del PC? (S/N)
set /p AUTORUN="Scelta (S/N): "
if /i "%AUTORUN%"=="S" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\create-shortcut.ps1" -AddToStartup
)

echo.
echo Operazione completata!
pause
