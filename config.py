import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google API Key for Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# BigQuery Project & Dataset
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
#LOCATION = os.getenv("LOCATION")

BIGQUERY_DATASET_ID = os.getenv("BIGQUERY_DATASET_ID")
BIGQUERY_TABLE_ID = os.getenv("BIGQUERY_TABLE_ID")  # Load table ID


# Construct BigQuery URI
BIGQUERY_URI = f"bigquery://{GCP_PROJECT_ID}/{BIGQUERY_DATASET_ID}"
BIGQUERY_TABLE_URI = f"{BIGQUERY_URI}.{BIGQUERY_TABLE_ID}"

# Pinecone API Credentials
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")