@echo off
TITLE Live Webhook Tunnel Launcher (Ngrok Setup)
COLOR 0B

echo ===================================================================
echo 🌐 LIVE VAPI / TWILIO WEBHOOK TUNNEL SETUP (NGROK)
echo ===================================================================
echo.
echo Instructions:
echo 1. Ensure your Express server or n8n instance is running locally on port 3000 or 5678.
echo 2. This script launches an ngrok public HTTPS tunnel.
echo.

set /p PORT="Enter local port to tunnel (default 3000 for Express, 5678 for n8n): "
if "%PORT%"=="" set PORT=3000

echo [INFO] Exposing http://localhost:%PORT% to public HTTPS...
ngrok http %PORT%

pause
