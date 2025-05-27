"""Chat Node"""

from typing import List, cast, Literal
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import SystemMessage, AIMessage, ToolMessage
from langchain.tools import tool
from langgraph.types import Command
from copilotkit.langgraph import copilotkit_customize_config

from cola.state import AgentState
from cola.model import LLM, ADAPT_MODEL


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

    model = LLM.get_model(ADAPT_MODEL)
    # Prepare the kwargs for the ainvoke method
    ainvoke_kwargs = {}
    if model.__class__.__name__ in ["ChatOpenAI"]:
        ainvoke_kwargs["parallel_tool_calls"] = False

    response = await model.ainvoke([
        SystemMessage(
            content=f"""     
                你是一位资深景观设计提示词专家，专门将景观设计文档转写为Stable Diffusion系列模型可直接使用的英文平面图生成提示词。  
                你的工作流程如下：  
                1. 阅读并理解用户提供的设计方案文档，提炼出简明扼要的摘要；  
                2. 根据摘要并结合给出的专业词汇，用英文撰写高质量的平面图生成提示词；  
                3. 聚焦空间布局、材质质感、光影氛围、构图视角、风格特征等要素，确保提示词精炼、具体、具备可视化指导性；  
                你应仅输出平面图生成提示词，不应包含多余内容。

                以下是设计方案文档：
                {design_plan}
                
                以下是专业词汇：
                {vocab}
                
                以下是平面图生成提示词：
                {plan2img_prompt}
                """
        ),

        *state["messages"],
        ToolMessage(
            tool_call_id=ai_message.tool_calls[0]["id"],
            content=""
        )
    ], config)

    plan2img_prompt = response.content
    return Command(
        goto="chat_node",
        update={
            "plan2img_prompt": plan2img_prompt,
            "messages": [# Message for passing the result of executing a tool back to a model
                         ToolMessage(
                             tool_call_id=ai_message.tool_calls[0]["id"],
                             content="Plan2image prompt written."
                         )]
        }
    )
