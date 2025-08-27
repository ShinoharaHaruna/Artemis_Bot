from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from datetime import datetime
import pytz
from app.core.config import TIMEZONE


def reminder_callback(context: CallbackContext):
    """
    Callback function for the reminder job. Sends the reminder message.
    回调函数，用于提醒任务。发送提醒消息。
    """
    job = context.job
    chat_id = job.context["chat_id"]
    message = job.context["message"]
    context.bot.send_message(chat_id=chat_id, text=f"【提醒】\n{message}")


def set_reminder_command(update: Update, context: CallbackContext):
    """
    Sets a reminder for the user.
    为用户设置一个提醒。
    """
    # 仅限私聊 / Private chat only
    if update.message.chat.type != "private":
        update.message.reply_text("此命令仅限私聊使用。")
        return

    chat_id = update.effective_chat.id

    try:
        # 解析参数 / Parse arguments
        parts = context.args
        if len(parts) < 2:
            update.message.reply_text("使用方法: /reminder YYYYMMDDHHMM <提醒内容>")
            return

        datetime_str = parts[0]
        reminder_message = " ".join(parts[1:])

        # 验证和转换日期时间 / Validate and convert datetime
        try:
            # The format is YYYYMMDDHHMM
            reminder_time_naive = datetime.strptime(datetime_str, "%Y%m%d%H%M")
            # Localize the time
            local_tz = pytz.timezone(TIMEZONE)
            reminder_time = local_tz.localize(reminder_time_naive)
        except ValueError:
            update.message.reply_text("日期时间格式错误。请使用 YYYYMMDDHHMM 格式。")
            return

        # 检查时间是否在未来 / Check if the time is in the future
        now = datetime.now(pytz.timezone(TIMEZONE))
        if reminder_time <= now:
            update.message.reply_text("提醒时间必须在未来。")
            return

        # 安排任务 / Schedule the job
        context.job_queue.run_once(
            reminder_callback,
            reminder_time,
            context={"chat_id": chat_id, "message": reminder_message},
            name=f"reminder_{chat_id}_{datetime_str}",
        )

        update.message.reply_text(
            f"好的，我会在 {reminder_time.strftime('%Y-%m-%d %H:%M:%S %Z')} 提醒你：\n{reminder_message}"
        )

    except (IndexError, ValueError) as e:
        update.message.reply_text(f"设置提醒时出错: {e}\n请检查你的命令格式。")


def register(dispatcher):
    """
    Registers the /reminder command handler.
    注册 /reminder 命令处理器。
    """
    dispatcher.add_handler(CommandHandler("reminder", set_reminder_command))
