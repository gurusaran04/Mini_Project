@echo off
title Fresh Upload to GitHub (Mini_Project)
color 0A
cd /d D:\Mini_Project

echo =========================================================================
echo       FRESH CLEAN GITHUB UPLOAD FOR MINI_PROJECT REPOSITORY
echo =========================================================================
echo.

echo Configuring Git author details...
git config user.name "gurusaran04"
git config user.email "gurusaran@example.com"

if not exist .git (
    echo Initializing fresh Git repository...
    git init
)

echo Staging all current project files...
git add -A

echo Committing all project files...
git commit -m "Fresh Clean Upload - AI Voice IVR System"

echo Setting main branch...
git branch -M main

echo Configuring GitHub remote URL...
git remote remove origin 2>nul
git remote add origin https://github.com/gurusaran04/Mini_Project.git

echo Force-pushing fresh files to GitHub (replacing old repo files)...
git push -u origin main --force

echo.
echo =========================================================================
echo [SUCCESS] All fresh files uploaded to https://github.com/gurusaran04/Mini_Project.git!
echo Old files on GitHub replaced. Vercel auto-deploying in 10 seconds!
echo =========================================================================
echo.
pause
