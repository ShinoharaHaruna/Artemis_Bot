import requests


class OneWordService:
    """
    从 Hitokoto API 获取一言的服务。
    Service to get a "one-word" quote from the Hitokoto API.
    """

    def __init__(self):
        """
        初始化一言服务。
        Initializes the OneWordService.
        """
        self.api_url = "https://v1.hitokoto.cn/"
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    def get_one_word(self):
        """
        获取一句一言。
        Gets a quote.

        Returns:
            str: 获取到的一言或错误信息。
        """
        try:
            response = requests.get(self.api_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            response_json = response.json()
            return response_json.get("hitokoto", "无法获取一言。")
        except requests.exceptions.RequestException as e:
            return f"请求一言 API 失败: {e}"
        except (KeyError, IndexError):
            return "解析一言 API 响应失败。"
