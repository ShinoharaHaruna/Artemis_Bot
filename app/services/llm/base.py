from abc import ABC, abstractmethod


class LLMService(ABC):
    """
    LLM 服务的抽象基类。
    Abstract base class for LLM services.

    A provider implements get_response and returns the generated text,
    or an error string — matching the old chatgpt_service contract.
    """

    @abstractmethod
    def get_response(self, prompt: str, system_prompt: str | None = None) -> str:
        """
        获取 LLM 的响应。
        Gets a response from the LLM.

        Args:
            prompt (str): 用户提示 / user prompt.
            system_prompt (str | None): 系统级提示 / system prompt.

        Returns:
            str: LLM 的响应文本，或在出错时返回错误信息。
        """
