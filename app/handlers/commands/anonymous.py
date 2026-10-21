from telegram.ext import CommandHandler

from app.core.config import GROUP_CHAT_ID
from app.handlers.permissions import require_master


def admin_command(update, context):
    """处理 /admin 命令。"""
    # handle /admin command
    message = update.message
    if message.text is None:
        return
    if not require_master(update, silent=True):
        return
    if not context.args:
        message.reply_text("使用方法: /admin <消息>")
        return
    context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=" ".join(context.args),
        parse_mode="HTML",
    )


def anonymous_command(update, context):
    """处理 /anonymous 命令。"""
    # handle /anonymous command
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
    if not context.args:
        message.reply_text("使用方法: /anonymous <消息>")
        return
    context.bot.send_message(
        chat_id=GROUP_CHAT_ID,
        text=f"匿名消息：{' '.join(context.args)}",
    )


def register(dispatcher):
    dispatcher.add_handler(CommandHandler("anonymous", anonymous_command))
    dispatcher.add_handler(CommandHandler("admin", admin_command))
