import requests


class ChatGPTService:
    """
    与 OpenAI ChatGPT API 交互的服务。
    Service to interact with the OpenAI ChatGPT API.
    """

    def __init__(self, api_key):
        """
        初始化 ChatGPT 服务。
        Initializes the ChatGPT service.

        Args:
            api_key (str): OpenAI API 密钥。
        """
        self.api_key = api_key
        self.api_url = "https://api.openai.com/v1/chat/completions"

    def get_response(
        self,
        prompt,
        system_prompt="你是阿尔忒弥斯，是群组的月神，并且你能回答群组成员的话。",
    ):
        """
        获取 ChatGPT 的响应。
        Gets a response from ChatGPT.

        Args:
            prompt (str): 发送给用户的提示。
            system_prompt (str): 系统级提示。

        Returns:
            str: ChatGPT 的响应文本，或在出错时返回错误信息。
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
