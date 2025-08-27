from telegram.ext import Updater
from app.core.config import API_TOKEN
from app.handlers.commands import register_all_commands
from app.handlers.messages import register_all_message_handlers
from app.handlers.error import register as register_error_handler
from app.scheduled.reminders import schedule_reminders


def run_bot(bot_data=None):
    """
    初始化并运行 Bot。
    Initializes and runs the Bot.
    """
    # 初始化 Updater 和 Dispatcher
    # Initialize Updater and Dispatcher
    updater = Updater(token=API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # 如果提供了 bot_data，则注入服务
    # If bot_data is provided, inject the services
    if bot_data:
        dispatcher.bot_data.update(bot_data)

    # 注册所有命令和消息处理器
    # Register all command and message handlers
    register_all_commands(dispatcher)
    register_all_message_handlers(dispatcher)

    # 注册错误处理器
    # Register error handler
    register_error_handler(dispatcher)

    # 安排定时任务
    # Schedule jobs
    schedule_reminders(updater.job_queue)

    # 启动 Bot
    # Start the Bot
    updater.start_polling()
    updater.idle()
