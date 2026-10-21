import asyncio

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

    async def send_setu(self, update, context):
        """
        发送一张涩图。
        Sends a setu image.
        """
        # requests 网络 I/O → to_thread，避免阻塞事件循环
        # requests network I/O → to_thread, to avoid blocking the event loop
        image_url = await asyncio.to_thread(self.get_setu_url)
        if image_url:
            # MarkdownV2 无法解析 `||...||` 剧透语法且 `~` 为保留字符，故使用 HTML。
            # `||...||` is not valid MarkdownV2 and `~` is a reserved char, so use HTML.
            text = f'<span class="tg-spoiler"><a href="{image_url}">又看涩图！那，那……那就给你吧~</a></span>'
            await update.message.reply_text(text, parse_mode="HTML")
        else:
            await update.message.reply_text("抱歉，获取涩图失败，请稍后再试。")
