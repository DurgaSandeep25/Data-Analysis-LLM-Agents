# Import required packages
import sys
sys.path.append("/project/pi_hongyu_umass_edu/zonghai/clinical-llm-alignment/durga_sandeep/Aira/submission/helper")

import pandas as pd

# import the retrieval agent
from retrieve_top_k_columns import RetrievalAgent
from custom_sql_prompt import get_custom_sql_prompt
from write_and_validate_sql_query import write_sql_query
from extract_sql import extract_sql_query
from execute_query import execute_query

class SQLAgent:
    def __init__(self, verbose=False):
        
        self.retrieve_agent = RetrievalAgent(model="gpt-3.5-turbo", k=5)
        # verbose=True - if you want the intermediate outputs to be shown while execution
        self.verbose=verbose
    
    def run(self, question):
        
        if self.verbose: print(f"Question: {question}")
        
        # retrieve top k columns from the question that are relevant to answer the question
        top_k_columns = self.retrieve_agent.run(question)
        if self.verbose: 
            print(f"Top k Columns: {top_k_columns}")
            print("\n")
        # custom sql prompt - modify the prompt such that in the table only relevant column information is present
        agent_prompt = get_custom_sql_prompt(top_k_columns)
        
        # write and validate sql query - in single prompt (it can be done in two prompts - but requires more cost)
        sql_query_raw = write_sql_query(question=question, system=agent_prompt)
        if self.verbose: 
            print(f"SQL Query Raw: \n{sql_query_raw}")
            print("\n")
        
        # Extract SQL query from raw output - sometimes sql special token is added in the raw output
        sql_query = extract_sql_query(sql_query_raw)
        if self.verbose: 
            print(f"SQL Final Query: \n{sql_query}")
            print("\n")
            
        # Query Execute - execute the query to extract the relevant information and use pandas agent for analysis
        output = execute_query(question=question,query=sql_query)
        
        return output
        
        
        
    


