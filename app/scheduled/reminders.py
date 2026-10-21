import asyncio
from datetime import time

import pytz
from telegram.constants import ParseMode
from telegram.ext import JobQueue

from app.core.config import GROUP_CHAT_ID, TIMEZONE


async def send_reminder(context):
    """
    发送喝水提醒。
    Sends a drink water reminder.
    """
    drink_water_service = context.bot_data.get("drink_water_service")
    if not drink_water_service:
        # 可以选择在这里记录一个错误，但为了简单起见，我们暂时跳过
        # You could log an error here, but for simplicity, we'll skip it for now
        return
    # 纯字符串拼接，无 I/O，无需 to_thread / Pure string building, no I/O
    message = drink_water_service.get_drink_water_message()
    await context.bot.send_message(
        chat_id=GROUP_CHAT_ID, text=message, parse_mode=ParseMode.HTML
    )


async def off_work_reminder(context):
    """
    发送下班提醒。
    Sends an off-work reminder.
    """
    off_work_service = context.bot_data.get("off_work_service")
    if not off_work_service:
        return
    # 内部会调用天气 API（网络 I/O），放到线程执行 / Network I/O via weather API → to_thread
    message = await asyncio.to_thread(off_work_service.get_off_work_message)
    await context.bot.send_message(
        chat_id=GROUP_CHAT_ID, text=message, parse_mode=ParseMode.HTML
    )


async def on_work_reminder(context):
    """
    发送上班提醒。
    Sends an on-work reminder.
    """
    one_word_service = context.bot_data.get("one_word_service")
    if one_word_service:
        # requests 网络 I/O → to_thread / requests network I/O → to_thread
        quote = await asyncio.to_thread(one_word_service.get_one_word)
        text = f"新的一天，新的开始！上班加油！\n\n今日一言：{quote}"
    else:
        text = "新的一天，新的开始！上班加油！"

    await context.bot.send_message(chat_id=GROUP_CHAT_ID, text=text)


def schedule_reminders(job_queue: JobQueue):
    """
    安排所有定时提醒任务。
    Schedules all reminder jobs.

    Args:
        job_queue (JobQueue): a job queue instance from the application.
    """
    tz = pytz.timezone(TIMEZONE)

    # 定义喝水提醒时间 / Define reminder times
    reminder_times = [
        time(hour=8, minute=50, tzinfo=tz),
        time(hour=9, minute=50, tzinfo=tz),
        time(hour=11, tzinfo=tz),
        time(hour=12, minute=30, tzinfo=tz),
        time(hour=14, minute=50, tzinfo=tz),
        time(hour=15, minute=50, tzinfo=tz),
        time(hour=17, tzinfo=tz),
        time(hour=18, minute=30, tzinfo=tz),
        time(hour=20, minute=50, tzinfo=tz),
    ]

    # 定义上下班提醒时间 / Define on/off work times
    on_work_time = time(hour=7, minute=30, tzinfo=tz)
    off_work_time = time(hour=22, minute=30, tzinfo=tz)

    # 安排喝水提醒 / Schedule drink water reminders
    for t in reminder_times:
        job_queue.run_daily(send_reminder, t, days=tuple(range(7)))

    # 安排上下班提醒 (周一至周五) / Schedule on/off work reminders (Mon-Fri)
    job_queue.run_daily(on_work_reminder, on_work_time, days=tuple(range(5)))
    job_queue.run_daily(off_work_reminder, off_work_time, days=tuple(range(5)))
