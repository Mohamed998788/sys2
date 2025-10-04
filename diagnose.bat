@echo off
echo ========================================
echo    System Diagnosis - Admin App
echo ========================================
echo.

echo [1/6] Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found
    goto :end
) else (
    echo ✅ Python OK
)
echo.

echo [2/6] Checking required packages...
python -c "import streamlit; print('✅ Streamlit:', streamlit.__version__)" 2>nul || echo ❌ Streamlit not installed
python -c "import pandas; print('✅ Pandas:', pandas.__version__)" 2>nul || echo ❌ Pandas not installed
python -c "import firebase_admin; print('✅ Firebase Admin: OK')" 2>nul || echo ❌ Firebase Admin not installed
python -c "import requests; print('✅ Requests: OK')" 2>nul || echo ❌ Requests not installed
echo.

echo [3/6] Checking environment file...
if exist ".env" (
    echo ✅ .env file exists
    findstr /C:"OPENROUTER_API_KEY" .env >nul && echo ✅ OpenRouter API key configured || echo ❌ OpenRouter API key missing
    findstr /C:"FIREBASE_PROJECT_ID" .env >nul && echo ✅ Firebase project ID configured || echo ❌ Firebase project ID missing
) else (
    echo ❌ .env file not found
    echo   Please copy .env.example to .env and configure it
)
echo.

echo [4/6] Checking main application file...
if exist "main.py" (
    echo ✅ main.py exists
) else (
    echo ❌ main.py not found
)
echo.

echo [5/6] Checking database file...
if exist "school_data.db" (
    echo ✅ Database file exists
) else (
    echo ℹ Database file will be created on first run
)
echo.

echo [6/6] Testing Streamlit command...
streamlit --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Streamlit command available
) else (
    echo ❌ Streamlit command not found
    echo   Try: pip install streamlit
)
echo.

echo ========================================
echo Diagnosis complete!
echo.
echo If all checks pass, run: streamlit run main.py
echo If issues found, check the installation guide
echo ========================================

:end
pause