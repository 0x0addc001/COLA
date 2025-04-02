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

from modeler.state import AgentState
from modeler.nodes.download import download_node
from modeler.nodes.chat import chat_node
from modeler.nodes.search import search_node
from modeler.nodes.delete import delete_node, perform_delete_node

# Define a new graph
workflow = StateGraph(AgentState)
workflow.add_node("chat_node", chat_node)
# References
workflow.add_node("search_node", search_node)
workflow.add_node("download", download_node)
workflow.add_node("delete_node", delete_node)
workflow.add_node("perform_delete_node", perform_delete_node)


memory = MemorySaver()
workflow.set_entry_point("chat_node")
# References
workflow.add_edge("search_node", "download")
workflow.add_edge("download", "chat_node")
workflow.add_edge("delete_node", "perform_delete_node")
workflow.add_edge("perform_delete_node", "chat_node")
graph = workflow.compile(checkpointer=memory, interrupt_after=["delete_node"])
