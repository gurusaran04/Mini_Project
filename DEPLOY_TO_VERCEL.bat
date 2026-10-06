@echo off
title Vercel Auto-Deployment & GitHub Sync Guide
color 0A
cd /d D:\Mini_Project

echo =========================================================================
echo       VERCEL AUTO-DEPLOYMENT & CONTINUOUS INTEGRATION SETUP
echo =========================================================================
echo.
echo 1. Creating Git repository structure...
where git >nul 2>nul
if %errorlevel% equ 0 (
    if not exist .git (
        git init
        git add .
        git commit -m "Initial commit - AI Voice IVR System Vercel Ready"
        echo [GIT SUCCESS] Git repository initialized locally!
    ) else (
        echo [GIT SUCCESS] Local Git repository is ready.
    )
) else (
    echo [NOTICE] Git CLI is not installed locally. Follow the steps below.
)

echo.
echo =========================================================================
echo  HOW TO HOST ON VERCEL & AUTO-UPDATE ON CHANGES:
echo =========================================================================
echo.
echo STEP 1: Push code to GitHub
echo -------------------------------------------------------------------------
echo 1. Go to https://github.com/new and create a repository (e.g., aura-voice-ivr).
echo 2. Run these commands in your terminal:
echo    git remote add origin https://github.com/YOUR_GITHUB_USERNAME/aura-voice-ivr.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo STEP 2: Deploy on Vercel
echo -------------------------------------------------------------------------
echo 1. Go to https://vercel.com/new and login with GitHub.
echo 2. Select your repository (aura-voice-ivr) and click "Deploy".
echo.
echo STEP 3: Auto-Update Guarantee (Whenever you change code)
echo -------------------------------------------------------------------------
echo Whenever you edit files in D:\Mini_Project, run:
echo    git add .
echo    git commit -m "Updated code"
echo    git push
echo Vercel will automatically re-deploy your live website in 10 seconds!
echo =========================================================================
echo.
pause
