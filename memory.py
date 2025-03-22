import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_pinecone import Pinecone as PineconeVectorStore

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

def update_memory(user_input, bot_response):
    """Stores chat history as embeddings in Pinecone."""
    text = f"User: {user_input}\nBot: {bot_response}"
    vector = embedding_model.embed_query(text)

    index.upsert(
        vectors=[{"id": user_input[:20], "values": vector, "metadata": {"chat": text}}]
    )

def get_chat_history(user_query: str = ""):
    """Retrieves the most relevant chat history from Pinecone using query embeddings."""
    if not user_query:
        return []  # ✅ Fix: Return empty list instead of throwing an error

    query_embedding = embedding_model.embed_query(user_query)
    results = index.query(vector=query_embedding, top_k=5, include_metadata=True)

    return [res["metadata"]["chat"] for res in results.get("matches", [])]  # ✅ Avoid KeyErrors

def clear_memory():
    """Deletes all chat history in Pinecone."""
    index_stats = index.describe_index_stats()
    
    if index_stats["total_vector_count"] > 0:
        index.delete(delete_all=True)
