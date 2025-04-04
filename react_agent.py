from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from database import db
from config import GCP_PROJECT_ID #, GOOGLE_API_KEY
from metadata import FULL_METADATA, METRICS, COLUMN_MAPPINGS
from prompts import SYSTEM_INSTRUCTIONS, PROMPT_TEMPLATE
from persona_prompt import PERSONA_PROMPT  # Include Persona Prompt
from general_responses import handle_general_queries
from memory import get_chat_history, update_memory
from langchain_core.messages import HumanMessage

import vertexai
#from vertexai.generative_models import GenerativeModel, Part
from langchain_google_vertexai import VertexAI

# Initialize Gemini LLM
#llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-001", temperature=0.1, api_key=GOOGLE_API_KEY)

LOCATION = "us-central1"
# Initialize Vertex AI
#vertexai.init(project=GCP_PROJECT_ID, location=LOCATION)
#llm = GenerativeModel("gemini-2.0-flash-001")

llm = VertexAI(model_name="gemini-2.0-flash-001", project=GCP_PROJECT_ID, location=LOCATION)

# Instantiate toolkit for agent to access database
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# ReAct Agent with Memory and Persona Integration
react_agent = initialize_agent(
    llm=llm,
    tools=toolkit.get_tools(),
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def map_columns(user_query: str):
    """Maps user-friendly terms in the query to actual BigQuery column names."""
    for user_friendly, actual_column in COLUMN_MAPPINGS.items():
        user_query = user_query.lower().replace(user_friendly.lower(), actual_column)
    return user_query

def clean_sql_query(query: str) -> str:
    """Cleans the generated SQL query by removing markdown formatting and backticks."""
    query = query.strip()
    if query.startswith("```sql"):
        query = query[6:]  # Remove ```sql
    if query.startswith("```"):
        query = query[3:]  # Remove starting backticks
    if query.endswith("```"):
        query = query[:-3]  # Remove ending backticks
    return query.strip()

def generate_sql_query(user_query: str):
    """Dynamically generates a SQL query using LLM based on user input."""
    
    # ✅ Map user-friendly terms to actual column names
    mapped_query = map_columns(user_query)
    
    # ✅ Extract relevant columns based on metadata dictionary
    selected_columns = [
        f"SUM({col}) AS total_{col}" if col in METRICS else col
        for col in FULL_METADATA.keys() if col in mapped_query.lower()
    ]

    # ✅ Default selection if no specific column is mentioned
    if not selected_columns:
        selected_columns = ["*"]

    # ✅ Use PROMPT_TEMPLATE for structured query generation
    llm_prompt = PROMPT_TEMPLATE.format(metadata=FULL_METADATA, query=mapped_query)

    sql_query = llm.invoke([HumanMessage(content=llm_prompt)])  # ✅ Proper format
    
    # ✅ Clean the generated SQL query
    sql_query_cleaned = clean_sql_query(str(sql_query))

    return sql_query_cleaned

def execute_react_query(user_query: str):
    """Processes user query using persona-based reasoning and metadata."""

    # ✅ Check if the query is a general (non-SQL) question
    general_response = handle_general_queries(user_query)
    if general_response:
        return general_response  # ✅ Directly return a predefined response for general questions
    
    chat_history = get_chat_history()
    sql_query = generate_sql_query(user_query)
    
    # ✅ Now generate a response using Persona and System Instructions
    final_prompt = f"""
    {PERSONA_PROMPT}

    {SYSTEM_INSTRUCTIONS}

    ### **Chat History:**
    {chat_history}

    ### **User Query:** {user_query}

    ### **SQL Query:**
    {sql_query}

    Please generate only the final answer as a well-framed and complete sentence, including all key details necessary for clarity. Do NOT return just the SQL query. Instead, execute the query and provide the complete final answer in proper format.
    - First, generate a SQL query based on the user's question.  
    - Execute the query and retrieve the results.  
    - Format the final response as structured JSON.
    Also, If the user query doesn't provide enough information to generate a meaningful SQL query and if it seems like an incomplete or nonsensical query, then don't try to generate a SQL query for it instead printout- "provide full information to execute this"
    """

    # ✅ Let the AI format the response naturally
    response = react_agent.invoke(final_prompt, handle_parsing_errors=True)

    # ✅ Extract only the final answer
    if isinstance(response, dict) and 'output' in response:
        final_answer = response['output']  # ✅ Extract clean answer
    else:
        final_answer = response.strip()

    # ✅ Update memory and return only the output
    update_memory(user_query, final_answer)

    return final_answer  # ✅ Now it returns only the answer

    #done hai na bro