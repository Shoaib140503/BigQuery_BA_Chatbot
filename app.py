import streamlit as st
from agent import execute_query
from utils import validate_query, format_response

# Streamlit UI Setup
st.set_page_config(page_title="Gemini-Powered BigQuery Chatbot", layout="wide")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Header
st.title("Gemini-Powered BigQuery Chatbot 🤖")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field
user_query = st.chat_input("Ask something about your BigQuery data...")

if user_query:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Validate SQL security
    if not validate_query(user_query):
        response = "⚠️ Unsafe query detected. Please refine your question."
    else:
        response = execute_query(user_query)

    # Format response
    formatted_response = format_response(response)

    # Display Assistant response
    with st.chat_message("assistant"):
        st.markdown(formatted_response["response"])

    # Store Assistant message
    st.session_state.messages.append({"role": "assistant", "content": formatted_response["response"]})

    # Keep only the last 20 messages
    st.session_state.messages = st.session_state.messages[-20:]

# Add a delete button to clear chat history
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()
