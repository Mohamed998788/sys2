import firebase_admin
from firebase_admin import credentials, firestore
from typing import Dict, List, Optional
import json
from config import FIREBASE_SERVICE_ACCOUNT_PATH

class FirebaseManager:
    def __init__(self):
        self.db = None
        self.init_firebase()
    
    def init_firebase(self):
        """تهيئة Firebase"""
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(FIREBASE_SERVICE_ACCOUNT_PATH)
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            print("تم الاتصال بـ Firebase بنجاح")
        except Exception as e:
            print(f"خطأ في الاتصال بـ Firebase: {e}")
    
    def sync_teachers(self, teachers_data: List[Dict]) -> bool:
        """مزامنة بيانات المعلمين مع Firebase"""
        try:
            if not self.db:
                return False
            
            # حذف البيانات القديمة
            teachers_ref = self.db.collection('teachers')
            docs = teachers_ref.stream()
            for doc in docs:
                doc.reference.delete()
            
            # إضافة البيانات الجديدة
            for teacher in teachers_data:
                teachers_ref.add(teacher)
            
            return True
        except Exception as e:
            print(f"خطأ في مزامنة المعلمين: {e}")
            return False
    
    def sync_schedule(self, schedule_data: Dict) -> bool:
        """مزامنة الجدول المدرسي مع Firebase"""
        try:
            if not self.db:
                return False
            
            # حفظ الجدول
            schedule_ref = self.db.collection('schedules').document('current')
            schedule_ref.set({
                'data': schedule_data,
                'last_updated': firestore.SERVER_TIMESTAMP,
                'is_active': True
            })
            
            return True
        except Exception as e:
            print(f"خطأ في مزامنة الجدول: {e}")
            return False
    
    def update_attendance(self, attendance_data: Dict) -> bool:
        """تحديث بيانات الحضور والغياب"""
        try:
            if not self.db:
                return False
            
            date_str = attendance_data.get('date', '')
            attendance_ref = self.db.collection('attendance').document(date_str)
            attendance_ref.set(attendance_data)
            
            return True
        except Exception as e:
            print(f"خطأ في تحديث الحضور: {e}")
            return False
    
    def update_substitute_classes(self, substitute_data: List[Dict]) -> bool:
        """تحديث بيانات الحصص الاحتياطية"""
        try:
            if not self.db:
                return False
            
            # حذف البيانات القديمة لهذا الأسبوع
            week_number = substitute_data[0].get('week_number') if substitute_data else 0
            
            substitutes_ref = self.db.collection('substitute_classes')
            old_docs = substitutes_ref.where('week_number', '==', week_number).stream()
            for doc in old_docs:
                doc.reference.delete()
            
            # إضافة البيانات الجديدة
            for substitute in substitute_data:
                substitutes_ref.add(substitute)
            
            return True
        except Exception as e:
            print(f"خطأ في تحديث الحصص الاحتياطية: {e}")
            return False
    
    def get_teachers(self) -> List[Dict]:
        """الحصول على بيانات المعلمين من Firebase"""
        try:
            if not self.db:
                return []
            
            teachers_ref = self.db.collection('teachers')
            docs = teachers_ref.stream()
            
            teachers = []
            for doc in docs:
                teacher_data = doc.to_dict()
                teacher_data['id'] = doc.id
                teachers.append(teacher_data)
            
            return teachers
        except Exception as e:
            print(f"خطأ في جلب بيانات المعلمين: {e}")
            return []
    
    def get_current_schedule(self) -> Optional[Dict]:
        """الحصول على الجدول الحالي من Firebase"""
        try:
            if not self.db:
                return None
            
            schedule_ref = self.db.collection('schedules').document('current')
            doc = schedule_ref.get()
            
            if doc.exists:
                return doc.to_dict().get('data')
            return None
        except Exception as e:
            print(f"خطأ في جلب الجدول: {e}")
            return None
    
    def delete_all_teachers(self) -> bool:
        """حذف جميع بيانات المعلمين من Firebase"""
        try:
            if not self.db:
                return False
            
            teachers_ref = self.db.collection('teachers')
            docs = teachers_ref.stream()
            
            deleted_count = 0
            for doc in docs:
                doc.reference.delete()
                deleted_count += 1
            
            print(f"تم حذف {deleted_count} معلم من Firebase")
            return True
        except Exception as e:
            print(f"خطأ في حذف بيانات المعلمين: {e}")
            return False
    
    def delete_all_schedules(self) -> bool:
        """حذف جميع الجداول من Firebase"""
        try:
            if not self.db:
                return False
            
            schedules_ref = self.db.collection('schedules')
            docs = schedules_ref.stream()
            
            deleted_count = 0
            for doc in docs:
                doc.reference.delete()
                deleted_count += 1
            
            print(f"تم حذف {deleted_count} جدول من Firebase")
            return True
        except Exception as e:
            print(f"خطأ في حذف الجداول: {e}")
            return False
    
    def delete_all_attendance(self) -> bool:
        """حذف جميع بيانات الحضور من Firebase"""
        try:
            if not self.db:
                return False
            
            attendance_ref = self.db.collection('attendance')
            docs = attendance_ref.stream()
            
            deleted_count = 0
            for doc in docs:
                doc.reference.delete()
                deleted_count += 1
            
            print(f"تم حذف {deleted_count} سجل حضور من Firebase")
            return True
        except Exception as e:
            print(f"خطأ في حذف بيانات الحضور: {e}")
            return False
    
    def delete_all_substitute_classes(self) -> bool:
        """حذف جميع بيانات الحصص الاحتياطية من Firebase"""
        try:
            if not self.db:
                return False
            
            substitutes_ref = self.db.collection('substitute_classes')
            docs = substitutes_ref.stream()
            
            deleted_count = 0
            for doc in docs:
                doc.reference.delete()
                deleted_count += 1
            
            print(f"تم حذف {deleted_count} حصة احتياطية من Firebase")
            return True
        except Exception as e:
            print(f"خطأ في حذف الحصص الاحتياطية: {e}")
            return False
    
    def delete_all_data(self) -> bool:
        """حذف جميع البيانات من Firebase"""
        try:
            success = True
            success &= self.delete_all_teachers()
            success &= self.delete_all_schedules()
            success &= self.delete_all_attendance()
            success &= self.delete_all_substitute_classes()
            
            if success:
                print("تم حذف جميع البيانات من Firebase بنجاح")
            else:
                print("حدث خطأ أثناء حذف بعض البيانات")
            
            return success
        except Exception as e:
            print(f"خطأ في حذف جميع البيانات: {e}")
            return False