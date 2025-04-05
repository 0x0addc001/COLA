from typing import ClassVar, Dict
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel

CREATIVE_MODEL = "creative"
FACTUAL_MODEL = "factual"

class Model:
    _instances: ClassVar[Dict[str, BaseChatModel]] = {}  # Class-level storage for singleton instances

    @classmethod
    def get_model(cls, model_type: str) -> BaseChatModel:
        """
        Get a singleton model instance based on the type (creative/factual).

        Args:
            model_type: Either "creative" (temperature=1) or "factual" (temperature=0).

        Returns:
            BaseChatModel: Singleton instance of the requested model.

        Raises:
            ValueError: If an invalid model type is specified.
        """
        if model_type not in cls._instances:
            if model_type == CREATIVE_MODEL:
                cls._instances[model_type] = ChatOpenAI(
                    model="deepseek-chat",
                    base_url="https://api.deepseek.com",
                    temperature=1
                )
            elif model_type == FACTUAL_MODEL:
                cls._instances[model_type] = ChatOpenAI(
                    model="deepseek-chat",
                    base_url="https://api.deepseek.com",
                    temperature=0
                )
            else:
                raise ValueError("Invalid model type specified. Use 'creative' or 'factual'.")

        return cls._instances[model_type]
