"""Chat Node"""

from typing import List, cast, Literal
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage
from langchain.tools import tool
from langgraph.types import Command
from copilotkit.langgraph import copilotkit_customize_config
import httpx

from cola.state import AgentState
from cola.model import VLM, TXT2IMG_MODEL
from cola.nodes.download import get_reference


async def render_node(state: AgentState, config: RunnableConfig) -> \
    Command[Literal["chat_node"]]:
    """
    Render Node
    """

    ai_message = cast(AIMessage, state["messages"][-1])

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

    model = VLM.get_model(TXT2IMG_MODEL)

    response = await model.text2img(plan2img_prompt)
    print("response:", response)

    if response and response['code'] == 1:
        for i in range(len(response['data']['images'])):
            prototype_imgs.append({"url": response['data']['images'][i]['imageUrl']})
        print("prototype_imgs:", prototype_imgs)
    elif response and response['code'] == 0:
        print("Error:", response['msg'])
    else:
        print("Error:", response)

    return Command(
        goto="chat_node",
        update={
            "prototype_imgs": prototype_imgs,
            "messages": [# Message for passing the result of executing a tool back to a model
                         ToolMessage(
                             tool_call_id=ai_message.tool_calls[0]["id"],
                             content="Prototype image rendered."
            )]
        }
    )
