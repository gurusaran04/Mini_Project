@echo off
TITLE Setup Custom Local Domain - aura-ivr.local
COLOR 0B

echo ===================================================================
echo 🌐 SETTING UP CUSTOM PROJECT DOMAIN: http://aura-ivr.local
echo ===================================================================
echo.

:: Check for Administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️ Administrator privileges required to update Windows hosts file.
    echo Please right-click 'setup-custom-domain.bat' and select 'Run as Administrator'.
    echo.
    pause
    exit /b
)

set HOSTS_FILE=%WINDIR%\System32\drivers\etc\hosts
set DOMAIN=aura-ivr.local

findstr /i "%DOMAIN%" "%HOSTS_FILE%" >nul
if %errorlevel% equ 0 (
    echo [OK] %DOMAIN% is already configured in Windows hosts file!
) else (
    echo 127.0.0.1    %DOMAIN% >> "%HOSTS_FILE%"
    echo [SUCCESS] Added '127.0.0.1    %DOMAIN%' to Windows hosts file!
)

echo.
echo ===================================================================
echo 🎉 CUSTOM DOMAIN SETUP COMPLETE!
echo You can now access your Staff Dashboard at:
echo 👉 http://aura-ivr.local
echo ===================================================================
echo.
pause
