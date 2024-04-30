# load required packages
import os
import sys
import pandas as pd
from openai import OpenAI
from typing import Any, Dict, List, Literal, Optional, Sequence, Union
sys.path.append("../")

from openai_creds import get_key, get_url
## OpenAI Credentials
client = OpenAI(api_key=get_key(), base_url= get_url())

# Long Description of each column has been modified using ChatGPT - for compact representation of column information
rephrased = pd.read_csv("/project/pi_hongyu_umass_edu/zonghai/clinical-llm-alignment/durga_sandeep/Aira/data/rephrased_column_description")
rephrased = "\n".join(rephrased['rephrased_description'].tolist())

def get_simple_retrieval_prompt(input: str, k: int = 5) -> str:
    
    """Construct a prompt to retrieve top k columns  that might be required to answer the given query in the order of their relevance to answer the query.

    Args:
        input: User question/query.
        k: number of relevant columns to be extracted (higher k can have higher accuracy but increases gpt inference cost).

    Returns:
        prompt: string, the prompt to retrieve top k columns 
    """
    
    cols = [f'col{i+1}' for i in range(k)]
    
    naive_prompt = f""""### Instruction: Your task is to retrieve top {k} columns that might be required to answer the given query in the order of their relevance to answer the query.

Following are the small description about each column in the pandas dataframe.

### Columns:
{rephrased}

Retrieve Top {k} columns from above to answer the given query. Response format should be `{cols}`.
- Query: {input}

    """
    return naive_prompt

# code snippet to connect with OpenAI API
def get_gpt_output_top_k(input_prompt: str, model: str = "gpt-3.5-turbo") -> str:
    
    """Access OpenAI premium models through API
    
    Args:
        input_prompt: language model prompt
        model: choosing OpenAI models (Ex: GPT-3.5/GPT-4 models) - refer -> https://platform.openai.com/docs/models/overview
    Returns:
        output: string, model generated text for the given input_prompt
        
    """
    
    completion = client.chat.completions.create(
    model=model,
    temperature=0.0,
    messages=[
        {"role": "system", "content": "You are a helpful assitant which follows instructions strictly."},
        {"role": "user", "content": input_prompt}
    ]
    )
    return completion.choices[0].message.content

sample_data = pd.read_csv('/project/pi_hongyu_umass_edu/zonghai/clinical-llm-alignment/durga_sandeep/Aira/data/sample_data.csv')
def extract_column_content(input_text: str) -> List[str]:
    
    """Parse column information in the input_text
    
    Args:
        input_text: generated text from the OpenAI
    Returns:
        res: list of strings, extracted column names
        
    """
    
    res = []
    for col in sample_data.columns.tolist():
        if col in input_text:
            res.append(col)
    return res


def add_confused_columns(lis: List[str]):
    """Adding following columns increased the accuracy of our overall system by more than 8% (on my test data)"""
    
    # Following 2 columns are being confused gpt with other columns in the data while extracting relevant columns
    cols = ["SOURCE_REPORTING_UNIT_NAME", "SOURCE_SYSTEM"]
    for col in cols:
        if col not in lis:
            lis.append(col)
    return lis

# Agent that can provide top 5 relevant columns in the dataframe to answer the user query
class RetrievalAgent:
    def __init__(self, model = "gpt-3.5-turbo", k=5):
        self.model = model
        self.k = k
        print("Retrieval Agent Configurations")
        print("Model : ", model)
        print("k (no. of columns to extract): ", k)
        
    def run(self, query):
        try:
            system_prompt = get_simple_retrieval_prompt(query)
            output = get_gpt_output_top_k(system_prompt)
        except:
            print("Error while retrieving......")
            print("Suggestion: Try rephrasing the question")
            output = "[]"
        
        # parse the output for final result
        res = [] 
        try:
            res = eval(output)
        except:
            res = extract_column_content(output)
        
        if len(res) == 0:
            print(f"Error: Could not find top {self.k} columns, considering all the columns as default")
            res = sample_data.columns.tolist()
            res.remove('shape')
        else:
            for col in ['SOURCE_REPORTING_UNIT_NAME', 'SOURCE_SYSTEM']:
                if col not in res:
                    res.append(col)
        return res