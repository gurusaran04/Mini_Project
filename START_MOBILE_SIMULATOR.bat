@echo off
title AI Voice IVR System Launcher
color 0A
cd /d D:\Mini_Project

echo =========================================================================
echo       ST. JUDE AI VOICE IVR & MOBILE PHONE SIMULATOR LAUNCHER
echo =========================================================================
echo.

set PY_EXE=

py --version >nul 2>&1
if %errorlevel% equ 0 set PY_EXE=py

if "%PY_EXE%"=="" (
    if exist "C:\Program Files\Python313\python.exe" set PY_EXE="C:\Program Files\Python313\python.exe"
    if exist "C:\Program Files\Python312\python.exe" set PY_EXE="C:\Program Files\Python312\python.exe"
    if exist "C:\Program Files\Python311\python.exe" set PY_EXE="C:\Program Files\Python311\python.exe"
    if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" set PY_EXE="%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" set PY_EXE="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" set PY_EXE="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
)

if "%PY_EXE%"=="" set PY_EXE=py

echo Starting Voice IVR Python Server on Port 3000 using %PY_EXE%...
start "Voice IVR Server Engine" cmd /k "cd /d D:\Mini_Project && %PY_EXE% server\free_voice_ivr_server.py"

echo Waiting 3 seconds for server initialization...
timeout /t 3 /nobreak >nul

echo Opening Faculty Dashboard...
start http://localhost:3000

echo Opening Mobile Phone IVR Simulator...
start http://localhost:3000/mobile.html

echo.
echo =========================================================================
echo [SYSTEM ACTIVE AND RUNNING]
echo 1. Faculty Dashboard: http://localhost:3000
echo 2. Mobile Phone IVR Simulator: http://localhost:3000/mobile.html
echo.
echo Keep the "Voice IVR Server Engine" window OPEN while using the system!
echo =========================================================================
echo.
pause
