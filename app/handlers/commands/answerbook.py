from telegram.ext import CommandHandler


def answer_command(update, context):
    """
    处理 /answer 命令，从答案之书中获取一个答案。
    Handles the /answer command, getting an answer from the answer book.
    """
    answerbook_service = context.bot_data.get("answerbook_service")

    if not answerbook_service:
        update.message.reply_text("答案之书服务未初始化，请联系管理员。")
        return

    answer = answerbook_service.get_random_answer()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=answer,
        reply_to_message_id=update.message.message_id,
    )


def register(dispatcher):
    """
    注册 /answer 命令处理器。
    Registers the /answer command handler.
    """
    dispatcher.add_handler(CommandHandler("answer", answer_command))
