"""
This module contains helper functions for working with the composio MCP server.
"""
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_mcp_adapters.client import MultiServerMCPClient

COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY", "")
COMPOSIO_MCP_URL = os.getenv("COMPOSIO_MCP_URL", "")

def get_mcp_client():
    client =  MultiServerMCPClient(
        {
            "composio": {
                "url": COMPOSIO_MCP_URL,
                "transport": "streamable_http",
                "headers": {
                    "x-api-key": COMPOSIO_API_KEY,
                },
            }
        }
    )
    return client

async def get_calendar_tools(client: MultiServerMCPClient):
    """
    Get the calendar tools from the composio MCP server.
    """
    tools = await client.get_tools()
    return [t for t in tools if "calendar" in t.name.lower()]


async def get_gmail_tools(client: MultiServerMCPClient):
    """
    Get the gmail tools from the composio MCP server.
    """
    tools = await client.get_tools()
    return [t for t in tools if "gmail" in t.name.lower()]


async def get_all_tools(client: MultiServerMCPClient):
    """
    Get all tools from the composio MCP server.
    """
    tools = await client.get_tools()
    return tools