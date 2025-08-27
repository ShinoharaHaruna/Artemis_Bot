from telegram.ext import CommandHandler
from modules.list_help import list_help


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("help", list_help))
