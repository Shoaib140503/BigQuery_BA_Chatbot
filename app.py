import streamlit as st
from react_agent import execute_react_query
from utils import validate_query, format_response
from memory import get_chat_history, update_memory, clear_memory

# Streamlit UI Setup
st.set_page_config(page_title="Gemini-Powered BigQuery Chatbot", layout="wide")

# Initialize chat history from Pinecone
if "messages" not in st.session_state:
    st.session_state.messages = get_chat_history(user_query="")  # ✅ Fix: Provide a default empty query
    st.session_state.page = 0  # Initialize pagination index

# Header
st.title("Gemini-Powered BigQuery Chatbot 🤖")

# Pagination for Chat History
messages_per_page = 5
start_idx = st.session_state.page * messages_per_page
end_idx = start_idx + messages_per_page

# Display paginated chat history
for message in st.session_state.messages[start_idx:end_idx]:
    with st.chat_message("assistant" if "Bot:" in message else "user"):
        st.markdown(message)

# Pagination Controls
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Previous", disabled=st.session_state.page == 0):
        st.session_state.page -= 1
        st.rerun()
with col2:
    if st.button("Next ➡️", disabled=end_idx >= len(st.session_state.messages)):
        st.session_state.page += 1
        st.rerun()

# Input field
user_query = st.chat_input("Ask something about your BigQuery data...")

if user_query:
    # Store user message
    st.session_state.messages.append(f"User: {user_query}")

    # Validate SQL security
    if not validate_query(user_query):
        response = "⚠️ Unsafe query detected. Please refine your question."
    else:
        response = execute_react_query(user_query)

    # Format response
    formatted_response = format_response(response)

    # Display Assistant response
    with st.chat_message("assistant"):
        st.markdown(f"Bot: {formatted_response['response']}")

    # Store Assistant message
    st.session_state.messages.append(f"Bot: {formatted_response['response']}")
    update_memory(user_query, formatted_response['response'])  # Store in Pinecone

    # Keep only the last 20 messages
    st.session_state.messages = st.session_state.messages[-20:]

# Add a delete button to clear chat history
if st.button("🗑️ Clear Chat"):
    clear_memory()
    st.session_state.messages = []
    st.session_state.page = 0
    st.rerun()
