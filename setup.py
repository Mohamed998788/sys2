from setuptools import setup, find_packages

setup(
    name="school-management-admin",
    version="1.0.0",
    description="نظام إدارة المدرسة - تطبيق الأدمن",
    author="School Management Team",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "pandas>=2.0.0",
        "plotly>=5.15.0",
        "firebase-admin>=6.2.0",
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "openpyxl>=3.1.0",
        "xlrd>=2.0.1",
        "requests>=2.31.0",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "school-admin=main:main",
        ],
    },
)