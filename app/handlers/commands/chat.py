from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from modules.chatgpt import chat_command as original_chat_command


def chat_command(update: Update, context: CallbackContext):
    """
    处理 /chat 命令，调用原始的 chat_command 函数。
    Handles the /chat command by calling the original chat_command function.
    """
    original_chat_command(update, context)


def register(dispatcher):
    """
    注册 chat 命令处理器。
    Registers the chat command handler.
    """
    dispatcher.add_handler(CommandHandler("chat", chat_command))
