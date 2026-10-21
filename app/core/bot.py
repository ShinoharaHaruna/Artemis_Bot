import logging
from datetime import datetime

import pytz
from telegram.ext import Application

from app.core.config import API_TOKEN, MASTER_ID, TIMEZONE
from app.handlers.commands import register_all_commands
from app.handlers.error import register as register_error_handler
from app.handlers.messages import register_all_message_handlers
from app.scheduled.reminders import schedule_reminders

logger = logging.getLogger(__name__)


async def _post_init(application: Application) -> None:
    """
    Application 初始化后发送启动成功消息给 master。
    Sends the startup success message to master after the Application is initialized.
    """
    try:
        start_time = datetime.now(pytz.timezone(TIMEZONE))
        await application.bot.send_message(
            chat_id=MASTER_ID,
            text=f"✅ Bot 启动成功\n启动时间: {start_time.strftime('%Y-%m-%d %H:%M:%S %Z')}",
        )
    except Exception as e:
        logger.error(f"Failed to send startup message to master: {e}")


def run_bot(bot_data=None):
    """
    初始化并运行 Bot。
    Initializes and runs the Bot.
    """
    # 初始化 Application
    # Initialize the Application
    app = Application.builder().token(API_TOKEN).post_init(_post_init).build()

    # 如果提供了 bot_data，则注入服务
    # If bot_data is provided, inject the services
    if bot_data:
        app.bot_data.update(bot_data)

    # 注册所有命令和消息处理器
    # Register all command and message handlers
    register_all_commands(app)
    register_all_message_handlers(app)

    # 注册错误处理器
    # Register error handler
    register_error_handler(app)

    # 安排定时任务（job-queue extra 已安装，job_queue 必存在）
    # Schedule jobs (job-queue extra installed, so job_queue always exists)
    if app.job_queue is None:
        raise RuntimeError("JobQueue is not available — install python-telegram-bot[job-queue]")
    schedule_reminders(app.job_queue)

    # 启动 Bot（阻塞直到收到停止信号，并自行处理信号）
    # Start the Bot (blocks until a stop signal, which it handles itself)
    app.run_polling()
