@echo off
echo ========================================
echo   Stop All Services
echo ========================================
echo.
echo Stopping all Python processes...
echo.

taskkill /F /IM python.exe 2>nul

if %errorlevel% equ 0 (
    echo [OK] All Python processes stopped
) else (
    echo [Info] No Python processes found
)

echo.
echo Checking port 8000...
netstat -ano | findstr :8000 >nul 2>&1
if %errorlevel% equ 0 (
    echo [Warning] Port 8000 still in use
    netstat -ano | findstr :8000
) else (
    echo [OK] Port 8000 is free
)

echo.
echo ========================================
echo   All services stopped
echo ========================================
echo.
pause
