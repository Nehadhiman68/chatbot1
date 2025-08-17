import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import time
import json

# File to manage user authentication
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def create_user(username, password):
    users = load_users()
    if username in users:
        return False  # user exists
    users[username] = {"password": password}
    save_users(users)
    return True

def authenticate_user(username, password):
    users = load_users()
    return username in users and users[username]["password"] == password

#authentication pop up 

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "show_login" not in st.session_state:
    st.session_state.show_login = False


with st.sidebar:
# Check if the user is authenticated
# Toggle login
        if st.button("🔐 log In / Sign Up"):
            st.session_state.show_login = True

        # Simulated "modal"
        if st.session_state.show_login:
            with st.container():
                st.markdown("### 🔐 Login or Sign Up")
                username = st.text_input("Username", key="username_input")
                password = st.text_input("Password", type="password", key="password_input")
                action = st.radio("Action", ["login", "Sign Up"])

                if st.button("Submit"):
                    if action == "login":
                        if authenticate_user(username, password):
                            st.session_state.authenticated = True
                            st.session_state.username = username
                            st.success(f"Welcome back, {username}!")
                            st.session_state.show_login = False
                        else:
                            st.error("Invalid username or password.")
                    else:  # Sign Up
                        if create_user(username, password):
                            st.success("Account created! You can now log in.")
                        else:
                            st.warning("Username already exists.")

                if st.button("Cancel"):
                    st.session_state.show_login = False

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=api_key)

# Page Configuration
st.set_page_config(page_title="AI Career Chatbot 🤖", page_icon="💬", layout="centered")

# ---- Custom Styling ----
st.markdown("""
    <style>
        body {
            background-color: #f9f9f9;
        }
        .main {
            background-color: #ffffff;
            padding: 2rem;
            border-radius: 12px;
        }
        .title-style {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            color: #2c3e50;
        }
        .intro-card {
            background-color: #eef2f7;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            border-left: 5px solid #4b7bec;
        }
        .tip-box {
            background-color: #fef8e7;
            padding: 1rem;
            border-radius: 10px;
            border-left: 5px solid #f9ca24;
        }
    </style>
""", unsafe_allow_html=True)

# ---- Sidebar ----

# logout user
with st.sidebar:
    if st.session_state.authenticated:
        st.markdown(f"👤 Logged in as: `{st.session_state.username}`")
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.experimental_rerun()



with st.sidebar:
    st.image("https://i.imgur.com/4M34hi2.png", width=120)
    st.markdown("### 🤖 Meet Your AI Career Assistant")
    st.write(
        "Hi! I'm your intelligent assistant here to guide you into the world of Artificial Intelligence and Machine Learning careers. "
        "Whether you're just starting or looking to advance your skills, I'm here to help."
    )
    st.markdown("---")
    st.markdown("💡 **Try asking:**")
    st.markdown("- What skills do I need for an AI job?\n- Best courses for ML?\n- Trends in AI careers?")




# ---- Main Title ----
st.markdown('<div class="title-style">💼 Explore Careers in AI with Your Personal Chatbot</div>', unsafe_allow_html=True)

# ---- Introduction Card ----
# Typing effect for the introduction card
intro_text = (
    "👋 **Welcome!** This chatbot is here to help you explore, learn, and grow "
    "in the field of AI and ML. You can ask me about job roles, required skills, "
    "career paths, interview prep, or learning resources."
)

# Word-by-word animation
placeholder = st.empty()
animated_text = ""

for word in intro_text.split():
    animated_text += word + " "
    placeholder.markdown(
        f"""
        <div class="intro-card">{animated_text}</div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(0.15)  # Adjust speed here


# ---- Chat History Initialization ----
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hi there! 👋 I'm your AI chatbot. How can I assist you today?"}
    ]

# ---- Display Chat History ----
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- User Chat Input ----
user_input = st.chat_input("Ask me anything about AI careers...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Check for custom message
    lowered_input = user_input.lower()
    if any(kw in lowered_input for kw in ["who made you", "who built you", "your creator"]):
        bot_reply = (
            "👩‍💻 This AI chatbot was developed by **Neha Dhiman**, an MCA (2nd Year) student at "
            "Chaudhary Ranbir Singh University, Jind. It uses **Streamlit**, **Groq**, and the **LLaMA 3.3-70B Versatile** model "
            "to help you navigate career paths in Artificial Intelligence. 🚀"
        )
    else:
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.chat_history
                )
                bot_reply = response.choices[0].message.content
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                bot_reply = "Sorry, I couldn't process that due to an error."

    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

# ---- Reset Chat Button ----
if st.button("🔄 Reset Chat"):
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hi there! 👋 I'm your AI chatbot. How can I assist you today?"}
    ]
    st.rerun()

# ---- Footer ----
st.markdown("---")
st.caption("🧠 Powered by Groq + LLaMA 3 + Streamlit | Created with ❤️ by Neha Dhiman")
