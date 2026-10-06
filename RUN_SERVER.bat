@echo off
title Voice IVR Server Engine (Port 3000)
color 0A
cd /d D:\Mini_Project

echo =========================================================================
echo       ST. JUDE AI VOICE IVR SERVER ENGINE (PORT 3000)
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

echo Running Python Server using: %PY_EXE%
echo Server URL: http://localhost:3000
echo Mobile Simulator URL: http://localhost:3000/mobile.html
echo.
%PY_EXE% server\free_voice_ivr_server.py

pause
