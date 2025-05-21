"""Chat Node"""

from typing import List, cast, Literal
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage
from langchain.tools import tool
from langgraph.types import Command
from copilotkit.langgraph import copilotkit_customize_config

from cola.state import AgentState
from cola.model import LLM, CHAT_MODEL
from cola.nodes.download import get_reference

@tool
def Search(queries: List[str]): # pylint: disable=invalid-name,unused-argument
    """A list of one or more search queries to find good references to support the design."""

@tool
def DeleteReferences(urls: List[str]): # pylint: disable=invalid-name,unused-argument
    """Delete the URLs from the references."""

@tool
def WriteDesignPlan(): # pylint: disable=invalid-name,unused-argument
    """Write the design plan."""

@tool
def WritePlan2ImgPrompt(): # pylint: disable=invalid-name,unused-argument
    """Write the plan2img prompt."""

@tool
def RenderPrototypeImgs(): # pylint: disable=invalid-name,unused-argument
    """Render the prototype images."""

@tool
def WriteAssessmentReport(): # pylint: disable=invalid-name,unused-argument
    """Write the assessment report."""


async def chat_node(state: AgentState, config: RunnableConfig) -> \
    Command[Literal["search_node", "delete_node", "plan_node", "adapt_node", "render_node", "kpi_rate_node", "__end__"]]:
    """
    Chat Node
    """

    """
    Streaming state updates
    Out of the box, CopilotKit will sync the state of your LangGraph agent with the frontend, whenever entering or exiting a node.
    You can also configure CopilotKit to stream messages, LLM state updates and tool calls from your LangGraph agent.
    """
    config = copilotkit_customize_config(
        config,
        # Lets you emit tool calls as streaming LangGraph state.
        emit_intermediate_state=[{
             "state_key": "references",
             "tool": "Search",
             "tool_argument": "queries",
        },
        {
             "state_key": "references",
             "tool": "DeleteReferences",
             "tool_argument": "urls",
        },
        {
            "state_key": "design_plan",
            "tool": "WriteDesignPlan",
            "tool_argument": "",
        },
        {
            "state_key": "plan2img_prompt",
            "tool": "WritePlan2ImgPrompt",
            "tool_argument": "",
        },
        {
            "state_key": "prototype_imgs",
            "tool": "RenderPrototypeImgs",
            "tool_argument": "",
        },
        {
             "state_key": "assessment_report",
             "tool": "WriteAssessmentReport",
             "tool_argument": "",
        }
        ],
    )

    project_settings = state.get("project_settings", "")
    design_plan = state.get("design_plan", "")
    plan2img_prompt = state.get("plan2img_prompt", "")
    prototype_imgs = state.get("prototype_imgs", [])
    assessment_report = state.get("assessment_report", "")

    state["references"] = state.get("references", [])
    state["img_references"] = state.get("img_references", [])
    references = []
    for reference in state["references"]:
        content = get_reference(reference["url"])
        if content == "ERROR":
            continue
        references.append({
            **reference,
            "content": content
        })
    img_references = []
    for img_reference in state["img_references"]:
        img_references.append(img_reference)

    model = LLM.get_model(CHAT_MODEL)
    # Prepare the kwargs for the ainvoke method
    ainvoke_kwargs = {}
    if model.__class__.__name__ in ["ChatOpenAI"]:
        ainvoke_kwargs["parallel_tool_calls"] = False

    response = await model.bind_tools(
        [
            Search,
            DeleteReferences,
            WriteDesignPlan,
            WritePlan2ImgPrompt,
            RenderPrototypeImgs,
            WriteAssessmentReport,
        ],
        **ainvoke_kwargs  # Pass the kwargs conditionally
    ).ainvoke([
        SystemMessage(
            content=f"""
                你是一位景观设计助手，负责协助用户完成景观设计。
                请严格按照以下7步进行工作：
                1. 获取项目设定。
                2. 使用 Search 工具查找参考资料。
                3. 使用 WriteDesignPlan 工具撰写设计方案文档。
                4. 使用 WritePlan2ImgPrompt 工具撰写平面图生成提示词。
                5. 获取参考图。
                6. 使用 RenderPrototypeImgs 工具渲染设计平面图。
                7. 使用 WriteAssessmentReport 工具评估设计方案和平面图。
                在完成每一步时，你应主动向用户征询这一步所需的考虑因素，不应询问用户这一步之后的步骤。
                在完成每一步后，你应主动中断工作并向用户征询这一步的意见，不应复述工作文档中的内容。
                全部工作文档如下。

                以下是项目设定：
                {project_settings}
                
                以下是参考资料：
                {references}

                以下是设计方案文档：
                {design_plan}
                
                以下是平面图生成提示词：
                {plan2img_prompt}
                
                以下是参考图：
                {img_references}
                
                以下是设计平面图：
                {prototype_imgs}
                
                以下是评估报告：
                {assessment_report}
                """
        ),
        *state["messages"],
    ], config)

    ai_message = cast(AIMessage, response)

    ## Handle tool calls
    goto = "__end__"
    if ai_message.tool_calls and ai_message.tool_calls[0]["name"] == "Search":
        goto = "search_node"
    elif ai_message.tool_calls and ai_message.tool_calls[0]["name"] == "DeleteReferences":
        goto = "delete_node"
    elif ai_message.tool_calls and ai_message.tool_calls[0]["name"] == "WriteDesignPlan":
        goto = "plan_node"
    elif ai_message.tool_calls and ai_message.tool_calls[0]["name"] == "WritePlan2ImgPrompt":
        goto = "adapt_node"
    elif ai_message.tool_calls and ai_message.tool_calls[0]["name"] == "RenderPrototypeImgs":
        goto = "render_node"
    elif ai_message.tool_calls and ai_message.tool_calls[0]["name"] == "WriteAssessmentReport":
        goto = "kpi_rate_node"

    return Command(
        goto=goto,
        update={
            "messages": response
        }
    )
