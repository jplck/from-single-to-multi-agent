# Copyright (c) Microsoft. All rights reserved.

import asyncio
import os
from openai import AsyncOpenAI

from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.core_plugins.time_plugin import TimePlugin
from semantic_kernel.core_plugins.math_plugin import MathPlugin
from semantic_kernel.core_plugins.text_plugin import TextPlugin
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
from semantic_kernel.contents.chat_message_content import ChatMessageContent
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.functions.kernel_function_from_prompt import KernelFunctionFromPrompt
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)
from semantic_kernel.functions import KernelArguments, kernel_function
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.kernel import Kernel
from dotenv import load_dotenv
from plugins import ChefPlugin

load_dotenv()

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "o3-mini"

openai_client = AsyncOpenAI(
    base_url=endpoint,
    api_key=token
)

EXPERT_NAME = "Expert"

def _create_kernel_with_chat_completion(service_id: str) -> Kernel:
        
    chat_completion_service = OpenAIChatCompletion(
        ai_model_id=model_name,
        api_key=token,
        async_client=openai_client,
        service_id=service_id
    )

    kernel = Kernel()
    kernel.add_service(chat_completion_service)
    kernel.add_plugin(
      ChefPlugin(),
      plugin_name="Chef",
   )
    return kernel

def _create_chat_completion_client() -> OpenAIChatCompletion:
    
    reasoning_kernel = _create_kernel_with_chat_completion(EXPERT_NAME)
    execution_settings = reasoning_kernel.get_prompt_execution_settings_from_service_id(service_id=EXPERT_NAME)
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()
    
    agent_expert_instance = ChatCompletionAgent(
        kernel=reasoning_kernel,
        name=EXPERT_NAME,
        arguments=KernelArguments(settings=execution_settings),
        instructions="""
            Your sole responsiblity is provide the best recommendation possible using all tools and information available.

            - Never address the user.
            """,
    )

    return agent_expert_instance

async def main():
    
    agent_expert = _create_chat_completion_client()
    thread: ChatHistoryAgentThread = None

    is_complete: bool = False
    while not is_complete:
        user_input = input("User:> ")
        if not user_input:
            continue

        if user_input.lower() == "exit":
            is_complete = True
            break

        if user_input.lower() == "reset":
            await thread.delete() if thread else None
            await thread.create() if thread else None
            print("[Conversation has been reset]")
            continue

        async for response in agent_expert.invoke(messages=user_input, thread=thread):
            print(f"# {response.role} - {response.name or '*'}: '{response.content}'")
            thread = response.thread


if __name__ == "__main__":
    asyncio.run(main())