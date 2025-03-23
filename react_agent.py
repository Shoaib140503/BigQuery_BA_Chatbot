from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain_experimental.sql import SQLDatabaseChain 
from langchain.tools import Tool
import sympy as sp 
from database import db
from config import GOOGLE_API_KEY
from metadata import FULL_METADATA, METRICS
from prompts import SYSTEM_INSTRUCTIONS, PROMPT_TEMPLATE
from persona_prompt import PERSONA_PROMPT  # Include Persona Prompt
from memory import get_chat_history, update_memory
from langchain_core.messages import HumanMessage

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
    
    # ✅ Extract relevant columns based on metadata dictionary
    selected_columns = [
        f"SUM({col}) AS total_{col}" if col in METRICS else col
        for col in FULL_METADATA.keys() if col in user_query.lower()
    ]

    # ✅ Default selection if no specific column is mentioned
    if not selected_columns:
        selected_columns = ["*"]

    # ✅ Use PROMPT_TEMPLATE for structured query generation
    llm_prompt = PROMPT_TEMPLATE.format(query=user_query)

    sql_query = llm.invoke([HumanMessage(content=llm_prompt)])  # ✅ Proper format

    return sql_query.content.strip() 

def execute_react_query(user_query: str):
    """Processes user query using persona-based reasoning and metadata."""
    chat_history = get_chat_history()
    sql_query = generate_sql_query(user_query)

    # ✅ Execute SQL query first to get the actual result
    sql_result = sql_chain.invoke(sql_query)

    # Extract SQL execution output
    if isinstance(sql_result, dict) and 'result' in sql_result:
        sql_answer = sql_result['result']
    else:
        sql_answer = "I couldn't retrieve the data. Please check the query."

    # ✅ Now generate a response using Persona and System Instructions
    final_prompt = f"""
    {PERSONA_PROMPT}
    
    {SYSTEM_INSTRUCTIONS}

    ### **Chat History:**
    {chat_history}

    ### **User Query:** {user_query}

    ### **SQL Result:**
    {sql_answer}

    Please generate a clear and structured response.
    """

    # ✅ Let the AI format the response naturally
    response = react_agent.run(final_prompt)

    # ✅ Update memory and return the final response
    update_memory(user_query, response)

    return response

