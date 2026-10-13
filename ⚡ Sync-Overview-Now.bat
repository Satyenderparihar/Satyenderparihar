@echo off
title Auto-Sync GitHub Overview Catalog
cd /d "%~dp0"
echo ===================================================
echo   Syncing all GitHub Repositories to Overview...
echo ===================================================
node scripts/auto_catalog.js
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to run sync script.
    pause
    exit /b %ERRORLEVEL%
)

git add README.md scripts/
git diff --staged --quiet
if %ERRORLEVEL% EQU 0 (
    echo [INFO] No changes detected. Overview is already up-to-date!
) else (
    echo [INFO] Committing and pushing catalog updates to GitHub...
    git commit -m "auto-sync: update categorized repositories in Overview"
    git push origin main
    echo [SUCCESS] Overview updated and pushed to GitHub!
)

echo ===================================================
echo Done! Check https://github.com/Satyenderparihar
echo ===================================================
timeout /t 5
