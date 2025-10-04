"""
مشغل Streamlit كتطبيق EXE
"""
import subprocess
import sys
import os
import webbrowser
import time
import threading
from pathlib import Path

def check_port(port):
    """فحص إذا كان المنفذ متاح"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0

def find_free_port():
    """العثور على منفذ متاح"""
    for port in range(8501, 8510):
        if check_port(port):
            return port
    return 8501

def open_browser(url, delay=3):
    """فتح المتصفح بعد تأخير"""
    time.sleep(delay)
    webbrowser.open(url)

def main():
    print("🏫 نظام إدارة المدرسة")
    print("=" * 40)
    
    # التحقق من الملفات المطلوبة
    required_files = [
        "main.py",
        "alnassr-ab9fd-firebase-adminsdk-fbsvc-24f5614874.json"
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ ملف مطلوب غير موجود: {file}")
            input("اضغط Enter للخروج...")
            return
    
    # العثور على منفذ متاح
    port = find_free_port()
    url = f"http://localhost:{port}"
    
    print(f"🚀 بدء تشغيل التطبيق على المنفذ {port}")
    print(f"🌐 رابط التطبيق: {url}")
    print("⏹ اضغط Ctrl+C لإيقاف التطبيق")
    print("-" * 40)
    
    # فتح المتصفح في خيط منفصل
    browser_thread = threading.Thread(
        target=open_browser, 
        args=(url,)
    )
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # تشغيل Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "main.py",
            "--server.port", str(port),
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n⏹ تم إيقاف التطبيق")
    except Exception as e:
        print(f"❌ خطأ: {e}")
        input("اضغط Enter للخروج...")

if __name__ == "__main__":
    main()