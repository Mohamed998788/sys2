"""
سكريبت لبناء تطبيق الإدارة كملف EXE
"""
import os
import subprocess
import sys

def install_pyinstaller():
    """تثبيت PyInstaller"""
    print("تثبيت PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def create_spec_file():
    """إنشاء ملف spec مخصص"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('alnassr-ab9fd-firebase-adminsdk-fbsvc-24f5614874.json', '.'),
        ('.env', '.'),
    ],
    hiddenimports=[
        'streamlit',
        'pandas',
        'firebase_admin',
        'google.cloud.firestore',
        'requests',
        'plotly',
        'openpyxl',
        'sqlite3',
        'python-dotenv'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SchoolManagementAdmin',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='school_icon.ico'
)
'''
    
    with open('school_admin.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("تم إنشاء ملف school_admin.spec")

def build_exe():
    """بناء ملف EXE"""
    print("بناء ملف EXE...")
    
    # إنشاء ملف spec
    create_spec_file()
    
    # بناء EXE
    subprocess.check_call([
        "pyinstaller", 
        "--onefile",
        "--name=SchoolManagementAdmin",
        "--add-data=alnassr-ab9fd-firebase-adminsdk-fbsvc-24f5614874.json;.",
        "--hidden-import=streamlit",
        "--hidden-import=pandas",
        "--hidden-import=firebase_admin",
        "--hidden-import=requests",
        "--hidden-import=plotly",
        "--hidden-import=openpyxl",
        "main.py"
    ])
    
    print("تم بناء ملف EXE بنجاح!")
    print("الملف موجود في: dist/SchoolManagementAdmin.exe")

if __name__ == "__main__":
    try:
        install_pyinstaller()
        build_exe()
    except Exception as e:
        print(f"خطأ: {e}")
        input("اضغط Enter للخروج...")