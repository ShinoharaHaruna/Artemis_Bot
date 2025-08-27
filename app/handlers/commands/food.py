from telegram.ext import CommandHandler
from modules.food import food_command


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("food", food_command))
