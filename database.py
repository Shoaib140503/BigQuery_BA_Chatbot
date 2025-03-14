from langchain_community.utilities import SQLDatabase
from config import BIGQUERY_URI

# Establish connection to BigQuery
db = SQLDatabase.from_uri(BIGQUERY_URI)
