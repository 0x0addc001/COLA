from langchain_core.runnables import RunnableConfig

from renderer.state import AgentState

async def render_node(state: AgentState, config: RunnableConfig):
    # Add your code here
    return state