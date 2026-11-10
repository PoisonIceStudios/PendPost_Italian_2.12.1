@echo off
chcp 65001 > nul
title Arresta pendpost

echo ===================================================
echo           Arresto di pendpost in corso...
echo ===================================================
echo.

setlocal enabledelayedexpansion
set FOUND=0
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8090" ^| findstr "LISTENING"') do (
    set FOUND=1
    echo Terminazione del processo con PID %%a...
    taskkill /f /pid %%a >nul 2>&1
)

if %FOUND%==1 (
    echo.
    echo pendpost e' stato arrestato con successo.
) else (
    echo Nessuna istanza attiva di pendpost trovata sulla porta 8090.
)

echo.
ping 127.0.0.1 -n 3 >nul
