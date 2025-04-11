import streamlit as st
from semantic_kernel.contents.chat_history import ChatHistory
import asyncio
import os
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.kernel import Kernel
from semantic_kernel.functions import KernelArguments

from semantic_kernel.connectors.ai.azure_ai_inference import AzureAIInferenceChatCompletion
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

from dotenv import load_dotenv

load_dotenv()

def init_chat_completion_service():
    service_id = "azure_openai"

    if os.environ.get("AZURE_OPENAI_API_KEY"):
        print("Using Azure OpenAI")
        chat_completion_service = AzureChatCompletion(
            deployment_name=os.environ["AZURE_OPENAI_COMPLETION_DEPLOYMENT_NAME"],  
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            service_id=service_id,
        )
    else:
        # To authenticate with the model you will need to generate a personal access token (PAT) in your GitHub settings. 
        # Create your PAT token by following instructions here: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
        base_url="https://models.inference.ai.azure.com"
        api_key=os.environ["GITHUB_TOKEN"]

        chat_completion_service = AzureAIInferenceChatCompletion(
            ai_model_id="gpt-4o-mini",
            api_key=api_key,
            endpoint=base_url,
            service_id=service_id,
        )

    return chat_completion_service

class JokePlugin:
    """A plugin that generates jokes based on a topic"""

    @kernel_function(name="generate_joke", description="Generate a joke about a specific topic")
    async def generate_joke(self, input: str, style: str = "silly") -> str:
        """
        Generate a joke about a given topic using the AI model
        
        Args:
            input: The topic to create a joke about
            style: The style of the joke (silly, clever, pun, etc.)
        """
        print(f"Generating a {style} joke about {input}")
        # This function doesn't directly generate the joke - it returns
        # a prompt that will be sent to the model to generate the joke
        return f"Create a {style} joke about {input}. Keep it short and family-friendly."

def create_kernel():
    """Create a kernel with the chat completion service"""
    kernel = Kernel()
    kernel.add_service(init_chat_completion_service())
    kernel.add_plugin(JokePlugin())
    return kernel

def create_agent():
    """Create an agent with the chat completion service"""
    kernel = create_kernel()

    # Create the agent
    joke_agent = ChatCompletionAgent(
        kernel=kernel,
        name="joke_agent",
        instructions="You are a helpful assistant that tells jokes. Keep it short, family-friendly and entertaining.",
    )
    
    return joke_agent

# A helper method to invoke the agent with the user input
async def invoke_agent(agent, input_text):
    """Invoke the agent to create a joke for a topic with the user input."""
    st.session_state["history"].add_user_message(input_text)
    
    # Get the result from the agent
    result = await agent.get_response(
        messages=st.session_state["history"]
    )
    
    # Extract the joke text from the response
    joke = result.content.content
    
    st.session_state["history"].add_assistant_message(joke)
    return joke

async def run_app():
    st.title("Joke Bot")
    st.write('Give a topic so I can give you back a joke')
    
    reset = st.button('Reset Messages')
    if "history" not in st.session_state or reset:
        st.write('Resetting messages...' if reset else 'Initializing chat history...')
        st.session_state["history"] = ChatHistory()
        st.session_state["history"].add_system_message("You are a helpful assistant that tells jokes.")

    if "agent" not in st.session_state:
        st.session_state["agent"] = create_agent()
    
    for msg in st.session_state["history"]:
        with st.chat_message(msg.role):
            st.markdown(msg.content)
    
    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Use the joke_agent with our invoke_agent function
        result = await invoke_agent(st.session_state["agent"], prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(result)

asyncio.run(run_app())