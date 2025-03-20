from google.cloud import bigquery
import os

# Load credentials (Ensure that GOOGLE_APPLICATION_CREDENTIALS is set)
if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
    print("ERROR: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set.")
    print("Set it using: export GOOGLE_APPLICATION_CREDENTIALS='/path/to/your-service-account.json'")
    exit()

# Set Project ID and Dataset
PROJECT_ID = "your-gcp-project-id"
DATASET_ID = "your-dataset-id"
TABLE_NAME = "your-table-name"

# Initialize BigQuery Client
try:
    client = bigquery.Client(project=PROJECT_ID)
    print("Successfully connected to BigQuery!")
except Exception as e:
    print(f"ERROR: Could not connect to BigQuery.\n{e}")
    exit()

# Test Query: Fetch 5 sample rows from the table
query = f"""
SELECT * 
FROM `{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}`
LIMIT 5;
"""

try:
    query_job = client.query(query)  # Run query
    results = query_job.result()  # Get results
    
    print("Successfully fetched data! Here are the first 5 rows:")
    for row in results:
        print(dict(row))  # Print row as a dictionary

except Exception as e:
    print(f"ERROR: Could not fetch data from BigQuery.\n{e}")