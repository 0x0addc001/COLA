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


async def render_node(state: AgentState, config: RunnableConfig) -> \
    Command[Literal["render_node", "search_node", "delete_node", "__end__"]]:
    """
    Render Node
    """

    plan2img_prompt = state.get("plan2img_prompt", "")
    prototype_imgs = state.get("prototype_imgs", [])
    state["img_references"] = state.get("img_references", [])
    img_references = []
    for img_reference in state["img_references"]:
        content = get_reference(img_reference["url"])
        if content == "ERROR":
            continue
        img_references.append({
            **img_reference,
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
                以下是plan2image提示词：
                {plan2img_prompt}

                以下是参考图片：
                {img_references}
                
                以下是设计图：
                {prototype_imgs}
                """
        ),

        *state["messages"],
    ], config)

    ai_message = cast(AIMessage, response)
    # prototype_imgs = ai_message.tool_calls[0]["args"].get("prototype_imgs", "")
    prototype_imgs = []
    return Command(
        goto="chat_node",
        update={
            "prototype_imgs": prototype_imgs,
            "messages": [ai_message, ToolMessage(
                tool_call_id=ai_message.tool_calls[0]["id"],
                content="Design plan written."
            )]
        }
    )
