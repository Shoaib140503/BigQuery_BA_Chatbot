import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google API Key for Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# BigQuery Project & Dataset
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
BIGQUERY_DATASET_ID = os.getenv("BIGQUERY_DATASET_ID")
BIGQUERY_URI = f"bigquery://{GCP_PROJECT_ID}/{BIGQUERY_DATASET_ID}"