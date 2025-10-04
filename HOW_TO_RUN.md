# كيفية تشغيل تطبيق الإدارة

## ⚠️ تنبيه مهم
**لا تستخدم `python main.py` مباشرة!**

تطبيق الإدارة مبني بـ Streamlit ويجب تشغيله بالطريقة الصحيحة.

## ✅ الطرق الصحيحة للتشغيل

### 1. الطريقة السريعة (Windows)
```cmd
# في مجلد admin_app
run.bat
```

### 2. باستخدام PowerShell
```powershell
# في مجلد admin_app
.\run.ps1
```

### 3. الطريقة اليدوية
```cmd
# في مجلد admin_app
streamlit run main.py
```

### 4. من المجلد الرئيسي
```cmd
# في مجلد school_management_system
run_admin.bat
```

## 🌐 الوصول للتطبيق

بعد التشغيل الناجح:
1. افتح المتصفح
2. اذهب إلى: `http://localhost:8501`
3. ستظهر واجهة تطبيق الإدارة

## 🔧 حل المشاكل

### مشكلة: "streamlit: command not found"
```cmd
pip install streamlit
```

### مشكلة: "No module named 'streamlit'"
```cmd
pip install -r requirements.txt
```

### مشكلة: "Port 8501 is already in use"
```cmd
# استخدم منفذ آخر
streamlit run main.py --server.port 8502
```

### مشكلة: Firebase connection error
1. تأكد من وجود ملف `.env`
2. تحقق من صحة مفاتيح Firebase
3. تأكد من تفعيل Firestore في Firebase Console

### مشكلة: OpenRouter API error
1. تأكد من صحة `OPENROUTER_API_KEY` في `.env`
2. تحقق من رصيد الحساب في OpenRouter
3. تأكد من اتصال الإنترنت

## 📋 متطلبات التشغيل

### Python Packages:
- streamlit
- pandas
- firebase-admin
- requests
- python-dotenv

### ملفات الإعداد:
- `.env` (منسوخ من `.env.example`)
- Firebase service account key

### الخدمات الخارجية:
- Firebase Firestore (مفعل)
- OpenRouter API key (مجاني)

## 🎯 الاستخدام الأول

1. **إعداد Firebase:**
   - إنشاء مشروع Firebase
   - تفعيل Firestore
   - تحميل service account key
   - تحديث `.env`

2. **إعداد OpenRouter:**
   - التسجيل في openrouter.ai
   - إنشاء API key
   - إضافة المفتاح في `.env`

3. **تشغيل التطبيق:**
   ```cmd
   run.bat
   ```

4. **رفع أول جدول:**
   - اختر ملف Excel
   - اضغط "معالجة البيانات"
   - راجع النتائج

## 📞 الدعم

إذا واجهت مشاكل:
1. تحقق من ملفات السجل في Terminal
2. راجع ملف `INSTALLATION.md`
3. تأكد من إعداد `.env` بشكل صحيح

---

🎉 **مبروك!** الآن يمكنك استخدام تطبيق الإدارة بشكل صحيح!