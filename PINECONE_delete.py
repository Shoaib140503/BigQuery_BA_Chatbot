import os
from pinecone import Pinecone

# Load Pinecone API Key
api_key = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone client
pc = Pinecone(api_key=api_key)

# Delete old index
index_name = "business-analytics"
pc.delete_index(index_name)

print(f"Deleted index: {index_name}")