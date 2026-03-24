import os
from dotenv import load_dotenv
load_dotenv()

from langchain_mcp_adapters.client import MultiServerMCPClient

COMPOSIO_MCP_URL = os.getenv("COMPOSIO_MCP_URL")
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY")

def get_mcp_client():
    client = MultiServerMCPClient({
    "composio": {
        "transport": "streamable_http",           
        "url": COMPOSIO_MCP_URL,
        "headers": {
            "x-api-key": COMPOSIO_API_KEY
        }
    }
})

    return client


async def get_calender_tools(client: MultiServerMCPClient):
    """
    Get the calendar tools from the composio MCP server.
    """
    tools = await client.get_tools()
    return [t for t in tools if "calendar" in t.name.lower()]