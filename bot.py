import datetime
import yaml
from datetime import time
from telegram.ext import Updater, JobQueue, CommandHandler
from modules.drinkwater import send_drink_water_message
from modules.chatgpt import handle_message


def load_config():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


config = load_config()
API_TOKEN = config["API_TOKEN"]
GROUP_CHAT_ID = config["GROUP_CHAT_ID"]
OPENAI_API_KEY = config["OPENAI_API_KEY"]


def send_reminder(context):
    job = context.job
    send_drink_water_message(context.bot, GROUP_CHAT_ID)


def chat_command(update, context):
    message = " ".join(context.args)  # 获取命令后的字符串作为message
    handle_message(context.bot, GROUP_CHAT_ID, message, OPENAI_API_KEY)  # 调用处理消息的函数


def schedule_reminders(job_queue):
    # Define the times for the reminders
    reminder_times = [
        time(hour=0, minute=50),  # 08:50
        time(hour=1, minute=50),  # 09:50
        time(hour=3),  # 11:00
        time(hour=4, minute=30),  # 12:30
        time(hour=6, minute=50),  # 14:50
        time(hour=7, minute=50),  # 15:50
        time(hour=9),  # 17:00
        time(hour=10, minute=30),  # 18:30
        time(hour=12, minute=50),  # 20:50
    ]

    # Schedule the reminders at the specified times
    for reminder_time in reminder_times:
        job_queue.run_daily(send_reminder, reminder_time, days=(0, 1, 2, 3, 4, 5, 6))


def list_help(update, context):
    help_message = """
    <b>月神的温馨提示：</b>
    <b>1. 喝水提醒</b>
    月神会在每天的以下时间提醒大家喝水：
    08:50, 09:50, 11:00, 12:30, 14:50, 15:50, 17:00, 18:30, 20:50
    <b>2. 聊天功能</b>
    月神可以和大家聊天哦！只需要在群组中输入/chat+空格+你想说的话，月神就会回复你啦！
    例如：/chat 你好呀！
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=help_message,
        parse_mode="HTML",
    )


def main():
    # Set up the bot's updater
    updater = Updater(token=API_TOKEN, use_context=True)
    job_queue = updater.job_queue

    # Schedule the reminders
    schedule_reminders(job_queue)

    # 获取Dispatcher对象
    dispatcher = updater.dispatcher

    # 将chat_command函数与/chat命令绑定
    dispatcher.add_handler(CommandHandler("chat", chat_command))

    dispatcher.add_handler(CommandHandler("help", list_help))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    print("Bot started at", datetime.datetime.now())
    main()
