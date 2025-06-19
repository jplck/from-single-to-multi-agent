# Distributed Agents with Model Context Protocol (MCP)

This lab demonstrates how to build a distributed agent system using the Model Context Protocol (MCP). The system consists of multiple components that communicate with each other to complete complex tasks using specialized AI agents.

## Architecture Overview

The distributed agents system consists of three main components:

1. **Client** (`client.py`) - The orchestrator that initiates the agent workflow
2. **MCP Server** (`mcp_agents.py`) - A middleware that exposes tools for the client to discover and interact with agents
3. **Agent Server** (`agents.py`) - A FastAPI server that hosts specialized AI agents

```
┌──────────┐     ┌──────────────┐     ┌───────────────┐
│          │     │              │     │  Writer Agent │
│  Client  │─────┤  MCP Server  │─────┤               │
│          │     │              │     │ Editor Agent  │
└──────────┘     └──────────────┘     └───────────────┘
```

## Prerequisites

Before running the distributed agents system, ensure you have the following:

1. Python 3.9+ installed
2. Required packages installed:
   ```bash
   pip install fastapi uvicorn langchain-mcp-adapters langchain-openai langgraph fastmcp pydantic requests dotenv
   ```
3. Azure OpenAI API key or GitHub token set in environment variables

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
AZURE_OPENAI_API_KEY=<your-api-key>
AZURE_OPENAI_ENDPOINT=<your-endpoint>
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_COMPLETION_DEPLOYMENT_NAME=<your-deployment-name>
# Optional, for GitHub Inference
GITHUB_TOKEN=<your-github-token>
AZURE_OPENAI_COMPLETION_MODEL=<model-name>
```

## How It Works

### 1. Agent Server (agents.py)

The Agent Server hosts specialized AI agents through FastAPI endpoints:

- `/writer_agent` - Creates creative written content
- `/editor_agent` - Edits and improves text content

Each agent leverages LLMs to perform its specialized task.

### 2. MCP Server (mcp_agents.py)

The MCP Server acts as a registry and router for agents, providing two key tools:

- `list_agents()` - Returns information about available agents
- `execute_agent(id, content)` - Calls a specific agent with content

### 3. Client (client.py)

The Client connects to the MCP Server and creates an orchestration agent that:

1. Discovers available agents via `list_agents()`
2. Sends user requests to appropriate agents via `execute_agent()`
3. Returns the results to the user

The client uses ReAct (Reasoning + Acting) to make decisions about which agents to call.

## Running the System

To run the complete system, open three separate terminal windows and execute the following commands in order:

### Terminal 1: Start the Agent Server
```bash
cd /workspaces/from-single-to-multi-agent/labs/07-distributed-agents
python agents.py
```

### Terminal 2: Start the MCP Server
```bash
cd /workspaces/from-single-to-multi-agent/labs/07-distributed-agents
python mcp_agents.py
```

### Terminal 3: Run the Client
```bash
cd /workspaces/from-single-to-multi-agent/labs/07-distributed-agents
python client.py
```

## Debugging with VS Code

VS Code provides powerful debugging capabilities that can help you troubleshoot issues in your distributed agents system. Follow these steps to set up and use the VS Code debugger effectively:

### Setting up VS Code Debug Configurations

Create a `.vscode/launch.json` file in your workspace with the following configurations:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Agent Server",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/labs/07-distributed-agents/agents.py",
            "console": "integratedTerminal",
            "justMyCode": false,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "MCP Server",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/labs/07-distributed-agents/mcp_agents.py",
            "console": "integratedTerminal",
            "justMyCode": false,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "Client",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/labs/07-distributed-agents/client.py",
            "console": "integratedTerminal",
            "justMyCode": false,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "Agent Server (Remote Attach)",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "."
                }
            ]
        }
    ],
    "compounds": [
        {
            "name": "All Components",
            "configurations": ["Agent Server", "MCP Server", "Client"]
        }
    ]
}
```

### Using the VS Code Debugger

1. **Setting Breakpoints**:
   - Click in the gutter next to the line numbers where you want to pause execution
   - Breakpoints appear as red dots

2. **Starting Debugging Sessions**:
   - Open the Debug panel (Ctrl+Shift+D or Cmd+Shift+D)
   - Select a configuration from the dropdown menu (e.g., "Agent Server")
   - Click the green play button or press F5

3. **Debugging Multiple Components**:
   - Use the "All Components" compound configuration to launch all three services
   - Or launch each component separately in different debugging sessions

4. **Debug Console**:
   - When hitting a breakpoint, use the Debug Console to inspect variables
   - Type variable names to see their values
   - Use expressions like `dir(variable)` to explore objects

5. **Remote Debugging**:
   - For debugging a running process, add this code at the beginning of your script:
     ```python
     import debugpy
     debugpy.listen(5678)
     print("Waiting for debugger to attach...")
     debugpy.wait_for_client()
     ```
   - Then use the "Agent Server (Remote Attach)" configuration

6. **Watch Variables**:
   - Add important variables to the Watch panel
   - They'll be automatically evaluated as you step through code

7. **Step Through Code**:
   - Use Step Over (F10) to execute the current line
   - Use Step Into (F11) to dive into function calls
   - Use Step Out (Shift+F11) to complete the current function

8. **Debug HTTP Requests**:
   - Set breakpoints in your endpoint handlers to inspect incoming requests
   - Examine the `request` object in FastAPI endpoints
   - Check request body, headers, and query parameters

### Debugging Across Components

To debug the interaction between components:

1. Launch each component in separate debugging sessions
2. Set breakpoints at key communication points:
   - Before making HTTP requests
   - When handling incoming requests
   - When parsing responses

3. When a breakpoint is hit, examine the variables to see what data is being sent/received
4. Use the Debug Console to modify variables if needed to test different scenarios

## Debugging Common Issues

### 1. HTTP 422 Unprocessable Entity Errors

If you encounter 422 errors when calling agents, check:

- **JSON Payload Format**: Ensure the payload sent to agent endpoints matches their expected format
- **Request Headers**: Verify the Content-Type header is set to application/json
- **Endpoint Handlers**: Check if the endpoint is properly parsing the incoming request

To debug:

```python
# Add this to your agent endpoint for debugging
print(f"Received payload: {await request.json()}")
```

### 2. Connection Errors

If components can't connect:

- **Port Conflicts**: Check if ports 8000 and 8001 are already in use
- **Host Binding**: Ensure servers are binding to the correct interface (0.0.0.0 or 127.0.0.1)
- **Firewall Issues**: Check if your firewall is blocking any connections

### 3. LLM API Errors

If LLM calls fail:

- **API Keys**: Verify environment variables are correctly set
- **Rate Limits**: Check if you're hitting API rate limits
- **Model Availability**: Ensure the specified model is available in your region

### 4. Agent Orchestration Issues

If the client isn't properly orchestrating agents:

- **Tool Discovery**: Check if `list_agents()` is returning the expected results
- **Agent Execution**: Debug the execute_agent function to see what's being sent to agents
- **Response Parsing**: Verify the client correctly parses agent responses

To debug tool execution, add a logging statement:

```python
@mcp.tool()
def execute_agent(id: str, content: str) -> str:
    print(f"Executing agent: {id} with content: {content}")
    # ... rest of the code
```

## Extending the System

You can extend this system by:

1. **Adding New Agents**: Create new endpoints in agents.py and register them in mcp_agents.py
2. **Improving the Orchestrator**: Enhance the client's prompting to make better decisions
3. **Adding Memory**: Implement a state management system for maintaining context between calls
4. **Adding Authentication**: Secure the API endpoints with proper authentication
5. **Implementing Streaming**: Add streaming responses for more responsive interactions

## Architecture Benefits

This distributed architecture offers several advantages:

- **Modularity**: Agents can be developed and deployed independently
- **Scalability**: Components can be scaled individually based on demand
- **Specialization**: Each agent can be optimized for specific tasks
- **Resilience**: The system can continue operating even if some agents fail
- **Flexibility**: New agents can be added without modifying the client

## Advanced Debugging Techniques

### Logging with VS Code Debug Output

Instead of using `print()` statements, you can use Python's logging module which integrates well with VS Code:

```python
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Use throughout your code
logger.debug("Request received: %s", request_data)
logger.info("Agent executed successfully")
logger.warning("API call took longer than expected")
logger.error("Failed to connect to agent: %s", error)
```

This provides more structured logs in the VS Code Debug Console, with different colors for different log levels.

### Debugging Network Issues

For network issues, VS Code's debugger can be complemented with:

1. **HTTP Inspection**:
   - Add the VS Code "Thunder Client" or "REST Client" extension
   - Send test requests to your endpoints to verify they're working correctly
   - Inspect the raw responses

2. **Async Debugging**:
   - For async code, set the `"justMyCode": false` option in launch configurations
   - This allows you to step through the async runtime libraries
   - Use the "Call Stack" view to understand the async execution flow

### Profiling Performance

If you encounter performance issues:

1. Install `cProfile` and use it to profile your code:
   ```python
   import cProfile
   
   def run_with_profiling():
       cProfile.runctx('main()', globals(), locals(), 'output.prof')
   
   if __name__ == "__main__":
       run_with_profiling()
   ```

2. Use VS Code's built-in Performance view (Shift+Cmd+P or Shift+Ctrl+P, then "Developer: Show Performance") to monitor resource usage.

### Debugging Concurrency Issues

When debugging concurrency across your distributed agents:

1. Use VS Code's built-in "Run and Debug" view to see multiple debugging sessions side by side
2. Set breakpoints with conditions to only break when specific conditions are met
3. Use the "Call Stack" view to understand execution flow across async boundaries
4. Add logging with timestamps to track the sequence of events across components
