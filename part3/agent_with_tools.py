# import generic packages
import os
import sys

# OpenAI credentials
sys.path.append("../")
from openai_creds import get_key, get_url

# import langchain packages
from langchain.llms import OpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
from langchain_openai import ChatOpenAI, OpenAI

# import external tools
from weather_api import CurrentWeatherInput, CurrentWeatherTool
from wikipedia_api import WikipediaSearchInput, WikipediaSearchTool

# Google search as a tool
os.environ["GOOGLE_CSE_ID"] = "your_cse_id"
os.environ["GOOGLE_API_KEY"] = "your_api_key"

from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_core.tools import Tool

search = GoogleSearchAPIWrapper()

GoogleSearchTool = Tool(
    name="google_search",
    description="use this google search tool whenever wikipedia is not resulting in appropriate results",
    func=search.run,
)


class PandasAgentWithTools:
    def __init__(self, df, model="gpt-3.5-turbo-0613", temperature=0):
        
        llm = ChatOpenAI(
                openai_api_key=get_key(),
                openai_api_base= get_url(),
                temperature=temperature, 
                model= model #"gpt-3.5-turbo-0613" #"gpt-4-turbo-preview"
                )

        # Create the Pandas Dataframe Agent
        self.agent = create_pandas_dataframe_agent(
            llm,
            df,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, #AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            # agent_executor_kwargs={"handle_parsing_errors": True},
            verbose=False,
            extra_tools = [CurrentWeatherTool(), WikipediaSearchTool(), GoogleSearchTool]
            )
        
    def run(self, question):
        
        try:
            agent_response = self.agent.invoke(question)
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

