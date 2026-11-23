@echo off
title Mingli PWA Server
cd /d "%~dp0"

echo.
echo ==========================================
echo   Mingli ClearLogic - PWA Local Server
echo ==========================================
echo.

set "PY="
if exist "C:\Users\86137\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe" (
  set "PY=C:\Users\86137\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
)
if not defined PY (
  python --version >nul 2>nul
  if not errorlevel 1 set "PY=python"
)
if not defined PY (
  py --version >nul 2>nul
  if not errorlevel 1 set "PY=py"
)

if not defined PY (
  echo [ERROR] Python not found.
  echo.
  echo Install Python from https://www.python.org/downloads/
  echo Check "Add python.exe to PATH", then double-click this file again.
  echo.
  pause
  exit /b 1
)

echo Starting local server...
start "MingliPWA Server" /min cmd /c "%PY% -m http.server 8080"
ping -n 3 127.0.0.1 >nul
start "" "http://localhost:8080"

echo.
echo Browser should open: http://localhost:8080
echo If not, open Chrome/Edge and type that address manually.
echo After installing the PWA, you can close this window.
echo.
pause
