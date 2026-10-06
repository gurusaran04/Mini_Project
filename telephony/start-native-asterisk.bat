@echo off
TITLE NATIVE ASTERISK PBX TELEPHONY ENGINE (PORT 5060 UDP/TCP)
COLOR 0A

echo ===================================================================
echo 🚀 STARTING NATIVE ASTERISK PBX ENGINE (PORT 5060 UDP/TCP)
echo (Zero Docker Dependencies Required!)
echo ===================================================================
echo.

SET PY_CMD="C:\Program Files\Python313\python.exe"

echo Launching Native Asterisk Telephony Engine on UDP Port 5060...
cd /d D:\Mini_Project
%PY_CMD% asterisk\start_asterisk_emulator.py

pause
