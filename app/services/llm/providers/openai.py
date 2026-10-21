import requests

from app.services.llm.base import LLMService


class OpenAIProvider(LLMService):
    """
    与 OpenAI Chat Completions API 交互的 LLM 提供商。
    LLM provider that interacts with the OpenAI Chat Completions API.

    Ported from the old chatgpt_service — this is the reference
    implementation for future providers.
    """

    def __init__(self, api_key: str):
        """
        初始化 OpenAI 提供商。
        Initializes the OpenAI provider.

        Args:
            api_key (str): OpenAI API 密钥。
        """
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/chat/completions"

    def get_response(self, prompt: str, system_prompt: str | None = None) -> str:
        """
        获取 OpenAI 的响应。
        Gets a response from OpenAI.

        Args:
            prompt (str): 发送给用户的提示。
            system_prompt (str | None): 系统级提示。

        Returns:
            str: 响应文本，或在出错时返回错误信息。
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
        }

        try:
            response = requests.post(
                self.api_url, headers=headers, json=data, timeout=60
            )
            response.raise_for_status()
            response_json = response.json()
            return response_json["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            return f"请求 OpenAI API 失败: {e}"
        except (KeyError, IndexError):
            return "解析 OpenAI API 响应失败。"
