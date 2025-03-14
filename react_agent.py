from langchain_google_genai import ChatGoogleGenerativeAI # type: ignore
from langchain.agents import initialize_agent, AgentType
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from database import db
from config import GOOGLE_API_KEY
from persona_prompt import PERSONA_PROMPT
from prompts import SYSTEM_INSTRUCTIONS
from memory import get_chat_history, update_memory

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5, api_key=GOOGLE_API_KEY)

# SQL Agent Toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# ReAct Agent with Memory
react_agent = initialize_agent(
    llm=llm,
    tools=[toolkit],
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Function to Run Queries with Conversational Memory
def execute_react_query(user_query: str):
    """Processes user query with memory for context-aware responses."""
    chat_history = get_chat_history()
    prompt = f"{PERSONA_PROMPT}\n\n{SYSTEM_INSTRUCTIONS}\n\n### **Chat History:**\n{chat_history}\n\n### **User Query:** {user_query}"
    
    response = react_agent.run(prompt)

    # Update memory with the latest conversation
    update_memory(user_query, response)

    return response
