@echo off
echo ========================================
echo    Building Streamlit Launcher EXE
echo ========================================
echo.

echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building launcher EXE...
pyinstaller --onefile ^
    --name=SchoolManagementSystem ^
    --add-data="main.py;." ^
    --add-data="config.py;." ^
    --add-data="database.py;." ^
    --add-data="ai_processor.py;." ^
    --add-data="firebase_manager.py;." ^
    --add-data="alnassr-ab9fd-firebase-adminsdk-fbsvc-24f5614874.json;." ^
    --add-data=".env;." ^
    --hidden-import=streamlit ^
    --hidden-import=pandas ^
    --hidden-import=firebase_admin ^
    --hidden-import=requests ^
    --hidden-import=plotly ^
    --hidden-import=openpyxl ^
    --console ^
    streamlit_launcher.py

echo.
if exist "dist\SchoolManagementSystem.exe" (
    echo ✅ Build successful!
    echo EXE file: dist\SchoolManagementSystem.exe
) else (
    echo ❌ Build failed!
)

pause