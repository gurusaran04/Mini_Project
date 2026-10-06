@echo off
title Push Project to GitHub
color 0A
cd /d D:\Mini_Project

echo =========================================================================
echo             AUTOMATIC GITHUB PUSH FOR MINI_PROJECT
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
git commit -m "Initial commit - AI Voice IVR System Vercel Ready"

echo Setting main branch...
git branch -M main

echo Adding remote repository origin...
git remote remove origin 2>nul
git remote add origin https://github.com/gurusaran04/Mini_Project.git

echo Pushing code to GitHub...
git push -u origin main

echo.
echo =========================================================================
echo [SUCCESS] Code pushed to https://github.com/gurusaran04/Mini_Project.git!
echo Now go to https://vercel.com/new to deploy!
echo =========================================================================
echo.
pause
