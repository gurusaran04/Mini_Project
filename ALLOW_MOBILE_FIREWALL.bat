@echo off
title Allow Mobile Firewall Ports 3000 & 5060
echo =========================================================================
echo       ALLOW MOBILE SIMULATOR & SIP FIREWALL PORTS (3000 / 5060)
echo =========================================================================
echo.
echo Opening Windows Defender Firewall rule for inbound TCP Port 3000 (HTTP Server)
echo and UDP Port 5060 (Asterisk Voice SIP Engine)...
echo.

powershell -Command "Start-Process netsh -ArgumentList 'advfirewall firewall add rule name=\"Allow IVR Port 3000\" dir=in action=allow protocol=TCP localport=3000 profile=any' -Verb RunAs"
powershell -Command "Start-Process netsh -ArgumentList 'advfirewall firewall add rule name=\"Allow IVR Port 5060\" dir=in action=allow protocol=UDP localport=5060 profile=any' -Verb RunAs"

echo.
echo =========================================================================
echo [SUCCESS] Windows Defender Firewall rules created for Port 3000 and 5060!
echo Mobile phones on local Wi-Fi and PC Hotspot can now connect freely.
echo =========================================================================
echo.
pause
