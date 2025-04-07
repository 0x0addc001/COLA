from typing import ClassVar, Dict

from langchain.chains.qa_generation.prompt import CHAT_PROMPT
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from prompt_toolkit.enums import SEARCH_BUFFER


CHAT_MODEL = "chat"
SEARCH_MODEL = "search"
PLAN_MODEL = "plan"
ADAPT_MODEL = "adapt"
RENDER_MODEL = "render"

class Model:
    _instances: ClassVar[Dict[str, BaseChatModel]] = {}  # Class-level storage for singleton instances

    @classmethod
    def get_model(cls, model_type: str) -> BaseChatModel:
        """
        Get a singleton model instance based on the type (creative/factual).

        Args:
            model_type: CHAT_MODEL, SEARCH_MODEL, PLAN_MODEL, ADAPT_MODEL, RENDER_MODEL

        Returns:
            BaseChatModel: Singleton instance of the requested model.

        Raises:
            ValueError: If an invalid model type is specified.
        """
        if model_type not in cls._instances:
            if model_type == CHAT_MODEL:
                cls._instances[model_type] = ChatOpenAI(
                    model="deepseek-chat",
                    base_url="https://api.deepseek.com",
                    timeout=10000, # 10s timeout
                    # model="deepseek-v3",
                    # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                    temperature=1
                )
            elif model_type == SEARCH_MODEL:
                cls._instances[model_type] = ChatOpenAI(
                    model="deepseek-chat",
                    base_url="https://api.deepseek.com",
                    timeout=10000,  # 10s timeout
                    # model="deepseek-v3",
                    # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                    temperature=0
                )
            elif model_type == PLAN_MODEL:
                cls._instances[model_type] = ChatOpenAI(
                    model="deepseek-chat",
                    base_url="https://api.deepseek.com",
                    timeout=10000,  # 10s timeout
                    # model="deepseek-v3",
                    # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                    temperature=1
                )
            elif model_type == ADAPT_MODEL:
                cls._instances[model_type] = ChatOpenAI(
                    model="deepseek-chat",
                    base_url="https://api.deepseek.com",
                    timeout=10000,  # 10s timeout
                    # model="deepseek-v3",
                    # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                    temperature=1
                )
            elif model_type == RENDER_MODEL:
                cls._instances[model_type] = ChatOpenAI(
                    model="deepseek-chat",
                    base_url="https://api.deepseek.com",
                    timeout=10000,  # 10s timeout
                    # model="deepseek-v3",
                    # base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                    temperature=1
                )
            else:
                raise ValueError("Invalid model type specified. Use 'creative' or 'factual'.")

        return cls._instances[model_type]
