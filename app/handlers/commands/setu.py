import requests
from telegram.ext import CommandHandler


def setu_command(update, context):
    """
    处理 /setu 命令，发送一张涩图。
    Handles the /setu command, sending a "setu" (lewd picture).
    """
    url = "https://api.nyan.xyz/httpapi/sexphoto?r18=true"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        image_url = data.get("data", {}).get("url", [None])[0]

        if image_url:
            # The || syntax creates a spoiler in Telegram MarkdownV2
            text = f"||[又看涩图！那，那……那就给你吧\~]({image_url})||"
            update.message.reply_text(
                text,
                parse_mode="MarkdownV2",
                disable_web_page_preview=True,
            )
        else:
            update.message.reply_text("涩图找不到了，下次再试吧。")

    except requests.exceptions.RequestException as e:
        update.message.reply_text(f"获取涩图失败: {e}")
    except (KeyError, IndexError):
        update.message.reply_text("获取涩图失败，API 响应格式不正确。")


def register(dispatcher):
    """
    注册 /setu 命令处理器。
    Registers the /setu command handler.
    """
    dispatcher.add_handler(CommandHandler("setu", setu_command))
