@echo off
TITLE Staff Dashboard - http://aura-ivr.local
COLOR 0A

echo ===================================================================
echo 🚀 STARTING STAFF DASHBOARD WEB SERVER
echo ===================================================================
echo.
echo Project Custom URL:  http://aura-ivr.local
echo Standard Local URL: http://localhost:8080
echo.

cd /d "%~dp0dashboard"
python -m http.server 8080

pause
