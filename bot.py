import yaml
import pytz
import modules.tricks as tricks
from datetime import datetime, time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from modules.drinkwater import send_drink_water_message
from modules.chatgpt import chat_command
from modules.dalle import image_generator
from modules.weather import (
    handle_weather,
    handle_forecast,
    weather_command,
    forecast_command,
)
from modules.random_pixiv import handle_random_pixiv
from modules.offWork import send_off_work_message
from modules.onWork import send_on_work_message
from modules.setu import setu_command
from modules.answerbook import answer_command
from modules.scholar import scholar_command
from modules.food import food_command
from modules.anonymous import admin_command, anonymous_command
from modules.tarot import tarot_command
from modules.fortune import tell_fortune
from modules.remake import remake_command 
from modules.list_help import list_help


def load_config():
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
    return config


config = load_config()
TIMEZONE = config["Basic"]["TIMEZONE"]
API_TOKEN = config["Basic"]["API_TOKEN"]
GROUP_CHAT_ID = config["GroupChat"][0][0]
OPENAI_API_KEY = config["OpenAI"]["OPENAI_API_KEY"]
WEATHER_LAT = config["Weather"]["LAT"]
WEATHER_LON = config["Weather"]["LON"]
WEATHER_API_KEY = config["Weather"]["API_KEY"]
MASTER_ID = config["Basic"]["MASTER_ID"]


timerOn = False
timerA = datetime.now()
timerB = datetime.now()


def send_reminder(context):
    send_drink_water_message(context.bot, GROUP_CHAT_ID)


def offWork_reminder(context):
    send_off_work_message(context.bot, GROUP_CHAT_ID, WEATHER_API_KEY, TIMEZONE)


def onWork_reminder(context):
    send_on_work_message(context.bot, GROUP_CHAT_ID, WEATHER_API_KEY)


def private_message_handler(update, context):
    user = update.message.from_user
    message = update.message

    if message.text is not None:
        if message.text.startswith("/random_pixiv"):
            handle_random_pixiv(context.bot, update)
        elif message.text.startswith("/setu"):
            setu_command(context, update)
        elif message.text.startswith("/answer"):
            answer_command(context, update)
        elif message.text.startswith("/scholar"):
            scholar_command(context, update)
        elif message.text.startswith("/help"):
            list_help(context, update)
        elif message.text.startswith("/weather"):
            handle_weather(
                context.bot,
                update.effective_chat.id,
                WEATHER_API_KEY,
                update.message.message_id,
            )
        elif message.text.startswith("/forecast"):
            handle_forecast(
                context.bot,
                user.id,
                WEATHER_API_KEY,
                TIMEZONE,
                update.message.message_id,
            )


def schedule_reminders(job_queue):
    # Define the times for the reminders
    reminder_times = [
        time(hour=8, minute=50),
        time(hour=9, minute=50),
        time(hour=11),
        time(hour=12, minute=30),
        time(hour=14, minute=50),
        time(hour=15, minute=50),
        time(hour=17),
        time(hour=18, minute=30),
        time(hour=20, minute=50),
    ]

    OnWorkTime = time(hour=7, minute=30)
    OffWorkTime = time(hour=22, minute=30)

    timezone = pytz.timezone(TIMEZONE)
    reminder_times_utc = []
    for reminder_time in reminder_times:
        current_time = datetime.now().date()
        dt_with_tz = timezone.localize(datetime.combine(current_time, reminder_time))
        dt_utc = dt_with_tz.astimezone(pytz.utc)
        reminder_time_utc = dt_utc.time()
        reminder_times_utc.append(reminder_time_utc)
    OnWorkTime_utc = (
        timezone.localize(datetime.combine(current_time, OnWorkTime))
        .astimezone(pytz.utc)
        .time()
    )
    OffWorkTime_utc = (
        timezone.localize(datetime.combine(current_time, OffWorkTime))
        .astimezone(pytz.utc)
        .time()
    )

    # Schedule the reminders at the specified times
    for reminder_time_utc in reminder_times_utc:
        job_queue.run_daily(
            send_reminder, reminder_time_utc, days=(0, 1, 2, 3, 4, 5, 6)
        )
    job_queue.run_daily(offWork_reminder, OffWorkTime_utc, days=(0, 1, 2, 3, 4))
    job_queue.run_daily(onWork_reminder, OnWorkTime_utc, days=(0, 1, 2, 3, 4))


def timer_handler(update, context):
    global timerOn
    global timerA
    global timerB
    if timerOn:
        timerB = datetime.now()
        timerOn = False
        delta = timerB - timerA
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="计时结束！\n用时：{}秒".format(delta.seconds),
        )
    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="计时开始！"
        )
        timerA = datetime.now()
        timerOn = True

def main():
    # Set up the bot's updater
    updater = Updater(token=API_TOKEN, use_context=True)
    job_queue = updater.job_queue

    # Schedule the reminders
    schedule_reminders(job_queue)

    # 获取Dispatcher对象
    dispatcher = updater.dispatcher

    # 响应群聊消息
    dispatcher.add_handler(CommandHandler("chat", chat_command))
    dispatcher.add_handler(CommandHandler("draw", image_generator))
    dispatcher.add_handler(CommandHandler("weather", weather_command))
    dispatcher.add_handler(CommandHandler("forecast", forecast_command))
    dispatcher.add_handler(CommandHandler("random_pixiv", handle_random_pixiv))
    dispatcher.add_handler(CommandHandler("setu", setu_command))
    dispatcher.add_handler(CommandHandler("answer", answer_command))
    dispatcher.add_handler(CommandHandler("scholar", scholar_command))
    dispatcher.add_handler(CommandHandler("food", food_command))
    dispatcher.add_handler(CommandHandler("anonymous", anonymous_command))
    dispatcher.add_handler(CommandHandler("admin", admin_command))
    dispatcher.add_handler(CommandHandler("tarot", tarot_command))
    dispatcher.add_handler(CommandHandler("suangua", tell_fortune))
    dispatcher.add_handler(CommandHandler("timer", timer_handler))
    dispatcher.add_handler(CommandHandler("remake", remake_command))
    dispatcher.add_handler(CommandHandler("help", list_help))

    # 响应特定消息
    dispatcher.add_handler(MessageHandler(Filters.text, tricks.handle_message))

    # 响应私聊
    dispatcher.add_handler(MessageHandler(Filters.private, private_message_handler))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    print("Bot started at", datetime.now(pytz.timezone(TIMEZONE)))
    main()
