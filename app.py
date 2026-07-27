import os
import streamlit as st
from typing import Dict, Any

# 1. إعداد الصفحة بنفس أسلوب وهوية المعهد
st.set_page_config(
    page_title="مساعد معهد المشورة - خدمة العملاء",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. تحميل المفاتيح ومتغيرات البيئة من Streamlit Secrets
def load_secrets():
    secret_keys = ["LLM_API", "MODEL_NAME", "GROQ_API_KEY"]
    for key in secret_keys:
        if key in st.secrets:
            os.environ[key] = str(st.secrets[key])

load_secrets()

# 3. استيراد الـ Workflow الخفيف المصمم للمعهد
try:
    from workflow import app as workflow_app
except Exception as e:
    st.error("تعذر تحميل نظام المساعد الذكي (workflow.py). يرجى التأكد من المجلد والملفات.")
    st.exception(e)
    st.stop()

# 4. تهيئة حالة الجلسة (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. واجهة المعهد الرئيسية (الهيدر)
st.title("🏛️ مساعد معهد المشورة الذكي")
st.caption("أهلاً بك! أنا السكرتيرة الافتراضية لمعهد المشورة. أقدر أساعدك في الاستفسار عن الكورسات، الدبلومة، والمحتوى المتاح.")

# 6. الشريط الجانبي (Sidebar)
with st.sidebar:
    st.header("📌 معلومات سريعة")
    st.markdown("""
    **عن المعهد:**
    يقدم معهد المشورة دبلومات وكورسات متخصصة في المشورة النفسية، هندسة العلاقات، التربية، وإدارة المشاعر.
    
    ---
    
    **💡 أسئلة مقترحة للتجربة:**
    - إيه هي محاور كورس فهم أعمق للمراهقين؟
    - كلميني عن دبلومة المشورة الأساسية والترمات بتاعتها.
    - إزاي أقدر أتواصل مع المعهد أو أعرف المواعيد؟
    - إيه الكورسات المتاحة الخاصة بالتربية والاطفال؟
    """)
    
    st.divider()
    
    # زر إعادة إعادة المحادثة
    if st.button("🗑️ مسح المحادثة وبدء من جديد", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 7. عرض تاريخ المحادثة في الواجهة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 8. منطقة إدخال السؤال من العميل
user_query = st.chat_input(" اكتب استفسارك هنا...")

if user_query:
    # إضافة سؤال العميل للواجهة وللـ State
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)

    # تحضير الـ chat_history بالشكل المطلوب لـ LangGraph
    # نمرر المحادثات السابقة بدون السؤال الأخير
    formatted_history = [
        {"role": msg["role"], "content": msg["content"]} 
        for msg in st.session_state.messages[:-1]
    ]

    # بناء المدخلات الموجهة لـ workflow.py
    initial_input = {
        "user_query": user_query,
        "chat_history": formatted_history
    }

    # تشغيل الـ Workflow والحصول على الرد
    with st.chat_message("assistant"):
        with st.spinner("جاري مراجعة معلومات المعهد والرد عليك..."):
            try:
                # استدعاء الـ LangGraph المباشر
                result = workflow_app.invoke(initial_input)
                
                # استخراج الرد
                assistant_response = result.get("response") or "عذراً، لم أتمكن من إيجاد رد مناسب حالياً."
                
                # عرض الرد
                st.write(assistant_response)

                # حفظ رد السكرتيرة في الـ session state
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})

            except Exception as e:
                error_msg = "حدث خطأ أثناء معالجة الطلب. يرجى التأكد من مفاتيح الـ API وإعدادات النظام."
                st.error(error_msg)
                with st.expander("تفاصيل الخطأ"):
                    st.exception(e)