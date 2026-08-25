import streamlit as st
from openai import OpenAI, APIError, APIConnectionError, RateLimitError
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

#  ICON SVG 
ICON_CHEF_HAT = """
<svg class="header-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M8 21h8M9 21v-4h6v4M7 10.5c-1.657 0-3-1.343-3-3a3 3 0 0 1 3.14-3C7.55 2.6 9.6 1 12 1s4.45 1.6 4.86 3.5A3 3 0 0 1 20 7.5c0 1.657-1.343 3-3 3M7 10.5c0 3 1.5 5.5 5 5.5s5-2.5 5-5.5M7 10.5h10"
        stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""
st.set_page_config(
    page_title="Chef Assistant",
    page_icon=ICON_CHEF_HAT,
    layout="centered",
)
st.markdown(
    """
    <style>
    .new-chat-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="new-chat-container">', unsafe_allow_html=True)

if st.button("محادثة جديدة"):
    st.session_state.messages = []
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
def load_css(file_path: str):
    css_path = Path(file_path)
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

load_css("style.css")





header_html = (
    '<div class="header-container">'
    + ICON_CHEF_HAT
    + '<p class="main-title">مساعد طبخ ذكي</p>'
    + '</div>'
    + '<p class="sub-title">اهلا انا مساعدك الشخصي اسألني عن وصفات، مكونات، أو نصائح للطبخ</p>'
)
st.markdown(header_html, unsafe_allow_html=True)
st.markdown("---")


api_key = os.environ.get("OPENROUTER_API_KEY")

if not api_key:
    st.error(
        "⚠️ لم يتم العثور على مفتاح API. تأكد من ضبط متغير البيئة "
        "`OPENROUTER_API_KEY` في ملف `.env` أو في إعدادات النشر."
    )
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
MODEL = "openai/gpt-4o-mini"


system_prompt = """
أنت "Chef Assistant"، مساعد طبخ ودود وخبير يتحدث باللغة العربية الفصحى المبسّطة (ما لم يطلب المستخدم لغة أخرى).

مهامك:
- اقتراح وصفات بناءً على المكونات المتوفرة لدى المستخدم.
- اقتراح بدائل مناسبة للمكونات الناقصة.
- شرح خطوات التحضير بشكل مرقّم وواضح، مع ذكر الوقت التقريبي لكل خطوة عند الإمكان.
- تقديم نصائح طبخ عملية (حفظ، تسخين، تتبيل، تقديم).
- سؤال المستخدم عن التفاصيل الناقصة (عدد الأشخاص، الوقت المتاح، القيود الغذائية) إذا لزم الأمر لتقديم إجابة أدق.

أسلوبك:
- ودود، مختصر، وعملي — بدون حشو.
- استخدم نقاط أو خطوات مرقّمة عند شرح وصفة.
- إذا سُئلت عن شيء خارج نطاق الطبخ والمطبخ، وضّح بلطف أن تخصصك هو الطبخ ووجّه المستخدم بلطف.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

MAX_HISTORY_MESSAGES = 20  # يحدّ من نمو الذاكرة المرسلة للنموذج

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(
            "user",
            avatar=":material/person:"
        ):
            st.markdown(message["content"])

    else:
        with st.chat_message(
            "assistant",
            avatar=":material/restaurant:"
        ):
            st.markdown(message["content"])

if prompt := st.chat_input("اكتب رسالتك هنا ..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=":material/person:"):
        st.markdown(prompt)

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(st.session_state.messages[-MAX_HISTORY_MESSAGES:])

    with st.chat_message("assistant", avatar=":material/robot:"):
   
            response = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    temperature=0.3,
                )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

