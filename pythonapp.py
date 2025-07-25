import streamlit as st
from gtts import gTTS
from io import BytesIO
from streamlit_drawable_canvas import st_canvas
import os
import re

# ---------- File Handling ----------
USER_FILE = "users.txt"

# Ensure the user file exists
if not os.path.exists(USER_FILE):
    open(USER_FILE, "w").close()

def load_users():
    with open(USER_FILE, "r") as f:
        lines = f.readlines()
    return {line.strip().split(",")[0]: line.strip().split(",")[1] for line in lines if "," in line}

def save_user(username, password):
    with open(USER_FILE, "a") as f:
        f.write(f"{username},{password}\n")

# ---------- Ensure Session State Keys Exist ----------
st.session_state.logged_in = st.session_state.get("logged_in", False)
st.session_state.username = st.session_state.get("username", "")

# ---------- Background Styling ----------
def set_background():
    bg_css = """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1503264116251-35a269479413");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    div[data-testid="stHeader"], div[class^="block-container"] {
        background-color: rgba(0, 0, 0, 0.6);
        padding: 2rem;
        border-radius: 12px;
        color: white;
        backdrop-filter: blur(8px);
    }
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

set_background()

# ---------- Login / Signup ----------
def login_signup():
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])

    with tab1:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            users = load_users()
            if username in users and users[username] == password:
                st.success(f"Welcome back, {username}!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password.")

    with tab2:
        st.subheader("Create an Account")
        new_user = st.text_input("New Username", key="signup_user")
        new_pass = st.text_input("New Password", type="password", key="signup_pass")
        if st.button("Sign Up"):
            users = load_users()
            if new_user in users:
                st.warning("Username already exists.")
            elif new_user == "" or new_pass == "":
                st.warning("Please fill in both fields.")
            else:
                save_user(new_user, new_pass)
                st.success("Account created! You can now log in.")

# ---------- Even / Odd Page ----------
def even_odd_page():
    st.title(f"Welcome {st.session_state.username}! Let's Play Even or Odd 🎉")

    name = st.text_input("🧒 What's your name?")
    num_input = st.text_input("🎲 Type any number (as long as you want):")

    languages = {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "Chinese": "zh-cn",
        "Italian": "it"
    }
    selected_lang = st.selectbox("🌍 Choose a language:", list(languages.keys()))

    # --- Validation ---
    num = None
    if num_input:
        if re.fullmatch(r"-?\d+", num_input.strip()):
            num = int(num_input.strip())
        else:
            st.error("Please enter a valid number (digits only).")

    valid_name = True
    if name:
        if not re.fullmatch(r"[a-zA-Z\s'-]+", name):
            st.error("Please enter a valid name (letters only).")
            valid_name = False

    # --- Result Display ---
    if valid_name and num is not None and selected_lang:
        is_even = num % 2 == 0
        result_en = "even" if is_even else "odd 😎"

        translated_texts = {
            "English": f"{name}, {num} is an {result_en} number.",
            "Spanish": f"{name}, {num} es un número {'par' if is_even else 'impar 😎'}.",
            "French": f"{name}, {num} est un nombre {'pair' if is_even else 'impair 😎'}.",
            "Chinese": f"{name}，{num} 是一个{'偶数' if is_even else '奇数 😎'}。",
            "Italian": f"{name}, {num} è un numero {'pari' if is_even else 'dispari 😎'}."
        }

        translated_message = translated_texts[selected_lang]

        st.markdown(f"### 🗣️ In {selected_lang}:")
        st.markdown(f"**{translated_message}**")

        # Voice output
        tts = gTTS(text=translated_message, lang=languages[selected_lang])
        audio_fp = BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        st.audio(audio_fp, format='audio/mp3')

    st.markdown("---")
    st.subheader("🎨 Draw Anything You Like!")

    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=4,
        stroke_color="#000000",
        background_color="#ffffff",
        height=300,
        drawing_mode="freedraw",
        key="canvas"
    )

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

# ---------- Main ----------
if st.session_state.logged_in:
    even_odd_page()
else:
    login_signup()
