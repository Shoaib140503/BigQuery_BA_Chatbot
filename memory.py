from langchain.memory import ConversationBufferMemory

# Initialize conversational memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

def update_memory(user_input, bot_response):
    """Stores chat history in memory."""
    memory.save_context({"input": user_input}, {"output": bot_response})

def get_chat_history():
    """Retrieves chat history for context-aware responses."""
    return memory.load_memory_variables({})["chat_history"]
