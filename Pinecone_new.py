import os
from pinecone import Pinecone, ServerlessSpec

# Load API Key
api_key = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone client
pc = Pinecone(api_key=api_key)

# Create a new index with 768 dimensions
index_name = "business-analytics"
pc.create_index(
    name=index_name,
    dimension=768,  # ✅ Set to 768 dimensions
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-west-2")  # Adjust region if needed
)

print(f"New Pinecone index '{index_name}' created with 768 dimensions.")
