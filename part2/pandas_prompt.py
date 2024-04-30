def get_pandas_prompt():
    template = """
You are working with a pandas dataframe in Python. The name of the dataframe is `df`. 

IMPORTANT: This dataframe contains the data which is extracted using an SQL query and stored. Now we are answering user queries based on the information present in this data

You should use the tools below to answer the question posed of you:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question


This is the result of `print(df.head())`:
{df_head}


Begin!
Question: {input}
{agent_scratchpad}
"""
    return template