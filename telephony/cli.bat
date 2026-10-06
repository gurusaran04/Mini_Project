@echo off
TITLE ASTERISK LIVE CALL LOGS CONSOLE (asterisk -rvvv)
COLOR 0B

echo ===================================================================
echo 📞 CONNECTING TO LIVE ASTERISK PBX CLI LOGS...
echo Press Ctrl+C or type 'exit' to disconnect console.
echo ===================================================================
echo.

docker exec -it asterisk-pbx asterisk -rvvv
pause
