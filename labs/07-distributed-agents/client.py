from typing import Any
import asyncio
import json
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("AZURE_OPENAI_API_KEY")
if api_key:
    print("Using Azure OpenAI")
    deployment_name=os.environ["AZURE_OPENAI_COMPLETION_DEPLOYMENT_NAME"] 
    llm = init_chat_model(
        deployment_name, 
        model_provider="azure_openai", 
        api_key=api_key, 
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), 
        api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    )
    
else:
    print("Using GitHub Inference")
    llm = init_chat_model(
        model=os.environ.get("AZURE_OPENAI_COMPLETION_MODEL"), 
        model_provider="openai", 
        temperature=0.7, 
        api_key=os.getenv("GITHUB_TOKEN"), 
        base_url="https://models.inference.ai.azure.com"
    )

async def main():
    # Initialize the MCP client
    mcp_client = MultiServerMCPClient({
        "MCP_Agents": {
                "url": "http://127.0.0.1:8001/mcp",
                "transport": "streamable_http",
        },
    })

    tools = await mcp_client.get_tools()
    print(f"Available tools: {tools}")

    
    agent = create_react_agent(
        model=llm,
        tools=tools,
    )

    system_prompt = """
    Your job is to orchestrate multiple agents to complete tasks. Create a plan what to call and when. 
    Use the tools provided to you to select the right agents to call. Start always with getting the list of available agents. 
    Iterate on your results and refine your plan based on the responses you get from the agents by calling an agent from the list of available agents. 
    If you need to call an agent, use the `execute_agent` tool with the agent ID and the content you want to send.
    """

    inputs = {"messages": [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Write a short story about a robot learning to dance."}]}
    response = await agent.ainvoke(inputs)
    print("Agent response:", response)

if __name__ == "__main__":
    asyncio.run(main())