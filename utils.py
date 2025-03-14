def validate_query(query: str) -> bool:
    """Reject queries that could be unsafe (DROP, DELETE, etc.)."""
    blacklist = ["DROP", "DELETE", "TRUNCATE", "ALTER", "--", "xp_"]
    return not any(term in query.upper() for term in blacklist)

def format_response(data):
    """Format BigQuery results for better readability."""
    if isinstance(data, list):
        return {"data": data[:10]}  # Limit to 10 results
    return {"response": data}
