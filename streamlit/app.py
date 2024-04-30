# Imports
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from html_templates import css, user_template, bot_template
import sqlite3
import warnings
warnings.filterwarnings("ignore")

# pandas dataframe
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI, OpenAI


import sys
sys.path.append(".././part1")
sys.path.append(".././part2")
sys.path.append(".././part3")

# import agent modules
from pandas_agent import PandasAgent
from agent_with_tools import PandasAgentWithTools
from sql_agent import SQLAgent

def main():
    st.set_page_config(page_title="AIRA LLM Agent")
    st.subheader("LLM Agent")
    # st.write("Upload your .db file and query answers from your data.")

    # # Apply CSS
    st.write(css, unsafe_allow_html=True)

    # Define chat history session state variable
    st.session_state.setdefault('chat_history', [])

    
    
    # Temperature slider
    st.sidebar.subheader("Agent Configuration")
    with st.sidebar:
        
        # Agent Selection - Pandas, SQL
        agent_options = ["Pandas", "SQL", "Pandas with Tools"]
        AGENT = st.sidebar.selectbox("Select Agent", agent_options, index=0)
        
        # Dropdown for model selection
        model_options = ["gpt-3.5-turbo-0613", "gpt-3.5-turbo-instruct", "gpt-4-turbo-preview", "gpt-4-turbo-2024-04-09", "gpt-4-0125-preview", ]
        MODEL = st.sidebar.selectbox("Select Model", model_options, index=0)
        
        TEMP = st.slider(label="LLM Temperature", min_value=0.0, max_value=1.0, value=0.0)
        
    file = "/project/pi_hongyu_umass_edu/zonghai/clinical-llm-alignment/durga_sandeep/Aira/submission/data/fires_database.db"
    
    # read the .db file
    # cnx = sqlite3.connect(file)
    
    basic_query = "select * from fires limit 5"
    sample_data = pd.read_csv('../data/sample_data.csv') #pd.read_sql_query(basic_query, cnx)
    
    # Display Data Head
    st.write("Data Preview:")
    st.dataframe(sample_data.head()) 
    
    
    df = pd.read_csv('../data/sample_data.csv') #pd.read_sql_query("select * from fires", cnx)
    
    # llm = ChatOpenAI(
    #     openai_api_key="sk-xxxxx",
    #     openai_api_base= "https:xxxx",
    #     temperature=TEMP, 
    #     model= MODEL #"gpt-4-turbo-preview"
    #     )

    # # Create the Pandas Dataframe Agent
    # agent = create_pandas_dataframe_agent(
    #     llm,
    #     df,
    #     agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    #     agent_executor_kwargs={"handle_parsing_errors": True},
    #     verbose=False,
    #     # extra_tools = tools
    #     )
    
    if AGENT == "Pandas":
        agent = PandasAgent(df, model=MODEL, temperature=TEMP)
    elif AGENT == 'SQL':
        agent = SQLAgent(verbose=False)
    else:
        agent = PandasAgentWithTools(df, model=MODEL, temperature=TEMP)

    # Accept input from user
    query = st.text_input("Enter a query:") 

    # Execute Button Logic
    if st.button("Execute") and query:
        with st.spinner('Generating response...'):
            try:

                # Get answer from agent
                answer = agent.run(query)
                # answer = answer['output']
                
                # Store conversation
                st.session_state.chat_history.append(f"USER: {query}")
                st.session_state.chat_history.append(f"AI: {answer}")

                # Display conversation in reverse order
                for i, message in enumerate(reversed(st.session_state.chat_history)):
                    if i % 2 == 0: st.markdown(bot_template.replace("{{MSG}}", message), unsafe_allow_html=True)
                    else: st.markdown(user_template.replace("{{MSG}}", message), unsafe_allow_html=True)

            # Error Handling
            except Exception as e:
                st.error(f"An error occurred: {str(e)} \nsuggestion: Re-run the question, if not, rephrase the question for better responses")

  
if __name__ == "__main__":
    load_dotenv() # Import enviornmental variables
    main()   
