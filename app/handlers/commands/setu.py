from telegram.ext import CommandHandler
from modules.setu import setu_command


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("setu", setu_command))
