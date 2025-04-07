"""
This is the main entry point for the AI.
It defines the workflow graph and the entry point for the agent.
"""
from langgraph.graph import StateGraph
from langgraph.checkpoint.memory import MemorySaver

from cola.state import AgentState
from cola.nodes.download import download_node
from cola.nodes.chat import chat_node
from cola.nodes.search import search_node
from cola.nodes.delete import delete_node, perform_delete_node
from cola.nodes.plan import plan_node
from cola.nodes.adapt import adapt_node
from cola.nodes.render import render_node

# Define a new graph
workflow = StateGraph(AgentState)
workflow.add_node("chat_node", chat_node)
workflow.add_node("search_node", search_node)
workflow.add_node("download", download_node)
workflow.add_node("delete_node", delete_node)
workflow.add_node("perform_delete_node", perform_delete_node)
workflow.add_node("plan_node", plan_node)
workflow.add_node("adapt_node", adapt_node)
workflow.add_node("render_node", render_node)
workflow.set_entry_point("chat_node")
workflow.set_finish_point("chat_node")
workflow.add_edge("search_node", "download")
workflow.add_edge("download", "chat_node")
workflow.add_edge("delete_node", "perform_delete_node")
workflow.add_edge("perform_delete_node", "chat_node")
# workflow.add_edge("plan_node", "chat_node")
workflow.add_edge("adapt_node", "chat_node")
workflow.add_edge("render_node", "chat_node")
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory, interrupt_after=["delete_node"])
