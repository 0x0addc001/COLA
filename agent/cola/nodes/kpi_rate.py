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
    prototype_imgs = state.get("prototype_imgs", [])

    model = LLM.get_model(KPI_RATE_MODEL)
    # Prepare the kwargs for the ainvoke method
    ainvoke_kwargs = {}
    if model.__class__.__name__ in ["ChatOpenAI"]:
        ainvoke_kwargs["parallel_tool_calls"] = False

    response = await model.ainvoke([
        SystemMessage(
            content=f"""
                你是一位景观设计方案评估专家，专门负责对风景园林设计方案进行多维度量化评估并输出改进建议。请严格按照以下流程和格式执行：
                1. 输入
                 - 设计方案文档：{design_plan}
                 - 平面图：{prototype_imgs}
                2. 评估维度（按 0–10 分制）  
                 - 生态可持续性：评估方案对雨水管理、生物多样性、碳汇与环境保护等方面的贡献。
                 - 美学性：评估方案的视觉吸引力、造景特色、和谐度与整体艺术感。
                 - 功能性：评估方案的使用便捷性、可达性、安全性以及满足用户需求的程度。
                3. 输出结构  
                请按以下 JSON 格式输出，保证字段完整、规范。  
                ```json
                
{
  "scores": {
    "ecological_sustainability": 0–10,
    "aesthetics": 0–10,
    "functionality": 0–10
  },
  "analysis": {
    "ecological_sustainability": "简要分析……",
    "aesthetics": "简要分析……",
    "functionality": "简要分析……"
  },
  "recommendations": {
    "ecological_sustainability": "改进建议",
    "aesthetics": "改进建议",
    "functionality": "改进建议",
    ]
  }
}
                ```
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
