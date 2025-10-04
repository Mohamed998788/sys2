@echo off
echo ========================================
echo   إنشاء نسخة محمولة من تطبيق الأدمن
echo ========================================

echo.
echo [1/4] إنشاء مجلد النسخة المحمولة...
if exist "portable_admin" rmdir /s /q portable_admin
mkdir portable_admin

echo.
echo [2/4] نسخ الملفات...
copy *.py portable_admin\
copy requirements.txt portable_admin\
if exist ".streamlit" xcopy /s /e .streamlit portable_admin\.streamlit\
if exist "*.db" copy *.db portable_admin\

echo.
echo [3/4] إنشاء ملف التشغيل...
echo @echo off > portable_admin\run_admin.bat
echo echo تشغيل تطبيق إدارة المدرسة... >> portable_admin\run_admin.bat
echo echo. >> portable_admin\run_admin.bat
echo echo التحقق من المتطلبات... >> portable_admin\run_admin.bat
echo pip install -r requirements.txt ^>nul 2^>^&1 >> portable_admin\run_admin.bat
echo echo. >> portable_admin\run_admin.bat
echo echo تشغيل التطبيق... >> portable_admin\run_admin.bat
echo streamlit run main.py >> portable_admin\run_admin.bat
echo pause >> portable_admin\run_admin.bat

echo.
echo [4/4] إنشاء ملف README...
echo # تطبيق إدارة المدرسة - النسخة المحمولة > portable_admin\README.md
echo. >> portable_admin\README.md
echo ## متطلبات التشغيل: >> portable_admin\README.md
echo - Python 3.8 أو أحدث >> portable_admin\README.md
echo - pip ^(مدير حزم Python^) >> portable_admin\README.md
echo. >> portable_admin\README.md
echo ## طريقة التشغيل: >> portable_admin\README.md
echo 1. تأكد من تثبيت Python >> portable_admin\README.md
echo 2. اضغط مرتين على run_admin.bat >> portable_admin\README.md
echo 3. انتظر حتى يفتح التطبيق في المتصفح >> portable_admin\README.md
echo. >> portable_admin\README.md
echo ## الملفات المهمة: >> portable_admin\README.md
echo - main.py: الملف الرئيسي للتطبيق >> portable_admin\README.md
echo - config.py: إعدادات التطبيق >> portable_admin\README.md
echo - requirements.txt: المتطلبات >> portable_admin\README.md
echo - school_data.db: قاعدة البيانات المحلية >> portable_admin\README.md

echo.
echo ========================================
echo تم إنشاء النسخة المحمولة بنجاح!
echo المجلد: portable_admin\
echo للتشغيل: اضغط مرتين على portable_admin\run_admin.bat
echo ========================================
pause