@echo off
chcp 65001 >nul
echo ========================================
echo   Dental Clinic Streamlit Admin
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Checking virtual environment...
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    echo Virtual environment exists
)

echo.
echo [2/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [3/3] Starting Streamlit application...
echo Browser will open http://localhost:8501
echo Press Ctrl+C to stop
echo.
echo ========================================
echo.

streamlit run app.py

pause
