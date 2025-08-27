from telegram.ext import CommandHandler
from modules.answerbook import answer_command


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("answer", answer_command))
