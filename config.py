import os
from dotenv import load_dotenv

load_dotenv()

# Firebase Configuration - استخدام ملف JSON
FIREBASE_SERVICE_ACCOUNT_PATH = "alnassr-ab9fd-firebase-adminsdk-fbsvc-24f5614874.json"

# AI API Configuration (استخدام OpenRouter مع Grok-4-Fast المجاني)
AI_API_KEY = os.getenv("OPENROUTER_API_KEY")
AI_API_URL = "https://openrouter.ai/api/v1/chat/completions"
AI_MODEL = "x-ai/grok-4-fast:free"

# OpenRouter Headers
OPENROUTER_HEADERS = {
    "HTTP-Referer": "https://school-management-system.local",
    "X-Title": "School Management System"
}

# Database Configuration
DATABASE_PATH = "school_data.db"

# App Configuration
APP_TITLE = "نظام إدارة المدرسة - لوحة التحكم"
APP_ICON = "🏫"