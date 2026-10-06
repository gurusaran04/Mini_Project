@echo off
TITLE Live Webhook Tunnel Launcher
COLOR 0B

echo ===================================================================
echo 🌐 LIVE CLOUD TELEPHONY WEBHOOK TUNNEL SETUP
echo ===================================================================
echo.
echo Connecting Ngrok IPv4 tunnel to http://127.0.0.1:3000...
echo.

WHERE ngrok >nul 2>nul
IF %ERRORLEVEL% EQU 0 (
    echo [SUCCESS] Found ngrok! Starting public HTTPS IPv4 tunnel on 127.0.0.1:3000...
    ngrok http 127.0.0.1:3000
) ELSE IF EXIST "%~dp0ngrok.exe" (
    echo [SUCCESS] Found local ngrok.exe! Starting public HTTPS IPv4 tunnel on 127.0.0.1:3000...
    "%~dp0ngrok.exe" http 127.0.0.1:3000
) ELSE (
    echo ⚠️ ngrok.exe was not found in PATH or in D:\Mini_Project\scripts\
    echo.
    echo Please download ngrok.exe from https://ngrok.com/download and place it in this folder:
    echo D:\Mini_Project\scripts\
    echo.
)

pause
