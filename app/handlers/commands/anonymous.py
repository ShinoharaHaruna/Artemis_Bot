from telegram.ext import CommandHandler
from app.core.config import GROUP_CHAT_ID, MASTER_ID


def admin_command(update, context):
    message = update.message
    if message.text is None:
        return
    if update.message.from_user.id != MASTER_ID:
        return
    context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=message.text.replace("/admin ", ""),
        parse_mode="HTML",
    )


def anonymous_command(update, context):
    message = update.message
    if message.text is None:
        return
    if update.effective_chat.id == GROUP_CHAT_ID:
        context.bot.delete_message(
            chat_id=update.effective_chat.id, message_id=update.message.message_id
        )
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='私聊月神才可以匿名哦~发送"/anonymous + 消息"，即可匿名发送消息',
        )
        return
    context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=f"匿名消息：{message.text.replace('/anonymous ', '')}",
    )


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("anonymous", anonymous_command))
    dispatcher.add_handler(CommandHandler("admin", admin_command))
