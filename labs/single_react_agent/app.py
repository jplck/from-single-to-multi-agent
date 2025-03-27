import os

from langchain import agents
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import tool
from src.single_react_agent.llm import prepare_azure_openai_completion_model

import pytz
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

model_name = os.getenv("AZURE_OPENAI_MODEL_NAME")

llm = prepare_azure_openai_completion_model()
    
@tool
def get_current_username(input: str) -> str:
    "Get the username of the current user."
    return "Dennis"

@tool
def get_current_location(username: str) -> str:
    "Get the current timezone location of the user for a given username."
    print(username)
    if "Dennis" in username:
        return "Europe/Berlin"
    else:
        return "America/New_York"

@tool
def get_current_time(location: str) -> str:
    "Get the current time in the given location. The pytz is used to get the timezone for that location. Location names should be in a format like America/Seattle, Asia/Bangkok, Europe/London. Anything in Germany should be Europe/Berlin"
    try:
        print("get current time for location: ", location)
        location = str.replace(location, " ", "")
        location = str.replace(location, "\"", "")
        location = str.replace(location, "\n", "")
        # Get the timezone for the city
        timezone = pytz.timezone(location)

        # Get the current time in the timezone
        now = datetime.now(timezone)
        current_time = now.strftime("%I:%M:%S %p")

        return current_time
    except Exception as e:
        print("Error: ", e)
        return "Sorry, I couldn't find the timezone for that location."
    
tools = []
tools = [get_current_time]
tools = [get_current_username, get_current_location, get_current_time]

commandprompt = '''
    ##
    You are a helpfull assistent and should respond to user questions.
    If you cannot answer a question then say so explicitly and stop.
    
    '''

promptString = commandprompt +  """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer

Thought: you should always think about what to do

Action: the action to take, should be one of [{tool_names}]. Make sure that Actions are not commands. They should be the name of the tool to use.

Action Input: the input to the action according to the tool signature

Observation: the result of the action

... (this Thought/Action/Action Input/Observation can repeat N times)

Thought: I now know the final answer

Final Answer: the final answer to the original input question

Begin!

Question: {input}

Thought:{agent_scratchpad}

"""
prompt = PromptTemplate.from_template(promptString)

agent = create_react_agent(llm, tools, prompt)

agent_executor = agents.AgentExecutor(
        name="Tools Agent",
        agent=agent, tools=tools,  verbose=True, handle_parsing_errors=True, max_iterations=10, return_intermediate_steps=True,
    )

input = "What is the current time in Berlin?"

response = agent_executor.invoke(
    {"input": input},
)
       