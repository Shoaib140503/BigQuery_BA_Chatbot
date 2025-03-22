import os
from pinecone import Pinecone

# Load API Key and Environment
api_key = os.getenv("PINECONE_API_KEY")

# Create Pinecone client instance
pc = Pinecone(api_key=api_key)

# Get index details
index_name = os.getenv("PINECONE_INDEX")
index = pc.Index(index_name)
index_stats = index.describe_index_stats()

print(f"Index Name: {index_name}")
print(f"Index Dimension: {index_stats['dimension']}")
