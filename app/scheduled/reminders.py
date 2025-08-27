import pytz
from datetime import datetime, time
from telegram.ext import JobQueue

from app.core.config import GROUP_CHAT_ID, TIMEZONE, WEATHER_API_KEY
from modules.drinkwater import send_drink_water_message
from modules.offWork import send_off_work_message
from modules.onWork import send_on_work_message


def send_reminder(context):
    """
    发送喝水提醒。
    Sends a drink water reminder.
    """
    send_drink_water_message(context.bot, GROUP_CHAT_ID)


def off_work_reminder(context):
    """
    发送下班提醒。
    Sends an off-work reminder.
    """
    send_off_work_message(context.bot, GROUP_CHAT_ID, WEATHER_API_KEY, TIMEZONE)


def on_work_reminder(context):
    """
    发送上班提醒。
    Sends an on-work reminder.
    """
    send_on_work_message(context.bot, GROUP_CHAT_ID, WEATHER_API_KEY)


def schedule_reminders(job_queue: JobQueue):
    """
    安排所有定时提醒任务。
    Schedules all reminder jobs.

    Args:
        job_queue (JobQueue): a job queue instance from the updater.
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
