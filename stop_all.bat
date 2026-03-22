@echo off
chcp 65001 >nul
echo ========================================
echo   停止所有服务
echo   牙科修复复诊提醒与管理系统
echo ========================================
echo.

setlocal enabledelayedexpansion

echo [1/4] 正在查找 Streamlit 进程...
echo.

:: 查找 Streamlit 进程
for /f "tokens=2" %%i in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH 2^>nul') do (
    set "PID=%%i"
    for /f "delims=" %%a in ('wmic process where "ProcessId=!PID!" get CommandLine ^| findstr /i "streamlit"') do (
        echo [发现] Streamlit 进程 (PID: !PID!)
        taskkill /F /PID !PID! >nul 2>&1
        if !errorlevel! equ 0 (
            echo [OK] 已停止 Streamlit 进程 (PID: !PID!)
        ) else (
            echo [警告] 无法停止进程 (PID: !PID!)
        )
    )
)

echo.
echo [2/4] 正在查找后端服务进程...
echo.

:: 查找后端服务进程（包含 uvicorn 或 main.py）
for /f "tokens=2" %%i in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV /NH 2^>nul') do (
    set "PID=%%i"
    for /f "delims=" %%a in ('wmic process where "ProcessId=!PID!" get CommandLine ^| findstr /i "uvicorn main.py"') do (
        echo [发现] 后端服务进程 (PID: !PID!)
        taskkill /F /PID !PID! >nul 2>&1
        if !errorlevel! equ 0 (
            echo [OK] 已停止后端服务进程 (PID: !PID!)
        ) else (
            echo [警告] 无法停止进程 (PID: !PID!)
        )
    )
)

echo.
echo [3/4] 检查端口状态...
echo.

:: 检查端口 8000
netstat -ano | findstr :8000 >nul 2>&1
if !errorlevel! equ 0 (
    echo [警告] 端口 8000 仍被占用:
    netstat -ano | findstr :8000
) else (
    echo [OK] 端口 8000 已释放
)

:: 检查端口 8501
netstat -ano | findstr :8501 >nul 2>&1
if !errorlevel! equ 0 (
    echo [警告] 端口 8501 仍被占用:
    netstat -ano | findstr :8501
) else (
    echo [OK] 端口 8501 已释放
)

echo.
echo [4/4] 清理完成
echo.

echo ========================================
echo   所有服务已停止
echo ========================================
echo.

timeout /t 2 /nobreak >nul
