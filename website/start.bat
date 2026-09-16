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

echo Versuche Python Server (server.py) zu starten...
python server.py

if %errorlevel% neq 0 (
    echo.
    echo Fehler beim Starten von server.py. Starte Fallback-Server...
    python -m http.server 8080 --bind 127.0.0.1
)

echo.
echo Server wurde beendet. Das Fenster bleibt nun offen.
pause
