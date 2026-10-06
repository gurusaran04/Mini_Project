@echo off
TITLE WINDOWS FIREWALL - ALLOW MOBILE ACCESS (PORTS 3000 & 5060)
COLOR 0A

:: Self-elevate to Run as Administrator automatically
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [INFO] Requesting Administrator Elevation...
    powershell -Command "Start-Process '%~0' -Verb RunAs"
    exit /b
)

echo ===================================================================
echo 🛡️ OPENING INBOUND PORTS 3000 & 5060 IN WINDOWS FIREWALL (ALL NETWORKS)
echo ===================================================================
echo.

netsh advfirewall firewall delete rule name="AURA IVR Server 3000" >nul 2>&1
netsh advfirewall firewall delete rule name="AURA Asterisk UDP 5060" >nul 2>&1
netsh advfirewall firewall delete rule name="AURA Asterisk TCP 5060" >nul 2>&1
netsh advfirewall firewall delete rule name="AURA RTP UDP 10000-20000" >nul 2>&1

netsh advfirewall firewall add rule name="AURA IVR Server 3000" dir=in action=allow protocol=TCP localport=3000 profile=any
netsh advfirewall firewall add rule name="AURA Asterisk UDP 5060" dir=in action=allow protocol=UDP localport=5060 profile=any
netsh advfirewall firewall add rule name="AURA Asterisk TCP 5060" dir=in action=allow protocol=TCP localport=5060 profile=any
netsh advfirewall firewall add rule name="AURA RTP UDP 10000-20000" dir=in action=allow protocol=UDP localport=10000-20000 profile=any

echo.
echo [SUCCESS] Windows Firewall Inbound Rules Added for ALL Networks!
echo Mobile phones can now connect to http://YOUR_PC_IP:3000 directly from any smartphone browser!
echo.
pause
