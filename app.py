import streamlit as st
from react_agent import execute_react_query
from utils import validate_query, format_response
from memory import get_chat_history, update_memory, clear_memory

# Streamlit UI Setup
st.set_page_config(page_title="Gemini-Powered BigQuery Chatbot", layout="wide")

# ✅ Load last 20 chats from Pinecone on startup
if "messages" not in st.session_state:
    st.session_state.messages = get_chat_history()

# Header
st.title("Gemini-Powered BigQuery Chatbot 🤖")

# ✅ Display previous chat history
for message in st.session_state.messages:
    role, content = message.split(": ", 1) if ": " in message else ("assistant", message)
    with st.chat_message("assistant" if role == "Bot" else "user"):
        st.markdown(content)

# ✅ User Input Field
user_query = st.chat_input("Ask something about your BigQuery data...")

if user_query:
    with st.chat_message("user"):
        st.markdown(user_query)

    st.session_state.messages.append(f"User: {user_query}")

    if not validate_query(user_query):
        response = "⚠️ Unsafe query detected. Please refine your question."
    else:
        response = execute_react_query(user_query)

    formatted_response = format_response(response)

    with st.chat_message("assistant"):
        st.markdown(formatted_response["response"])

    st.session_state.messages.append(f"Bot: {formatted_response['response']}")
    update_memory(user_query, formatted_response["response"])

    # ✅ Keep only the last 20 messages
    st.session_state.messages = st.session_state.messages[-20:]

# ✅ Add "Clear Chat" Button
if st.button("🗑️ Clear Chat"):
    clear_memory()
    st.session_state.messages = []
    st.rerun()
