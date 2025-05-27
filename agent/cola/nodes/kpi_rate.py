"""KPI-Assess Node"""

from typing import List, cast, Literal
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage
from langchain.tools import tool
from langgraph.types import Command
from copilotkit.langgraph import copilotkit_customize_config

from cola.state import AgentState
from cola.model import LLM, KPI_RATE_MODEL
from cola.nodes.download import get_reference


async def kpi_rate_node(state: AgentState, config: RunnableConfig) -> \
        Command[Literal["chat_node"]]:
    """
    KPI-Rate Node
    """

    ai_message = cast(AIMessage, state["messages"][-1])
    # print("ai_message", ai_message)

    # project_settings = state.get("project_settings", "")
    design_plan = state.get("design_plan", "")
    # prototype_imgs = state.get("prototype_imgs", [])
    prototype_imgs = []
    for prototype_img in state["prototype_imgs"]:
        prototype_imgs.append(prototype_img["url"])
    print("prototype_imgs:", prototype_imgs)

    model = LLM.get_model(KPI_RATE_MODEL)
    # Prepare the kwargs for the ainvoke method
    ainvoke_kwargs = {}
    if model.__class__.__name__ in ["ChatOpenAI"]:
        ainvoke_kwargs["parallel_tool_calls"] = False

    response = await model.ainvoke([
        SystemMessage(
            content=[
                {
                    "type": "text",
                    "text": f"""
                你是一位景观设计方案评估专家，专门负责对风景园林设计方案进行多维度量化评估并输出改进建议。
                你的工作流程如下：  
                1. 读取输入的设计方案文档和平面图及示意图。
                2. 撰写评估报告。
                   请从以下三个核心维度进行评估，每个维度按 0–10 分打分，并逐项撰写分析与改进建议：
                   （1）生态可持续性
                     分数：__ /10
                     分析：考察雨水管理、生物多样性、碳汇潜力、环境保护等要素  
                     改进建议：提出一条或多条具体、可操作的优化建议。
                   （2）美学性
                     分数：__ /10
                     分析：考察视觉吸引力、景观特色、色彩与材质协调性、整体艺术感等方面 
                     改进建议：提出改进方案以提升整体美感与辨识度。
                   （3）功能性
                     分数：__ /10
                     分析：考察使用便捷性、空间可达性、安全性、功能布局合理性与对用户需求的满足程度
                     改进建议：指出设计中存在的功能性问题，并提出优化措施。
                你应仅输出评估报告，不应包含多余内容。
              
                以下是设计方案文档：
                {design_plan}
                
                平面图已作为附件上传
                """
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": prototype_imgs[0],
                    },
                },
            ]
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
