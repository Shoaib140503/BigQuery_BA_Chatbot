from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain_experimental.sql import SQLDatabaseChain 
from langchain.tools import Tool
import sympy as sp 
from database import db
from config import GOOGLE_API_KEY
from metadata import DIMENSIONS, METRICS
from prompts import SYSTEM_INSTRUCTIONS, PROMPT_TEMPLATE
from persona_prompt import PERSONA_PROMPT  # Include Persona Prompt
from memory import get_chat_history, update_memory

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2, api_key=GOOGLE_API_KEY)

# SQL Database Chain (Replaces SQLDatabaseToolkit)
sql_chain = SQLDatabaseChain.from_llm(llm, db)

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
    tools=[math_tool],  # ✅ Removed deprecated SQLDatabaseToolkit
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def generate_sql_query(user_query: str):
    """Dynamically generates a SQL query using LLM based on user input."""

    table_name = "`windy-skyline-453612-q2.data_for_testing.shopify_sales`"
    
    # ✅ Extract relevant columns from metadata
    selected_columns = []
    
    for col in DIMENSIONS.keys():
        if col in user_query.lower():
            selected_columns.append(col)

    for col in METRICS.keys():
        if col in user_query.lower():
            selected_columns.append(f"SUM({col}) AS total_{col}")

    # ✅ Default selection if no specific column is mentioned
    if not selected_columns:
        selected_columns = ["*"]

    # ✅ Prompt LLM to generate SQL query dynamically
    llm_prompt = f"""
    You are an expert in SQL and BigQuery. Based on the user's question, generate an optimized SQL query.
    - Use {table_name} as the table.
    - Select only the necessary columns.
    - Use WHERE conditions when applicable.
    - Apply GROUP BY, ORDER BY, or LIMIT as needed.
    - Do not add explanations—only output the raw SQL query.

    ### User Query:
    "{user_query}"

    ### SQL Query:
    """
    
    sql_query = llm(llm_prompt)  # Use Gemini LLM to generate the SQL query dynamically

    return sql_query.strip()  # ✅ Ensures clean output


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

    # ✅ Execute SQL query separately using SQLDatabaseChain
    sql_result = sql_chain.invoke(sql_query)  

    response = react_agent.run(final_prompt)

    # Update memory with the latest conversation
    update_memory(user_query, response)

    return f"{response}\n\n**SQL Result:**\n{sql_result}"