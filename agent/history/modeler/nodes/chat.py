"""Chat Node"""

from typing import List, cast, Literal
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage
from langchain.tools import tool
from langgraph.types import Command
from copilotkit.langgraph import copilotkit_customize_config

from modeler.state import AgentState
from modeler.model import Model, CREATIVE_MODEL
from modeler.nodes.download import get_reference


@tool
def Search(queries: List[str]): # pylint: disable=invalid-name,unused-argument
    """A list of one or more search queries to find good references to support the design."""

@tool
def WriteDesignPlan(design_plan: str): # pylint: disable=invalid-name,unused-argument
    """Write the design plan."""

@tool
def WriteProjectSettings(project_settings: str): # pylint: disable=invalid-name,unused-argument
    """Write the project settings."""

@tool
def DeleteReferences(urls: List[str]): # pylint: disable=invalid-name,unused-argument
    """Delete the URLs from the references."""


async def chat_node(state: AgentState, config: RunnableConfig) -> \
    Command[Literal["search_node", "chat_node", "delete_node", "__end__"]]:
    """
    Chat Node
    """

    config = copilotkit_customize_config(
        config,
        emit_intermediate_state=[{ # Lets you emit tool calls as streaming LangGraph state.
            "state_key": "design_plan",
            "tool": "WriteDesignPlan",
            "tool_argument": "design_plan",
        }, {
            "state_key": "project_settings",
            "tool": "WriteProjectSettings",
            "tool_argument": "project_settings",
        }],
    )

    state["references"] = state.get("references", [])
    project_settings = state.get("project_settings", "")
    design_plan = state.get("design_plan", "")

    references = []

    for reference in state["references"]:
        content = get_reference(reference["url"])
        if content == "ERROR":
            continue
        references.append({
            **reference,
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
            WriteDesignPlan,
            WriteProjectSettings,
            DeleteReferences,
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
                你是一位景观设计助手，负责协助用户撰写景观设计方案。
                在撰写设计方案之前，你应使用 Search 工具查找参考资料。
                不要照搬参考资料的内容，而是从中提炼出能够满足用户项目需求的特征，并在你的设计中创造性地加以运用。
                当你完成设计方案撰写后，应主动询问用户下一步的需求、修改意见等，使设计方案更加全面且富有吸引力。
                为撰写设计方案时，你应使用 WriteDesignPlan 工具。

                以下是项目设定：
                {project_settings}

                以下是设计方案：
                {design_plan}

                以下是可供参考的资料：
                {references}
                """
        ),

        *state["messages"],
    ], config)

    ai_message = cast(AIMessage, response)

    print("````````````chat.py:response:", response)

    ## Handle tool calls
    # reflexive tool calls
    if ai_message.tool_calls:
        if ai_message.tool_calls[0]["name"] == "WriteProjectSettings":
            print("````````````chat.py:reflexive: WriteProjectSettings")
            # ...
            return Command(
                goto="chat_node",
                update={
                    "project_settings": ai_message.tool_calls[0]["args"]["project_settings"],
                    "messages": [ai_message, ToolMessage(
                        tool_call_id=ai_message.tool_calls[0]["id"],
                        content="Project settings written."
                    )]
                }
            )
        if ai_message.tool_calls[0]["name"] == "WriteDesignPlan":
            print("````````````chat.py:reflexive: WriteDesignPlan")
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
    # non-reflexive tool calls
    goto = "__end__"
    if ai_message.tool_calls and ai_message.tool_calls[0]["name"] == "Search":
        goto = "search_node"
    elif ai_message.tool_calls and ai_message.tool_calls[0]["name"] == "DeleteReferences":
        goto = "delete_node"


    return Command(
        goto=goto,
        update={
            "messages": response
        }
    )
