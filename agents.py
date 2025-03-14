from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.tools import Tool
import sympy as sp  # Using SymPy instead of LLMMathChain
from database import db
from prompts import SYSTEM_INSTRUCTIONS, PROMPT_TEMPLATE
from config import GOOGLE_API_KEY

# Gemini LLM Setup
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5, api_key=GOOGLE_API_KEY)

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

# SQL Agent Toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Function to Run Queries
def execute_query(user_query: str):
    formatted_prompt = PROMPT_TEMPLATE.format(query=user_query)
    return llm.invoke(formatted_prompt)
