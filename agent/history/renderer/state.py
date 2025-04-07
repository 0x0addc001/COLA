"""
This is the state definition for the AI.
It defines the state of the agent and the state of the conversation.
"""

from typing import List, TypedDict
from langgraph.graph import MessagesState

class Reference(TypedDict):
    """
    Represents an reference. Give it a precise title and a short description.
    """
    url: str
    title: str
    description: str

class Log(TypedDict):
    """
    Represents a log of an action performed by the agent.
    """
    message: str
    done: bool

class AgentState(MessagesState):
    """
    This is the state of the agent.
    It is a subclass of the MessagesState class from langgraph.
    """
    plan2img_prompt: str
    img_references: List[Reference]
    prototype_imgs: List[Reference]
    logs: List[Log]
