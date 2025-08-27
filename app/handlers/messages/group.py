from telegram.ext import Filters, MessageHandler
import modules.tricks as tricks


def register(dispatcher):
    """
    注册群聊消息处理器，用于处理特定的文本模式。
    Registers the group message handler for specific text patterns.
    """
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, tricks.handle_message)
    )
