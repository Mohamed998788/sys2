@echo off
echo ========================================
echo    بناء تطبيق إدارة المدرسة - الأدمن
echo ========================================

echo.
echo [1/6] التحقق من Python...
python --version
if %errorlevel% neq 0 (
    echo خطأ: Python غير مثبت أو غير موجود في PATH
    pause
    exit /b 1
)

echo.
echo [2/6] تثبيت المتطلبات...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo خطأ: فشل في تثبيت المتطلبات
    pause
    exit /b 1
)

echo.
echo [3/6] تثبيت PyInstaller...
pip install pyinstaller
if %errorlevel% neq 0 (
    echo خطأ: فشل في تثبيت PyInstaller
    pause
    exit /b 1
)

echo.
echo [4/6] إنشاء مجلد .streamlit...
if not exist ".streamlit" mkdir .streamlit

echo.
echo [5/6] تنظيف البناء السابق...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build

echo.
echo [6/6] بناء التطبيق باستخدام المشغل...
pyinstaller launcher.spec
if %errorlevel% neq 0 (
    echo خطأ: فشل في بناء التطبيق
    pause
    exit /b 1
)

echo.
echo ========================================
echo تم بناء التطبيق بنجاح!
echo الملف التنفيذي موجود في: dist\SchoolManagementAdmin.exe
echo 
echo ملاحظة: هذا التطبيق يحتاج إلى:
echo - Python مثبت على النظام
echo - Streamlit مثبت (pip install streamlit)
echo ========================================
pause