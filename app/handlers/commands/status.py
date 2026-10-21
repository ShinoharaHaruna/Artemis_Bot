from datetime import datetime

import pytz
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from app.core.config import TIMEZONE
from app.handlers.permissions import require_master

# 任务标签映射，便于展示 / Job label mapping for better display
JOB_LABEL_OVERRIDES = {
    "send_reminder": "喝水提醒",
    "on_work_reminder": "上班提醒",
    "off_work_reminder": "下班提醒",
    "send_tutoring_reminder": "家教提醒",
    "reminder_callback": "自定义提醒",
}


def _localize_datetime(dt: datetime | None, tz: pytz.timezone) -> datetime | None:
    """
    将 datetime 对象转化为目标时区。
    Normalize datetime objects into target timezone.
    """
    if dt is None:
        return None
    if dt.tzinfo is None:
        # 处理 naive datetime，假定为本地时间 / Handle naive datetime as local time
        return tz.localize(dt)
    return dt.astimezone(tz)


def _format_timedelta(delta: datetime) -> str:
    """
    将时间差转为可读的中文描述。
    Format timedelta into a human readable Chinese string.
    """
    if delta.total_seconds() < 0:
        return "时间未就绪"
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if hours:
        parts.append(f"{hours}小时")
    if minutes:
        parts.append(f"{minutes}分钟")
    if seconds or not parts:
        parts.append(f"{seconds}秒")
    return "".join(parts)


def _build_timer_section(context: CallbackContext, tz: pytz.timezone) -> str:
    """
    构造计时器状态文本。
    Build status text for timer feature.
    """
    timer_on = context.chat_data.get("timer_on", False)
    if not timer_on:
        return "- 状态：已关闭"

    start_time = context.chat_data.get("timer_start_time")
    localized_start = _localize_datetime(start_time, tz) if start_time else None

    if localized_start:
        now = datetime.now(tz)
        elapsed = now - localized_start
        formatted_elapsed = _format_timedelta(elapsed)
        start_str = localized_start.strftime("%Y-%m-%d %H:%M:%S %Z")
        return (
            "- 状态：运行中\n"
            f"- 开始时间：{start_str}\n"
            f"- 已运行：{formatted_elapsed}"
        )
    return "- 状态：运行中 (开始时间缺失)"


def _derive_job_label(job) -> str:
    """
    根据任务信息获取展示名称。
    Derive a display label for the job.
    """
    name = getattr(job, "name", None)
    callback = getattr(job, "callback", None)
    callback_name = getattr(callback, "__name__", None)

    if name and name.startswith("reminder_"):
        return "自定义提醒"
    if name and name in JOB_LABEL_OVERRIDES:
        return JOB_LABEL_OVERRIDES[name]
    if callback_name and callback_name in JOB_LABEL_OVERRIDES:
        return JOB_LABEL_OVERRIDES[callback_name]
    if name:
        return name
    if callback_name:
        return callback_name
    return "未命名任务"


def _build_jobs_section(context: CallbackContext, tz: pytz.timezone) -> str:
    """
    构造定时任务状态文本。
    Build status text for scheduled jobs.
    """
    jobs = context.job_queue.jobs() if context.job_queue else []
    if not jobs:
        return "- 暂无定时任务"

    lines = []
    max_t = datetime.max.replace(tzinfo=pytz.utc)
    for job in sorted(jobs, key=lambda j: getattr(j, "next_t", None) or max_t):
        label = _derive_job_label(job)
        next_run = getattr(job, "next_t", None)
        localized_next = _localize_datetime(next_run, tz)
        if localized_next:
            next_str = localized_next.strftime("%Y-%m-%d %H:%M:%S %Z")
        else:
            next_str = "未知时间"
        lines.append(f"- {label}：下一次 {next_str}")
    return "\n".join(lines)


async def status_handler(update: Update, context: CallbackContext):
    """
    处理 /status 命令，展示功能状态，仅限 MASTER 使用。
    Handle /status command, show feature status, restricted to MASTER.
    """
    if not await require_master(update):
        return

    tz = pytz.timezone(TIMEZONE)
    timer_section = _build_timer_section(context, tz)
    jobs_section = _build_jobs_section(context, tz)

    report = (
        "🔧 功能状态概览 / Feature Status Overview\n\n"
        "⏱ 计时器 / Timer\n"
        f"{timer_section}\n\n"
        "🕒 定时任务 / Scheduled Jobs\n"
        f"{jobs_section}"
    )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=report)


def register(application):
    """
    注册 /status 命令处理器。
    Register the /status command handler.
    """
    application.add_handler(CommandHandler("status", status_handler))
