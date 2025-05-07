"""KPI-Assess Node"""

from typing import List, cast, Literal
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage
from langchain.tools import tool
from langgraph.types import Command
from copilotkit.langgraph import copilotkit_customize_config

from cola.state import AgentState
from cola.model import LLM, KPI_ASSESS_MODEL
from cola.nodes.download import get_reference


async def kpi_assess_node(state: AgentState, config: RunnableConfig) -> \
        Command[Literal["chat_node"]]:
    """
    KPI-Assess Node
    """

    ai_message = cast(AIMessage, state["messages"][-1])
    # print("ai_message", ai_message)

    project_settings = state.get("project_settings", "")
    design_plan = state.get("design_plan", "")
    prototype_imgs = state.get("prototype_imgs", [])

    model = LLM.get_model(KPI_ASSESS_MODEL)
    # Prepare the kwargs for the ainvoke method
    ainvoke_kwargs = {}
    if model.__class__.__name__ in ["ChatOpenAI"]:
        ainvoke_kwargs["parallel_tool_calls"] = False

    response = await model.ainvoke([
        SystemMessage(
            content=f"""
                你是一位景观设计方案评估专家，负责协助用户评估景观设计方案。
                在评估设计方案时，你应参!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                你只应回复评估结果，不应回复任何多余的内容。

                以下是项目设定：
                {project_settings}
                
                以下是设计方案：
                {design_plan}
                
                以下是设计平面图：
                {prototype_imgs}
                """
        ),
        *state["messages"],
        ToolMessage(
            tool_call_id=ai_message.tool_calls[0]["id"],
            content=""
        )
    ], config)

    assessment_report = response.content
    print("response:", response)
    return Command(
        goto="chat_node",
        update={
            "assessment_report": assessment_report,
            "messages": [  # Message for passing the result of executing a tool back to a model
                ToolMessage(
                    tool_call_id=ai_message.tool_calls[0]["id"],
                    content="Assessment report written."
                )]
        }
    )
