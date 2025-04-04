"""
This is the main entry point for the AI.
It defines the workflow graph and the entry point for the agent.
"""
# pylint: disable=line-too-long, unused-import
import json
from typing import cast

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from adapter.state import AgentState
from adapter.nodes.download import download_node
from adapter.nodes.chat import chat_node
from adapter.nodes.search import search_node
from adapter.nodes.delete import delete_node, perform_delete_node

# Define a new graph
workflow = StateGraph(AgentState)
workflow.add_node("chat_node", chat_node)


memory = MemorySaver()
workflow.set_entry_point("chat_node")
