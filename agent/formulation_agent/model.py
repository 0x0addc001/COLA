"""
This module provides a function to get a model based on the configuration.
"""
import os
from typing import cast, Any
from langchain_core.language_models.chat_models import BaseChatModel

from formulation_agent.state import AgentState

def get_model(state: AgentState) -> BaseChatModel:
    """
    Get a model based on the environment variable.
    """

    state_model = state.get("model")
    model = os.getenv("MODEL", state_model)

    print(f"Using model: {model}")

    if model == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model="deepseek-chat", base_url='https://api.deepseek.com')
    # temperature=0,

    raise ValueError("Invalid model specified")
