@echo off
chcp 65001 > nul
title Pubblica su GitHub

cd /d "%~dp0"

echo ========================================================
echo       Pubblicazione su GitHub (Progetto Personale)
echo ========================================================
echo.
echo 1. Assicurati di aver prima creato un repository VUOTO su GitHub
echo    (ad es. https://github.com/PoisonIceStudios/pendpost )
echo.
set /p REPO_URL="Incolla l'URL del tuo repository GitHub (premi INVIO per usare https://github.com/PoisonIceStudios/pendpost.git): "

if "%REPO_URL%"=="" (
    set "REPO_URL=https://github.com/PoisonIceStudios/pendpost.git"
)

echo.
echo Configurazione remote su: %REPO_URL%
git remote set-url origin %REPO_URL%

echo.
echo Salvataggio modifiche locali in corso...
git add -A
git commit -m "Personal fork: traduzione italiana frontend, correzioni Windows e script di avvio"

echo.
echo Invio a GitHub in corso...
git branch -M main
git push -u origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo [SUCCESSO] Il progetto e' stato pubblicato con successo sul tuo GitHub!
) else (
    echo [AVVISO] Se il push non e' andato a buon fine, verifica di:
    echo 1. Aver creato prima il repository vuoto su https://github.com/new
    echo 2. Aver effettuato l'accesso a GitHub se richiesto dal browser/terminale.
)

echo.
pause
