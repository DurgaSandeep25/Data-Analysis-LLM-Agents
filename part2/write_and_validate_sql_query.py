# Import required packages
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities import SQLDatabase

from typing import Any, Dict, List, Literal, Optional, Sequence, Union

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

# connect to SQL database

db = SQLDatabase.from_uri("sqlite:///../data/fires_database.db")
context = db.get_context()

def parse_final_answer(output: str) -> str:
    """Final answer: - is the type of special token to identify the SQL output"""
    try:
        return output.split("Final answer: ")[1]
    except:
        return output

def write_sql_query(question: str, system: str) -> str:
    
    """
    Write and validate sql query using chains
    
    Args:
        question: str, question: str, initial user question (ex: How many columns are in the database)
        system: str, single system prompt that contains validation step as well
    Returns:
        output: string, SQL query (it might contains some special tokens)
    """
    
    # create a chat template
    prompt = ChatPromptTemplate.from_messages([("system", system), ("human", "{input}")]).partial(dialect=db.dialect)
    
    # create a chain
    write_query = create_sql_query_chain(llm, db, prompt=prompt) 
    chain = write_query | parse_final_answer
    
    # invoke the chain to generate and also validate sql query (validation is incorporated inside the prompt)
    query = chain.invoke(
        {
            "question": question
        }
    )
    return query