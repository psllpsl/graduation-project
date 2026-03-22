@echo off
chcp 65001 >nul
echo ========================================
echo   Dental Clinic Streamlit Admin
echo ========================================
echo.

cd /d "%~dp0"

echo [检查] 检查虚拟环境...
if not exist "venv" (
    echo 创建虚拟环境中...
    python -m venv venv
    echo 安装依赖中...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    echo 虚拟环境已存在
)

echo.
echo [启动] 启动 Streamlit 应用...
echo.

python start_streamlit.py
