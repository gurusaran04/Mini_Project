@echo off
title Instant Mobile Public Tunnel Launcher
color 0A
cd /d D:\Mini_Project

echo =========================================================================
echo       INSTANT FREE PUBLIC MOBILE TUNNEL LAUNCHER
echo =========================================================================
echo.
echo Launching instant public HTTPS tunnel for Port 3000...
echo This URL can be opened on ANY mobile phone browser over 4G, 5G, or Wi-Fi!
echo.

where npx >nul 2>nul
if %errorlevel% equ 0 (
    echo Using localtunnel via npx...
    npx -y localtunnel --port 3000
    goto end
)

echo Using SSH Tunnel Gateway (serveo.net)...
ssh -o StrictHostKeyChecking=no -R 80:localhost:3000 serveo.net

:end
pause
