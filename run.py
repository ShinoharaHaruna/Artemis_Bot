import pytz
import signal
import threading
from datetime import datetime
from app.core.bot import run_bot
from app.core.web import web_app
from app.core.config import TIMEZONE, OPENAI_API_KEY, MASTER_ID, API_TOKEN
from app.services.tarot_service import TarotService
from app.services.chatgpt_service import ChatGPTService
from app.services.answerbook_service import AnswerbookService
from app.services.one_word_service import OneWordService
from app.services.canned_response_service import CannedResponseService
from app.services.setu_service import SetuService
from app.services.weather_service import WeatherService
from app.services.off_work_service import OffWorkService
from app.services.drink_water_service import DrinkWaterService
import telegram


def send_message_to_master(message):
    """
    发送消息给 master。
    Send a message to the master.
    """
    try:
        bot = telegram.Bot(token=API_TOKEN)
        bot.send_message(chat_id=MASTER_ID, text=message)
    except Exception as e:
        print(f"Failed to send message to master: {e}")


def main():
    """启动 Bot 并注入服务。"""
    # 设置并打印启动时间
    # Set and print the start time
    start_time = datetime.now(pytz.timezone(TIMEZONE))
    print(f"Bot started at {start_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # 初始化服务
    # Initialize services
    tarot_service = TarotService()
    chatgpt_service = ChatGPTService(api_key=OPENAI_API_KEY)
    answerbook_service = AnswerbookService()
    one_word_service = OneWordService()
    canned_response_service = CannedResponseService()
    setu_service = SetuService()
    weather_service = WeatherService()
    off_work_service = OffWorkService(weather_service=weather_service)
    drink_water_service = DrinkWaterService()

    # 创建 bot_data 字典来存储服务
    # Create bot_data dictionary to store services
    bot_data = {
        "tarot_service": tarot_service,
        "chatgpt_service": chatgpt_service,
        "answerbook_service": answerbook_service,
        "one_word_service": one_word_service,
        "canned_response_service": canned_response_service,
        "setu_service": setu_service,
        "weather_service": weather_service,
        "off_work_service": off_work_service,
        "drink_water_service": drink_water_service,
    }

    # 在一个单独的线程中运行 Flask 应用
    # Run the Flask app in a separate thread
    web_thread = threading.Thread(target=lambda: web_app.run(host="0.0.0.0", port=8080))
    web_thread.daemon = True
    web_thread.start()

    # 设置信号处理器用于优雅退出
    # Set up signal handler for graceful shutdown
    def signal_handler(sig, frame):
        print("\nReceived shutdown signal, notifying master...")
        shutdown_time = datetime.now(pytz.timezone(TIMEZONE))
        send_message_to_master(
            f"🛑 Bot 正在关闭\n"
            f"关闭时间: {shutdown_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        )
        exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # 运行 Bot 并传递 bot_data
    # Run the Bot and pass bot_data
    run_bot(bot_data)


if __name__ == "__main__":
    main()
