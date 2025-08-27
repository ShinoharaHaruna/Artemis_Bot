from telegram.ext import CommandHandler
from modules.anonymous import admin_command, anonymous_command


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("anonymous", anonymous_command))
    dispatcher.add_handler(CommandHandler("admin", admin_command))
