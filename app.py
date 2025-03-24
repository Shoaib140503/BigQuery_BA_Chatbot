import streamlit as st
from react_agent import execute_react_query
from utils import validate_query, format_response
from memory import get_chat_history, update_memory, clear_memory

# Streamlit UI Setup
st.set_page_config(page_title="Gemini-Powered BigQuery Chatbot", layout="wide")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = get_chat_history(user_query="")
    st.session_state.page = 0

# Header
st.title("Gemini-Powered BigQuery Chatbot 🤖")

# Pagination for Chat History
messages_per_page = 5
start_idx = st.session_state.page * messages_per_page
end_idx = start_idx + messages_per_page

# ✅ Display chat history safely
for message in st.session_state.messages[start_idx:end_idx]:
    if ": " in message:
        role, content = message.split(": ", 1)
    else:
        role, content = "assistant", message  # Default role if formatting fails

    with st.chat_message("assistant" if role == "Bot" else "user"):
        st.markdown(content)

# ✅ Pagination Controls
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Previous", disabled=st.session_state.page == 0):
        st.session_state.page -= 1
        st.rerun()
with col2:
    if st.button("Next ➡️", disabled=end_idx >= len(st.session_state.messages)):
        st.session_state.page += 1
        st.rerun()

# ✅ User Input Field
user_query = st.chat_input("Ask something about your BigQuery data...")

if user_query:
    # ✅ Display user message before processing
    with st.chat_message("user"):
        st.markdown(user_query)

    st.session_state.messages.append(f"User: {user_query}")

    # ✅ Validate query security
    if not validate_query(user_query):
        response = "⚠️ Unsafe query detected. Please refine your question."
    else:
        response = execute_react_query(user_query)

    # ✅ Format and display bot response
    formatted_response = format_response(response)

    with st.chat_message("assistant"):
        st.markdown(formatted_response["response"])

    # ✅ Store chat in history
    st.session_state.messages.append(f"Bot: {formatted_response['response']}")
    update_memory(user_query, formatted_response["response"])

    # ✅ Keep only the last 20 messages
    st.session_state.messages = st.session_state.messages[-20:]

# ✅ Add "Clear Chat" Button
if st.button("🗑️ Clear Chat"):
    clear_memory()
    st.session_state.messages = []
    st.session_state.page = 0
    st.rerun()
