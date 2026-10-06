@echo off
title Find PC IP Address for Mobile Chrome
color 0A
cd /d D:\Mini_Project

echo =========================================================================
echo       HOW TO CONNECT MOBILE CHROME TO PC IVR SERVER
echo =========================================================================
echo.
echo 1. Ensure your Phone and PC are connected to the SAME Wi-Fi or PC Hotspot.
echo.
echo 2. Run ALLOW_MOBILE_FIREWALL.bat on PC once (Right-click -> Run as Administrator).
echo.
echo 3. Open Google Chrome on your Mobile Phone and type one of these URLs:
echo.

powershell -Command "Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*'} | ForEach-Object { Write-Host '   👉 http://' $_.IPAddress ':3000/mobile.html' -ForegroundColor Green }"

echo.
echo =========================================================================
echo OR scan the QR Code from the Faculty Dashboard: http://localhost:3000
echo (Click "Mobile Phone Simulator & QR" in top bar)
echo =========================================================================
echo.
pause
