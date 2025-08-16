import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=api_key)

# Page config
st.set_page_config(page_title="Chat with AI Chatbot 🤖", page_icon="💬", layout="centered")

# Sidebar
with st.sidebar:
    st.image("https://i.imgur.com/4M34hi2.png", width=120)
    st.markdown("### 🤖 Meet Your AI Chatbot")
    st.write(
        "Hello! I'm your AI-powered career assistant. I specialize in artificial intelligence "
        "and machine learning, and I'm here to help you explore exciting opportunities in tech. "
        "Ask me anything—I'm always ready to share insights with clarity and enthusiasm!"
    )
    st.markdown("---")
    st.write("💡 Tip: Ask about AI roles, required skills, future trends, or learning paths!")

# Title
st.title("💼 Explore Careers in AI Technology with Your AI Chatbot")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hii !! This is your AI chatbot. How can I assist you today?"}
    ]

# Display full chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input field
user_input = st.chat_input("Ask me anything about AI careers...")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get AI response
    # Check for custom query before calling Groq API
    lowered_input = user_input.lower()

    if any(kw in lowered_input for kw in ["who made you", "who built you", "who created you", "your creator"]):
        bot_reply = "This AI chatbot is developed by ** Neha Dhiman **.😊. She is a student of MCA(2nd year) at Chaudhary Ranbir Singh University,JInd " \
                "and it leverages datasets and foundational technologies from Meta AI." \
                "It is designed to assist users in exploring AI career opportunities using streamlit , Groq, and Llama 3.3-70B Versatile model." \
                "It helps you find relevant resources, understand job requirements, and navigate your career path in AI."
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



            # Add AI response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)


# Optional reset chat button
if st.button("🔄 Reset Chat"):
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hii !! This is your AI chatbot. How can I assist you today?"}
    ]
    st.rerun()

# Footer
st.markdown("---")
st.caption("Made with ❤️ by AI Chatbot (powered by Groq + Streamlit)")
