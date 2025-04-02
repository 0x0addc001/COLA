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
            content=f"""
            You are a design assistant. You help the user with writing a design plan.
            You should use the search tool to get references before writing the design plan.
            Do not recite the references, instead, use them to seek traits that could satisfy the user's project settings and creatively use the traits in your own design.
            If you finished writing the design plan, ask the user proactively for next steps, changes etc, make it engaging.
            To write the design plan, you should use the WriteDesignPlan tool. Never EVER respond with the design plan, only use the tool.

            This is the project settings:
            {project_settings}

            This is the design plan:
            {design_plan}

            Here are the references that you have available:
            {references}
            """
        ),
        *state["messages"],
    ], config)

    ai_message = cast(AIMessage, response)

    print("````````````chat.py:response:", response)

    if ai_message.tool_calls:
        if ai_message.tool_calls[0]["name"] == "WriteProjectSettings":
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
