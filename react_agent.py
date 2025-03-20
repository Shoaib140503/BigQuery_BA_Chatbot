from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.tools import Tool
import sympy as sp  # Using SymPy for mathematical evaluations
from database import db
from config import GOOGLE_API_KEY
from metadata import DIMENSIONS, METRICS
from prompts import SYSTEM_INSTRUCTIONS, PROMPT_TEMPLATE
from persona_prompt import PERSONA_PROMPT  # Include Persona Prompt
from memory import get_chat_history, update_memory

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5, api_key=GOOGLE_API_KEY)

# SQL Agent Toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# SymPy-based Math Tool
def sympy_calculator(expression: str):
    """Safely evaluates mathematical expressions using SymPy."""
    try:
        return str(sp.sympify(expression).evalf())
    except Exception:
        return "Invalid mathematical expression."

math_tool = Tool(
    name="Calculator",
    func=sympy_calculator,
    description="Accurately evaluates mathematical expressions using SymPy."
)

# ReAct Agent with Memory and Persona Integration
react_agent = initialize_agent(
    llm=llm,
    tools=[toolkit, math_tool],
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def generate_sql_query(user_query: str):
    """Uses metadata to structure SQL query generation."""
    query_keywords = user_query.lower().split()
    selected_columns = []
    filters = []
    
    # Identify required columns
    for col in DIMENSIONS.keys():
        if col in query_keywords:
            selected_columns.append(col)

    for col in METRICS.keys():
        if col in query_keywords:
            selected_columns.append(f"SUM({col}) AS total_{col}")

    # Default selection
    if not selected_columns:
        selected_columns = ["*"]

    # Generate SQL Query using the prompt template
    query = PROMPT_TEMPLATE.format(query=user_query)
    
    return query

def execute_react_query(user_query: str):
    """Processes user query using persona-based reasoning and metadata."""
    chat_history = get_chat_history()
    sql_query = generate_sql_query(user_query)

    final_prompt = f"""
    {PERSONA_PROMPT}
    
    {SYSTEM_INSTRUCTIONS}

    ### **Chat History:**
    {chat_history}

    ### **User Query:** {user_query}

    ### **Generated SQL Query:**
    {sql_query}
    """
    
    response = react_agent.run(final_prompt)

    # Update memory with the latest conversation
    update_memory(user_query, response)

    return response
