import os
import streamlit as st

# 1. إعداد الصفحة
st.set_page_config(
    page_title="مساعد معهد المشورة - خدمة العملاء",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. تحميل كل المتغيرات مباشرة في os.environ فوراً
def load_all_secrets():
    # نقل كل Secrets الموجودة في Streamlit لـ os.environ بشكل عام
    if hasattr(st, "secrets"):
        for key, value in st.secrets.items():
            os.environ[str(key)] = str(value)

load_all_secrets()

# 3. استيراد الـ Workflow بعد التأكد من تسجيل os.environ
try:
    from workflow import app as workflow_app
except Exception as e:
    st.error("تعذر تحميل نظام المساعد الذكي (workflow.py). يرجى التأكد من المجلد والملفات.")
    st.exception(e)
    st.stop()

# 4. تهيئة حالة الجلسة (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 5. واجهة المعهد الرئيسية
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
    
    if st.button("🗑️ مسح المحادثة وبدء من جديد", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 7. عرض تاريخ المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 8. منطقة الإدخال والتشغيل
user_query = st.chat_input("اكتب استفسارك هنا...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.write(user_query)

    formatted_history = [
        {"role": msg["role"], "content": msg["content"]} 
        for msg in st.session_state.messages[:-1]
    ]

    initial_input = {
        "user_query": user_query,
        "chat_history": formatted_history
    }

    with st.chat_message("assistant"):
        with st.spinner("جاري مراجعة معلومات المعهد والرد عليك..."):
            try:
                result = workflow_app.invoke(initial_input)
                assistant_response = result.get("response") or "عذراً، لم أتمكن من إيجاد رد مناسب حالياً."
                st.write(assistant_response)
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})

            except Exception as e:
                error_msg = "حدث خطأ أثناء معالجة الطلب. يرجى التأكد من مفاتيح الـ API وإعدادات النظام."
                st.error(error_msg)
                with st.expander("تفاصيل الخطأ"):
                    st.exception(e)