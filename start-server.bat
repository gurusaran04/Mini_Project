@echo off
TITLE AI Voice IVR Leave Management System - http://aura-ivr.local
COLOR 0A

echo ===================================================================
echo 🚀 STARTING AI VOICE IVR LEAVE SYSTEM BACKEND SERVER
echo ===================================================================
echo.
echo Project Custom URL: http://aura-ivr.local:3000
echo Local HTTP URL:    http://localhost:3000
echo Webhook API URL:   http://aura-ivr.local:3000/api/webhook/vapi-end-call
echo.

cd /d "%~dp0server"

if not exist node_modules (
    echo [INFO] Installing Node.js dependencies...
    npm install
)

echo [INFO] Launching Express server...
node server.js

pause
