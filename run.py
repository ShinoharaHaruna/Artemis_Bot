import asyncio
import atexit
import logging
import threading
from datetime import datetime

import pytz
import telegram

from app.core.bot import run_bot
from app.core.config import API_TOKEN, MASTER_ID, TIMEZONE
from app.core.web import web_app
from app.services.answerbook_service import AnswerbookService
from app.services.canned_response_service import CannedResponseService
from app.services.drink_water_service import DrinkWaterService
from app.services.llm import create_llm_service
from app.services.off_work_service import OffWorkService
from app.services.one_word_service import OneWordService
from app.services.setu_service import SetuService
from app.services.tarot_service import TarotService
from app.services.weather_service import WeatherService

logger = logging.getLogger(__name__)


def send_message_to_master(message):
    """
    发送消息给 master。
    Send a message to the master.
    """
    try:
        bot = telegram.Bot(token=API_TOKEN)
        asyncio.run(bot.send_message(chat_id=MASTER_ID, text=message))
    except Exception as e:
        logger.error(f"Failed to send message to master: {e}")


def main():
    """启动 Bot 并注入服务。"""
    # 配置日志 / Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # 设置并打印启动时间
    # Set and print the start time
    start_time = datetime.now(pytz.timezone(TIMEZONE))
    logger.info(f"Bot started at {start_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # 初始化服务
    # Initialize services
    answerbook_service = AnswerbookService()
    one_word_service = OneWordService()
    canned_response_service = CannedResponseService()
    setu_service = SetuService()
    weather_service = WeatherService()
    off_work_service = OffWorkService(weather_service=weather_service)
    drink_water_service = DrinkWaterService()
    tarot_service = TarotService()
    # 未配置 LLM 时返回 None，相关命令会提示未配置 / None when LLM is not configured
    llm_service = create_llm_service()

    # 创建 bot_data 字典来存储服务
    # Create bot_data dictionary to store services
    bot_data = {
        "answerbook_service": answerbook_service,
        "one_word_service": one_word_service,
        "canned_response_service": canned_response_service,
        "setu_service": setu_service,
        "weather_service": weather_service,
        "off_work_service": off_work_service,
        "drink_water_service": drink_water_service,
        "tarot_service": tarot_service,
        "llm_service": llm_service,
    }

    # 在一个单独的线程中运行 Flask 应用
    # Run the Flask app in a separate thread
    web_thread = threading.Thread(
        target=lambda: web_app.run(
            host="0.0.0.0",
            port=8080,
            debug=False,
            use_reloader=False,
        )
    )
    web_thread.daemon = True
    web_thread.start()

    # PTB 的 updater.idle() 会注册自己的信号处理器并覆盖我们设置的，
    # 因此改用 atexit：优雅停止完成后、解释器退出时通知 master。
    # PTB's updater.idle() registers its own signal handlers and would
    # overwrite ours, so notify the master via atexit instead — it runs
    # after the graceful stop completes, at interpreter exit.
    def _notify_shutdown():
        logger.info("Bot is shutting down, notifying master...")
        shutdown_time = datetime.now(pytz.timezone(TIMEZONE))
        send_message_to_master(
            f"🛑 Bot 正在关闭\n"
            f"关闭时间: {shutdown_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        )

    atexit.register(_notify_shutdown)

    # 运行 Bot 并传递 bot_data
    # Run the Bot and pass bot_data
    run_bot(bot_data)


if __name__ == "__main__":
    main()
