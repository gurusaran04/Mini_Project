@echo off
TITLE TRIGGER PARENT MOBILE SIM CALL (+91 9087598993)
COLOR 0A

echo ===================================================================
echo 📱 TRIGGERING INBOUND IVR CALL FROM PARENT MOBILE (+91 9087598993)
echo ===================================================================
echo.

SET PY_CMD="C:\Program Files\Python313\python.exe"

echo [1/2] Connecting Parent Mobile Line (+91 9087598993) to Asterisk PBX Port 5060...
%PY_CMD% D:\Mini_Project\asterisk\gsm_sim_gateway_bridge.py +919087598993 1

echo.
echo [2/2] Call completed! Opening Faculty Dashboard...
timeout /t 2 >nul
start http://localhost:3000

pause
