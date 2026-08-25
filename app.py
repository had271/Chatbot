import streamlit as st
from openai import OpenAI
import os 
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
MODEL = "openai/gpt-4o-mini"
st.title("Chef assistant")
#  CSS style
st.markdown(
    """
    <style>
    .stApp {
        background-color: #eafaf1;
    }
    .main-title {
        text-align: center;
        color: #1b5e20;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #388e3c;
        font-size: 18px;
        margin-bottom: 25px;
    }
    section[data-testid="stSidebar"] {
        background-color: #d7f2dc;
    }
    .stChatMessage {
        border-radius: 15px;
        padding: 8px;
    }
    button[kind="primary"] {
        background-color: #4caf50 !important;
        border-radius: 10px !important;
    }
    .stChatInputContainer {
        border: 1px solid #a5d6a7;
        border-radius: 12px;
    }
    hr {
        border: 1px solid #a5d6a7;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

system_prompt = """
"""

# Accept user input
if prompt := st.chat_input("اكتب رسالتك هنا ..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message
    with st.chat_message("user"):
      st.markdown(prompt)
    # Create messages for API
    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]
    messages.extend(st.session_state.messages)
    
    # Generate response
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.3
        )
        answer = response.choices[0].message.content
        st.markdown(answer)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
