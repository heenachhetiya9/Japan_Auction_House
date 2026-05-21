from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
# from langchain.agents.agent_types import AgentType

from database.db_connection import engine

def get_sql_agent():

    db = SQLDatabase(engine)

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        ZERO_SHOT_REACT_DESCRIPTION = 'zero-shot-react-description',
        verbose=True
    )

    return agent_executor