import requests


class SetuService:
    """
    提供从 apy.lolicon.app 获取涩图的服务。
    Service for fetching setu from apy.lolicon.app.
    """

    def __init__(self):
        """
        初始化服务。
        Initializes the service.
        """
        self.api_url = "https://api.lolicon.app/setu/v2?r18=0&size=regular"

    def get_setu_url(self):
        """
        获取一张涩图的 URL。
        Gets a setu URL.

        Returns:
            str: 图片 URL，或在失败时返回 None。
        """
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("error") == "" and data.get("data"):
                return data["data"][0]["urls"]["regular"]
        except (requests.exceptions.RequestException, KeyError, IndexError):
            pass
        return None

    def send_setu(self, update, context):
        """
        发送一张涩图。
        Sends a setu image.
        """
        image_url = self.get_setu_url()
        if image_url:
            text = f"||[又看涩图！那，那……那就给你吧~]({image_url})||"
            update.message.reply_text(text, parse_mode="MarkdownV2")
        else:
            update.message.reply_text("抱歉，获取涩图失败，请稍后再试。")
