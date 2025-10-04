import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "school_data.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """إنشاء قاعدة البيانات والجداول"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # جدول المعلمين
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS teachers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    teacher_code TEXT UNIQUE NOT NULL,
                    supervisor_code TEXT UNIQUE,
                    subjects TEXT,
                    classes TEXT,
                    is_supervisor_enabled BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول الجداول المدرسية
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS schedules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    schedule_data TEXT NOT NULL,
                    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # جدول الحضور والغياب
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    teacher_id INTEGER,
                    date DATE,
                    is_present BOOLEAN,
                    FOREIGN KEY (teacher_id) REFERENCES teachers (id)
                )
            ''')
            
            # جدول الحصص الاحتياطية
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS substitute_classes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_teacher_id INTEGER,
                    substitute_teacher_id INTEGER,
                    class_name TEXT,
                    period TEXT,
                    date DATE,
                    week_number INTEGER,
                    FOREIGN KEY (original_teacher_id) REFERENCES teachers (id),
                    FOREIGN KEY (substitute_teacher_id) REFERENCES teachers (id)
                )
            ''')
            
            conn.commit()
    
    def add_teacher(self, name: str, teacher_code: str, supervisor_code: str = None, 
                   subjects: List[str] = None, classes: List[str] = None) -> bool:
        """إضافة معلم جديد"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO teachers (name, teacher_code, supervisor_code, subjects, classes)
                    VALUES (?, ?, ?, ?, ?)
                ''', (name, teacher_code, supervisor_code, 
                     json.dumps(subjects or []), json.dumps(classes or [])))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def get_all_teachers(self) -> List[Dict]:
        """الحصول على جميع المعلمين"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM teachers')
            teachers = []
            for row in cursor.fetchall():
                teacher = {
                    'id': row[0],
                    'name': row[1],
                    'teacher_code': row[2],
                    'supervisor_code': row[3],
                    'subjects': json.loads(row[4]) if row[4] else [],
                    'classes': json.loads(row[5]) if row[5] else [],
                    'is_supervisor_enabled': bool(row[6]),
                    'created_at': row[7]
                }
                teachers.append(teacher)
            return teachers
    
    def update_supervisor_status(self, teacher_id: int, enabled: bool) -> bool:
        """تحديث حالة الإشراف للمعلم"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE teachers SET is_supervisor_enabled = ? WHERE id = ?
                ''', (enabled, teacher_id))
                conn.commit()
                return True
        except:
            return False
    
    def save_schedule(self, schedule_data: Dict) -> bool:
        """حفظ الجدول المدرسي"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # إلغاء تفعيل الجداول السابقة
                cursor.execute('UPDATE schedules SET is_active = 0')
                # إضافة الجدول الجديد
                cursor.execute('''
                    INSERT INTO schedules (schedule_data, is_active)
                    VALUES (?, 1)
                ''', (json.dumps(schedule_data),))
                conn.commit()
                return True
        except:
            return False
    
    def get_active_schedule(self) -> Optional[Dict]:
        """الحصول على الجدول النشط"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT schedule_data FROM schedules WHERE is_active = 1 ORDER BY upload_date DESC LIMIT 1')
            result = cursor.fetchone()
            if result:
                return json.loads(result[0])
            return None
    
    def delete_all_teachers(self) -> bool:
        """حذف جميع المعلمين من قاعدة البيانات المحلية"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM teachers')
                count = cursor.fetchone()[0]
                
                cursor.execute('DELETE FROM teachers')
                conn.commit()
                
                print(f"تم حذف {count} معلم من قاعدة البيانات المحلية")
                return True
        except Exception as e:
            print(f"خطأ في حذف المعلمين من قاعدة البيانات المحلية: {e}")
            return False
    
    def delete_all_schedules(self) -> bool:
        """حذف جميع الجداول من قاعدة البيانات المحلية"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM schedules')
                count = cursor.fetchone()[0]
                
                cursor.execute('DELETE FROM schedules')
                conn.commit()
                
                print(f"تم حذف {count} جدول من قاعدة البيانات المحلية")
                return True
        except Exception as e:
            print(f"خطأ في حذف الجداول من قاعدة البيانات المحلية: {e}")
            return False
    
    def delete_all_attendance(self) -> bool:
        """حذف جميع بيانات الحضور من قاعدة البيانات المحلية"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM attendance')
                count = cursor.fetchone()[0]
                
                cursor.execute('DELETE FROM attendance')
                conn.commit()
                
                print(f"تم حذف {count} سجل حضور من قاعدة البيانات المحلية")
                return True
        except Exception as e:
            print(f"خطأ في حذف بيانات الحضور من قاعدة البيانات المحلية: {e}")
            return False
    
    def delete_all_substitute_classes(self) -> bool:
        """حذف جميع الحصص الاحتياطية من قاعدة البيانات المحلية"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM substitute_classes')
                count = cursor.fetchone()[0]
                
                cursor.execute('DELETE FROM substitute_classes')
                conn.commit()
                
                print(f"تم حذف {count} حصة احتياطية من قاعدة البيانات المحلية")
                return True
        except Exception as e:
            print(f"خطأ في حذف الحصص الاحتياطية من قاعدة البيانات المحلية: {e}")
            return False
    
    def delete_all_data(self) -> bool:
        """حذف جميع البيانات من قاعدة البيانات المحلية"""
        try:
            success = True
            success &= self.delete_all_substitute_classes()  # حذف الحصص الاحتياطية أولاً (foreign keys)
            success &= self.delete_all_attendance()  # حذف الحضور ثانياً (foreign keys)
            success &= self.delete_all_teachers()  # حذف المعلمين
            success &= self.delete_all_schedules()  # حذف الجداول
            
            if success:
                print("تم حذف جميع البيانات من قاعدة البيانات المحلية بنجاح")
            else:
                print("حدث خطأ أثناء حذف بعض البيانات من قاعدة البيانات المحلية")
            
            return success
        except Exception as e:
            print(f"خطأ في حذف جميع البيانات من قاعدة البيانات المحلية: {e}")
            return False