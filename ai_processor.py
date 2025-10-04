import requests
import json
import pandas as pd
from typing import Dict, List, Optional
from config import AI_API_KEY, AI_API_URL, AI_MODEL, OPENROUTER_HEADERS

class AIProcessor:
    def __init__(self):
        self.api_key = AI_API_KEY
        self.api_url = AI_API_URL
    
    def process_excel_to_json(self, excel_data: pd.DataFrame) -> Dict:
        """تحويل ملف Excel إلى JSON باستخدام الذكاء الاصطناعي"""
        
        # تحويل البيانات إلى نص
        excel_text = excel_data.to_string()
        
        prompt = f"""
        أنت Grok، مساعد ذكي متخصص في تحليل الجداول المدرسية. قم بتحليل البيانات التالية وتحويلها إلى JSON منظم.

        البيانات المدرسية:
        {excel_text}

        المهام المطلوبة:
        1. استخراج أسماء جميع المعلمين بدقة
        2. تحديد المواد التي يدرسها كل معلم
        3. تحديد الفصول التي يدرس لها كل معلم
        4. إنشاء جدول زمني منظم للحصص
        5. إنشاء أكواد تلقائية للمعلمين والمشرفين

        تنسيق JSON المطلوب:
        {{
            "teachers": [
                {{
                    "name": "اسم المعلم",
                    "subjects": ["المادة1", "المادة2"],
                    "classes": ["1/1", "1/2"],
                    "teacher_code": "T001",
                    "supervisor_code": "S001"
                }}
            ],
            "schedule": {{
                "classes": {{
                    "1/1": {{
                        "الأحد": [
                            {{"period": "الحصة الأولى", "subject": "الرياضيات", "teacher": "أحمد محمد"}},
                            {{"period": "الحصة الثانية", "subject": "العلوم", "teacher": "فاطمة علي"}}
                        ],
                        "الاثنين": [
                            {{"period": "الحصة الأولى", "subject": "اللغة العربية", "teacher": "محمد سالم"}}
                        ]
                    }}
                }}
            }}
        }}

        قواعد مهمة:
        - استخرج الأسماء العربية بدقة تامة
        - نظم الجدول حسب الأيام (الأحد، الاثنين، الثلاثاء، الأربعاء، الخميس)
        - أنشئ أكواد متسلسلة للمعلمين (T001, T002, ...) والمشرفين (S001, S002, ...)
        - أرجع JSON صالح فقط بدون أي نص إضافي أو تفسيرات
        - تأكد من صحة تركيب JSON
        """
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                **OPENROUTER_HEADERS
            }
            
            data = {
                "model": AI_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": "أنت Grok، مساعد ذكي متخصص في تحليل وتنظيم البيانات المدرسية. تتميز بالدقة في استخراج الأسماء العربية وتنظيم الجداول الزمنية."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.2,
                "max_tokens": 6000,
                "top_p": 0.9,
                "frequency_penalty": 0.1,
                "presence_penalty": 0.1
            }
            
            response = requests.post(self.api_url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                # محاولة تحليل JSON من الاستجابة
                try:
                    # البحث عن JSON في الاستجابة
                    start_idx = ai_response.find('{')
                    end_idx = ai_response.rfind('}') + 1
                    json_str = ai_response[start_idx:end_idx]
                    
                    parsed_data = json.loads(json_str)
                    return self._validate_and_enhance_data(parsed_data)
                    
                except json.JSONDecodeError:
                    # في حالة فشل التحليل، إنشاء بيانات افتراضية
                    return self._create_fallback_data(excel_data)
            else:
                return self._create_fallback_data(excel_data)
                
        except Exception as e:
            print(f"خطأ في معالجة AI: {e}")
            return self._create_fallback_data(excel_data)
    
    def _validate_and_enhance_data(self, data: Dict) -> Dict:
        """التحقق من صحة البيانات وتحسينها"""
        
        # إضافة أكواد للمعلمين
        if 'teachers' in data:
            for i, teacher in enumerate(data['teachers']):
                teacher['teacher_code'] = f"T{str(i+1).zfill(3)}"
                teacher['supervisor_code'] = f"S{str(i+1).zfill(3)}"
        
        # التأكد من وجود هيكل الجدول
        if 'schedule' not in data:
            data['schedule'] = {"classes": {}}
        
        return data
    
    def _create_fallback_data(self, excel_data: pd.DataFrame) -> Dict:
        """إنشاء بيانات افتراضية في حالة فشل AI"""
        
        # استخراج أسماء المعلمين من البيانات
        teachers = []
        teacher_names = set()
        
        # البحث عن أسماء في البيانات
        for col in excel_data.columns:
            for val in excel_data[col].dropna():
                if isinstance(val, str) and len(val.split()) >= 2:
                    teacher_names.add(val)
        
        # إنشاء قائمة المعلمين
        for i, name in enumerate(list(teacher_names)[:20]):  # حد أقصى 20 معلم
            teachers.append({
                "name": name,
                "subjects": ["مادة عامة"],
                "classes": ["1/1"],
                "teacher_code": f"T{str(i+1).zfill(3)}",
                "supervisor_code": f"S{str(i+1).zfill(3)}"
            })
        
        return {
            "teachers": teachers,
            "schedule": {
                "classes": {
                    "1/1": {
                        "الأحد": [
                            {"period": "الحصة الأولى", "subject": "مادة عامة", "teacher": teachers[0]["name"] if teachers else "معلم افتراضي"}
                        ]
                    }
                }
            }
        }
    
    def generate_teacher_codes(self, teachers_count: int) -> List[Dict[str, str]]:
        """إنشاء أكواد للمعلمين"""
        codes = []
        for i in range(1, teachers_count + 1):
            codes.append({
                "teacher_code": f"T{str(i).zfill(3)}",
                "supervisor_code": f"S{str(i).zfill(3)}"
            })
        return codes