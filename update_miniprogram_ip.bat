@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ============================================================
echo   微信小程序 API 地址修改工具
echo   牙科修复复诊提醒与管理系统
echo ============================================================
echo.

:: 获取当前电脑 IP 地址（WLAN 适配器）
echo [1/3] 正在获取当前电脑 IP 地址...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4" ^| findstr /C:"192.168"') do (
    set "CURRENT_IP=%%a"
    set "CURRENT_IP=!CURRENT_IP: =!"
    goto :found_ip
)

:found_ip
if defined CURRENT_IP (
    set "CURRENT_IP=!CURRENT_IP: =!"
    echo   检测到当前 IP: !CURRENT_IP!
) else (
    echo   ⚠ 未检测到 192.168.x.x 格式的 IP 地址
    echo   请手动输入 IP 地址
)
echo.

:: 读取当前小程序配置的 IP
set "MINIPROGRAM_FILE=miniprogram\app.js"
if not exist "%MINIPROGRAM_FILE%" (
    echo [错误] 找不到文件：%MINIPROGRAM_FILE%
    echo 请确保在 毕业设计 目录下运行此脚本
    pause
    exit /b 1
)

echo [2/3] 当前小程序配置的 API 地址：
findstr /C:"baseUrl:" "%MINIPROGRAM_FILE%"
echo.

:: 提示用户输入新 IP
if defined CURRENT_IP (
    echo.
    echo   直接回车使用检测到的 IP: !CURRENT_IP!
    set /p "NEW_IP=请输入新的 IP 地址："
    if "!NEW_IP!"=="" set "NEW_IP=!CURRENT_IP!"
) else (
    set /p "NEW_IP=请输入新的 IP 地址："
)

:: 验证 IP 格式（简化版）
echo !NEW_IP! | findstr /C:"." >nul
if errorlevel 1 (
    echo.
    echo [错误] IP 地址不能为空！
    pause
    exit /b 1
)

echo.
echo [3/3] 正在修改配置文件...

:: 使用 PowerShell 进行文件替换（支持 UTF-8）
set "NEW_URL=http://!NEW_IP!:8000/api"
powershell -Command "(Get-Content '%MINIPROGRAM_FILE%' -Encoding UTF8) -replace 'http://[\d.]+:8000/api', '%NEW_URL%' | Set-Content '%MINIPROGRAM_FILE%' -Encoding UTF8"

if errorlevel 1 (
    echo [错误] 修改文件失败！
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   ✅ 修改成功！
echo ============================================================
echo   新 API 地址：%NEW_URL%
echo   配置文件：%MINIPROGRAM_FILE%
echo.
echo   ⚠ 请在微信开发者工具中重新编译小程序
echo ============================================================
echo.

:: 显示修改后的配置
echo 修改后的配置：
findstr /C:"baseUrl:" "%MINIPROGRAM_FILE%"
echo.

pause
