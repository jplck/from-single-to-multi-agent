
import asyncio
import os
import pytz
from datetime import datetime
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import (
    MagenticOneGroupChat,
)
from autogen_agentchat.teams._group_chat._magentic_one._magentic_one_orchestrator import MagenticOneOrchestrator
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

load_dotenv()

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o-mini"

model_client = OpenAIChatCompletionClient(
    model=model_name,
    base_url=endpoint,
    api_key=token
)

# Define a tool
async def get_weather(city: str) -> str:
    print("executing get_weather")
    return f"The weather in {city} is 73 degrees and Sunny."

async def get_medical_history(username: str) -> str:
    "Get the medical history for a given username with known allergies and food restrictions."
    print("executing get_medical_history")
    return f"{username} has an allergy to peanuts and eggs."

async def get_available_incredients(location: str) -> str:
    "Get the available incredients for a given location."
    print("executing get_available_incredients")
    return f"Available incredients in {location} are: eggs, milk, bread, peanuts, beer, wine, salmon, spinache, oil and butter."

def get_current_username(input: str) -> str:
    "Get the username of the current user."
    print("executing get_current_username")
    return "Dennis"

def get_current_location_of_user(username: str) -> str:
    "Get the current timezone location of the user for a given username."
    print("executing get_current_location")
    print(username)
    if "Dennis" in username:
        return "Europe/Berlin"
    else:
        return "America/New_York"

def get_current_time(location: str) -> str:
    "Get the current time in the given location. The pytz is used to get the timezone for that location. Location names should be in a format like America/Seattle, Asia/Bangkok, Europe/London. Anything in Germany should be Europe/Berlin"
    try:
        print("get current time for location: ", location)
        timezone = pytz.timezone(location)
        # Get the current time in the timezone
        now = datetime.now(timezone)
        current_time = now.strftime("%I:%M:%S %p")
        return current_time
    except Exception as e:
        print("Error: ", e)
        return "Sorry, I couldn't find the timezone for that location."
    

users_agent = AssistantAgent(
    "users_agent",
    model_client=model_client,
    tools=[get_current_username, get_medical_history],
    description="A helpful assistant that can knows things about the user like the username and the medical history of the user.",
    system_message="You are a helpful assistant that can retrieve the username and medical history of the current user.",
)

location_agent = AssistantAgent(
    "location_agent",
    model_client=model_client,
    tools=[get_current_location_of_user],
    description="A assistant that can find the physical location of a user.",
    system_message="You are a helpful assistant that can suggest details for a location and can utilize any context information provided.",
)

time_agent = AssistantAgent(
    "time_agent",
    model_client=model_client,
    tools=[get_current_time],
    description="A helpful assistant that knows time in a specific location.",
    system_message="You are a helpful assistant that can retrieve the current time for a given location.",
)

chef_agent = AssistantAgent(
    "chef_agent",
    model_client=model_client,
    tools=[get_available_incredients],
    description="A helpful assistant that can suggest meals and dishes for the right time of the day, location, available ingredients, user preferences and allergies.",
    system_message="You are a helpful assistant that can recommend dishes for the right time of the day, location, available ingredients and user preferences. Make sure you ask for individual food preferences and allergies as input. If you do not have concrete information about allergies you must ask the question and not prepare a dish until you get information.",
)


summary_agent = AssistantAgent(
    "summary_agent",
    model_client=model_client,
    description="A helpful assistant that can summarize details about conversations.",
    system_message="You are a helpful assistant that can take in all of the suggestions and advice from the other agents and leverage them to answer questions. You must ensure that you use that the other agents can solve the problem. When all open questions have been answered, you can respond with TERMINATE.",
)

async def main() -> None:

    inner_termination = MaxMessageTermination(20)
    magenticteam = MagenticOneGroupChat([users_agent, location_agent, time_agent, chef_agent], model_client=model_client, termination_condition=inner_termination)

    # Run the team and stream messages to the console
    stream = magenticteam.run_stream(task="I want to have something to eat. What would you recommend?.")
    await Console(stream)

asyncio.run(main())
