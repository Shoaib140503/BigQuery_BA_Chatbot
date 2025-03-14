from react_agent import execute_react_query
from persona_prompt import PERSONA_PROMPT

def execute_query_with_persona(user_query: str):
    """Combines persona-based reasoning with ReAct agent execution."""
    final_prompt = f"{PERSONA_PROMPT}\n\nUser Query: {user_query}"
    return execute_react_query(final_prompt)
