import pytz
from datetime import datetime
from app.core.bot import run_bot
from app.core.config import TIMEZONE

if __name__ == "__main__":
    # 设置并打印启动时间
    # Set and print the start time
    start_time = datetime.now(pytz.timezone(TIMEZONE))
    print(f"Bot started at {start_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # 运行 Bot
    # Run the Bot
    run_bot()
