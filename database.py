import logging
import time
from langchain_community.utilities import SQLDatabase
from config import BIGQUERY_URI

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def connect_to_bigquery(retries=3, delay=2):
    """Attempts to establish a connection to BigQuery with exponential backoff."""
    for attempt in range(retries):
        try:
            db = SQLDatabase.from_uri(BIGQUERY_URI)
            logging.info("✅ Successfully connected to BigQuery database.")
            return db
        except Exception as e:
            logging.error(f"❌ BigQuery connection failed (Attempt {attempt+1}/{retries}): {e}")
            time.sleep(delay * (2 ** attempt))  # Exponential backoff
    logging.error("🚨 Maximum retries reached. Could not connect to BigQuery.")
    return None

# Establish connection to BigQuery
db = connect_to_bigquery()