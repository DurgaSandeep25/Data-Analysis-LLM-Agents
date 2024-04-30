import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI

from pandas_prompt import get_pandas_prompt
# append the path to retrieve open ai credentials
import sys
sys.path.append("../")
from openai_creds import get_key, get_url

# import OpenAI model - remember to provide your OpenAI credentials
llm = ChatOpenAI(
    model="gpt-3.5-turbo", 
    temperature=0, 
    api_key=get_key(), 
    base_url= get_url()
    )
    

def execute_query(question: str, query: str) -> str:
    
    """
    Execute SQL by connecting to SQL database and analyze the data using pandas agent
    
    Args:
        question: str, initial user question (ex: How many columns are in the database)
        query: str, SQL query that need to be executed in order to answer the question
    Returns:
        response: string, output of OpenAI models
    """
    
    # connect to database
    cnx = sqlite3.connect('/project/pi_hongyu_umass_edu/zonghai/clinical-llm-alignment/durga_sandeep/Aira/submission/data/fires_database.db')

    extracted_data = pd.read_sql_query(query, cnx)
    
    cnx.close()
    
    # to answer point queries - we do not require pandas agent
    if extracted_data.shape[0] == 1 and extracted_data.shape[1] == 1:
        response = f"{question} : {extracted_data.values[0][0]}"  
        return response

    # for complex queries
    ## load the dataframe into pandas agent for further analysis/generate final response based on the sql output
    # Create the Pandas Dataframe Agent
    
    # print(extracted_data.head())
    
    agent = create_pandas_dataframe_agent(
        llm,
        extracted_data,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        # agent_executor_kwargs={"handle_parsing_errors": True},
        verbose=False,
        # extra_tools = tools,
        # return_intermediate_steps=True
        )
    
    # change the default pandas prompt
    agent.agent.runnable.middle[0].template = get_pandas_prompt()
    
    
    try:
        agent_response = agent.invoke(question)
        return  agent_response['output']
    except Exception as e:
        try:
            response = str(e)
            if "Parsing LLM output produced both a final answer and a parse-able action" in response:
                output = response.split("Final Answer: ")[-1]
                idx = output.find("An output parsing error occurred") 
                if idx != -1:
                    return output[:idx]
                else:
                    return output
            elif "Could not parse LLM output: `" in response:
                idx_prefix = response.find("Could not parse LLM output: `")
                # 29 chars are present in above string - "Could not parse LLM output: `"
                response = response[idx_prefix+29:]
                return response
            
            return response
        except:
            return "Please re-run the pipeline, if it does not work again, please rephrase the prompt for easier understanding"
        