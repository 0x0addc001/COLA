"""Chat Node"""

from typing import List, cast, Literal
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage
from langchain.tools import tool
from langgraph.types import Command
from copilotkit.langgraph import copilotkit_customize_config

from adapter.state import AgentState
from adapter.model import Model, CREATIVE_MODEL


import os
current_directory = os.getcwd()
print("当前工作目录：", current_directory)
try:
    with open(r"D:\ThesisProjects\COLA\agent\adapter\nodes\vocab.txt", "r", encoding="utf-8") as file:
        references = file.read()
        print("````````````chat.py:references:", references)
except FileNotFoundError:
    print("错误：文件未找到。请检查文件路径是否正确。")
except UnicodeDecodeError:
    print("错误：文件解码失败。请检查文件编码是否为 UTF-8。")
except Exception as e:
    print(f"发生未知错误：{e}")


@tool
def Search(queries: List[str]): # pylint: disable=invalid-name,unused-argument
    """A list of one or more search queries to find good references to support the design."""

@tool
def WritePlan2ImgPrompt(plan2img_prompt: str): # pylint: disable=invalid-name,unused-argument
    """Write the plan2img prompt."""


async def chat_node(state: AgentState, config: RunnableConfig) -> \
    Command[Literal["__end__"]]:
    """
    Chat Node
    """

    config = copilotkit_customize_config(
        config,
        emit_intermediate_state=[{ # Lets you emit tool calls as streaming LangGraph state.
            "state_key": "plan2img_prompt",
            "tool": "WritePlan2ImgPrompt",
            "tool_argument": "plan2img_prompt",
        }],
    )

    design_plan = state.get("design_plan", "")
    plan2img_prompt = state.get("plan2img_prompt", "")

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
            WritePlan2ImgPrompt,
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
                你是一位景观设计助手，负责协助用户撰写plan2image提示词（即将景观设计方案改写成用于Stable Diffusion图像生成的提示词，**要求必须全文使用英文**）。
                在撰写plan2image提示词时，你应查找并使用参考资料中的专业词汇。
                当你完成plan2image提示词撰写后，应主动询问用户下一步的需求、修改意见等，使提示词更加全面且富有吸引力。
                为撰写plan2image提示词，你应使用 WritePlan2ImgPrompt 工具。

                以下是设计方案：
                {design_plan}
                
                以下是plan2image提示词：
                {plan2img_prompt}

                以下是可供参考的专业词汇：
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
        if ai_message.tool_calls[0]["name"] == "WritePlan2ImgPrompt":
            print("````````````chat.py:reflexive tool calls: WritePlan2ImgPrompt")
            plan2img_prompt = ai_message.tool_calls[0]["args"].get("plan2img_prompt", "")
            return Command(
                goto="chat_node",
                update={
                    "plan2img_prompt": plan2img_prompt,
                    "messages": [ai_message,
                                 # Message for passing the result of executing a tool back to a model
                                 ToolMessage(tool_call_id=ai_message.tool_calls[0]["id"],content="plan2image prompt written.")]
                }
            )
    # non-reflexive tool calls
    goto = "__end__"

    return Command(
        goto=goto,
        update={
            "messages": response
        }
    )
