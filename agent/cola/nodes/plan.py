"""Chat Node"""

from typing import List, cast, Literal
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage
from langchain.tools import tool
from langgraph.types import Command
from copilotkit.langgraph import copilotkit_customize_config

from cola.state import AgentState
from cola.model import Model, CREATIVE_MODEL
from cola.nodes.download import get_reference


async def plan_node(state: AgentState, config: RunnableConfig) -> \
    Command[Literal["chat_node"]]:
    """
    Plan Node
    """

    project_settings = state.get("project_settings", "")
    design_plan = state.get("design_plan", "")
    state["references"] = state.get("references", [])
    references = []
    for reference in state["references"]:
        content = get_reference(reference["url"])
        if content == "ERROR":
            continue
        references.append({
            **reference,
            "content": content
        })

    model = Model.get_model(CREATIVE_MODEL)
    # Prepare the kwargs for the ainvoke method
    ainvoke_kwargs = {}
    if model.__class__.__name__ in ["ChatOpenAI"]:
        ainvoke_kwargs["parallel_tool_calls"] = False

    response = await model.ainvoke([
        SystemMessage(
            content=f"""
                你是一位景观设计方案专家，负责协助用户撰写景观设计方案。
                在撰写设计方案时，你应参照参考资料而不要照搬参考资料的内容，你应从中提炼出能够满足用户项目设定的特征，并在你的设计中创造性地加以运用。

                以下是项目设定：
                {project_settings}
                
                以下是参考资料：
                {references}

                以下是设计方案：
                {design_plan}
                """
        ),

        *state["messages"],
    ], config)

    ai_message = cast(AIMessage, response)
    design_plan = ai_message.tool_calls[0]["args"].get("design_plan", "")
    return Command(
        goto="chat_node",
        update={
            "design_plan": design_plan,
            "messages": [ai_message, ToolMessage(
                tool_call_id=ai_message.tool_calls[0]["id"],
                content="Design plan written."
            )]
        }
    )
