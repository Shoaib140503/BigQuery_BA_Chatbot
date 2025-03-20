import pinecone
import os
from langchain.embeddings import VertexAIEmbeddings  # Using Vertex AI for embeddings
from langchain.vectorstores import Pinecone
from langchain.schema import Document
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Pinecone
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_ENV"))

# Define Pinecone index
index_name = os.getenv("PINECONE_INDEX", "chat-history")
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=768)  # Adjusted for Vertex AI embeddings

index = pinecone.Index(index_name)
embedding_model = VertexAIEmbeddings()  # Using Vertex AI embeddings

def update_memory(user_input, bot_response):
    """Stores chat history as embeddings in Pinecone."""
    text = f"User: {user_input}\nBot: {bot_response}"
    vector = embedding_model.embed_query(text)
    index.upsert([(user_input[:20], vector, {"chat": text})])

def get_chat_history(user_query: str):
    """Retrieves the most relevant chat history from Pinecone using query embeddings."""
    if not user_query:
        return []  # Return empty if no query provided

    # Convert user query into an embedding using Vertex AI
    query_embedding = embedding_model.embed_query(user_query)

    # Retrieve top 5 most relevant past conversations
    results = index.query(vector=query_embedding, top_k=5, include_metadata=True)

    return [res["metadata"]["chat"] for res in results["matches"]] if results["matches"] else []

def clear_memory():
    """Deletes chat history in Pinecone."""
    index.delete(delete_all=True)