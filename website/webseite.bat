@echo off
cd /d "%~dp0"
title Dr. Rahemi Pour - Website Server
echo ========================================================
echo   Dr. med. Rahemi Pour - Lokaler Entwicklungsserver
echo ========================================================
echo.
echo Starte Webserver...
echo Oeffne Website unter http://localhost:8080 ...
echo.
start http://localhost:8080
python server.py
if errorlevel 1 (
    echo.
    echo Starte Fallback-Server...
    python -m http.server 8080 --bind 127.0.0.1
)
pause

