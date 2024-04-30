# Aira-LLM-Agents
Installation Guidelines: Virtual environment is preferred over global environment
1. conda create --name Aira python=3.9
2. pip install pandas numpy openai langchain langchain-experimental langchain-openai
3. pip install tabulate langchainhub scikit-learn
4. pip install matplotlib
5. pip install streamlit python-dotenv


# Streamlit app
1. conda activate Aira
2. cd streamlit
3. streamlit run app.py or streamlit run app.py --server.fileWatcherType none
![https://github.com/DurgaSandeep25/Aira-LLM-Agents/blob/main/demo/streamlit_examples/0_interface.PNG]

# Dataset url - download and add it in your data
- https://www.kaggle.com/datasets/rtatman/188-million-us-wildfires/data
- https://drive.google.com/file/d/14Q3tXrebIwoNOOFsVTP3jj_7VQjxJ7KX/view?usp=sharing

Important:
1. Add your openai credentials in the openai_creds - both key and url
2. Instead of langchain from pip, I have restructured some of the code in langchain source code, please install from there
    - cd langchain/libs/langchain
    - pip install -e .
3. OpenAI has variability even though we set temperature=0.0 (can be related to the security reasons) - please re-run or change our prompt (few changes) to get desired outputs


Main Files:
- Part 1 - pandas_agent.py
- Part 2 - sql_agent.py
- Part 3 - agent_with_tools.py


Usage Guidelines: Please refer demo folder for examples
- retrieve_performance.ipynb
    - helps to scale our agents to very large datasets
    - to evaluate the robustness of our system 
    - Evaluation data is generated using ChatGPT through few-shot prompting
    - this module can be used in pandas agent and sql agent - can help scaling these modules for very large datasets

- pandas_agent_demo.ipynb
    - demonstrates how my agent can answer wide-variety of data analysis queries, it is flexible enough to steer our agent based on user-intent

- sql_agent_demo.ipynb
    - In this notebook, it shows how our agent able to answer queries specific database without loading the whole data

- agent_with_tools.ipynb
    - demonstrates how my agent can access external real-world knowledge like wikipedia, google search and weather data
