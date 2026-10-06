@echo off
TITLE ASTERISK PBX TELEPHONY LAUNCHER (DOCKER AND NATIVE FALLBACK)
COLOR 0A

echo ===================================================================
echo STARTING ASTERISK PBX TELEPHONY SYSTEM (PORT 5060 UDP/TCP)
echo ===================================================================
echo.

SET PY_CMD="C:\Program Files\Python313\python.exe"

docker ps >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo INFO: Docker Engine Active. Starting Asterisk PBX Container...
    cd /d "%~dp0"
    docker compose up -d
    echo SUCCESS: Docker Asterisk Container Running!
) ELSE (
    echo NOTICE: Docker Engine not active or not responding.
    echo FALLBACK: Launching Native Asterisk PBX Engine on UDP Port 5060...
    start "Asterisk PBX Engine" cmd /k "cd /d D:\Mini_Project && %PY_CMD% asterisk\start_asterisk_emulator.py"
    echo SUCCESS: Native Asterisk Engine Running on UDP Port 5060!
)

echo.
echo To view live call logs or connect ZoiPer:
echo   - SIP Server: 127.0.0.1:5060
echo   - Extension 1001 (User: 1001, Pass: password1001)
echo   - Extension 1002 (User: 1002, Pass: password1002)
echo.
pause
