import requests
from telegram.ext import CommandHandler


def random_pixiv_command(update, context):
    """发送一张随机的 Pixiv 图片。"""
    # send a random pixiv image
    url = "https://pixiv-api.vercel.app/api"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # Raise an exception for bad status codes
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=response.content,
            reply_to_message_id=update.message.message_id,
        )
    except requests.exceptions.RequestException as e:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"获取图片失败: {e}",
            reply_to_message_id=update.message.message_id,
        )


def register(dispatcher):
    """注册 /random_pixiv 命令处理器。"""
    # register /random_pixiv command handler
    dispatcher.add_handler(CommandHandler("random_pixiv", random_pixiv_command))
