from telegram import Update
from telegram.ext import CallbackContext, Filters, MessageHandler
from modules.random_pixiv import handle_random_pixiv
from modules.setu import setu_command
from modules.answerbook import answer_command
from modules.scholar import scholar_command
from modules.list_help import list_help
from modules.weather import handle_weather, handle_forecast
from app.core.config import WEATHER_API_KEY, TIMEZONE


def private_message_handler(update: Update, context: CallbackContext):
    """
    处理私聊消息。
    Handles private messages.
    """
    user = update.message.from_user
    message = update.message

    if message.text is not None:
        # 这部分未来也可以重构为 CommandHandlers，以获得更好的一致性
        # This part can also be refactored into CommandHandlers in the future for better consistency
        if message.text.startswith("/random_pixiv"):
            handle_random_pixiv(context.bot, update)
        elif message.text.startswith("/setu"):
            setu_command(context, update)
        elif message.text.startswith("/answer"):
            answer_command(context, update)
        elif message.text.startswith("/scholar"):
            scholar_command(context, update)
        elif message.text.startswith("/help"):
            list_help(context, update)
        elif message.text.startswith("/weather"):
            handle_weather(
                context.bot,
                update.effective_chat.id,
                WEATHER_API_KEY,
                update.message.message_id,
            )
        elif message.text.startswith("/forecast"):
            handle_forecast(
                context.bot,
                user.id,
                WEATHER_API_KEY,
                TIMEZONE,
                update.message.message_id,
            )


def register(dispatcher):
    """
    注册私聊消息处理器。
    Registers the private message handler.
    """
    dispatcher.add_handler(MessageHandler(Filters.private, private_message_handler))
