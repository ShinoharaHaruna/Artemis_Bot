import logging
import traceback
import html
import json
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from app.core.config import MASTER_ID

# 设置日志记录
# Setup logging
logger = logging.getLogger(__name__)


def error_handler(update: object, context: CallbackContext) -> None:
    """
    全局错误处理器。捕获所有未处理的异常，并向开发者发送通知。
    Global error handler. Catches all unhandled exceptions and sends a notification to the developer.
    """
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # 格式化 traceback
    # Format the traceback
    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)

    # 准备要发送给开发者的消息
    # Prepare the message for the developer
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        f"</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    # 将消息发送给开发者，如果消息太长则分段发送
    # Send the message to the developer, splitting it if it's too long
    if MASTER_ID:
        for i in range(0, len(message), 4096):
            context.bot.send_message(
                chat_id=MASTER_ID, text=message[i : i + 4096], parse_mode=ParseMode.HTML
            )


def register(dispatcher):
    """
    注册错误处理器。
    Registers the error handler.
    """
    dispatcher.add_error_handler(error_handler)
