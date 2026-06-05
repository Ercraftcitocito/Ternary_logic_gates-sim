@echo off
REM Start the Ternary Logic Gate Simulator on Windows
title Ternary Logic Gate Simulator Server

echo.
echo ============================================
echo   Ternary Logic Gate Simulator
echo ============================================
echo.
echo Starting server...
echo.

python -m http.server 8000

REM If Python not found, try python3
if %ERRORLEVEL% NEQ 0 (
    echo Python not found. Trying python3...
    python3 -m http.server 8000
)

echo.
pause
