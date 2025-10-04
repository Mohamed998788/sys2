#!/usr/bin/env python3
"""
مشغل تطبيق إدارة المدرسة
يقوم بتشغيل Streamlit في نافذة منفصلة
"""

import os
import sys
import subprocess
import webbrowser
import time
import socket
from threading import Thread
import tkinter as tk
from tkinter import messagebox, ttk

class SchoolAdminLauncher:
    def __init__(self):
        self.process = None
        self.port = 8501
        self.root = None
        
    def find_free_port(self):
        """البحث عن منفذ متاح"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    def is_port_in_use(self, port):
        """التحقق من استخدام المنفذ"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0
    
    def start_streamlit(self):
        """تشغيل Streamlit"""
        try:
            # البحث عن منفذ متاح إذا كان المنفذ الافتراضي مستخدم
            if self.is_port_in_use(self.port):
                self.port = self.find_free_port()
            
            # تشغيل Streamlit
            cmd = [
                sys.executable, "-m", "streamlit", "run", "main.py",
                "--server.port", str(self.port),
                "--server.headless", "true",
                "--browser.gatherUsageStats", "false"
            ]
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            
            # انتظار تشغيل الخادم
            time.sleep(3)
            
            # فتح المتصفح
            url = f"http://localhost:{self.port}"
            webbrowser.open(url)
            
            return True
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تشغيل التطبيق:\n{str(e)}")
            return False
    
    def stop_streamlit(self):
        """إيقاف Streamlit"""
        if self.process:
            self.process.terminate()
            self.process = None
    
    def create_gui(self):
        """إنشاء واجهة المستخدم"""
        self.root = tk.Tk()
        self.root.title("نظام إدارة المدرسة")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # تعيين الخط العربي
        try:
            self.root.option_add('*Font', 'Arial 12')
        except:
            pass
        
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # العنوان
        title_label = ttk.Label(
            main_frame, 
            text="🏫 نظام إدارة المدرسة", 
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # معلومات التطبيق
        info_text = """
        تطبيق إدارة المدرسة - لوحة التحكم
        
        • رفع وتحليل الجداول المدرسية
        • إدارة المعلمين والأكواد
        • مراقبة الحضور والغياب
        • إحصائيات شاملة
        """
        
        info_label = ttk.Label(main_frame, text=info_text, justify=tk.CENTER)
        info_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # أزرار التحكم
        start_button = ttk.Button(
            main_frame, 
            text="🚀 تشغيل التطبيق", 
            command=self.on_start_click,
            width=20
        )
        start_button.grid(row=2, column=0, padx=(0, 10), pady=5)
        
        stop_button = ttk.Button(
            main_frame, 
            text="⏹️ إيقاف التطبيق", 
            command=self.on_stop_click,
            width=20
        )
        stop_button.grid(row=2, column=1, padx=(10, 0), pady=5)
        
        # شريط الحالة
        self.status_var = tk.StringVar()
        self.status_var.set("جاهز للتشغيل")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        # معلومات إضافية
        footer_text = "الإصدار 1.0.0 | تطوير فريق إدارة المدرسة"
        footer_label = ttk.Label(main_frame, text=footer_text, font=('Arial', 8))
        footer_label.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        # إعداد الإغلاق
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        return self.root
    
    def on_start_click(self):
        """معالج زر التشغيل"""
        self.status_var.set("جاري تشغيل التطبيق...")
        self.root.update()
        
        if self.start_streamlit():
            self.status_var.set(f"التطبيق يعمل على المنفذ {self.port}")
        else:
            self.status_var.set("فشل في تشغيل التطبيق")
    
    def on_stop_click(self):
        """معالج زر الإيقاف"""
        self.stop_streamlit()
        self.status_var.set("تم إيقاف التطبيق")
    
    def on_closing(self):
        """معالج إغلاق النافذة"""
        if self.process:
            if messagebox.askokcancel("إغلاق", "هل تريد إيقاف التطبيق والخروج؟"):
                self.stop_streamlit()
                self.root.destroy()
        else:
            self.root.destroy()
    
    def run(self):
        """تشغيل المشغل"""
        gui = self.create_gui()
        gui.mainloop()

def main():
    """الدالة الرئيسية"""
    # التحقق من وجود الملفات المطلوبة
    if not os.path.exists('main.py'):
        messagebox.showerror("خطأ", "ملف main.py غير موجود!")
        return
    
    # تشغيل المشغل
    launcher = SchoolAdminLauncher()
    launcher.run()

if __name__ == "__main__":
    main()