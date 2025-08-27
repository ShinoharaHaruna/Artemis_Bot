from telegram.ext import CommandHandler
from modules.weather import weather_command, forecast_command


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("weather", weather_command))
    dispatcher.add_handler(CommandHandler("forecast", forecast_command))
