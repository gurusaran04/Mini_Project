@echo off
title Find Current PC IP Address
color 0A
cd /d D:\Mini_Project

echo =========================================================================
echo             CURRENT PC NETWORK IP ADDRESSES
echo =========================================================================
echo.
echo Active IPv4 Addresses on this PC:
echo.

powershell -Command "Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*'} | Select-Object IPAddress, InterfaceAlias | Format-Table -AutoSize"

echo.
echo =========================================================================
echo Try typing these exact URLs into your Mobile Phone Chrome browser:
powershell -Command "Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*'} | ForEach-Object { Write-Host ' 👉 http://' $_.IPAddress ':3000/mobile.html' -ForegroundColor Green }"
echo =========================================================================
echo.
pause
