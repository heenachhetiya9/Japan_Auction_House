import streamlit as st
from agents.sql_agent import get_sql_agent
from datetime import datetime
from dotenv import load_dotenv
import os
# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="AI Chat Bot",
    page_icon="🤖",
    layout="wide"
)

# =========================
# CUSTOM CSS (DARK THEME)
# =========================
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0E1117;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161A23;
    border-right: 1px solid #2A2F3A;
}

/* Chat bubbles */
.user-message {
    background-color: #2B313E;
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 10px;
    margin-left: 30%;
    color: white;
    font-size: 16px;
}

.bot-message {
    background-color: #1E2530;
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 10px;
    margin-right: 30%;
    color: white;
    font-size: 16px;
}

/* Input box */
.stTextInput > div > div > input {
    background-color: #1E2530;
    color: white;
    border: 1px solid #3A4553;
}

/* Buttons */
.stButton button {
    background-color: #4F8BF9;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
}

.stButton button:hover {
    background-color: #3B6FD8;
    color: white;
}

/* Title */
.title {
    font-size: 42px;
    font-weight: bold;
    color: white;
    margin-bottom: 10px;
}

/* Subtitle */
.subtitle {
    color: #A0A0A0;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0

if "total_requests" not in st.session_state:
    st.session_state.total_requests = 0

# =========================
# SIDEBAR
# =========================
with st.sidebar:

    st.title("📊 Usage Metrics")

    st.metric("Total Chats", len(st.session_state.chat_history))
    st.metric("Successful Requests", st.session_state.total_requests)

    st.markdown("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

# =========================
# MAIN UI
# =========================
st.markdown('<div class="title">SQL 🛢 Database Chatbot</div>',
            unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">Ask questions about the SQL database and get answers!</div>',
    unsafe_allow_html=True
)

# =========================
# DISPLAY CHAT HISTORY
# =========================
for chat in st.session_state.chat_history:

    if chat["role"] == "user":
        st.markdown(
            f"""
            <div class="user-message">
                🧑 {chat["message"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f"""
            <div class="bot-message">
                🤖 {chat["message"]}
            </div>
            """,
            unsafe_allow_html=True
        )

# =========================
# USER INPUT
# =========================
user_question = st.chat_input("Ask your SQL question...")

# =========================
# PROCESS QUESTION
# =========================
if user_question:

    # Save user message
    st.session_state.chat_history.append({
        "role": "user",
        "message": user_question,
        "time": datetime.now().strftime("%H:%M")
    })

    # Display user instantly
    st.markdown(
        f"""
        <div class="user-message">
            🧑 {user_question}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Generate response
    with st.spinner("Thinking..."):

        try:
            agent = get_sql_agent()

            response = agent.run(user_question)

            # Save bot response
            st.session_state.chat_history.append({
                "role": "assistant",
                "message": response,
                "time": datetime.now().strftime("%H:%M")
            })

            st.session_state.total_requests += 1

            # Display bot response
            st.markdown(
                f"""
                <div class="bot-message">
                    🤖 {response}
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:

            error_message = f"Error: {str(e)}"

            st.session_state.chat_history.append({
                "role": "assistant",
                "message": error_message,
                "time": datetime.now().strftime("%H:%M")
            })

            st.error(error_message)