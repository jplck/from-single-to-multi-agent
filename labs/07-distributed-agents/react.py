import os
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage
from langgraph.func import entrypoint, task
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class CustomReactAgent:

    def __init__(self, tools, llm: BaseChatModel):
        self.model = llm
        self.tools = tools
        self.tools_by_name = {tool.name: tool for tool in tools}
        
    async def ainvoke(self, messages: list[BaseMessage], callbacks=[]):
        @task
        async def call_model(messages):
            response = await self.model.bind_tools(self.tools).ainvoke(messages, config={"callbacks": callbacks})
            return response
                
        @task
        async def call_tool(tool_call) -> ToolMessage:
            tool = self.tools_by_name[tool_call["name"]]
            observation = await tool.ainvoke(tool_call["args"])
            return ToolMessage(content=observation, tool_call_id=tool_call["id"])

        @entrypoint()
        async def custom_react_agent(messages: list):
            llm_response = await call_model(messages)

            while True:
                if not llm_response.tool_calls:
                    break

                # Execute tools
                tool_result_futures = [
                    call_tool(tool_call) for tool_call in llm_response.tool_calls
                ]
                tool_results = [await fut for fut in tool_result_futures]

                # Append to message list
                messages = add_messages(messages, [llm_response, *tool_results])

                # Call model again
                llm_response = await call_model(messages)

            return llm_response

        async for step in custom_react_agent.astream(messages):
            for task_name, message in step.items():
                if task_name == "custom_react_agent":
                    continue  # Just print task updates
                print(f"\n{task_name}:")
                message.pretty_print()
    