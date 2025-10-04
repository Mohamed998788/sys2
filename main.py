import streamlit as st
import pandas as pd
import json
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
from database import DatabaseManager
from ai_processor import AIProcessor
from firebase_manager import FirebaseManager
from config import APP_TITLE, APP_ICON

# إعداد الصفحة
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# تهيئة المكونات
def init_components():
    db = DatabaseManager()
    ai = AIProcessor()
    firebase = FirebaseManager()
    return db, ai, firebase

# إعادة تهيئة المكونات في كل مرة لتجنب مشاكل التخزين المؤقت
db, ai, firebase = init_components()

def main():
    st.title(f"{APP_ICON} {APP_TITLE}")
    
    # الشريط الجانبي
    with st.sidebar:
        st.header("القائمة الرئيسية")
        page = st.selectbox(
            "اختر الصفحة",
            [
                "رفع الجدول المدرسي",
                "إدارة المعلمين",
                "إدارة الأكواد",
                "عرض الجدول",
                "الإحصائيات",
                "حذف البيانات"
            ]
        )
    
    # عرض الصفحات
    if page == "رفع الجدول المدرسي":
        upload_schedule_page()
    elif page == "إدارة المعلمين":
        manage_teachers_page()
    elif page == "إدارة الأكواد":
        manage_codes_page()
    elif page == "عرض الجدول":
        view_schedule_page()
    elif page == "الإحصائيات":
        statistics_page()
    elif page == "حذف البيانات":
        delete_data_page()

def upload_schedule_page():
    st.header("📁 رفع الجدول المدرسي")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("رفع ملف Excel")
        uploaded_file = st.file_uploader(
            "اختر ملف Excel",
            type=['xlsx', 'xls'],
            help="قم برفع ملف Excel يحتوي على الجدول المدرسي"
        )
        
        if uploaded_file is not None:
            try:
                # قراءة الملف
                df = pd.read_excel(uploaded_file)
                
                st.success("تم رفع الملف بنجاح!")
                
                # عرض معاينة البيانات
                st.subheader("معاينة البيانات")
                st.dataframe(df.head(10))
                
                # زر المعالجة
                if st.button("🤖 معالجة البيانات بالذكاء الاصطناعي", type="primary"):
                    with st.spinner("جاري معالجة البيانات..."):
                        # معالجة البيانات بالذكاء الاصطناعي
                        processed_data = ai.process_excel_to_json(df)
                        
                        if processed_data:
                            st.success("تم معالجة البيانات بنجاح!")
                            
                            # حفظ في قاعدة البيانات المحلية
                            if db.save_schedule(processed_data):
                                st.success("تم حفظ الجدول محلياً")
                            
                            # مزامنة مع Firebase
                            if firebase.sync_schedule(processed_data):
                                st.success("تم رفع الجدول إلى Firebase")
                            
                            # مزامنة المعلمين
                            if 'teachers' in processed_data:
                                teachers = processed_data['teachers']
                                for teacher in teachers:
                                    db.add_teacher(
                                        teacher['name'],
                                        teacher.get('teacher_code', ''),
                                        teacher.get('supervisor_code', ''),
                                        teacher.get('subjects', []),
                                        teacher.get('classes', [])
                                    )
                                
                                if firebase.sync_teachers(teachers):
                                    st.success("تم مزامنة بيانات المعلمين")
                            
                            # عرض النتائج
                            st.subheader("نتائج المعالجة")
                            
                            # عرض المعلمين
                            if 'teachers' in processed_data:
                                st.write("**المعلمين المستخرجين:**")
                                teachers_df = pd.DataFrame(processed_data['teachers'])
                                st.dataframe(teachers_df)
                            
                            # عرض الجدول
                            if 'schedule' in processed_data:
                                st.write("**الجدول المدرسي:**")
                                st.json(processed_data['schedule'])
                        else:
                            st.error("فشل في معالجة البيانات")
                            
            except Exception as e:
                st.error(f"خطأ في قراءة الملف: {e}")
    
    with col2:
        st.subheader("إرشادات")
        st.info("""
        **تنسيق الملف المطلوب:**
        - ملف Excel (.xlsx أو .xls)
        - يحتوي على أسماء المعلمين
        - يحتوي على المواد والفصول
        - منظم في جدول زمني
        
        **سيقوم النظام بـ:**
        - استخراج أسماء المعلمين
        - إنشاء أكواد تلقائية
        - تنظيم الجدول الزمني
        - حفظ البيانات محلياً
        - مزامنة مع Firebase
        """)

def manage_teachers_page():
    st.header("👥 إدارة المعلمين")
    
    # الحصول على المعلمين
    teachers = db.get_all_teachers()
    
    if teachers:
        st.subheader(f"المعلمين المسجلين ({len(teachers)})")
        
        # عرض المعلمين في جدول
        teachers_data = []
        for teacher in teachers:
            teachers_data.append({
                'الاسم': teacher['name'],
                'كود المعلم': teacher['teacher_code'],
                'كود المشرف': teacher['supervisor_code'] or 'غير محدد',
                'المواد': ', '.join(teacher['subjects']),
                'الفصول': ', '.join(teacher['classes']),
                'حالة الإشراف': 'مفعل' if teacher['is_supervisor_enabled'] else 'معطل'
            })
        
        df = pd.DataFrame(teachers_data)
        st.dataframe(df, use_container_width=True)
        
        # إحصائيات سريعة
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("إجمالي المعلمين", len(teachers))
        with col2:
            supervisors = sum(1 for t in teachers if t['supervisor_code'])
            st.metric("المشرفين", supervisors)
        with col3:
            active_supervisors = sum(1 for t in teachers if t['is_supervisor_enabled'])
            st.metric("المشرفين النشطين", active_supervisors)
    else:
        st.info("لا توجد بيانات معلمين. قم برفع جدول مدرسي أولاً.")

def manage_codes_page():
    st.header("🔐 إدارة الأكواد")
    
    teachers = db.get_all_teachers()
    
    if teachers:
        st.subheader("إدارة أكواد المعلمين")
        
        for teacher in teachers:
            with st.expander(f"👤 {teacher['name']}"):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.text_input(
                        "كود المعلم",
                        value=teacher['teacher_code'],
                        disabled=True,
                        key=f"teacher_code_{teacher['id']}"
                    )
                
                with col2:
                    st.text_input(
                        "كود المشرف",
                        value=teacher['supervisor_code'] or 'غير محدد',
                        disabled=True,
                        key=f"supervisor_code_{teacher['id']}"
                    )
                
                with col3:
                    current_status = teacher['is_supervisor_enabled']
                    new_status = st.toggle(
                        "تفعيل الإشراف",
                        value=current_status,
                        key=f"supervisor_toggle_{teacher['id']}"
                    )
                    
                    if new_status != current_status:
                        if db.update_supervisor_status(teacher['id'], new_status):
                            # مزامنة مع Firebase
                            updated_teachers = db.get_all_teachers()
                            firebase.sync_teachers(updated_teachers)
                            st.success("تم تحديث الحالة")
                            st.rerun()
                
                # معلومات إضافية
                st.write(f"**المواد:** {', '.join(teacher['subjects'])}")
                st.write(f"**الفصول:** {', '.join(teacher['classes'])}")
    else:
        st.info("لا توجد بيانات معلمين.")

def view_schedule_page():
    st.header("📅 عرض الجدول المدرسي")
    
    # الحصول على الجدول النشط
    schedule = db.get_active_schedule()
    
    if schedule and 'schedule' in schedule:
        schedule_data = schedule['schedule']
        
        if 'classes' in schedule_data:
            classes = schedule_data['classes']
            
            # اختيار الفصل
            class_names = list(classes.keys())
            selected_class = st.selectbox("اختر الفصل", class_names)
            
            if selected_class and selected_class in classes:
                st.subheader(f"جدول الفصل: {selected_class}")
                
                class_schedule = classes[selected_class]
                
                # عرض الجدول
                days = list(class_schedule.keys())
                
                for day in days:
                    st.write(f"**{day}**")
                    
                    periods = class_schedule[day]
                    
                    # إنشاء جدول للحصص
                    periods_data = []
                    for period in periods:
                        periods_data.append({
                            'الحصة': period.get('period', ''),
                            'المادة': period.get('subject', ''),
                            'المعلم': period.get('teacher', '')
                        })
                    
                    if periods_data:
                        df = pd.DataFrame(periods_data)
                        st.dataframe(df, use_container_width=True)
                    
                    st.divider()
        else:
            st.warning("لا توجد بيانات فصول في الجدول")
    else:
        st.info("لا يوجد جدول مدرسي نشط. قم برفع جدول أولاً.")

def add_sample_data_page():
    st.header("📝 إضافة بيانات تجريبية")
    
    if st.button("إضافة معلمين تجريبيين", type="primary"):
        sample_teachers = [
            {
                "name": "أحمد محمد",
                "teacher_code": "T001",
                "supervisor_code": "S001",
                "subjects": ["رياضيات", "فيزياء"],
                "classes": ["1/1", "1/2"],
                "is_supervisor_enabled": True
            },
            {
                "name": "فاطمة علي",
                "teacher_code": "T002", 
                "supervisor_code": "S002",
                "subjects": ["علوم", "كيمياء"],
                "classes": ["2/1", "2/2"],
                "is_supervisor_enabled": True
            },
            {
                "name": "محمد سالم",
                "teacher_code": "T003",
                "supervisor_code": "S003", 
                "subjects": ["لغة عربية"],
                "classes": ["3/1"],
                "is_supervisor_enabled": False
            }
        ]
        
        success_count = 0
        for teacher in sample_teachers:
            if db.add_teacher(
                teacher["name"],
                teacher["teacher_code"],
                teacher["supervisor_code"],
                teacher["subjects"],
                teacher["classes"]
            ):
                success_count += 1
        
        if success_count > 0:
            st.success(f"تم إضافة {success_count} معلمين بنجاح!")
            
            # مزامنة مع Firebase
            all_teachers = db.get_all_teachers()
            if firebase.sync_teachers(all_teachers):
                st.success("تم رفع البيانات إلى Firebase")
            else:
                st.warning("فشل في رفع البيانات إلى Firebase")
        else:
            st.error("فشل في إضافة المعلمين")
    
    st.subheader("الأكواد التجريبية:")
    st.code("""
أكواد المعلمين:
- T001 (أحمد محمد) - كود مشرف: S001
- T002 (فاطمة علي) - كود مشرف: S002  
- T003 (محمد سالم) - كود مشرف: S003 (معطل)

للاختبار:
1. معلم عادي: T003
2. معلم مع إشراف: T001 + S001
3. معلم مع إشراف معطل: T003 + S003
    """)

def statistics_page():
    st.header("📊 الإحصائيات")
    
    teachers = db.get_all_teachers()
    schedule = db.get_active_schedule()
    
    if teachers:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("إجمالي المعلمين", len(teachers))
        
        with col2:
            supervisors = sum(1 for t in teachers if t['supervisor_code'])
            st.metric("المشرفين", supervisors)
        
        with col3:
            active_supervisors = sum(1 for t in teachers if t['is_supervisor_enabled'])
            st.metric("المشرفين النشطين", active_supervisors)
        
        with col4:
            total_subjects = set()
            for teacher in teachers:
                total_subjects.update(teacher['subjects'])
            st.metric("إجمالي المواد", len(total_subjects))
        
        # رسم بياني للمواد
        st.subheader("توزيع المواد")
        subjects_count = {}
        for teacher in teachers:
            for subject in teacher['subjects']:
                subjects_count[subject] = subjects_count.get(subject, 0) + 1
        
        if subjects_count:
            fig = px.bar(
                x=list(subjects_count.keys()),
                y=list(subjects_count.values()),
                title="عدد المعلمين لكل مادة"
            )
            fig.update_layout(
                xaxis_title="المواد",
                yaxis_title="عدد المعلمين"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # رسم بياني للفصول
        st.subheader("توزيع الفصول")
        classes_count = {}
        for teacher in teachers:
            for class_name in teacher['classes']:
                classes_count[class_name] = classes_count.get(class_name, 0) + 1
        
        if classes_count:
            fig = px.pie(
                values=list(classes_count.values()),
                names=list(classes_count.keys()),
                title="توزيع المعلمين على الفصول"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("لا توجد بيانات لعرض الإحصائيات.")

def delete_data_page():
    st.header("🗑️ حذف البيانات")
    
    # زر إعادة تحميل المكونات
    if st.button("🔄 إعادة تحميل المكونات", help="في حالة ظهور أخطاء في الوظائف"):
        st.cache_data.clear()
        st.rerun()
    
    st.warning("⚠️ تحذير: هذه العملية لا يمكن التراجع عنها!")
    
    # إحصائيات البيانات الحالية
    st.subheader("📊 إحصائيات البيانات الحالية")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # عدد المعلمين
    teachers = db.get_all_teachers()
    with col1:
        st.metric("المعلمين (محلي)", len(teachers))
    
    # عدد الجداول
    active_schedule = db.get_active_schedule()
    with col2:
        st.metric("الجداول النشطة (محلي)", 1 if active_schedule else 0)
    
    # بيانات Firebase
    firebase_teachers = firebase.get_teachers()
    with col3:
        st.metric("المعلمين (Firebase)", len(firebase_teachers))
    
    firebase_schedule = firebase.get_current_schedule()
    with col4:
        st.metric("الجداول (Firebase)", 1 if firebase_schedule else 0)
    
    st.divider()
    
    # خيارات الحذف
    st.subheader("🎯 خيارات الحذف")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💾 البيانات المحلية")
        
        if st.button("🗑️ حذف جميع المعلمين (محلي)", type="secondary", use_container_width=True):
            if db.delete_all_teachers():
                st.success("✅ تم حذف جميع المعلمين من قاعدة البيانات المحلية")
                st.rerun()
            else:
                st.error("❌ فشل في حذف المعلمين")
        
        if st.button("🗑️ حذف جميع الجداول (محلي)", type="secondary", use_container_width=True):
            if db.delete_all_schedules():
                st.success("✅ تم حذف جميع الجداول من قاعدة البيانات المحلية")
                st.rerun()
            else:
                st.error("❌ فشل في حذف الجداول")
        
        if st.button("🗑️ حذف بيانات الحضور (محلي)", type="secondary", use_container_width=True):
            if db.delete_all_attendance():
                st.success("✅ تم حذف جميع بيانات الحضور من قاعدة البيانات المحلية")
                st.rerun()
            else:
                st.error("❌ فشل في حذف بيانات الحضور")
        
        if st.button("🗑️ حذف الحصص الاحتياطية (محلي)", type="secondary", use_container_width=True):
            if db.delete_all_substitute_classes():
                st.success("✅ تم حذف جميع الحصص الاحتياطية من قاعدة البيانات المحلية")
                st.rerun()
            else:
                st.error("❌ فشل في حذف الحصص الاحتياطية")
    
    with col2:
        st.markdown("### ☁️ بيانات Firebase")
        
        if st.button("🗑️ حذف جميع المعلمين (Firebase)", type="secondary", use_container_width=True):
            try:
                if hasattr(firebase, 'delete_all_teachers'):
                    if firebase.delete_all_teachers():
                        st.success("✅ تم حذف جميع المعلمين من Firebase")
                        st.rerun()
                    else:
                        st.error("❌ فشل في حذف المعلمين من Firebase")
                else:
                    st.error("❌ الوظيفة غير متوفرة - يرجى إعادة تشغيل التطبيق")
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")
        
        if st.button("🗑️ حذف جميع الجداول (Firebase)", type="secondary", use_container_width=True):
            try:
                if hasattr(firebase, 'delete_all_schedules'):
                    if firebase.delete_all_schedules():
                        st.success("✅ تم حذف جميع الجداول من Firebase")
                        st.rerun()
                    else:
                        st.error("❌ فشل في حذف الجداول من Firebase")
                else:
                    st.error("❌ الوظيفة غير متوفرة - يرجى إعادة تشغيل التطبيق")
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")
        
        if st.button("🗑️ حذف بيانات الحضور (Firebase)", type="secondary", use_container_width=True):
            try:
                if hasattr(firebase, 'delete_all_attendance'):
                    if firebase.delete_all_attendance():
                        st.success("✅ تم حذف جميع بيانات الحضور من Firebase")
                        st.rerun()
                    else:
                        st.error("❌ فشل في حذف بيانات الحضور من Firebase")
                else:
                    st.error("❌ الوظيفة غير متوفرة - يرجى إعادة تشغيل التطبيق")
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")
        
        if st.button("🗑️ حذف الحصص الاحتياطية (Firebase)", type="secondary", use_container_width=True):
            try:
                if hasattr(firebase, 'delete_all_substitute_classes'):
                    if firebase.delete_all_substitute_classes():
                        st.success("✅ تم حذف جميع الحصص الاحتياطية من Firebase")
                        st.rerun()
                    else:
                        st.error("❌ فشل في حذف الحصص الاحتياطية من Firebase")
                else:
                    st.error("❌ الوظيفة غير متوفرة - يرجى إعادة تشغيل التطبيق")
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")
    
    st.divider()
    
    # حذف جميع البيانات
    st.subheader("💥 حذف جميع البيانات")
    
    st.error("⚠️ خطر: سيتم حذف جميع البيانات نهائياً!")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("💾 حذف جميع البيانات المحلية", type="primary", use_container_width=True):
            with st.spinner("جاري حذف البيانات المحلية..."):
                if db.delete_all_data():
                    st.success("✅ تم حذف جميع البيانات المحلية بنجاح")
                    st.rerun()
                else:
                    st.error("❌ فشل في حذف البيانات المحلية")
    
    with col2:
        if st.button("☁️ حذف جميع بيانات Firebase", type="primary", use_container_width=True):
            with st.spinner("جاري حذف بيانات Firebase..."):
                try:
                    if hasattr(firebase, 'delete_all_data'):
                        if firebase.delete_all_data():
                            st.success("✅ تم حذف جميع بيانات Firebase بنجاح")
                            st.rerun()
                        else:
                            st.error("❌ فشل في حذف بيانات Firebase")
                    else:
                        st.error("❌ الوظيفة غير متوفرة - يرجى إعادة تشغيل التطبيق")
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")
    
    with col3:
        if st.button("🔥 حذف جميع البيانات (محلي + Firebase)", type="primary", use_container_width=True):
            with st.spinner("جاري حذف جميع البيانات..."):
                try:
                    local_success = db.delete_all_data()
                    firebase_success = False
                    
                    if hasattr(firebase, 'delete_all_data'):
                        firebase_success = firebase.delete_all_data()
                    else:
                        st.warning("⚠️ وظائف حذف Firebase غير متوفرة")
                    
                    if local_success and firebase_success:
                        st.success("✅ تم حذف جميع البيانات بنجاح من المصدرين")
                        st.rerun()
                    elif local_success:
                        st.warning("⚠️ تم حذف البيانات المحلية فقط")
                    elif firebase_success:
                        st.warning("⚠️ تم حذف بيانات Firebase فقط")
                    else:
                        st.error("❌ فشل في حذف البيانات من كلا المصدرين")
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")
    
    # معلومات إضافية
    st.divider()
    st.info("""
    📝 **ملاحظات مهمة:**
    - عملية الحذف لا يمكن التراجع عنها
    - يُنصح بعمل نسخة احتياطية قبل الحذف
    - البيانات المحلية محفوظة في ملف `school_data.db`
    - بيانات Firebase محفوظة في السحابة
    - يمكن حذف البيانات من مصدر واحد أو كلا المصدرين
    """)

if __name__ == "__main__":
    main()