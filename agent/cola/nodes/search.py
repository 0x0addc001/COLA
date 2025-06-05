"""
The search node is responsible for searching the internet for information.
"""

import os
from typing import cast, List
from pydantic import BaseModel, Field
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage, ToolMessage, SystemMessage
from langchain.tools import tool
from tavily import TavilyClient
from copilotkit.langgraph import copilotkit_emit_state, copilotkit_customize_config

from cola.state import AgentState
from cola.model import LLM, SEARCH_MODEL

class ReferenceInput(BaseModel):
    """A reference with a short description"""
    url: str = Field(description="The URL of the reference")
    title: str = Field(description="The title of the reference")
    description: str = Field(description="A short description of the reference")

@tool
def ExtractReferences(references: List[ReferenceInput]): # pylint: disable=invalid-name,unused-argument
    """Extract the 3 most relevant references from a search result."""

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

async def search_node(state: AgentState, config: RunnableConfig):
    """
    The search node is responsible for searching the internet for references.
    """

    ai_message = cast(AIMessage, state["messages"][-1])

    project_settings = state.get("project_settings", "")

    state["references"] = state.get("references", [])
    state["logs"] = state.get("logs", [])
    queries = ai_message.tool_calls[0]["args"]["queries"]

    for query in queries:
        state["logs"].append({
            "message": f"正在查找 {query}",
            "done": False
        })

    await copilotkit_emit_state(config, state)

    search_results = []

    for i, query in enumerate(queries):
        response = tavily_client.search(query)
        search_results.append(response)
        state["logs"][i]["done"] = True
        await copilotkit_emit_state(config, state)





    config = copilotkit_customize_config(
        config,
        emit_intermediate_state=[{
            "state_key": "references",
            "tool": "ExtractReferences",
            "tool_argument": "references",
        }],
    )

    model = LLM.get_model(SEARCH_MODEL)
    ainvoke_kwargs = {}
    if model.__class__.__name__ in ["ChatOpenAI"]:
        ainvoke_kwargs["parallel_tool_calls"] = False

    # figure out which references to use
    response = await model.bind_tools(
        [ExtractReferences],
        tool_choice="ExtractReferences",
        **ainvoke_kwargs
    ).ainvoke([
        # 选取并格式化
        SystemMessage(
            content=f"""
                你是一名景观设计方案资料筛选专家，负责为设计创作甄选高质量的参考资料。
                你的工作流程如下：
                1. 仔细研读用户提供的项目设定，并对照检索结果进行比对分析。
                2. 从检索结果中筛选出与项目设定最相关并且最有参考价值的3条资料，需要具备一定的可持续性、美学性或功能性。
                
                以下是项目设定：
                {project_settings}
                """
        ),
        *state["messages"],
        ToolMessage(
            tool_call_id=ai_message.tool_calls[0]["id"],
            content=f"已检索到的参考资料: {search_results}"
    )
    ], config)

    state["logs"] = [] # 清空日志
    await copilotkit_emit_state(config, state)

    ai_message_response = cast(AIMessage, response)
    references = ai_message_response.tool_calls[0]["args"]["references"]

    state["references"].extend(references)

    state["messages"].append(ToolMessage(
        tool_call_id=ai_message.tool_calls[0]["id"],
        content=f"已添加以下参考资料: {references}"
    ))

    return state
