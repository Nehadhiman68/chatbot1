import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get Groq API key from environment
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=api_key)

# Page configuration
st.set_page_config(page_title="Chat with AI Chatbot 🤖", page_icon="💬", layout="centered")

# Sidebar with persona info
with st.sidebar:
    st.image("https://i.imgur.com/4M34hi2.png", width=120)  # Optional avatar
    st.markdown("### 🤖 Meet Your AI Chatbot")
    st.write(
        "Hello! I'm your AI-powered career assistant. I specialize in artificial intelligence "
        "and machine learning, and I'm here to help you explore exciting opportunities in tech. "
        "Ask me anything—I'm always ready to share insights with clarity and enthusiasm!"
    )
    st.markdown("---")
    st.write("💡 Tip: Ask about AI roles, required skills, future trends, or learning paths!")

# Main title
st.title("💼 Explore Careers in AI Technology with Your AI Chatbot")

# Input field
user_input = st.text_input("What would you like to know?", placeholder="e.g., What are the top AI roles in 2025?")

# Submit button
if st.button("Get Advice"):
    if user_input.strip():
        with st.spinner("Thinking..."):
            try:
                # Call Groq API with updated persona
                chat_completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": user_input
                        }
                    ]
                )

                response = chat_completion.choices[0].message.content

                # Display response in chat format
                st.success("AI Chatbot says:")
                st.markdown(f"🗨️ *{response}*")

            except Exception as e:
                st.error(f"Oops! Something went wrong: {e}")
    else:
        st.warning("Please enter a question before submitting.")

# Footer
st.markdown("---")
st.caption("Made with ❤️ by AI Chatbot (powered by Groq + Streamlit)")