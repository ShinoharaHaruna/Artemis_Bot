from telegram.ext import CommandHandler
from modules.scholar import scholar_command


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("scholar", scholar_command))
