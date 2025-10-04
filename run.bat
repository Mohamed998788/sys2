@echo off
echo ========================================
echo    School Management System - Admin
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Checking Streamlit installation...
python -c "import streamlit; print('Streamlit version:', streamlit.__version__)"
if %errorlevel% neq 0 (
    echo Error: Streamlit is not installed
    echo Installing Streamlit...
    pip install streamlit
)

echo.
echo Checking environment file...
if not exist ".env" (
    echo Warning: .env file not found
    echo Please copy .env.example to .env and configure your API keys
    echo.
    echo Do you want to continue anyway? (y/n)
    set /p continue=
    if /i not "%continue%"=="y" (
        echo Setup cancelled
        pause
        exit /b 1
    )
)

echo.
echo Starting Streamlit application...
echo Open your browser and go to: http://localhost:8501
echo Press Ctrl+C to stop the application
echo.

streamlit run main.py

echo.
echo Application stopped
pause