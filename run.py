import pytz
from datetime import datetime
from app.core.bot import run_bot
from app.core.config import TIMEZONE, OPENAI_API_KEY
from app.services.tarot_service import TarotService
from app.services.chatgpt_service import ChatGPTService
from app.services.answerbook_service import AnswerbookService


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

    # 创建 bot_data 字典来存储服务
    # Create bot_data dictionary to store services
    bot_data = {
        "tarot_service": tarot_service,
        "chatgpt_service": chatgpt_service,
        "answerbook_service": answerbook_service,
    }

    # 运行 Bot 并传递 bot_data
    # Run the Bot and pass bot_data
    run_bot(bot_data)


if __name__ == "__main__":
    main()
