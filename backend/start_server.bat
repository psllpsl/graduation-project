@echo off
echo ========================================
echo Dental Clinic AI System - FastAPI Server
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Starting FastAPI server...
echo.
echo API Docs: http://localhost:8000/docs
echo Swagger UI: http://localhost:8000/docs
echo ReDoc: http://localhost:8000/redoc
echo.
echo Press Ctrl+C to stop server
echo.

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
