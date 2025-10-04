@echo off
echo ========================================
echo    Building School Management Admin EXE
echo ========================================
echo.

echo [1/4] Installing PyInstaller...
pip install pyinstaller

echo.
echo [2/4] Checking required files...
if not exist "main.py" (
    echo Error: main.py not found
    pause
    exit /b 1
)

if not exist "alnassr-ab9fd-firebase-adminsdk-fbsvc-24f5614874.json" (
    echo Error: Firebase JSON file not found
    pause
    exit /b 1
)

echo.
echo [3/4] Building EXE file...
pyinstaller --onefile ^
    --name=SchoolManagementAdmin ^
    --add-data="alnassr-ab9fd-firebase-adminsdk-fbsvc-24f5614874.json;." ^
    --add-data=".env;." ^
    --hidden-import=streamlit ^
    --hidden-import=pandas ^
    --hidden-import=firebase_admin ^
    --hidden-import=google.cloud.firestore ^
    --hidden-import=requests ^
    --hidden-import=plotly ^
    --hidden-import=openpyxl ^
    --hidden-import=sqlite3 ^
    --console ^
    main.py

echo.
echo [4/4] Checking build result...
if exist "dist\SchoolManagementAdmin.exe" (
    echo ✅ Build successful!
    echo EXE file location: dist\SchoolManagementAdmin.exe
    echo File size:
    dir "dist\SchoolManagementAdmin.exe" | find "SchoolManagementAdmin.exe"
) else (
    echo ❌ Build failed!
)

echo.
echo ========================================
echo Build process completed
echo ========================================
pause