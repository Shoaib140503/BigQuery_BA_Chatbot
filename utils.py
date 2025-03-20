import re

def validate_query(query: str) -> bool:
    """Reject queries that could be unsafe (DROP, DELETE, etc.)."""
    blacklist = ["DROP", "DELETE", "TRUNCATE", "ALTER", "--", "xp_", "UNION", "INSERT", "UPDATE"]
    
    # Check for dangerous keywords
    if any(term in query.upper() for term in blacklist):
        return False

    # Prevent nested queries (subqueries within parentheses)
    if re.search(r"\(\s*SELECT", query, re.IGNORECASE):
        return False
    
    return True

def format_response(data):
    """Format BigQuery results for better readability and structure."""
    if isinstance(data, list):
        return {
            "status": "success",
            "message": "Query executed successfully.",
            "data": data[:10]  # Limit to 10 results
        }
    return {
        "status": "success",
        "message": "Query executed successfully.",
        "response": data
    }
