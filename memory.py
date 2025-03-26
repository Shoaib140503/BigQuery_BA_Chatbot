import os
import hashlib
import json
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_pinecone import Pinecone as PineconeVectorStore
import pinecone 

# Load environment variables
load_dotenv()

# Initialize Pinecone client
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Define Pinecone index
index_name = os.getenv("PINECONE_INDEX", "chat-history")

# Check if the index exists
existing_indexes = [i.name for i in pc.list_indexes()]
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-west-2")
    )

# Connect to the index
index = pc.Index(index_name)

# Initialize Vertex AI Embeddings
embedding_model = VertexAIEmbeddings(model_name="textembedding-gecko-multilingual")

def generate_unique_id(text: str):
    """Generate a unique ID using a hash function to prevent duplicates."""
    return hashlib.md5(text.encode()).hexdigest()

def update_memory(user_input, bot_response):
    """Stores chat history in Pinecone with a max limit of 20 messages."""
    text = f"User: {user_input}\nBot: {bot_response}"
    vector = embedding_model.embed_query(text)

    unique_id = generate_unique_id(text)  # Use a unique hash for storage

    # Store new chat entry
    index.upsert(
        vectors=[{"id": unique_id, "values": vector, "metadata": {"chat": text}}]
    )

    # Fetch latest 20 chat messages
    chat_history = get_chat_history()
    if len(chat_history) > 20:
        # Delete the oldest chat from Pinecone
        oldest_chat_id = generate_unique_id(chat_history[0])
        index.delete(ids=[oldest_chat_id])

def get_chat_history():
    """Retrieves the last 20 chat history entries from Pinecone."""
    results = index.query(vector=[0.0] * 768, top_k=20, include_metadata=True)

    history = [res["metadata"]["chat"] for res in results.get("matches", [])]

    return history if history else ["No previous chat history found."]

def clear_memory():
    """Deletes all chat history in Pinecone and handles empty namespace errors."""
    try:
        index.delete(delete_all=True, namespace="")
        return "✅ Chat history cleared successfully."
    except pinecone.exceptions.PineconeException as e:
        if "Namespace not found" in str(e):
            return "⚠️ No previous chat present to clear."
        else:
            return f"🚨 Error clearing chat: {e}"