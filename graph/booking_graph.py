"""
Booking graph : This graph manages the entire booking process, wires the booking agent node into the langraph stategraph.
"""

from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition
from agents.booking_agent import create_booking_node
from tools.mcp_tool import get_mcp_client, get_calender_tools

async def build_booking_graph():
    client = get_mcp_client()
    calender_tools = await get_calender_tools(client)

    if not calender_tools:
        raise RuntimeError("No calendar tools found in MCP server. Please check your MCP configuration and ensure calendar tools are available.")
    booking_node, tools = create_booking_node(calender_tools)

    builder = StateGraph(MessagesState)
    builder.add_node("booking_agent", booking_node)
    builder.add_node("tools", ToolNode(tools))

    builder.add_edge(START, "booking_agent")
    builder.add_conditional_edges("booking_agent", tools_condition)
    builder.add_edge("tools", "booking_agent")

    booking_graph = builder.compile()

    return booking_graph, client