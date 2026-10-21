from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

# Old chatgpt_service default system prompt — kept in the command,
# not the provider, so it stays provider-agnostic.
DEFAULT_SYSTEM_PROMPT = "你是阿尔忒弥斯，是群组的月神，并且你能回答群组成员的话。"


def chat_command(update: Update, context: CallbackContext):
    """
    处理 /chat 命令，与 LLM 进行交互。
    Handles the /chat command to interact with the LLM.
    """
    llm_service = context.bot_data.get("llm_service")
    if not llm_service:
        update.message.reply_text("LLM 服务未配置，请联系管理员。")
        return

    if not context.args:
        update.message.reply_text("请在 /chat 命令后输入您想说的话。")
        return

    prompt = " ".join(context.args)
    response = llm_service.get_response(prompt, system_prompt=DEFAULT_SYSTEM_PROMPT)
    update.message.reply_text(response)


def register(dispatcher):
    """
    注册 chat 命令处理器。
    Registers the chat command handler.
    """
    dispatcher.add_handler(CommandHandler("chat", chat_command))
