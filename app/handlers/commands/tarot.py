from telegram.ext import CommandHandler
from modules.tarot import tarot_command


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("tarot", tarot_command))
