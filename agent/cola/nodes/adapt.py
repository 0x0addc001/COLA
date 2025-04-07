"""Chat Node"""

from typing import List, cast, Literal
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage
from langchain.tools import tool
from langgraph.types import Command
from copilotkit.langgraph import copilotkit_customize_config

from cola.state import AgentState
from cola.model import Model, ADAPT_MODEL


import os
current_directory = os.getcwd()
print("当前工作目录：", current_directory)
try:
    with open(r".\cola\nodes\vocab.txt", "r", encoding="utf-8") as file:
        vocab = file.read()
        # print("vocab:", vocab)
except FileNotFoundError:
    print("错误：文件未找到。请检查文件路径是否正确。")
except UnicodeDecodeError:
    print("错误：文件解码失败。请检查文件编码是否为 UTF-8。")
except Exception as e:
    print(f"发生未知错误：{e}")


async def adapt_node(state: AgentState, config: RunnableConfig) -> \
    Command[Literal["chat_node"]]:
    """
    Adapt Node
    """

    ai_message = cast(AIMessage, state["messages"][-1])

    design_plan = state.get("design_plan", "")
    plan2img_prompt = state.get("plan2img_prompt", "")

    model = Model.get_model(ADAPT_MODEL)
    # Prepare the kwargs for the ainvoke method
    ainvoke_kwargs = {}
    if model.__class__.__name__ in ["ChatOpenAI"]:
        ainvoke_kwargs["parallel_tool_calls"] = False

    response = await model.ainvoke([
        SystemMessage(
            content=f"""
                你是一位景观设计提示词专家，负责协助用户撰写plan2image提示词（即将景观设计方案改写成用于Stable Diffusion图像生成的提示词）。
                在撰写plan2image提示词时，你应全文使用英文，并且查找并使用专业词汇。
                你只需返回plan2image提示词，不要返回任何多余的内容。

                以下是设计方案：
                {design_plan}
                
                以下是专业词汇：
                {vocab}
                
                以下是plan2image提示词：
                {plan2img_prompt}
                """
        ),

        *state["messages"],
    ], config)

    plan2img_prompt = response
    return Command(
        goto="chat_node",
        update={
            "plan2img_prompt": plan2img_prompt,
            "messages": [# Message for passing the result of executing a tool back to a model
                         ToolMessage(
                             tool_call_id=ai_message.tool_calls[0]["id"],
                             content="plan2image prompt written."
                         )]
        }
    )
