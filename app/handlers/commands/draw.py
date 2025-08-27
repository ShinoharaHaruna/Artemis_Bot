from telegram.ext import CommandHandler
from modules.dalle import image_generator


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("draw", image_generator))
