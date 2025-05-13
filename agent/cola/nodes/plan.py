"""Chat Node"""

from typing import List, cast, Literal
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage
from langchain.tools import tool
from langgraph.types import Command
from copilotkit.langgraph import copilotkit_customize_config

from cola.state import AgentState
from cola.model import LLM, PLAN_MODEL
from cola.nodes.download import get_reference


async def plan_node(state: AgentState, config: RunnableConfig) -> \
    Command[Literal["chat_node"]]:
    """
    Plan Node
    """

    ai_message = cast(AIMessage, state["messages"][-1])
    # print("ai_message", ai_message)

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

    model = LLM.get_model(PLAN_MODEL)
    # Prepare the kwargs for the ainvoke method
    ainvoke_kwargs = {}
    if model.__class__.__name__ in ["ChatOpenAI"]:
        ainvoke_kwargs["parallel_tool_calls"] = False

    response = await model.ainvoke([
        SystemMessage(
            content=f"""
                你是一位资深的景观设计方案专家，专门为各类项目撰写创新、可落地的景观设计方案。  
                你的工作流程如下：  
                1. 阅读并理解用户提供的项目设定，明确需求目标、场地特征、预算与功能要求；  
                2. 研读参考资料，吸收其中灵感和要点，但绝不照搬原文，而是提炼出能满足项目设定的关键元素，并在设计中以创造性方式加以整合与优化；  
                3. 输出完整的设计方案，包括总体构思、景观分区、植物配置、材料与工艺、造型与细节等；  
                4. 整体方案需兼顾可持续性、美学与功能性，并突出创新亮点，仅输出设计方案内容，不要包含过程说明或多余评论；  

                以下是项目设定：
                {project_settings}
                
                以下是参考资料：
                {references}

                以下是设计方案：
                {design_plan}
                """
        ),
        *state["messages"],
        ToolMessage(
            tool_call_id=ai_message.tool_calls[0]["id"],
            content=""
        )
    ], config)

    design_plan = response.content
    print("response:", response)
    return Command(
        goto="chat_node",
        update={
            "design_plan": design_plan,
            "messages": [# Message for passing the result of executing a tool back to a model
                ToolMessage(
                tool_call_id=ai_message.tool_calls[0]["id"],
                content="Design plan written."
            )]
        }
    )
