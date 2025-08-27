from telegram.ext import CommandHandler
from modules.remake import remake_command


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("remake", remake_command))
