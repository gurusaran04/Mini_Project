@echo off
title Push Updates to GitHub & Auto-Deploy Vercel
color 0A
cd /d D:\Mini_Project

echo =========================================================================
echo       AUTOMATIC GITHUB PUSH & VERCEL AUTO-DEPLOYMENT SYNC
echo =========================================================================
echo.

if not exist .git (
    echo Initializing Git repository...
    git init
)

echo Configuring Git author details...
git config user.name "gurusaran04"
git config user.email "gurusaran@example.com"

echo Staging all files...
git add .

echo Committing files...
git commit -m "Fix Vercel & Mobile QR URL generator without hardcoded 3000 port" 2>nul

echo Setting main branch...
git branch -M main

echo Adding remote repository origin...
git remote remove origin 2>nul
git remote add origin https://github.com/gurusaran04/Mini_Project.git

echo Pushing code to GitHub...
git push -u origin main --force

echo.
echo =========================================================================
echo [SUCCESS] Code pushed to GitHub! Vercel is auto-deploying in 10 seconds!
echo =========================================================================
echo.
pause
