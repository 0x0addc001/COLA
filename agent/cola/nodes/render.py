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


@tool
def Search(queries: List[str]): # pylint: disable=invalid-name,unused-argument
    """A list of one or more search queries to find good references to support the design."""

@tool
def RenderPrototypeImgs(urls: List[str]): # pylint: disable=invalid-name,unused-argument
    """Render the prototype images."""

@tool
def DeleteImgReferences(urls: List[str]): # pylint: disable=invalid-name,unused-argument
    """Delete the URLs from the image references."""


async def chat_node(state: AgentState, config: RunnableConfig) -> \
    Command[Literal["render_node", "search_node", "delete_node", "__end__"]]:
    """
    Chat Node
    """

    config = copilotkit_customize_config(
        config,
        emit_intermediate_state=[{ # Lets you emit tool calls as streaming LangGraph state.
            "state_key": "prototype_imgs",
            "tool": "RenderPrototypeImgs",
            "tool_argument": "prototype_imgs",
        }],
    )

    plan2img_prompt = state.get("plan2img_prompt", "")
    state["img_references"] = state.get("img_references", [])
    prototype_img = state.get("prototype_img", [])

    img_references = []

    for img_reference in state["img_references"]:
        content = get_reference(img_reference["url"])
        if content == "ERROR":
            continue
        img_references.append({
            **img_reference,
            "content": content
        })


    # print("````````````chat.py:state:", state)

    # model = get_model(state)
    model = Model.get_model(CREATIVE_MODEL)
    # Prepare the kwargs for the ainvoke method
    ainvoke_kwargs = {}
    if model.__class__.__name__ in ["ChatOpenAI"]:
        ainvoke_kwargs["parallel_tool_calls"] = False

    response = await model.bind_tools(
        [
            Search,
            RenderPrototypeImgs,
            DeleteImgReferences,
        ],
        **ainvoke_kwargs  # Pass the kwargs conditionally
    ).ainvoke([
        SystemMessage(
        #     content=f"""
        #     You are a Landscape Architecture design assistant. You help the user with writing a Landscape Architecture design plan.
        #     You should use the Search tool to get references before writing the design plan.
        #     Do not recite the references, instead, use them to seek traits that could satisfy the user's project settings and creatively use the traits in your own design.
        #     If you finished writing the design plan, ask the user proactively for next steps, changes etc, to make the design plan more comprehensive and engaging.
        #     To write the design plan, you should use the WriteDesignPlan tool. Never EVER respond with the design plan, only use the tool.
        #
        #     This is the project settings:
        #     {project_settings}
        #
        #     This is the design plan:
        #     {design_plan}
        #
        #     Here are the references that you have available:
        #     {references}
        #     """
            content=f"""
                你是一位景观设计助手，负责协助用户渲染设计图。
                在撰写设计方案之前，你应使用 Search 工具查找参考图。
                不要照搬参考图，而是从中提炼出能够满足用户项目需求的风格或轮廓特征，并在你的设计中创造性地加以运用。
                当你完成设计方案撰写后，应主动询问用户下一步的需求、修改意见等，使设计图更加全面且富有吸引力。
                为渲染设计图，你应使用 RenderPrototypeImgs 工具。

                以下是plan2image提示词：
                {plan2img_prompt}

                以下是设计图：
                {prototype_img}

                以下是可供参考的图片：
                {img_references}
                """
        ),

        *state["messages"],
    ], config)

    ai_message = cast(AIMessage, response)

    print("````````````chat.py:response:", response)

    ## Handle tool calls
    # reflexive tool calls
    # non-reflexive tool calls
    goto = "__end__"
    if ai_message.tool_calls and ai_message.tool_calls[0]["name"] == "Search":
        goto = "search_node"
    elif ai_message.tool_calls and ai_message.tool_calls[0]["name"] == "DeleteImgReferences":
        goto = "delete_node"
    elif ai_message.tool_calls and ai_message.tool_calls[0]["name"] == "RenderPrototypeImgs":
        goto = "render_node"


    return Command(
        goto=goto,
        update={
            "messages": response
        }
    )
