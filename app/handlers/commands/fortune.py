from telegram.ext import CommandHandler
from modules.fortune import tell_fortune


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("suangua", tell_fortune))
