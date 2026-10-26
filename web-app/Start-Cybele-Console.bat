@echo off
title Cybele Design Console (server)
cd /d "%~dp0"

rem If the server is already running, just open the dashboard and exit.
netstat -ano | findstr ":3491 " | findstr "LISTENING" >nul 2>&1
if %errorlevel%==0 (
  start "" "http://localhost:3491"
  exit
)

rem Open the dashboard a couple of seconds after the server boots (detached, no extra window).
start "" powershell -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process 'http://localhost:3491'"

echo ============================================================
echo   Cybele Design Console - server running on http://localhost:3491
echo   Keep this window open. Close it to stop the server.
echo   (It restarts itself automatically if it ever crashes.)
echo ============================================================
echo.

:loop
node server.js
echo.
echo [Cybele] Server stopped - restarting in 2 seconds...  (close this window to stop)
timeout /t 2 /nobreak >nul
goto loop
