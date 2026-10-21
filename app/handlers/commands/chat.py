import asyncio

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from app.handlers.permissions import require_authorized

# Old chatgpt_service default system prompt — kept in the command,
# not the provider, so it stays provider-agnostic.
DEFAULT_SYSTEM_PROMPT = "你是阿尔忒弥斯，是群组的月神，并且你能回答群组成员的话。"


async def chat_command(update: Update, context: CallbackContext):
    """
    处理 /chat 命令，与 LLM 进行交互。
    Handles the /chat command to interact with the LLM.
    """
    if not await require_authorized(update, context):
        return

    llm_service = context.bot_data.get("llm_service")
    if not llm_service:
        await update.message.reply_text("LLM 服务未配置，请联系管理员。")
        return

    if not context.args:
        await update.message.reply_text("请在 /chat 命令后输入您想说的话。")
        return

    prompt = " ".join(context.args)
    response = await asyncio.to_thread(llm_service.get_response, prompt, DEFAULT_SYSTEM_PROMPT)
    await update.message.reply_text(response)


def register(application):
    """
    注册 chat 命令处理器。
    Registers the chat command handler.
    """
    application.add_handler(CommandHandler("chat", chat_command))
