from telegram.ext import CommandHandler
from modules.random_pixiv import handle_random_pixiv


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("random_pixiv", handle_random_pixiv))
