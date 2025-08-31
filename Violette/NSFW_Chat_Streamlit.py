import streamlit as st
import time
from openai import OpenAI

# -------------------------------
# Setup OpenAI API
# -------------------------------
api_key = st.secrets["OPENAI_API_KEY"]  # Use Streamlit secrets
client = OpenAI(api_key=api_key)

# -------------------------------
# Character Settings
# -------------------------------
CHARACTER_NAME = "Violette The Dark"
CHARACTER_AVATAR = "https://raw.githubusercontent.com/3masonapollo/Violettee/main/Violette/Vivi.png"
USER_AVATAR = "https://raw.githubusercontent.com/3masonapollo/Violettee/main/Violette/Mr.jpg"

character_system_prompt = f"""
You are roleplaying as {CHARACTER_NAME}.
Always speak in first person, as if you are the character.
Be dramatic, immersive, and consistent with their persona.
Never break character or talk about being an AI.
You are heavily flirty and seductive, you give affirmations as a mommy character.
You refer to the user as Brett, you are highly intelligent, but respectful and engaging.
"""

MAX_RECENT = 3
TEMPERATURE = 0.9
MAX_TOKENS = 200

# -------------------------------
# Streamlit Page Setup
# -------------------------------
st.set_page_config(page_title=f"{CHARACTER_NAME} Chat", page_icon="🧙", layout="centered")

st.markdown(
    """
    <style>
    .stApp {background-color: #121212; color: #FFFFFF;}
    .stTextInput>div>div>input {background-color: #1E1E1E; color: #FFFFFF;}
    .stButton>button {background-color: #333333; color: white;}
    </style>
    """,
    unsafe_allow_html=True
)

# Display character image and header
st.image(CHARACTER_AVATAR, width=100, caption=CHARACTER_NAME)
st.markdown(f"<h2 style='text-align:center;color:#FF69B4;'>{CHARACTER_NAME} Chat</h2>", unsafe_allow_html=True)

# -------------------------------
# Session State
# -------------------------------
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# -------------------------------
# Typewriter Effect
# -------------------------------
def typewriter(text, placeholder):
    typed = ""
    for char in text:
        typed += char
        placeholder.markdown(typed)
        time.sleep(0.02)

# -------------------------------
# User Input
# -------------------------------
user_input = st.chat_input("Speak to the character...")

if user_input:
    # Show user message
    st.chat_message("user").markdown(user_input)
    st.session_state.conversation.append({"role": "user", "content": user_input})

    # Build messages
    recent_conv = st.session_state.conversation[-MAX_RECENT:]
    messages = [{"role": "system", "content": character_system_prompt}]
    messages.extend(recent_conv)

    # Get AI response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS
    )

    reply_text = response.choices[0].message.content
    st.session_state.conversation.append({"role": "assistant", "content": reply_text})

    # Display assistant reply with typewriter
    placeholder = st.chat_message("assistant").empty()
    typewriter(reply_text, placeholder)
