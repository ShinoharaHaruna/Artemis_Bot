from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


def chat_command(update: Update, context: CallbackContext):
    """
    处理 /chat 命令，与 ChatGPT 进行交互。
    Handles the /chat command to interact with ChatGPT.
    """
    chatgpt_service = context.bot_data.get("chatgpt_service")
    if not chatgpt_service:
        update.message.reply_text("ChatGPT 服务未初始化，请联系管理员。")
        return

    if not context.args:
        update.message.reply_text("请在 /chat 命令后输入您想说的话。")
        return

    prompt = " ".join(context.args)
    response = chatgpt_service.get_response(prompt)
    update.message.reply_text(response)


def register(dispatcher):
    """
    注册 chat 命令处理器。
    Registers the chat command handler.
    """
    dispatcher.add_handler(CommandHandler("chat", chat_command))
