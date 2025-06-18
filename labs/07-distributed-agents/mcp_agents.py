from fastmcp import FastMCP
import requests
import json

mcp = FastMCP("MCP_Agents")

cards = [
    {
        "id": "writer_agent",
        "name": "Writer Agent",
        "description": "An agent that helps with writing tasks.",
        "url": "http://localhost:8000/writer_agent"
    },
    {
        "id": "editor_agent",
        "name": "Editor Agent",
        "description": "An agent that reviews and edits text, provided by a writer agent.",
        "url": "http://localhost:8000/editor_agent"
    }
]

@mcp.tool()
def list_agents() -> list[dict]:
    """
    Returns a list of available agents with their details.
    """
    return cards

@mcp.tool()
def execute_agent(id: str, payload: str) -> str:
    """
    Executes the specified agent.

    Args:
        id (str): The ID of the agent to execute.
        payload (str): The payload to send to the agent's endpoint, in JSON format.

    """
    for card in cards:
        if card["id"] == id:
            url = card["url"]
            try:
                payload = json.loads(payload)  # Convert string payload to JSON
            except json.JSONDecodeError:
                return "Invalid JSON payload"
            
            # Make the REST call
            try:
                response = requests.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(payload)
                )
                response.raise_for_status()
                
                return response.text
            except requests.exceptions.RequestException as e:
                return f"Error executing agent: {str(e)}"
            
    return "Agent not found"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8001)


